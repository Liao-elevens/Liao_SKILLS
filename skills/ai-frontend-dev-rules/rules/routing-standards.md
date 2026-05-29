# Routing standards

## About / 简介

**EN:** Route, screen, and navigation organization rules so frontend expansion stays predictable across frameworks.

**中文：** 约定路由、屏幕和导航组织方式，让任意前端技术栈下的页面扩展都保持稳定、可维护。

## How to use

Add routes, screens, tabs, menus, or navigation entries through the project's established routing/navigation mechanism. Keep route definitions, lazy loading, permissions, layouts, and fallbacks consistent with nearby code.

---

## 1. Route structure

- Prefer one clear source of truth for route, screen, or navigation configuration when the project supports it.
- Keep layout routes, nested screens, tabs, and parent-child relationships explicit.
- Preserve fallback routes, 404 pages, empty states, or platform-equivalent "not found" behavior.
- Avoid scattering route definitions across feature files unless the framework or project convention intentionally supports feature-owned routing.

## 2. Lazy loading pattern

- Use page/screen/route-level lazy loading when the project already uses it or when the framework makes it standard.
- Keep loading fallbacks consistent with existing UX.
- Preserve existing error boundaries, error pages, guard wrappers, or framework-equivalent failure handling.
- Do not introduce a new lazy-loading pattern for one route when the project already has one.

## 3. Path and naming

| Rule | Detail |
|------|--------|
| Path style | Use readable, stable route paths or screen identifiers that match feature intent and project naming. |
| Route file | Place route registration where the project expects it: central config, module route file, file-based route folder, or framework manifest. |
| Nested routes | Model child routes/screens under their parent instead of duplicating parent state in separate definitions. |
| Params/query | Use params for identity and query/search state for filters, tabs, sorting, pagination, or view options. |

## 4. Navigation rules

- Use the framework or project navigation API for internal navigation. Avoid raw location changes unless the project convention requires them.
- Cross-page entry buttons should navigate to explicit route targets with required params/query/search state.
- If navigation depends on business state, compute the target first and navigate once.
- Keep permission checks, route guards, and redirect behavior centralized where possible.

## 5. Guard and permission

- Use route-level guards, layout checks, middleware, loaders, navigation guards, or platform equivalents when auth/permission affects multiple screens.
- Do not duplicate permission checks in every leaf page if a parent route or shared guard can centralize them.
- Keep unauthorized, unauthenticated, not-found, and no-access states visually and semantically distinct.

## 6. Checklist

- [ ] New route/screen/navigation entry is registered in the project's expected place.
- [ ] Lazy loading, fallback, and error handling match existing patterns.
- [ ] 404/not-found behavior is preserved.
- [ ] Internal navigation uses project/framework APIs.
- [ ] Params/query/search semantics are clear.
- [ ] Guards and permissions are centralized where appropriate.
