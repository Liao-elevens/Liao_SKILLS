# Type and schema standards

## About / 简介

**EN:** Use the simplest accurate contracts, trust established internal data, and validate at real boundaries.

**中文：** 使用简单准确的类型契约，信任已经建立的内部数据约定，并在真实边界执行必要校验。

## Contracts and inference

Use the project's current TypeScript, Flow, JSDoc, generated clients, schemas, prop contracts, or other established mechanism. Do not require TypeScript or introduce a runtime schema library merely to apply this skill.

- Reuse existing domain and generated API types. Infer obvious local values; annotate public contracts or ambiguous results where that improves the interface.
- Export only types consumers need. A component prop type or function-local shape does not automatically need an export or a separate `types` file.
- Prefer ordinary object shapes, unions, and simple generics. Use a discriminated union when different states require different fields; do not model impossible combinations as many independent optional properties.
- Distinguish DTOs, domain models, and view models when they have genuinely different shapes or responsibilities. Do not create three identical interfaces and pass-through mappers for every response.
- Use `unknown` for genuinely unknown values, including catch variables, generic validation inputs, and untrusted input. Narrow it where knowledge becomes available. Do not use `any`, casts, or suppression comments to evade a known contract mismatch.
- Preserve required fields. Do not make them optional or assert an unrelated type merely to silence an error.

## Contract trust and validation boundaries

Static types and type assertions do not validate runtime input. Identify real trust boundaries such as API responses, storage, URL input, messages, user JSON, and third-party integrations; apply the project's validation policy and the consequences of malformed data. Do not invent endpoints, fields, or enum values.

Validate/parse once **per trust-boundary crossing** where needed, then expose the established internal type. Do not repeat the same structural validation in every consumer. A new boundary, a business invariant, authorization, or a value changed since validation may require a different check; this rule does not remove those checks.

Inside the trusted domain:

- Access required values directly. Avoid defensive optional chaining, normalization, and defaults that conceal a producer or contract bug.
- Use `?.` only where that receiver is actually nullable/optional; use required nested fields directly. Consider whether an optional access/call's resulting `undefined` is permitted by the consumer.
- Preserve intentional nullable fields, search misses, partial drafts, and loading states. Narrow genuine unions before accessing variant-specific properties; this is not redundant validation.
- Add a fallback only when the contract/product defines that missing-value behavior. Keep `0`, `false`, and empty strings when valid; see [default semantics](control-flow-and-data-transformations.md#preserve-semantics).
- Fix a wrong producer, type, or boundary parser instead of making all downstream consumers guess. Do not catch contract failures merely to return empty plausible data.

## Placement and verification

Keep contracts with their owner: request/response types at the API or generated-client boundary, view types near the view/mapper, private types near their function/component. Promote only actual shared contracts using [shared-module rules](project-shared-modules.md).

Check changed code with the project's type checker and relevant boundary/variant cases. Verify both missing/invalid external values and valid internal values; passing a type check alone does not establish runtime validity.
