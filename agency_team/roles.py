"""Load team-member definitions from .claude/agents/*.md.

The Markdown files are the single source of truth for each agent's role: the
same file works as a Claude Code subagent and as the system prompt for the
autonomous runner.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / ".claude" / "agents"

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class Role:
    name: str
    description: str
    body: str
    path: Path

    @property
    def system_prompt(self) -> str:
        return (
            f"You are `{self.name}`, one member of a fully autonomous AI agency "
            "team executing JP Middleton's $5.4M AI-agency blueprint. There is no "
            "human in the loop: act, record your work through your tools, and "
            "never end a task by asking a person for permission.\n\n"
            f"{self.body}"
        )


def _parse(path: Path) -> Role:
    text = path.read_text(encoding="utf-8")
    name = path.stem
    description = ""
    match = _FRONTMATTER_RE.match(text)
    body = text
    if match:
        body = text[match.end():]
        for line in match.group(1).splitlines():
            key, _, value = line.partition(":")
            key = key.strip().lower()
            if key == "name" and value.strip():
                name = value.strip()
            elif key == "description":
                description = value.strip()
    return Role(name=name, description=description, body=body.strip(), path=path)


def load_roles(agents_dir: Path | None = None) -> dict[str, Role]:
    directory = agents_dir or AGENTS_DIR
    roles: dict[str, Role] = {}
    for path in sorted(directory.glob("*.md")):
        role = _parse(path)
        roles[role.name] = role
    return roles
