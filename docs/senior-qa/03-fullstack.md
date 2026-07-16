# Senior Q&A — Full-Stack (81–120)

Cross-cutting system answers: auth, caching, realtime, migrations, and product features spanning FE+BE.

## Q81. End-to-end auth for a Next.js + API app.

**Expected answer**

Prefer BFF: browser hits Next same-origin; server sets HttpOnly Secure SameSite session cookie; API validates session/JWT server-side; CSRF for cookie mutations; refresh/rotation; logout clears server session.

**Common wrong answer**

SPA stores long-lived JWT in `localStorage` and calls APIs directly — XSS = account theft.

**Follow-ups**

- How protect Server Actions?
- Mobile client differences?

**Trade-offs**

- Cookie CSRF complexity vs bearer simplicity.
- SSR session fetch vs edge middleware checks.

**Production relevance**

NextAuth/Auth.js or custom BFF sessions; never trust client role flags.

---

## Q82. Design a full-stack feature: “shareable filtered table”.

**Expected answer**

Filters/sort/page in URL; server or client fetch with React Query keyed by URL; API cursor pagination + indexes; columns virtualized; export async; authz on API.

**Common wrong answer**

Keep filters only in React state — not shareable/bookmarkable.

**Follow-ups**

- SSR first paint with filters?
- How avoid double fetch in App Router?

**Trade-offs**

- URL complexity vs shareability.
- Server tables vs client interactivity.

**Production relevance**

Admin consoles and search results pages use this pattern constantly.

---

## Q83. Optimistic UI across client cache and DB.

**Expected answer**

Client patches React Query cache; API uses idempotency key; server returns canonical entity; client reconciles; rollback on failure; conflict policy (LWW/version).

**Common wrong answer**

Optimistic update without server version checks — silent overwrites.

**Follow-ups**

- How handle two tabs?
- ETag/If-Match?

**Trade-offs**

- Speed vs correctness.
- Conflict UX complexity.

**Production relevance**

Collaborative settings and carts need explicit conflict rules.

---

## Q84. File upload full-stack flow.

**Expected answer**

Client requests pre-signed URL from API (authz); uploads direct to S3; notifies API with object key; virus scan/async processing; UI polls or receives WS/SSE status.

**Common wrong answer**

Upload multipart through Next API to disk on serverless — size/time limits and cost.

**Follow-ups**

- How secure the complete callback?
- Progress UX?

**Trade-offs**

- Direct upload vs proxy control.
- Multipart complexity.

**Production relevance**

Avatars/docs: pre-sign + async pipeline + CDN read.

---

## Q85. Realtime chat: FE + BE outline.

**Expected answer**

WS/SSE gateway; messages persisted; fan-out via pub/sub; client virtualized list; optimistic send; delivery/read receipts; auth on connect; backpressure; rate limits; media via object storage.

**Common wrong answer**

Store messages only in memory on one node — lost on deploy.

**Follow-ups**

- How scale WS horizontally?
- Ordering guarantees?

**Trade-offs**

- WS infra cost vs polling latency.
- Exactly-once vs idempotent message ids.

**Production relevance**

Chat services: sticky or pub/sub broadcaster + durable store.

---

## Q86. tRPC vs REST vs GraphQL for your stack.

**Expected answer**

tRPC: great TS monorepo end-to-end types. REST: universal, cacheable, public ecosystems. GraphQL: flexible client shapes, heavier cache/auth complexity. Choose based on clients and team.

**Common wrong answer**

GraphQL because it’s modern — ignoring ops and authz complexity.

**Follow-ups**

- How expose public third-party API if internal is tRPC?
- Versioning?

**Trade-offs**

- Type safety vs ecosystem constraints.
- BFF proliferation.

**Production relevance**

Internal product: tRPC/REST; public partners: versioned REST.

---

## Q87. End-to-end type safety strategies.

**Expected answer**

Shared zod schemas or OpenAPI → types; validate at boundaries; never trust network types; generate clients; branded IDs; avoid `as` casts on API results.

**Common wrong answer**

Share only TypeScript interfaces without runtime validation — lies at runtime.

**Follow-ups**

- zod vs OpenAPI first?
- How version schemas?

**Trade-offs**

- Strictness vs shipping speed.
- Generated code churn.

**Production relevance**

Monorepo shared contracts package used by web and API.

---

## Q88. Caching across CDN, HTTP, Redis, and React Query.

**Expected answer**

Layers: browser/CDN for public; Redis for shared server reads; React Query for per-client session UX. Define TTLs and invalidation ownership per layer; don’t double-cache secrets.

**Common wrong answer**

Cache personalized HTML at CDN without Vary/cookie strategy — data leaks.

**Follow-ups**

- How invalidate CDN on publish?
- Cache key design?

**Trade-offs**

- Hit rate vs personalization.
- Stale layers fighting each other.

**Production relevance**

Public marketing CDN; user dashboards Redis+RQ with careful keys.

---

## Q89. SSR data fetching auth pitfalls.

**Expected answer**

Forward cookies carefully; don’t cache authenticated RSC/fetch globally; use `cache: 'no-store'` or per-user keys; never log secrets; consistent auth between middleware and server components.

**Common wrong answer**

Cache `fetch` of user profile across users — cross-user data leak.

**Follow-ups**

- How pass auth to nested fetches?
- Edge middleware limits?

**Trade-offs**

- CDN caching vs auth correctness.
- Duplicated auth checks.

**Production relevance**

Review every cached fetch for user-specific data.

---

## Q90. Search feature full-stack.

**Expected answer**

Indexer async from source DB; query API with relevance + filters; debounce FE input; highlight; empty states; rate limit; fallback to SQL if search cluster down.

**Common wrong answer**

Live `LIKE %q%` on primary for every keystroke at scale — DB melt.

**Follow-ups**

- How keep index fresh?
- Typo tolerance?

**Trade-offs**

- Search quality vs infra cost.
- Eventual consistency of results.

**Production relevance**

Postgres FTS first; ES when facets/relevance demand it.

---

## Q91. Payments full-stack (Stripe-like).

**Expected answer**

Checkout session or PaymentIntent on server; never handle raw cards if possible (hosted fields); webhooks as source of truth; idempotent webhook handlers; reconcile UI via status API.

**Common wrong answer**

Trust client `paymentSuccess=true` redirect alone — forgeable.

**Follow-ups**

- Webhook signature verify?
- How handle delayed async payment methods?

**Trade-offs**

- PCI scope reduction vs custom UX.
- Idempotency storage.

**Production relevance**

Stripe Checkout/Elements + webhook outbox pattern.

---

## Q92. Feature flags across FE and BE.

**Expected answer**

Same flag keys evaluated in both tiers; backend enforces for security; frontend for UX. Bootstrap without flicker; audit; clean up.

**Common wrong answer**

FE-only flags for authz — trivially bypassed.

**Follow-ups**

- Percentage rollout consistency?
- Kill switch during incident?

**Trade-offs**

- Consistency lag between tiers.
- Flag debt.

**Production relevance**

Security-sensitive flags must be server-enforced.

---

## Q93. Observability across FE and BE.

**Expected answer**

Correlate browser RUM trace/span ids with backend traces; shared `request_id`; FE error reporting with release; BE metrics/logs/traces; dashboards for journey success (checkout).

**Common wrong answer**

Only backend APM — miss JS errors killing conversion.

**Follow-ups**

- How sample without losing SEVs?
- PII scrubbing in FE logs?

**Trade-offs**

- Cardinality/cost vs visibility.
- Privacy constraints.

**Production relevance**

Sentry + OpenTelemetry end-to-end; business KPIs beside latency.

---

## Q94. Multi-region full-stack considerations.

**Expected answer**

Data residency, latency, failover, session affinity, CDN at edge, regional APIs, conflict-free design or strong primary region for writes.

**Common wrong answer**

Active-active writes everywhere without conflict plan — split brain.

**Follow-ups**

- Read replicas global vs write primary?
- Edge auth?

**Trade-offs**

- Complexity vs latency wins.
- Consistency UX.

**Production relevance**

Start single region + global CDN; expand with clear write story.

---

## Q95. Background jobs triggered from UI.

**Expected answer**

API enqueues job, returns `jobId`; UI polls/SSE for status; workers update progress; authorize job ownership; timeouts and cancelation tokens.

**Common wrong answer**

Long request runs the job inline — gateway timeouts.

**Follow-ups**

- Progress granularity?
- How cancel safely?

**Trade-offs**

- Polling load vs WS complexity.
- User expectations for duration.

**Production relevance**

Exports/renders/video: always async with status API.

---

## Q96. RBAC across UI and API.

**Expected answer**

Single source of permissions; API enforces; UI hides/disables for UX only. Permission catalog; role assignments; audit; test matrix for critical actions.

**Common wrong answer**

Hide button = secure — attackers call API directly.

**Follow-ups**

- How share permission map with FE?
- Resource-level checks?

**Trade-offs**

- Coarse roles vs fine-grained policies.
- Caching permission lookups.

**Production relevance**

Central policy module imported by API; FE gets capability bootstrap.

---

## Q97. Email + magic link login full-stack.

**Expected answer**

Rate limit requests; single-use signed tokens with expiry; invalidate on use; consider session fixation; don’t reveal whether email exists (enumeration); fallback MFA.

**Common wrong answer**

Long-lived links in URLs logged by proxies forever.

**Follow-ups**

- Enumeration-safe responses?
- Deep link mobile handling?

**Trade-offs**

- UX convenience vs email latency/spam filters.
- Token storage.

**Production relevance**

Signed JWT/random token in DB; short TTL; rotate signing keys.

---

## Q98. Draft autosave architecture.

**Expected answer**

Local debounce → PATCH draft API with version; conflict detection; offline queue; visibility restore; don’t autosave secrets into logs.

**Common wrong answer**

Save on every keystroke synchronously — storms and races.

**Follow-ups**

- CRDT vs versions for collaboration?
- IndexedDB offline?

**Trade-offs**

- Complexity of collab vs single-user drafts.
- Battery/network cost.

**Production relevance**

Docs/editors: debounce + version; collab tools may need CRDTs.

---

## Q99. Image-heavy social feed design.

**Expected answer**

CDN images with transforms; virtualized feed; progressive loading; API returns cursors + signed URLs; prefetch next page; moderation pipeline; CLS-safe placeholders.

**Common wrong answer**

Load full-res original for every thumbnail.

**Follow-ups**

- How personalize ranking?
- Client cache vs CDN?

**Trade-offs**

- Quality vs bandwidth.
- Moderation latency vs publish UX.

**Production relevance**

Feed API + image CDN + virtual list is the standard shape.

---

## Q100. Admin impersonation safely.

**Expected answer**

Special audit-logged grant; short TTL; clear UI banner; separate cookie/session claims; restrict to support roles; no password reveal; 2P approval for sensitive tenants.

**Common wrong answer**

Login as user by resetting their password — irreversible harm.

**Follow-ups**

- How revoke mid-session?
- What to redact in audit?

**Trade-offs**

- Support speed vs privacy risk.
- Legal/compliance constraints.

**Production relevance**

Break-glass tooling with mandatory audit trail.

---

## Q101. Monorepo CI for FE+BE.

**Expected answer**

Affected-project detection; build/test only changed packages; shared caching; preview deploys per app; contract tests between API and web.

**Common wrong answer**

Rebuild everything every PR — slow feedback.

**Follow-ups**

- How test cross-package types?
- Preview env data?

**Trade-offs**

- CI minutes cost vs confidence.
- Flaky e2e gating merges.

**Production relevance**

Turborepo/Nx + Playwright smoke on previews.

---

## Q102. Graceful degradation strategies.

**Expected answer**

If search down → SQL fallback; if recommendations down → popular list; if WS down → polling; circuit breakers; FE skeletons/errors with retry; never blank the whole app.

**Common wrong answer**

Full-page error if one widget fails.

**Follow-ups**

- How detect partial outages?
- SLO for optional features?

**Trade-offs**

- Fallback quality vs complexity.
- User messaging honesty.

**Production relevance**

Error boundaries per widget; backend feature fallbacks.

---

## Q103. Migration: monolith → services without pausing product.

**Expected answer**

Strangle pattern; extract with antifraud seams; shared DB last; dual-write carefully; contract tests; feature flags; measure latency/error budgets.

**Common wrong answer**

Big-bang rewrite freeze for 6 months — usually death march.

**Follow-ups**

- How split data ownership?
- Frontend BFF during migration?

**Trade-offs**

- Temporary complexity vs risk.
- Team structure Conway’s law.

**Production relevance**

Extract bounded contexts behind stable APIs first.

---

## Q104. CSRF + CORS + cookies in one story.

**Expected answer**

Same-origin BFF avoids CORS for browser. Cookie sessions need CSRF tokens on state-changing requests. Cross-site APIs with cookies need tight CORS + `SameSite=None; Secure` carefully.

**Common wrong answer**

Disable CSRF because you “have CORS”.

**Follow-ups**

- When is CSRF irrelevant?
- Double-submit cookie pattern?

**Trade-offs**

- Token plumbing vs bearer auth.
- Third-party cookie restrictions.

**Production relevance**

Prefer same-site BFF; CSRF on POSTs; document exceptions.

---

## Q105. A/B testing full-stack.

**Expected answer**

Assign experiment at edge/server; sticky assignment; send exposure events; FE renders variant; BE respects same assignment for logic; stats engine; ethics/sample ratio mismatch checks.

**Common wrong answer**

Randomize on every page load — unsticked experience.

**Follow-ups**

- How avoid CLS from variants?
- SSR flicker?

**Trade-offs**

- Speed of learning vs UX consistency.
- Peeking/statistical rigor.

**Production relevance**

Experiment platform integrated with flags + analytics.

---

## Q106. Search-as-you-type system.

**Expected answer**

Debounce FE; autocomplete API with prefix index/trie/ES completion; limit results; cancel in-flight (`AbortController`); cache; analytics on CTR.

**Common wrong answer**

Query primary DB `LIKE` per keypress without debounce.

**Follow-ups**

- How rank suggestions?
- Personalization privacy?

**Trade-offs**

- Freshness vs index cost.
- Latency budget (~100–200ms).

**Production relevance**

Dedicated suggest endpoint + CDN caching for popular prefixes.

---

## Q107. Multi-tab consistency.

**Expected answer**

BroadcastChannel/localStorage events for logout and cache invalidation; React Query focus refetch; version vectors for edits; avoid duplicate WS connections if possible (shared worker).

**Common wrong answer**

Ignore multi-tab — users routinely open many tabs.

**Follow-ups**

- SharedWorker for WS?
- Conflict UX?

**Trade-offs**

- Complexity vs correctness.
- Battery from many connections.

**Production relevance**

Logout sync mandatory; document editors need conflict policy.

---

## Q108. PDF/report generation feature.

**Expected answer**

Server worker renders (headless/browser or template engine); store artifact; pre-signed download; queue; timeouts; template versioning; authz checks on download.

**Common wrong answer**

Generate PDF in the browser only — inconsistent fonts/OS and weak auth for data.

**Follow-ups**

- Headless Chrome in K8s pitfalls?
- How cache identical reports?

**Trade-offs**

- Quality vs infra cost.
- Sync vs async UX.

**Production relevance**

Async worker + object storage is the default production shape.

---

## Q109. Rate limit UX + API together.

**Expected answer**

API returns 429 + `Retry-After`; FE surfaces friendly message and backs off; distinguish user vs IP limits; don’t infinite-retry.

**Common wrong answer**

Silent fail on 429 — users think the app is broken.

**Follow-ups**

- How show remaining quota?
- Burst tokens UX?

**Trade-offs**

- Strict limits vs power users.
- Support override processes.

**Production relevance**

Document limits; dashboard for quota; exponential backoff client helper.

---

## Q110. Content moderation pipeline.

**Expected answer**

Upload → async classifiers/human queue → states (pending/approved/rejected); FE shows pending; appeals; audit; rate limits; privacy for reviewers.

**Common wrong answer**

Only blocklist words client-side — trivial bypass.

**Follow-ups**

- How handle false positives?
- Live streaming moderation?

**Trade-offs**

- Automation scale vs human cost.
- Latency to publish.

**Production relevance**

UGC platforms need async moderation + clear state machine.

---

## Q111. i18n + locale routing full-stack.

**Expected answer**

Locale in URL or cookie; SSR respects locale; API returns localized content or message keys; currency/timezone separate from language; fallbacks.

**Common wrong answer**

Translate FE only; API errors remain English-only and dates wrong.

**Follow-ups**

- How localize emails?
- SEO hreflang?

**Trade-offs**

- URL locale vs cookie prefs.
- Bundle size of catalogs.

**Production relevance**

Next locale segments; localized transactional email templates.

---

## Q112. Soft launch / dark launch a feature.

**Expected answer**

Ship code behind flag off; dark launch server path with shadow traffic; monitor errors/latency; ramp %; kill switch; then announce.

**Common wrong answer**

Launch to 100% on Friday without metrics — classic incident.

**Follow-ups**

- Shadow reads vs dual writes?
- What dashboards required?

**Trade-offs**

- Ramp speed vs statistical confidence.
- Support readiness.

**Production relevance**

Flags + canary + runbook before marketing blast.

---

## Q113. Handling schema changes with old mobile clients.

**Expected answer**

Additive API changes; version negotiation; compatibility window; feature detection; don’t remove fields until clients obsolete; contract tests against old fixtures.

**Common wrong answer**

Break mobile by renaming JSON fields in one deploy.

**Follow-ups**

- How force-upgrade policy?
- BFF adapters per version?

**Trade-offs**

- Speed of cleanup vs user upgrade rates.
- Maintenance cost of N versions.

**Production relevance**

Mobile: long compatibility; web: shorter with continuous deploy.

---

## Q114. Personalization vs caching.

**Expected answer**

Cache public shells; personalize via edge includes, client fetch, or `Vary` carefully. Fragment caching. Never cache one user’s private HTML as public.

**Common wrong answer**

CDN cache HTML with user name baked in without vary — leak PII.

**Follow-ups**

- Edge-side includes?
- Signed cookies at CDN?

**Trade-offs**

- Personalization lift vs cache hit rate.
- Complexity of fragment architecture.

**Production relevance**

Cache public; load private widgets client-side or ESI carefully.

---

## Q115. Audit logging for sensitive actions.

**Expected answer**

Immutable append-only logs: who/what/when/where/before-after; protect from tampering; retention; FE shows limited history; API enforces.

**Common wrong answer**

Only `console.log` changes — not queryable or trustworthy.

**Follow-ups**

- How prevent admin deleting audits?
- PII in audits?

**Trade-offs**

- Storage cost vs compliance.
- Synchronous vs async audit write.

**Production relevance**

Billing/permission changes must be audited and alertable.

---

## Q116. Full-stack performance budget.

**Expected answer**

Agree budgets: LCP, INP, API p95, payload sizes, query times. CI checks FE; load tests BE; RUM verifies. Optimize highest leverage bottleneck first.

**Common wrong answer**

Optimize random microbenchmarks without user journeys.

**Follow-ups**

- How set budgets?
- Regressions in CI?

**Trade-offs**

- Perf vs feature velocity.
- Over-optimizing rare paths.

**Production relevance**

Budgets in engineering handbook; fail builds on major regressions.

---

## Q117. Data export / portability feature.

**Expected answer**

Async job packages user data; authz; encrypt at rest; expiring download link; notify user; rate limit; audit; exclude secrets/tokens.

**Common wrong answer**

Sync zip of all data on request thread — timeouts and abuse.

**Follow-ups**

- GDPR timing requirements?
- How include related tenant data carefully?

**Trade-offs**

- Completeness vs safety.
- Support burden.

**Production relevance**

Privacy programs require tested export/delete pipelines.

---

## Q118. Webhooks inbound (Stripe/GitHub style) in your app.

**Expected answer**

Verify signatures; idempotent processing; quick 200 then async work; store raw event; replay tooling; alert on handler failures.

**Common wrong answer**

Do heavy DB work before responding — provider retries amplify load.

**Follow-ups**

- Ordering of events?
- Clock skew tolerance?

**Trade-offs**

- Sync simplicity vs resilience.
- Poison event handling.

**Production relevance**

Inbox table + worker is the reliable pattern.

---

## Q119. Choosing SSR vs SPA for a product surface.

**Expected answer**

SSR/RSC for SEO, fast first paint, secure data gating. SPA for highly interactive authenticated tools. Often hybrid: marketing SSR, app client-heavy.

**Common wrong answer**

One architecture dogma for every page.

**Follow-ups**

- How decide per route?
- Hydration cost?

**Trade-offs**

- Complexity of hybrid vs consistency.
- SEO needs vs eng cost.

**Production relevance**

Route-level choices in Next App Router are normal and healthy.

---

## Q120. How do you lead a senior full-stack design interview answer?

**Expected answer**

Clarify requirements/constraints → API + data model → FE architecture → consistency/auth → failure modes → observability → trade-offs → iterate with interviewer. Quantify when possible (QPS, size, p99).

**Common wrong answer**

Jump into tech buzzwords without requirements or failure modes.

**Follow-ups**

- What numbers do you ask for?
- How deep to go on FE vs BE given role?

**Trade-offs**

- Breadth vs depth under timebox.
- Perfect design vs shippable MVP.

**Production relevance**

Practice aloud with timers; always mention risks and rollbacks.
