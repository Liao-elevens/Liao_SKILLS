# Functions and abstraction

## About / 简介

**EN:** Extract useful responsibilities while keeping simple work direct and avoiding layers that only forward calls.

**中文：** 封装有实际职责的逻辑，让简单操作保持直接，避免只转发调用的层层包装和过度抽象。

## Extract when it earns a name

Extract a function when it names a meaningful operation, isolates a coherent algorithm or effect boundary, removes repeated domain knowledge, or makes a mixed workflow readable. Keep a short event callback or simple expression inline when another name would add a navigation step without explaining intent.

- A function's name, inputs, and output should reflect what it does. A formatter, selector, or predicate should not secretly mutate state, send requests, or display notifications.
- Split a function that mixes unrelated purposes or abstraction levels; do not force a line-count maximum. A cohesive algorithm can be longer than a trivial event handler.
- Keep required side effects visible in the workflow. Do not disguise them as getters or hide execution order in a generic pipeline.
- Extracting a function does not imply exporting it, moving it to another file, or creating a folder. Follow [module layout](ui-module-split.md).

## Parameters and results

Use positional parameters for a few distinct, obvious inputs. Use a named options object when several similar values, optional settings, or booleans make calls ambiguous. Do not turn every single-argument function into an options API.

Review flag arguments such as `save(item, true, false)`: use named options or distinct operations if they express different responsibilities. A natural boolean value such as `setOpen(false)` is fine. Return a clear domain result; do not package a single value in a generic result envelope without a contract reason.

## Wrappers and generalization

| Situation | Decision |
| --- | --- |
| A private wrapper only forwards identical arguments and result | Inline when the name adds no domain meaning and no boundary is served |
| A thin function provides API ownership, authorization, telemetry, platform adaptation, or a stable public contract | Keep the boundary; line count alone does not make it useless |
| Two pieces of code look similar but obey different domain rules | Keep separate until their shared meaning and change reasons are established |
| Repeated domain knowledge has one owner | Extract the smallest interface that removes that duplication |
| Only one current implementation exists | Use direct code unless a real extension point is already required |

Do not introduce generic factories, strategies, plugins, base classes, or configurable pipelines for hypothetical future variants. Ordinary objects and functions are often sufficient. Conversely, preserve an existing framework/SDK interface when required even if its implementation is small.

Assess an abstraction by how much complexity it hides relative to the interface and navigation it adds. See [wrapper and sharing cases](../references/code-quality-examples.md#useful-boundaries-and-accidental-similarity).
