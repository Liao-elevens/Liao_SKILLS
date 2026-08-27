# Type and schema standards

## About / 简介

**EN:** Type, schema, and data-contract rules for AI-written frontend code across typed and untyped stacks.

**中文：** 面向任意前端技术栈的类型、Schema 和数据契约规范，帮助 AI 生成更清晰、更可维护的代码。

## How to use

Apply this file to new or changed frontend modules. Use the project's existing type system or validation approach: TypeScript, Flow, JSDoc, runtime schemas, prop validators, generated API types, framework model files, or another established convention.

---

## 1. Must

- Export contracts that cross module boundaries, such as component props, API shapes, domain models, store state, event payloads, route params, and shared utility inputs/outputs.
- Keep request/response contracts close to the API/service modules that own them, unless the project has a generated or central contract system.
- Use the project's existing naming style, but prefer domain names over generic names such as `Data`, `Item`, `Info`, or `Result` without context.
- When the project uses TypeScript, use `unknown` only for raw values at an explicitly identified untrusted boundary and narrow or validate them once before exposing a concrete trusted type.
- When the project does not use TypeScript, use the established alternative: JSDoc, schema validators, prop validators, generated clients, or clear model documentation.

## 1.1 Contract trust and validation boundaries

- Treat values with an established static type as trusted inside the typed application domain. Use required fields directly.
- Use optional chaining only when the receiver at that exact access step is declared optional or nullable. Do not propagate optional chaining through required nested fields merely because an earlier receiver is optional.
- Account for the resulting expression type. For example, `obj.arr?.map(...)` returns `undefined` when `arr` is absent and is appropriate only when that result is intentional.
- Contract violations should fail visibly during development, testing, or runtime rather than being converted into plausible fallback values.
- Perform runtime validation only at explicitly identified untrusted boundaries, such as raw network responses when the project requires runtime verification, browser storage, URL input, `postMessage` payloads, user-authored JSON, or third-party JavaScript data.
- Validate or parse an untrusted value once when it enters the trusted domain. After parsing succeeds, expose a concrete typed model and do not revalidate it downstream.
- Do not introduce runtime schemas or validators merely because static types exist. Runtime validation requires an actual untrusted boundary or an explicit project requirement.
- When the runtime value violates its declared contract, fix the contract, generated type, producer, or boundary parser instead of adding consumer-side patches.

## 2. Avoid

- Unnecessary `any`, overly wide object types, or unvalidated external data.
- Silent type suppression comments when the type issue can be fixed or isolated behind a typed wrapper.
- Duplicating the same DTO/model/shape in multiple files.
- Mixing backend DTOs, domain models, and UI view models without clear naming or conversion boundaries.
- Guessing field names, enum values, route params, or query shapes when the API/requirement is unknown.
- Optional chaining on required receivers or fields, such as `user?.profile?.name` when the contract requires `user.profile.name`.
- Fallback defaults such as `items ?? []`, `name || ''`, or `count ?? 0` when the contract does not explicitly define that fallback behavior.
- Type guards, `safeGet` helpers, repeated narrowing, or runtime type checks for values already trusted by the internal contract.
- Revalidating, reparsing, or renormalizing a value after it has crossed its designated validation boundary.
- Catching contract errors only to return an empty value or continue with incomplete data.
- Weakening a required field to optional merely to silence a type error.

## 3. Files

- Feature-specific contracts belong with the feature module.
- Shared contracts belong in the project's shared type/model/schema location only when multiple features use them.
- Generated contracts should stay in the generated-client location and be wrapped or adapted only where the project convention requires it.
- View models should live near the UI or mapper that creates them, not inside low-level API functions unless that is the project pattern.

## 4. Checklist

- [ ] Public functions, modules, components, stores, and services have clear input/output contracts.
- [ ] Explicitly untrusted external data is parsed once at its owning boundary before entering trusted UI code.
- [ ] Required typed fields are accessed directly, and every optional chain corresponds to declared optionality at that exact access step.
- [ ] Optional calls and accesses produce an optional result only where the consumer intentionally supports it.
- [ ] No guard, fallback, or optional chain hides a contract violation.
- [ ] Every runtime validator corresponds to an identified untrusted boundary, and each value is validated at most once before entering trusted code.
- [ ] API/service contracts match the backend or documented mock contract.
- [ ] No unnecessary `any`, untyped payloads, or silent suppression comments were introduced.
