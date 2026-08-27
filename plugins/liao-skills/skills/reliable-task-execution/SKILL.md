---
name: reliable-task-execution
description: Improve reliability when planning or executing tasks that may produce code, file, configuration, data, or external-system changes, and for complex, ambiguous, multi-step, or high-impact work. Use when Codex needs to confirm execution authorization, refine ambiguous requirements, brainstorm alternatives, critically interview the user about consequential decisions, match planning and validation depth to risk, assess code-change impact, coordinate independent workstreams, red-team a proposal, or test a real user journey. Apply the smallest sufficient workflow; do not use for simple read-only questions.
---

# Reliable Task Execution

Choose the smallest workflow that makes the result dependable. Do not turn a simple request into a ceremony.

Match the user's language unless they request otherwise.

When the user asks how to use this skill, read [the complete usage guide](references/usage/使用说明.md).

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

## Refine requirements and design

Inspect available project context before questioning the user. Resolve discoverable facts through safe read-only inspection, then choose the lightest sufficient mode. Do not require the user to know mode names or present a mode menu by default.

| Mode | Use when | Interaction |
| --- | --- | --- |
| Targeted clarification | One to three material gaps block an otherwise clear task | Ask only the blocking questions, include a recommendation when useful, then continue |
| Guided Design | The goal is rough or several approaches are credible, but a formal design package is unnecessary | Explore material decisions, compare alternatives, and shape an implementation-ready design |
| Full Brainstorm | Multiple subsystems or design domains interact, or the work needs formal review, handoff, or visual design artifacts | Run a complete design cycle with staged approval and conditional artifacts |
| Strict Grill | An existing consequential proposal has unresolved critical branches or weak assumptions | Build a decision tree and close one critical node per turn before finalizing the design |

Skip refinement when the request, project conventions, and acceptance criteria already make the implementation path clear.

### Escalate progressively

- Start with targeted clarification or Guided Design unless the user explicitly requests a deeper mode.
- Recommend only one next mode at a time. State why it fits, what additional outputs or interaction it adds, and whether any file or external write would still need authorization.
- Wait for the user's answer before entering Full Brainstorm or Strict Grill. Do not silently impose a long workflow.
- If the user declines, continue with the lighter mode, record the accepted limitation or risk, and do not repeat the recommendation unless the scope materially changes.
- Honor explicit user overrides such as "keep it quick," "full brainstorm," or "strictly grill this" without asking them to choose again.
- Do not automatically chain Full Brainstorm into Strict Grill. Recommend Strict Grill afterward only if major decision branches remain unresolved.

#### Decide whether to recommend Full Brainstorm

Recommend Full Brainstorm when at least one strong signal or at least two supporting signals are present.

Strong signals:

- The work spans three or more interacting subsystems with distinct responsibilities, data, or interface boundaries. Do not count ordinary components within one page as separate subsystems.
- The user is designing a broad product, platform, or business domain from scratch and its boundaries are not established.
- Architecture, data modeling, and user flow must be designed together.
- The outcome requires a formal design specification for team review or cross-role handoff.
- The work explicitly needs several design artifacts such as architecture, entity-relationship, state, and interaction diagrams.
- The scope must first be decomposed into multiple independently deliverable projects or phases.

Supporting signals:

- At least three design domains among product, interaction, architecture, data, interfaces, security, operations, testing, and rollout contain material unknowns.
- Two or more credible approaches would produce materially different architecture, data, or user experience.
- Permissions, state transitions, failure recovery, or data consistency cross module boundaries.
- Acceptance criteria cannot be made concrete without resolving several material decisions.
- The work requires migration, staged rollout, backward compatibility, or coexistence with a legacy path.
- Multiple user or consumer groups have materially different goals.
- One local decision affects three or more downstream modules or consumers.

#### Decide whether to recommend Strict Grill

Recommend Strict Grill only when all three conditions are true: a concrete proposal exists, at least one high-impact signal is present, and at least one critical decision branch is unresolved.

A concrete proposal names an intended approach, not merely a goal. Examples include splitting a monolith, adopting a shared database, changing an authentication model, or migrating frameworks.

High-impact signals:

- The decision is costly or difficult to reverse.
- It changes a public API, shared schema, protocol, common component, or security boundary.
- It involves production data migration, deletion, or format conversion.
- It affects authentication, authorization, privacy, payments, or other sensitive behavior.
- It affects multiple systems, teams, or existing consumers.
- Failure could cause material downtime, incorrect data, or serious user harm.
- It creates significant vendor lock-in or long-term infrastructure cost.
- It requires broad migration, dual-write, staged rollout, or legacy compatibility.
- It relies on unverified performance, capacity, availability, or reliability assumptions.

A critical branch is unresolved when a different answer could materially change scope, architecture, data consistency, public interfaces, security, failure behavior, migration, cost, sequencing, or acceptance criteria, and the branch has no explicit disposition.

Treat a critical branch as explicitly disposed only when it is confirmed, accepted as an assumption with its risk, explicitly deferred with its impact, evidence-blocked with a named validation path, or declared out of scope. Do not treat vague statements such as "later" or "probably fine" as closure.

### Clarify targeted gaps

- Ask no more than one to three related questions at once.
- Ask only questions whose answers could materially change scope, architecture, behavior, risk, or acceptance criteria.
- Give a recommended default and its main consequence when that helps the user decide.
- Continue immediately after the blocking gaps are resolved; do not reconfirm settled choices.

### Guide a design

1. Establish the objective, affected users or consumers, current context, and constraints.
2. Explore one material decision area at a time. Prefer a focused question over a large questionnaire.
3. Present two or three materially different approaches when credible alternatives exist. Lead with the recommendation and explain the decisive tradeoff.
4. Develop the design in readable sections and seek confirmation only at points that would change downstream work.
5. Cover relevant boundaries, data or interaction flow, failure behavior, acceptance criteria, and exclusions.
6. Summarize the resulting design and remaining assumptions. Treat design approval as alignment, not implementation authorization.

### Run a Full Brainstorm

1. Inspect the current project, related documentation, and established patterns before detailed questioning.
2. Assess scope first. If independent subsystems make one design too broad, propose a decomposition and brainstorm one coherent unit at a time.
3. Ask one question per turn to establish purpose, users, constraints, success criteria, and cross-domain decisions.
4. Present two or three approaches with tradeoffs and a recommendation. Remove unnecessary scope.
5. Present the design in sections sized to their complexity and obtain confirmation after each section.
6. Cover relevant architecture, component boundaries, user and data flow, state and data model, interfaces, failure handling, security, performance, operations, testing, acceptance criteria, migration, and rollback.
7. Produce only decision-relevant artifacts. Use Mermaid for flows, architecture, state, or entity relationships when it materially improves understanding.
8. When a visual question would genuinely benefit from mockups or side-by-side visual comparison and a visual capability is available, offer it just in time and wait for consent. If unavailable, use Mermaid or a static description and state the limitation.
9. Self-review the completed design for placeholders, contradictions, ambiguous requirements, missing failure cases, and excessive scope; fix issues before presenting the final draft.
10. Ask for separate authorization before writing a design document, committing it, or moving into implementation planning. A brainstorming request is read-only by default.

### Run a Strict Grill

1. Restate the proposal and build a structured decision tree covering relevant goals, users, scope, constraints, architecture, data and state, interfaces, failure behavior, security, performance, migration, operations, testing, and acceptance criteria.
2. Mark each node as unresolved, confirmed, accepted assumption, explicitly deferred, or evidence-blocked.
3. Ask exactly one question per turn, targeting the highest-impact unresolved node.
4. Explain the concrete consequence and tradeoff without silently deciding for the user.
5. Follow new critical branches exposed by the answer before moving to unrelated nodes.
6. Every three to five questions, show decision-tree progress. Treat this as a checkpoint, not an exit condition.
7. Do not finalize the design while critical nodes remain unresolved unless the user explicitly accepts, defers, or stops the session.
8. Finish with the closed decision tree, decision snapshot, final design, accepted assumptions, deferred items, and acceptance criteria.

Finish refinement when the objective, scope, constraints, recommended approach, major tradeoffs, acceptance criteria, and material assumptions are sufficiently clear for the selected mode. Do not seek certainty that is unnecessary for the task's risk.

## Select a workflow

### Red-team a plan

Use after a plan or design exists when it involves consequential architecture choices, expensive commitments, or a broad failure surface. Guided Design and Full Brainstorm form a design, Strict Grill closes its decision branches, and red-teaming evaluates the resulting proposal; combine them only when each adds distinct value.

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

After requirement refinement, include a compact decision snapshot when it helps preserve alignment:

- confirmed decisions;
- accepted assumptions and unverified facts;
- recommended approach and decisive tradeoffs;
- material risks or unresolved issues;
- next step and whether implementation authorization is still required.

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
