# UI library usage

## About / 简介

**EN:** Match the installed UI library and keep components, templates, styles, and accessibility readable.

**中文：** 匹配已安装 UI 库版本，保持组件接口、模板、样式与可访问性实现清晰。

## Version-correct APIs

Identify the actual library/design system and installed version from package metadata, lockfiles, local types, or vendored source. Check props, events, slots, tokens, parameters, and styling hooks against that version.

When unsure, prefer installed types/source, then official documentation for that version; nearby working code provides project conventions. Do not copy a newer version's API into an older installation. Do not add deprecated usage when a supported replacement exists in the installed version. Migrate touched deprecated usage only where the local change is compatible; do not expand into an unrelated upgrade.

## Component and template simplicity

- Keep interfaces centered on meaningful data and actions. Avoid exposing many internal setters or mode booleans that let callers produce impossible combinations.
- Use composition/slots/children when variants diverge substantially. Do not build a universal component whose behavior is mostly conditionals for unrelated screens.
- Keep simple expressions and short event handlers in templates/rendering. Move substantial filtering, grouping, or workflow logic to named values/functions near the owner.
- Data-drive repeated UI with the same structure. Keep genuinely different layouts explicit instead of creating a giant configuration renderer.
- Use stable domain keys for changing/reordered lists; do not generate new keys on every render or use indices when identity can move.
- Extract a UI component for a real responsibility or useful reuse, not merely to shorten a CSS class string. Use [layout rules](ui-module-split.md) for files and folders.

## Styling and accessibility

Use the project's theme tokens, scoped styles, CSS Modules, utility classes, CSS-in-JS, or existing mechanism. Prefer supported styling hooks over fragile internal DOM overrides. Verify portal/overlay styling attaches to the intended element in the installed version.

Keep native semantics and the library's keyboard, focus, labeling, validation, and error-description behavior. Do not replace buttons/links with clickable generic containers merely to reduce markup. Placeholder text does not replace an essential label. Preserve focus management for dialogs and other composite controls.

## Verify

Run applicable type/lint/build checks and inspect changed interactions where needed. Confirm supported APIs, overlay styles, form errors, keyboard behavior, stable identity, and no new deprecation warnings. Static checking alone does not establish visual or accessibility behavior.
