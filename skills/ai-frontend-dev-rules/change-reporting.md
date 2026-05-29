# Change reporting

## About / 简介

**EN:** When code changes are guided by this skill, summarize which rules were applied, why they were used, and what the same rules could still improve.

**中文：** 当 AI 因识别到 `ai-frontend-dev-rules` 中的规范而调整项目代码时，需要在交付说明中用表格说明调整内容、命中的规范、使用原因和后续可优化点。

## How to use

After substantial or final project code changes based on files under `ai-frontend-dev-rules/rules`, include a reporting table in the final delivery note.

For trivial follow-up edits, pure Q&A, code review with no code change, or documentation-only review, do not force this table unless the user explicitly asks for it. For small code edits, group related changes into one concise row instead of producing a long report.

Use this exact table header:

| 调整功能 | 使用skills | 使用原因 | 可优化点 |
| --- | --- | --- | --- |
| Form option normalization | `rules/utils-data-mapping.md`: use the project option shape, usually `code`/`value` plus `label`; avoid unnecessary mapping methods | The feature only needs stable values for display and submission, so extra wrappers would add maintenance burden | If the product later needs i18n or dynamic copy, add a centralized copy layer without changing business values |
| Modal section split | `rules/ui-module-split.md`: move complex UI blocks into feature-local modules | The entry file would otherwise mix layout, state wiring, and form sections | Validation helpers can be moved into feature-local utilities if they become reused |

## Rules

- The `调整功能` column must name the feature, module, or behavior that changed.
- The `使用skills` column must name the exact rule file and the specific rule point used.
- The `使用原因` column must explain why the rule applies to the changed feature.
- The `可优化点` column should describe follow-up improvements supported by the skill but not included in the current change.
- If no specific rule was used for a changed item, write `No specific rule matched; followed existing project conventions`.
- Do not use this table to justify unrelated refactors.
- Keep the table concise; group related changes when they used the same rule for the same reason.
- Full change-reporting output is required for substantial frontend feature changes or final delivery. Minor follow-up fixes may use a compact version when the user does not need the full report.

## Checklist

- [ ] Final delivery note includes the required table for substantial frontend code changes or final delivery using this skill.
- [ ] Each row points to a concrete rule file and rule point.
- [ ] Reasons explain the fit for the actual code change.
- [ ] Follow-up optimization points are not mixed into the completed implementation.
