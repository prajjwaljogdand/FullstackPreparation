from pathlib import Path

OUT = Path("/Users/prajjwal/jvl/interview/docs/senior-qa")

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

fs = []

fs.append(Q(81, "End-to-end auth for a Next.js + API app.",
"Prefer BFF: browser hits Next same-origin; server sets HttpOnly Secure SameSite session cookie; API validates session/JWT server-side; CSRF for cookie mutations; refresh/rotation; logout clears server session.",
"SPA stores long-lived JWT in `localStorage` and calls APIs directly — XSS = account theft.",
["How protect Server Actions?", "Mobile client differences?"],
["Cookie CSRF complexity vs bearer simplicity.", "SSR session fetch vs edge middleware checks."],
"NextAuth/Auth.js or custom BFF sessions; never trust client role flags."))

fs.append(Q(82, "Design a full-stack feature: “shareable filtered table”.",
"Filters/sort/page in URL; server or client fetch with React Query keyed by URL; API cursor pagination + indexes; columns virtualized; export async; authz on API.",
"Keep filters only in React state — not shareable/bookmarkable.",
["SSR first paint with filters?", "How avoid double fetch in App Router?"],
["URL complexity vs shareability.", "Server tables vs client interactivity."],
"Admin consoles and search results pages use this pattern constantly."))

fs.append(Q(83, "Optimistic UI across client cache and DB.",
"Client patches React Query cache; API uses idempotency key; server returns canonical entity; client reconciles; rollback on failure; conflict policy (LWW/version).",
"Optimistic update without server version checks — silent overwrites.",
["How handle two tabs?", "ETag/If-Match?"],
["Speed vs correctness.", "Conflict UX complexity."],
"Collaborative settings and carts need explicit conflict rules."))

fs.append(Q(84, "File upload full-stack flow.",
"Client requests pre-signed URL from API (authz); uploads direct to S3; notifies API with object key; virus scan/async processing; UI polls or receives WS/SSE status.",
"Upload multipart through Next API to disk on serverless — size/time limits and cost.",
["How secure the complete callback?", "Progress UX?"],
["Direct upload vs proxy control.", "Multipart complexity."],
"Avatars/docs: pre-sign + async pipeline + CDN read."))

fs.append(Q(85, "Realtime chat: FE + BE outline.",
"WS/SSE gateway; messages persisted; fan-out via pub/sub; client virtualized list; optimistic send; delivery/read receipts; auth on connect; backpressure; rate limits; media via object storage.",
"Store messages only in memory on one node — lost on deploy.",
["How scale WS horizontally?", "Ordering guarantees?"],
["WS infra cost vs polling latency.", "Exactly-once vs idempotent message ids."],
"Chat services: sticky or pub/sub broadcaster + durable store."))

fs.append(Q(86, "tRPC vs REST vs GraphQL for your stack.",
"tRPC: great TS monorepo end-to-end types. REST: universal, cacheable, public ecosystems. GraphQL: flexible client shapes, heavier cache/auth complexity. Choose based on clients and team.",
"GraphQL because it’s modern — ignoring ops and authz complexity.",
["How expose public third-party API if internal is tRPC?", "Versioning?"],
["Type safety vs ecosystem constraints.", "BFF proliferation."],
"Internal product: tRPC/REST; public partners: versioned REST."))

fs.append(Q(87, "End-to-end type safety strategies.",
"Shared zod schemas or OpenAPI → types; validate at boundaries; never trust network types; generate clients; branded IDs; avoid `as` casts on API results.",
"Share only TypeScript interfaces without runtime validation — lies at runtime.",
["zod vs OpenAPI first?", "How version schemas?"],
["Strictness vs shipping speed.", "Generated code churn."],
"Monorepo shared contracts package used by web and API."))

fs.append(Q(88, "Caching across CDN, HTTP, Redis, and React Query.",
"Layers: browser/CDN for public; Redis for shared server reads; React Query for per-client session UX. Define TTLs and invalidation ownership per layer; don’t double-cache secrets.",
"Cache personalized HTML at CDN without Vary/cookie strategy — data leaks.",
["How invalidate CDN on publish?", "Cache key design?"],
["Hit rate vs personalization.", "Stale layers fighting each other."],
"Public marketing CDN; user dashboards Redis+RQ with careful keys."))

fs.append(Q(89, "SSR data fetching auth pitfalls.",
"Forward cookies carefully; don’t cache authenticated RSC/fetch globally; use `cache: 'no-store'` or per-user keys; never log secrets; consistent auth between middleware and server components.",
"Cache `fetch` of user profile across users — cross-user data leak.",
["How pass auth to nested fetches?", "Edge middleware limits?"],
["CDN caching vs auth correctness.", "Duplicated auth checks."],
"Review every cached fetch for user-specific data."))

fs.append(Q(90, "Search feature full-stack.",
"Indexer async from source DB; query API with relevance + filters; debounce FE input; highlight; empty states; rate limit; fallback to SQL if search cluster down.",
"Live `LIKE %q%` on primary for every keystroke at scale — DB melt.",
["How keep index fresh?", "Typo tolerance?"],
["Search quality vs infra cost.", "Eventual consistency of results."],
"Postgres FTS first; ES when facets/relevance demand it."))

fs.append(Q(91, "Payments full-stack (Stripe-like).",
"Checkout session or PaymentIntent on server; never handle raw cards if possible (hosted fields); webhooks as source of truth; idempotent webhook handlers; reconcile UI via status API.",
"Trust client `paymentSuccess=true` redirect alone — forgeable.",
["Webhook signature verify?", "How handle delayed async payment methods?"],
["PCI scope reduction vs custom UX.", "Idempotency storage."],
"Stripe Checkout/Elements + webhook outbox pattern."))

fs.append(Q(92, "Feature flags across FE and BE.",
"Same flag keys evaluated in both tiers; backend enforces for security; frontend for UX. Bootstrap without flicker; audit; clean up.",
"FE-only flags for authz — trivially bypassed.",
["Percentage rollout consistency?", "Kill switch during incident?"],
["Consistency lag between tiers.", "Flag debt."],
"Security-sensitive flags must be server-enforced."))

fs.append(Q(93, "Observability across FE and BE.",
"Correlate browser RUM trace/span ids with backend traces; shared `request_id`; FE error reporting with release; BE metrics/logs/traces; dashboards for journey success (checkout).",
"Only backend APM — miss JS errors killing conversion.",
["How sample without losing SEVs?", "PII scrubbing in FE logs?"],
["Cardinality/cost vs visibility.", "Privacy constraints."],
"Sentry + OpenTelemetry end-to-end; business KPIs beside latency."))

fs.append(Q(94, "Multi-region full-stack considerations.",
"Data residency, latency, failover, session affinity, CDN at edge, regional APIs, conflict-free design or strong primary region for writes.",
"Active-active writes everywhere without conflict plan — split brain.",
["Read replicas global vs write primary?", "Edge auth?"],
["Complexity vs latency wins.", "Consistency UX."],
"Start single region + global CDN; expand with clear write story."))

fs.append(Q(95, "Background jobs triggered from UI.",
"API enqueues job, returns `jobId`; UI polls/SSE for status; workers update progress; authorize job ownership; timeouts and cancelation tokens.",
"Long request runs the job inline — gateway timeouts.",
["Progress granularity?", "How cancel safely?"],
["Polling load vs WS complexity.", "User expectations for duration."],
"Exports/renders/video: always async with status API."))

fs.append(Q(96, "RBAC across UI and API.",
"Single source of permissions; API enforces; UI hides/disables for UX only. Permission catalog; role assignments; audit; test matrix for critical actions.",
"Hide button = secure — attackers call API directly.",
["How share permission map with FE?", "Resource-level checks?"],
["Coarse roles vs fine-grained policies.", "Caching permission lookups."],
"Central policy module imported by API; FE gets capability bootstrap."))

fs.append(Q(97, "Email + magic link login full-stack.",
"Rate limit requests; single-use signed tokens with expiry; invalidate on use; consider session fixation; don’t reveal whether email exists (enumeration); fallback MFA.",
"Long-lived links in URLs logged by proxies forever.",
["Enumeration-safe responses?", "Deep link mobile handling?"],
["UX convenience vs email latency/spam filters.", "Token storage."],
"Signed JWT/random token in DB; short TTL; rotate signing keys."))

fs.append(Q(98, "Draft autosave architecture.",
"Local debounce → PATCH draft API with version; conflict detection; offline queue; visibility restore; don’t autosave secrets into logs.",
"Save on every keystroke synchronously — storms and races.",
["CRDT vs versions for collaboration?", "IndexedDB offline?"],
["Complexity of collab vs single-user drafts.", "Battery/network cost."],
"Docs/editors: debounce + version; collab tools may need CRDTs."))

fs.append(Q(99, "Image-heavy social feed design.",
"CDN images with transforms; virtualized feed; progressive loading; API returns cursors + signed URLs; prefetch next page; moderation pipeline; CLS-safe placeholders.",
"Load full-res original for every thumbnail.",
["How personalize ranking?", "Client cache vs CDN?"],
["Quality vs bandwidth.", "Moderation latency vs publish UX."],
"Feed API + image CDN + virtual list is the standard shape."))

fs.append(Q(100, "Admin impersonation safely.",
"Special audit-logged grant; short TTL; clear UI banner; separate cookie/session claims; restrict to support roles; no password reveal; 2P approval for sensitive tenants.",
"Login as user by resetting their password — irreversible harm.",
["How revoke mid-session?", "What to redact in audit?"],
["Support speed vs privacy risk.", "Legal/compliance constraints."],
"Break-glass tooling with mandatory audit trail."))

fs.append(Q(101, "Monorepo CI for FE+BE.",
"Affected-project detection; build/test only changed packages; shared caching; preview deploys per app; contract tests between API and web.",
"Rebuild everything every PR — slow feedback.",
["How test cross-package types?", "Preview env data?"],
["CI minutes cost vs confidence.", "Flaky e2e gating merges."],
"Turborepo/Nx + Playwright smoke on previews."))

fs.append(Q(102, "Graceful degradation strategies.",
"If search down → SQL fallback; if recommendations down → popular list; if WS down → polling; circuit breakers; FE skeletons/errors with retry; never blank the whole app.",
"Full-page error if one widget fails.",
["How detect partial outages?", "SLO for optional features?"],
["Fallback quality vs complexity.", "User messaging honesty."],
"Error boundaries per widget; backend feature fallbacks."))

fs.append(Q(103, "Migration: monolith → services without pausing product.",
"Strangle pattern; extract with antifraud seams; shared DB last; dual-write carefully; contract tests; feature flags; measure latency/error budgets.",
"Big-bang rewrite freeze for 6 months — usually death march.",
["How split data ownership?", "Frontend BFF during migration?"],
["Temporary complexity vs risk.", "Team structure Conway’s law."],
"Extract bounded contexts behind stable APIs first."))

fs.append(Q(104, "CSRF + CORS + cookies in one story.",
"Same-origin BFF avoids CORS for browser. Cookie sessions need CSRF tokens on state-changing requests. Cross-site APIs with cookies need tight CORS + `SameSite=None; Secure` carefully.",
"Disable CSRF because you “have CORS”.",
["When is CSRF irrelevant?", "Double-submit cookie pattern?"],
["Token plumbing vs bearer auth.", "Third-party cookie restrictions."],
"Prefer same-site BFF; CSRF on POSTs; document exceptions."))

fs.append(Q(105, "A/B testing full-stack.",
"Assign experiment at edge/server; sticky assignment; send exposure events; FE renders variant; BE respects same assignment for logic; stats engine; ethics/sample ratio mismatch checks.",
"Randomize on every page load — unsticked experience.",
["How avoid CLS from variants?", "SSR flicker?"],
["Speed of learning vs UX consistency.", "Peeking/statistical rigor."],
"Experiment platform integrated with flags + analytics."))

fs.append(Q(106, "Search-as-you-type system.",
"Debounce FE; autocomplete API with prefix index/trie/ES completion; limit results; cancel in-flight (`AbortController`); cache; analytics on CTR.",
"Query primary DB `LIKE` per keypress without debounce.",
["How rank suggestions?", "Personalization privacy?"],
["Freshness vs index cost.", "Latency budget (~100–200ms)."],
"Dedicated suggest endpoint + CDN caching for popular prefixes."))

fs.append(Q(107, "Multi-tab consistency.",
"BroadcastChannel/localStorage events for logout and cache invalidation; React Query focus refetch; version vectors for edits; avoid duplicate WS connections if possible (shared worker).",
"Ignore multi-tab — users routinely open many tabs.",
["SharedWorker for WS?", "Conflict UX?"],
["Complexity vs correctness.", "Battery from many connections."],
"Logout sync mandatory; document editors need conflict policy."))

fs.append(Q(108, "PDF/report generation feature.",
"Server worker renders (headless/browser or template engine); store artifact; pre-signed download; queue; timeouts; template versioning; authz checks on download.",
"Generate PDF in the browser only — inconsistent fonts/OS and weak auth for data.",
["Headless Chrome in K8s pitfalls?", "How cache identical reports?"],
["Quality vs infra cost.", "Sync vs async UX."],
"Async worker + object storage is the default production shape."))

fs.append(Q(109, "Rate limit UX + API together.",
"API returns 429 + `Retry-After`; FE surfaces friendly message and backs off; distinguish user vs IP limits; don’t infinite-retry.",
"Silent fail on 429 — users think the app is broken.",
["How show remaining quota?", "Burst tokens UX?"],
["Strict limits vs power users.", "Support override processes."],
"Document limits; dashboard for quota; exponential backoff client helper."))

fs.append(Q(110, "Content moderation pipeline.",
"Upload → async classifiers/human queue → states (pending/approved/rejected); FE shows pending; appeals; audit; rate limits; privacy for reviewers.",
"Only blocklist words client-side — trivial bypass.",
["How handle false positives?", "Live streaming moderation?"],
["Automation scale vs human cost.", "Latency to publish."],
"UGC platforms need async moderation + clear state machine."))

fs.append(Q(111, "i18n + locale routing full-stack.",
"Locale in URL or cookie; SSR respects locale; API returns localized content or message keys; currency/timezone separate from language; fallbacks.",
"Translate FE only; API errors remain English-only and dates wrong.",
["How localize emails?", "SEO hreflang?"],
["URL locale vs cookie prefs.", "Bundle size of catalogs."],
"Next locale segments; localized transactional email templates."))

fs.append(Q(112, "Soft launch / dark launch a feature.",
"Ship code behind flag off; dark launch server path with shadow traffic; monitor errors/latency; ramp %; kill switch; then announce.",
"Launch to 100% on Friday without metrics — classic incident.",
["Shadow reads vs dual writes?", "What dashboards required?"],
["Ramp speed vs statistical confidence.", "Support readiness."],
"Flags + canary + runbook before marketing blast."))

fs.append(Q(113, "Handling schema changes with old mobile clients.",
"Additive API changes; version negotiation; compatibility window; feature detection; don’t remove fields until clients obsolete; contract tests against old fixtures.",
"Break mobile by renaming JSON fields in one deploy.",
["How force-upgrade policy?", "BFF adapters per version?"],
["Speed of cleanup vs user upgrade rates.", "Maintenance cost of N versions."],
"Mobile: long compatibility; web: shorter with continuous deploy."))

fs.append(Q(114, "Personalization vs caching.",
"Cache public shells; personalize via edge includes, client fetch, or `Vary` carefully. Fragment caching. Never cache one user’s private HTML as public.",
"CDN cache HTML with user name baked in without vary — leak PII.",
["Edge-side includes?", "Signed cookies at CDN?"],
["Personalization lift vs cache hit rate.", "Complexity of fragment architecture."],
"Cache public; load private widgets client-side or ESI carefully."))

fs.append(Q(115, "Audit logging for sensitive actions.",
"Immutable append-only logs: who/what/when/where/before-after; protect from tampering; retention; FE shows limited history; API enforces.",
"Only `console.log` changes — not queryable or trustworthy.",
["How prevent admin deleting audits?", "PII in audits?"],
["Storage cost vs compliance.", "Synchronous vs async audit write."],
"Billing/permission changes must be audited and alertable."))

fs.append(Q(116, "Full-stack performance budget.",
"Agree budgets: LCP, INP, API p95, payload sizes, query times. CI checks FE; load tests BE; RUM verifies. Optimize highest leverage bottleneck first.",
"Optimize random microbenchmarks without user journeys.",
["How set budgets?", "Regressions in CI?"],
["Perf vs feature velocity.", "Over-optimizing rare paths."],
"Budgets in engineering handbook; fail builds on major regressions."))

fs.append(Q(117, "Data export / portability feature.",
"Async job packages user data; authz; encrypt at rest; expiring download link; notify user; rate limit; audit; exclude secrets/tokens.",
"Sync zip of all data on request thread — timeouts and abuse.",
["GDPR timing requirements?", "How include related tenant data carefully?"],
["Completeness vs safety.", "Support burden."],
"Privacy programs require tested export/delete pipelines."))

fs.append(Q(118, "Webhooks inbound (Stripe/GitHub style) in your app.",
"Verify signatures; idempotent processing; quick 200 then async work; store raw event; replay tooling; alert on handler failures.",
"Do heavy DB work before responding — provider retries amplify load.",
["Ordering of events?", "Clock skew tolerance?"],
["Sync simplicity vs resilience.", "Poison event handling."],
"Inbox table + worker is the reliable pattern."))

fs.append(Q(119, "Choosing SSR vs SPA for a product surface.",
"SSR/RSC for SEO, fast first paint, secure data gating. SPA for highly interactive authenticated tools. Often hybrid: marketing SSR, app client-heavy.",
"One architecture dogma for every page.",
["How decide per route?", "Hydration cost?"],
["Complexity of hybrid vs consistency.", "SEO needs vs eng cost."],
"Route-level choices in Next App Router are normal and healthy."))

fs.append(Q(120, "How do you lead a senior full-stack design interview answer?",
"Clarify requirements/constraints → API + data model → FE architecture → consistency/auth → failure modes → observability → trade-offs → iterate with interviewer. Quantify when possible (QPS, size, p99).",
"Jump into tech buzzwords without requirements or failure modes.",
["What numbers do you ask for?", "How deep to go on FE vs BE given role?"],
["Breadth vs depth under timebox.", "Perfect design vs shippable MVP."],
"Practice aloud with timers; always mention risks and rollbacks."))

header = """# Senior Q&A — Full-Stack (81–120)

Cross-cutting system answers: auth, caching, realtime, migrations, and product features spanning FE+BE.

"""
(OUT / "03-fullstack.md").write_text(header + "\n---\n\n".join(fs))
(OUT / "index.md").write_text("""# Senior Interview Q&A

120 questions for mid → senior full-stack interviews. Each item has:

1. **Expected answer** — what a strong hire says
2. **Common wrong answer** — trap to avoid
3. **Follow-ups** — interviewer probes
4. **Trade-offs** — senior signal
5. **Production relevance** — why it matters on the job

## Tracks

| Range | Focus | File |
| --- | --- | --- |
| Q1–40 | Frontend (JS/React/Next/a11y/perf/security) | [01-frontend](/senior-qa/01-frontend) |
| Q41–80 | Backend (API/data/queues/ops/security) | [02-backend](/senior-qa/02-backend) |
| Q81–120 | Full-stack (auth, BFF, realtime, migrations) | [03-fullstack](/senior-qa/03-fullstack) |

```mermaid
flowchart LR
  FE[Frontend 1–40] --> FS[Full-stack 81–120]
  BE[Backend 41–80] --> FS
```

## How to drill

1. Draw 10 random numbers; answer out loud in ≤2 minutes.
2. Only then read the expected answer and follow-ups.
3. Re-answer the follow-ups.

> [!TIP]
> Seniors narrate **trade-offs and failure modes**. Juniors list tools.
""")
print("fullstack", len(fs))
