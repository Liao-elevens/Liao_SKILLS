# Project-level shared modules

## About / 简介

**EN:** Where to put reusable frontend code shared by multiple features: UI modules, state/data logic, services, utilities, models, schemas, and design-system wrappers.

**中文：** 约定多个功能复用的前端代码如何落盘，包括 UI 模块、状态/数据逻辑、服务、工具函数、模型、Schema 和设计系统封装。

## How to use

Start with feature-local code following `ui-module-split.md`. Promote code to a shared location only when two or more features need it or when the project already has a documented shared module boundary for that concern.

Use the project's existing source root and naming convention. The examples below use common names, but they are not mandatory:

```text
<source-root>/
  shared/ or components/ or ui/
  hooks/ or composables/ or services/
  utils/ or lib/
  models/ or types/ or schemas/
  stores/ or state/
```

---

## 1. Recommended shared tree

Choose the branch that matches the project's stack and existing conventions:

```text
<source-root>/
  ui/ or components/
    <domain-or-component>/
      entry-file
      styles-file          # optional; match the project
      types-or-models      # optional; scoped to this shared module
  hooks/ or composables/ or services/
    <name>
    <domain>/              # optional; when several modules belong together
  utils/ or lib/
    <name>
    <domain>/
  models/ or types/ or schemas/
  stores/ or state/
```

### 1.1 Shared UI modules

| Item | Rule |
|------|------|
| Purpose | Presentational or interactive blocks shared by two or more features. |
| Layout | Prefer one folder per reusable unit when the module has styles, tests, types, or submodules. |
| Styling | Use the project's established styling method and design-system tokens. |
| Naming | Prefer domain or UI-purpose names over vague buckets such as `common` when a clearer name exists. |

### 1.2 Shared state/data logic

| Item | Rule |
|------|------|
| Purpose | Reusable hooks, composables, services, stores, request helpers, selectors, or framework equivalents. |
| Shape | Match the project framework: hooks for React, composables for Vue, services for Angular, stores for state libraries, or another existing convention. |
| Content | Inputs, outputs, side effects, and cache behavior should be explicit and documented through types, schemas, or clear names. |

### 1.3 Shared utilities

| Item | Rule |
|------|------|
| Purpose | Pure helpers first; shared constants and thin adapters are allowed when they belong to a clear domain. |
| Shape | Use one module-level file for small related utilities. Use a domain folder only when several related helpers grow together and the domain boundary is clear. |
| Boundary | Keep utilities framework-agnostic unless the shared utility is explicitly tied to a framework or UI library. |

### 1.4 Cross-cutting

| Topic | Rule |
|-------|------|
| Imports | Feature code may depend on shared modules; shared modules should not depend on feature-specific modules. |
| Naming | Follow project conventions. If no convention exists, prefer clear domain names and kebab-case folders. |
| Public surface | Export only what consumers need. Avoid wide barrel exports that hide ownership. |

---

## 2. Promote checklist

- Used by two or more features, screens, routes, or independently owned modules.
- No feature-specific copy, route assumptions, permissions, or state shape are hardcoded.
- Public API is minimal, typed or schema-backed where possible, and easy to test.
- Move does not introduce circular dependencies.
- The shared location matches the project's existing source-root and ownership convention.

---

## 3. Post-change placement review

After implementing local logic, review whether new functions, helpers, renderers, mappings, or adapters are placed at the right ownership boundary before finalizing the change.

- Data source: logic tightly coupled to a data shape should live near that data adapter, model, or type definition.
- Reuse boundary: logic used by multiple local components should move to feature-local utilities before becoming global shared code.
- Component responsibility: components should keep view wiring and interaction composition; reusable data-shaping, option-mapping, and rendering rules should live outside the component when their ownership is broader than that component.
- Stability: avoid promoting code to shared modules until reuse is real or the boundary is clearly stable.
- Granularity: when promoting shared utilities, keep related helpers together in one domain/module file first. Avoid creating many tiny shared utility files unless they have separate owners, tests, or reuse boundaries.

---

## 4. Anti-patterns

- Promoting one-off feature logic before reuse exists.
- Creating shared folders outside the project's source-root convention.
- Shared modules depending on feature-specific modules.
- Large `common` or `utils` buckets with unrelated responsibilities.
- One-helper-per-file shared utility layouts that make a domain harder to scan without creating a clearer public API.
- Design-system wrappers that silently change behavior across the app without clear naming or documentation.
