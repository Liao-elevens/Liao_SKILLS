# Backend API integration

## About / 简介

**EN:** Reuse the project's request boundary and keep transport, contracts, adaptation, and product errors clearly owned.

**中文：** 复用项目已有请求边界，明确传输、契约、数据转换与用户错误提示的职责。

## Existing boundary first

Identify the current request client, auth handling, API/generated contracts, loader/service pattern, and error convention before adding another abstraction. Keep raw HTTP details out of presentational components when a project boundary already owns them.

If none exists, add the smallest useful feature-local boundary. Framework-native loaders, server actions, services, and resources can already provide it; do not force every stack into an API → repository → service → hook chain.

- A thin API function is useful when it owns the endpoint, contract, transport configuration, or stable public interface. Do not remove it solely because it is short; see [abstraction decisions](functions-and-abstraction.md#wrappers-and-generalization).
- Keep request/response contracts with their API/generated owner. Transform DTOs into view models only when the shape or responsibility actually differs.
- Put non-trivial adaptation near its owner, away from repeated rendering. Trivial local display expressions can remain local.
- Name exported operations clearly (`fetchProfile`, `submitResult`, or domain-qualified forms when caller context requires them). Preserve backend names at the external contract.

## Responses and errors

Use the existing definitions of transport and business success; an HTTP success response can still represent a documented business failure. Preserve the project's authentication, token refresh, redirect, and permission behavior for `401`/`403`.

Validate untrusted data where the project's policy and risk require it, then return the established internal contract. Do not revalidate in each consumer; follow [type and trust-boundary rules](type-standards.md#contract-trust-and-validation-boundaries).

Show product errors at the existing workflow/error owner; avoid API wrappers that only add generic toasts and duplicate upper-layer notifications. Handle or propagate failures intentionally using [async error ownership](state-and-data.md#async-calls-and-error-ownership). Keep loading, empty, and failure states distinct.

## Configuration and unknown contracts

Use the existing configuration mechanism for public base URLs and runtime settings. Public frontend configuration must not contain secrets. This skill does not authorize reading or changing sensitive environment files; follow the user's and project's access rules. Check permitted configuration schemas/examples for key consistency rather than exposing sensitive values.

Do not guess endpoint paths, parameters, enum values, or response fields. Confirm the contract, or use an explicitly agreed mock/stub and report its limitation. A TODO/mock marker does not make an unfinished integration complete.

## Verify

Check actual request parameters, success/business-failure handling, authentication behavior, mapping, and user-visible errors for the affected workflow. Preserve runtime and lazy-loading boundaries when moving request code.
