# UI library usage

## About / 简介

**EN:** Use the project's UI library or design system in a version-safe way: match the installed version, avoid deprecated APIs, and follow local styling and accessibility conventions.

**中文：** 按项目实际使用的 UI 库或设计系统进行开发：匹配已安装版本，避免废弃 API，并遵循项目内样式与可访问性约定。

### Mandatory: match the installed UI library version

All UI library usage must match the exact version installed in the project. This includes APIs, props, parameters, events, slots, component names, types, theme tokens, and styling hooks.

Do not use deprecated APIs in new or changed code when the installed version provides a supported replacement.

## How to use

1. Identify the UI library or design system used by the project.
2. Check the installed version from dependency files such as `package.json`, lockfiles, package manager metadata, framework manifests, or vendored package files.
3. Use APIs, props, parameters, events, slots, types, and styling hooks that match that exact version.
4. Do not copy API names, examples, or parameters from docs for a different major/minor version, generic tutorials, or model memory.
5. Follow nearby code for styling strategy, naming, theming, form validation, and accessibility behavior.

---

## 1. Version-safe API usage

Treat the installed dependency version as the source of truth. When unsure, prefer these sources in order:

1. Local type declarations or source files from the installed package.
2. Official documentation for the exact installed version.
3. Existing project code that is already compatible with the current dependency version.

If a prop, event, slot, token, or parameter is missing from the installed version, do not use it. If the installed version marks an API as deprecated, follow the replacement documented for that same version.

## 2. Semantic components and styling

Use semantic UI library components where they match the required behavior. Style them through the project's established mechanism, such as theme tokens, CSS Modules, scoped styles, utility classes, CSS-in-JS, component props, design-system wrappers, or framework-native styling.

Avoid ad-hoc DOM overrides unless the project already uses that pattern or the UI library has no supported styling hook. If custom overlay, portal, popup, dropdown, modal, or tooltip styles are changed, verify that the class or style hook attaches to the expected DOM for the installed version.

## 3. Deprecated APIs

Do not introduce deprecated APIs in new or changed code.

If touched code already uses deprecated UI library APIs, migrate only the affected area when the replacement is supported by the installed version. Do not rewrite unrelated legacy usage unless the user asks for it.

After edits, run the project verification that can reveal UI library warnings, such as dev server console checks, build, type check, lint, unit tests, or storybook checks. Fix new deprecation warnings caused by the change.

## 4. Forms and accessibility

Use the UI library's current form, validation, focus, keyboard, and accessibility APIs. Do not rely on placeholder-only labels for essential fields. Preserve keyboard navigation and screen-reader semantics when customizing components.

When the design requires custom controls, keep native semantics or explicitly add labels, roles, focus management, and error descriptions according to the project's accessibility standard.

## 5. Verification checklist

- [ ] The UI library or design system and installed version were identified.
- [ ] New or changed APIs, props, parameters, events, slots, and types match the installed version.
- [ ] No deprecated API was introduced.
- [ ] Existing deprecated usage was migrated only where it was touched and the installed version supports the replacement.
- [ ] Styling follows existing project conventions and uses supported hooks/tokens.
- [ ] Form and interactive components preserve accessibility expectations.
