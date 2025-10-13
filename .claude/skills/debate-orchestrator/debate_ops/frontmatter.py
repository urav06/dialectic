"""JSON frontmatter parsing - zero dependencies."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Document:
    metadata: dict[str, Any]
    content: str

    def __getitem__(self, key: str) -> Any:
        return self.metadata[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)


def _find_json_end(text: str) -> int:
    depth = in_string = escape_next = 0
    for i, char in enumerate(text):
        if escape_next:
            escape_next = 0
            continue
        if char == '\\':
            escape_next = 1
            continue
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return i + 1
    return -1


def parse(text: str) -> Document:
    text = text.lstrip()
    if not text.startswith('{'):
        raise ValueError("JSON frontmatter must start with '{'")

    end_pos = _find_json_end(text)
    if end_pos == -1:
        raise ValueError("JSON frontmatter not properly closed")

    try:
        metadata = json.loads(text[:end_pos])
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in frontmatter: {e}")

    if not isinstance(metadata, dict):
        raise ValueError("JSON frontmatter must be object")

    return Document(metadata=metadata, content=text[end_pos:].lstrip('\n'))


def dumps(metadata: dict[str, Any], content: str) -> str:
    return f"{json.dumps(metadata, indent=2)}\n\n{content}"


def load(filepath: Path | str) -> Document:
    return parse(Path(filepath).read_text())


def dump(doc: Document, filepath: Path | str) -> None:
    Path(filepath).write_text(dumps(doc.metadata, doc.content))


def update_metadata(filepath: Path | str, **updates: Any) -> None:
    doc = load(filepath)
    doc.metadata.update(updates)
    dump(doc, filepath)
