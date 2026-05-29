# State and data

## About / 简介

**EN:** How to choose local state, feature state, shared stores, server-data caches, and request libraries while respecting the project's existing stack.

**中文：** 约定如何选择局部状态、功能状态、共享 store、服务端数据缓存和请求库，并优先遵循项目已有技术栈。

## How to use

Start with the smallest state scope that satisfies the feature. Use libraries and patterns already present in the project. Do not install or download a new state/request library unless the user explicitly approves it after reviewing a comparison table.

---

## 1. Local UI state

- Use component/view-local state for UI state that belongs to one component or a small subtree.
- Keep derived values computed from source data instead of storing duplicate sources of truth.
- Use reducers, state machines, computed values, or framework equivalents when transitions become complex.

## 2. Feature scope

- Lift state to the feature entry, a feature-level state module, a hook/composable/service, or another project-standard feature boundary when multiple child modules need it.
- Keep feature providers, contexts, stores, or services close to the feature unless multiple features reuse them.
- Keep form state, table state, filters, pagination, and selection state explicit and easy to reset.

## 3. Global or shared state

- Do not introduce global state for one-off pages or isolated widgets.
- Use the existing global solution only when the data is genuinely shared across distant features, routes, sessions, or app shell concerns.
- Keep global stores focused on durable app state. Avoid storing transient UI details globally unless the project already does this intentionally.

## 4. Server data

- Prefer the project's existing request, cache, query, loader, resource, or service pattern.
- Keep loading, empty, error, retry, and stale states explicit.
- Avoid request waterfalls and duplicated fetching for the same data.
- Keep mutation success/failure behavior aligned with project UX and API rules.

## 4.1 Effect / lifecycle data orchestration

- Keep lifecycle hooks focused on triggering work and cleaning it up. Lifecycle entry points should mainly express when work starts, when it should rerun, and how it is disposed.
- Move non-trivial async work into named functions, services, hooks, composables, controllers, stores, or framework-equivalent modules. This includes request orchestration, sequential or parallel calls, result normalization, loading state updates, and failure handling.
- Name async functions by user-facing or domain intent, such as `loadOptions`, `refreshList`, `syncProfile`, or `submitForm`, instead of vague names that only describe implementation mechanics.
- Make stale response handling explicit for async work started by lifecycle hooks. Account for unmounts, dependency changes, route changes, subscription disposal, cancellation, abort signals, or the framework's equivalent mechanism.
- Choose data ownership by consumer scope. Keep data local when one component or view consumes it; lift it to a shared parent or feature-level state module when nearby modules share it; promote it to shared or global state only when reuse crosses feature, route, session, or ownership boundaries.
- Treat complex lifecycle callbacks as a split signal. If a lifecycle callback combines multiple requests, nested loops, data transformation, branching, loading/finally handling, and user-visible error logic, split the workflow into named units before adding more behavior.

## 4.2 New state/request library approval

If a third-party state or request library not currently used by the project appears to be a better fit, do not install or download it immediately.

Before using it:

1. Identify the current project state/request libraries and patterns.
2. Identify the proposed third-party library and why it may be better.
3. Present a comparison table to the user.
4. Ask whether the user wants to adopt the new library.
5. Only install/download/use the new library after the user confirms.

Use this table format:

| Option | Pros | Cons | Fit for this task |
|--------|------|------|-------------------|
| Current project library/pattern | Existing dependency, familiar to the codebase, no install needed | List limitations for this task | Explain whether it can satisfy the requirement |
| Proposed third-party library | List concrete benefits for this task | New dependency, migration/learning burden, bundle impact, maintenance risk | Explain why it may be better |

If the user does not confirm the new library, implement the feature with the project's existing state/request library or pattern.

## 5. Checklist

- [ ] State scope matches actual consumers.
- [ ] No duplicate sources of truth were introduced.
- [ ] Server data uses the project's existing request/cache pattern where available.
- [ ] Async effects/subscriptions have cleanup or stale-response handling where needed.
- [ ] No new state/request library was installed or used without user approval after a comparison table.
