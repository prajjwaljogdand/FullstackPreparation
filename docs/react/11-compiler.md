# React Compiler

The React Compiler (formerly React Forget) is a build-time optimizing compiler that **automatically memoizes** values and components where it can prove purity rules hold — reducing the need for hand-written `useMemo` / `useCallback` / `memo`. It does not replace React; it generates code that plays with the runtime’s bailout mechanisms.

## Problem it solves

Manual memoization is:

- Easy to get wrong (unstable deps, over/under memo)
- Noisy (wrapper hell)
- Incomplete (missed hot paths)

The compiler analyzes render functions and inserts memoization slots akin to what you’d write by hand — but consistently.

```mermaid
flowchart LR
  S[Source component] --> C[React Compiler]
  C --> O[Optimized JS with memo cache]
  O --> R[React runtime bailouts]
```

## Purity rules (what the compiler assumes)

Components and hooks should be **idempotent** with respect to render:

- No mutating props/state during render
- No reading/writing external mutable stores during render without proper APIs
- Same inputs → same output elements (modulo intentional non-determinism you opt out of)

```tsx
// ❌ Impure render — compiler may bail out of optimizing
let id = 0
function List({ items }: { items: string[] }) {
  return items.map((x) => <li key={id++}>{x}</li>) // unstable keys + mutation
}

// ✅
function List({ items }: { items: string[] }) {
  return items.map((x) => <li key={x}>{x}</li>)
}
```

## Mental model of generated memo

Conceptually (not exact emitted code):

```tsx
function Profile({ user }: { user: User }) {
  'use memo' // illustrative
  const label = user.first + ' ' + user.last
  return <Card title={label} />
}

// Compiler roughly:
function Profile(props) {
  const $ = useMemoCache(n)
  const user = props.user
  let label
  if ($[0] !== user) {
    label = user.first + ' ' + user.last
    $[0] = user
    $[1] = label
  } else {
    label = $[1]
  }
  // similarly memoize element creation for Card
  return /* cached element */
}
```

Dependencies are tracked by **mutability / value identity analysis**, not by you listing deps arrays.

## Enabling (ecosystem sketch)

Exact setup evolves — interview-level:

- Babel/SWC plugin in Next.js / Vite / Metro
- ESLint plugin `eslint-plugin-react-compiler` to surface rule violations
- Opt-out directives when needed (e.g. `"use no memo"` at function level — check current docs for exact pragma)

```js
// next.config — conceptual
const nextConfig = {
  experimental: {
    reactCompiler: true,
  },
}
```

Always verify against current Next/React docs for the flag name.

## What it does **not** do

- Doesn’t remove the need for **virtualization** or architectural state colocation
- Doesn’t make impure effects safe
- Doesn’t automatically parallelize network
- Doesn’t replace `startTransition` for priority
- Won’t optimize across modules it can’t analyze

## Compiler vs manual memo

| | Compiler | Manual |
| --- | --- | --- |
| Coverage | Broad, consistent | Spotty |
| Correctness | Tied to purity lint | Easy stale deps |
| Escape hatches | Directives / eslint suppress | Everywhere |
| Debugging | Need to understand cache | Explicit hooks |
| Legacy code | May skip unsafe functions | Already annotated |

Keep intentional `useMemo` when:

- Memoizing **non-React** expensive work you want explicit
- Coordinating with libs that depend on reference equality and compiler skip
- Until compiler covers your toolchain

## Rules of React (reinforced)

1. **Pure renders** — compute, don’t command.
2. **One-way data** — props down, events up.
3. **Immutability** — don’t mutate props/state; copy.
4. **Effects for sync** — external systems only.

The compiler is the enforcement + reward mechanism for those rules.

## Interview Q&A

**Q: What is React Compiler?**  
A: A build-time compiler that auto-memoizes React components/hooks when safe, reducing manual `memo`/`useMemo`/`useCallback`.

**Q: Does it change React semantics?**  
A: It should preserve semantics for pure components; impure code may be unoptimized or flagged.

**Q: Still need useMemo?**  
A: Less often. Still understand it; use when compiler doesn’t apply or for non-UI expensive work.

**Q: How does it know dependencies?**  
A: Static analysis of reads/writes and reactive values — not a deps array you write.

**Q: Relation to Forget?**  
A: “React Forget” was the research/code name; shipped branding is React Compiler.

**Q: Can it break my app?**  
A: If you relied on impure render behavior (accidental), optimizing might expose bugs — that’s good; fix purity.

## Common Mistakes

- Expecting compiler to fix Context blast radius — still split stores/contexts.
- Mutating arrays/objects in render and blaming the compiler.
- Disabling eslint rules instead of fixing violations.
- Assuming zero need to profile after enabling.
- Shipping compiler without CI lint for purity regressions.

## Trade-offs

| Aspect | Upside | Downside |
| --- | --- | --- |
| Auto-memo | Less boilerplate | Build complexity |
| Purity lint | Catches bugs early | Migration cost on impure codebases |
| Cache slots | Fine-grained bailouts | Slightly harder to mentally simulate |
| Opt-out pragmas | Escape hatch | Fragmentation if overused |

**Senior takeaway:** React Compiler industrializes memoization under the **Rules of React**. In interviews, connect purity → auto-memo → fewer manual hooks, while admitting architecture (state location, lists, concurrency) still matters.



## Migration playbook

1. Enable eslint-plugin-react-compiler in CI  
2. Fix impure render violations  
3. Turn on compiler for app or per-directory  
4. Remove redundant manual memos gradually  
5. Profile before/after on slow routes  

## Extra Q&A

**Q: Does the compiler rewrite hooks?**  
A: It memoizes around expressions/jsx; hooks still exist and must follow rules — compiler doesn’t let you call hooks conditionally.
