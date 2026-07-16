# Browser Interview Q&A

This chapter is a **teaching** bank of browser interview questions — not one-line flashcards. Each answer explains the idea so you could re-derive it. Use it after (or alongside) the topical chapters: [Architecture](/browser/01-architecture), [Rendering](/browser/02-rendering-pipeline), [Event Loop](/browser/03-event-loop), [CSS Internals](/browser/04-css-internals), [Networking](/browser/05-networking), [Security](/browser/06-security), [Memory](/browser/07-memory-gc), [Storage](/browser/08-storage), [Optimization](/browser/09-optimization).

For every question:

- **Expected** — what a strong answer sounds like (paragraph)
- **Common wrong** — frequent mix-ups
- **Follow-ups** — how interviewers dig
- **Production** — what teams actually do

---

## A. Origins, windows, and the browser as a platform

### Q1. What is a browsing context?
**Expected:** A browsing context is an environment that displays a document — roughly a tab, window, or iframe. Each has its own `Window`, history, and document. Iframes are nested browsing contexts: the child has its own window/document but is embedded in a parent page. Understanding this matters because script, navigation, and storage rules are tied to which context and origin you are in — not merely “the browser.”  
**Common wrong:** “It’s just another name for a tab.” (Misses iframes and nested contexts.)  
**Follow-ups:** How does `window.parent` / `window.top` relate? What is a cross-origin iframe allowed to do?  
**Production:** Third-party widgets often run in iframes to isolate CSS/JS; postMessage is how you talk across origins safely.

### Q2. What is an origin, precisely?
**Expected:** An origin is the tuple of **scheme**, **host**, and **port**. `https://example.com` and `http://example.com` differ. `https://a.example.com` and `https://b.example.com` differ. Default ports (443/80) are implied, so `https://example.com` and `https://example.com:443` are the same origin. The browser uses origins as the primary isolation key for DOM access, storage APIs, and many permissions.  
**Common wrong:** “Origin means domain name.”  
**Follow-ups:** Same-site vs same-origin? Why does that matter for `SameSite` cookies?  
**Production:** Split frontends (`app.` vs `api.`) force CORS and cookie-domain design early — document it.

### Q3. What does the Same-Origin Policy actually restrict?
**Expected:** SOP is the browser’s default rule that script from one origin cannot freely **read** another origin’s document, storage, or (without CORS) response bodies. It is why an evil site cannot open your bank in a hidden iframe and scrape the DOM. SOP does **not** block all cross-origin network activity: you can often send requests, load images/scripts, and navigate. CSRF and script-based XSS sit in those gaps.  
**Common wrong:** “SOP blocks every cross-origin request.”  
**Follow-ups:** Why can `<script src="https://other.com/x.js">` run? Whose privileges does it get?  
**Production:** Treat SOP as isolation, not a complete application security program — still authenticate on the server.

### Q4. How do tabs relate to processes (high level)?
**Expected:** Modern browsers use multi-process architectures: typically a browser process plus one or more **renderer** processes for page content, plus GPU/network utility processes. Sites are often isolated into different renderer processes (site isolation) so a compromise in one page is harder to turn into a full browser compromise. From an app developer’s view: your JS runs in a renderer; crashing that tab need not kill the whole browser. Exact process maps vary by browser and memory pressure.  
**Common wrong:** “Each tab is always exactly one OS process forever, guaranteed.”  
**Follow-ups:** What is site isolation trying to prevent?  
**Production:** Heavy pages still hurt — memory limits; don’t assume infinite renderer memory on mobile.

### Q5. `window` vs `document` — what’s the difference?
**Expected:** `window` is the global object for the browsing context (timers, location, fetch, storage accessors, etc.). `document` is the DOM Document loaded in that window — the tree of nodes you query and mutate. `window.document === document`. Many “browser APIs” hang off `window`; DOM APIs hang off `document` / nodes.  
**Common wrong:** Treating them as interchangeable names.  
**Follow-ups:** What is `window.self` vs `window.top`?  
**Production:** In SSR, `window`/`document` are missing — gate browser APIs behind effects or `typeof window` checks carefully.

---

## B. Parsing, rendering, and layout

### Q6. Walk through HTML → pixels at a high level.
**Expected:** The browser downloads HTML and builds a **DOM**. It downloads CSS and builds a **CSSOM**. They combine into a **render tree** of visible content. **Layout** assigns geometry (boxes). **Paint** records drawing commands (text, colors, images). **Compositing** layers those outputs onto the screen, often using the GPU. JavaScript can mutate DOM/CSS at any time and force parts of this pipeline to re-run. Performance work is often about reducing how often and how much of that pipeline you invalidate.  
**Common wrong:** “The browser just shows HTML; CSS is cosmetic only.”  
**Follow-ups:** Where does JavaScript fit if a sync script appears mid-HTML?  
**Production:** Critical CSS and deferring JS are levers on this path — measure LCP before micro-tuning paint.

### Q7. What is reflow (layout) vs repaint?
**Expected:** **Layout/reflow** recalculates geometric information — sizes and positions. Changing document flow (width, height, adding/removing elements in flow, some font changes) triggers it. **Repaint** updates pixels for visual properties that don’t necessarily change layout (e.g. color). Layout is typically more expensive and can cascade to children. Animating geometric properties every frame is a common jank source; transforming a layer can be cheaper.  
**Common wrong:** Using the words interchangeably.  
**Follow-ups:** Give an example API read that forces layout.  
**Production:** In scroll/resize handlers, batch DOM reads/writes; avoid layout thrash loops.

### Q8. What is the render-blocking nature of CSS?
**Expected:** Browsers generally avoid painting unstyled content for stylesheets that apply to the page, because FOUC (flash of unstyled content) is worse UX. A CSS file in the critical path can delay first paint until it is fetched and processed (with nuances around media attributes). That is why huge CSS bundles or slow CDN CSS hurt perceived performance even when HTML arrived quickly.  
**Common wrong:** “CSS never affects load performance.”  
**Follow-ups:** How can `media` attributes help? What about critical CSS inlining?  
**Production:** Split critical vs deferred CSS; audit unused rules with Coverage.

### Q9. Why do sync scripts block HTML parsing?
**Expected:** When the parser hits `<script src>` without `async`/`defer` (and not `type="module"`), it must download and execute the script before continuing to parse the rest of the HTML — because classic scripts can document.write and assume a specific parse state. That stalls DOM construction and often delays first paint. `defer` downloads in parallel and runs after parse; modules defer by default. `async` runs when ready, unordered relative to DOM completion.  
**Common wrong:** “All scripts are non-blocking now.”  
**Follow-ups:** Difference between `async` and `defer`?  
**Production:** Prefer modules/`defer` for app code; reserve carefully ordered classic scripts only when required.

### Q10. What is compositing and why do people animate `transform`?
**Expected:** Compositing combines painted layers into the final frame. If an element can be promoted to its own layer, changing `transform`/`opacity` can often be handled without re-laying out or repainting the whole document each frame — the compositor updates. Animating `top`/`left`/`width` usually forces more expensive work. This is a guideline with exceptions; over-promoting layers costs memory.  
**Common wrong:** “`transform` is free, always.”  
**Follow-ups:** What does `will-change` do and when does it hurt?  
**Production:** Profile janky animations in Performance panel; verify paint rectangles.

### Q11. What causes Cumulative Layout Shift (CLS)?
**Expected:** CLS measures unexpected movement of visible content. Common causes: images/ads/embeds without reserved size, web fonts swapping to different metrics, late-injected banners, and asynchronous content pushing layout. Fix by reserving space (width/height or aspect-ratio), matching font metrics, and avoiding inserting above existing content without space.  
**Common wrong:** “CLS is just slow LCP.”  
**Follow-ups:** How do late fonts contribute?  
**Production:** Track CLS in RUM; screenshot labs miss some real-user shifts.

---

## C. Event loop, tasks, and rendering timing

### Q12. Explain the browser event loop in plain language.
**Expected:** The browser runs a loop that picks **tasks** (macrotasks) from queues — things like event handlers, `setTimeout` callbacks, I/O completions — runs them one at a time on the main thread, and between tasks may update rendering if needed. **Microtasks** (promise jobs, `queueMicrotask`) run after the current task finishes, before rendering/other tasks. Long tasks delay everything else, including input and paint. This is why a tight CPU loop freezes the UI.  
**Common wrong:** “Promises are multithreaded.”  
**Follow-ups:** Order: `setTimeout(0)` vs `Promise.resolve().then`?  
**Production:** Keep handlers short; chunk work; use workers for heavy CPU.

### Q13. Microtasks vs macrotasks — teach with an example.
**Expected:** After a task completes, the engine drains the **microtask** queue completely before leaving to the next macrotask or render opportunity. So:

```js
setTimeout(() => console.log("timeout"), 0)
Promise.resolve().then(() => console.log("promise"))
console.log("sync")
// sync, promise, timeout
```

`sync` runs now; the promise microtask runs before the timeout task. Infinite microtask scheduling can starve rendering.  
**Common wrong:** Claiming timeouts always run before promises.  
**Follow-ups:** Where does `MutationObserver` land?  
**Production:** Don’t chain unbounded microtasks in hot paths.

### Q14. What is `requestAnimationFrame` for?
**Expected:** `rAF` schedules a callback before the next repaint, aligned to the display’s refresh when possible. Use it to update visual state so you read/write DOM in sync with frames instead of inventing your own timer cadence. It is not a general-purpose delay API — tab backgrounding may throttle it. For idle work, prefer `requestIdleCallback` (where available) or chunking.  
**Common wrong:** Using `rAF` as a substitute for `setInterval` for non-visual polling.  
**Follow-ups:** What happens to rAF in background tabs?  
**Production:** Animation loops must cancel on unmount (`cancelAnimationFrame`).

### Q15. Why can `setTimeout(fn, 0)` still feel delayed?
**Expected:** `0` means “as soon as the task queue allows,” not “preempt the current work.” The callback waits until the current task and queued microtasks finish, and browsers impose minimum delays and nesting clamps. If the main thread is busy with other tasks, your timeout waits. It also does not run *between* microtasks of the current turn.  
**Common wrong:** “`setTimeout(0)` is an accurate high-resolution timer.”  
**Follow-ups:** How does this interact with await breakpoints?  
**Production:** For UI yielding, prefer explicit chunking patterns / scheduler APIs where appropriate.

---

## D. Events and the DOM

### Q16. Capture vs bubble?
**Expected:** When an event travels through the DOM, it can go through a **capture** phase from the root down toward the target, then a **bubble** phase from the target back up (for bubbling events). `addEventListener(type, fn, true)` listens on capture; default is bubble. Most app code uses bubble. Understanding phases explains why a parent can see events before/after children and how `stopPropagation` cuts the trip short.  
**Common wrong:** “Events only ever go upward.”  
**Follow-ups:** Does `focus` bubble? What about `focusin`?  
**Production:** Prefer `stopPropagation` sparingly — it breaks unrelated listeners; often redesign instead.

### Q17. `preventDefault` vs `stopPropagation`?
**Expected:** `preventDefault` cancels the **browser’s default action** (e.g. navigating a link, submitting a form, checking a checkbox) if the event is cancelable. `stopPropagation` stops the event from reaching other listeners on other nodes in the path. They solve different problems; using one when you mean the other is a classic bug. Neither removes the element’s own other listeners on the same node unless you also stopImmediatePropagation.  
**Common wrong:** Equating them.  
**Follow-ups:** Why does `passive: true` on touch/wheel matter?  
**Production:** Passive scroll listeners improve scroll performance by promising you won’t cancel.

### Q18. Event delegation — why?
**Expected:** Instead of binding listeners to every child, bind one listener on a parent and use `event.target` (or `closest`) to see which child was interacted with. Benefits: fewer listeners, works for elements added later, lower memory. Costs: must carefully filter targets; logic can get clever. Delegation is how many large lists stay cheap.  
**Common wrong:** “Delegation is only an old jQuery pattern.”  
**Follow-ups:** How do you ignore clicks on nested interactive children?  
**Production:** Great for dynamic tables; still clean up the parent listener on unmount.

### Q19. What is a DocumentFragment useful for?
**Expected:** A DocumentFragment is a lightweight document piece you can build off-DOM and then insert into the document in one operation. Batching DOM insertions reduces intermediate layouts/reflows compared with appending nodes one-by-one into a live parent inside a tight loop (engines optimize some cases, but fragments remain a clear intent).  
**Common wrong:** Thinking fragments survive as nodes in the tree after insert (children move in; fragment empties).  
**Follow-ups:** How does virtual DOM relate philosophically?  
**Production:** Prefer framework list rendering; fragments still help in vanilla widgets.

---

## E. Networking and caching

### Q20. HTTP/1.1 vs HTTP/2 for frontends?
**Expected:** HTTP/1.1 historically suffered from few parallel connections per host and head-of-line blocking at the HTTP layer — hence domain sharding and bundling folklore. HTTP/2 multiplexes many streams over one connection, making many small requests less disastrous. HTTP/3/QUIC improves loss recovery further. You still care about **bytes**, **CPU parse cost**, and **critical path depth** — multiplexing does not make a 3MB JS file free.  
**Common wrong:** “HTTP/2 means we should never bundle.”  
**Follow-ups:** What is head-of-line blocking at TCP vs HTTP/2?  
**Production:** Still bundle/split thoughtfully; measure waterfalls on real networks.

### Q21. What do `Cache-Control` headers change for browsers?
**Expected:** They tell browsers (and intermediaries) whether a response can be stored and how long it can be reused without revalidation (`max-age`), whether it must revalidate (`no-cache` is subtler than “don’t store”), and whether it’s private vs public. Fingerprinted static assets often use long `max-age` + immutable. HTML entry documents often use short freshness or revalidation so users get new app shells. Misconfiguration causes sticky old bugs or unnecessary refetches.  
**Common wrong:** “`no-cache` means do not store at all” (that’s closer to `no-store`).  
**Follow-ups:** `ETag` vs `max-age`?  
**Production:** Separate caching policy for `index.html` vs hashed `/assets/*`.

### Q22. What is a service worker’s role in networking?
**Expected:** A service worker is a programmable network proxy for your origin (within scope): it can intercept `fetch` events and decide cache-first, network-first, stale-while-revalidate, etc., using the Cache API. It enables offline shells and faster repeat loads. It also adds complexity: update cycles, cache versioning, and subtle bugs when serving stale HTML/JS pairs.  
**Common wrong:** “Service worker is just a background thread for CPU.”  
**Follow-ups:** How do you invalidate caches on deploy?  
**Production:** Version cache names; never cache opaque error responses blindly.

### Q23. CORS preflight — when and why?
**Expected:** For cross-origin requests that are not “simple,” browsers send an `OPTIONS` preflight asking permission (methods/headers). The server responds with `Access-Control-Allow-*`. Only then does the browser proceed and expose the response to JS if allowed. Preflights protect servers from “silent” cross-origin authenticated requests shaped like classic form posts, within the CORS model. Non-browser clients are unaffected.  
**Common wrong:** “Preflight authenticates the user.”  
**Follow-ups:** Why does adding `Authorization` trigger preflight?  
**Production:** Minimize custom headers if you need to cut latency; cache preflights with `Access-Control-Max-Age`.

---

## F. Security

### Q24. Teach XSS in a paragraph.
**Expected:** Cross-site scripting means attacker-controlled script runs **with the privileges of your origin**. The attacker finds a way to get the browser to treat their bytes as your page’s JavaScript — via stored HTML, reflected URL parameters, or DOM sinks like `innerHTML` with `location` data. Once running, the script can read the DOM, call your APIs as the user, and exfiltrate non-HttpOnly secrets. Defense is context-aware escaping, safe sinks, sanitization when HTML is required, CSP, and reducing sensitive data exposure to JS.  
**Common wrong:** Confusing XSS with CSRF.  
**Follow-ups:** Stored vs reflected vs DOM-based examples?  
**Production:** Ban unsafe HTML sinks in code review; CSP with nonces in report-then-enforce rollout.

### Q25. Teach CSRF in a paragraph.
**Expected:** Cross-site request forgery tricks a victim’s browser into issuing a request to a site where the victim is already authenticated. The browser automatically attaches cookies (subject to SameSite), so the server performs a state-changing action the user did not intend. The attacker often does not need to read the response. Defenses include SameSite cookies, CSRF tokens the attacker cannot read cross-origin, preferring non-cookie auth headers for APIs, and re-authentication for sensitive actions.  
**Common wrong:** “CORS stops CSRF.”  
**Follow-ups:** Why doesn’t SOP prevent the request from being sent?  
**Production:** For cookie sessions, default `SameSite=Lax` + tokens for dangerous POST routes.

### Q26. How does CSP reduce XSS impact?
**Expected:** Content Security Policy tells the browser which script sources may run, and can ban inline scripts unless nonced/hashed. If an attacker injects `<script>…</script>` or an inline handler, a strict policy refuses execution. `connect-src` can limit exfiltration endpoints. CSP is defense-in-depth — it does not replace escaping — and a policy full of `'unsafe-inline'` is weak.  
**Common wrong:** “CSP means we can skip output encoding.”  
**Follow-ups:** Nonce vs hash? Report-Only mode?  
**Production:** Start Report-Only; fix violations; enforce; automate nonce plumbing in templates.

### Q27. What does `HttpOnly` on a cookie buy you?
**Expected:** It prevents JavaScript from reading that cookie via `document.cookie`, so a simple XSS exfiltration of the session id becomes harder. It does **not** stop XSS from making same-origin requests that automatically include the cookie — the attacker can still act as the user until the session ends. Pair with XSS prevention and short session lifetimes / rotation.  
**Common wrong:** “HttpOnly fixes XSS.”  
**Follow-ups:** `Secure` and `SameSite` roles?  
**Production:** Session cookies: `Secure; HttpOnly; SameSite=…; Path=/` as baseline.

### Q28. Is CORS a security boundary for your API?
**Expected:** CORS is enforced by browsers to control which **web pages** can read responses. Attackers using curl, Postman, or their own servers ignore CORS. Your API must still authenticate and authorize every request. Misconfigured `Access-Control-Allow-Origin: *` with credentials is invalid/problematic; reflecting arbitrary origins with credentials is dangerous.  
**Common wrong:** “We enabled CORS, so only our frontend can call us.”  
**Follow-ups:** Credentialed CORS requirements?  
**Production:** Allowlist exact frontend origins; test with a malicious page on another origin.

### Q29. Cookie session vs token in `localStorage` — trade-offs?
**Expected:** HttpOnly cookies are not readable by JS and participate in CSRF risk because browsers attach them automatically — mitigate with SameSite and/or CSRF tokens. Tokens in `localStorage` are not auto-attached, which avoids classic cookie CSRF, but any XSS can read and steal them easily, and they persist until cleared. Memory-only tokens reduce durable theft but complicate refresh. Choose explicitly; document threat model.  
**Common wrong:** “localStorage JWT is always best practice.”  
**Follow-ups:** How do SPAs on another API origin change the design?  
**Production:** Many first-party apps use cookie sessions with strict CSRF strategy; BFF patterns also appear.

---

## G. Storage

### Q30. When cookies vs `localStorage`?
**Expected:** Use cookies when the **server** must receive the value on ordinary HTTP requests (sessions, some SSR preferences). Use `localStorage` for origin-scoped client preferences that only JS needs, accepting sync API limits and XSS readability. Cookies are tiny (~4KB) and attribute-rich; `localStorage` is larger (~5MB) string KV and never auto-sent. Putting large JSON in cookies wastes bandwidth on every request.  
**Common wrong:** Storing big app state in cookies.  
**Follow-ups:** Who can read each under XSS?  
**Production:** Prefer cookies for session ids; Web Storage for theme/locale flags.

### Q31. `localStorage` vs `sessionStorage`?
**Expected:** Both are synchronous string key/value maps per origin. `localStorage` persists across browser restarts until cleared. `sessionStorage` is scoped to a tab/session: reload keeps it; a new tab typically starts empty (with nuances around duplication). Use session for ephemeral per-tab flows (wizards); local for durable UI prefs.  
**Common wrong:** “sessionStorage clears on every reload.”  
**Follow-ups:** Does the `storage` event fire across tabs for both?  
**Production:** Don’t store secrets; wrap JSON parse in try/catch; handle quota errors.

### Q32. Why IndexedDB over Web Storage for large data?
**Expected:** IndexedDB is asynchronous, transactional, and built for structured/binary data with much larger quotas. Web Storage is synchronous and string-only — multi-megabyte `getItem` blocks the main thread and hits small quotas. Offline editors, caches of entities, and file drafts belong in IndexedDB (often via a wrapper library).  
**Common wrong:** “IndexedDB is just async localStorage.”  
**Follow-ups:** What happens in `onupgradeneeded`?  
**Production:** Plan schema versions/migrations; handle quota; don’t block UI when decoding huge results.

### Q33. What is the Cache API for?
**Expected:** It stores HTTP `Request`/`Response` pairs, primarily so service workers can serve offline/fast responses. It is not a general document database — use IndexedDB for mutable app entities. Version your caches (`static-v3`) and delete old ones on activate so deploys don’t strand users on stale shells.  
**Common wrong:** Using Cache API as the only store for user notes.  
**Follow-ups:** Cache-first vs network-first trade-offs?  
**Production:** Never cache personalized authenticated responses as if they were public static assets without care.

### Q34. What is storage partitioning?
**Expected:** Browsers increasingly key embedded third-party storage not only by the embed’s origin but also by the top-level site, so a tracker iframe cannot reuse one shared storage jar across unrelated sites as a stable cross-site id. Combined with third-party cookie restrictions, this reshapes advertising and embedded auth designs toward first-party flows.  
**Common wrong:** Ignoring it when designing cross-site widgets.  
**Follow-ups:** How do first-party sets / related website sets enter the chat (high level)?  
**Production:** Assume third-party cookies/storage are unreliable; prefer first-party implementations.

---

## H. Memory and GC

### Q35. How does garbage collection decide what to free?
**Expected:** Engines keep objects that are **reachable from roots** (stack, globals, and other runtime roots). Mark-and-sweep style collection marks the reachable graph, then reclaims unmarked objects. You don’t free memory by “finishing a function” alone if something still references your objects — listeners, arrays, maps, detached DOM wrappers, etc.  
**Common wrong:** “JS reference-counts everything and never has cycles issues” (historical; modern GC handles cycles).  
**Follow-ups:** What is a detached DOM node?  
**Production:** Profile SPAs with heap snapshots after open/close cycles.

### Q36. Why do event listeners leak?
**Expected:** A listener function registered on a long-lived target (`window`, `document`, a parent) stays reachable. Its closure keeps captured variables alive — including large data and DOM nodes. If a component unmounts without `removeEventListener` / framework cleanup, memory ratchets up as users navigate. Observers and intervals have the same shape.  
**Common wrong:** “Removing a DOM node always drops its listeners and everything they capture instantly in all cases.” (Detached but JS-referenced nodes still leak.)  
**Follow-ups:** Show a cleanup pattern.  
**Production:** Enforce effect cleanups; destroy third-party widgets explicitly.

### Q37. What is a detached DOM node leak?
**Expected:** The node is no longer in the document tree, but JavaScript still holds a reference (array, map, closure, React ref store). GC cannot reclaim it; the node may retain a large subtree and listeners. Symptoms: DOM node counts climb after repeated open/close UI. Fix by dropping references and disconnecting listeners/observers.  
**Common wrong:** Calling any `createElement` result “detached leak.”  
**Follow-ups:** How do you find them in DevTools?  
**Production:** Compare heap snapshots; search for “Detached HTML…” retainers.

### Q38. Is a growing heap always a leak?
**Expected:** No. Caches grow by design, users open more documents, and heaps spike before GC. A leak is **unintended** retention after the logical lifetime ended — e.g. after closing a modal, memory never returns near baseline across many cycles. Distinguish with snapshots and clear reproduction steps.  
**Common wrong:** Panic at every GC sawtooth.  
**Follow-ups:** Retained size vs shallow size?  
**Production:** Bound caches (LRU); virtualize large lists.

---

## I. Performance optimization

### Q39. What does “measure first” mean in practice?
**Expected:** Identify whether slowness is network (waterfall, TTFB, weight), main-thread JS (long tasks), rendering (layout/paint), or layout shift. Use field Web Vitals when possible and lab tools to dig. Only then apply the matching fix — code splitting won’t heal an uncompressed 5MB hero image, and compressing images won’t heal a 300ms click handler. Remeasure after changes.  
**Common wrong:** Applying a generic checklist blindly.  
**Follow-ups:** Lab vs field differences?  
**Production:** Performance budgets in CI; RUM dashboards for LCP/INP/CLS.

### Q40. What is the critical rendering path?
**Expected:** The sequence of dependencies required to paint meaningful pixels: fetch/parse HTML → DOM; fetch/parse CSS → CSSOM; render tree → layout → paint → composite, with JS potentially blocking along the way. Optimizing CRP means shortening or parallelizing those dependencies for above-the-fold content — less blocking CSS/JS, faster TTFB, prioritized hero assets.  
**Common wrong:** Equating it only with “minify everything.”  
**Follow-ups:** Role of `preload` / `preconnect`?  
**Production:** Don’t preload the world — contend for bandwidth wisely.

### Q41. Explain layout thrashing.
**Expected:** Alternating DOM writes that invalidate layout with reads of geometry (`offsetHeight`, `getBoundingClientRect`, etc.) forces the browser to recalculate layout repeatedly in a loop. Batch reads together and writes together (or use rAF scheduling) to let the browser layout once. This is a classic scroll-jank bug in vanilla code.  
**Common wrong:** “Any DOM read is thrashing.”  
**Follow-ups:** Write a before/after snippet.  
**Production:** Avoid geometry reads inside tight animations without batching.

### Q42. How does code splitting improve UX?
**Expected:** You ship less JavaScript for the initial route, so download/parse/compile cost drops and interaction becomes possible sooner. Features load via dynamic `import()` when needed. Trade-off: first visit to a heavy route pays a fetch latency — mitigate with prefetch on intent and good loading UI. Splitting does not shrink work you still must do on that route.  
**Common wrong:** Split every function into its own chunk.  
**Follow-ups:** How do bundlers form chunks?  
**Production:** Route-level splits + analyzer to catch accidental giant shared vendors.

### Q43. Why can lazy-loading images hurt LCP?
**Expected:** LCP often is the largest above-the-fold image. `loading="lazy"` delays loading until near viewport heuristics fire, which can postpone the hero. Lazy-load **offscreen** media; eager-load/preload the LCP candidate and include dimensions to avoid CLS.  
**Common wrong:** “lazy on all images is always best practice.”  
**Follow-ups:** How do `srcset`/`sizes` help LCP bytes?  
**Production:** Explicitly mark hero images in templates; test on mobile throttling.

### Q44. How do fonts affect performance metrics?
**Expected:** Font files are extra network bytes on the critical text path. `font-display: swap` shows fallback text quickly but may shift layout when the webfont metrics differ (CLS). `optional` can avoid late swaps on slow networks. Subsetting and preloading critical woff2 reduce delay. Invisible text periods hurt perceived performance even when “LCP element” is something else.  
**Common wrong:** Ignoring fonts after optimizing images.  
**Follow-ups:** Why does font preload need `crossorigin`?  
**Production:** Self-host fonts; match fallback metrics where possible.

### Q45. Transform/opacity vs top/left for animation?
**Expected:** Changing `top`/`left`/`width`/`height` typically triggers layout and more painting. `transform` and `opacity` can often be composited, keeping animation on a cheaper path when layers are set up well. Prefer them for UI motion; still verify with profilers because filters/shadows and excessive layers change the story.  
**Common wrong:** Spraying `will-change: transform` on everything.  
**Follow-ups:** Memory cost of layer promotion?  
**Production:** Motion design systems standardize on transform-based tokens.

---

## J. CSS / layout mental models (interview classics)

### Q46. What is the difference between block and inline formatting?
**Expected:** Block-level boxes typically stack vertically and take available width (subject to CSS). Inline boxes flow horizontally within lines, wrapping text. `inline-block` mixes: flows like inline but can have width/height like block. Modern layout often uses flex/grid for UI structure; understanding inline vs block still explains text and unexpected whitespace gaps.  
**Common wrong:** “Everything is flex now so this doesn’t matter.”  
**Follow-ups:** Why do spaces between inline-blocks create gaps?  
**Production:** Prefer flex/grid for app chrome; keep inline for text semantics.

### Q47. Content-box vs border-box?
**Expected:** In `content-box` (default historically), `width` applies to content; padding and border add outside it. In `border-box`, `width` includes padding and border, which makes grid/UI math predictable. Most design systems set `box-sizing: border-box` globally.  
**Common wrong:** Guessing which is default without saying.  
**Follow-ups:** How do `min-width: auto` flex items surprise people?  
**Production:** Global border-box reset is standard.

### Q48. What does `position: absolute` position against?
**Expected:** Absolute positioning is relative to the nearest **positioned** ancestor (not `static`) — the containing block formed by that ancestor — or the initial containing block if none. It is removed from normal flow, so siblings layout as if it weren’t there. `fixed` is typically viewport-related (with transform-containing ancestors creating gotchas).  
**Common wrong:** “Always relative to the parent element.”  
**Follow-ups:** How does a `transform` on a parent affect `fixed`?  
**Production:** Document stacking contexts when building overlays/modals.

### Q49. What is a stacking context?
**Expected:** A stacking context is a local z-ordering layer. Certain properties create one (`opacity < 1`, `transform`, `position` + `z-index`, etc.). Children’ `z-index` values compete inside that context and cannot interleave arbitrarily with outside content. This is why a modal inside a transformed parent may fail to overlay the whole page as expected.  
**Common wrong:** “Higher z-index always wins globally.”  
**Follow-ups:** Name three ways to create a stacking context.  
**Production:** Keep overlays at predictable roots (e.g. portal to `document.body`).

---

## K. Cross-cutting / scenario questions

### Q50. A button click feels delayed — how do you debug?
**Expected:** Reproduce with Performance panel: is the click handler a long task? Is there forced layout inside? Is the main thread busy with unrelated JS? Is a network call awaited before UI feedback? Fix by providing immediate UI feedback, moving heavy work off-thread or chunking, and separating network from paint. Check INP in field data if available.  
**Common wrong:** Jumping straight to “add memo.”  
**Follow-ups:** How would a worker help or not help DOM updates?  
**Production:** Always show pending states; avoid sync JSON parse of megabytes on click.

### Q51. First contentful paint is fine but the page isn’t usable — why?
**Expected:** Paint can show a shell or text while hydration/large JS still runs, blocking interaction. Or visuals appear while critical data fetches pending. Distinguish LCP/FCP from Time to Interactive / INP. Fixes: less client JS, progressive enhancement, defer non-critical hydration, skeleton states that match final layout (CLS).  
**Common wrong:** Only optimizing images when JS owns the bottleneck.  
**Follow-ups:** How do SSR + hydration costs show in profiles?  
**Production:** Islands/partial hydration architectures exist for this reason.

### Q52. How would you design offline support for a reading app?
**Expected:** Cache API + service worker for app shell and static assets; IndexedDB for articles/user progress; clear versioning and sync conflict strategy when back online; quota error UX; don’t store secrets durable client-side carelessly. Prefer network-first for freshness-sensitive feeds with cache fallback, cache-first for immutable article snapshots.  
**Common wrong:** “Just put everything in localStorage.”  
**Follow-ups:** How do you migrate IndexedDB schemas?  
**Production:** Background sync / periodic sync where available; always keep server authority.

### Q53. Third-party script on your page — risks and mitigations?
**Expected:** Third-party JS runs with your origin’s privileges — full XSS-equivalent trust. Risks: performance (main thread, bytes), privacy, supply-chain compromise, CSP complexity. Mitigate: load sparingly, `async`/`defer`, sandbox via iframe when possible, SRI (subresource integrity) for static CDNs, strict CSP, vendor review, self-host when feasible.  
**Common wrong:** “It’s fine, it’s only analytics.”  
**Follow-ups:** What does SRI not protect against?  
**Production:** Tag managers multiply risk — gate behind consent and least privilege.

### Q54. Explain clickjacking and a defense.
**Expected:** Clickjacking UI-redresses your site in a transparent iframe so users click actions they don’t see. Defenses: `Content-Security-Policy: frame-ancestors` (or legacy `X-Frame-Options`) to control who may embed you; for sensitive actions, require reconfirmation.  
**Common wrong:** Only mentioning CAPTCHA.  
**Follow-ups:** Why CSP `frame-ancestors` vs `X-Frame-Options`?  
**Production:** Default deny embedding except known partners.

### Q55. How do iframes change the security story?
**Expected:** Cross-origin iframes are SOP-isolated: parent can’t read child DOM and vice versa. Communication uses `postMessage` with explicit origin checks. Cookies/storage for the iframe origin follow cookie rules and increasingly partitioning by top-level site. Sandbox attribute can strip privileges from framed content.  
**Common wrong:** Assuming parent JS can always reach into any iframe.  
**Follow-ups:** What should you verify on `message` events?  
**Production:** Always check `event.origin`; don’t use `*`; sandbox third-party embeds.

---

## L. Quick fire teaching extras

### Q56. What is `defer` vs `async` on classic scripts?
**Expected:** Both download without blocking HTML parse the same way sync scripts do. `defer` preserves order and runs after document parsing completes. `async` runs as soon as downloaded, unordered relative to other async scripts and possibly before DOM is ready — fine for independent tags, risky for scripts that depend on order or full DOM. Modules behave like deferred by default.  
**Common wrong:** Swapping them casually.  
**Follow-ups:** Where should DOMContentLoaded listeners be registered?  
**Production:** App bundles: module or defer; pure analytics: async is common.

### Q57. Why give images width and height?
**Expected:** The browser can reserve aspect ratio before the image bytes arrive, reducing layout shift when the image paints. Modern HTML uses width/height attributes to compute aspect ratio. Without them, content below jumps when the image loads — CLS and annoying UX.  
**Common wrong:** “Only CSS matters for size.”  
**Follow-ups:** How does `aspect-ratio` CSS interact?  
**Production:** Enforce dimensions in image components; CDNs can inject them.

### Q58. What is hydration (browser-facing)?
**Expected:** In SSR/SSG apps, the server sends HTML so users see content early. The client JS then **hydrates** — attaches event handlers and virtual DOM state to that existing markup. Until hydration finishes, some interactivity may be missing or mismatched. Large hydration bundles delay usability even when paint looked fine.  
**Common wrong:** “Hydration means downloading CSS.”  
**Follow-ups:** What is a hydration mismatch?  
**Production:** Reduce client components; serialize less state; prefer progressive patterns.

### Q59. How does `postMessage` stay safe?
**Expected:** `postMessage` allows cross-origin communication between windows/iframes. Safety requires: specify exact target origin when sending (not `*`), and on receive verify `event.origin` (and maybe `event.source`) before trusting data. Never `eval` message data. Treat messages as UGC from a security perspective.  
**Common wrong:** Listening without origin checks.  
**Follow-ups:** How do you hand off auth across embeds carefully?  
**Production:** Version message schemas; ignore unknown shapes.

### Q60. Summarize a performance pass on a slow landing page.
**Expected:** Pull field LCP/INP/CLS. Inspect waterfall: hero image weight/discovery, blocking CSS/JS, font strategy. Shrink and prioritize LCP image (format, size, preload, not lazy). Defer non-critical JS/CSS; split below-fold widgets. Reserve sizes to kill CLS. Recheck on throttled mobile. Only then micro-optimize code.  
**Common wrong:** Starting with rewriting the React tree.  
**Follow-ups:** What budget would you set for initial JS?  
**Production:** Make the checklist a team runbook with owners per metric.

---

## M. More scenarios interviewers love

### Q61. You set a cookie without `SameSite` — what happens today?
**Expected:** Modern browsers default unspecified SameSite behavior toward `Lax`-like protection for many cookies, but relying on defaults is fragile across browsers and time. Explicitly set `SameSite=Lax` or `Strict` for first-party sessions, or `None; Secure` only when you truly need cross-site sends — and then add CSRF defenses. Interviews want you to show you know defaults changed historically and that explicit attributes are clearer in code review.  
**Common wrong:** “Cookies always send everywhere unless blocked by CORS.”  
**Follow-ups:** Top-level GET navigations under Lax?  
**Production:** Set attributes explicitly in `Set-Cookie` helpers; test embedded flows separately.

### Q62. Why might `getBoundingClientRect` in a loop be expensive?
**Expected:** Each geometry read can force the browser to flush pending style and layout so the returned box is up to date. In a loop interleaved with style writes, you thrash layout. Even read-only loops over many nodes cost if each read flushes. Prefer batching: read all measurements in one phase after styles settle, then write.  
**Common wrong:** “Rect reads are O(1) dictionary lookups.”  
**Follow-ups:** How does this show up in a Performance profile?  
**Production:** Virtualize large lists so you aren’t measuring thousands of cells per frame.

### Q63. What is the difference between `preload` and `prefetch`?
**Expected:** `preload` is for resources needed for the **current** navigation — high priority, critical path (hero font/image, critical script). `prefetch` is a hint for resources likely needed for a **future** navigation — lower priority, speculative. Misusing preload for everything competes with true critical bytes; over-prefetch wastes data.  
**Common wrong:** Using the terms interchangeably.  
**Follow-ups:** When is `modulepreload` appropriate?  
**Production:** Automate preload only for known LCP/critical assets from the template.

### Q64. Can service workers run without HTTPS?
**Expected:** Service workers require a secure context — HTTPS (or localhost for development). That requirement exists because a compromised SW could persistently hijack your origin’s network. Mixed content and insecure origins are non-starters for SW-powered offline apps.  
**Common wrong:** “SW works on any http site in production.”  
**Follow-ups:** What else requires a secure context? (`crypto.subtle`, etc.)  
**Production:** Terminate HTTP; HSTS; fix mixed content before PWA work.

### Q65. How do you explain `async`/`await` on the main thread vs “blocking”?
**Expected:** `await` yields the function’s continuation as a microtask/job after the awaited promise settles — it does **not** freeze the browser the way a tight sync loop does. However, the code **before** the await and the continuation **after** still run on the main thread and can be long tasks. Also, awaiting doesn’t make DOM updates free; you still need to structure UI work carefully.  
**Common wrong:** “await means background thread.”  
**Follow-ups:** Where do promise reactions sit relative to rendering?  
**Production:** Don’t do heavy JSON parse right after await without yielding for paint if UI must update first.

### Q66. What is sticky session UI state you should *not* put in `localStorage`?
**Expected:** Highly sensitive tokens, PII you aren’t allowed to persist, or huge datasets that belong in IndexedDB/server. Also ephemeral draft state that should die with the tab — that is `sessionStorage` or memory. Cross-tab sync via `storage` events can be surprising for auth state. Prefer server sessions and short-lived client caches with clear TTL.  
**Common wrong:** Caching everything client-side “for speed.”  
**Follow-ups:** How do you expire client caches?  
**Production:** Write a storage policy doc per app: what, where, TTL, PII rules.

---

## How to practice with this file

1. Pick a section (e.g. Security).  
2. Answer aloud for 60–90 seconds **without** looking.  
3. Compare to **Expected** — fill gaps.  
4. Ask yourself the **Follow-ups**.  
5. Add one **Production** note from a real project you’ve seen.

### Self-check rubric

| Signal | Weak | Strong |
| --- | --- | --- |
| Attack vs defense | Names buzzwords only | Explains abuse then control |
| Performance | “Minify and CDN” | Bottleneck → matching fix → remeasure |
| Storage | Lists APIs | Capacity, sync/async, server visibility |
| Memory | “GC collects unused vars” | Reachability + retainer examples |
| Security | Mixes XSS/CSRF | Correct primary defenses each |

Related deep dives: [Security](/browser/06-security) · [Memory](/browser/07-memory-gc) · [Storage](/browser/08-storage) · [Optimization](/browser/09-optimization) · [Rendering](/browser/02-rendering-pipeline) · [Event Loop](/browser/03-event-loop) · [Networking](/browser/05-networking).
