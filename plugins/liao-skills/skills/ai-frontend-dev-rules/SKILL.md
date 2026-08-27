---
name: ai-frontend-dev-rules
description: Technology-neutral frontend architecture rules for AI-assisted development. Use this skill when creating, extending, refactoring, or reviewing frontend features in any stack. Covers UI module split, shared modules, routing, type/schema boundaries, API/service integration, state/data strategy, code/value-label mapping, UI library usage, frontend performance, and change reporting. Always read rules/ui-module-split.md for non-trivial page or feature work, then report applied rules with change-reporting.md after substantial or final code changes.
---

# AI frontend dev rules

## About / 简介

**EN:** This skill provides technology-neutral frontend engineering rules that can be reused in any frontend project and adapted to the project's existing stack, framework, file layout, design system, and tooling.

**中文：** 本技能提供与技术栈无关的前端工程规范，可复用于任意前端项目，并按项目已有技术栈、框架、文件结构、设计系统和工具链适配。

## Binding in a project

Skill descriptions alone are not guaranteed to load for every model or session. If a project needs these rules to apply consistently, bind this skill through that project's agent rules, repository instructions, or equivalent workspace mechanism.

## Agent: module split is part of this skill

Whenever you implement or refactor a non-trivial frontend page, view, route, screen, or feature module, follow `rules/ui-module-split.md`. Keep the entry file thin, move meaningful UI blocks, state/data logic, types/models, and pure helpers into the project-appropriate module locations. Do not default to a single large entry file unless the feature is trivially small.

## When to Apply

Use this skill when:
- Scaffolding or extending frontend feature modules, pages, routes, screens, views, widgets, forms, tables, or dashboards.
- Refactoring code that mixes layout, interaction logic, request handling, display mapping, and types/models in one file.
- Defining project-wide shared components, composables/hooks/services, utilities, stores, models, or design-system wrappers.
- Adding routes, screens, navigation entries, guards, permissions, or lazy-loaded feature boundaries.
- Writing typed or schema-backed frontend code and keeping data contracts close to the modules that own them.
- Choosing state scope: local, feature-level, shared, global, or server-cache state.
- Implementing or using a dedicated API/service layer while following the current project's conventions.
- Using a UI library or design system with version-correct, non-deprecated APIs.
- Reviewing frontend performance, bundle impact, render/update overhead, data fetching, or loading behavior.
- Reporting code changes that were guided by rules in this skill.

### Recognition cues

| User intent (examples) | Agent should |
|------------------------|--------------|
| New page, route, screen, list, form, dashboard, or widget | Apply `rules/ui-module-split.md`, then routing/state/type rules as needed. |
| "Split modules", "componentize", "too large", "messy structure" | Keep the entry thin and split by UI block, state/data logic, types/models, and utilities. |
| Shared UI, shared state logic, shared utilities, cross-feature reuse | Start local, then promote only when reuse is real and boundaries stay clean. |
| Code review, standards, architecture, maintainability | Check module layout, API usage, state/data, mappings, UI library usage, performance, and reporting. |

## Trust typed contracts; validate boundaries once

- Treat required values with an established static type as trusted inside the typed application domain and use them directly.
- Use optional chaining only for the exact receiver declared optional or nullable. Each `?.` must correspond to optionality in the contract; access required nested fields directly.
- Remember that an optional call or access makes the whole expression optional. Use forms such as `obj.arr?.map(...)` only when both the optional collection and an `undefined` result are intentional.
- Do not add guards, fallback values, defensive optional chaining, repeated normalization, or runtime validators to hide contract mismatches. Contract errors should fail fast.
- Perform runtime validation only at an explicitly identified untrusted boundary, and validate once as data enters the trusted domain. Downstream code consumes the resulting concrete type without revalidation.
- Do not introduce runtime schemas or validators merely because the project uses static types. They require an actual untrusted boundary or an explicit project requirement.

## Rule Categories by Priority

| Priority | Category | Impact | Related File |
|----------|----------|--------|--------------|
| 1 | UI Module Splitting | CRITICAL | `rules/ui-module-split.md` |
| 2 | Code Sharing | HIGH | `rules/project-shared-modules.md` |
| 3 | Routing | HIGH | `rules/routing-standards.md` |
| 4 | Type / Schema Safety | HIGH | `rules/type-standards.md` |
| 5 | API Layer | HIGH | `rules/backend-api-integration.md` |
| 6 | State Management | HIGH | `rules/state-and-data.md` |
| 7 | Utils Data Mapping | MEDIUM | `rules/utils-data-mapping.md` |
| 8 | UI Library Usage | MEDIUM | `rules/ui-library-usage.md` |
| 9 | Frontend Performance | MEDIUM | `rules/frontend-performance.md` |
| 10 | Change Reporting | MEDIUM | `change-reporting.md` |

## Quick Reference

### 1. UI Module Splitting (CRITICAL)
- `rules/ui-module-split.md` - Technology-neutral feature/module split, entry-file responsibilities, UI block placement, state/data logic placement, helper placement, and split heuristics.

### 2. Code Sharing (HIGH)
- `rules/project-shared-modules.md` - Shared UI modules, composables/hooks/services, utilities, state, and models.

### 3. Routing (HIGH)
- `rules/routing-standards.md` - Route/navigation organization, lazy loading, guards, fallback routes, and internal navigation.

### 4. Type / Schema Safety (HIGH)
- `rules/type-standards.md` - Type, schema, DTO, model, and boundary guidance for typed and untyped frontend projects.

### 5. API Layer (HIGH)
- `rules/backend-api-integration.md` - API/service layer boundaries, errors, naming, and environment rules.

### 6. State Management (HIGH)
- `rules/state-and-data.md` - Local vs feature vs shared/global vs server data, plus approval rules for new state/request libraries.

### 7. Utils Data Mapping (MEDIUM)
- `rules/utils-data-mapping.md` - Code/value to label mapping, project option shape, `code` or `value` plus `label`, naming, placement, and avoiding magic values.

### 8. UI Library (MEDIUM)
- `rules/ui-library-usage.md` - UI library and design-system usage: installed version, correct APIs/parameters, no deprecated APIs, styling, forms, and accessibility.

### 9. Performance (MEDIUM)
- `rules/frontend-performance.md` - General frontend performance checklist for data fetching, rendering, bundle size, loading, and verification.

### 10. Change Reporting (MEDIUM)
- `change-reporting.md` - Required final-delivery table for code changes guided by this skill.

## How to Use

Read individual rule files for detailed explanations and conventions:

```text
rules/ui-module-split.md
rules/routing-standards.md
rules/type-standards.md
rules/state-and-data.md
rules/ui-library-usage.md
change-reporting.md
...
```

## Agent Workflow

1. Confirm the project's frontend stack, routing/navigation model, UI library/design system, source-root layout, state/data libraries, and existing conventions.
2. For a new feature or non-trivial page/screen/view edit, open and follow `rules/ui-module-split.md` first, then `rules/routing-standards.md` and `rules/type-standards.md` as needed.
3. For shared code promotion, use `rules/project-shared-modules.md` and keep dependencies flowing from feature code to shared code, not the reverse.
4. After local edits, run the post-edit split check in `rules/ui-module-split.md` for touched frontend files, using line count as a review trigger rather than an automatic split rule, and paying special attention to files around 300+ lines or changes that add/expand UI blocks or renderers. Include style ownership in this check: UI-block-specific styles should be co-located with the owning block, while entry stylesheets should keep only shell layout, shared theme tokens, or cross-block utilities.
5. After local edits, apply the post-change placement review in `rules/project-shared-modules.md` before finalizing functions, helpers, renderers, mappings, or adapters.
6. For data and API work, use `rules/backend-api-integration.md` and `rules/state-and-data.md`.
7. For UI libraries, use `rules/ui-library-usage.md` and match the installed version exactly.
8. For performance, use `rules/frontend-performance.md` and the project's existing profiling/build tools.
9. After substantial or final code changes guided by this skill, include the table required by `change-reporting.md` in the delivery note. For trivial follow-up edits, pure Q&A, or documentation-only review with no project code change, do not force the table unless the user asks for it.

Only the `About / 简介` sections in rule files should be bilingual by default. Other rule content should be written in English unless a user explicitly asks for another language, a project-specific rule requires another language, or a required output format uses another language.
