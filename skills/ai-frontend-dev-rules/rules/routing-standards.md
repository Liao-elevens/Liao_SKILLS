# Routing standards

## About / 简介

**EN:** Preserve native routing boundaries, navigation behavior, and intentional URL state.

**中文：** 遵循项目路由机制，保留导航语义、路由边界与有明确用途的 URL 状态。

## Structure and navigation

Register routes/screens through the project's central config, feature route file, file-based routing, or platform manifest. Preserve layout nesting, lazy loading, loading/error boundaries, and not-found handling. Do not impose a central route registry on a framework whose routes are intentionally file-owned.

Use readable stable paths and the project navigation/link API for internal navigation. Preserve link semantics such as keyboard access and opening a new tab. Raw location changes are appropriate for intentional full-page or external navigation, not a substitute for the existing router.

If several conditions choose a destination, compute the target clearly, then navigate once where this preserves behavior. Keep guard/redirect ownership at the appropriate shared route or layout boundary.

## URL state

Use path parameters for resource identity where the router expects them. Put filters, pagination, tabs, or sorting in query/search state when sharing, bookmarking, restoration, or browser-history behavior is required. Transient popovers and temporary input do not automatically belong in the URL.

Choose a clear source of truth. Avoid independent URL and local state with watchers/effects continuously copying in both directions. An editable local draft before applying search is a valid separate lifecycle. Parse untrusted URL values at the route boundary using [type rules](type-standards.md); preserve defaults and back/forward navigation behavior.

## Permissions and verification

Centralize common guard logic without deleting resource-specific authorization or distinct permissions. Preserve the distinction between unauthenticated, unauthorized, and not found. Client-side hiding or routing is not a substitute for required server authorization.

Check direct navigation, required parameters, back/forward behavior, lazy loading, failures, and redirects affected by the change. Do not alter unrelated route definitions merely for consistency.
