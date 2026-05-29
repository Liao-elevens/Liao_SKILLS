# Frontend performance

## About / 简介

**EN:** General frontend performance rules for data fetching, rendering, bundle size, loading behavior, and verification across frameworks.

**中文：** 面向任意前端技术栈的通用性能规范，覆盖数据请求、渲染更新、包体积、加载体验和交付校验。

## How to use

Use this file when writing, reviewing, or refactoring frontend code that affects data loading, rendering, lists, routing, bundle size, assets, or user-perceived responsiveness. Prefer the project's existing profiling, build, and monitoring tools.

---

## 1. Data fetching

- Avoid serial request waterfalls when independent data can be requested in parallel.
- Add cancellation, stale-response guards, or framework-equivalent cleanup for async work that can outlive the current view.
- Keep loading, empty, error, and retry states explicit and aligned with project UX.
- Reuse the project's server-data cache/request layer when it exists.
- Avoid refetching stable data on every render/update/navigation unless the product requires it.

## 2. Rendering and updates

- Avoid broad parent state updates that force unrelated child UI to rerender or recompute.
- Keep derived values computed from source data instead of duplicating state.
- Use memoization, computed values, selectors, or framework equivalents only when there is clear churn, expensive work, or measured benefit.
- Keep list keys stable. Avoid index keys for mutable lists.
- Virtualize or paginate large lists only when the list size and UX justify it.

## 3. Bundle and loading

- Preserve route/page/screen-level lazy loading when the project uses it.
- Do not add heavy dependencies when a small existing helper or native API is enough.
- Split rarely used heavy code paths, editors, charts, maps, or media tools when supported by the bundler/framework.
- Keep assets appropriately sized and compressed. Avoid importing large media into the initial bundle by accident.

## 4. Verification

Use the project's available verification path: build, type check, lint, tests, storybook, bundle analyzer, performance profiler, browser performance tools, or monitoring dashboards.

If no formal performance tool exists, at minimum check:

1. Independent requests are not accidentally serialized.
2. New dependencies are necessary and scoped.
3. Large lists have stable keys and reasonable rendering behavior.
4. New loading/error states do not block unrelated content.

## 5. Checklist

- [ ] No obvious fetch waterfall was introduced.
- [ ] Async work has stale-response or cleanup handling where needed.
- [ ] State changes are scoped to actual consumers.
- [ ] Large lists use stable keys and avoid unnecessary full rerenders.
- [ ] Bundle impact was considered for new dependencies or heavy modules.
- [ ] Project-appropriate verification was run or the gap was documented.
