# Ownership (post-bootstrap)

The bootstrap agents are done; the repo is now owned by the two students. Each package stays a
standalone npm project (no root workspaces). Shared files change only by agreement of both.

| Area | Student A — levels & market | Student B — economy & runs |
|---|---|---|
| Contract | `contracts/src/LevelNFT.sol`, `test/LevelNFT.t.sol` | `contracts/src/ForgeCoin.sol`, `test/ForgeCoin.t.sol`, `src/mocks/` |
| EIP-712 | `ClearProof` | `RunResult`, `RaceResult`, `SeasonResult`, ERC-2612 `Permit` |
| Server | `/levels/pin`, `/levels/clear-proof`, level schema/analysis, indexer (LevelNFT events) | `/runs/validate`, plausibility/replay validation, rooms (race/co-op), indexer (ForgeCoin events) |
| Web | editor + publish modal, browse, level detail, market (`usePublishLevel`, `useMarket`, `useLevel`) | play + race pages/scenes, profile/faucet (`useSettleRun`, `useFaucet`, `useForgeBalance`), Colyseus client |

**Shared (both review):** `contracts/src/interfaces/`, `test/Integration.ts`, Ignition module,
`game-core/` (controller + elements), `web/src/game/elements/bridge.ts`, `web/src/game/level/` (format +
canonical JSON), `test-vectors/`, `docs/`, root scripts. Generated files (`web/src/contracts/generated/*`,
`server/abi/*.json`) are only produced by `contracts/scripts/export-abi.ts` / `npm run deploy:local`.
