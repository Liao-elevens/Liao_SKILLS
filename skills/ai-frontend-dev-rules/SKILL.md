---
name: ai-frontend-dev-rules
description: Framework-neutral frontend implementation and architecture rules for creating, extending, refactoring, or reviewing frontend features. Guides readable naming, control flow, functions, helper grouping, module boundaries, types, state, API integration, routing, UI libraries, and performance in the project's existing stack.
---

# AI frontend dev rules

## About / 简介

**EN:** Write concise, readable frontend code with clear ownership and enough structure for the actual feature. Adapt to the project's framework, version, layout, and tooling.

**中文：** 让前端代码简洁、易读、易维护，按实际职责组织模块，避免冗长实现和过度拆分，并适配项目已有框架、版本、目录与工具链。

## Scope and rule strength

Apply to frontend implementation, refactoring, and review in Vue, React, Angular, Svelte, plain JavaScript/TypeScript, or another frontend stack. Identify the actual framework and version first. Preserve its idioms, including Vue Options API or Composition API; this skill does not require a framework, API-style, or state-library migration.

- **Hard constraints:** preserve required behavior, contracts, error handling, accessibility, and runtime boundaries. Do not prefix function calls with unary `void`; see [async calls](rules/state-and-data.md#async-calls-and-error-ownership).
- **Defaults:** prefer direct expressions, short clear names, local ownership, and grouped helpers. Depart when a concrete contract, framework constraint, or simpler reading path justifies it.
- **Review triggers:** size, name length, repeated branches, and repeated code prompt inspection. They are not quotas or automatic extraction rules.

Explicit user instructions and applicable project rules take precedence over these defaults. Surface a material conflict instead of silently changing behavior. Apply rules to the relevant change; do not expand a small fix into a repository-wide cleanup. Fewer lines, files, or conditional operators alone do not establish better code.

## Essential decisions

1. Read [code readability](rules/code-readability.md) for implementation or review. Keep the shortest name and expression that still communicate intent and required distinctions.
2. Select `if`, `switch`, maps, or collection operations by the decision's meaning; do not mechanically eliminate branches. Read [control flow and data transformations](rules/control-flow-and-data-transformations.md) when changing them.
3. Extracting a function, a file, and a folder are separate decisions. Keep small private helpers local; group module-shared helpers. Read [module layout](rules/ui-module-split.md) for non-trivial feature work or placement changes.
4. Trust established internal contracts without redundant guards, while preserving genuine optional values and untrusted-boundary checks. Read [types and contracts](rules/type-standards.md) when changing data contracts or defensive code.
5. Derive state using the current framework's idioms. Preserve async sequencing and explicit error ownership. Read [state and data](rules/state-and-data.md) when changing state, lifecycle work, or calls returning promises.

## Read only the relevant rules

| Task | Reference |
| --- | --- |
| Names, variable scope, comments, readable expressions | [Code readability](rules/code-readability.md) |
| Branches, maps, defaults, collection transformations | [Control flow and data transformations](rules/control-flow-and-data-transformations.md) |
| Function extraction, parameters, wrappers, abstraction | [Functions and abstraction](rules/functions-and-abstraction.md) |
| Feature layout, helper files, `utils`/`util`, components and styles | [UI module and folder split](rules/ui-module-split.md) |
| Reuse across features, shared exports and dependency direction | [Project shared modules](rules/project-shared-modules.md) |
| Types, optionality, validation, DTOs and models | [Type standards](rules/type-standards.md) |
| Derived state, framework lifecycle, async calls and errors | [State and data](rules/state-and-data.md) |
| Requests, transport, API adaptation and configuration | [Backend API integration](rules/backend-api-integration.md) |
| Stable values, labels, options and display metadata | [Utils data mapping](rules/utils-data-mapping.md) |
| Routes, URL state, guards and lazy boundaries | [Routing standards](rules/routing-standards.md) |
| Library versions, templates, component APIs and accessibility | [UI library usage](rules/ui-library-usage.md) |
| Rendering, fetching, bundles and justified optimization | [Frontend performance](rules/frontend-performance.md) |
| Reporting completed changes and verification | [Change reporting](change-reporting.md) |

For paired examples and cases that should stay unchanged, read the relevant section of [code quality examples](references/code-quality-examples.md). For rationale and framework-specific documentation, use [code quality sources](references/code-quality-sources.md); books inform the rules but are not mandatory reading for every task.

## Working loop

1. Inspect nearby implementation, installed versions, contracts, and existing project conventions before choosing a structure.
2. Identify the behavior to preserve and the smallest ownership boundary that fits the change. Select only relevant rule files.
3. Implement directly; add a function, abstraction, type, state value, or file only when its responsibility earns the extra indirection.
4. Review touched code for redundant names, branches, guards, wrappers, derived state, and fragmented helpers. Around 300 lines, review cohesion as described in the module rule; do not split solely to reach a number.
5. Run proportional project checks and behavior cases. Verify defaults, ordering, mutation, errors, and framework behavior when refactoring changes their expression.
6. Report the actual changes and verification using [change reporting](change-reporting.md). In a review-only task, report findings without editing unless asked to fix them.

Bind this skill through project agent instructions when consistent loading is required; its description alone cannot guarantee invocation. Keep only `About / 简介` sections bilingual by default; other skill content is English unless the user or project requires another language.
