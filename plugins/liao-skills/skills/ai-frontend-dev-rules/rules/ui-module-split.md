# UI module and folder split

## About / 简介

**EN:** Where to put views, UI blocks, state/data logic, models, utilities, styles, and assets so each frontend feature stays readable and AI changes stay scoped.

**中文：** 约定视图、UI 区块、状态/数据逻辑、模型、工具函数、样式和资源的落盘方式，让功能结构清晰，并让 AI 修改范围可控。

---

## 0. Agent triggers and default behavior

If `ai-frontend-dev-rules` is available and the task touches a non-trivial page, view, route, screen, widget, table, form, modal, or feature module, treat this file as the default structure guide. Do not wait for the user to explicitly say "split modules".

### 0.1 When this document applies

| Situation | Action |
|-----------|--------|
| New page, screen, route, view, or feature module | Create a project-appropriate feature tree; keep the entry file thin. |
| Adding a table, form, wizard, modal, dashboard, or two or more distinct UI blocks | Put meaningful UI blocks into their own feature-local modules. |
| Entry file holds UI, request handling, mapping data, state clusters, and types/models together | Move state/data logic, type/model definitions, mappings, and pure helpers out of the entry file. |
| File is already large or likely to grow after the change | Split into UI blocks, state/data logic, types/models, and utilities without changing behavior. |
| User says "split modules", "componentize", "too large", "messy structure", or asks for standards | Apply this document to the relevant frontend feature. |

### 0.2 Default responsibilities

| Location or concept | Owns |
|---------------------|------|
| Feature entry | Route/view/screen shell, high-level composition, and wiring child modules together. Avoid long inline data arrays, request logic, or complex UI blocks. |
| UI block modules | Presentational or semi-controlled sections such as toolbars, tables, cards, panels, modals, and form sections. |
| State/data logic | Feature-specific state, effects/subscriptions, pagination, request orchestration, cache wiring, and derived data. |
| Types/models/schemas | Feature-owned interfaces, DTOs, schemas, prop contracts, view models, and domain models. |
| Utilities | Pure functions, formatters, parsers, validators, option builders, and static config factories. |
| Styles/assets | Co-located styles and assets when they are specific to the feature or UI block. |

### 0.3 Decide ownership before editing

Before writing or moving code, decide where the code should live by responsibility and consumer scope. Treat placement as part of the implementation, not as cleanup after the fact.

- Place code by ownership, not by convenience, currently open files, shortest import paths, or where the immediate caller happens to be.
- For each new component, state module, hook, composable, service, utility, mapper, type, schema, style, or asset, ask which layer owns it: entry composition, UI block, state/data orchestration, API/service boundary, type/model contract, pure utility, shared module, or styling/resource layer.
- Keep orchestration, auxiliary data, API contracts, view models, display mappings, and rendering logic in the layer that owns them. Do not hide unrelated responsibilities inside a broad page or feature coordinator just because several children need the result.
- Use consumer scope to choose location: one component or view can keep code local; nearby modules can share a feature-local module; cross-feature or cross-route reuse can move to a shared module after the dependency direction is clear.
- When a change introduces a new helper or data source, prefer a small named module at the correct boundary over adding another concern to an already busy entry file or coordinator.

---

## How to use

For every new non-trivial feature, create a structure that matches the project's existing framework and source-root convention. The tree below is an example, not a required path shape:

```text
<source-root>/
  <feature-root>/
    entry-file
    styles-file            # optional; match project convention
    assets/                # optional; feature-only assets
    ui/ or components/     # optional; UI blocks
      <feature-part>/
        entry-file
        styles-file        # optional; match project convention
    state/ or hooks/ or composables/ or services/
    utils/                 # or one module-level utility file for related helpers
    types/ or models/ or schemas/
```

Use the names already common in the project. For example, React projects may use `components` and hooks, Vue projects may use `components` and composables, Angular projects may use components/services/models, and Svelte projects may use components/stores/modules. Do not introduce a new naming system for one feature alone.

### Style files

Follow the existing styling strategy in nearby code: CSS Modules, scoped styles, Sass/Less, utility classes, CSS-in-JS, framework-scoped styles, design tokens, or another project convention. Do not introduce a new style-file suffix or styling system for one feature unless the task explicitly requires it.

### Utility file granularity

Prefer one utility file per feature or functional module for small, related pure helpers. For example, `utils.ts`, `utils/index.ts`, or an existing project-specific equivalent such as `utils/view-model.ts` can hold related formatters, parsers, validators, option builders, and view-model helpers for that module.

Do not create many tiny utility files such as `format-time.ts`, `build-options.ts`, and `parse-status.ts` when they are only used by the same feature module and are easier to scan together. Split a utility folder by domain only when the helpers are numerous, independently reusable, tested separately, or owned by clearly different subdomains.

### 1.5 Split heuristics

Prefer splitting when any of the following is true. If none apply and the feature is a one-off trivial screen, a minimal entry file is acceptable.

| Heuristic | Prefer split |
|-----------|--------------|
| A touched file is large and has mixed responsibilities, complex UI blocks, or growing renderers | Yes |
| It contains two or more of: UI sections, option/column builders, request orchestration, local state clusters, mapping tables, validation rules | Yes |
| A reusable-looking UI block clutters the entry file | Move to a feature-local UI module first. |
| Mock/static data or option lists become lengthy | Move to a feature-local constants, data, or utils module. |

### 1.5.1 Post-edit split check

After any frontend file edit, re-check the touched files before finalizing, even when the requested change was small.

- Use line count as a review trigger, not an automatic split rule:
  - Around 180 lines: scan for separable UI blocks or mixed responsibilities.
  - Around 300 lines: perform a mandatory split review and record why large code remains local if not split.
  - Around 500 lines: split by default unless the file is mostly flat configuration, types, generated code, or a cohesive single-purpose definition.
- Consider responsibility signals alongside size: complex renderers, table action areas, modal sections, form sections, toolbars, cards, request orchestration, local state clusters, data mappings, and styles mixed in one file all increase the need to split.
- Be tolerant of cohesive long files when they are intentionally single-purpose, such as stable column configuration, type declarations, static config maps, or flat option data; extract only the complex cells, blocks, or helpers that improve readability.
- If the edit adds or expands a visible UI block, cell renderer, modal section, form section, table action area, toolbar, card, or other meaningful UI unit, consider extracting it into a feature-local component module.
- When splitting UI blocks, check whether the block's dedicated styles are still sitting in the page or feature entry stylesheet. Move those styles next to the owning UI block unless they are truly shared layout, theme tokens, or cross-block utilities.
- If extraction is not performed, be able to state why the logic remains local: trivial size, a single-use simple expression, or extraction would add more indirection than clarity.
- Perform this check before the final placement review for shared or feature-local ownership.

Naming should follow the project convention. If the project has no convention, prefer kebab-case folders for UI modules and one obvious entry file per folder.

### 1.6 UI blocks use their own module

Every exported UI block split from a larger feature should live in its own feature-local module folder when it has independent responsibility. Avoid adding several loose sibling UI files at the same level when each is a distinct block.

Non-UI modules that export only constants, option builders, validators, mapping tables, or state/data helpers may stay in an existing feature utility/state folder or a module-level utility file. Do not force every non-UI file into a UI-block folder, and do not create a separate utility file for each small helper.

## 2. Rules

| Area | Rule |
|------|------|
| Entry file | Compose high-level layout and wire child modules. Keep detailed UI, request logic, and mappings outside when they grow. |
| UI modules | Split by visible block or interaction boundary. Co-locate styles when the block owns dedicated styling. |
| State/data logic | Keep feature-specific state and request orchestration close to the feature. Promote only when reuse is real. |
| Utilities | Keep utilities pure and framework-agnostic when possible. Group small related helpers in one module-level utility file; split only when domain ownership or size justifies it. |
| Types/models/schemas | Keep feature-only contracts with the feature; promote shared contracts only when multiple features need them. |
| Shared code | Move to shared roots only after two or more features need the same code. |

## 3. Anti-patterns

- Oversized single entry files with UI, state, API calls, mappings, validations, and types mixed together.
- Promoting one-off feature logic to shared folders before reuse exists.
- Duplicating shared helpers under multiple features.
- Placing feature-specific assets in a global public/static folder when they belong with the feature.
- Adding multiple loose sibling UI files when each file is a distinct block that should be a module.
- Creating one utility file per small helper inside the same feature module, which fragments related logic without improving ownership.

## 3.1 Agent checklist

If you added or edited a frontend feature, confirm:

- [ ] The feature entry is composition-focused or intentionally minimal.
- [ ] Touched files passed the post-edit split check; large files and newly expanded UI blocks were extracted or intentionally kept local.
- [ ] Meaningful UI blocks live in feature-local modules with project-consistent naming.
- [ ] Styles for meaningful UI blocks are co-located with the owning block; page/feature entry stylesheets contain only shell layout, shared theme tokens, or cross-block utilities.
- [ ] Feature state/data logic is not mixed into long UI files.
- [ ] Types/models/schemas and pure utilities are placed near the feature or in shared roots only when reused.
- [ ] Small related utilities are grouped by feature or functional module instead of being scattered across many tiny files.
- [ ] Shared promotion happened only when reuse and dependency direction are clear.

## 4. Routing or navigation

- Register routes, screens, or navigation entries through the project's established routing/navigation mechanism.
- Preserve lazy loading, guards, error boundaries, and fallback behavior when the project already uses them.

## 5. Page scroll and viewport

- Ensure long pages, screens, modals, and panels can scroll without clipping content.
- Prefer one clear scroll container for a region. Avoid nested scrolling unless the design or platform requires it.
