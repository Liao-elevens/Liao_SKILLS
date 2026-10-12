# Project-level shared modules

## About / 简介

**EN:** Promote code when consumers share a stable responsibility, not merely similar syntax.

**中文：** 按稳定职责和真实复用提升共享代码，避免因形式相似就抽公共层。

## Promotion decision

Start with [feature-local placement](ui-module-split.md). Two or more consumers trigger a reuse assessment, not automatic promotion to global shared code. Nearby components can share feature-local helpers. Use a project-wide shared location when the same domain meaning, contract, and change reasons span features, or an established shared boundary already owns the concern.

Before promotion, verify:

- Consumers need the same behavior, not just similarly shaped loops or UI.
- The interface does not acquire feature flags, hardcoded copy, route assumptions, or unrelated optional parameters to serve each caller.
- Feature-specific dependencies will not leak into shared code or create cycles.
- The shared module has a clear owner, focused public surface, and compatible runtime/dependency requirements.

If these do not hold, keep the code separate or share only the stable common operation. Do not pre-build extension points for imagined consumers.

## Shape and location

| Kind | Placement and boundary |
| --- | --- |
| Shared UI | Existing components/UI/design-system location; follow project composition, styling, and accessibility conventions |
| State/data logic | Existing hooks, composables, services, stores, or framework equivalents; make effects, cache, and lifecycle ownership clear |
| Pure helpers | A focused domain/module file in the existing shared utility location; use the grouping and naming rules in [module layout](ui-module-split.md#helper-files-and-utils--util) |
| Types/contracts | The existing owning model/type/generated-client location; export only what consumers need |
| Thin adapters | Keep when they enforce a stable external/platform/design-system boundary; avoid silent behavior changes |

Do not introduce a parallel source root or alternative `util`/`utils` naming convention. Group small related helpers before creating domain subfolders. Individual tests are not a reason to fragment helpers.

Feature code can depend on shared code; shared code must not import feature-specific implementations. Avoid broad barrels that obscure ownership or pull incompatible runtimes into one import. Keep a public barrel only where it serves an intentional interface.

## Review the move

Check actual imports/callers, side effects, bundle boundaries, and behavior after a move. A second caller or a shorter import path alone is not evidence that a new shared abstraction is better. See [sharing cases](../references/code-quality-examples.md#useful-boundaries-and-accidental-similarity).
