# Change reporting

## About / 简介

**EN:** Report concrete changes, why they help, and what was actually verified without speculative follow-up work.

**中文：** 简洁说明实际改动、原因与验证结果，不强制附带未来优化事项。

## Delivery

For substantial frontend changes guided by this skill, explain:

- What changed and why it improves the affected behavior or reading/maintenance cost.
- Which specific rules informed non-obvious structural choices; link relevant files when helpful.
- Which checks actually ran, their results, and material gaps or unresolved issues.

Use concise prose or, when several changes are easier to compare, a table such as:

| Change | Rule and reason | Validation |
| --- | --- | --- |
| Grouped order display helpers | Module layout: related helpers share consumers and change reasons | Focused formatting/selection cases and project typecheck |

The example is not a claim that these checks ran. Report only observed results. Do not require a fixed table, a rule citation for every line, or a future-optimization column. Include follow-up work only when it is a real unresolved need, and distinguish it from completed work.

Minor edits can use one short paragraph. Pure Q&A, review-only work, and documentation changes do not need an implementation table. Respect review-only scope and report findings without silently fixing code.
