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
- When the project uses TypeScript, prefer `unknown` over `any` at external boundaries and narrow before use.
- When the project does not use TypeScript, use the established alternative: JSDoc, schema validators, prop validators, generated clients, or clear model documentation.

## 2. Avoid

- Unnecessary `any`, overly wide object types, or unvalidated external data.
- Silent type suppression comments when the type issue can be fixed or isolated behind a typed wrapper.
- Duplicating the same DTO/model/shape in multiple files.
- Mixing backend DTOs, domain models, and UI view models without clear naming or conversion boundaries.
- Guessing field names, enum values, route params, or query shapes when the API/requirement is unknown.

## 3. Files

- Feature-specific contracts belong with the feature module.
- Shared contracts belong in the project's shared type/model/schema location only when multiple features use them.
- Generated contracts should stay in the generated-client location and be wrapped or adapted only where the project convention requires it.
- View models should live near the UI or mapper that creates them, not inside low-level API functions unless that is the project pattern.

## 4. Checklist

- [ ] Public functions, modules, components, stores, and services have clear input/output contracts.
- [ ] External data is narrowed, validated, or adapted before deep UI usage.
- [ ] API/service contracts match the backend or documented mock contract.
- [ ] No unnecessary `any`, untyped payloads, or silent suppression comments were introduced.
