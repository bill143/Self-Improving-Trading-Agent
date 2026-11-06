# AlphaInsider skill catalog

Routable specialists and their canonical sources. The API skill is hosted by
Mintlify; Strategy Creator is published from this repository.

For requested installation, use the environment's supported skill manager or
skill-file storage. If unavailable, provide the
[Download and Install guide](https://github.com/AlphaInsider/skills#download-and-install) and report
that installation is incomplete. The guide covers direct skill ZIP downloads,
manual packaging when assets are unavailable, and the separately hosted API skill.

## alphainsider-api

- When to use: REST or WebSocket API behavior, request examples,
  authentication, orders, positions, bots, market data, billing, or streams.
- Read the [hosted API skill](https://api.alphainsider.com/skill.md) and its linked
  guides; no GitHub API package or persistent installation is required.
- Install only when requested: save the hosted file as `alphainsider-api/SKILL.md`
  in the supported skill storage. Its linked guides remain online. Do not install
  an older GitHub API package.

## alphainsider-strategy-creator

- When to use: define, backtest, implement, schedule, run, resume, recover,
  or update a trading strategy with a persistent project plan and
  AlphaInsider forward testing.
- Source: the [latest release](https://github.com/AlphaInsider/skills/releases/latest)
  and its [Strategy Creator ZIP](https://github.com/AlphaInsider/skills/releases/latest/download/alphainsider-strategy-creator.zip).
  Use the selected version's assets instead when the user specifies a release.
- Install only when requested. Keep the complete skill folder, including
  `SKILL.md`, references, and scripts, in the supported skill storage.
- For conversation-only fallback, read the [raw Strategy Creator skill](https://raw.githubusercontent.com/AlphaInsider/skills/master/skills/alphainsider-strategy-creator/SKILL.md)
  and its required references. Use the selected release's Git ref for every file;
  the `master` link applies when no release was selected.
