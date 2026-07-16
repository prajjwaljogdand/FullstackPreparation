from pathlib import Path

OUT = Path("/Users/prajjwal/jvl/interview/docs/senior-qa")
OUT.mkdir(parents=True, exist_ok=True)

def Q(n, title, expected, wrong, followups, tradeoffs, prod):
    fu = "\n".join(f"- {x}" for x in followups)
    to = "\n".join(f"- {x}" for x in tradeoffs)
    return f"""## Q{n}. {title}

**Expected answer**

{expected}

**Common wrong answer**

{wrong}

**Follow-ups**

{fu}

**Trade-offs**

{to}

**Production relevance**

{prod}
"""

fe = []

fe.append(Q(1, "Explain the browser critical rendering path.",
"HTML parses to DOM; CSS to CSSOM; combined into a render tree; layout computes geometry; paint fills pixels; composite layers for the screen. JS can block parsing. Critical CSS/fonts gate FCP/LCP.",
"“Download HTML then paint” — skips CSSOM, layout, compositing, and script-blocking nuances.",
["`defer` vs `async`?", "What is layout thrashing?", "How does `content-visibility` help?"],
["Inline critical CSS helps FCP but hurts cache reuse.", "Font subsetting vs brand completeness."],
"Optimize landing/auth LCP; measure with CrUX + lab tools."))

fe.append(Q(2, "Microtasks vs macrotasks in the event loop.",
"After the call stack clears, the microtask queue (`Promise.then`, `queueMicrotask`) drains completely, then a macrotask runs (timers, I/O, many UI events). Rendering is scheduled around this. Node adds libuv phases.",
"“`setTimeout(0)` always runs before `Promise.then`” — false; microtasks run first.",
["Where does `requestAnimationFrame` fit?", "Infinite microtask scheduling impact?"],
["Heavy microtasks starve paint/INP.", "Yielding to macrotasks improves responsiveness."],
"Keep fetch-then chains lean; break CPU work across turns."))

fe.append(Q(3, "React reconciliation at a high level.",
"Fiber compares element type and key; same type → update props and recurse; different type → remount. Lists need stable keys. Concurrent rendering can interrupt/resume work before commit.",
"“React diffs the real DOM every render” — it diffs the virtual/Fiber tree, then commits minimal DOM ops.",
["Why keys matter?", "What is a bailout?", "How does React Compiler change memo guidance?"],
["Index keys break state on reorder.", "Over-memoization adds complexity."],
"Feeds/tables: correct keys + virtualization prevent remount storms."))

fe.append(Q(4, "Controlled vs uncontrolled inputs.",
"Controlled: React state is the source of truth (`value` + `onChange`). Uncontrolled: DOM owns the value (`ref`/`defaultValue`). Controlled enables live validation; file inputs are typically uncontrolled.",
"“Always controlled” — costly for huge forms and awkward for files.",
["Cursor jumps when formatting?", "How do libraries like RHF mix both?"],
["Per-keystroke re-renders vs simplicity.", "Syncing uncontrolled values into app state."],
"Checkout fields often controlled; uploads uncontrolled; RHF for scale."))

fe.append(Q(5, "When to use `useMemo` / `useCallback`.",
"Stabilize expensive pure computations or referential identity for memoized children/effect deps. Default is not to use them — profile first. React Compiler may memoize automatically.",
"Wrap every handler in `useCallback` even when children aren’t memoized.",
["Does `useMemo` guarantee no recomputation?", "Compiler vs hand memo?"],
["Memo cost/noise vs render savings.", "Stale closures from bad deps."],
"Memoize heavy transforms fed into virtualized lists/charts."))

fe.append(Q(6, "Context vs Redux/Zustand.",
"Context is great for infrequent values (theme, auth user). Frequent updates re-render all consumers. External stores with selectors give fine-grained subscriptions. Server state belongs in React Query/SWR, not Context.",
"“Put all server cache in Context” — render storms and sync bugs.",
["How do selectors prevent re-renders?", "When is Context enough?"],
["Store boilerplate vs prop drilling.", "One mega-context vs many small ones."],
"Theme/auth Context; UI store for client state; React Query for API data."))

fe.append(Q(7, "React Query stale-while-revalidate.",
"Cache keyed by `queryKey`. Stale data can still display while a background refetch updates it. `staleTime` defines freshness; `gcTime` controls inactive garbage collection. Mutations invalidate/update related keys.",
"“It just replaces `useEffect`” — ignores keys, invalidation, and deduping.",
["Invalidate vs `setQueryData`?", "What is structural sharing?"],
["Short staleTime → more network; long → freshness risk.", "Optimistic updates vs rollback complexity."],
"Tune per resource; invalidate lists after creates/updates."))

fe.append(Q(8, "SSR vs SSG vs ISR vs CSR (Next.js).",
"CSR: browser loads shell then data. SSR: HTML per request. SSG: build-time HTML. ISR: static + revalidation. App Router uses RSC/streaming; caching via `fetch` options, tags, and `revalidate`.",
"“SSR is always faster/better for SEO” — TTFB and cache hit rate decide.",
["When prefer RSC over client fetch?", "`revalidatePath` vs tags?"],
["Personalization vs CDN caching.", "Rebuild cost of pure SSG vs ISR."],
"Marketing: SSG/ISR; authenticated app: dynamic + client islands."))

fe.append(Q(9, "Hydration mismatch causes.",
"Server HTML ≠ first client render: `Date.now()`, random IDs, `window` without guards, invalid HTML nesting, extensions mutating DOM before hydrate.",
"Assume React is broken — usually nondeterministic app code.",
["Locale/date fixes?", "What does `suppressHydrationWarning` actually do?"],
["Client-only rendering delays LCP/SEO.", "Determinism vs true randomness needs."],
"Guard browser APIs; consistent timezone formatting on server/client."))

fe.append(Q(10, "Preventing XSS in React apps.",
"Text children are escaped by default. Risk vectors: `dangerouslySetInnerHTML`, unsanitized HTML, `javascript:` URLs, open redirects. Use sanitizers (DOMPurify), CSP, HttpOnly cookies.",
"“React means no XSS” — false once you inject HTML or unsafe URLs.",
["CSP nonces with Next?", "Why not store tokens in `localStorage`?"],
["Strict CSP vs third-party scripts.", "Rich text features vs sanitization."],
"Sanitize CMS HTML; validate redirect targets; prefer HttpOnly sessions."))

fe.append(Q(11, "CORS and when to use a BFF.",
"Browsers enforce same-origin; CORS headers allow cross-origin XHR/fetch. Non-simple requests preflight. A BFF (e.g. Next route handlers) keeps the browser same-origin while the server calls APIs with secrets.",
"`Access-Control-Allow-Origin: *` with credentials — browsers reject it.",
["Simple vs preflight?", "CSRF when using cookies?"],
["Extra BFF hop vs exposing public APIs.", "Tight origin allowlists vs partner integrations."],
"SPA → BFF → internal services; cookie `SameSite` + CSRF for mutations."))

fe.append(Q(12, "CSS cascade and specificity.",
"Cascade: origin/importance → specificity (inline > IDs > classes/attributes > elements) → source order. `@layer` manages library precedence. Shadow DOM scopes styles.",
"`!important` always wins forever — still ordered within importance/origin.",
["CSS Modules vs Tailwind conflict strategy?", "What problem do layers solve?"],
["High specificity is hard to override.", "Utilities vs semantic classes."],
"Design systems: tokens + layers; avoid deep nested selectors."))

fe.append(Q(13, "Layout vs paint vs composite.",
"Layout computes geometry; paint rasterizes; composite combines layers (often GPU). Animate `transform`/`opacity` to avoid layout/paint when possible.",
"Animate `top`/`width` freely — causes layout thrash and jank.",
["What promotes a layer?", "How to debug with Performance panel?"],
["Too many layers → memory pressure.", "True layout changes still need layout."],
"Modal/toast motion via transforms; verify with Chrome Performance."))

fe.append(Q(14, "List virtualization.",
"Render only visible rows (+ overscan). Needs item size estimates, scroll position math. Use TanStack Virtual / react-window. Mind focus and a11y.",
"Pagination always replaces virtualization — not for long continuous feeds.",
["Dynamic row heights?", "How keep screen-reader experience sane?"],
["Implementation complexity vs DOM cost.", "Overscan smoothness vs extra work."],
"Admin grids, chat history, log viewers."))

fe.append(Q(15, "Accessible modal checklist.",
"`role=\"dialog\"`, `aria-modal`, label via `aria-labelledby`; focus trap; restore focus on close; Escape closes; background inert; honor `prefers-reduced-motion`.",
"Only handle outside click — ignore keyboard and SR users.",
["Nested dialogs?", "Is removing focus outlines ever OK?"],
["Custom traps vs Radix/Headless UI.", "Animation vs reduced motion."],
"Prefer primitives; test keyboard + VoiceOver/NVDA."))

fe.append(Q(16, "JavaScript bundle size tactics.",
"Route-based code splitting, analyze duplicates, prefer ESM tree-shaking, replace heavy libs, set CI size budgets, careful dynamic import UX.",
"“Tree shaking always deletes unused exports” — side-effectful CJS packages often don’t.",
["Detect duplicate React?", "When CDN a vendor lib?"],
["Many tiny chunks vs request overhead.", "Loading spinners vs prefetch."],
"Next/Vite route splitting; fail CI on unexpected growth."))

fe.append(Q(17, "Client vs server vs URL state.",
"Server state: remote resources (React Query). Client state: ephemeral UI. URL state: shareable filters/sort/page. Bookmarkable UI belongs in the URL.",
"Mirror all fetched lists into Redux — duplicated source of truth.",
["Sync filters to search params?", "Who owns optimistic entity patches?"],
["URL length limits.", "Duplicating server cache in a client store."],
"E-commerce facets in URL; cart hybrid; catalog from query cache."))

fe.append(Q(18, "Design system architecture.",
"Tokens → primitives → composites → patterns. A11y built in. Versioned package, docs, visual regression, strict peer deps.",
"Copy-paste styled components without tokens — inevitable drift.",
["CSS-in-JS vs Tailwind for a system?", "Theming strategy?"],
["Flexibility vs consistency.", "Runtime style cost vs DX."],
"Publish internally; semantic versioning; visual tests in CI."))

fe.append(Q(19, "Error boundaries: catch vs miss.",
"Catch render/lifecycle errors in the subtree and show fallback. Do not catch event handlers, async code, or SSR by themselves — need route `error.tsx`, try/catch, and reporting.",
"One boundary, no logging — failures become silent UX dead-ends.",
["Async error patterns?", "Next `error.tsx` vs class boundary?"],
["Granular vs top-level boundaries.", "Retry vs hard fail."],
"Per-route boundaries + Sentry with release digests."))

fe.append(Q(20, "Frontend testing strategy.",
"Unit pure logic; RTL for components (user-centric queries); Playwright for critical journeys; MSW for network. Keep e2e focused to reduce flake.",
"Enzyme snapshots for everything — brittle, low confidence.",
["Contract tests?", "Visual regression role?"],
["E2E coverage vs flake cost.", "Mock fidelity vs realism."],
"PR: unit+component; deploy smoke e2e; nightly broader suite."))

fe.append(Q(21, "HTTP caching for static assets.",
"Hashed assets: long `max-age` + `immutable`. HTML: short cache or revalidate. ETag/Last-Modified enable conditional requests. CDN sits in front.",
"Year-long cache on HTML — users stuck on old shells.",
["`stale-while-revalidate`?", "SW cache vs CDN?"],
["Cache strength vs instant rollback needs — content hashes.", "`private` vs `public`."],
"Build pipelines emit hashed assets; edge rules for HTML."))

fe.append(Q(22, "Service workers: value and pitfalls.",
"Intercept network for offline/PWA, push, background sync. Choose cache-first vs network-first carefully; version caches; plan updates (`skipWaiting`).",
"Ship a SW without an update strategy — clients stick on broken caches.",
["Force update UX?", "Security scope concerns?"],
["Complexity vs offline value.", "Storage quotas."],
"Field/offline apps; never cache authenticated HTML naively."))

fe.append(Q(23, "Core Web Vitals: LCP, CLS, INP.",
"LCP: largest content paint. CLS: unexpected layout shift. INP: interaction latency to next paint. Fix images/fonts/reserved space/long tasks/third parties.",
"Optimize only Lighthouse lab score — ignore field CrUX.",
["Lab vs field?", "Debug CLS practically?"],
["Image quality vs LCP bytes.", "Third-party tags vs INP."],
"RUM dashboards + CI budgets; block regressions."))

fe.append(Q(24, "CSRF with cookie sessions.",
"Cookies are sent automatically on cross-site navigations/requests depending on `SameSite`. Mitigate with `SameSite`, CSRF tokens, or avoid cookies for API auth (bearer). CORS ≠ CSRF protection.",
"“CORS stops CSRF” — incorrect mental model.",
["`SameSite=None` requirements?", "When Lax still vulnerable?"],
["Strict cookies vs cross-site SSO.", "Token UX overhead."],
"BFF cookie session + CSRF on mutating routes."))

fe.append(Q(25, "Image optimization in production.",
"Correct dimensions (anti-CLS), modern formats, `srcset`, CDN transforms, lazy below-fold, **eager/priority for LCP image**.",
"Lazy-load the LCP hero — directly hurts LCP.",
["Blur placeholders?", "Client resize vs CDN?"],
["Encode CPU vs bandwidth.", "Art direction complexity."],
"Next/Image or CDN image pipeline; prioritize hero."))

fe.append(Q(26, "TypeScript structural typing pitfalls.",
"Compatibility is by shape. Excess property checks apply to fresh literals. `any` disables checking; prefer `unknown` + narrowing. Use zod at boundaries; branded types for IDs.",
"Treat interfaces as nominal Java-style types.",
["Function parameter variance?", "When branding helps?"],
["`strict` friction vs safety.", "Assertions vs runtime validation."],
"Validate API I/O at the edge of the app."))

fe.append(Q(27, "Frontend monorepo layout.",
"`apps/` deployables, `packages/` shared UI/config. Clear boundaries, shared lint/tsconfig, task caching (Turborepo), ship only affected packages in CI.",
"One unstructured mega-`src` — coupling and slow CI.",
["Internal package versioning?", "How cache builds?"],
["Shared package overhead vs copy-paste.", "Over-sharing types."],
"pnpm workspaces + Turborepo remote cache."))

fe.append(Q(28, "Feature flags on the frontend.",
"Bootstrap flags without flicker (prefer server decision for SSR). Support kill switches and percentage rollouts. Clean up graduated flags.",
"Permanent `if (flag)` forever — permanent debt.",
["Prevent CLS across variants?", "Client vs server evaluation?"],
["Flag debt vs ship speed.", "Realtime updates vs cached bootstrap."],
"Use a flag platform; remove flags after full rollout."))

fe.append(Q(29, "Optimistic UI done right.",
"Update cache immediately, snapshot previous data, rollback on error, reconcile with server ids. React Query `onMutate`/`onError`/`onSettled` is the usual pattern.",
"Optimistic write with no rollback — permanent corruption on failure.",
["Concurrent mutation races?", "Idempotency keys?"],
["Complexity vs perceived performance.", "Conflict resolution policy."],
"Likes, toggles, cart qty — low-risk high-frequency actions."))

fe.append(Q(30, "Micro-frontends: when yes/no.",
"Justified for strong team/deploy autonomy at org scale. Costs: shared runtime, design consistency, auth, performance duplication. Alternatives: modular monorepo.",
"Default to MFEs for any mid-size app — usually premature.",
["Share one React copy?", "Cross-MFE routing?"],
["Team autonomy vs UX consistency.", "Bundle duplication."],
"Adopt only with platform investment and clear ownership."))

fe.append(Q(31, "Internationalization strategy.",
"Catalogs with ICU plurals, locale-aware `Intl` formats, locale routing, RTL testing, no string concatenation for sentences.",
"Translate labels only — ignore dates, numbers, legal copy, RTL.",
["SSR + locale?", "Pseudo-localization?"],
["All locales in bundle vs async load.", "TMS cost vs in-house."],
"Per-route namespaces; Crowdin/Lokalise workflows."))

fe.append(Q(32, "WebSocket vs SSE vs polling.",
"WS bidirectional; SSE one-way over HTTP with simpler reconnect; polling simplest with higher load/latency. Consider auth, backoff, ordering, mobile battery.",
"Always WebSocket — overkill for one-way notification feeds.",
["Reconnect/backoff design?", "At-least-once delivery handling?"],
["Infra cost vs latency needs.", "Polling battery impact."],
"Notifications: SSE; collab editors: WS; metrics: poll/SWR."))

fe.append(Q(33, "When form libraries beat DIY controlled state.",
"Large forms, field arrays, schema validation, performance → React Hook Form + zod. Uncontrolled registration reduces re-renders.",
"One giant controlled state object for 80 fields — input jank.",
["zod resolver wiring?", "Mirror server validation errors?"],
["Dependency weight vs features.", "Multi-step wizard state ownership."],
"Checkout/onboarding: RHF + shared zod schemas with API."))

fe.append(Q(34, "SPA memory leak sources.",
"Listeners/intervals/subscriptions not cleaned; caches that only grow; module singletons retaining screens; aborted fetches not canceled.",
"Blame React for all heap growth without snapshots.",
["Heap snapshot workflow?", "Where WeakRef helps?"],
["Large cache UX vs memory.", "Global stores retaining routes."],
"Effect cleanups; bound query `gcTime`; profile navigate loops."))

fe.append(Q(35, "CSS architecture at scale.",
"Design tokens, limited globals, scoped modules or utilities, consistent spacing/type scales, CSS variables for themes, lint against raw colors.",
"Ad-hoc class names with no tokens — visual inconsistency.",
["Modules vs Tailwind in a system?", "Runtime theming?"],
["Utility verbosity vs custom CSS control.", "Global reset risks."],
"Document tokens; stylelint; dark mode via variables."))

fe.append(Q(36, "Browser auth: cookies vs JWT storage.",
"Prefer HttpOnly Secure SameSite cookies via BFF. If SPA bearer tokens, keep access token in memory and refresh via cookie. Avoid long-lived JWT in `localStorage` (XSS).",
"`localStorage` JWT is fine because APIs are HTTPS — XSS still steals it.",
["Refresh rotation?", "Multi-tab logout sync?"],
["Cookie CSRF needs vs bearer ergonomics.", "Web vs native storage models."],
"Web cookie sessions; mobile secure storage + refresh."))

fe.append(Q(37, "GraphQL clients: cache and cost.",
"Normalized caches, fragments colocating fields, persisted queries, careful null/error partials. Still need authz and performance work on the server (N+1).",
"GraphQL automatically solves overfetch and auth — it doesn’t.",
["Persisted queries benefits?", "Client vs server N+1?"],
["Schema coupling vs REST/tRPC simplicity.", "Cache complexity."],
"Use when many clients need flexible graphs; otherwise simpler RPC is fine."))

fe.append(Q(38, "Improving INP / long tasks.",
"Split work (`scheduler.yield`, chunking), keep event handlers light, virtualize, move CPU to workers, reduce hydration JS, defer non-critical third parties.",
"Only shrink bundle — main-thread long tasks still destroy INP.",
["Profile an interaction?", "Worker + DOM limitations?"],
["Worker serialization overhead.", "Deferred UI consistency."],
"Lightweight handlers; heavy analytics after idle."))

fe.append(Q(39, "Reusable component API design.",
"Prefer composition over boolean knobs; forward a11y props; support controlled/uncontrolled where needed; limited variants; treat as versioned public API.",
"20 booleans (`sizeSm`, `danger`, …) — combinatorial explosion.",
["Polymorphic `as` pitfalls?", "Headless vs styled?"],
["Flexibility vs guardrails.", "Breaking change policy / codemods."],
"Design-system RFCs; semver; visual regression."))

fe.append(Q(40, "Migrating CRA → Next App Router.",
"Strangle pattern: shared UI package, migrate high-value routes first, introduce RSC gradually, keep client islands, fix auth/cookies/env split, measure CWV continuously.",
"Big-bang rewrite in a quarter — usually fails.",
["Client-only libraries?", "`NEXT_PUBLIC_` boundaries?"],
["Dual-system cost vs incremental value.", "SEO gains vs eng time."],
"Ship marketing/SSR wins first; keep authenticated app stable."))

header = """# Senior Q&A — Frontend (1–40)

Practice aloud (~90–120s). Each item includes the expected answer, a common trap, follow-ups, trade-offs, and production notes.

"""
(OUT / "01-frontend.md").write_text(header + "\n---\n\n".join(fe))
print("frontend", len(fe))
