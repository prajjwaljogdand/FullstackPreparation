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

be = []

be.append(Q(41, "Design a REST API for a multi-tenant SaaS resource.",
"Resource-oriented URLs, tenant isolation in authz (not just URL), pagination, filtering, idempotent writes (`Idempotency-Key`), problem+json errors, versioning strategy, rate limits per tenant.",
"Put `tenantId` only in the body and trust the client — IDOR waiting to happen.",
["Cursor vs offset pagination?", "How version without `/v2` forever?"],
["Strict REST vs pragmatic RPC endpoints.", "Global vs per-tenant rate limits."],
"Enforce tenant from auth context on every query; audit access."))

be.append(Q(42, "SQL vs NoSQL: how do you choose?",
"SQL for relational integrity, complex queries, transactions. NoSQL (document/kv/wide-column) for flexible schemas, massive scale patterns, simple access by key. Many systems are polyglot.",
"“NoSQL is always more scalable” — depends on access patterns and ops maturity.",
["When NewSQL/distributed SQL?", "How migrate later?"],
["Flexible schema vs long-term queryability.", "Ops expertise on the team."],
"Orders/payments → SQL; session/cache → Redis; activity feed often hybrid."))

be.append(Q(43, "Explain indexes and when they hurt.",
"B-tree indexes speed lookups/ranges/sorts matching left-prefix. Covering indexes avoid table lookups. They slow writes, use disk, and wrong ones confuse the planner. Measure with `EXPLAIN`.",
"Index every column — write amplification and bloat.",
["Composite index column order?", "Partial/filtered indexes?"],
["Read latency vs write throughput.", "Index maintenance during migrations."],
"Index hot filters/FKs; drop unused via stats; review slow query logs."))

be.append(Q(44, "Transactions: isolation levels and anomalies.",
"Read uncommitted/committed, repeatable read, serializable. Anomalies: dirty/non-repeatable/phantom reads. Choose the weakest level that preserves correctness for the use case.",
"“Serializable always” without discussing latency/abort rates.",
["Optimistic vs pessimistic concurrency?", "Idempotent retries on abort?"],
["Strong isolation vs throughput.", "App-level invariants vs DB constraints."],
"Payments: stronger isolation + idempotency keys; feeds: often weaker."))

be.append(Q(45, "ORM vs query builder vs raw SQL.",
"ORM: speed for CRUD, relations, migrations. Query builder: composable SQL with less magic. Raw: hot paths, complex analytics, precise plans. Mix deliberately.",
"ORM for everything including reporting — N+1 and opaque queries.",
["How prevent N+1?", "Migration strategies?"],
["DX vs control.", "Vendor lock-in to ORM features."],
"CRUD via ORM; dashboards via SQL; always log slow queries."))

be.append(Q(46, "Caching with Redis: patterns and pitfalls.",
"Cache-aside, read-through, write-through, write-behind. Key design, TTLs, stampede protection (locking/singleflight), invalidation on writes, memory eviction policies.",
"Cache forever without invalidation — stale money/permissions bugs.",
["Thundering herd fixes?", "Cache nulls?"],
["Freshness vs hit rate.", "Redis as primary store anti-pattern."],
"Cache public reads; never trust cache alone for authz decisions."))

be.append(Q(47, "Idempotency for payment/order APIs.",
"Client sends `Idempotency-Key`; server persists key→response; retries return same result. Deduplicate side effects (charges, emails) with unique constraints and outbox.",
"“Just retry POST” without keys — double charge.",
["Where store keys?", "TTL for idempotency records?"],
["Storage cost vs safety.", "Exactly-once vs at-least-once + idempotent handlers."],
"Mandatory for billing, payouts, provisioning."))

be.append(Q(48, "Rate limiting algorithms.",
"Fixed window, sliding window, token bucket, leaky bucket. Enforce at edge/API gateway and app. Keys: IP, user, API key, tenant. Return `Retry-After`.",
"Only rate limit by IP — shared NATs punish many users.",
["Distributed rate limits with Redis?", "How handle authenticated bursts?"],
["Fairness vs abuse protection.", "False positives on mobile carriers."],
"Layer CDN + Redis token bucket per API key/tenant."))

be.append(Q(49, "Authentication vs authorization.",
"Authn: who are you (session/JWT/OIDC). Authz: what can you do (RBAC/ABAC/ReBAC). Never encode authz only in the frontend. Prefer deny-by-default.",
"Hide admin buttons and call that security.",
["RBAC vs ABAC?", "JWT claims for roles — risks?"],
["Central policy service vs local checks.", "Token size vs lookup latency."],
"Enforce authz in API/DB policies; audit sensitive actions."))

be.append(Q(50, "JWT access vs refresh tokens.",
"Short-lived access tokens; longer refresh with rotation and reuse detection. Store refresh securely (HttpOnly cookie). Revocation via denylist/version or short TTL + rotation.",
"Week-long JWT in localStorage with no rotation.",
["How detect refresh reuse?", "Opaque vs self-contained tokens?"],
["Stateless verification vs revocation difficulty.", "Cookie CSRF vs bearer XSS surface."],
"Access 5–15m; rotating refresh; revoke on logout/password change."))

be.append(Q(51, "Password storage and login hardening.",
"Hash with Argon2id/bcrypt/scrypt + unique salt; never reversible encryption for passwords. Rate limit, lockouts/backoff, MFA, breach detection, secure reset flows.",
"SHA-256 password hashing — too fast, no work factor.",
["Pepper vs salt?", "Passkeys/WebAuthn benefits?"],
["UX friction of MFA vs account takeover risk.", "Legacy hash migration."],
"Argon2id params tuned to CPU; force reset on suspected breach."))

be.append(Q(52, "Design a job queue system.",
"Producers enqueue; workers pull with visibility timeout; retries with backoff; DLQ; idempotent handlers; metrics on lag/age; poison message handling.",
"Process async work in the web request thread forever.",
["At-least-once delivery implications?", "Priority queues?"],
["SQS/Rabbit/Kafka suitability.", "Ordering vs throughput."],
"Emails, webhooks, image processing — SQS/BullMQ with DLQ alarms."))

be.append(Q(53, "Kafka vs RabbitMQ vs SQS (interview framing).",
"Kafka: durable log, high throughput, consumer groups, replay. Rabbit: flexible routing, classic work queues. SQS: managed, simple, at-least-once, limited ordering (FIFO).",
"“Kafka is a message queue” only — it’s a distributed log with different semantics.",
["When need exactly-once?", "Compaction use cases?"],
["Ops complexity vs capability.", "Fan-out patterns."],
"Event streaming/analytics → Kafka; task queues → SQS/Rabbit."))

be.append(Q(54, "Database migrations in production.",
"Expand/contract: additive changes first, dual-write/read if needed, backfill, then remove old. Avoid long locks; online schema tools; expand app compatibility window.",
"Rename column in one deploy — breaks old app instances.",
["How backfill large tables?", "Zero-downtime expand/contract examples?"],
["Migration speed vs lock risk.", "Feature flags for dual paths."],
"Strong migration review culture; runbooks for rollback."))

be.append(Q(55, "Observability: metrics, logs, traces.",
"Metrics for SLOs/alerts; structured logs for forensics; traces for request fan-out. Correlate with `trace_id`. RED/USE methods. Alert on symptoms (latency/error) not only causes.",
"Log everything at INFO and page on every error — noise.",
["SLI vs SLO vs SLA?", "Cardinality pitfalls in metrics?"],
["Retention cost vs debuggability.", "Sampling traces."],
"p95/p99 latency + error rate burn alerts; exemplars to traces."))

be.append(Q(56, "Circuit breaker, bulkhead, retry.",
"Retries with jittered backoff for transient faults; circuit breaker stops calling unhealthy deps; bulkheads isolate pools. Don’t retry non-idempotent requests without keys.",
"Blind infinite retries — amplify outages.",
["When fail-fast vs queue?", "Hedged requests?"],
["Availability vs duplicate side effects.", "Timeouts too aggressive vs too long."],
"Outbound HTTP clients: timeouts + breaker + metrics."))

be.append(Q(57, "Horizontal scaling Node.js APIs.",
"Cluster/PM2 or multiple containers behind LB; stickiness only if required; externalize sessions; share-nothing; watch event-loop lag; separate CPU-heavy work to workers.",
"Bigger single VM forever — vertical scaling ceiling.",
["Sticky sessions problems?", "How measure event-loop delay?"],
["Process count vs memory.", "Stateful websocket routing."],
"K8s HPA on CPU/RPS/lag; Redis sessions; workers for CPU."))

be.append(Q(58, "File uploads at scale.",
"Direct-to-object-storage with pre-signed URLs; virus scan; size/type limits; multipart for large files; async processing pipeline; CDN for download.",
"Stream all uploads through app servers to disk — bottleneck and risk.",
["How secure pre-signed URLs?", "Image transformation pipeline?"],
["App proxy control vs S3 direct cost/complexity.", "Retention/GDPR deletes."],
"S3/GCS pre-sign; Lambda/workers for thumbnails; lifecycle policies."))

be.append(Q(59, "Search: Postgres vs Elasticsearch.",
"Postgres full-text / trigram for moderate needs and simpler ops. ES/OpenSearch for relevance tuning, facets, high-volume text. Keep source of truth in primary DB; async index.",
"ES as system of record — durability/consistency pain.",
["How handle indexing lag?", "Synonyms/ranking?"],
["Ops complexity vs search quality.", "Dual-write consistency."],
"Start with Postgres; graduate to ES when relevance/scale demands."))

be.append(Q(60, "Multi-tenant data isolation strategies.",
"Shared schema + `tenant_id` (RLS), schema-per-tenant, DB-per-tenant. Shared is cheapest; separate is strongest isolation. Always filter by auth tenant — never trust client.",
"Only separate by subdomain — still shared tables without filters.",
["Postgres RLS patterns?", "Noisy neighbor mitigations?"],
["Cost vs isolation.", "Migration/customization per tenant."],
"Most SaaS: shared + RLS; enterprise: dedicated DB option."))

be.append(Q(61, "API gateway responsibilities.",
"TLS termination, authn, rate limit, routing, request validation, canary, WAF. Keep business logic in services. Avoid god-gateway that owns domain rules.",
"Put all business logic in the gateway — unmaintainable.",
["Gateway vs service mesh?", "Auth at edge vs service?"],
["Central control vs service autonomy.", "Latency hop cost."],
"Kong/Cloud API Gateway for cross-cutting concerns only."))

be.append(Q(62, "Event-driven architecture pitfalls.",
"Dual writes without outbox, unordered consumers, poison messages, schema evolution breaks, debugging complexity, eventual consistency surprises for product.",
"“Events mean we don’t need transactions” — you still need consistency patterns.",
["Transactional outbox?", "Consumer idempotency?"],
["Coupling via event schemas.", "Sync UX vs async reality."],
"Outbox + idempotent consumers + schema registry."))

be.append(Q(63, "Design a notification system.",
"Ingest events → preference service → fan-out to channels (email/push/SMS/in-app) via queues; templates; quiet hours; dedupe; delivery receipts; rate limits; user preference center.",
"Send email synchronously in the request — timeouts and spikes.",
["How avoid spammy duplicates?", "Priority channels?"],
["Fan-out cost vs personalization.", "Provider redundancy."],
"Queue per channel; templates versioned; metrics on send/fail."))

be.append(Q(64, "Secrets management.",
"No secrets in git or images. Use KMS/Secrets Manager/Vault; short-lived credentials; rotate; least privilege IAM; inject at runtime; audit access.",
"`.env` committed “just for staging” — still a leak vector.",
["How rotate DB passwords with zero downtime?", "Workload identity?"],
["Central vault vs cloud-native secrets.", "Developer DX."],
"OIDC to cloud; rotate automatically; scan repos for secrets."))

be.append(Q(65, "Blue/green vs canary vs rolling deploys.",
"Rolling: gradually replace. Blue/green: switch traffic between two envs. Canary: small % traffic then promote. Need health checks, metrics, and fast rollback.",
"Canary without metrics — you’re just slow-rolling failures.",
["DB migrations with canaries?", "Feature flags vs deploy strategies?"],
["Infra cost of blue/green.", "Canary analysis complexity."],
"K8s rolling + canary analysis; flags for risky features."))

be.append(Q(66, "Database connection pooling.",
"Pools limit connections; PgBouncer transaction pooling for scale; beware session features with transaction pooling; size pools by DB `max_connections` and app replicas.",
"Each pod opens 100 connections with 50 replicas — meltdown.",
["Transaction vs session pooling?", "How size the pool?"],
["Latency of pool wait vs DB overload.", "ORM pool + external pooler."],
"External pooler in prod; alert on pool wait and DB conn usage."))

be.append(Q(67, "Handling large exports/reports.",
"Async job; stream to object storage; cursor through DB; notify when ready; don’t hold HTTP open for minutes; consider materialized aggregates.",
"Sync endpoint that `SELECT *` joins forever — timeouts/OOM.",
["How stream CSV without loading all RAM?", "Authz on download links?"],
["Freshness vs precomputation.", "Cost of big scans."],
"Export service + pre-signed download URLs."))

be.append(Q(68, "gRPC vs REST/JSON.",
"gRPC: efficient protobuf, streaming, strict contracts, great service-to-service. REST/JSON: browser-friendly, cacheable, universal. Gateways can translate.",
"gRPC everywhere including browsers without a proxy — painful.",
["When GraphQL instead?", "Versioning protobuf?"],
["Debuggability of JSON vs efficiency of protobuf.", "Tooling maturity."],
"External public APIs REST; internal mesh often gRPC."))

be.append(Q(69, "Data consistency across services.",
"Sagas/process managers, outbox, idempotent consumers, compensating actions. Prefer avoiding distributed transactions (2PC) in modern microservice designs.",
"XA/2PC everywhere — fragile and slow at scale.",
["Choreography vs orchestration sagas?", "Inbox pattern?"],
["Autonomy vs consistency UX.", "Compensation complexity."],
"Order→payment→fulfillment saga with compensations."))

be.append(Q(70, "Security headers and API hardening.",
"TLS everywhere, HSTS, secure cookies, input validation, output encoding, rate limits, WAF, dependency scanning, least privilege DB users, parameterized queries.",
"Rely on client validation alone.",
["SQL injection defenses?", "SSRF risks with URL fetchers?"],
["Strict security vs partner integrations.", "WAF false positives."],
"Baseline security checklist in every service template."))

be.append(Q(71, "Node event loop phases (interview level).",
"Timers → pending callbacks → idle/prepare → poll (I/O) → check (`setImmediate`) → close callbacks. Microtasks between. Don’t block the loop with CPU sync work.",
"“Node is multi-threaded for JS” — JS is single-threaded; libuv threadpool for some I/O/CPU.",
["`setImmediate` vs `setTimeout(0)`?", "When worker_threads?"],
["Throughput vs latency under CPU load.", "Threadpool size tuning."],
"Move CPU to workers; monitor event-loop lag."))

be.append(Q(72, "Designing webhooks reliably.",
"Sign payloads (HMAC), retries with backoff, idempotency for receivers, timeout budgets, delivery logs, rotate secrets, allowlist IPs if needed.",
"Fire-and-forget HTTP without retries or signatures.",
["How receivers verify signatures?", "Replay attack prevention?"],
["At-least-once duplicates vs loss.", "Customer endpoint flakiness."],
"Outbound webhook worker + DLQ + signature headers."))

be.append(Q(73, "Read replicas and replication lag.",
"Scale reads with replicas; writes to primary. Lag means stale reads — route read-after-write to primary or use session consistency tokens.",
"Send all reads to replicas including after write — users miss their updates.",
["Async vs sync replication?", "Failover process?"],
["Stale reads vs primary load.", "Cross-region lag."],
"Sticky read-your-writes for user sessions; replicas for analytics."))

be.append(Q(74, "Capacity planning basics.",
"Measure RPS, payload sizes, p99 latency, concurrency, DB QPS, cache hit rate. Load test; set headroom targets; know saturation signals.",
"Guess instance size from vibes — then page at launch.",
["How design a load test?", "Knee of the curve?"],
["Overprovision cost vs risk.", "Synthetic vs real traffic shapes."],
"Load test critical paths pre-launch; autoscale with proven metrics."))

be.append(Q(75, "GDPR/PII considerations for backends.",
"Data minimization, purpose limitation, encryption in transit/rest, access controls, retention/deletion, audit logs, DPA with vendors, regional residency if required.",
"“We hash emails so GDPR doesn’t apply” — still personal data in many cases.",
["Right to erasure with backups/logs?", "Tokenization vs encryption?"],
["Analytics value vs privacy risk.", "Retention cost."],
"PII inventory; delete workflows; scrub logs; legal review."))

be.append(Q(76, "Feature stores / config for backends.",
"Dynamic config and flags for kill switches without redeploy. Validate schemas; default safely; audit changes; separate from secrets.",
"Redeploy to change a boolean — slow incident response.",
["Config vs secret distinction?", "Consistency across fleet?"],
["Realtime config vs cache staleness.", "Who can change prod flags."],
"Central config service; break-glass procedures."))

be.append(Q(77, "Pagination: cursor vs offset.",
"Offset simple but slow/unstable on shifting data. Cursor/keyset stable and scalable using indexed sort keys. Expose opaque cursors to clients.",
"Always `OFFSET` into millions of rows — gets slower linearly.",
["How cursor with multi-column sort?", "Total counts expensive?"],
["Exact totals vs infinite scroll UX.", "Cursor opacity vs debuggability."],
"Public APIs: cursor pagination by default."))

be.append(Q(78, "Soft deletes vs hard deletes.",
"Soft delete preserves history/recovery but complicates unique constraints and queries (`deleted_at IS NULL`). Hard delete simpler with archival elsewhere.",
"Soft delete everything forever — unique email collisions and huge tables.",
["Partial unique indexes?", "Retention jobs?"],
["Recoverability vs query complexity.", "Legal retention needs."],
"Soft delete user content short-term; hard delete/anonymize on schedule."))

be.append(Q(79, "Testing backends effectively.",
"Unit domain logic; integration tests against real DB (testcontainers); contract tests for APIs; load tests for critical paths. Prefer fewer brittle e2e.",
"Only mock the database everywhere — false confidence.",
["How test migrations?", "Idempotency tests?"],
["Integration fidelity vs speed.", "Flake management."],
"CI: unit + DB integration; nightly load on staging."))

be.append(Q(80, "On-call and incident response expectations.",
"Detect via alerts → triage severity → mitigate (rollback/page) → communicate → fix → postmortem with action items. Runbooks beat heroics.",
"Only fix forward during SEV1 with no communication — stakeholders blind.",
["What belongs in a runbook?", "Error budgets?"],
["Alert noise vs missed pages.", "Blameful vs blameless culture."],
"SLO-based alerts; blameless postmortems; tracked follow-ups."))

header = """# Senior Q&A — Backend (41–80)

API design, data, reliability, security, and operations. Answer with trade-offs, not slogans.

"""
(OUT / "02-backend.md").write_text(header + "\n---\n\n".join(be))
print("backend", len(be))
