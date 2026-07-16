# Senior Full-Stack Interview Handbook

Teach-from-scratch notes for **mid → senior** full-stack interviews — frontend *and* backend.

**Live site:** [prajjwaljogdand.github.io/FullstackPreparation](https://prajjwaljogdand.github.io/FullstackPreparation/)

Every chapter follows the same shape:

**concept → diagram → code → interview Q&A → common mistakes → trade-offs**

---

## What’s inside

| Track | Topics |
| --- | --- |
| **Frontend** | JavaScript internals (24 ch), Browser, TypeScript, React Fiber, Next.js App Router, FE system design, machine coding |
| **Backend** | Node/Express, APIs, SQL/NoSQL, Redis, queues, auth, ops, language-agnostic backend system design |
| **Shared** | Coding patterns + ~100 TypeScript problems, 100+ senior Q&A (FE / BE / full-stack) |

Built with [VitePress](https://vitepress.dev/) (Markdown + Mermaid + local search).

---

## Quick revise (few hours)

1. **Warm-up (30–45m)** — [Event Loop](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/10-event-loop) → [Closures](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/05-closures) → [TypeScript pitfalls](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/10-pitfalls)
2. **Role focus (60–90m)** — FE: [React Fiber](https://prajjwaljogdand.github.io/FullstackPreparation/react/01-fiber) + [Next caching](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/10-caching) · BE: [Node phases](https://prajjwaljogdand.github.io/FullstackPreparation/node/02-event-loop) + [Backend SD](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/)
3. **Drill (45m)** — [Coding](https://prajjwaljogdand.github.io/FullstackPreparation/coding/) + one [Machine Coding](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/) build
4. **Mock (30m)** — [Senior Q&A](https://prajjwaljogdand.github.io/FullstackPreparation/senior-qa/) — answer 10 out loud, then check follow-ups

---

## Chapters

Base URL: `https://prajjwaljogdand.github.io/FullstackPreparation`

<details>
<summary><strong>JavaScript Deep Dive</strong> (24)</summary>

1. [Fundamentals Revisited](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/01-fundamentals)
2. [Execution Context](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/02-execution-context)
3. [Scope & Lexical Environment](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/03-scope)
4. [Hoisting](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/04-hoisting)
5. [Closures](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/05-closures)
6. [this Keyword](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/06-this)
7. [Prototype Chain](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/07-prototype)
8. [Classes](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/08-classes)
9. [Functions](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/09-functions)
10. [Event Loop](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/10-event-loop)
11. [Asynchronous JS](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/11-async)
12. [Memory Management](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/12-memory)
13. [Modules](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/13-modules)
14. [Objects](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/14-objects)
15. [Arrays](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/15-arrays)
16. [Strings](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/16-strings)
17. [Numbers](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/17-numbers)
18. [Error Handling](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/18-errors)
19. [Browser APIs](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/19-browser-apis)
20. [Browser Rendering](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/20-rendering)
21. [Security](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/21-security)
22. [Performance](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/22-performance)
23. [Machine Coding Utils](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/23-machine-coding)
24. [150 Senior JS Q&A](https://prajjwaljogdand.github.io/FullstackPreparation/javascript/24-senior-js-qa)

Source: [`docs/javascript/`](docs/javascript/)

</details>

<details>
<summary><strong>Browser Internals</strong> (10)</summary>

1. [Architecture](https://prajjwaljogdand.github.io/FullstackPreparation/browser/01-architecture)
2. [Rendering Pipeline](https://prajjwaljogdand.github.io/FullstackPreparation/browser/02-rendering-pipeline)
3. [Event Loop](https://prajjwaljogdand.github.io/FullstackPreparation/browser/03-event-loop)
4. [CSS Internals](https://prajjwaljogdand.github.io/FullstackPreparation/browser/04-css-internals)
5. [Networking](https://prajjwaljogdand.github.io/FullstackPreparation/browser/05-networking)
6. [Security](https://prajjwaljogdand.github.io/FullstackPreparation/browser/06-security)
7. [Memory & GC](https://prajjwaljogdand.github.io/FullstackPreparation/browser/07-memory-gc)
8. [Storage](https://prajjwaljogdand.github.io/FullstackPreparation/browser/08-storage)
9. [Rendering Optimization](https://prajjwaljogdand.github.io/FullstackPreparation/browser/09-optimization)
10. [Interview Q&A](https://prajjwaljogdand.github.io/FullstackPreparation/browser/10-interview-qa)

Source: [`docs/browser/`](docs/browser/)

</details>

<details>
<summary><strong>TypeScript</strong> (11)</summary>

1. [Type System Internals](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/01-type-system)
2. [Generics](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/02-generics)
3. [Conditional Types](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/03-conditional-types)
4. [Infer](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/04-infer)
5. [Utility Types](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/05-utility-types)
6. [Declaration Merging](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/06-declaration-merging)
7. [Module Resolution](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/07-module-resolution)
8. [Structural Typing](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/08-structural-typing)
9. [Variance](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/09-variance)
10. [Common Pitfalls](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/10-pitfalls)
11. [Advanced Interview Q&A](https://prajjwaljogdand.github.io/FullstackPreparation/typescript/11-interview-qa)

Source: [`docs/typescript/`](docs/typescript/)

</details>

<details>
<summary><strong>React Internals</strong> (12)</summary>

1. [Fiber Architecture](https://prajjwaljogdand.github.io/FullstackPreparation/react/01-fiber)
2. [Reconciliation](https://prajjwaljogdand.github.io/FullstackPreparation/react/02-reconciliation)
3. [Hooks Implementation](https://prajjwaljogdand.github.io/FullstackPreparation/react/03-hooks)
4. [Concurrent Rendering](https://prajjwaljogdand.github.io/FullstackPreparation/react/04-concurrent)
5. [Suspense](https://prajjwaljogdand.github.io/FullstackPreparation/react/05-suspense)
6. [React Query Internals](https://prajjwaljogdand.github.io/FullstackPreparation/react/06-react-query)
7. [Context vs Redux](https://prajjwaljogdand.github.io/FullstackPreparation/react/07-context-redux)
8. [Rendering Optimization](https://prajjwaljogdand.github.io/FullstackPreparation/react/08-optimization)
9. [Memoization](https://prajjwaljogdand.github.io/FullstackPreparation/react/09-memoization)
10. [Server Components](https://prajjwaljogdand.github.io/FullstackPreparation/react/10-rsc)
11. [React Compiler](https://prajjwaljogdand.github.io/FullstackPreparation/react/11-compiler)
12. [Interview Q&A](https://prajjwaljogdand.github.io/FullstackPreparation/react/12-interview-qa)

Source: [`docs/react/`](docs/react/)

</details>

<details>
<summary><strong>Next.js</strong> (14)</summary>

1. [App Router](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/01-app-router)
2. [RSC](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/02-rsc)
3. [SSR](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/03-ssr)
4. [ISR](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/04-isr)
5. [SSG](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/05-ssg)
6. [Hydration](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/06-hydration)
7. [Streaming](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/07-streaming)
8. [Route Handlers](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/08-route-handlers)
9. [Middleware](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/09-middleware)
10. [Caching](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/10-caching)
11. [Server Actions](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/11-server-actions)
12. [Authentication](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/12-authentication)
13. [Deployment](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/13-deployment)
14. [Interview Q&A](https://prajjwaljogdand.github.io/FullstackPreparation/nextjs/14-interview-qa)

Source: [`docs/nextjs/`](docs/nextjs/)

</details>

<details>
<summary><strong>Node.js + Express</strong> (14)</summary>

1. [libuv](https://prajjwaljogdand.github.io/FullstackPreparation/node/01-libuv)
2. [Event Loop Phases](https://prajjwaljogdand.github.io/FullstackPreparation/node/02-event-loop)
3. [Streams](https://prajjwaljogdand.github.io/FullstackPreparation/node/03-streams)
4. [Buffers](https://prajjwaljogdand.github.io/FullstackPreparation/node/04-buffers)
5. [Cluster](https://prajjwaljogdand.github.io/FullstackPreparation/node/05-cluster)
6. [Worker Threads](https://prajjwaljogdand.github.io/FullstackPreparation/node/06-worker-threads)
7. [V8](https://prajjwaljogdand.github.io/FullstackPreparation/node/07-v8)
8. [JWT & Auth](https://prajjwaljogdand.github.io/FullstackPreparation/node/08-jwt-auth)
9. [Middleware Internals](https://prajjwaljogdand.github.io/FullstackPreparation/node/09-middleware)
10. [Scaling](https://prajjwaljogdand.github.io/FullstackPreparation/node/10-scaling)
11. [Performance](https://prajjwaljogdand.github.io/FullstackPreparation/node/11-performance)
12. [Security](https://prajjwaljogdand.github.io/FullstackPreparation/node/12-security)
13. [Production Architecture](https://prajjwaljogdand.github.io/FullstackPreparation/node/13-production)
14. [Interview Q&A](https://prajjwaljogdand.github.io/FullstackPreparation/node/14-interview-qa)

Source: [`docs/node/`](docs/node/)

</details>

<details>
<summary><strong>Backend Engineering</strong> (11)</summary>

1. [API Design](https://prajjwaljogdand.github.io/FullstackPreparation/backend/01-api-design)
2. [SQL & Indexes](https://prajjwaljogdand.github.io/FullstackPreparation/backend/02-sql)
3. [NoSQL Trade-offs](https://prajjwaljogdand.github.io/FullstackPreparation/backend/03-nosql)
4. [ORM vs Query Builder](https://prajjwaljogdand.github.io/FullstackPreparation/backend/04-orm)
5. [Redis Caching](https://prajjwaljogdand.github.io/FullstackPreparation/backend/05-redis)
6. [Queues & Messaging](https://prajjwaljogdand.github.io/FullstackPreparation/backend/06-queues)
7. [Auth at Scale](https://prajjwaljogdand.github.io/FullstackPreparation/backend/07-auth)
8. [Rate Limit & Idempotency](https://prajjwaljogdand.github.io/FullstackPreparation/backend/08-rate-limit)
9. [Observability](https://prajjwaljogdand.github.io/FullstackPreparation/backend/09-observability)
10. [Deployment & Ops](https://prajjwaljogdand.github.io/FullstackPreparation/backend/10-ops)
11. [Interview Q&A](https://prajjwaljogdand.github.io/FullstackPreparation/backend/11-interview-qa)

Source: [`docs/backend/`](docs/backend/)

</details>

<details>
<summary><strong>Backend System Design</strong> (12)</summary>

1. [Overview](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/)
2. [URL Shortener](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/01-url-shortener)
3. [News Feed](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/02-news-feed)
4. [Chat / Messaging](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/03-chat)
5. [Rate Limiter](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/04-rate-limiter)
6. [Notification System](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/05-notifications)
7. [File Upload / CDN](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/06-file-cdn)
8. [Search Autocomplete](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/07-autocomplete)
9. [Job Queue](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/08-job-queue)
10. [Multi-tenant SaaS API](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/09-saas-api)
11. [Auth Service](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/10-auth-service)
12. [Cache Layer](https://prajjwaljogdand.github.io/FullstackPreparation/backend-system-design/11-cache-layer)

Source: [`docs/backend-system-design/`](docs/backend-system-design/)

</details>

<details>
<summary><strong>Frontend System Design</strong> (8)</summary>

1. [Overview](https://prajjwaljogdand.github.io/FullstackPreparation/frontend-system-design/)
2. [News Feed UI](https://prajjwaljogdand.github.io/FullstackPreparation/frontend-system-design/01-feed)
3. [Autocomplete](https://prajjwaljogdand.github.io/FullstackPreparation/frontend-system-design/02-autocomplete)
4. [Chat UI](https://prajjwaljogdand.github.io/FullstackPreparation/frontend-system-design/03-chat)
5. [Design System](https://prajjwaljogdand.github.io/FullstackPreparation/frontend-system-design/04-design-system)
6. [Image Gallery](https://prajjwaljogdand.github.io/FullstackPreparation/frontend-system-design/05-image-gallery)
7. [Dashboard / Analytics](https://prajjwaljogdand.github.io/FullstackPreparation/frontend-system-design/06-dashboard)
8. [Observability (FE)](https://prajjwaljogdand.github.io/FullstackPreparation/frontend-system-design/07-observability)

Source: [`docs/frontend-system-design/`](docs/frontend-system-design/)

</details>

<details>
<summary><strong>Coding Interview</strong> (15)</summary>

1. [Overview & Patterns](https://prajjwaljogdand.github.io/FullstackPreparation/coding/)
2. [Debounce / Throttle](https://prajjwaljogdand.github.io/FullstackPreparation/coding/01-debounce-throttle)
3. [Promise from Scratch](https://prajjwaljogdand.github.io/FullstackPreparation/coding/02-promise)
4. [EventEmitter](https://prajjwaljogdand.github.io/FullstackPreparation/coding/03-event-emitter)
5. [Deep Clone](https://prajjwaljogdand.github.io/FullstackPreparation/coding/04-deep-clone)
6. [LRU Cache](https://prajjwaljogdand.github.io/FullstackPreparation/coding/05-lru)
7. [Flatten / Trie](https://prajjwaljogdand.github.io/FullstackPreparation/coding/06-flatten-trie)
8. [Binary Search](https://prajjwaljogdand.github.io/FullstackPreparation/coding/07-binary-search)
9. [Sliding Window](https://prajjwaljogdand.github.io/FullstackPreparation/coding/08-sliding-window)
10. [Graphs](https://prajjwaljogdand.github.io/FullstackPreparation/coding/09-graphs)
11. [Dynamic Programming](https://prajjwaljogdand.github.io/FullstackPreparation/coding/10-dp)
12. [Problems 1–25](https://prajjwaljogdand.github.io/FullstackPreparation/coding/11-problems-01-25)
13. [Problems 26–50](https://prajjwaljogdand.github.io/FullstackPreparation/coding/12-problems-26-50)
14. [Problems 51–75](https://prajjwaljogdand.github.io/FullstackPreparation/coding/13-problems-51-75)
15. [Problems 76–100](https://prajjwaljogdand.github.io/FullstackPreparation/coding/14-problems-76-100)

Source: [`docs/coding/`](docs/coding/)

</details>

<details>
<summary><strong>Senior Interview Q&A</strong> (4)</summary>

1. [Overview](https://prajjwaljogdand.github.io/FullstackPreparation/senior-qa/)
2. [Frontend (1–40)](https://prajjwaljogdand.github.io/FullstackPreparation/senior-qa/01-frontend)
3. [Backend (41–80)](https://prajjwaljogdand.github.io/FullstackPreparation/senior-qa/02-backend)
4. [Full-Stack (81–120)](https://prajjwaljogdand.github.io/FullstackPreparation/senior-qa/03-fullstack)

Source: [`docs/senior-qa/`](docs/senior-qa/)

</details>

<details>
<summary><strong>Frontend Machine Coding</strong> (9)</summary>

1. [Overview](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/)
2. [Build React Query](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/01-react-query)
3. [Build Redux](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/02-redux)
4. [Infinite Scroll](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/03-infinite-scroll)
5. [Virtual List](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/04-virtual-list)
6. [Drag & Drop](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/05-drag-drop)
7. [File Upload](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/06-file-upload)
8. [Chat UI](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/07-chat-ui)
9. [Optimized Table](https://prajjwaljogdand.github.io/FullstackPreparation/machine-coding/08-optimized-table)

Source: [`docs/machine-coding/`](docs/machine-coding/)

</details>

---

## Repo layout

```
docs/
  javascript/   browser/   typescript/   react/   nextjs/
  node/   backend/   backend-system-design/   frontend-system-design/
  coding/   senior-qa/   machine-coding/
  .vitepress/config.ts
```

---

## Run locally

```bash
npm install
npm run dev       # http://localhost:5173/FullstackPreparation/
npm run build
npm run preview
```

> The site uses `base: '/FullstackPreparation/'` so local and GitHub Pages URLs match the repo name.

---

## Deploy (GitHub Pages)

Deploys automatically on push to `main` via [`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml).

**One-time:** repo **Settings → Pages → Source → GitHub Actions**.

If you rename the repo, update `base` in [`docs/.vitepress/config.ts`](docs/.vitepress/config.ts):

```ts
base: '/YourRepoName/',
```

---

## Contributing

- Prefer **teach-from-scratch** prose over revision-only bullet dumps  
- Keep the chapter template (concept → diagram → code → Q&A → mistakes → trade-offs)  
- Run `npm run build` before PRs — VitePress fails the build on dead links  

---

## License

Personal interview prep material. Use and adapt as you like; no warranty.
