# Code quality examples

Use the relevant cases when applying or reviewing the rules. These are focused examples, not a required project architecture. Preserve the stated preconditions; a shorter alternative is not automatically equivalent.

## Contents

- [Short names with enough context](#short-names-with-enough-context)
- [Helpers and folder granularity](#helpers-and-folder-granularity)
- [Choose by decision meaning](#choose-by-decision-meaning)
- [Preserve defaults and evaluation](#preserve-defaults-and-evaluation)
- [Async calls without unary void](#async-calls-without-unary-void)
- [Framework-native derived state](#framework-native-derived-state)
- [Useful boundaries and accidental similarity](#useful-boundaries-and-accidental-similarity)

## Short names with enough context

Inside a component with one user selection:

| Before | Prefer | Retain more context when |
| --- | --- | --- |
| `currentlySelectedUserIdentifier` | `selectedId` | Several entity kinds are selected: use `selectedUserId` |
| `handleUserFormSubmitEvent` | `handleSubmit` | Several independent forms have handlers in the same scope |
| `isUserDataCurrentlyLoading` | `isLoading` | User loading must be distinguished from another request |

Keep `timeoutMs`, `sourceId`, `targetId`, `previousTotal`, and a public `fetchUserProfile` where those distinctions matter. Do not replace them with `timeout`, `id1`, `id2`, `total`, or `fup` just to shorten names. See [readability](../rules/code-readability.md).

## Helpers and folder granularity

A small feature's private helpers can stay beside their sole consumer. Several small helpers used by neighboring components belong together in its existing `utils.ts`, `util.ts`, or utility implementation file, according to project convention.

Avoid fragmenting the same small feature:

```text
orders/utils/
  format-price/index.ts
  format-date/index.ts
  calc-subtotal/index.ts
  calc-total/index.ts
```

When a growing helper file contains distinct groups that would read better separately, prefer:

```text
orders/utils/
  totals.ts     # subtotal, tax, total calculations
  filters.ts    # shared order-selection predicates
  display.ts    # amount/date/status presentation
```

The files stay in `utils/`; each can contain several functions. Do not introduce both `utils.ts` and a competing `util/` for the same role. Around 300 lines prompts a cohesion review, not a forced split.

Cases to leave together: a 330-line cohesive algorithm; 340 lines of flat static config; several 10-line helpers with their own test cases. Cases that can split earlier: a 40-line browser-only adapter and server-only code; a small helper importing a heavy lazy-loaded editor. A 300-line count does not override runtime boundaries. See [module layout](../rules/ui-module-split.md).

## Choose by decision meaning

**Fixed labels:** a closed contract allows direct, exhaustive lookup instead of repeated branches. This example uses TypeScript `satisfies`; on older compilers use the project's supported annotation pattern.

```ts
type Status = 'draft' | 'sent' | 'paid'

const labels = {
  draft: 'Draft',
  sent: 'Sent',
  paid: 'Paid',
} satisfies Record<Status, string>
```

Inside a caller whose `status` has type `Status`, use `labels[status]` directly. Do not add a wrapper solely to rename this lookup. A component needing only ordered options can instead own a plain option list; it need not create every representation.

**Membership:** for strings, `['draft', 'sent'].includes(status)` can express a repeated same-field membership check. A reused larger collection may warrant a `Set`. Keep `status === 'draft'` or a simple two-value comparison when already clear. Do not replace `Number.NaN === value` with membership and assume identical results.

**Different payloads:** use a discriminated `switch` when each operation needs different fields. Forcing these handlers into one map would obscure narrowing.

```ts
type Action =
  | { kind: 'open'; id: string }
  | { kind: 'search'; query: string }
  | { kind: 'close' }

function actionText(action: Action): string {
  switch (action.kind) {
    case 'open':
      return `Open ${action.id}`
    case 'search':
      return `Search ${action.query}`
    case 'close':
      return 'Close'
    default:
      return unreachable(action)
  }
}

function unreachable(value: never): never {
  throw new Error(`Unexpected action: ${String(value)}`)
}
```

Use the project's existing exhaustiveness helper if present. A map is suitable for handlers with the same signature; do not cast unlike handlers to fit one.

**Keep ordered conditions:** a priority rule such as “blocked first, then overdue, then normal” naturally uses guards or ordered `if` branches. Ranges such as age bands also belong in conditions. `isOpen ? 'Hide' : 'Show'` is a readable binary expression and needs no abstraction. See [control-flow rules](../rules/control-flow-and-data-transformations.md).

## Preserve defaults and evaluation

```ts
// Deliberately different contracts:
const pageSize = suppliedSize ?? 20   // retains 0
const title = suppliedTitle || 'Untitled' // replaces an empty string too
const { enabled = true } = settings  // defaults undefined, not null or false
```

Do not change between these forms without confirming the intended missing-value behavior. Likewise, `[0, false, '', null, undefined].filter(Boolean)` is not a nullish filter. When only nullish entries are absent, use a predicate such as `value !== null && value !== undefined` with the project's supported type narrowing.

Avoid eager action tables:

```ts
// Wrong when only one action should run:
const result = { save: save(), remove: remove() }[action]
```

If `save` and `remove` truly share a call contract, a function map invokes only the chosen action:

```ts
const handlers = { save, remove }
const result = handlers[action]()
```

Keep a `switch` if they need different arguments or ownership. For a trusted closed key set, index directly. For an open string at a genuine boundary, guard ownership:

```ts
const externalLabels: Readonly<Record<string, string>> = { draft: 'Draft' }

function externalLabel(key: string): string {
  const label = Object.prototype.hasOwnProperty.call(externalLabels, key)
    ? externalLabels[key]
    : undefined
  return label ?? 'Unknown'
}
```

The explicit missing-value result also supports TypeScript `noUncheckedIndexedAccess`. An alternative is `Map<string, string>` with declared unknown handling. The boundary must reject inherited keys such as `toString`; closed trusted maps do not need this defensive wrapper.

Collection checks also preserve order, input mutation, duplicate precedence, and callback effects. Replacing `filter(...).length > 0` with `some(...)` is suitable for a pure predicate; a predicate with required effects on every element is not equivalent.

## Async calls without unary void

These expression forms are forbidden:

```ts
void submit()
void refresh()
const onReload = () => void reload()
void (async () => { await save() })()
```

A UI handler that owns failure can await completion inside its error boundary. Here `save` returns a promise and `showError` is the existing synchronous, non-throwing presentation handler:

```ts
async function handleSubmit(): Promise<void> {
  try {
    await save()
  } catch (error: unknown) {
    showError(error)
  }
}
```

A callback API that expects a synchronous callback can attach error handling:

```ts
function handleClick(): void {
  save().catch(showError)
}
```

This works only when `showError` safely handles the failure; if it throws or returns a rejecting promise, another unowned rejection remains. Prefer an existing task owner where appropriate. Do not add a generic discard wrapper or suppress a floating-promise warning.

Valid types remain valid:

```ts
type Listener = () => void
async function submit(): Promise<void> {
  await save()
}
```

The caller of `submit` still owns its promise. Independent calls may start together with `Promise.all` when collective failure is intended; dependent calls must retain ordering. See [async rules](../rules/state-and-data.md#async-calls-and-error-ownership).

## Framework-native derived state

In an existing Vue Composition API component, derive a total normally:

```ts
const total = computed(() => items.value.reduce((sum, item) => sum + item.price, 0))
```

Do not replace this with a ref plus a watcher just to avoid “memoization.” An Options API component can use its existing `computed` option; no API-style migration is implied.

In an existing React component, a simple calculation usually stays in render:

```ts
const total = items.reduce((sum, item) => sum + item.price, 0)
```

Do not add a second state value and an Effect to keep it synchronized, or add `useMemo` without a need. These snippets assume the framework imports and component context already exist; they are not standalone applications.

Keep an editable draft separate from saved data when editing and cancellation need that lifecycle. A watcher/Effect that synchronizes a real external system can also be appropriate. Use the project's existing query status instead of inventing duplicate loading flags. See [state rules](../rules/state-and-data.md).

## Useful boundaries and accidental similarity

| Case | Decision and reason |
| --- | --- |
| `const readLabel = (status: Status) => labels[status]` used once with no extra domain role | Inline the lookup; the function adds only navigation |
| A short API function owns `/orders`, authentication options, and an established return contract | Keep it; consumers should not repeat transport knowledge |
| Two similar formulas represent tax and loyalty rules that evolve independently | Keep separate; syntax is not shared business knowledge |
| Three nearby components format the same order amounts under one contract | Group the common behavior in feature utilities |
| A generic renderer needs many mode flags for unrelated layouts | Prefer explicit components/composition with smaller interfaces |
| An existing platform adapter is only one line today | Keep its required external/runtime boundary |

See [functions and abstraction](../rules/functions-and-abstraction.md) and [shared-module rules](../rules/project-shared-modules.md).
