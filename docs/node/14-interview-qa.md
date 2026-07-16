# Node.js Interview Q&A

Dense drill set spanning [libuv](/node/01-libuv) through [Production](/node/13-production). Answer out loud, then check. Cross-check browser loop differences in [JS Event Loop](/javascript/10-event-loop).

## Event loop & libuv

**Q1. Draw Node’s event loop phases.**  
**Expected:** timers → pending → idle/prepare → poll → check → close; nextTick + microtasks between callbacks.  
**Wrong:** Browser macrotask/render model only.  
**Follow-up:** When does `setImmediate` beat `setTimeout(0)`?

**Q2. What uses the UV thread pool?**  
**Expected:** Much of fs, `dns.lookup`, async crypto/zlib; not TCP I/O.  
**Wrong:** “All async.”  
**Follow-up:** `UV_THREADPOOL_SIZE` effects?

**Q3. `process.nextTick` vs `Promise.then`?**  
**Expected:** nextTick drains first; both can starve poll if recursive.  
**Production:** Prefer yielding via `setImmediate` for long jobs.

**Q4. Why can Node serve 10k connections but fail one CPU endpoint?**  
**Expected:** Concurrent idle sockets cheap; CPU monopolizes single JS thread.

**Q5. `dns.lookup` vs `dns.resolve`?**  
**Expected:** lookup → getaddrinfo/pool; resolve → c-ares.

## Streams & buffers

**Q6. What is backpressure?**  
**Expected:** Writable buffer full → `write` false → wait `drain`; propagates upstream.  
**Wrong:** “Just pipe and forget.”

**Q7. `pipe` vs `pipeline`?**  
**Expected:** pipeline destroys on error and cleans up; pipe error-prone.

**Q8. When is `Buffer.allocUnsafe` safe?**  
**Expected:** Only if every byte overwritten before exposure.  
**Security:** Uncleared memory disclosure.

**Q9. Why `StringDecoder` for TCP text?**  
**Expected:** UTF-8 characters can split across chunks.

**Q10. Object mode streams — when?**  
**Expected:** Parsing to objects (NDJSON); not for raw file bytes.

## Cluster & workers

**Q11. Cluster vs worker_threads?**  
**Expected:** Processes for HTTP multi-core / isolation; threads for CPU with shared process.  
**Follow-up:** Sticky sessions?

**Q12. Why in-memory rate limits break with cluster?**  
**Expected:** Per-process counters; need Redis — [Rate limit](/backend/08-rate-limit).

**Q13. Why not spawn a Worker per HTTP request?**  
**Expected:** Isolate startup cost; use a pool.

**Q14. Can workers share a TCP server handle like cluster?**  
**Expected:** Different model; cluster is for shared ports. Workers ≠ drop-in cluster.

**Q15. SharedArrayBuffer risks?**  
**Expected:** Data races without Atomics; never `Atomics.wait` on main.

## V8 & performance

**Q16. What is a deopt?**  
**Expected:** Optimized code invalidated; fall back to slower tier.

**Q17. Event loop delay high — first checks?**  
**Expected:** Sync work, GC, CPU profiles; vs low delay → downstream waits — [Performance](/node/11-performance).

**Q18. Why raise `--max-old-space-size` isn’t a leak fix?**  
**Expected:** Delays OOM; find retainers.

**Q19. Keep-alive timeout mismatch symptom?**  
**Expected:** Intermittent 502s with LB.

**Q20. p99 vs average?**  
**Expected:** Tail latency drives UX/SLO burn.

## Express, auth, security

**Q21. Why Express 4 async errors hang?**  
**Expected:** No automatic catch; wrap → `next(err)`.

**Q22. Error middleware arity?**  
**Expected:** `(err, req, res, next)` — four args.

**Q23. JWT vs session?**  
**Expected:** Stateless vs revocable server state; hybrid refresh common — [JWT](/node/08-jwt-auth).

**Q24. Why HttpOnly cookies?**  
**Expected:** Mitigate token theft via XSS (not CSRF).

**Q25. Algorithm confusion attack on JWT?**  
**Expected:** Attacker sets `alg: none` or HS with public key; allowlist algs.

**Q26. Prototype pollution vector?**  
**Expected:** Unsafe recursive merge of JSON `__proto__`.

**Q27. SSRF from webhook URL feature?**  
**Expected:** Server fetches attacker URL → metadata IPs; allowlist/block private ranges.

**Q28. `trust proxy` importance?**  
**Expected:** Correct client IP for rate limits/cookies; only trust real proxy hops.

**Q29. Mass assignment?**  
**Expected:** Binding `req.body` into ORM update → privilege escalation; use DTOs.

**Q30. ReDoS in Node?**  
**Expected:** Catastrophic regex blocks event loop — CPU DoS.

## Production & scaling

**Q31. Liveness vs readiness?**  
**Expected:** Restart vs traffic admission — [Production](/node/13-production).

**Q32. Graceful shutdown steps?**  
**Expected:** SIGTERM → fail ready → `server.close` → close pools → exit; deadline.

**Q33. Scale WebSockets across nodes?**  
**Expected:** Pub/sub fanout; sticky optional — [Chat SD](/backend-system-design/03-chat).

**Q34. DB pool storm after HPA?**  
**Expected:** pods × pool > DB max; centralize sizing.

**Q35. When to queue vs sync?**  
**Expected:** Long/fragile side effects → 202 + job — [Queues](/backend/06-queues).

## Rapid-fire (one-liners)

| Q | A |
| --- | --- |
| Is Node multi-threaded for JS? | One JS thread per isolate/process |
| Who owns TCP async? | libuv + kernel, not FS pool |
| Microtask vs timer? | Microtasks first |
| `unref` timer? | Don’t keep process alive |
| Duplex vs Transform? | Independent sides vs map chunks |
| HS256 vs RS256? | Shared vs asymmetric verify |
| Cluster in k8s? | Usually prefer multi-pod |
| `alloc` vs `allocUnsafe`? | Zeroed vs fast dirty |
| Cap body size? | DoS / memory |
| Structured logs? | JSON + requestId |

## Scenario prompts

**S1.** “p99 latency jumped after deploy; CPU flat.”  
Walk: traces → DB/Redis; lock contention; downstream timeout retries amplification.

**S2.** “Uploads OOM the API.”  
Walk: buffering whole file; switch to streams/S3; size limits; [Streams](/node/03-streams).

**S3.** “Login works but random 401s with 4 workers.”  
Walk: sticky session memory store; move sessions to Redis.

**S4.** “Crypto login endpoint stalls FS reads.”  
Walk: shared UV pool; raise size carefully / separate concerns / rate limit login.

**S5.** “After k8s rollout, 30s of 502s.”  
Walk: no graceful drain; readiness; LB idle; migration lock.

## Common Mistakes (meta)

- Memorizing phase names without nextTick/microtask rules.
- Treating JWT as encrypted.
- Scaling out stateful nodes.
- Profiling only in local without prod-like data.
- Skipping idempotency when introducing queues.

## Trade-offs (meta)

Senior answers always add: **consistency vs latency**, **stateless vs revoke**, **copy vs share**, **one process vs many**, **sync UX vs async jobs**. Tie choices to SLOs and failure modes — practice with [Backend System Design](/backend-system-design/index).

## Study path (2 hours)

1. [libuv](/node/01-libuv) + [Event loop](/node/02-event-loop) + [JS loop](/javascript/10-event-loop) (45m)  
2. Streams/Buffers + one flamechart mental model (20m)  
3. Auth + Security + Middleware (30m)  
4. Scaling + Production + this Q&A aloud (25m)


## Extra deep questions

**Q36. How does `async_hooks` / ALS break?**  
**Expected:** Native callbacks or broken promise chains lose context; some DB drivers historically needed explicit propagation.  
**Production:** Prefer well-supported OTEL instrumentation.

**Q37. Backpressure across HTTP/2?**  
**Expected:** Stream-level flow control; still apply app-level limits on concurrent streams/handlers.

**Q38. Why might `server.close` never callback?**  
**Expected:** Keep-alive sockets still open; destroy idle connections or set shorter keepAliveTimeout on shutdown.

**Q39. Difference between `res.end` and `res.destroy`?**  
**Expected:** end finishes gracefully; destroy aborts socket — use on client abort / timeout.

**Q40. How to safely parse multipart?**  
**Expected:** Busboy/multer with limits; stream to disk/S3; never buffer unbounded.

## Cheat sheet: “what blocks Node?”

| Blocks loop | Doesn’t (usually) |
| --- | --- |
| Sync FS/crypto/zlib | Network I/O |
| Tight CPU JS | `fs.promises.*` |
| Huge JSON.parse | Worker offload |
| Sync child_process | Thread pool work (except pool wait) |
| Catastrophic regex | Timers waiting |
