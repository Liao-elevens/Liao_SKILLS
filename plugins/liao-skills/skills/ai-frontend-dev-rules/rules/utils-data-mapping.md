# Utils data mapping

## About / 简介

**EN:** Keep domain values, backend codes, UI option values, and display labels centralized, simple, and type-safe or schema-safe.

**中文：** 统一管理领域值、后端码值、UI 选项值和展示文案，保持结构简单，并尽量通过类型或 Schema 约束保证正确性。

## How to use

For feature-local mappings, place value/label data near the feature utilities, constants, models, or option builders. Prefer the module's existing utility or constants file for small related mappings instead of creating one mapping file per option set. When two or more features need the same mapping, promote it to the project's shared utility/model location.

Use the project's existing option shape first. If the project has no established shape, use plain `code` or `value` for the stable value and `label` for display text. Do not create extra mapping methods or wrapper objects just to translate between stable values and labels.

---

## 1. Recommended patterns

### 1.1 Stable domain codes

- Use a single stable value source for backend codes, domain values, route intents, action keys, or UI option values.
- In TypeScript projects, use `enum`, literal unions, `as const` arrays/objects, or generated types according to the project convention.
- In JavaScript projects, use frozen constants, documented objects, schema validators, or project-standard model definitions.
- Keep display labels in a clearly named label map or option list.

Example:

```ts
export enum StatusCode {
  New = 1,
  InProgress = 2,
}

export const STATUS_LABEL: Record<StatusCode, string> = {
  [StatusCode.New]: 'New',
  [StatusCode.InProgress]: 'In progress',
}
```

### 1.2 Option data uses a stable value and `label`

When a UI component, API adapter, form field, table filter, dropdown, or selector needs option data, use the project's established option fields. If there is no project convention, use either `code` or `value` for the stable value and `label` for the display text.

Example:

```ts
export const STATUS_OPTIONS: Array<{ code: StatusCode; label: string }> = [
  { code: StatusCode.New, label: STATUS_LABEL[StatusCode.New] },
  { code: StatusCode.InProgress, label: STATUS_LABEL[StatusCode.InProgress] },
]
```

For UI libraries that expect `value`, the equivalent shape is also acceptable:

```ts
export const STATUS_OPTIONS: Array<{ value: StatusCode; label: string }> = [
  { value: StatusCode.New, label: STATUS_LABEL[StatusCode.New] },
  { value: StatusCode.InProgress, label: STATUS_LABEL[StatusCode.InProgress] },
]
```

Do not add extra conversion helpers such as `getStatusLabelByCode`, `mapStatusCodeToLabel`, or `buildStatusMeta` when direct indexing or plain option data is enough.

### 1.3 Frontend actions and UI semantics

When identifiers are UI event names, action keys, menu keys, toolbar actions, or route intents, keep one canonical value set. Use a label map or option data for display.

If extra UI semantics are genuinely needed, such as tone, icon, permission, disabled reason, or analytics metadata, keep them in a clearly named map or config object. Do not infer styling or behavior from localized label text.

## 2. Rules

| Area | Rule |
|------|------|
| UI display | Read display strings from a centralized label map or from plain option data. Do not scatter localized strings in cells, tags, details, or forms. |
| Business logic | Compare using stable constants or enum members. Avoid magic numbers and magic strings. |
| Option shape | Use the project's existing option shape. If none exists, use `code` or `value` for stable values and `label` for display text. |
| No extra mapping methods | Do not create unnecessary helper methods solely to map between stable values and labels; use direct maps or plain options. |
| Coverage | Prefer exhaustive maps in typed projects. Use schema or tests in untyped projects when missing labels would be risky. |
| Unknown values | For closed typed value sets, use exhaustive maps and let missing coverage fail type checking or tests; do not add an `Unknown` fallback. Add unknown-value presentation only when the contract explicitly permits unknown or forward-compatible values, and handle it at one declared boundary. |
| Extra metadata | Add extra maps only for real needs such as i18n, permissions, dynamic copy, icons, tones, or analytics. |

## 3. Placement

- Feature-local mappings belong near the feature utilities, constants, models, schemas, or option builders.
- Small mappings owned by the same functional module should stay together in that module's existing utility/constants/model file unless they become large enough to deserve a domain file.
- Shared mappings belong in the project's shared utility/model location only when multiple features use them.
- Generated backend code/value contracts should stay in the generated or API-owned location; UI labels can adapt them in a feature or shared mapping layer.

## 4. Naming

- Value set: use domain names such as `StatusCode`, `PaymentStatus`, `OrderAction`, or the project equivalent.
- Label map: use a clear suffix such as `LABEL`, `LABELS`, or the project naming convention.
- Option list: use a clear suffix such as `OPTIONS`.
- One value set should have one obvious label source. Do not mix unrelated domain values in the same label map.

## 5. Avoid

- Ad-hoc maps inside components:
  - `const statusMap = { 1: 'New' }`
- Magic value checks:
  - `status === 1`
- Scattered localized strings:
  - `statusText = 'New'`
- Unnecessary wrappers:
  - `getLabelByCode(code)`
  - `mapCodeToLabel(code)`
  - `{ value, text, name, code, label }` when one stable value field plus `label` is enough
- Overly wide untyped maps:
  - `Record<number, string>` when a stable value type exists
- Fallback labels for closed typed values:
  - `STATUS_LABEL[status] ?? 'Unknown'` when `status` is a closed union or enum

## 6. Checklist

- [ ] Stable values are centralized.
- [ ] Display labels come from a label map or plain option data.
- [ ] Option-like data uses the project option shape, or `code`/`value` plus `label` when no standard exists.
- [ ] No unnecessary mapping method was added just to translate stable values to labels.
- [ ] UI does not inline raw codes or scattered localized strings.
- [ ] Logic does not rely on magic numbers or magic strings.
- [ ] Placement matches feature-local vs shared promotion rules.
- [ ] Closed typed value sets are exhaustive and do not hide missing coverage behind an unknown fallback.
