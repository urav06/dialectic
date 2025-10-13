"""Debate state management."""
from __future__ import annotations

from pathlib import Path
from typing import Literal, TypedDict

from debate_ops import frontmatter


Phase = Literal['awaiting_arguments', 'awaiting_judgment']


class DebateState(TypedDict):
    """Debate state from frontmatter."""
    debate_id: str
    current_exchange: int
    current_phase: Phase


def read_debate_state(debate: str) -> DebateState:
    """Read current debate state from debate.md frontmatter."""
    debate_file = Path.cwd() / debate / 'debate.md'
    doc = frontmatter.load(debate_file)

    return DebateState(
        debate_id=doc['debate_id'],
        current_exchange=doc['current_exchange'],
        current_phase=doc['current_phase']  # type: ignore
    )


def update_debate_state(
    debate: str,
    current_exchange: int | None = None,
    current_phase: Phase | None = None
) -> None:
    """Update debate.md frontmatter with new state values."""
    debate_file = Path.cwd() / debate / 'debate.md'
    doc = frontmatter.load(debate_file)

    if current_exchange is not None:
        doc.metadata['current_exchange'] = current_exchange

    if current_phase is not None:
        doc.metadata['current_phase'] = current_phase

    frontmatter.dump(doc, debate_file)
