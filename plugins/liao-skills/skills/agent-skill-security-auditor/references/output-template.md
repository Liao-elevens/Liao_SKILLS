# Output Template

Use this format for final audit reports.

```md
## Verdict
Install / Install with caution / Do not install

Policy: personal / team / enterprise / marketplace
Scope reviewed: files, folders, diff, repository, or package source

## Findings
- [P0/P1/P2/P3] Short title
  Evidence: path:line
  Risk: what could happen
  Fix: concrete mitigation

## Sensitive Capabilities
- Network access:
- File writes:
- Secret access:
- External services:
- Subprocess execution:
- Destructive actions:

## Recommended Changes
1. ...
2. ...

## Residual Risk
State what was not verified, such as runtime behavior, remote history, dependency reputation, or external service behavior.
```

When no findings are present, keep the same structure and write:

```md
## Findings
No blocking or high-risk findings were identified in the reviewed files.
```

