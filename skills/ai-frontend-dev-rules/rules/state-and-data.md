# State and data

## About / 简介

**EN:** Keep state minimal, use the current framework's reactive model, and make async ownership explicit.

**中文：** 保持状态精简，遵循当前框架的响应式习惯，并明确异步调用、错误和清理的归属。

## State ownership

Use the smallest scope that satisfies actual consumers: component, nearby shared parent, feature, then genuinely shared app state. Do not create global state for an isolated page or duplicate a server cache in another store.

- Derive values from their source instead of storing a second value and synchronizing it. Separate editable drafts, snapshots, optimistic changes, and undo history are valid when their independent lifecycle is intentional.
- Use a status/variant for mutually exclusive phases (`idle`, `loading`, `success`, `error`) when it rules out impossible combinations. Keep independent flags for genuinely independent concerns.
- Lift state for real shared consumers; do not create a hook/composable/store for every field. Use a reducer or state machine when actual transition complexity warrants it.
- Reuse an existing query/cache/loader/resource's data, loading, and error states. Add retry, staleness, persistence, or caching only when the workflow requires them.

## Framework adaptation and lifecycle

| Stack | Apply the principle using existing conventions |
| --- | --- |
| Vue | `computed` is normal derived state in both Options API and Composition API, not an optimization requiring a measured bottleneck. Use watchers for actual side effects, not copying a calculation into another ref. |
| React | Calculate simple derived values during render. Use Effects for external synchronization, not for pure calculations or ordinary user-event logic. Do not add `useMemo` by default. |
| Angular | Follow the installed version's component/service and reactive conventions; use the existing signal/computed or observable approach where appropriate. |
| Svelte | Follow the installed version and project's reactive syntax; do not migrate legacy reactivity to newer APIs as incidental cleanup. |
| Other stacks | Use native derivation and lifecycle mechanisms. Do not translate React hook rules mechanically into another framework. |

Keep user actions in event/workflow handlers. A short lifecycle callback can remain inline; extract a named operation when requests, transformations, conditions, and error handling obscure its purpose. Do not require a controller/service layer for simple work.

Effects, watchers, subscriptions, and requests must retain cleanup, cancellation, or stale-result handling when work can outlive its owner or be superseded. Preserve intentional order and avoid applying a stale response to a newer selection. Use existing framework/query-library support before building another mechanism.

## Async calls and error ownership

**Do not use unary `void` before function calls.** This includes `void submit()`, `void refresh()`, `() => void reload()`, and `void (async () => { ... })()`. This is an explicit coding convention; unary `void` discards a result and does not handle a rejection.

The restriction is about expressions, not types. Keep legitimate `(): void`, `() => void`, and `Promise<void>` annotations. Use syntax-aware linting/review if enforcing it automatically; searching for the word `void` cannot distinguish these cases.

| Call meaning | Required handling |
| --- | --- |
| Synchronous call | Call it directly; discard an unused result normally |
| Caller needs completion, result, or error propagation | `await` it in an appropriate async flow, or return the promise to a caller that owns it |
| Deliberate background work | Use the project's task owner, or attach explicit rejection handling; its error handler must not itself leave an unhandled rejection |
| Framework/library owns a promise | Return/pass it through its documented async API; verify that the API actually awaits or handles failure |
| UI callback API ignores its return value | Handle failure in the callback or use a synchronous callback that attaches rejection handling |

Do not just remove `void` and leave a rejecting promise unowned. Do not mechanically add `await` and serialize independent work. A callback typed `() => void` alone does not prove that a returned promise is handled. Do not evade the rule with casts, discard wrappers, or lint suppressions.

Start independent requests together when appropriate; keep dependent calls sequential. Choose `Promise.all` for collective failure semantics or `allSettled` when partial results must be handled. Neither choice automatically cancels other requests.

Catch errors where the code can recover, add useful context, or present the product's error state. Otherwise propagate to the known owner. Avoid stacked catch/log/toast layers, empty catches, unchanged catch-and-rethrow, and failure converted to `[]` or success-like defaults. Distinguish expected cancellation from an actionable failure using the project's convention. Cleanup belongs in the lifecycle owner or `finally` as appropriate.

See [async examples](../references/code-quality-examples.md#async-calls-without-unary-void).

## Dependencies

Use existing state and request tools. If proposing a new library, explain its concrete benefit, tradeoffs, and cost against the current approach before adoption; a short comparison table helps when several options matter. Follow the user's dependency authorization requirements and do not install/download a new library without the required approval. Existing authorization for the specific dependency need not be requested again.

## Verify

Check source vs derived state, intentional drafts, success/failure ownership, overlapping requests, and disposal where relevant. Use the actual framework's behavior; a plain JavaScript calculation test does not prove lifecycle integration.
