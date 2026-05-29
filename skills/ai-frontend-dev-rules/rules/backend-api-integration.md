# Backend API integration

## About / 简介

**EN:** HTTP calls should live behind the project's dedicated API/service layer. Pages, views, and components should call typed wrappers, hooks, services, or adapters rather than owning low-level request details.

**中文：** HTTP 调用应收口到项目已有的 API / service 封装层。页面、视图和组件应调用类型明确的封装方法、hooks、services 或 adapters，而不是直接承载底层请求细节。

## How to use / 使用方法

**EN:** First identify the project's existing API layer, request client, environment configuration, auth handling, error handling, and data adaptation conventions. Follow those conventions before introducing new folders, clients, wrappers, or response shapes.

**中文：** 先识别项目已有的 API 层、请求客户端、环境配置、鉴权处理、错误处理和数据适配约定。新增目录、客户端、封装方法或响应结构前，应优先沿用已有约定。

---

## 1. Configuration and environments

- Use the project's existing environment/configuration mechanism for base URLs, feature flags, mock endpoints, and public runtime settings.
- If the project has multiple environment files, keep required keys consistent across those files.
- Do not commit secrets, private tokens, or production-only credentials into frontend configuration.
- Mark placeholder, mock, or unknown endpoints explicitly with a `TODO`, mock flag, or project-standard marker.

## 2. API layer structure

- Use the project's existing API, service, client, repository, or data-access layer.
- If no API layer exists, create the smallest project-appropriate boundary near the feature first; promote it to shared code only when multiple features need it.
- Keep HTTP transport details, request typing, and response typing out of page/view/component files.
- Put backend DTOs, frontend view models, and UI option data at the boundary where the project convention expects them. Do not mix all three inside rendering components.
- Keep data adaptation close to the boundary that owns the transformation: API adapter, feature service, hook/composable, or view-model utility.

## 3. Rules

| Area | Rule |
| --- | --- |
| Existing conventions | Reuse the project's request client, auth flow, environment config, and error/display patterns before adding new ones. |
| No raw HTTP in UI | Avoid scattered `fetch`, `axios`, or equivalent direct request calls in pages, views, and presentational components when the project has an API/service boundary. |
| Auth failures | Handle `401` / `403` according to the project's login, refresh-token, redirect, or permission-denied convention. |
| Transport success | Define transport success using the project's request library or HTTP status convention. Non-success responses must be handled or propagated intentionally. |
| Business success | If the backend has business status fields such as `code`, `success`, or `message`, parse them at the API/service boundary or call site according to existing project convention. |
| User-visible failure | Show user-visible errors at the workflow/call site using product copy and the project notification pattern. Avoid low-level API wrappers whose only role is to show generic failure messages. |
| Types and schemas | Type or validate request params, response payloads, and adapted frontend models when the project supports TypeScript, schemas, generated clients, or runtime validators. |
| Data adaptation | Keep DTO-to-view-model conversion out of render-heavy components unless the transformation is trivial and local. |
| Comments | Add comments or JSDoc when the endpoint, business meaning, or transformation is not obvious, using the project's normal documentation language. |
| Errors | Handle or propagate errors intentionally; no empty `catch`. |
| Unknown contracts | Do not guess endpoint paths, params, or response fields. Use an explicit mock/TODO marker until the contract is confirmed. |
| Loading / empty / error | Match the project's established loading, empty, retry, and error-state UI patterns. |

## 4. Naming

- Use clear verb + resource names for API functions, such as `fetchUserProfile`, `submitLessonResult`, or the project's equivalent naming convention.
- Use backend contract names for DTOs and frontend domain names for view models when the project distinguishes them.
- Avoid generic names such as `requestData`, `getList`, or `handleApi` when a domain-specific name is available.

## 5. Checklist

- [ ] Existing API/service/request conventions were identified before adding new API code.
- [ ] No page/view/component owns low-level HTTP details when a service boundary exists.
- [ ] Environment/config keys follow the project's existing mechanism and are consistent where required.
- [ ] Auth failure behavior follows the project's login/permission convention.
- [ ] Transport success and business success are both handled according to the project contract.
- [ ] User-visible failures use product copy and the project notification pattern at the workflow/call site.
- [ ] Request params, response payloads, and adapted frontend models are typed or validated where the project supports it.
- [ ] DTO-to-view-model conversion has a clear owner.
- [ ] Unknown endpoints or fields are marked as mock/TODO rather than guessed.
- [ ] Errors are handled or propagated intentionally; no empty `catch`.
