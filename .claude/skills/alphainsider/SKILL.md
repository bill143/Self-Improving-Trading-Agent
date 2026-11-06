---
name: alphainsider
description: All-in-one access to AlphaInsider skills for API work, strategy creation, backtesting, and automation. Loads the matching specialist on request. Use only when the user runs /alphainsider, says "use the alphainsider skill", "route this with alphainsider", or "which AlphaInsider skill".
---

# AlphaInsider

Version: 1.1.1

## Updates

1. On first interactive use per conversation, inspect installed versions of this
   repository's `alphainsider` and `alphainsider-strategy-creator` skills, and read
   all pages of [public GitHub releases](https://api.github.com/repos/AlphaInsider/skills/releases?per_page=100)
   without authentication. Compare numerically with the highest published stable
   `vX.Y.Z`; ignore drafts, prereleases, bare tags, and Latest. For older/unknown
   copies, show installed/available versions, label unknowns, and pause:
   **Update all** or **Continue**. Share results/choices across skills; recheck
   on request. Skip unattended runs. Continue quietly on automatic lookup failure
   or no releases; explain explicit-check failures. The hosted API skill is
   maintained by Mintlify and is excluded from this GitHub release check.

2. On **Update all**, use available capabilities to update existing older/unknown
   copies from the selected release, preserving installation scope. Keep current/newer
   copies; install no missing skills. Reload updated instructions when supported
   and resume. If unable to update, report outcomes, link the release, and give
   suitable manual instructions; continue with available versions.

The all-in-one AlphaInsider skill provides one entry point for API work, strategy
creation, backtesting, and automation. Load the matching specialist as needed;
users do not need to install each one separately. Specialists also remain
available on their own.

## Start

Read [`references/catalog.md`](references/catalog.md). Match the user query to
catalog entries. Do not preload specialist skills.
For web-loaded files, resolve relative links against each fetched file's URL,
retaining the same Git ref (`master` in the links below, or the selected release).

## Route

- Zero matches: say so, list the catalog, and ask which skill.
- Two or more matches: always ask. Do not silently pick.
- One match or a user pick: load that specialist in this turn.

## Load

For API work, read the live [AlphaInsider API skill](https://api.alphainsider.com/skill.md)
and follow its navigation and prerequisite guides. Use this source even if an
older GitHub API skill is installed. If required guidance cannot be fetched,
report the missing source and pause dependent API work.

For Strategy Creator:

1. Use the environment's discovery tools to find an installed specialist.
   Follow its `SKILL.md`, references, and scripts.
2. Otherwise, when downloads and extraction are available, load the complete
   package from the selected release in the [catalog](references/catalog.md)
   into temporary storage. Use the latest release unless the user selected a
   version. Follow that package's `SKILL.md` and retain its relative references
   and scripts. This loads it for the conversation without installing it.
3. If package access is unavailable, read
   [Strategy Creator](https://raw.githubusercontent.com/AlphaInsider/skills/master/skills/alphainsider-strategy-creator/SKILL.md)
   directly, then its required references. For a selected release, resolve its
   tag and use that tag in all raw URLs instead of `master`. Do not silently
   substitute another version if retrieval fails. Report any required file
   that cannot be fetched and stop dependent work.

## Persist

Install a specialist only when the user asks, using its source in the
[catalog](references/catalog.md) and the environment's supported skill manager
or skill-file storage. Never install the API skill from the GitHub repository.
For filesystem installation, if the user does not say global vs this project,
ask and recommend global. Respect an already selected scope.

For Strategy Creator, download the complete selected release package, including
references and scripts, preserving its directory layout and Git ref. For the API
skill, save the hosted file as described in the catalog. After installation, confirm the
location, version when available, and whether the agent can discover and load
the skill. Load it using the source rules above. If installation is unavailable
or incomplete, report that outcome and provide the catalog's ZIP/upload steps;
describe a web-loaded skill as loaded for this conversation, not installed.

Do not require any specialist to be preinstalled. Do not install specialists
as a side effect of routing. Never inspect or print existing API keys or
`.env` values.

## References

- [`references/catalog.md`](references/catalog.md) — routable specialists
