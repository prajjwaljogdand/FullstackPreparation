# Generics

Generics parameterize types and functions over **type variables**, preserving relationships between inputs and outputs. They’re how libraries express reusable, type-safe APIs without `any`.

Related: [Conditional Types](/typescript/03-conditional-types) · [Infer](/typescript/04-infer) · [Variance](/typescript/09-variance) · [React hooks typing](/react/03-hooks)

## Why generics

```ts
function identity<T>(x: T): T {
  return x
}
const a = identity(1)        // number
const b = identity<string>('x') // explicit
```

Without `T`, you’d return `any` or overload endlessly. Generic **constraints** limit `T`:

```ts
function prop<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]
}
prop({ a: 1, b: 'x' }, 'a') // number
```

```mermaid
flowchart LR
  Call[Call site] --> Infer[Infer type args]
  Infer --> Check[Check constraints]
  Check --> Subst[Substitute into signature]
  Subst --> Result[Result type]
```

## Inference rules (practical)

TypeScript infers type arguments from arguments (and sometimes expected return type / contextual typing).

```ts
function map<T, U>(arr: T[], f: (x: T) => U): U[] {
  return arr.map(f)
}
map([1, 2], (n) => `${n}`) // T=number, U=string
```

**Failures:** inference can’t invent types from nowhere; circular constraints; multiple candidates → often `{}` or error. Fix with explicit args or `satisfies`.

```ts
function createPair<T>(a: T, b: T): [T, T] {
  return [a, b]
}
createPair(1, 'x') // error — T can't be both
createPair<number | string>(1, 'x') // OK
```

## Constraints & `keyof`

```ts
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b
}
longest([1], [1, 2]) // number[]
longest('a', 'bb')   // string
```

`K extends keyof T` is the standard “safe property access” pattern. Nested: `K extends keyof T`, `T[K] extends ...`.

## Defaults & multiple params

```ts
type ApiResponse<TData, TError = Error> = {
  data?: TData
  error?: TError
}

type Box<T = string> = { value: T }
```

Order: required type params before optional/defaulted; inference fills left-to-right typically.

## Generic classes & interfaces

```ts
interface Repository<T, TId extends string | number = string> {
  get(id: TId): Promise<T | null>
  save(entity: T): Promise<T>
}

class MemoryRepo<T extends { id: string }> implements Repository<T> {
  private map = new Map<string, T>()
  async get(id: string) {
    return this.map.get(id) ?? null
  }
  async save(entity: T) {
    this.map.set(entity.id, entity)
    return entity
  }
}
```

## Higher-order generics (factory patterns)

```ts
function withId<TBase extends object>(base: TBase) {
  return { ...base, id: crypto.randomUUID() as string }
}
// Return type inferred as TBase & { id: string }
```

For components (React):

```ts
type Props<T> = { items: T[]; render: (item: T) => React.ReactNode }
function List<T>({ items, render }: Props<T>) {
  return <>{items.map(render)}</>
}
// <List items={users} render={(u) => u.name} />
```

See [React](/react/03-hooks) for `useState` generic inference quirks.

## Generic vs overload vs union

```ts
// Prefer generic when input/output related
function first<T>(arr: T[]): T | undefined {
  return arr[0]
}

// Overloads when behavior branches by input type distinctly
function parse(x: string): object
function parse(x: ArrayBuffer): object
function parse(x: string | ArrayBuffer): object {
  return {}
}
```

Don’t write `function f(x: A | B): A | B` when `f<T extends A | B>(x: T): T` preserves the member.

## Variance preview

`Producer<T>` (getter) is covariant in `T`; `Consumer<T>` (setter) is contravariant; mutable `Array<T>` is invariant in practice for soundness. Deep dive: [Variance](/typescript/09-variance).

```ts
type ReadonlyArrayish<out T> = { readonly [n: number]: T } // TS 4.7+ variance ann.
type Writer<in T> = { write: (value: T) => void }
```

## Interview Questions

**Q1. When do you need an explicit type argument?**  
When inference has no argument to draw from (`empty` collections, `useRef` initial null, ambiguous overloads).

**Q2. `T extends any` trick?**  
Distributes over unions in conditional types — see [Conditional Types](/typescript/03-conditional-types). Not needed for ordinary generics.

**Q3. Why `K extends keyof T` instead of `key: string`?**  
`string` allows invalid keys and returns inflated value types; `keyof` ties key→value.

**Q4. Generics at runtime?**  
Erased — no `T` in JS. Can’t `new T()` without passing a constructor value: `c: new () => T`.

**Q5. Generic defaults vs optional props?**  
Defaults kick in when type arg omitted; optional props are value-level. Don’t confuse `T = void` patterns in event emitters.

## Common Mistakes

- Constraining to `any` (`T extends any`) accidentally for non-conditional code.
- Returning `T | null` but implementing with `as T` unsafely.
- Over-generic APIs (`T` unused) — noise.
- Using generics where a simple union suffices.
- `React.FC` + generics pain — prefer function declarations.

## Trade-offs

| Approach | Pros | Cons |
| --- | --- | --- |
| Generics | Precise relationships | Harder errors / learning curve |
| Overloads | Documented branches | Combinatorial explosion |
| `any` | Fast | Zero safety |
| Concrete unions | Simple | Doesn’t scale to libraries |

**Senior takeaway:** Generics exist to **carry information from call site to return type** — if `T` doesn’t appear twice (or in a constraint relationship), you probably don’t need it.

## Deep dive — inference priority

TS prefers candidates that succeed constraints. Ambiguous cases may pick the first viable or error. Conditional types can block inference (`NoInfer<T>` in TS 5.4+):

```ts
function pair<T>(a: T, b: NoInfer<T>): [T, T] {
  return [a, b]
}
pair('a', 'b') // T from first arg only
```

## Deep dive — generic instantiation & errors

Cryptic errors often come from nested instantiations (`Promise<AxiosResponse<...>>`). Simplify by naming intermediate types; avoid ultra-deep recursion in public APIs ([Conditionals](/typescript/03-conditional-types)).

```ts
type Ok<T> = { ok: true; data: T }
type Err = { ok: false; error: string }
type Result<T> = Ok<T> | Err

function mapResult<T, U>(r: Result<T>, f: (t: T) => U): Result<U> {
  return r.ok ? { ok: true, data: f(r.data) } : r
}
```

## Deep dive — constructor generics

```ts
function factory<T>(Ctor: new (n: number) => T, n: number): T {
  return new Ctor(n)
}
class Box {
  constructor(public n: number) {}
}
factory(Box, 1)
```

## Extra Q&A

**Q6. `extends unknown` vs unconstrained?**  
Similar; sometimes used to force distribution.

**Q7. Why error “T could be instantiated with arbitrary type”?**  
Returning value that isn’t proven to be `T` (e.g. always `null as T`).

**Q8. Generic JSX components?**  
`const Cmp = <T,>(props: Props<T>) => ...` — trailing comma needed in TSX.

**Q9. Higher-kinded types?**  
TS lacks true HKTs; encode with interfaces + infer tricks carefully.

**Q10. Variance of `Promise<T>`?**  
Covariant in `T` (producer). → [Variance](/typescript/09-variance)


## Worked example — typed event emitter

```ts
type Ev = { ping: void; msg: string }
class Emitter<E extends Record<string, unknown>> {
  // simplified
  on<K extends keyof E>(e: K, cb: (p: E[K]) => void) {}
  emit<K extends keyof E>(...args: E[K] extends void ? [K] : [K, E[K]]) {}
}
const em = new Emitter<Ev>()
em.on('msg', (m) => m.toUpperCase())
em.emit('ping')
em.emit('msg', 'hi')
```

## Constraints vs intersections

`T extends Foo` constrains candidates; `T & Foo` forces members — different error messages and inference.

## Glossary

| Term | Definition |
| --- | --- |
| Type parameter | `T` in `<T>` |
| Constraint | `extends ...` bound |
| Instantiation | Filling `T` with a concrete type |
| Inference | Filling `T` from arguments |
| Default | `T = string` |


## Declaration vs call site

```ts
function zip<A, B>(a: A[], b: B[]): [A, B][] {
  return a.map((x, i) => [x, b[i]!])
}
zip([1], ['x']) // A=number, B=string inferred at call site
```

Library authors design signatures so inference “just works”; if users always pass type args, redesign.

## `extends` with unions of constraints

```ts
type Id = string | number
function show<T extends Id>(id: T): T { return id }
show(1)
show('a')
```
