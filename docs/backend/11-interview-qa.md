# Backend Engineering Interview Q&A

Cross-cutting drill for [API Design](/backend/01-api-design) through [Ops](/backend/10-ops). Pair with [Node Q&A](/node/14-interview-qa) and [Backend System Design](/backend-system-design/index).

## APIs & HTTP

**Q1. Idempotent methods?**  
**Expected:** GET/PUT/DELETE idempotent; POST not unless Idempotency-Key.  
**Follow-up:** Design idempotent charge API.

**Q2. Cursor vs offset pagination?**  
**Expected:** Cursor stable under inserts; offset drifts / expensive deep pages.  
**Use:** Feeds — [News Feed](/backend-system-design/02-news-feed).

**Q3. 401 vs 403?**  
**Expected:** 401 unauthenticated; 403 authenticated lacking permission.

**Q4. When GraphQL over REST?**  
**Expected:** Multi-client field needs / BFF; accept caching & cost control complexity.

**Q5. Why not 200 for all errors?**  
**Expected:** Breaks HTTP clients/caches/monitors; use proper status + body.

## SQL & data

**Q6. Leftmost prefix rule?**  
**Expected:** `(a,b,c)` helps `a`, `a,b`, `a,b,c` — not `b` alone.

**Q7. What does EXPLAIN tell you?**  
**Expected:** Access method, joins, costs; ANALYZE shows actual rows/time.

**Q8. Isolation level you’d pick for transfers?**  
**Expected:** Transaction with sufficient isolation / `FOR UPDATE` / serializable; discuss anomalies.

**Q9. N+1 fix?**  
**Expected:** Join/include/IN batch/DataLoader; measure query count.

**Q10. Zero-downtime add NOT NULL column?**  
**Expected:** Expand nullable → backfill → constrain; avoid long locks.

**Q11. Optimistic vs pessimistic locking?**  
**Expected:** Version column retries vs `FOR UPDATE`; contention profile decides.

## NoSQL & ORM

**Q12. Embed vs reference?**  
**Expected:** Bounded co-read embed; shared/unbounded reference.

**Q13. Hot partition?**  
**Expected:** Salt/bucket keys; fan-out writes.

**Q14. ORM production footgun?**  
**Expected:** N+1, overfetch, migrate locks, hidden queries.

**Q15. When raw SQL?**  
**Expected:** Windows/CTEs/`SKIP LOCKED`/bulk updates.

## Redis & cache

**Q16. Cache-aside flow?**  
**Expected:** Read cache → miss DB → set TTL; write updates DB → invalidate.

**Q17. Stampede control?**  
**Expected:** Single-flight lock, stale-while-revalidate, jitter TTL — [Redis](/backend/05-redis).

**Q18. Why TTL even with invalidation?**  
**Expected:** Safety net for missed invalidations / memory.

**Q19. Redis down strategy?**  
**Expected:** Fail-open vs closed; circuit breaker; degrade features.

**Q20. Is Redis a DB?**  
**Expected:** Can be with persistence/HA design; usually cache/session — be explicit about durability.

## Queues

**Q21. At-least-once implication?**  
**Expected:** Idempotent consumers / dedupe.

**Q22. Visibility timeout too short?**  
**Expected:** Duplicate processing while first still runs.

**Q23. Outbox why?**  
**Expected:** Atomically commit state + message intent; relay publishes.

**Q24. DLQ purpose?**  
**Expected:** Isolate poison; alert; manual replay.

**Q25. Kafka vs SQS one-liner?**  
**Expected:** Log/replay/partitions vs simple managed queue.

## Auth & abuse

**Q26. Refresh rotation + reuse?**  
**Expected:** New refresh each use; reuse → revoke family.

**Q27. PKCE why?**  
**Expected:** Secure auth code for public clients.

**Q28. Token bucket vs fixed window?**  
**Expected:** Bucket bursts smoothly; fixed easy but boundary burst.

**Q29. Rate limit key for login?**  
**Expected:** IP + account identifier; lockout UX; CAPTCHA — avoid pure IP on CGNAT.

**Q30. CSRF with cookie sessions?**  
**Expected:** SameSite + CSRF token for mutating routes.

## Observability & ops

**Q31. RED metrics?**  
**Expected:** Rate, Errors, Duration.

**Q32. High cardinality mistake?**  
**Expected:** `userId` as Prometheus label.

**Q33. Liveness vs readiness?**  
**Expected:** Restart vs traffic; DB in ready not live.

**Q34. Zero-downtime ingredients?**  
**Expected:** Multi-replica, probes, drain, compatible migrate, SLO watch.

**Q35. Error budget?**  
**Expected:** Allowed unreliability guiding release pace.

## Scenario drills

**S1. Checkout p99 spike, DB CPU high.**  
Indexes? Lock waits? Cache miss storm? Connection storm after scale-out?

**S2. Double charges reported.**  
Retries without idempotency; visibility timeout; missing unique constraint.

**S3. Cache returns other user’s data.**  
Cache key missing user/tenant scope; CDN cached `Authorization` variant wrong.

**S4. Deploy caused 15m outage.**  
Breaking migrate; single replica; no drain; readiness always 200.

**S5. Redis memory maxed.**  
No TTL; big keys; `keys *`; eviction → stampede to DB.

## Rapid-fire

| Prompt | Punchline |
| --- | --- |
| CAP tweet answer | Tunable consistency; patterns > slogans |
| Exactly-once | Effective via idempotency |
| 429 body | Include Retry-After |
| GraphQL N+1 | DataLoader |
| Connection pools | pods × pool < DB max |
| Secrets | Manager + rotate |
| Canary | % traffic + SLO abort |
| Message order | Per partition key |
| SSRF | Block link-local |
| Soft delete index | Partial `WHERE deleted_at IS NULL` |

## Common Mistakes (meta)

- Jumping to Kafka before proving need.
- Caching without invalidation story.
- Authz only in UI.
- Migrations as afterthought.
- Alerts without user-facing SLIs.

## Trade-offs (meta)

Senior answers name **consistency, latency, cost, operability, and failure modes**. Practice end-to-end designs: [URL shortener](/backend-system-design/01-url-shortener), [Rate limiter](/backend-system-design/04-rate-limiter), [Auth service](/backend-system-design/10-auth-service), [Cache layer](/backend-system-design/11-cache-layer).

## 90-minute revision path

1. API + SQL indexes/transactions (25m)  
2. Redis stampede + queues idempotency (25m)  
3. Auth/OIDC + rate limit (20m)  
4. Observability + ops zero-downtime (20m)  
5. Speak 5 scenarios from this page aloud


## Extra scenarios

**S6. Search results stale by minutes.**  
CDC lag? Cache TTL? Dual write bug? Index refresh interval?

**S7. One tenant starves others.**  
Missing per-tenant RL/quotas; noisy neighbor queries; need isolation — [SaaS API](/backend-system-design/09-saas-api).

**S8. Workers duplicate emails.**  
At-least-once + non-idempotent send; need provider idempotency key / sent_events table.

## Architecture narrative template

1. Requirements & SLOs  
2. API + data model  
3. Single-box design  
4. Bottlenecks  
5. Scale-out levers (cache/queue/shard)  
6. Failure modes  
7. Obs & ops  

Use on every [Backend System Design](/backend-system-design/index) problem.
