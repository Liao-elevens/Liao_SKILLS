# UI module and folder split

## About / 简介

**EN:** Organize features by responsibility without turning each function or component into its own directory.

**中文：** 按职责组织功能模块，聚合相关小函数，避免一个函数一个目录和机械拆分组件。

## Decide ownership before placement

Read this file for non-trivial feature work, growing files, or placement changes. Keep one-component logic near its consumer; put nearby consumers' genuinely shared code in the feature; use [shared-module rules](project-shared-modules.md) before moving it across features.

A component may contain its template/rendering, local state, a few handlers, private types, and small private helpers. Their coexistence alone is not a split signal. A thin entry is useful for complex composition, not a requirement that every page become a shell.

| Signal | Preferred action | Keep local when |
| --- | --- | --- |
| A UI section has its own substantial interactions and change reasons | Extract a feature-local component with a small interface | It is a short one-off block and extraction mostly adds props/wiring |
| A lifecycle/request workflow obscures the view | Extract meaningful operations or use existing hooks/composables/services | Simple lifecycle work remains readable beside its owner |
| Repeated helpers serve neighboring components | Group them in the module's existing utility file | They are private to one file and need no public interface |
| A type or constant is needed by several modules | Place it at its owning boundary | It is private or can be inferred without a separate file |

Preserve existing route, server/client, lazy-loading, style, and asset boundaries. Do not gather different runtime concerns into a universal utility bucket.

## Helper files and `utils` / `util`

**Extracting a function, a file, and a folder are three separate decisions.**

1. Keep small single-file private helpers in that file. Do not export them merely for testing.
2. Aggregate small module-shared helpers in an existing module-level helper file. Without an established convention, use `utils.ts` (or the language equivalent), or an implementation file inside an existing `utils/` directory such as `utils/index.ts`.
3. Default to the name `utils`. If the project already consistently uses `util`, keep it. These names do not imply different local/global or pure/impure responsibilities. Do not mix `util`, `utils`, `helpers`, and `common` for the same role.
4. When that file grows to around **300 lines of normally formatted source**, review cohesion. Split related groups by business intent, shared data, callers, and reasons to change. Keep the extracted helper files together inside the module's `utils/` directory (or its existing `util/` equivalent).
5. Each resulting file can hold several related functions. Name it for a responsibility, not an individual tiny operation or sequence number.

Example after a warranted split; the framework/file suffix is illustrative:

```text
orders/
  OrderList.vue
  OrderPanel.vue
  utils/
    totals.ts     # related amount calculations
    filters.ts    # related filtering predicates/transforms
    display.ts    # related formatting/display helpers
```

Do not create `utils/format-price/index.ts`, `utils/build-options/index.ts`, `utils1.ts`, or a folder per helper. Do not add forwarding `index` files to every directory. An existing `utils/index.ts` may contain implementations; a barrel is optional and must have an actual public-import purpose.

## Size is a review trigger

Around 300 lines, inspect the touched file's responsibilities and reading cost. This is not a maximum, not a target size, and not an instruction to pad or compress code. There is no additional 180-line extraction rule or 500-line automatic split rule.

- Keep a cohesive algorithm, generated file, type declaration, or flat static configuration together when splitting would obscure it. Do not edit generated output manually.
- Split before 300 lines when an actual independent public boundary, browser/server runtime, heavy dependency, or lazy-loaded path requires it.
- Tests alone do not justify a separate file or folder per function. Test through the appropriate public boundary or keep tests beside the existing module.
- After splitting, check that circular imports, cross-file private dependencies, and prop plumbing have not increased. If they have, reconsider the boundary.
- After merging, check that runtime isolation, tree shaking, loading behavior, and side-effect initialization are preserved.

## UI, styles, and folders

Flat sibling component files are valid. Create a component folder for a meaningful cluster of related resources/submodules or when the project already requires that layout. Do not require a folder just because a component is exported or has a test.

Co-locate block-owned styles/assets when extracting a block; keep shared layout and theme ownership where it belongs. Respect scoped styles, CSS Modules, design tokens, utility classes, or the project's existing approach. Do not create a new styling system.

Keep long pages, panels, and modals scrollable without clipping. Prefer one clear scroll container per region unless nested scrolling is required by the design.

## Post-change placement review

Review touched files for cohesion, utility grouping, and scope of consumers. Be able to explain substantial extraction or retention by responsibility and reading cost, not a numeric quota. Apply [state ownership](state-and-data.md), [API boundaries](backend-api-integration.md), and [types](type-standards.md) only where relevant. See [layout cases](../references/code-quality-examples.md#helpers-and-folder-granularity).
