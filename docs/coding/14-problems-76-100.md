# Problems 76–100

Graphs, Union-Find, design problems, and Trie — the hard half of the grind set.

| # | Problem | Pattern |
| --- | --- | --- |
| 76 | Connected Components | Union-Find |
| 77 | Redundant Connection | Union-Find |
| 78 | Accounts Merge | Union-Find |
| 79 | Graph Valid Tree | Union-Find |
| 80 | Network Delay Time | Dijkstra |
| 81 | Cheapest Flights K Stops | Bellman-Ford |
| 82 | Alien Dictionary | Topo |
| 83 | Course Schedule II | Topo |
| 84 | Word Ladder | BFS |
| 85 | Clone Graph | BFS |
| 86 | Surrounded Regions | DFS borders |
| 87 | Walls and Gates | Multi BFS |
| 88 | Rotting Oranges | Multi BFS |
| 89 | Shortest Path Binary Matrix | BFS |
| 90 | Pacific Atlantic | Multi DFS |
| 91 | Longest Consecutive | HashSet |
| 92 | Encode/Decode Strings | Serialization |
| 93 | Insert Delete GetRandom | Array+Map |
| 94 | LRU Cache | Ordered Map |
| 95 | Hit Counter | Queue |
| 96 | Logger Rate Limiter | HashMap |
| 97 | Browser History | Array pointer |
| 98 | Nested List Iterator | Stack |
| 99 | Implement Trie | Trie |
| 100 | Word Search II | Trie+DFS |

---

## 76. Number of Connected Components

**Difficulty:** Medium · **Pattern:** Union-Find

`n` nodes labeled 0..n-1 and undirected edges. Count connected components.

### Solution

```ts
export function countComponents(n: number, edges: number[][]): number {
  const parent = Array.from({ length: n }, (_, i) => i)
  const find = (x: number): number => {
    while (parent[x] !== x) {
      parent[x] = parent[parent[x]]
      x = parent[x]
    }
    return x
  }
  let comps = n
  for (const [a, b] of edges) {
    const ra = find(a), rb = find(b)
    if (ra !== rb) {
      parent[rb] = ra
      comps--
    }
  }
  return comps
}
```

### Explanation

Each successful union merges two components; start at `n` and decrement.

### Complexity

- **Time:** O(n + m·α(n))
- **Space:** O(n)

---

## 77. Redundant Connection

**Difficulty:** Medium · **Pattern:** Union-Find

Undirected graph that started as a tree + one extra edge. Return the edge that can be removed to restore a tree (last redundant in input order).

### Solution

```ts
export function findRedundantConnection(edges: number[][]): number[] {
  const n = edges.length
  const parent = Array.from({ length: n + 1 }, (_, i) => i)
  const find = (x: number): number => {
    while (parent[x] !== x) {
      parent[x] = parent[parent[x]]
      x = parent[x]
    }
    return x
  }
  for (const [a, b] of edges) {
    const ra = find(a), rb = find(b)
    if (ra === rb) return [a, b]
    parent[rb] = ra
  }
  return []
}
```

### Explanation

First edge whose endpoints are already united closes a cycle.

### Complexity

- **Time:** O(n·α(n))
- **Space:** O(n)

---

## 78. Accounts Merge

**Difficulty:** Medium · **Pattern:** Union-Find

Accounts as `[name, email…]`. Merge accounts sharing an email; return name + sorted emails.

### Solution

```ts
export function accountsMerge(accounts: string[][]): string[][] {
  const parent = new Map<string, string>()
  const emailName = new Map<string, string>()

  const find = (x: string): string => {
    if (!parent.has(x)) parent.set(x, x)
    while (parent.get(x) !== x) {
      parent.set(x, parent.get(parent.get(x)!)!)
      x = parent.get(x)!
    }
    return x
  }
  const union = (a: string, b: string) => {
    const ra = find(a), rb = find(b)
    if (ra !== rb) parent.set(rb, ra)
  }

  for (const [name, ...emails] of accounts) {
    for (const e of emails) {
      emailName.set(e, name)
      union(emails[0], e)
    }
  }

  const groups = new Map<string, string[]>()
  for (const e of emailName.keys()) {
    const root = find(e)
    if (!groups.has(root)) groups.set(root, [])
    groups.get(root)!.push(e)
  }

  return [...groups.values()].map((emails) => {
    emails.sort()
    return [emailName.get(emails[0])!, ...emails]
  })
}
```

### Explanation

Union emails within each account; shared emails connect components.

### Complexity

- **Time:** O(E·α + E log E) for sorts
- **Space:** O(E)

---

## 79. Graph Valid Tree

**Difficulty:** Medium · **Pattern:** Union-Find

`n` nodes, undirected edges. True iff the graph is a tree (connected + acyclic).

### Solution

```ts
export function validTree(n: number, edges: number[][]): boolean {
  if (edges.length !== n - 1) return false
  const parent = Array.from({ length: n }, (_, i) => i)
  const find = (x: number): number => {
    while (parent[x] !== x) {
      parent[x] = parent[parent[x]]
      x = parent[x]
    }
    return x
  }
  for (const [a, b] of edges) {
    const ra = find(a), rb = find(b)
    if (ra === rb) return false
    parent[rb] = ra
  }
  return true
}
```

### Explanation

Tree ↔ exactly `n-1` edges and no cycles (implies connected).

### Complexity

- **Time:** O(n·α(n))
- **Space:** O(n)

---

## 80. Network Delay Time

**Difficulty:** Medium · **Pattern:** Dijkstra

Weighted directed graph; from `k`, time for all nodes to receive signal. `-1` if impossible.

### Solution

```ts
export function networkDelayTime(times: number[][], n: number, k: number): number {
  const g: [number, number][][] = Array.from({ length: n + 1 }, () => [])
  for (const [u, v, w] of times) g[u].push([v, w])

  const dist = Array(n + 1).fill(Infinity)
  dist[k] = 0
  const pq: [number, number][] = [[0, k]] // [dist, node]

  while (pq.length) {
    pq.sort((a, b) => a[0] - b[0])
    const [d, u] = pq.shift()!
    if (d > dist[u]) continue
    for (const [v, w] of g[u]) {
      if (d + w < dist[v]) {
        dist[v] = d + w
        pq.push([dist[v], v])
      }
    }
  }

  let ans = 0
  for (let i = 1; i <= n; i++) {
    if (dist[i] === Infinity) return -1
    ans = Math.max(ans, dist[i])
  }
  return ans
}
```

### Explanation

Classic single-source shortest path; answer is max distance.

### Complexity

- **Time:** O(E²) with array PQ; O((V+E) log V) with binary heap
- **Space:** O(V+E)

---

## 81. Cheapest Flights Within K Stops

**Difficulty:** Medium · **Pattern:** Bellman-Ford

Cheapest price from `src` to `dst` with at most `k` stops (`k+1` edges).

### Solution

```ts
export function findCheapestPrice(
  n: number,
  flights: number[][],
  src: number,
  dst: number,
  k: number,
): number {
  let dist = Array(n).fill(Infinity)
  dist[src] = 0
  for (let i = 0; i <= k; i++) {
    const next = dist.slice()
    for (const [u, v, w] of flights) {
      if (dist[u] !== Infinity && dist[u] + w < next[v]) {
        next[v] = dist[u] + w
      }
    }
    dist = next
  }
  return dist[dst] === Infinity ? -1 : dist[dst]
}
```

### Explanation

Relax edges `k+1` rounds so path length is bounded.

### Complexity

- **Time:** O(k·E)
- **Space:** O(n)

---

## 82. Alien Dictionary

**Difficulty:** Hard · **Pattern:** Topological sort

Sorted alien words → derive character order. Invalid / cycle → `""`.

### Solution

```ts
export function alienOrder(words: string[]): string {
  const adj = new Map<string, Set<string>>()
  const indeg = new Map<string, number>()
  for (const w of words) for (const c of w) {
    if (!adj.has(c)) adj.set(c, new Set())
    if (!indeg.has(c)) indeg.set(c, 0)
  }

  for (let i = 0; i < words.length - 1; i++) {
    const a = words[i], b = words[i + 1]
    if (a.length > b.length && a.startsWith(b)) return ''
    const n = Math.min(a.length, b.length)
    for (let j = 0; j < n; j++) {
      if (a[j] !== b[j]) {
        if (!adj.get(a[j])!.has(b[j])) {
          adj.get(a[j])!.add(b[j])
          indeg.set(b[j], (indeg.get(b[j]) ?? 0) + 1)
        }
        break
      }
    }
  }

  const q: string[] = [...indeg.entries()].filter(([, d]) => d === 0).map(([c]) => c)
  let order = ''
  while (q.length) {
    const c = q.shift()!
    order += c
    for (const nei of adj.get(c)!) {
      indeg.set(nei, indeg.get(nei)! - 1)
      if (indeg.get(nei) === 0) q.push(nei)
    }
  }
  return order.length === indeg.size ? order : ''
}
```

### Explanation

Compare adjacent words for first differing chars → precedence edges; Kahn topo.

### Complexity

- **Time:** O(C) total chars
- **Space:** O(U²) alphabet edges worst case

---

## 83. Course Schedule II

**Difficulty:** Medium · **Pattern:** Topological sort

`numCourses`, prerequisites `[a,b]` meaning b→a. Return any valid order or `[]`.

### Solution

```ts
export function findOrder(numCourses: number, prerequisites: number[][]): number[] {
  const adj: number[][] = Array.from({ length: numCourses }, () => [])
  const indeg = Array(numCourses).fill(0)
  for (const [a, b] of prerequisites) {
    adj[b].push(a)
    indeg[a]++
  }
  const q: number[] = []
  for (let i = 0; i < numCourses; i++) if (indeg[i] === 0) q.push(i)
  const order: number[] = []
  while (q.length) {
    const u = q.shift()!
    order.push(u)
    for (const v of adj[u]) {
      if (--indeg[v] === 0) q.push(v)
    }
  }
  return order.length === numCourses ? order : []
}
```

### Explanation

Kahn BFS; incomplete order ⇒ cycle.

### Complexity

- **Time:** O(V+E)
- **Space:** O(V+E)

---

## 84. Word Ladder

**Difficulty:** Hard · **Pattern:** BFS

Shortest transformation length from `beginWord` to `endWord` changing one letter at a time; words must be in `wordList`.

### Solution

```ts
export function ladderLength(beginWord: string, endWord: string, wordList: string[]): number {
  const words = new Set(wordList)
  if (!words.has(endWord)) return 0
  const q: [string, number][] = [[beginWord, 1]]
  const seen = new Set([beginWord])

  while (q.length) {
    const [w, d] = q.shift()!
    if (w === endWord) return d
    const arr = w.split('')
    for (let i = 0; i < arr.length; i++) {
      const orig = arr[i]
      for (let c = 97; c <= 122; c++) {
        arr[i] = String.fromCharCode(c)
        const next = arr.join('')
        if (words.has(next) && !seen.has(next)) {
          seen.add(next)
          q.push([next, d + 1])
        }
      }
      arr[i] = orig
    }
  }
  return 0
}
```

### Explanation

Implicit graph of one-edit neighbors; BFS for shortest path.

### Complexity

- **Time:** O(N·L·26)
- **Space:** O(N·L)

---

## 85. Clone Graph

**Difficulty:** Medium · **Pattern:** BFS + HashMap

Deep clone undirected connected graph nodes with `val` and `neighbors`.

### Solution

```ts
class Node {
  val: number
  neighbors: Node[]
  constructor(val = 0, neighbors: Node[] = []) {
    this.val = val
    this.neighbors = neighbors
  }
}

export function cloneGraph(node: Node | null): Node | null {
  if (!node) return null
  const map = new Map<Node, Node>()
  const q: Node[] = [node]
  map.set(node, new Node(node.val))
  while (q.length) {
    const cur = q.shift()!
    for (const nei of cur.neighbors) {
      if (!map.has(nei)) {
        map.set(nei, new Node(nei.val))
        q.push(nei)
      }
      map.get(cur)!.neighbors.push(map.get(nei)!)
    }
  }
  return map.get(node)!
}
```

### Explanation

Map original→clone; BFS ensures each edge cloned once.

### Complexity

- **Time:** O(V+E)
- **Space:** O(V)

---

## 86. Surrounded Regions

**Difficulty:** Medium · **Pattern:** DFS from borders

Capture surrounded `'O'` regions (flip to `'X'`). Border-connected `'O'` stay.

### Solution

```ts
export function solve(board: string[][]): void {
  if (!board.length) return
  const m = board.length, n = board[0].length
  const dfs = (r: number, c: number) => {
    if (r < 0 || c < 0 || r >= m || c >= n || board[r][c] !== 'O') return
    board[r][c] = '#'
    dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)
  }
  for (let i = 0; i < m; i++) {
    dfs(i, 0); dfs(i, n - 1)
  }
  for (let j = 0; j < n; j++) {
    dfs(0, j); dfs(m - 1, j)
  }
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++) {
      if (board[i][j] === 'O') board[i][j] = 'X'
      else if (board[i][j] === '#') board[i][j] = 'O'
    }
}
```

### Explanation

Mark unsurrounded from borders; remaining `'O'` are captured.

### Complexity

- **Time:** O(mn)
- **Space:** O(mn) recursion worst case

---

## 87. Walls and Gates

**Difficulty:** Medium · **Pattern:** Multi-source BFS

Grid: `-1` wall, `0` gate, `INF` empty. Fill each empty with distance to nearest gate.

### Solution

```ts
const INF = 2147483647

export function wallsAndGates(rooms: number[][]): void {
  const m = rooms.length, n = rooms[0]?.length ?? 0
  const q: [number, number][] = []
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++)
      if (rooms[i][j] === 0) q.push([i, j])

  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]
  while (q.length) {
    const [r, c] = q.shift()!
    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc
      if (nr < 0 || nc < 0 || nr >= m || nc >= n || rooms[nr][nc] !== INF) continue
      rooms[nr][nc] = rooms[r][c] + 1
      q.push([nr, nc])
    }
  }
}
```

### Explanation

BFS from all gates simultaneously — first visit is shortest.

### Complexity

- **Time:** O(mn)
- **Space:** O(mn)

---

## 88. Rotting Oranges

**Difficulty:** Medium · **Pattern:** Multi-source BFS

`0` empty, `1` fresh, `2` rotten. Minutes until all fresh rotten; `-1` if impossible.

### Solution

```ts
export function orangesRotting(grid: number[][]): number {
  const m = grid.length, n = grid[0].length
  const q: [number, number][] = []
  let fresh = 0
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++) {
      if (grid[i][j] === 2) q.push([i, j])
      if (grid[i][j] === 1) fresh++
    }
  if (fresh === 0) return 0

  let minutes = 0
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]
  while (q.length && fresh > 0) {
    const size = q.length
    for (let s = 0; s < size; s++) {
      const [r, c] = q.shift()!
      for (const [dr, dc] of dirs) {
        const nr = r + dr, nc = c + dc
        if (nr < 0 || nc < 0 || nr >= m || nc >= n || grid[nr][nc] !== 1) continue
        grid[nr][nc] = 2
        fresh--
        q.push([nr, nc])
      }
    }
    minutes++
  }
  return fresh === 0 ? minutes : -1
}
```

### Explanation

Level-order BFS from all initially rotten cells.

### Complexity

- **Time:** O(mn)
- **Space:** O(mn)

---

## 89. Shortest Path in Binary Matrix

**Difficulty:** Medium · **Pattern:** BFS 8-direction

Shortest clear path length in `n×n` binary matrix from `(0,0)` to `(n-1,n-1)` (8-dir). `0` clear.

### Solution

```ts
export function shortestPathBinaryMatrix(grid: number[][]): number {
  const n = grid.length
  if (grid[0][0] || grid[n - 1][n - 1]) return -1
  const q: [number, number, number][] = [[0, 0, 1]]
  grid[0][0] = 1
  const dirs = [
    [1, 0], [-1, 0], [0, 1], [0, -1],
    [1, 1], [1, -1], [-1, 1], [-1, -1],
  ]
  while (q.length) {
    const [r, c, d] = q.shift()!
    if (r === n - 1 && c === n - 1) return d
    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc
      if (nr < 0 || nc < 0 || nr >= n || nc >= n || grid[nr][nc]) continue
      grid[nr][nc] = 1
      q.push([nr, nc, d + 1])
    }
  }
  return -1
}
```

### Explanation

Unweighted grid → BFS; mark visited in-place.

### Complexity

- **Time:** O(n²)
- **Space:** O(n²)

---

## 90. Pacific Atlantic Water Flow

**Difficulty:** Medium · **Pattern:** Multi-source DFS

Heights grid; cells that can flow to both Pacific (top/left) and Atlantic (bottom/right).

### Solution

```ts
export function pacificAtlantic(heights: number[][]): number[][] {
  const m = heights.length, n = heights[0].length
  const pac = Array.from({ length: m }, () => Array(n).fill(false))
  const atl = Array.from({ length: m }, () => Array(n).fill(false))

  const dfs = (r: number, c: number, seen: boolean[][], prev: number) => {
    if (r < 0 || c < 0 || r >= m || c >= n || seen[r][c] || heights[r][c] < prev) return
    seen[r][c] = true
    const h = heights[r][c]
    dfs(r + 1, c, seen, h); dfs(r - 1, c, seen, h)
    dfs(r, c + 1, seen, h); dfs(r, c - 1, seen, h)
  }

  for (let i = 0; i < m; i++) {
    dfs(i, 0, pac, 0); dfs(i, n - 1, atl, 0)
  }
  for (let j = 0; j < n; j++) {
    dfs(0, j, pac, 0); dfs(m - 1, j, atl, 0)
  }

  const res: number[][] = []
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++)
      if (pac[i][j] && atl[i][j]) res.push([i, j])
  return res
}
```

### Explanation

Flow uphill from oceans; intersection is the answer.

### Complexity

- **Time:** O(mn)
- **Space:** O(mn)

---

## 91. Longest Consecutive Sequence

**Difficulty:** Medium · **Pattern:** HashSet

Longest consecutive elements sequence length in unsorted array. O(n) required.

### Solution

```ts
export function longestConsecutive(nums: number[]): number {
  const set = new Set(nums)
  let best = 0
  for (const x of set) {
    if (set.has(x - 1)) continue // not a start
    let len = 1, y = x
    while (set.has(y + 1)) {
      y++
      len++
    }
    best = Math.max(best, len)
  }
  return best
}
```

### Explanation

Only start streaks at numbers with no predecessor.

### Complexity

- **Time:** O(n)
- **Space:** O(n)

---

## 92. Encode and Decode Strings

**Difficulty:** Medium · **Pattern:** Serialization

Design encode/decode for list of strings (may contain any UTF-16 / delimiters).

### Solution

```ts
export function encode(strs: string[]): string {
  return strs.map((s) => `${s.length}#${s}`).join('')
}

export function decode(s: string): string[] {
  const res: string[] = []
  let i = 0
  while (i < s.length) {
    let j = i
    while (s[j] !== '#') j++
    const len = Number(s.slice(i, j))
    res.push(s.slice(j + 1, j + 1 + len))
    i = j + 1 + len
  }
  return res
}
```

### Explanation

Length-prefix framing avoids delimiter collisions.

### Complexity

- **Time:** O(total chars)
- **Space:** O(total chars)

---

## 93. Insert Delete GetRandom O(1)

**Difficulty:** Medium · **Pattern:** Array + HashMap

`insert`, `remove`, `getRandom` all average O(1).

### Solution

```ts
export class RandomizedSet {
  private arr: number[] = []
  private idx = new Map<number, number>()

  insert(val: number): boolean {
    if (this.idx.has(val)) return false
    this.idx.set(val, this.arr.length)
    this.arr.push(val)
    return true
  }

  remove(val: number): boolean {
    if (!this.idx.has(val)) return false
    const i = this.idx.get(val)!
    const last = this.arr[this.arr.length - 1]
    this.arr[i] = last
    this.idx.set(last, i)
    this.arr.pop()
    this.idx.delete(val)
    return true
  }

  getRandom(): number {
    return this.arr[Math.floor(Math.random() * this.arr.length)]
  }
}
```

### Explanation

Swap-with-last on remove keeps the array dense for O(1) random index.

### Complexity

- **Time:** O(1) average each op
- **Space:** O(n)

---

## 94. LRU Cache

**Difficulty:** Medium · **Pattern:** Map insertion order

`get` / `put` O(1); evict least recently used when over capacity.

### Solution

```ts
export class LRUCache {
  private map = new Map<number, number>()
  constructor(private capacity: number) {}

  get(key: number): number {
    if (!this.map.has(key)) return -1
    const v = this.map.get(key)!
    this.map.delete(key)
    this.map.set(key, v) // refresh recency (end = newest)
    return v
  }

  put(key: number, value: number): void {
    if (this.map.has(key)) this.map.delete(key)
    this.map.set(key, value)
    if (this.map.size > this.capacity) {
      const oldest = this.map.keys().next().value!
      this.map.delete(oldest)
    }
  }
}
```

### Explanation

JS `Map` preserves insertion order; delete+set moves to newest.

### Complexity

- **Time:** O(1) average
- **Space:** O(capacity)

---

## 95. Hit Counter

**Difficulty:** Medium · **Pattern:** Queue

Record hits; return hits in past 300 seconds (inclusive).

### Solution

```ts
export class HitCounter {
  private q: number[] = []

  hit(timestamp: number): void {
    this.q.push(timestamp)
  }

  getHits(timestamp: number): number {
    while (this.q.length && this.q[0] <= timestamp - 300) this.q.shift()
    return this.q.length
  }
}
```

### Explanation

Expire timestamps outside the window on read (lazy).

### Complexity

- **Time:** amortized O(1) per hit; getHits O(expired)
- **Space:** O(hits in window)

---

## 96. Logger Rate Limiter

**Difficulty:** Easy/Medium · **Pattern:** HashMap

`shouldPrintMessage(timestamp, message)` — true if message not printed in last 10 seconds.

### Solution

```ts
export class Logger {
  private last = new Map<string, number>()

  shouldPrintMessage(timestamp: number, message: string): boolean {
    const prev = this.last.get(message)
    if (prev !== undefined && timestamp - prev < 10) return false
    this.last.set(message, timestamp)
    return true
  }
}
```

### Explanation

Store last print time per message.

### Complexity

- **Time:** O(1)
- **Space:** O(unique messages)

---

## 97. Browser History

**Difficulty:** Medium · **Pattern:** Array + pointer

`visit`, `back(steps)`, `forward(steps)` for URL history.

### Solution

```ts
export class BrowserHistory {
  private urls: string[]
  private i: number

  constructor(homepage: string) {
    this.urls = [homepage]
    this.i = 0
  }

  visit(url: string): void {
    this.urls = this.urls.slice(0, this.i + 1)
    this.urls.push(url)
    this.i++
  }

  back(steps: number): string {
    this.i = Math.max(0, this.i - steps)
    return this.urls[this.i]
  }

  forward(steps: number): string {
    this.i = Math.min(this.urls.length - 1, this.i + steps)
    return this.urls[this.i]
  }
}
```

### Explanation

Visit truncates forward stack; pointer moves within array.

### Complexity

- **Time:** O(1) amortized visit; O(1) back/forward
- **Space:** O(visits)

---

## 98. Nested List Iterator

**Difficulty:** Medium · **Pattern:** Stack

Flatten nested list of integers lazily via `hasNext` / `next`.

### Solution

```ts
interface NestedInteger {
  isInteger(): boolean
  getInteger(): number | null
  getList(): NestedInteger[]
}

export class NestedIterator {
  private stack: NestedInteger[]

  constructor(nestedList: NestedInteger[]) {
    this.stack = [...nestedList].reverse()
  }

  private prepare() {
    while (this.stack.length && !this.stack[this.stack.length - 1].isInteger()) {
      const list = this.stack.pop()!.getList()
      for (let i = list.length - 1; i >= 0; i--) this.stack.push(list[i])
    }
  }

  hasNext(): boolean {
    this.prepare()
    return this.stack.length > 0
  }

  next(): number {
    this.prepare()
    return this.stack.pop()!.getInteger()!
  }
}
```

### Explanation

Expand lists on demand so `hasNext` always tops an integer (or empty).

### Complexity

- **Time:** amortized O(1) per element
- **Space:** O(depth / nesting)

---

## 99. Implement Trie (Prefix Tree)

**Difficulty:** Medium · **Pattern:** Trie

`insert`, `search`, `startsWith`.

### Solution

```ts
class TrieNode {
  children = new Map<string, TrieNode>()
  end = false
}

export class Trie {
  private root = new TrieNode()

  insert(word: string): void {
    let node = this.root
    for (const ch of word) {
      if (!node.children.has(ch)) node.children.set(ch, new TrieNode())
      node = node.children.get(ch)!
    }
    node.end = true
  }

  private walk(s: string): TrieNode | null {
    let node = this.root
    for (const ch of s) {
      const next = node.children.get(ch)
      if (!next) return null
      node = next
    }
    return node
  }

  search(word: string): boolean {
    return this.walk(word)?.end === true
  }

  startsWith(prefix: string): boolean {
    return this.walk(prefix) != null
  }
}
```

### Explanation

Path of characters; `end` marks complete words.

### Complexity

- **Time:** O(L) per op
- **Space:** O(total characters inserted)

---

## 100. Word Search II

**Difficulty:** Hard · **Pattern:** Trie + DFS

Find all `words` that appear in the board by adjacent (4-dir) cells without reuse.

### Solution

```ts
export function findWords(board: string[][], words: string[]): string[] {
  class Node {
    children = new Map<string, Node>()
    word: string | null = null
  }
  const root = new Node()
  for (const w of words) {
    let node = root
    for (const ch of w) {
      if (!node.children.has(ch)) node.children.set(ch, new Node())
      node = node.children.get(ch)!
    }
    node.word = w
  }

  const m = board.length, n = board[0].length
  const res: string[] = []

  const dfs = (r: number, c: number, node: Node) => {
    if (r < 0 || c < 0 || r >= m || c >= n) return
    const ch = board[r][c]
    const next = node.children.get(ch)
    if (!next) return
    if (next.word) {
      res.push(next.word)
      next.word = null
    }
    board[r][c] = '#'
    dfs(r + 1, c, next)
    dfs(r - 1, c, next)
    dfs(r, c + 1, next)
    dfs(r, c - 1, next)
    board[r][c] = ch
  }

  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++) dfs(i, j, root)
  return res
}
```

### Explanation

Build trie of dictionary; DFS board while walking trie; clear `word` to dedupe.

### Complexity

- **Time:** O(m·n·4·L) practical bound
- **Space:** O(total dict chars)
