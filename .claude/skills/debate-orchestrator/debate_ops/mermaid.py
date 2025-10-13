"""Generate mermaid argument graph from debate state."""
from __future__ import annotations

import json
from pathlib import Path
from debate_ops import frontmatter


def generate_graph(debate: str) -> None:
    """Generate mermaid flowchart showing argument relationships and scores.

    Reads argument structure from frontmatter, scores from scores.json.
    Updates or creates {debate}/argument-graph.mmd.
    """
    debate_dir = Path.cwd() / debate
    args_dir = debate_dir / 'arguments'

    if not args_dir.exists():
        return

    # Load scores from scores.json
    scores_file = debate_dir / 'scores.json'
    scores_data = json.load(open(scores_file)) if scores_file.exists() else {}

    # Collect argument data
    arguments = []
    for arg_file in sorted(args_dir.glob('*.md')):
        doc = frontmatter.load(arg_file)
        meta = doc.metadata
        arg_id = meta.get('id', arg_file.stem)

        # Get score from scores.json instead of frontmatter
        score = scores_data.get(arg_id, {}).get('current_score', None)

        # Get attacks and defends (expect dict format with target_id and type)
        attacks = meta.get('attacks', [])
        defends = meta.get('defends', [])

        # Use title if available, otherwise fallback to truncated claim
        display_text = meta.get('title', meta.get('claim', 'No claim')[:50] + ('...' if len(meta.get('claim', '')) > 50 else ''))

        arguments.append({
            'id': arg_id,
            'side': meta.get('side', 'unknown'),
            'display': display_text,
            'score': score,
            'attacks': attacks,
            'defends': defends
        })

    if not arguments:
        return

    # Build mermaid syntax with ELK layout for better visualization
    lines = [
        '---',
        'config:',
        '  layout: elk',
        '  elk:',
        '    nodePlacementStrategy: NETWORK_SIMPLEX',
        '---',
        'graph TD',
        ''
    ]

    # Nodes - dark fills with white text for GitHub theme compatibility
    for arg in arguments:
        score = arg['score'] if arg['score'] is not None else 0
        score_display = f"{score:.2f}" if score is not None else "—"

        # Proposition: dark green, Opposition: dark red
        fill, stroke, border_width = (
            ('#1B5E20', '#4CAF50', '3px') if arg['side'] == 'prop' and score >= 0.75
            else ('#1B5E20', '#4CAF50', '2px') if arg['side'] == 'prop'
            else ('#B71C1C', '#F44336', '3px') if score >= 0.75
            else ('#B71C1C', '#F44336', '2px')
        )

        lines.extend([
            f'    {arg["id"]}["{arg["id"]}<br/>{arg["display"]}<br/>⭐ {score_display}"]',
            f'    style {arg["id"]} fill:{fill},stroke:{stroke},stroke-width:{border_width},color:#FFFFFF'
        ])

    lines.append('')

    # Edges - track index for linkStyle coloring
    edge_index = 0
    link_styles = []

    for arg in arguments:
        # Attacks: solid lines, orange color
        for attack in arg['attacks']:
            target_id = attack['target_id']
            attack_type = attack['type'].replace('_attack', '') if '_attack' in attack['type'] else attack['type']
            lines.append(f'    {arg["id"]} -->|⚔️ {attack_type}| {target_id}')
            link_styles.append(f'    linkStyle {edge_index} stroke:#ff9800,stroke-width:2px')
            edge_index += 1

        # Defends: blue color, style varies by type
        for defend in arg['defends']:
            target_id = defend['target_id']
            defense_type = defend['type']

            if defense_type == 'concede_and_pivot':
                # Concede and pivot: dotted line (retreat/weakness)
                emoji = '↩️'
                lines.append(f'    {arg["id"]} -.->|{emoji} {defense_type}| {target_id}')
            else:
                # Reinforce/clarify: solid line (strengthening)
                emoji = '🛡️'
                lines.append(f'    {arg["id"]} -->|{emoji} {defense_type}| {target_id}')

            link_styles.append(f'    linkStyle {edge_index} stroke:#2196F3,stroke-width:2px')
            edge_index += 1

    # Add link styles at the end
    if link_styles:
        lines.append('')
        lines.extend(link_styles)

    # Write to file
    output_file = debate_dir / 'argument-graph.mmd'
    output_file.write_text('\n'.join(lines) + '\n')
