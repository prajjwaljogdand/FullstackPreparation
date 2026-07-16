# Hoisting

Hoisting is the observable result of **binding instantiation before statement execution** — not a literal rearranging of source lines.

## Mental model

During context creation, the engine:

1. Creates bindings for declarations in that scope.
2. Initializes some of them early (`var` → `undefined`, function declarations → function object).
3. Leaves others uninitialized until the declaration is evaluated (**TDZ** for `let`/`const`/`class`).

```mermaid
sequenceDiagram
  participant Create as Creation phase
  participant Exec as Execution phase
  Create->>Create: bind params
  Create->>Create: hoist function decls
  Create->>Create: var = undefined
  Create->>Create: let/const in TDZ
  Exec->>Exec: run statements top to bottom
  Exec->>Exec: init let/const at decl lines
```

## `var` hoisting

```ts
function f() {
  console.log(x) // undefined — binding exists
  var x = 10
  console.log(x) // 10
}
```

Equivalent mental rewrite (not literal):

```ts
function f() {
  var x
  console.log(x)
  x = 10
  console.log(x)
}
```

Multiple `var` with the same name merge into one binding:

```ts
function g() {
  var x = 1
  var x = 2
  return x // 2
}
```

## Function declaration hoisting

```ts
hoisted() // works

function hoisted() {
  return "ok"
}
```

Initialized to the function object during creation — callable before the line in the same scope.

### Duplicate function declarations

Last wins (non-module / sloppy patterns):

```ts
function a() {
  return 1
}
function a() {
  return 2
}
a() // 2
```

Prefer one declaration; use `const` + function expression for clarity.

## Function expressions — not hoisted as functions

```ts
// expr() // TypeError: expr is not a function (if var) or TDZ (if let)
var expr = function () {
  return 1
}

// arrow() // TDZ
const arrow = () => 1
```

| Form | Binding hoist | Early init as callable |
| --- | --- | --- |
| `function f() {}` | yes | yes |
| `var f = function() {}` | yes (`undefined`) | no |
| `let f = () => {}` | yes (TDZ) | no |
| `const f = function*() {}` | TDZ | no |
| `async function f() {}` | like function decl | yes |
| class `C {}` | TDZ | no |

## `let` / `const` and the Temporal Dead Zone

```ts
{
  // TDZ starts at block entry
  // console.log(x) // ReferenceError
  let x = 1 // initialized here — TDZ ends
  console.log(x)
}
```

TDZ exists so shadowing is safe and `"use before declare"` is a hard error:

```ts
const x = 1
{
  // console.log(x) // ReferenceError — inner x in TDZ, not outer
  const x = 2
}
```

## `class` hoisting

Classes are hoisted into TDZ like `let`:

```ts
// new Person() // ReferenceError
class Person {
  constructor(public name: string) {}
}
```

Inheritance requires the parent to be initialized first — another reason for TDZ.

## Parameter scope & default values

Defaults see earlier params; TDZ applies between params:

```ts
function f(a = 1, b = a + 1) {
  return b
}
f() // 2

function g(a = b, b = 1) {
  // calling g() → ReferenceError (b in TDZ when evaluating a)
  return a
}
```

Params have their own environment nuances with defaults — treat default expressions as a mini scope.

## Preferential order (same name collisions)

Rough interview rule inside a function scope:

1. Parameters create bindings.
2. Function declarations can overwrite / share names depending on engine era — **avoid colliding names**.
3. `var` merges; `let`/`const` conflict with existing names → `SyntaxError`.

```ts
function bad(x: number) {
  // let x = 2 // SyntaxError in modern engines
  var x = 3 // merges with param (legacy footgun)
  return x
}
```

## Import hoisting (modules)

```ts
// usage before import line still works — imports are hoisted / linked first
console.log(add(1, 2))

import { add } from "./math"
```

Imports are live bindings resolved during module linking — before evaluation order of statements.

## Interview output drills

```ts
console.log(a)
var a = 1
// undefined

console.log(b)
let b = 1
// ReferenceError

foo()
function foo() {
  console.log(x)
  var x = 2
}
// undefined

bar()
var bar = function () {}
// TypeError
```

```ts
function demo() {
  return typeof x
  function x() {}
}
demo() // "function" — function decl wins over later var patterns in many cases

function demo2() {
  var x = 1
  function x() {}
  return typeof x
}
// often "number" after assignment — order of init matters; avoid dual declarations
```

## Why hoisting exists (historical)

- Allows mutual recursion of function declarations without forward-reference pain.
- `var` was function-scoped and initialized early for simplicity of early JS.
- Modern `let`/`const` keep declaration binding early for scope rules but defer init → TDZ.

## Interview Questions

**Q: Are variables moved to the top?**  
No. Bindings are created during instantiation; initialization timing differs by declaration kind.

**Q: What is TDZ?**  
Period from scope entry until `let`/`const`/`class` initialization where access throws `ReferenceError`.

**Q: Why can you call a function declaration before its line?**  
It is initialized during creation phase of the enclosing context.

**Q: Difference between `var` hoist and `let` hoist?**  
Both create bindings early; `var` initializes to `undefined`, `let` stays uninitialized (TDZ).

**Q: Do arrow functions hoist?**  
The binding may be in TDZ (`const`/`let`) or `undefined` (`var`); the function object is not available until assignment runs.

## Common Mistakes

- Relying on `var` hoisting for control flow.
- Using a `let` before declaration across nested blocks while expecting outer value.
- Mixing function declarations and `var` of the same name.
- Assuming class constructors can be used above their declaration.
- Teaching "hoisting = move code up" in interviews — correct to the binding model.

## Trade-offs / Production Notes

- Style: declare before use; enable `no-use-before-define` (with function decl exceptions if desired).
- Prefer `const`/`let` + function expressions for predictable dependency order in files.
- Mutual recursion: function declarations or hoist-safe patterns; or assign after both consts with deferred calls.
- Related: [Scope](/javascript/03-scope), [Execution Context](/javascript/02-execution-context), [Classes](/javascript/08-classes).
