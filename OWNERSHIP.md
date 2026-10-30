# Directory ownership (bootstrap phase)
Each agent writes ONLY inside its own paths. Nobody runs `git commit` (the coordinator commits).
Each package is standalone (own package.json + lockfile, npm). No root workspaces.

| Path | Owner |
|---|---|
| contracts/ | opus-contracts |
| web/ (except web/public/assets/ and web/src/game/elements/) | opus-web |
| server/ | opus-server |
| game-core/ (pure TS physics + Mario-like controller) | codex-controller |
| web/src/game/elements/ (Matter physics level elements) | codex-elements |
| assets/ and web/public/assets/ | codex-assets |
| docs/, root files | coordinator |
