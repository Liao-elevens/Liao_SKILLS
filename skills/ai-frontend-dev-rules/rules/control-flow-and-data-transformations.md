# Control flow and data transformations

## About / 简介

**EN:** Choose a control structure by the decision it expresses and preserve evaluation semantics when simplifying it.

**中文：** 按判断的实际含义选择对象映射、集合判断、switch 或 if，并在简化时保留原有求值语义。

## Select the simplest suitable structure

| Trigger | Prefer | Keep another structure when |
| --- | --- | --- |
| A finite key selects a fixed value/label/config | Object lookup | Branches contain conditions, side effects, or different computations |
| One value is compared against several allowed values | `includes`, or a `Set` for a reused/larger membership collection | A couple of direct comparisons is clearer; comparison semantics differ |
| A discriminator chooses different workflows or payload shapes | `switch` with explicit returns/breaks and coverage | Ranges or ordered overlapping predicates are involved |
| A key selects handlers with the same input/output contract | Function map | Signatures differ, narrowing is lost, or casts/adapters obscure the call |
| Ranges, combined conditions, or priority rules | `if` / `else if` | A genuine value mapping captures the entire decision |
| Invalid or finished cases obscure the main path | Early return/guard | Cleanup or ordering requires a structured branch |
| A simple two-way choice | `if` or one ternary | Either branch becomes a workflow needing statements |

Do not count `if`, `||`, or `&&` operators as violations. Remove repeated knowledge, not necessary decisions. Avoid nested ternaries; name complex predicates or use explicit branches.

## Preserve semantics

- `||` supplies a fallback for all falsy values; `??` only for `null`/`undefined`; destructuring/default parameters only replace `undefined`. Choose from the contract, not visual brevity. Preserve legitimate `0`, `false`, and `''`.
- Short-circuit evaluation may intentionally skip work. Do not replace branches with an object whose values eagerly call every handler. Store functions when dispatch is appropriate.
- Keep priority, evaluation order, call counts, exceptions, and side effects. A guard must not skip required cleanup.
- Object keys coerce to strings/symbols; they are not a replacement for arbitrary object/number identity. Use `Map` when its key semantics are required. `includes`/`Set` treat `NaN` as equal to itself, unlike `===`; account for this if it is in the domain.
- A closed, trusted key union can index an exhaustive map directly. At a real open/untrusted boundary, define missing-key behavior and exclude inherited properties as needed using the project's supported own-key check, a null-prototype object, or `Map`. Do not add unknown fallbacks to closed contracts.
- Prevent unintended `switch` fallthrough. Check closed variants using the project's exhaustiveness pattern (for example a `never` check) or focused tests. A silent `default` must not conceal a newly added variant.

Use [mapping rules](utils-data-mapping.md) for display data and [type rules](type-standards.md) for narrowing and validation. See [decision examples](../references/code-quality-examples.md#choose-by-decision-meaning) and [semantic counterexamples](../references/code-quality-examples.md#preserve-defaults-and-evaluation).

## Collections

| Intent | Prefer | Semantic check |
| --- | --- | --- |
| Transform each element | `map` | Do not use it only for side effects |
| Select elements | `filter` | Keep expected order and duplicates |
| Check existence | `some` | Short-circuiting must not skip required side effects |
| Find one item | `find` | Handle absence according to the contract |
| Visit with effects or several accumulators | A clear loop or project idiom | Preserve iteration order, early exit, and mutation |
| Aggregate a simple value | `reduce` or a clear loop | Avoid obscure accumulators and repeated growing-object/array spreads |

Keep a short readable chain. Use intermediate names or a loop if a chain hides several domain operations. Do not impose `reduce` or ban loops.

- Do not mutate caller-owned arrays with `sort`/`reverse` unless mutation is part of the contract. Use the project's supported non-mutating approach when needed.
- Preserve deduplication precedence and ordering; first-wins and last-wins are different behaviors.
- `filter(Boolean)` removes all falsy values, not just nullish ones. Use a nullish predicate if `0`, `false`, or `''` is valid.
- Avoid object/array/JSON round trips that add no meaningful transformation.
- Build indexes only when input size and repeated lookup cost justify them. A one-off small lookup does not need a cached `Map`.
