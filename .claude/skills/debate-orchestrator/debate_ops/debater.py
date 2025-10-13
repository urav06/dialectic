"""Process debater agent outputs."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from debate_ops import frontmatter


@dataclass
class ProcessResult:
    success: bool
    argument_id: str | list[str] | None = None
    errors: list[str] | None = None
    warnings: list[str] | None = None


REQUIRED_KEYS = {'title', 'claim', 'grounds', 'warrant'}
OPTIONAL_KEYS = {'backing', 'qualifier', 'attacks', 'defends'}
VALID_KEYS = REQUIRED_KEYS | OPTIONAL_KEYS


def process_debater(
    debate: str,
    side: Literal['proposition', 'opposition'],
    exchange: int,
    output: str | dict | list
) -> ProcessResult:
    """Process debater output, handling both single arguments and lists of arguments."""

    # Parse input to get data structure
    if isinstance(output, str):
        cleaned = re.sub(r'^```(?:json|yaml)?\s*|\s*```$', '', output.strip(), flags=re.MULTILINE)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            return ProcessResult(success=False, errors=[f"Invalid JSON: {e}"])
    else:
        parsed = output

    # Determine if single argument or list of arguments
    if isinstance(parsed, list):
        # Multiple arguments (e.g., opening statements)
        if not parsed:
            return ProcessResult(success=False, errors=["Empty argument list"])

        all_warnings = []
        arg_ids = []

        for idx, arg_data in enumerate(parsed):
            result = _process_single_argument(
                debate=debate,
                side=side,
                exchange=exchange,
                data=arg_data,
                index=idx
            )

            if not result.success:
                return result  # Fail fast on any error

            arg_ids.append(result.argument_id)
            if result.warnings:
                all_warnings.extend(result.warnings)

        return ProcessResult(
            success=True,
            argument_id=arg_ids,
            warnings=all_warnings or None
        )
    else:
        # Single argument (standard case)
        result = _process_single_argument(
            debate=debate,
            side=side,
            exchange=exchange,
            data=parsed,
            index=None
        )

        if not result.success:
            return result

        return result


def _process_single_argument(
    debate: str,
    side: Literal['proposition', 'opposition'],
    exchange: int,
    data: dict,
    index: int | None = None
) -> ProcessResult:
    """Process a single argument and create its file. Does not update debate state."""
    warnings = []

    # Validate required keys
    if missing := REQUIRED_KEYS - set(data.keys()):
        return ProcessResult(success=False, errors=[f"Missing required keys: {missing}"])

    if extra := set(data.keys()) - VALID_KEYS:
        warnings.append(f"Unrecognized keys (ignored): {extra}")

    # Validate grounds
    if not isinstance(data['grounds'], list) or not data['grounds']:
        return ProcessResult(success=False, errors=["'grounds' must be non-empty list"])

    if not (1 <= len(data['grounds']) <= 3):
        return ProcessResult(success=False, errors=[f"'grounds' must contain 1-3 entries (found {len(data['grounds'])})"])

    required_ground_keys = {'source', 'content', 'relevance'}
    for idx, ground in enumerate(data['grounds']):
        if missing_ground := required_ground_keys - set(ground.keys()):
            return ProcessResult(success=False, errors=[f"Ground {idx}: missing keys {missing_ground}"])

    # Validate attacks
    if len(attacks_list := data.get('attacks', [])) > 3:
        return ProcessResult(success=False, errors=[f"Too many attacks ({len(attacks_list)}). Maximum: 3"])

    # Validate defends
    if len(defends_list := data.get('defends', [])) > 2:
        return ProcessResult(success=False, errors=[f"Too many defends ({len(defends_list)}). Maximum: 2"])

    # Generate argument ID
    side_abbr = 'prop' if side == 'proposition' else 'opp'
    if index is not None:
        # Multiple arguments: prop_000a, prop_000b, prop_000c, etc.
        arg_id = f"{side_abbr}_{exchange:03d}{chr(ord('a') + index)}"
    else:
        # Single argument: prop_005
        arg_id = f"{side_abbr}_{exchange:03d}"

    # Create metadata
    metadata = {
        'id': arg_id,
        'side': side_abbr,
        'exchange': exchange,
        'title': data['title'],
        'claim': data['claim'],
        'attacks': [
            {'target_id': a['target_id'], 'type': a['attack_type']}
            for a in attacks_list if a.get('target_id')
        ],
        'defends': [
            {'target_id': d['target_id'], 'type': d['defense_type']}
            for d in data.get('defends', []) if d.get('target_id')
        ]
    }

    # Write argument file
    arg_file = Path.cwd() / debate / 'arguments' / f'{arg_id}.md'
    arg_file.parent.mkdir(parents=True, exist_ok=True)
    frontmatter.dump(frontmatter.Document(metadata, _format_argument_markdown(data)), arg_file)

    return ProcessResult(success=True, argument_id=arg_id, warnings=warnings or None)


def _format_argument_markdown(data: dict[str, Any]) -> str:
    sections = [f"## Claim\n\n{data['claim']}", "## Grounds"]

    # Updated to new ground structure
    for idx, g in enumerate(data['grounds'], 1):
        sections.extend([
            f"### {idx}. {g['source']}",
            f"> {g['content']}",
            f"**Relevance:** {g['relevance']}"
        ])

    sections.append(f"## Warrant\n\n{data['warrant']}")

    if backing := data.get('backing'):
        sections.append(f"## Backing\n\n{backing}")

    if qualifier := data.get('qualifier'):
        sections.append(f"## Qualifier\n\n{qualifier}")

    if attacks := data.get('attacks'):
        sections.append("## Attacks")
        for a in attacks:
            sections.extend([
                f"### Attacking {a.get('target_id', 'unknown')}",
                f"**Type:** {a.get('attack_type', 'unspecified')}",
                a.get('content', '')
            ])

    if defends := data.get('defends'):
        sections.append("## Defends")
        for d in defends:
            sections.extend([
                f"### Defending {d.get('target_id', 'unknown')}",
                f"**Type:** {d.get('defense_type', 'unspecified')}",
                d.get('content', '')
            ])

    return '\n\n'.join(sections)
