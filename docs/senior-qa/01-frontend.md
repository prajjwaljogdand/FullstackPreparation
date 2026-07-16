# Senior Q&A — Frontend (1–40)

Practice aloud (~90–120s). Each item includes the expected answer, a common trap, follow-ups, trade-offs, and production notes.

## Q1. Explain the browser critical rendering path.

**Expected answer**

HTML parses to DOM; CSS to CSSOM; combined into a render tree; layout computes geometry; paint fills pixels; composite layers for the screen. JS can block parsing. Critical CSS/fonts gate FCP/LCP.

**Common wrong answer**

“Download HTML then paint” — skips CSSOM, layout, compositing, and script-blocking nuances.

**Follow-ups**

- `defer` vs `async`?
- What is layout thrashing?
- How does `content-visibility` help?

**Trade-offs**

- Inline critical CSS helps FCP but hurts cache reuse.
- Font subsetting vs brand completeness.

**Production relevance**

Optimize landing/auth LCP; measure with CrUX + lab tools.

---

## Q2. Microtasks vs macrotasks in the event loop.

**Expected answer**

After the call stack clears, the microtask queue (`Promise.then`, `queueMicrotask`) drains completely, then a macrotask runs (timers, I/O, many UI events). Rendering is scheduled around this. Node adds libuv phases.

**Common wrong answer**

“`setTimeout(0)` always runs before `Promise.then`” — false; microtasks run first.

**Follow-ups**

- Where does `requestAnimationFrame` fit?
- Infinite microtask scheduling impact?

**Trade-offs**

- Heavy microtasks starve paint/INP.
- Yielding to macrotasks improves responsiveness.

**Production relevance**

Keep fetch-then chains lean; break CPU work across turns.

---

## Q3. React reconciliation at a high level.

**Expected answer**

Fiber compares element type and key; same type → update props and recurse; different type → remount. Lists need stable keys. Concurrent rendering can interrupt/resume work before commit.

**Common wrong answer**

“React diffs the real DOM every render” — it diffs the virtual/Fiber tree, then commits minimal DOM ops.

**Follow-ups**

- Why keys matter?
- What is a bailout?
- How does React Compiler change memo guidance?

**Trade-offs**

- Index keys break state on reorder.
- Over-memoization adds complexity.

**Production relevance**

Feeds/tables: correct keys + virtualization prevent remount storms.

---

## Q4. Controlled vs uncontrolled inputs.

**Expected answer**

Controlled: React state is the source of truth (`value` + `onChange`). Uncontrolled: DOM owns the value (`ref`/`defaultValue`). Controlled enables live validation; file inputs are typically uncontrolled.

**Common wrong answer**

“Always controlled” — costly for huge forms and awkward for files.

**Follow-ups**

- Cursor jumps when formatting?
- How do libraries like RHF mix both?

**Trade-offs**

- Per-keystroke re-renders vs simplicity.
- Syncing uncontrolled values into app state.

**Production relevance**

Checkout fields often controlled; uploads uncontrolled; RHF for scale.

---

## Q5. When to use `useMemo` / `useCallback`.

**Expected answer**

Stabilize expensive pure computations or referential identity for memoized children/effect deps. Default is not to use them — profile first. React Compiler may memoize automatically.

**Common wrong answer**

Wrap every handler in `useCallback` even when children aren’t memoized.

**Follow-ups**

- Does `useMemo` guarantee no recomputation?
- Compiler vs hand memo?

**Trade-offs**

- Memo cost/noise vs render savings.
- Stale closures from bad deps.

**Production relevance**

Memoize heavy transforms fed into virtualized lists/charts.

---

## Q6. Context vs Redux/Zustand.

**Expected answer**

Context is great for infrequent values (theme, auth user). Frequent updates re-render all consumers. External stores with selectors give fine-grained subscriptions. Server state belongs in React Query/SWR, not Context.

**Common wrong answer**

“Put all server cache in Context” — render storms and sync bugs.

**Follow-ups**

- How do selectors prevent re-renders?
- When is Context enough?

**Trade-offs**

- Store boilerplate vs prop drilling.
- One mega-context vs many small ones.

**Production relevance**

Theme/auth Context; UI store for client state; React Query for API data.

---

## Q7. React Query stale-while-revalidate.

**Expected answer**

Cache keyed by `queryKey`. Stale data can still display while a background refetch updates it. `staleTime` defines freshness; `gcTime` controls inactive garbage collection. Mutations invalidate/update related keys.

**Common wrong answer**

“It just replaces `useEffect`” — ignores keys, invalidation, and deduping.

**Follow-ups**

- Invalidate vs `setQueryData`?
- What is structural sharing?

**Trade-offs**

- Short staleTime → more network; long → freshness risk.
- Optimistic updates vs rollback complexity.

**Production relevance**

Tune per resource; invalidate lists after creates/updates.

---

## Q8. SSR vs SSG vs ISR vs CSR (Next.js).

**Expected answer**

CSR: browser loads shell then data. SSR: HTML per request. SSG: build-time HTML. ISR: static + revalidation. App Router uses RSC/streaming; caching via `fetch` options, tags, and `revalidate`.

**Common wrong answer**

“SSR is always faster/better for SEO” — TTFB and cache hit rate decide.

**Follow-ups**

- When prefer RSC over client fetch?
- `revalidatePath` vs tags?

**Trade-offs**

- Personalization vs CDN caching.
- Rebuild cost of pure SSG vs ISR.

**Production relevance**

Marketing: SSG/ISR; authenticated app: dynamic + client islands.

---

## Q9. Hydration mismatch causes.

**Expected answer**

Server HTML ≠ first client render: `Date.now()`, random IDs, `window` without guards, invalid HTML nesting, extensions mutating DOM before hydrate.

**Common wrong answer**

Assume React is broken — usually nondeterministic app code.

**Follow-ups**

- Locale/date fixes?
- What does `suppressHydrationWarning` actually do?

**Trade-offs**

- Client-only rendering delays LCP/SEO.
- Determinism vs true randomness needs.

**Production relevance**

Guard browser APIs; consistent timezone formatting on server/client.

---

## Q10. Preventing XSS in React apps.

**Expected answer**

Text children are escaped by default. Risk vectors: `dangerouslySetInnerHTML`, unsanitized HTML, `javascript:` URLs, open redirects. Use sanitizers (DOMPurify), CSP, HttpOnly cookies.

**Common wrong answer**

“React means no XSS” — false once you inject HTML or unsafe URLs.

**Follow-ups**

- CSP nonces with Next?
- Why not store tokens in `localStorage`?

**Trade-offs**

- Strict CSP vs third-party scripts.
- Rich text features vs sanitization.

**Production relevance**

Sanitize CMS HTML; validate redirect targets; prefer HttpOnly sessions.

---

## Q11. CORS and when to use a BFF.

**Expected answer**

Browsers enforce same-origin; CORS headers allow cross-origin XHR/fetch. Non-simple requests preflight. A BFF (e.g. Next route handlers) keeps the browser same-origin while the server calls APIs with secrets.

**Common wrong answer**

`Access-Control-Allow-Origin: *` with credentials — browsers reject it.

**Follow-ups**

- Simple vs preflight?
- CSRF when using cookies?

**Trade-offs**

- Extra BFF hop vs exposing public APIs.
- Tight origin allowlists vs partner integrations.

**Production relevance**

SPA → BFF → internal services; cookie `SameSite` + CSRF for mutations.

---

## Q12. CSS cascade and specificity.

**Expected answer**

Cascade: origin/importance → specificity (inline > IDs > classes/attributes > elements) → source order. `@layer` manages library precedence. Shadow DOM scopes styles.

**Common wrong answer**

`!important` always wins forever — still ordered within importance/origin.

**Follow-ups**

- CSS Modules vs Tailwind conflict strategy?
- What problem do layers solve?

**Trade-offs**

- High specificity is hard to override.
- Utilities vs semantic classes.

**Production relevance**

Design systems: tokens + layers; avoid deep nested selectors.

---

## Q13. Layout vs paint vs composite.

**Expected answer**

Layout computes geometry; paint rasterizes; composite combines layers (often GPU). Animate `transform`/`opacity` to avoid layout/paint when possible.

**Common wrong answer**

Animate `top`/`width` freely — causes layout thrash and jank.

**Follow-ups**

- What promotes a layer?
- How to debug with Performance panel?

**Trade-offs**

- Too many layers → memory pressure.
- True layout changes still need layout.

**Production relevance**

Modal/toast motion via transforms; verify with Chrome Performance.

---

## Q14. List virtualization.

**Expected answer**

Render only visible rows (+ overscan). Needs item size estimates, scroll position math. Use TanStack Virtual / react-window. Mind focus and a11y.

**Common wrong answer**

Pagination always replaces virtualization — not for long continuous feeds.

**Follow-ups**

- Dynamic row heights?
- How keep screen-reader experience sane?

**Trade-offs**

- Implementation complexity vs DOM cost.
- Overscan smoothness vs extra work.

**Production relevance**

Admin grids, chat history, log viewers.

---

## Q15. Accessible modal checklist.

**Expected answer**

`role="dialog"`, `aria-modal`, label via `aria-labelledby`; focus trap; restore focus on close; Escape closes; background inert; honor `prefers-reduced-motion`.

**Common wrong answer**

Only handle outside click — ignore keyboard and SR users.

**Follow-ups**

- Nested dialogs?
- Is removing focus outlines ever OK?

**Trade-offs**

- Custom traps vs Radix/Headless UI.
- Animation vs reduced motion.

**Production relevance**

Prefer primitives; test keyboard + VoiceOver/NVDA.

---

## Q16. JavaScript bundle size tactics.

**Expected answer**

Route-based code splitting, analyze duplicates, prefer ESM tree-shaking, replace heavy libs, set CI size budgets, careful dynamic import UX.

**Common wrong answer**

“Tree shaking always deletes unused exports” — side-effectful CJS packages often don’t.

**Follow-ups**

- Detect duplicate React?
- When CDN a vendor lib?

**Trade-offs**

- Many tiny chunks vs request overhead.
- Loading spinners vs prefetch.

**Production relevance**

Next/Vite route splitting; fail CI on unexpected growth.

---

## Q17. Client vs server vs URL state.

**Expected answer**

Server state: remote resources (React Query). Client state: ephemeral UI. URL state: shareable filters/sort/page. Bookmarkable UI belongs in the URL.

**Common wrong answer**

Mirror all fetched lists into Redux — duplicated source of truth.

**Follow-ups**

- Sync filters to search params?
- Who owns optimistic entity patches?

**Trade-offs**

- URL length limits.
- Duplicating server cache in a client store.

**Production relevance**

E-commerce facets in URL; cart hybrid; catalog from query cache.

---

## Q18. Design system architecture.

**Expected answer**

Tokens → primitives → composites → patterns. A11y built in. Versioned package, docs, visual regression, strict peer deps.

**Common wrong answer**

Copy-paste styled components without tokens — inevitable drift.

**Follow-ups**

- CSS-in-JS vs Tailwind for a system?
- Theming strategy?

**Trade-offs**

- Flexibility vs consistency.
- Runtime style cost vs DX.

**Production relevance**

Publish internally; semantic versioning; visual tests in CI.

---

## Q19. Error boundaries: catch vs miss.

**Expected answer**

Catch render/lifecycle errors in the subtree and show fallback. Do not catch event handlers, async code, or SSR by themselves — need route `error.tsx`, try/catch, and reporting.

**Common wrong answer**

One boundary, no logging — failures become silent UX dead-ends.

**Follow-ups**

- Async error patterns?
- Next `error.tsx` vs class boundary?

**Trade-offs**

- Granular vs top-level boundaries.
- Retry vs hard fail.

**Production relevance**

Per-route boundaries + Sentry with release digests.

---

## Q20. Frontend testing strategy.

**Expected answer**

Unit pure logic; RTL for components (user-centric queries); Playwright for critical journeys; MSW for network. Keep e2e focused to reduce flake.

**Common wrong answer**

Enzyme snapshots for everything — brittle, low confidence.

**Follow-ups**

- Contract tests?
- Visual regression role?

**Trade-offs**

- E2E coverage vs flake cost.
- Mock fidelity vs realism.

**Production relevance**

PR: unit+component; deploy smoke e2e; nightly broader suite.

---

## Q21. HTTP caching for static assets.

**Expected answer**

Hashed assets: long `max-age` + `immutable`. HTML: short cache or revalidate. ETag/Last-Modified enable conditional requests. CDN sits in front.

**Common wrong answer**

Year-long cache on HTML — users stuck on old shells.

**Follow-ups**

- `stale-while-revalidate`?
- SW cache vs CDN?

**Trade-offs**

- Cache strength vs instant rollback needs — content hashes.
- `private` vs `public`.

**Production relevance**

Build pipelines emit hashed assets; edge rules for HTML.

---

## Q22. Service workers: value and pitfalls.

**Expected answer**

Intercept network for offline/PWA, push, background sync. Choose cache-first vs network-first carefully; version caches; plan updates (`skipWaiting`).

**Common wrong answer**

Ship a SW without an update strategy — clients stick on broken caches.

**Follow-ups**

- Force update UX?
- Security scope concerns?

**Trade-offs**

- Complexity vs offline value.
- Storage quotas.

**Production relevance**

Field/offline apps; never cache authenticated HTML naively.

---

## Q23. Core Web Vitals: LCP, CLS, INP.

**Expected answer**

LCP: largest content paint. CLS: unexpected layout shift. INP: interaction latency to next paint. Fix images/fonts/reserved space/long tasks/third parties.

**Common wrong answer**

Optimize only Lighthouse lab score — ignore field CrUX.

**Follow-ups**

- Lab vs field?
- Debug CLS practically?

**Trade-offs**

- Image quality vs LCP bytes.
- Third-party tags vs INP.

**Production relevance**

RUM dashboards + CI budgets; block regressions.

---

## Q24. CSRF with cookie sessions.

**Expected answer**

Cookies are sent automatically on cross-site navigations/requests depending on `SameSite`. Mitigate with `SameSite`, CSRF tokens, or avoid cookies for API auth (bearer). CORS ≠ CSRF protection.

**Common wrong answer**

“CORS stops CSRF” — incorrect mental model.

**Follow-ups**

- `SameSite=None` requirements?
- When Lax still vulnerable?

**Trade-offs**

- Strict cookies vs cross-site SSO.
- Token UX overhead.

**Production relevance**

BFF cookie session + CSRF on mutating routes.

---

## Q25. Image optimization in production.

**Expected answer**

Correct dimensions (anti-CLS), modern formats, `srcset`, CDN transforms, lazy below-fold, **eager/priority for LCP image**.

**Common wrong answer**

Lazy-load the LCP hero — directly hurts LCP.

**Follow-ups**

- Blur placeholders?
- Client resize vs CDN?

**Trade-offs**

- Encode CPU vs bandwidth.
- Art direction complexity.

**Production relevance**

Next/Image or CDN image pipeline; prioritize hero.

---

## Q26. TypeScript structural typing pitfalls.

**Expected answer**

Compatibility is by shape. Excess property checks apply to fresh literals. `any` disables checking; prefer `unknown` + narrowing. Use zod at boundaries; branded types for IDs.

**Common wrong answer**

Treat interfaces as nominal Java-style types.

**Follow-ups**

- Function parameter variance?
- When branding helps?

**Trade-offs**

- `strict` friction vs safety.
- Assertions vs runtime validation.

**Production relevance**

Validate API I/O at the edge of the app.

---

## Q27. Frontend monorepo layout.

**Expected answer**

`apps/` deployables, `packages/` shared UI/config. Clear boundaries, shared lint/tsconfig, task caching (Turborepo), ship only affected packages in CI.

**Common wrong answer**

One unstructured mega-`src` — coupling and slow CI.

**Follow-ups**

- Internal package versioning?
- How cache builds?

**Trade-offs**

- Shared package overhead vs copy-paste.
- Over-sharing types.

**Production relevance**

pnpm workspaces + Turborepo remote cache.

---

## Q28. Feature flags on the frontend.

**Expected answer**

Bootstrap flags without flicker (prefer server decision for SSR). Support kill switches and percentage rollouts. Clean up graduated flags.

**Common wrong answer**

Permanent `if (flag)` forever — permanent debt.

**Follow-ups**

- Prevent CLS across variants?
- Client vs server evaluation?

**Trade-offs**

- Flag debt vs ship speed.
- Realtime updates vs cached bootstrap.

**Production relevance**

Use a flag platform; remove flags after full rollout.

---

## Q29. Optimistic UI done right.

**Expected answer**

Update cache immediately, snapshot previous data, rollback on error, reconcile with server ids. React Query `onMutate`/`onError`/`onSettled` is the usual pattern.

**Common wrong answer**

Optimistic write with no rollback — permanent corruption on failure.

**Follow-ups**

- Concurrent mutation races?
- Idempotency keys?

**Trade-offs**

- Complexity vs perceived performance.
- Conflict resolution policy.

**Production relevance**

Likes, toggles, cart qty — low-risk high-frequency actions.

---

## Q30. Micro-frontends: when yes/no.

**Expected answer**

Justified for strong team/deploy autonomy at org scale. Costs: shared runtime, design consistency, auth, performance duplication. Alternatives: modular monorepo.

**Common wrong answer**

Default to MFEs for any mid-size app — usually premature.

**Follow-ups**

- Share one React copy?
- Cross-MFE routing?

**Trade-offs**

- Team autonomy vs UX consistency.
- Bundle duplication.

**Production relevance**

Adopt only with platform investment and clear ownership.

---

## Q31. Internationalization strategy.

**Expected answer**

Catalogs with ICU plurals, locale-aware `Intl` formats, locale routing, RTL testing, no string concatenation for sentences.

**Common wrong answer**

Translate labels only — ignore dates, numbers, legal copy, RTL.

**Follow-ups**

- SSR + locale?
- Pseudo-localization?

**Trade-offs**

- All locales in bundle vs async load.
- TMS cost vs in-house.

**Production relevance**

Per-route namespaces; Crowdin/Lokalise workflows.

---

## Q32. WebSocket vs SSE vs polling.

**Expected answer**

WS bidirectional; SSE one-way over HTTP with simpler reconnect; polling simplest with higher load/latency. Consider auth, backoff, ordering, mobile battery.

**Common wrong answer**

Always WebSocket — overkill for one-way notification feeds.

**Follow-ups**

- Reconnect/backoff design?
- At-least-once delivery handling?

**Trade-offs**

- Infra cost vs latency needs.
- Polling battery impact.

**Production relevance**

Notifications: SSE; collab editors: WS; metrics: poll/SWR.

---

## Q33. When form libraries beat DIY controlled state.

**Expected answer**

Large forms, field arrays, schema validation, performance → React Hook Form + zod. Uncontrolled registration reduces re-renders.

**Common wrong answer**

One giant controlled state object for 80 fields — input jank.

**Follow-ups**

- zod resolver wiring?
- Mirror server validation errors?

**Trade-offs**

- Dependency weight vs features.
- Multi-step wizard state ownership.

**Production relevance**

Checkout/onboarding: RHF + shared zod schemas with API.

---

## Q34. SPA memory leak sources.

**Expected answer**

Listeners/intervals/subscriptions not cleaned; caches that only grow; module singletons retaining screens; aborted fetches not canceled.

**Common wrong answer**

Blame React for all heap growth without snapshots.

**Follow-ups**

- Heap snapshot workflow?
- Where WeakRef helps?

**Trade-offs**

- Large cache UX vs memory.
- Global stores retaining routes.

**Production relevance**

Effect cleanups; bound query `gcTime`; profile navigate loops.

---

## Q35. CSS architecture at scale.

**Expected answer**

Design tokens, limited globals, scoped modules or utilities, consistent spacing/type scales, CSS variables for themes, lint against raw colors.

**Common wrong answer**

Ad-hoc class names with no tokens — visual inconsistency.

**Follow-ups**

- Modules vs Tailwind in a system?
- Runtime theming?

**Trade-offs**

- Utility verbosity vs custom CSS control.
- Global reset risks.

**Production relevance**

Document tokens; stylelint; dark mode via variables.

---

## Q36. Browser auth: cookies vs JWT storage.

**Expected answer**

Prefer HttpOnly Secure SameSite cookies via BFF. If SPA bearer tokens, keep access token in memory and refresh via cookie. Avoid long-lived JWT in `localStorage` (XSS).

**Common wrong answer**

`localStorage` JWT is fine because APIs are HTTPS — XSS still steals it.

**Follow-ups**

- Refresh rotation?
- Multi-tab logout sync?

**Trade-offs**

- Cookie CSRF needs vs bearer ergonomics.
- Web vs native storage models.

**Production relevance**

Web cookie sessions; mobile secure storage + refresh.

---

## Q37. GraphQL clients: cache and cost.

**Expected answer**

Normalized caches, fragments colocating fields, persisted queries, careful null/error partials. Still need authz and performance work on the server (N+1).

**Common wrong answer**

GraphQL automatically solves overfetch and auth — it doesn’t.

**Follow-ups**

- Persisted queries benefits?
- Client vs server N+1?

**Trade-offs**

- Schema coupling vs REST/tRPC simplicity.
- Cache complexity.

**Production relevance**

Use when many clients need flexible graphs; otherwise simpler RPC is fine.

---

## Q38. Improving INP / long tasks.

**Expected answer**

Split work (`scheduler.yield`, chunking), keep event handlers light, virtualize, move CPU to workers, reduce hydration JS, defer non-critical third parties.

**Common wrong answer**

Only shrink bundle — main-thread long tasks still destroy INP.

**Follow-ups**

- Profile an interaction?
- Worker + DOM limitations?

**Trade-offs**

- Worker serialization overhead.
- Deferred UI consistency.

**Production relevance**

Lightweight handlers; heavy analytics after idle.

---

## Q39. Reusable component API design.

**Expected answer**

Prefer composition over boolean knobs; forward a11y props; support controlled/uncontrolled where needed; limited variants; treat as versioned public API.

**Common wrong answer**

20 booleans (`sizeSm`, `danger`, …) — combinatorial explosion.

**Follow-ups**

- Polymorphic `as` pitfalls?
- Headless vs styled?

**Trade-offs**

- Flexibility vs guardrails.
- Breaking change policy / codemods.

**Production relevance**

Design-system RFCs; semver; visual regression.

---

## Q40. Migrating CRA → Next App Router.

**Expected answer**

Strangle pattern: shared UI package, migrate high-value routes first, introduce RSC gradually, keep client islands, fix auth/cookies/env split, measure CWV continuously.

**Common wrong answer**

Big-bang rewrite in a quarter — usually fails.

**Follow-ups**

- Client-only libraries?
- `NEXT_PUBLIC_` boundaries?

**Trade-offs**

- Dual-system cost vs incremental value.
- SEO gains vs eng time.

**Production relevance**

Ship marketing/SSR wins first; keep authenticated app stable.
