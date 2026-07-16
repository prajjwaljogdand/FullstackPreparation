# Senior Q&A — Backend (41–80)

API design, data, reliability, security, and operations. Answer with trade-offs, not slogans.

## Q41. Design a REST API for a multi-tenant SaaS resource.

**Expected answer**

Resource-oriented URLs, tenant isolation in authz (not just URL), pagination, filtering, idempotent writes (`Idempotency-Key`), problem+json errors, versioning strategy, rate limits per tenant.

**Common wrong answer**

Put `tenantId` only in the body and trust the client — IDOR waiting to happen.

**Follow-ups**

- Cursor vs offset pagination?
- How version without `/v2` forever?

**Trade-offs**

- Strict REST vs pragmatic RPC endpoints.
- Global vs per-tenant rate limits.

**Production relevance**

Enforce tenant from auth context on every query; audit access.

---

## Q42. SQL vs NoSQL: how do you choose?

**Expected answer**

SQL for relational integrity, complex queries, transactions. NoSQL (document/kv/wide-column) for flexible schemas, massive scale patterns, simple access by key. Many systems are polyglot.

**Common wrong answer**

“NoSQL is always more scalable” — depends on access patterns and ops maturity.

**Follow-ups**

- When NewSQL/distributed SQL?
- How migrate later?

**Trade-offs**

- Flexible schema vs long-term queryability.
- Ops expertise on the team.

**Production relevance**

Orders/payments → SQL; session/cache → Redis; activity feed often hybrid.

---

## Q43. Explain indexes and when they hurt.

**Expected answer**

B-tree indexes speed lookups/ranges/sorts matching left-prefix. Covering indexes avoid table lookups. They slow writes, use disk, and wrong ones confuse the planner. Measure with `EXPLAIN`.

**Common wrong answer**

Index every column — write amplification and bloat.

**Follow-ups**

- Composite index column order?
- Partial/filtered indexes?

**Trade-offs**

- Read latency vs write throughput.
- Index maintenance during migrations.

**Production relevance**

Index hot filters/FKs; drop unused via stats; review slow query logs.

---

## Q44. Transactions: isolation levels and anomalies.

**Expected answer**

Read uncommitted/committed, repeatable read, serializable. Anomalies: dirty/non-repeatable/phantom reads. Choose the weakest level that preserves correctness for the use case.

**Common wrong answer**

“Serializable always” without discussing latency/abort rates.

**Follow-ups**

- Optimistic vs pessimistic concurrency?
- Idempotent retries on abort?

**Trade-offs**

- Strong isolation vs throughput.
- App-level invariants vs DB constraints.

**Production relevance**

Payments: stronger isolation + idempotency keys; feeds: often weaker.

---

## Q45. ORM vs query builder vs raw SQL.

**Expected answer**

ORM: speed for CRUD, relations, migrations. Query builder: composable SQL with less magic. Raw: hot paths, complex analytics, precise plans. Mix deliberately.

**Common wrong answer**

ORM for everything including reporting — N+1 and opaque queries.

**Follow-ups**

- How prevent N+1?
- Migration strategies?

**Trade-offs**

- DX vs control.
- Vendor lock-in to ORM features.

**Production relevance**

CRUD via ORM; dashboards via SQL; always log slow queries.

---

## Q46. Caching with Redis: patterns and pitfalls.

**Expected answer**

Cache-aside, read-through, write-through, write-behind. Key design, TTLs, stampede protection (locking/singleflight), invalidation on writes, memory eviction policies.

**Common wrong answer**

Cache forever without invalidation — stale money/permissions bugs.

**Follow-ups**

- Thundering herd fixes?
- Cache nulls?

**Trade-offs**

- Freshness vs hit rate.
- Redis as primary store anti-pattern.

**Production relevance**

Cache public reads; never trust cache alone for authz decisions.

---

## Q47. Idempotency for payment/order APIs.

**Expected answer**

Client sends `Idempotency-Key`; server persists key→response; retries return same result. Deduplicate side effects (charges, emails) with unique constraints and outbox.

**Common wrong answer**

“Just retry POST” without keys — double charge.

**Follow-ups**

- Where store keys?
- TTL for idempotency records?

**Trade-offs**

- Storage cost vs safety.
- Exactly-once vs at-least-once + idempotent handlers.

**Production relevance**

Mandatory for billing, payouts, provisioning.

---

## Q48. Rate limiting algorithms.

**Expected answer**

Fixed window, sliding window, token bucket, leaky bucket. Enforce at edge/API gateway and app. Keys: IP, user, API key, tenant. Return `Retry-After`.

**Common wrong answer**

Only rate limit by IP — shared NATs punish many users.

**Follow-ups**

- Distributed rate limits with Redis?
- How handle authenticated bursts?

**Trade-offs**

- Fairness vs abuse protection.
- False positives on mobile carriers.

**Production relevance**

Layer CDN + Redis token bucket per API key/tenant.

---

## Q49. Authentication vs authorization.

**Expected answer**

Authn: who are you (session/JWT/OIDC). Authz: what can you do (RBAC/ABAC/ReBAC). Never encode authz only in the frontend. Prefer deny-by-default.

**Common wrong answer**

Hide admin buttons and call that security.

**Follow-ups**

- RBAC vs ABAC?
- JWT claims for roles — risks?

**Trade-offs**

- Central policy service vs local checks.
- Token size vs lookup latency.

**Production relevance**

Enforce authz in API/DB policies; audit sensitive actions.

---

## Q50. JWT access vs refresh tokens.

**Expected answer**

Short-lived access tokens; longer refresh with rotation and reuse detection. Store refresh securely (HttpOnly cookie). Revocation via denylist/version or short TTL + rotation.

**Common wrong answer**

Week-long JWT in localStorage with no rotation.

**Follow-ups**

- How detect refresh reuse?
- Opaque vs self-contained tokens?

**Trade-offs**

- Stateless verification vs revocation difficulty.
- Cookie CSRF vs bearer XSS surface.

**Production relevance**

Access 5–15m; rotating refresh; revoke on logout/password change.

---

## Q51. Password storage and login hardening.

**Expected answer**

Hash with Argon2id/bcrypt/scrypt + unique salt; never reversible encryption for passwords. Rate limit, lockouts/backoff, MFA, breach detection, secure reset flows.

**Common wrong answer**

SHA-256 password hashing — too fast, no work factor.

**Follow-ups**

- Pepper vs salt?
- Passkeys/WebAuthn benefits?

**Trade-offs**

- UX friction of MFA vs account takeover risk.
- Legacy hash migration.

**Production relevance**

Argon2id params tuned to CPU; force reset on suspected breach.

---

## Q52. Design a job queue system.

**Expected answer**

Producers enqueue; workers pull with visibility timeout; retries with backoff; DLQ; idempotent handlers; metrics on lag/age; poison message handling.

**Common wrong answer**

Process async work in the web request thread forever.

**Follow-ups**

- At-least-once delivery implications?
- Priority queues?

**Trade-offs**

- SQS/Rabbit/Kafka suitability.
- Ordering vs throughput.

**Production relevance**

Emails, webhooks, image processing — SQS/BullMQ with DLQ alarms.

---

## Q53. Kafka vs RabbitMQ vs SQS (interview framing).

**Expected answer**

Kafka: durable log, high throughput, consumer groups, replay. Rabbit: flexible routing, classic work queues. SQS: managed, simple, at-least-once, limited ordering (FIFO).

**Common wrong answer**

“Kafka is a message queue” only — it’s a distributed log with different semantics.

**Follow-ups**

- When need exactly-once?
- Compaction use cases?

**Trade-offs**

- Ops complexity vs capability.
- Fan-out patterns.

**Production relevance**

Event streaming/analytics → Kafka; task queues → SQS/Rabbit.

---

## Q54. Database migrations in production.

**Expected answer**

Expand/contract: additive changes first, dual-write/read if needed, backfill, then remove old. Avoid long locks; online schema tools; expand app compatibility window.

**Common wrong answer**

Rename column in one deploy — breaks old app instances.

**Follow-ups**

- How backfill large tables?
- Zero-downtime expand/contract examples?

**Trade-offs**

- Migration speed vs lock risk.
- Feature flags for dual paths.

**Production relevance**

Strong migration review culture; runbooks for rollback.

---

## Q55. Observability: metrics, logs, traces.

**Expected answer**

Metrics for SLOs/alerts; structured logs for forensics; traces for request fan-out. Correlate with `trace_id`. RED/USE methods. Alert on symptoms (latency/error) not only causes.

**Common wrong answer**

Log everything at INFO and page on every error — noise.

**Follow-ups**

- SLI vs SLO vs SLA?
- Cardinality pitfalls in metrics?

**Trade-offs**

- Retention cost vs debuggability.
- Sampling traces.

**Production relevance**

p95/p99 latency + error rate burn alerts; exemplars to traces.

---

## Q56. Circuit breaker, bulkhead, retry.

**Expected answer**

Retries with jittered backoff for transient faults; circuit breaker stops calling unhealthy deps; bulkheads isolate pools. Don’t retry non-idempotent requests without keys.

**Common wrong answer**

Blind infinite retries — amplify outages.

**Follow-ups**

- When fail-fast vs queue?
- Hedged requests?

**Trade-offs**

- Availability vs duplicate side effects.
- Timeouts too aggressive vs too long.

**Production relevance**

Outbound HTTP clients: timeouts + breaker + metrics.

---

## Q57. Horizontal scaling Node.js APIs.

**Expected answer**

Cluster/PM2 or multiple containers behind LB; stickiness only if required; externalize sessions; share-nothing; watch event-loop lag; separate CPU-heavy work to workers.

**Common wrong answer**

Bigger single VM forever — vertical scaling ceiling.

**Follow-ups**

- Sticky sessions problems?
- How measure event-loop delay?

**Trade-offs**

- Process count vs memory.
- Stateful websocket routing.

**Production relevance**

K8s HPA on CPU/RPS/lag; Redis sessions; workers for CPU.

---

## Q58. File uploads at scale.

**Expected answer**

Direct-to-object-storage with pre-signed URLs; virus scan; size/type limits; multipart for large files; async processing pipeline; CDN for download.

**Common wrong answer**

Stream all uploads through app servers to disk — bottleneck and risk.

**Follow-ups**

- How secure pre-signed URLs?
- Image transformation pipeline?

**Trade-offs**

- App proxy control vs S3 direct cost/complexity.
- Retention/GDPR deletes.

**Production relevance**

S3/GCS pre-sign; Lambda/workers for thumbnails; lifecycle policies.

---

## Q59. Search: Postgres vs Elasticsearch.

**Expected answer**

Postgres full-text / trigram for moderate needs and simpler ops. ES/OpenSearch for relevance tuning, facets, high-volume text. Keep source of truth in primary DB; async index.

**Common wrong answer**

ES as system of record — durability/consistency pain.

**Follow-ups**

- How handle indexing lag?
- Synonyms/ranking?

**Trade-offs**

- Ops complexity vs search quality.
- Dual-write consistency.

**Production relevance**

Start with Postgres; graduate to ES when relevance/scale demands.

---

## Q60. Multi-tenant data isolation strategies.

**Expected answer**

Shared schema + `tenant_id` (RLS), schema-per-tenant, DB-per-tenant. Shared is cheapest; separate is strongest isolation. Always filter by auth tenant — never trust client.

**Common wrong answer**

Only separate by subdomain — still shared tables without filters.

**Follow-ups**

- Postgres RLS patterns?
- Noisy neighbor mitigations?

**Trade-offs**

- Cost vs isolation.
- Migration/customization per tenant.

**Production relevance**

Most SaaS: shared + RLS; enterprise: dedicated DB option.

---

## Q61. API gateway responsibilities.

**Expected answer**

TLS termination, authn, rate limit, routing, request validation, canary, WAF. Keep business logic in services. Avoid god-gateway that owns domain rules.

**Common wrong answer**

Put all business logic in the gateway — unmaintainable.

**Follow-ups**

- Gateway vs service mesh?
- Auth at edge vs service?

**Trade-offs**

- Central control vs service autonomy.
- Latency hop cost.

**Production relevance**

Kong/Cloud API Gateway for cross-cutting concerns only.

---

## Q62. Event-driven architecture pitfalls.

**Expected answer**

Dual writes without outbox, unordered consumers, poison messages, schema evolution breaks, debugging complexity, eventual consistency surprises for product.

**Common wrong answer**

“Events mean we don’t need transactions” — you still need consistency patterns.

**Follow-ups**

- Transactional outbox?
- Consumer idempotency?

**Trade-offs**

- Coupling via event schemas.
- Sync UX vs async reality.

**Production relevance**

Outbox + idempotent consumers + schema registry.

---

## Q63. Design a notification system.

**Expected answer**

Ingest events → preference service → fan-out to channels (email/push/SMS/in-app) via queues; templates; quiet hours; dedupe; delivery receipts; rate limits; user preference center.

**Common wrong answer**

Send email synchronously in the request — timeouts and spikes.

**Follow-ups**

- How avoid spammy duplicates?
- Priority channels?

**Trade-offs**

- Fan-out cost vs personalization.
- Provider redundancy.

**Production relevance**

Queue per channel; templates versioned; metrics on send/fail.

---

## Q64. Secrets management.

**Expected answer**

No secrets in git or images. Use KMS/Secrets Manager/Vault; short-lived credentials; rotate; least privilege IAM; inject at runtime; audit access.

**Common wrong answer**

`.env` committed “just for staging” — still a leak vector.

**Follow-ups**

- How rotate DB passwords with zero downtime?
- Workload identity?

**Trade-offs**

- Central vault vs cloud-native secrets.
- Developer DX.

**Production relevance**

OIDC to cloud; rotate automatically; scan repos for secrets.

---

## Q65. Blue/green vs canary vs rolling deploys.

**Expected answer**

Rolling: gradually replace. Blue/green: switch traffic between two envs. Canary: small % traffic then promote. Need health checks, metrics, and fast rollback.

**Common wrong answer**

Canary without metrics — you’re just slow-rolling failures.

**Follow-ups**

- DB migrations with canaries?
- Feature flags vs deploy strategies?

**Trade-offs**

- Infra cost of blue/green.
- Canary analysis complexity.

**Production relevance**

K8s rolling + canary analysis; flags for risky features.

---

## Q66. Database connection pooling.

**Expected answer**

Pools limit connections; PgBouncer transaction pooling for scale; beware session features with transaction pooling; size pools by DB `max_connections` and app replicas.

**Common wrong answer**

Each pod opens 100 connections with 50 replicas — meltdown.

**Follow-ups**

- Transaction vs session pooling?
- How size the pool?

**Trade-offs**

- Latency of pool wait vs DB overload.
- ORM pool + external pooler.

**Production relevance**

External pooler in prod; alert on pool wait and DB conn usage.

---

## Q67. Handling large exports/reports.

**Expected answer**

Async job; stream to object storage; cursor through DB; notify when ready; don’t hold HTTP open for minutes; consider materialized aggregates.

**Common wrong answer**

Sync endpoint that `SELECT *` joins forever — timeouts/OOM.

**Follow-ups**

- How stream CSV without loading all RAM?
- Authz on download links?

**Trade-offs**

- Freshness vs precomputation.
- Cost of big scans.

**Production relevance**

Export service + pre-signed download URLs.

---

## Q68. gRPC vs REST/JSON.

**Expected answer**

gRPC: efficient protobuf, streaming, strict contracts, great service-to-service. REST/JSON: browser-friendly, cacheable, universal. Gateways can translate.

**Common wrong answer**

gRPC everywhere including browsers without a proxy — painful.

**Follow-ups**

- When GraphQL instead?
- Versioning protobuf?

**Trade-offs**

- Debuggability of JSON vs efficiency of protobuf.
- Tooling maturity.

**Production relevance**

External public APIs REST; internal mesh often gRPC.

---

## Q69. Data consistency across services.

**Expected answer**

Sagas/process managers, outbox, idempotent consumers, compensating actions. Prefer avoiding distributed transactions (2PC) in modern microservice designs.

**Common wrong answer**

XA/2PC everywhere — fragile and slow at scale.

**Follow-ups**

- Choreography vs orchestration sagas?
- Inbox pattern?

**Trade-offs**

- Autonomy vs consistency UX.
- Compensation complexity.

**Production relevance**

Order→payment→fulfillment saga with compensations.

---

## Q70. Security headers and API hardening.

**Expected answer**

TLS everywhere, HSTS, secure cookies, input validation, output encoding, rate limits, WAF, dependency scanning, least privilege DB users, parameterized queries.

**Common wrong answer**

Rely on client validation alone.

**Follow-ups**

- SQL injection defenses?
- SSRF risks with URL fetchers?

**Trade-offs**

- Strict security vs partner integrations.
- WAF false positives.

**Production relevance**

Baseline security checklist in every service template.

---

## Q71. Node event loop phases (interview level).

**Expected answer**

Timers → pending callbacks → idle/prepare → poll (I/O) → check (`setImmediate`) → close callbacks. Microtasks between. Don’t block the loop with CPU sync work.

**Common wrong answer**

“Node is multi-threaded for JS” — JS is single-threaded; libuv threadpool for some I/O/CPU.

**Follow-ups**

- `setImmediate` vs `setTimeout(0)`?
- When worker_threads?

**Trade-offs**

- Throughput vs latency under CPU load.
- Threadpool size tuning.

**Production relevance**

Move CPU to workers; monitor event-loop lag.

---

## Q72. Designing webhooks reliably.

**Expected answer**

Sign payloads (HMAC), retries with backoff, idempotency for receivers, timeout budgets, delivery logs, rotate secrets, allowlist IPs if needed.

**Common wrong answer**

Fire-and-forget HTTP without retries or signatures.

**Follow-ups**

- How receivers verify signatures?
- Replay attack prevention?

**Trade-offs**

- At-least-once duplicates vs loss.
- Customer endpoint flakiness.

**Production relevance**

Outbound webhook worker + DLQ + signature headers.

---

## Q73. Read replicas and replication lag.

**Expected answer**

Scale reads with replicas; writes to primary. Lag means stale reads — route read-after-write to primary or use session consistency tokens.

**Common wrong answer**

Send all reads to replicas including after write — users miss their updates.

**Follow-ups**

- Async vs sync replication?
- Failover process?

**Trade-offs**

- Stale reads vs primary load.
- Cross-region lag.

**Production relevance**

Sticky read-your-writes for user sessions; replicas for analytics.

---

## Q74. Capacity planning basics.

**Expected answer**

Measure RPS, payload sizes, p99 latency, concurrency, DB QPS, cache hit rate. Load test; set headroom targets; know saturation signals.

**Common wrong answer**

Guess instance size from vibes — then page at launch.

**Follow-ups**

- How design a load test?
- Knee of the curve?

**Trade-offs**

- Overprovision cost vs risk.
- Synthetic vs real traffic shapes.

**Production relevance**

Load test critical paths pre-launch; autoscale with proven metrics.

---

## Q75. GDPR/PII considerations for backends.

**Expected answer**

Data minimization, purpose limitation, encryption in transit/rest, access controls, retention/deletion, audit logs, DPA with vendors, regional residency if required.

**Common wrong answer**

“We hash emails so GDPR doesn’t apply” — still personal data in many cases.

**Follow-ups**

- Right to erasure with backups/logs?
- Tokenization vs encryption?

**Trade-offs**

- Analytics value vs privacy risk.
- Retention cost.

**Production relevance**

PII inventory; delete workflows; scrub logs; legal review.

---

## Q76. Feature stores / config for backends.

**Expected answer**

Dynamic config and flags for kill switches without redeploy. Validate schemas; default safely; audit changes; separate from secrets.

**Common wrong answer**

Redeploy to change a boolean — slow incident response.

**Follow-ups**

- Config vs secret distinction?
- Consistency across fleet?

**Trade-offs**

- Realtime config vs cache staleness.
- Who can change prod flags.

**Production relevance**

Central config service; break-glass procedures.

---

## Q77. Pagination: cursor vs offset.

**Expected answer**

Offset simple but slow/unstable on shifting data. Cursor/keyset stable and scalable using indexed sort keys. Expose opaque cursors to clients.

**Common wrong answer**

Always `OFFSET` into millions of rows — gets slower linearly.

**Follow-ups**

- How cursor with multi-column sort?
- Total counts expensive?

**Trade-offs**

- Exact totals vs infinite scroll UX.
- Cursor opacity vs debuggability.

**Production relevance**

Public APIs: cursor pagination by default.

---

## Q78. Soft deletes vs hard deletes.

**Expected answer**

Soft delete preserves history/recovery but complicates unique constraints and queries (`deleted_at IS NULL`). Hard delete simpler with archival elsewhere.

**Common wrong answer**

Soft delete everything forever — unique email collisions and huge tables.

**Follow-ups**

- Partial unique indexes?
- Retention jobs?

**Trade-offs**

- Recoverability vs query complexity.
- Legal retention needs.

**Production relevance**

Soft delete user content short-term; hard delete/anonymize on schedule.

---

## Q79. Testing backends effectively.

**Expected answer**

Unit domain logic; integration tests against real DB (testcontainers); contract tests for APIs; load tests for critical paths. Prefer fewer brittle e2e.

**Common wrong answer**

Only mock the database everywhere — false confidence.

**Follow-ups**

- How test migrations?
- Idempotency tests?

**Trade-offs**

- Integration fidelity vs speed.
- Flake management.

**Production relevance**

CI: unit + DB integration; nightly load on staging.

---

## Q80. On-call and incident response expectations.

**Expected answer**

Detect via alerts → triage severity → mitigate (rollback/page) → communicate → fix → postmortem with action items. Runbooks beat heroics.

**Common wrong answer**

Only fix forward during SEV1 with no communication — stakeholders blind.

**Follow-ups**

- What belongs in a runbook?
- Error budgets?

**Trade-offs**

- Alert noise vs missed pages.
- Blameful vs blameless culture.

**Production relevance**

SLO-based alerts; blameless postmortems; tracked follow-ups.
