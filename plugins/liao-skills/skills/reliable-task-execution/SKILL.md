---
name: reliable-task-execution
description: Improve reliability when planning or executing tasks that may produce code, file, configuration, data, or external-system changes, and for complex, ambiguous, multi-step, or high-impact work. Use when Codex needs to confirm execution authorization, match planning and validation depth to risk, assess code-change impact, coordinate independent workstreams, red-team a proposal, or test a real user journey. Apply a lightweight workflow to simple authorized changes and deeper workflows only when risk or uncertainty requires them. Do not use for simple read-only questions.
---

# Reliable Task Execution

Choose the smallest workflow that makes the result dependable. Do not turn a simple request into a ceremony.

Match the user's language unless they request otherwise.

## Apply the execution gate

Distinguish discussion from authorization:

- Treat requests to analyze, diagnose, review, explain, research, or propose a plan as read-only.
- When the user describes a goal or idea without clearly asking to implement it, inspect only what is needed, align the plan, and ask whether to begin.
- Before asking, resolve discoverable facts through safe read-only inspection. Confirm only choices that materially affect scope or outcome.
- Treat phrases such as "开始做", "实现", "开发", "修改", "修复", or an equally clear instruction as execution authorization.
- Do not ask again when authorization is already explicit.
- Ask again before expanding scope or taking a newly introduced high-risk, destructive, sensitive, privileged, external-write, deployment, publication, or Git-history action.
- While waiting for authorization, do not modify code, files, configuration, data, or external systems.

Before implementation, align these items when relevant:

- objective and acceptance criteria;
- included and excluded scope;
- constraints and important tradeoffs;
- unresolved decisions that would materially change the result.

End a plan awaiting approval with a direct question asking whether to execute it.

### Control Git scope

Before Git writes, confirm any material scope the user has not made explicit:

- files included in the commit;
- whether creating a commit is authorized;
- target remote and target branch;
- whether creating or switching branches is authorized;
- whether pushing is authorized;
- whether opening a pull request is authorized.

Authorization to commit or push does not authorize choosing a different target branch, creating or deleting a branch, opening a pull request, merging, rebasing, or rewriting history. Do not infer a branch strategy from tooling defaults. If the user asks to push without naming a target branch, inspect the current branch and ask before creating, switching, or selecting one.

## Classify the task

Use one primary class and combine workflows only when necessary:

| Class | Signal | Response |
| --- | --- | --- |
| Quick | Clear, local, stable, and low risk | Answer or execute directly when authorized |
| Moderate | Several steps or limited uncertainty | State a short plan, then proceed when authorized |
| Deep | Cross-module, costly, high-impact, or decision-heavy | Align scope, risks, and acceptance criteria first |
| Experimental | The result cannot be established by reasoning alone | Define the smallest useful experiment and success criteria |

Identify missing information, ambiguity, and the most fragile assumption. Ask the user only when the answer cannot be discovered safely and a reasonable assumption could materially change the result. Report decision-relevant reasoning, evidence, assumptions, and intermediate conclusions; do not expose private chain-of-thought.

## Select a workflow

### Red-team a plan

Use for consequential plans, architecture choices, or expensive commitments:

1. Restate the objective and constraints concisely.
2. Assume the plan failed and identify the three most plausible causes.
3. Find unverified assumptions, omitted failure cases, optimistic shortcuts, and simpler paths.
4. For material risks, give the trigger, cost, early warning, and smallest falsification experiment.
5. Recommend one outcome: execute, test first, revise, or restart.

Skip a full red-team pass when the decision is cheap and easily reversible.

### Analyze code-change impact

Use before broad, shared, or uncertain code changes. Inspect the relevant structure, call paths, interfaces, data shapes, downstream consumers, tests, and related uncommitted changes.

| Risk | Signal | Default handling |
| --- | --- | --- |
| L1 | Local effect, stable interface, strong coverage | Implement after authorization and run focused checks |
| L2 | Cross-module effect or broad regression surface | Use separable, independently verifiable change units |
| L3 | Public interface, shared schema, common dependency, or production data | Present the plan and obtain specific approval first |

Name the most likely failure points and how to verify them. Apply the Git scope rules before any commit or related Git write.

### Coordinate independent workstreams

Use parallel agents only when at least two substantial workstreams are genuinely independent and parallelism is available. Do not parallelize tightly coupled work or tasks whose coordination cost exceeds the benefit.

For each workstream define its objective, boundary, deliverable, validation, dependencies, and completion criteria. Track progress, reconcile conflicts, integrate results, and perform final validation. Never present one completed workstream as completion of the whole task.

### Test a real user journey

Use when the user requests experience testing, end-to-end validation, or acceptance testing:

- Start from the real entry point and operate the product through browser or computer controls.
- Do not substitute code inspection for actual interaction.
- Check loading feedback, errors, discoverability, wording, state clarity, persistence, and success or failure feedback.
- Capture screenshots at key states and failures, not mechanically after every click.
- Report issues by severity with reproduction steps, evidence, impact, and a suggested direction.
- Treat a testing request as permission to test, not permission to fix.
- After an authorized fix, repeat the affected journey and check for regression.

## Present plans clearly

Lead with the recommendation. Keep plans concise, concrete, and executable.

| Information | Preferred form |
| --- | --- |
| Options, fields, or tradeoffs | Markdown table |
| Three or more sequential steps, states, or branches | Mermaid flowchart |
| Module, responsibility, or task hierarchy | Outline or Mermaid mindmap |
| Simple conclusion or a few steps | Short prose or numbered list |

Use a visual only when it materially improves understanding. Keep labels short, remove decision-irrelevant detail, and repeat critical conclusions in text so they do not exist only in a diagram.

For a substantial plan include:

- objective and scope;
- explicit exclusions;
- key decisions and execution flow;
- acceptance criteria;
- risks and unresolved issues;
- whether execution authorization is still required.

## Verify and finish

- After making code or project changes, inspect the final diff and confirm it contains only intended changes.
- Run checks proportional to the change and available project tooling: formatting, lint or static analysis, type checking, focused tests, broader tests when the regression surface requires them, build checks, and real user-path validation when behavior or UI changed.
- Start with the smallest relevant checks, then expand according to risk and observed failures.
- Inspect the change scope for unintended files, generated artifacts, credentials, and unrelated edits.
- Distinguish confirmed facts, inferences, unverified assumptions, and observed results.
- Never claim a check that was not run. Report unavailable or skipped checks, why they were not run, and the resulting risk.
- Do not confuse partial progress with completion.
- Continue through safe, authorized work until the acceptance criteria are met or a genuine blocker requires the user.
- Finish with the outcome, validation performed, anything unverified, the change scope, and risks or unresolved issues.
- If no risks or unresolved issues remain, say so explicitly.
