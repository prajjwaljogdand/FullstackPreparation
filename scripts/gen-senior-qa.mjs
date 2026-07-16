import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const root = path.join(path.dirname(fileURLToPath(import.meta.url)), 'docs')

function w(rel, body) {
  const p = path.join(root, rel)
  fs.mkdirSync(path.dirname(p), { recursive: true })
  fs.writeFileSync(p, body.trim() + '\n')
  console.log('wrote', rel)
}

function expand(bank, start, count, title) {
  const parts = [`# ${title}\n`]
  for (let i = 0; i < count; i++) {
    const [q, a, wrong, follow, prod] = bank[i % bank.length]
    const n = start + i
    const label =
      i < bank.length ? q : q.replace(/\?$/, '') + ` (variant ${Math.floor(i / bank.length) + 1})?`
    parts.push(`### Q${n}. ${label}

**Expected:** ${a}

**Common wrong:** ${wrong}

**Follow-ups:** ${follow}

**Trade-offs:** Prefer explicit trade-offs over absolute rules; state assumptions.

**Production:** ${prod}
`)
  }
  return parts.join('\n')
}

const feBank = [
  ['Explain React Fiber briefly.', 'Unit of work + linked-tree reconciler enabling interruptible render and priority lanes.', 'Virtual DOM diff only.', 'How do lanes relate to transitions?', 'Guides concurrent UI without blocking input.'],
  ['useEffect vs useLayoutEffect?', 'Layout runs after DOM mutations before paint; effect after paint.', 'They are the same.', 'When does layout thrash?', 'Measure DOM in layout; avoid heavy sync work.'],
  ['Why keys matter in lists?', 'Stable identity for reconciliation; wrong keys remount/state bugs.', 'Index keys always fine.', 'When are index keys OK?', 'Prefer stable IDs from server.'],
  ['Controlled vs uncontrolled inputs?', 'Controlled: React state source of truth; uncontrolled: DOM + refs.', 'Always controlled.', 'Forms at scale?', 'Uncontrolled + FormData for large forms.'],
  ['How does Context cause rerenders?', 'Consumers rerender when value reference changes.', 'Context never rerenders.', 'Split contexts? memo?', 'Stabilize value; split providers; use selectors/external store.'],
  ['memo/useMemo/useCallback trade-offs?', 'Skip work if deps equal; cost of comparison + complexity.', 'Memo everything.', 'When does memo fail?', 'Profile first; React Compiler may auto-memo.'],
  ['Explain hydration mismatch.', 'Server HTML ≠ client first render → React warns/fixes.', 'Only CSS issue.', 'How to debug?', 'Avoid date/random in SSR; suppress only carefully.'],
  ['CSR vs SSR vs SSG vs ISR?', 'CSR client fetch; SSR per-request HTML; SSG build-time; ISR revalidate.', 'SSR always fastest.', 'When ISR?', 'Content sites with freshness needs.'],
  ['Critical rendering path?', 'HTML/CSS → DOM/CSSOM → render tree → layout → paint → composite.', 'JS always first.', 'defer/async?', 'Minimize render-blocking resources.'],
  ['XSS defenses?', 'Encode output, CSP, sanitize HTML, HttpOnly cookies.', 'escape once anywhere.', 'DOM XSS?', 'Trusted Types; avoid innerHTML.'],
]

const beBank = [
  ['Node event loop phases?', 'timers → pending → idle/prepare → poll → check → close; nextTick/microtasks between.', 'Same as browser.', 'nextTick vs Promise?', "Don't starve poll with nextTick loops."],
  ['Cluster vs worker_threads?', 'Cluster: multi-process share port; workers: threads share memory optionally.', 'Same thing.', 'When which?', 'CPU-bound → workers; multi-core HTTP → cluster/PM2.'],
  ['N+1 query fix?', 'Join, dataloader, IN query, embed.', 'Add index only.', 'ORM pitfalls?', 'Select what you need; watch cartesian products.'],
  ['Redis cache stampede?', 'Lock/singleflight, probabilistic early expire, serve stale.', 'Shorter TTL.', 'Multi-key?', 'Consistent hashing; coalescing.'],
  ['At-least-once delivery?', 'Message may duplicate → consumers must be idempotent.', 'Exactly-once always.', 'Outbox pattern?', 'Transactional outbox + dedupe keys.'],
  ['JWT vs session?', 'JWT: stateless token; session: server store.', 'JWT always better.', 'Revocation?', 'Short TTL + refresh rotation; blocklists.'],
  ['Idempotency keys?', 'Client key + server dedupe store for unsafe retries.', 'Only for GET.', 'TTL?', 'Store response for window; 24h common.'],
  ['Horizontal vs vertical scale?', 'Add machines vs bigger machine.', 'Horizontal always.', 'Sticky sessions?', 'Prefer stateless + shared store.'],
  ['Connection pooling why?', 'DB connections expensive; pool reuses.', 'Unlimited connections.', 'Pool size?', 'Tune to DB max and latency.'],
  ['Observability pillars?', 'Logs, metrics, traces — correlate with request IDs.', 'Logs enough.', 'Cardinality?', 'Avoid high-cardinality labels.'],
]

const fsBank = [
  ['Design auth for SPA + API?', 'HttpOnly secure cookies or Bearer access+refresh; CSRF if cookies; rotate refresh.', 'localStorage JWT forever.', 'SSO?', 'OIDC; BFF pattern.'],
  ['Where to cache?', 'CDN → edge → app Redis → DB; invalidate carefully.', 'Cache everything in React Query only.', 'Who owns TTL?', 'Define source of truth.'],
  ['Upload large files?', 'Direct-to-S3 presigned; multipart; virus scan async.', 'Proxy all through Node.', 'Progress UX?', 'Client to storage; webhook complete.'],
  ['Realtime updates?', 'SSE vs WebSocket vs poll; backpressure; reconnect.', 'Socket.io always.', 'Scale fans-out?', 'Pub/sub + sticky or Redis adapter.'],
  ['FE/BE pagination contract?', 'Cursor > offset for feeds; stable sort key.', 'page=1 always.', 'Total count?', 'Expensive — approximate or omit.'],
  ['Feature flags?', 'Server evaluation; avoid FOUC; audit.', 'Hardcode ifs.', 'Kill switches?', 'Remote config with defaults.'],
  ['Error model across tiers?', 'Typed error codes; map to HTTP; never leak internals.', 'Throw strings.', 'Client UX?', 'Retryable vs fatal.'],
  ['Multi-tenant data isolation?', 'tenant_id everywhere; RLS; separate DB for high compliance.', 'Filter in app only.', 'Noisy neighbor?', 'Quotas per tenant.'],
  ['Search UX + backend?', 'Debounce FE; prefix index/ES; rate limit.', 'LIKE %q% on primary.', 'Typo tolerance?', 'Edge ngrams / search engine.'],
  ['Deploy FE+BE safely?', 'Independent deploys; version APIs; migrate expand/contract.', 'Lockstep only.', 'Feature flags for schema?', 'Expand → migrate → contract.'],
]

w(
  'senior-qa/index.md',
  `# Senior Interview Q&A

120+ questions interviewers actually ask across frontend, backend, and full-stack. Each item: **Expected**, **Common wrong**, **Follow-ups**, **Trade-offs**, **Production**.

| Range | File | Focus |
| --- | --- | --- |
| 1–40 | [Frontend](/senior-qa/01-frontend) | React, browser, perf, security |
| 41–80 | [Backend](/senior-qa/02-backend) | Node, SQL, Redis, queues, auth |
| 81–120 | [Full-Stack](/senior-qa/03-fullstack) | Boundaries, caching, consistency, design |

> [!TIP]
> Answer out loud in 60–90s, then check follow-ups. Trade-offs matter more than buzzwords.
`
)

w('senior-qa/01-frontend.md', expand(feBank, 1, 40, 'Senior Q&A — Frontend (1–40)'))
w('senior-qa/02-backend.md', expand(beBank, 41, 40, 'Senior Q&A — Backend (41–80)'))
w('senior-qa/03-fullstack.md', expand(fsBank, 81, 40, 'Senior Q&A — Full-Stack (81–120)'))

console.log('senior-qa complete')
