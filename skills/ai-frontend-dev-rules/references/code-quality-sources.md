# Code quality sources

Use these references for rationale or a relevant framework detail, not as a requirement to read every book during implementation. The rules are an adaptation for this skill. Book principles can disagree; preserve correctness, context, and the project's actual contracts before applying a stylistic recommendation.

## Books and author references

| Source | Relevant contribution | Adaptation boundary |
| --- | --- | --- |
| [The Art of Readable Code — Dustin Boswell and Trevor Foucher](https://www.oreilly.com/library/view/the-art-of/9781449318482/) | Names, expressions, control flow, and reducing the effort needed to understand code | A shorter name or fewer lines is useful only if meaning stays clear |
| [Code Complete, 2nd ed. — Steve McConnell, table-driven methods](https://www.oreilly.com/library/view/code-complete-2nd/0735619670/ch18.html) | Represent suitable decisions as data/table lookups | Not every range, priority rule, or workflow belongs in an object map |
| [Refactoring, 2nd ed. — Martin Fowler](https://www.informit.com/store/refactoring-improving-the-design-of-existing-code-9780134757711) | Extract, inline, move, and reshape code while preserving behavior | Extraction and inlining are both valid; use [Inline Function](https://refactoring.com/catalog/inlineFunction.html) and [Move Function](https://refactoring.com/catalog/moveFunction.html) where the reading path improves |
| [A Philosophy of Software Design — John Ousterhout](https://web.stanford.edu/~ouster/cgi-bin/book.php) | Complexity, information hiding, interfaces, and modules that hide more complexity than they expose | Do not equate many small methods/classes/files with good design; comments and cohesive implementations can be useful |
| [Clean Code — Robert C. Martin, publisher excerpt](https://www.informit.com/content/images/9780132350884/samplepages/9780132350884.pdf) | Meaningful names, focused functions, understandable responsibilities | Do not turn “small functions” into mandatory line limits or a folder per function |
| [Maintainable JavaScript — Nicholas C. Zakas](https://www.oreilly.com/library/view/maintainable-javascript/9781449328092/) | Consistency, event/business responsibilities, errors, and configuration | Use current framework and language conventions rather than copying older implementation patterns |
| [JavaScript Design Patterns and Development Practice — Zeng Tan / 《JavaScript 设计模式与开发实践》— 曾探](https://www.dedao.cn/ebook/detail?id=bxEYR1zAbZMmVzK4p1oxl67XeNaB83OpR9Vw92GJERgryYQdDnqjkPLvO5eOZ8Nq) | Strategy/dispatch ideas when several behaviors share a stable interface | A simple function map can suffice; do not introduce a strategy class system for a small branch |

The approximate 300-line cohesion review, one-to-three-word local naming default, and review of names longer than four words are this skill's practical heuristics, not quoted book limits. The ban on unary `void` before calls is the user's coding convention, not a claim that JavaScript or these books prohibit the operator. The `utils` default is a repository convention, not a language rule; existing `util` projects remain supported.

## Official language and framework references

Read only the stack relevant to the task. Check installed-version compatibility before using an API shown in current documentation.

- React: [Choosing the State Structure](https://react.dev/learn/choosing-the-state-structure) and [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) support source/derived state and event/effect ownership.
- Vue: [Computed Properties](https://vuejs.org/guide/essentials/computed.html), [Watchers](https://vuejs.org/guide/essentials/watchers.html), and [Composables](https://vuejs.org/guide/reusability/composables.html) provide Vue-native derivation, side effects, and reuse. Both Options API and Composition API should follow the project's style.
- TypeScript: [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) covers discriminated unions and exhaustiveness; [useUnknownInCatchVariables](https://www.typescriptlang.org/tsconfig/useUnknownInCatchVariables.html) illustrates legitimate `unknown` beyond external-data parsers.
- Angular, Svelte, and other frameworks remain in scope. Consult their official documentation for the project's installed version when framework-specific guidance is needed; React examples are not universal lifecycle rules.

## How to apply a source

Translate a principle into a trigger, a preferred action, meaningful exceptions, and a semantic check. Use the [examples](code-quality-examples.md) to compare the decision with cases that should stay unchanged. Do not justify a change with a book title alone or invent a numeric limit attributed to a book.
