"""Process judge agent outputs."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from debate_ops import frontmatter
from debate_ops import mermaid
from debate_ops.state import update_debate_state, read_debate_state


@dataclass
class ProcessResult:
    success: bool
    argument_id: str | list[str] | None = None
    score: float | list[float] | None = None
    rescored: list[str] | None = None
    errors: list[str] | None = None
    warnings: list[str] | None = None


def _parse_judge_output(output: str | dict) -> dict | ProcessResult:
    """Parse judge output from string or dict. Returns parsed dict or ProcessResult on error."""
    if isinstance(output, str):
        cleaned = re.sub(r'^```(?:json|yaml)?\s*|\s*```$', '', output.strip(), flags=re.MULTILINE)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            return ProcessResult(success=False, errors=[f"Invalid JSON: {e}"])
    return output


def _normalize_scores(data: dict) -> list[dict] | ProcessResult:
    """Normalize single or multiple score formats to unified list structure.

    Returns list of dicts with keys: argument_id, score, reasoning
    Or ProcessResult on error.
    """
    if 'scores' in data:
        # Multiple arguments format
        if not isinstance(data['scores'], list) or not data['scores']:
            return ProcessResult(success=False, errors=["'scores' must be non-empty list"])

        normalized = []
        for entry in data['scores']:
            if missing := {'argument_id', 'score', 'reasoning'} - set(entry.keys()):
                return ProcessResult(success=False, errors=[f"Score entry missing keys: {missing}"])

            if not (-1 <= entry['score'] <= 1):
                return ProcessResult(success=False, errors=[f"Score {entry['score']} for {entry['argument_id']} outside valid range [-1, 1]"])

            normalized.append(entry)

        # Zero-sum validation
        total = sum(entry['score'] for entry in normalized)
        if abs(total) > 0.01:  # Tolerance for floating point
            return ProcessResult(success=False, errors=[f"Scores must sum to 0 (got {total:.3f})"])

        return normalized
    else:
        # Single argument format
        if missing := {'argument_id', 'score', 'reasoning'} - set(data.keys()):
            return ProcessResult(success=False, errors=[f"Missing required keys: {missing}"])

        if not (-1 <= data['score'] <= 1):
            return ProcessResult(success=False, errors=[f"Score {data['score']} outside valid range [-1, 1]"])

        return [{'argument_id': data['argument_id'], 'score': data['score'], 'reasoning': data['reasoning']}]


def process_judge(debate: str, output: str | dict) -> ProcessResult:
    """Process judge output and update debate state."""
    warnings = []

    # Parse input
    data = _parse_judge_output(output)
    if isinstance(data, ProcessResult):  # Error case
        return data

    # Normalize to unified structure
    scores_normalized = _normalize_scores(data)
    if isinstance(scores_normalized, ProcessResult):  # Error case
        return scores_normalized

    # Record all primary scores
    debate_dir = Path.cwd() / debate
    scores_file = debate_dir / 'scores.json'

    arg_ids, score_values = [], []
    for entry in scores_normalized:
        _record_score(scores_file, entry['argument_id'], entry['score'], entry['reasoning'], triggered_by=None)
        arg_ids.append(entry['argument_id'])
        score_values.append(entry['score'])

    # Process rescores, update state, generate artifacts (unified flow)
    rescored = _process_rescores(scores_file, data.get('rescores', []), warnings, triggered_by_list=arg_ids)
    _update_cumulative_scores(debate, scores_file)
    mermaid.generate_graph(debate)
    _update_state_after_judgment(debate)

    # Return result (preserve single vs multiple structure for backward compatibility)
    return ProcessResult(
        success=True,
        argument_id=arg_ids if len(arg_ids) > 1 else arg_ids[0],
        score=score_values if len(score_values) > 1 else score_values[0],
        rescored=rescored or None,
        warnings=warnings or None
    )


def _process_rescores(
    scores_file: Path,
    rescores: list,
    warnings: list,
    triggered_by_list: list[str]
) -> list[str]:
    """Process rescores and return list of rescored argument IDs."""
    rescored = []

    for rescore in rescores:
        if not (rescore_id := rescore.get('argument_id')) or (new_score := rescore.get('new_score')) is None:
            warnings.append(f"Incomplete rescore entry: {rescore}")
            continue

        old_score = rescore.get('old_score')
        rescore_reasoning = rescore.get('reasoning', '')

        # Validate rescore is an adjustment (delta), not absolute score
        if old_score is not None:
            delta = new_score - old_score
            if not (-0.5 <= delta <= 0.5):
                warnings.append(f"Rescore delta for {rescore_id} is {delta:.3f}, outside valid range [-0.5, 0.5]")
                continue

        # For rescores triggered by multiple arguments, use first one
        triggered_by = triggered_by_list[0] if triggered_by_list else None

        _record_score(
            scores_file, rescore_id, new_score, rescore_reasoning,
            triggered_by=triggered_by, previous_score=old_score
        )
        rescored.append(rescore_id)

    return rescored


def _update_state_after_judgment(debate: str) -> None:
    """Update debate state after judgment completes."""
    state = read_debate_state(debate)
    update_debate_state(
        debate,
        current_phase='awaiting_arguments',
        current_exchange=state['current_exchange'] + 1
    )


def _record_score(
    file: Path,
    arg_id: str,
    score: float,
    reasoning: str,
    triggered_by: str | None = None,
    previous_score: float | None = None
) -> None:
    """Record a score or rescore in the argument-centric structure."""
    # Load existing data or initialize
    if file.exists():
        with open(file) as f:
            data = json.load(f)
    else:
        data = {}

    # Ensure argument entry exists
    if arg_id not in data:
        data[arg_id] = {
            'current_score': score,
            'history': []
        }

    # Build history entry
    entry = {
        'score': score,
        'reasoning': reasoning,
        'scored_at': datetime.now(timezone.utc).isoformat()
    }

    # If this is a rescore (has triggered_by), add rescore fields
    if triggered_by:
        entry['triggered_by'] = triggered_by
        if previous_score is not None:
            entry['previous_score'] = previous_score
            entry['diff'] = round(score - previous_score, 3)

    # Append to history and update current score
    data[arg_id]['history'].append(entry)
    data[arg_id]['current_score'] = score

    # Save
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)


def _update_cumulative_scores(debate: str, scores_file: Path) -> None:
    """Update cumulative scores in debate.md frontmatter (zero-sum tug-of-war)."""
    if not scores_file.exists():
        return

    with open(scores_file) as f:
        data = json.load(f)

    # Extract current scores
    prop_scores = [arg_data['current_score'] for arg_id, arg_data in data.items() if arg_id.startswith('prop_')]
    opp_scores = [arg_data['current_score'] for arg_id, arg_data in data.items() if arg_id.startswith('opp_')]

    # Zero-sum tug-of-war: sum all scores for each side
    prop_total = round(sum(prop_scores), 3) if prop_scores else 0
    opp_total = round(sum(opp_scores), 3) if opp_scores else 0

    doc = frontmatter.load(Path.cwd() / debate / 'debate.md')
    doc.metadata['cumulative_scores'] = {
        'proposition': {'total': prop_total, 'count': len(prop_scores)},
        'opposition': {'total': opp_total, 'count': len(opp_scores)}
    }
    frontmatter.dump(doc, Path.cwd() / debate / 'debate.md')
