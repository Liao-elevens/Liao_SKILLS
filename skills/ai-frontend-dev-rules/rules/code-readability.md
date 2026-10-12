# Code readability

## About / 简介

**EN:** Make intent easy to read without long names, unnecessary temporaries, or compressed expressions.

**中文：** 用简短准确的命名、清晰的表达式和局部变量作用域降低阅读成本，避免冗长或过度压缩。

## Naming by scope

Use the shortest name that distinguishes the value in its actual scope. Local names normally need one to three meaningful words; more than four words is a **review trigger**, not a character limit or a reason to invent abbreviations.

| Situation | Preferred decision | Keep the longer name when |
| --- | --- | --- |
| The component/module already supplies the domain | Remove repeated owner/domain words | Another domain is also in scope or the export needs standalone meaning |
| `current`, `actual`, `data`, `info`, or `object` adds no distinction | Remove the filler | It distinguishes current vs previous, raw vs parsed, or another real state |
| A handler repeats the component and event suffix | Use the project's `handleSubmit`, `onSubmit`, or equivalent | The framework or public API assigns a specific name or role |
| A name is shortened | Retain units, direction, and relevant state | Always preserve distinctions such as `timeoutMs`, `sourceId`, `targetId` |

In an unambiguous user-selection scope, prefer `selectedId` to `currentlySelectedUserIdentifier`, `handleSubmit` to `handleUserFormSubmitEvent`, and `isLoading` to `isUserDataCurrentlyLoading`. With multiple selections or loads, retain `selectedUserId` or `isUserLoading` as needed.

- Reuse the project's vocabulary for the same concept; avoid alternating between `item`, `record`, and `entity` for one domain object.
- Keep meaningful public names, backend fields, generated names, and framework conventions such as `use...`. Do not rename external contracts to meet a word count.
- Boolean names should read as predicates (`isOpen`, `hasAccess`, `canEdit`). Avoid double negatives.
- Conventional short names such as `id`, `url`, and a small loop's `i` are fine. Cryptic shortenings such as `slctUsrCfg` are not.
- Include action and resource in exported functions when caller context does not supply them; do not repeat the entire folder hierarchy.

## Variables and expressions

- Declare variables near first use with the smallest practical scope. Do not reuse one variable for different concepts or change its type through a workflow.
- Inline a temporary that only renames an obvious expression used once. Keep a variable that names a business predicate, expensive result, unit conversion, or meaningful intermediate step.
- Avoid assignments, mutations, or side effects hidden inside a condition or a long expression when separate statements read more clearly.
- Keep simple binary ternaries. Avoid nested ternaries and dense mixed `&&`/`||` chains; use named predicates, parentheses, or the decision rules in [control flow](control-flow-and-data-transformations.md).
- Do not replace straightforward statements with clever one-liners to reduce line count. Conversely, do not expand a direct lookup into a wrapper and several temporaries.

## Comments and formatting

Explain **why**, constraints, protocol details, and non-obvious algorithms. Do not narrate obvious syntax or use comments to rescue misleading names. Preserve useful public API documentation, licenses, and necessary reasoning.

Follow the existing formatter, import style, and file naming. Remove touched dead code, stale commented-out implementations, and inaccurate comments within scope. Do not introduce a new formatting scheme or unrelated cleanup.

## Review

Can a reader identify the value's meaning, units, and owner without decoding abbreviations or repeating its enclosing scope? Does each temporary or comment reduce uncertainty? See [naming examples](../references/code-quality-examples.md#short-names-with-enough-context).
