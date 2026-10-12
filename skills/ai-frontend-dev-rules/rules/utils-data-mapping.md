# Utils data mapping

## About / 简介

**EN:** Represent stable values, labels, and options with the smallest useful source of truth.

**中文：** 用最小必要的数据结构维护稳定值、显示文案和选项，避免多份定义与无意义转换函数。

## Choose only the representations consumers need

| Need | Prefer |
| --- | --- |
| Known code/value to label | A plain exhaustive label map in typed code, or tested coverage in untyped code |
| A selector's ordered options | Plain options in the project's expected shape |
| Both display lookup and options | One owned source with a simple derivation when useful; do not manually duplicate label knowledge |
| Icons, tone, permissions, or other real metadata | A focused metadata map/config only for fields actually consumed |
| Complex or contextual display rules | A meaningful function, using [control-flow rules](control-flow-and-data-transformations.md) |

Do not generate an enum, a union, a label map, an option list, and several conversion functions when the feature only needs one representation. Reuse existing/generated stable values; otherwise a clear string union may suffice. A readable check such as `status === 'draft'` is not automatically a magic-value violation. Give opaque protocol numbers and repeated unexplained business constants a named owner.

If no option convention exists, use `code` or `value` for the stable value and `label` for display. Do not duplicate `text`, `name`, `label`, `code`, and `value` without consumers needing them. Business logic must use stable values, not localized labels.

## Ownership and access

- A small single-component map can stay local. Group module-shared maps with related utilities/constants; do not force all labels into a global registry.
- Use direct indexing for a simple lookup. Avoid `getLabelByCode` wrappers that only rename indexing without adding meaning.
- Closed trusted value sets should have complete coverage; do not conceal missing entries behind `?? 'Unknown'`.
- Open/forward-compatible values need explicit missing-value presentation at the actual boundary. Protect open lookups from inherited properties as described in [lookup semantics](control-flow-and-data-transformations.md#preserve-semantics).
- Keep localization and dynamic labels reactive according to the existing i18n mechanism. Do not accidentally freeze translated strings in a module-level map at startup.
- Keep generated codes in their generated/API owner. Use [module grouping](ui-module-split.md#helper-files-and-utils--util) and [shared promotion](project-shared-modules.md) for frontend-owned mappings.

## Verify

Check coverage, option order, stable submitted values, legitimate unknown values, and locale changes where relevant. Examples are in [decision meaning](../references/code-quality-examples.md#choose-by-decision-meaning).
