# Frontend performance

## About / 简介

**EN:** Remove evident waste and optimize when actual workload or measurements justify the added complexity.

**中文：** 消除明显浪费，只在实际规模或测量结果支持时增加性能优化机制。

## Avoid default optimization layers

Do not add memoization, caches, debounce/throttle, virtualization, or elaborate indexes by default. Use them for measured bottlenecks, evident workload costs, or concrete behavioral/identity requirements. Document cache ownership and invalidation when adding a cache.

Framework-native derived state is not the same as optional optimization: Vue `computed` can be the ordinary correct model without a benchmark. React's simple derived values can be calculated during render. Preserve framework-required stable identities and dependencies; see [framework adaptation](state-and-data.md#framework-adaptation-and-lifecycle).

## Fetching and rendering

- Remove accidental serial waterfalls for independent calls without changing dependency or failure semantics. Use [async ownership](state-and-data.md#async-calls-and-error-ownership) for sequencing, cancellation, and stale responses.
- Reuse existing server caches and avoid refetching stable data on every update unless required by freshness semantics.
- Keep updates near actual consumers; avoid unnecessary broad state propagation. Do not split components solely on an assumed rerender benefit.
- Use stable list identity and consider pagination/virtualization when data size and UX justify it.
- Watch for repeated full scans in hot paths, growing accumulator copies, and redundant conversions; use [collection rules](control-flow-and-data-transformations.md#collections) without optimizing tiny one-off work speculatively.

## Bundles and loading

Preserve route and browser/server boundaries. Keep rarely used heavy editors, charts, maps, and media paths lazy when the framework supports it and the workload warrants it. Grouping utilities must not pull a heavy or incompatible dependency into every consumer.

Use existing helpers or native APIs before adding a dependency. Follow dependency authorization requirements. Keep assets sized for their actual use and avoid loading large media in the initial bundle accidentally.

## Verify the claim

Use available profiling, bundle analysis, request traces, or representative measurements to substantiate a performance claim. Type/lint/build success only shows compatibility. For ordinary changes, check relevant evident costs and report any performance claim that remains unmeasured; do not invent benchmark work without a concern.
