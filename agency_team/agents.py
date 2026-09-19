"""Run a team member: role Markdown as system prompt, CRM tools, Claude loop.

Uses the Anthropic SDK's beta tool runner (the SDK drives the request ->
execute-tools -> feed-back loop). Research-heavy roles also get the server-side
web_search tool; because server tools can pause a turn (`pause_turn`), the
runner is restarted with mirrored history when that happens.
"""

from __future__ import annotations

import os

from .crm import CRM
from .roles import Role
from .tools import build_tools

MODEL = os.environ.get("AGENCY_MODEL", "claude-opus-5")
MAX_TOKENS = 16000
MAX_PAUSE_RESTARTS = 5

# Roles whose work depends on live web research.
RESEARCH_ROLES = {"market-research-agent", "ads-agent", "lead-scraper-agent"}

WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search", "max_uses": 12}


class AgentRunError(RuntimeError):
    pass


def run_agent(role: Role, task: str, crm: CRM, model: str = MODEL) -> str:
    """Run one role on one task to completion; returns the agent's final text."""
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover
        raise AgentRunError(
            "The autonomous runner needs the `anthropic` package: "
            "pip install 'anthropic>=0.116' (or `uv sync --extra agency`)."
        ) from exc

    client = anthropic.Anthropic()  # resolves ANTHROPIC_API_KEY / auth profile
    tools = build_tools(crm)
    if role.name in RESEARCH_ROLES:
        tools = [*tools, WEB_SEARCH_TOOL]

    messages: list[dict] = [{"role": "user", "content": task}]
    crm.log("agent_task_started", agent=role.name, task=task[:300])

    last = None
    restarts = 0
    while True:
        runner = client.beta.messages.tool_runner(
            model=model,
            max_tokens=MAX_TOKENS,
            system=role.system_prompt,
            tools=tools,
            messages=messages,
        )
        for message in runner:
            last = message
            # Mirror history so a pause_turn can be resumed with a fresh runner.
            messages.append({"role": "assistant", "content": message.content})
            tool_response = runner.generate_tool_call_response()
            if tool_response is not None:
                messages.append(tool_response)
        if last is None or last.stop_reason != "pause_turn":
            break
        restarts += 1
        if restarts > MAX_PAUSE_RESTARTS:
            crm.log("agent_task_stalled", agent=role.name, reason="pause_turn limit")
            break

    if last is None:
        raise AgentRunError(f"{role.name} produced no response")
    if last.stop_reason == "refusal":
        crm.log("agent_task_refused", agent=role.name)
        return "(request declined by safety classifiers)"

    text = "".join(b.text for b in last.content if b.type == "text")
    crm.log("agent_task_finished", agent=role.name, stop_reason=last.stop_reason)
    return text
