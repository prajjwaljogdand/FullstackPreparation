from pathlib import Path

def P(num, title, difficulty, pattern, statement, solution, explanation, time_c, space_c, follow=""):
    follow_sec = f"\n**Follow-up:** {follow}\n" if follow else ""
    return f"""## {num}. {title}

**Difficulty:** {difficulty} · **Pattern:** {pattern}

{statement}

### Solution

```ts
{solution}
```

### Explanation

{explanation}

### Complexity

- **Time:** {time_c}
- **Space:** {space_c}
{follow_sec}
"""

items = []

items.append(P(76, "Number of Connected Components", "Medium", "Union-Find / DFS",
"`n` nodes labeled 0..n-1 and undirected edges. Count connected components.",
"""export function countComponents(n: number, edges: number[][]): number {
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
    if (ra !== rb) { parent[rb] = ra; comps-- }
  }
  return comps
}""",
"Each successful union merges two components.", "O(n + m·α(n))", "O(n)"))

items.append(P(77, "Redundant Connection", "Medium", "Union-Find",
"Undirected graph that started as a tree + one extra edge. Return the edge that can be removed.",
"""export function findRedundantConnection(edges: number[][]): number[] {
  const parent = Array.from({ length: edges.length + 1 }, (_, i) => i)
  const find = (x: number): number => {
    while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x] }
    return x
  }
  for (const [u, v] of edges) {
    const ru = find(u), rv = find(v)
    if (ru === rv) return [u, v]
    parent[rv] = ru
  }
  return []
}""",
"First edge whose endpoints already share a root creates the cycle.", "O(n·α(n))", "O(n)"))

items.append(P(78, "Accounts Merge", "Medium", "Union-Find + map",
"Accounts: [name, emails...]. Merge accounts sharing an email; return sorted emails per name.",
"""export function accountsMerge(accounts: string[][]): string[][] {
  const parent = new Map<string, string>()
  const emailToName = new Map<string, string>()
  const find = (x: string): string => {
    if (!parent.has(x)) parent.set(x, x)
    if (parent.get(x) !== x) parent.set(x, find(parent.get(x)!))
    return parent.get(x)!
  }
  const union = (a: string, b: string) => {
    parent.set(find(a), find(b))
  }
  for (const [name, ...emails] of accounts) {
    for (const e of emails) {
      emailToName.set(e, name)
      if (!parent.has(e)) parent.set(e, e)
      union(emails[0], e)
    }
  }
  const groups = new Map<string, string[]>()
  for (const e of parent.keys()) {
    const root = find(e)
    if (!groups.has(root)) groups.set(root, [])
    groups.get(root)!.push(e)
  }
  return [...groups.values()].map((emails) => {
    emails.sort()
    return [emailToName.get(emails[0])!, ...emails]
  })
}""",
"Union emails within an account; group by root; attach name.", "O(E·α + E log E)", "O(E)"))

items.append(P(79, "Graph Valid Tree", "Medium", "Union-Find",
"`n` nodes and edges; is it a valid tree? (connected + n-1 edges / no cycle).",
"""export function validTree(n: number, edges: number[][]): boolean {
  if (edges.length !== n - 1) return false
  const parent = Array.from({ length: n }, (_, i) => i)
  const find = (x: number): number => {
    while (parent[x] !== x) { parent[x] = parent[parent[x]]; x = parent[x] }
    return x
  }
  for (const [u, v] of edges) {
    const ru = find(u), rv = find(v)
    if (ru === rv) return false
    parent[rv] = ru
  }
  return true
}""",
"Tree ⇔ exactly n−1 edges and no cycle (or connected).", "O(n·α(n))", "O(n)"))

items.append(P(80, "Network Delay Time", "Medium", "Dijkstra",
"Directed weighted graph; time for signal from `k` to reach all nodes (or -1).",
"""export function networkDelayTime(times: number[][], n: number, k: number): number {
  const g: Array<Array<[number, number]>> = Array.from({ length: n + 1 }, () => [])
  for (const [u, v, w] of times) g[u].push([v, w])
  const dist = Array(n + 1).fill(Infinity)
  dist[k] = 0
  const used = Array(n + 1).fill(false)
  for (let i = 0; i < n; i++) {
    let u = -1
    for (let j = 1; j <= n; j++) if (!used[j] && (u === -1 || dist[j] < dist[u])) u = j
    if (u === -1 || dist[u] === Infinity) break
    used[u] = true
    for (const [v, w] of g[u]) dist[v] = Math.min(dist[v], dist[u] + w)
  }
  const ans = Math.max(...dist.slice(1))
  return ans === Infinity ? -1 : ans
}""",
"Shortest paths from k; answer is max distance.", "O(n² + E)", "O(n + E)",
"Binary heap Dijkstra O((n+E) log n)."))

items.append(P(81, "Cheapest Flights Within K Stops", "Medium", "Bellman-Ford / BFS",
"Flights [from,to,price]; cheapest price from src to dst with at most k stops.",
"""export function findCheapestPrice(
  n: number,
  flights: number[][],
  src: number,
  dst: number,
  k: number
): number {
  let dist = Array(n).fill(Infinity)
  dist[src] = 0
  for (let i = 0; i <= k; i++) {
    const next = dist.slice()
    for (const [u, v, w] of flights) {
      if (dist[u] !== Infinity) next[v] = Math.min(next[v], dist[u] + w)
    }
    dist = next
  }
  return dist[dst] === Infinity ? -1 : dist[dst]
}""",
"Relax edges for k+1 rounds (≤ k stops ⇒ ≤ k+1 edges).", "O(k·E)", "O(n)"))

items.append(P(82, "Alien Dictionary", "Hard", "Topo sort",
"Sorted words in alien language; return unique letter order (or '' if invalid).",
"""export function alienOrder(words: string[]): string {
  const g = new Map<string, Set<string>>()
  const indeg = new Map<string, number>()
  for (const w of words) for (const c of w) {
    if (!g.has(c)) g.set(c, new Set())
    if (!indeg.has(c)) indeg.set(c, 0)
  }
  for (let i = 0; i < words.length - 1; i++) {
    const a = words[i], b = words[i + 1]
    if (a.length > b.length && a.startsWith(b)) return ''
    const len = Math.min(a.length, b.length)
    for (let j = 0; j < len; j++) {
      if (a[j] !== b[j]) {
        if (!g.get(a[j])!.has(b[j])) {
          g.get(a[j])!.add(b[j])
          indeg.set(b[j], indeg.get(b[j])! + 1)
        }
        break
      }
    }
  }
  const q = [...indeg.entries()].filter(([, d]) => d === 0).map(([c]) => c)
  let order = ''
  for (let i = 0; i < q.length; i++) {
    const u = q[i]
    order += u
    for (const v of g.get(u)!) {
      indeg.set(v, indeg.get(v)! - 1)
      if (indeg.get(v) === 0) q.push(v)
    }
  }
  return order.length === indeg.size ? order : ''
}""",
"Compare adjacent words for ordering edges; Kahn topo; cycle ⇒ invalid.", "O(C)", "O(C)"))

items.append(P(83, "Course Schedule II", "Medium", "Topo sort",
"Return a valid course order to finish all, or empty if impossible.",
"""export function findOrder(numCourses: number, prerequisites: number[][]): number[] {
  const g: number[][] = Array.from({ length: numCourses }, () => [])
  const indeg = Array(numCourses).fill(0)
  for (const [a, b] of prerequisites) { g[b].push(a); indeg[a]++ }
  const q: number[] = []
  for (let i = 0; i < numCourses; i++) if (indeg[i] === 0) q.push(i)
  const order: number[] = []
  for (let i = 0; i < q.length; i++) {
    const u = q[i]
    order.push(u)
    for (const v of g[u]) if (--indeg[v] === 0) q.push(v)
  }
  return order.length === numCourses ? order : []
}""",
"Kahn; incomplete order ⇒ cycle.", "O(V+E)", "O(V+E)"))

items.append(P(84, "Word Ladder", "Hard", "BFS",
"Shortest transformation sequence length from beginWord to endWord (change one letter, must be in wordList).",
"""export function ladderLength(beginWord: string, endWord: string, wordList: string[]): number {
  const words = new Set(wordList)
  if (!words.has(endWord)) return 0
  const q: string[] = [beginWord]
  let steps = 1
  while (q.length) {
    const size = q.length
    for (let s = 0; s < size; s++) {
      const word = q.shift()!
      if (word === endWord) return steps
      const arr = word.split('')
      for (let i = 0; i < arr.length; i++) {
        const orig = arr[i]
        for (let c = 97; c <= 122; c++) {
          arr[i] = String.fromCharCode(c)
          const next = arr.join('')
          if (words.has(next)) {
            words.delete(next)
            q.push(next)
          }
        }
        arr[i] = orig
      }
    }
    steps++
  }
  return 0
}""",
"BFS on implicit graph of one-edit neighbors; delete visited from set.", "O(N·L·26)", "O(N·L)"))

items.append(P(85, "Clone Graph (adjacency list variant)", "Medium", "BFS clone",
"Deep clone undirected connected graph using BFS.",
"""class Node {
  val: number
  neighbors: Node[]
  constructor(val = 0, neighbors: Node[] = []) {
    this.val = val
    this.neighbors = neighbors
  }
}

export function cloneGraph(node: Node | null): Node | null {
  if (!node) return null
  const map = new Map<Node, Node>([[node, new Node(node.val)]])
  const q: Node[] = [node]
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
}""",
"Map original→clone; enqueue unseen; wire neighbor clones.", "O(V+E)", "O(V)"))

items.append(P(86, "Surrounded Regions", "Medium", "DFS borders",
"Capture surrounded 'O' regions by flipping to 'X'. Border-connected 'O' stay.",
"""export function solve(board: string[][]): void {
  if (!board.length) return
  const m = board.length, n = board[0].length
  const dfs = (r: number, c: number) => {
    if (r < 0 || c < 0 || r >= m || c >= n || board[r][c] !== 'O') return
    board[r][c] = 'B'
    dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)
  }
  for (let i = 0; i < m; i++) { dfs(i, 0); dfs(i, n - 1) }
  for (let j = 0; j < n; j++) { dfs(0, j); dfs(m - 1, j) }
  for (let i = 0; i < m; i++) {
    for (let j = 0; j < n; j++) {
      if (board[i][j] === 'O') board[i][j] = 'X'
      else if (board[i][j] === 'B') board[i][j] = 'O'
    }
  }
}""",
"Mark border-safe O's, flip remaining O→X, restore marked.", "O(mn)", "O(mn)"))

items.append(P(87, "Walls and Gates", "Medium", "Multi-source BFS",
"Grid: INF empty, 0 gate, -1 wall. Fill each empty with distance to nearest gate.",
"""export function wallsAndGates(rooms: number[][]): void {
  const m = rooms.length, n = rooms[0].length
  const q: Array<[number, number]> = []
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++)
      if (rooms[i][j] === 0) q.push([i, j])
  const dirs = [[1,0],[-1,0],[0,1],[0,-1]]
  for (let qi = 0; qi < q.length; qi++) {
    const [r, c] = q[qi]
    for (const [dr, dc] of dirs) {
      const nr = r + dr, nc = c + dc
      if (nr < 0 || nc < 0 || nr >= m || nc >= n) continue
      if (rooms[nr][nc] !== 2147483647) continue
      rooms[nr][nc] = rooms[r][c] + 1
      q.push([nr, nc])
    }
  }
}""",
"BFS from all gates simultaneously.", "O(mn)", "O(mn)"))

items.append(P(88, "Rotting Oranges", "Medium", "Multi-source BFS",
"0 empty, 1 fresh, 2 rotten. Minutes until all fresh rotten; -1 if impossible.",
"""export function orangesRotting(grid: number[][]): number {
  const m = grid.length, n = grid[0].length
  const q: Array<[number, number]> = []
  let fresh = 0
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++) {
      if (grid[i][j] === 2) q.push([i, j])
      if (grid[i][j] === 1) fresh++
    }
  let minutes = 0
  const dirs = [[1,0],[-1,0],[0,1],[0,-1]]
  while (q.length && fresh) {
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
  return fresh ? -1 : minutes
}""",
"Level-order BFS from initially rotten oranges.", "O(mn)", "O(mn)"))

items.append(P(89, "Shortest Path in Binary Matrix", "Medium", "BFS 8-dir",
"n×n grid 0 empty / 1 blocked. Shortest clear path length from (0,0) to (n-1,n-1) (8 directions).",
"""export function shortestPathBinaryMatrix(grid: number[][]): number {
  const n = grid.length
  if (grid[0][0] || grid[n - 1][n - 1]) return -1
  const q: Array<[number, number, number]> = [[0, 0, 1]]
  grid[0][0] = 1
  const dirs = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
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
}""",
"Unweighted shortest path ⇒ BFS; mark visited by setting cell to 1.", "O(n²)", "O(n²)"))

items.append(P(90, "Pacific Atlantic Water Flow", "Medium", "Multi-source DFS",
"(Reprise with cleaner API) cells that can reach both oceans.",
"""export function pacificAtlantic(heights: number[][]): number[][] {
  const m = heights.length, n = heights[0].length
  const pac = Array.from({ length: m }, () => Array(n).fill(false))
  const atl = Array.from({ length: m }, () => Array(n).fill(false))
  const dfs = (r: number, c: number, seen: boolean[][], prev: number) => {
    if (r < 0 || c < 0 || r >= m || c >= n || seen[r][c] || heights[r][c] < prev) return
    seen[r][c] = true
    dfs(r + 1, c, seen, heights[r][c])
    dfs(r - 1, c, seen, heights[r][c])
    dfs(r, c + 1, seen, heights[r][c])
    dfs(r, c - 1, seen, heights[r][c])
  }
  for (let i = 0; i < m; i++) { dfs(i, 0, pac, 0); dfs(i, n - 1, atl, 0) }
  for (let j = 0; j < n; j++) { dfs(0, j, pac, 0); dfs(m - 1, j, atl, 0) }
  const res: number[][] = []
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++)
      if (pac[i][j] && atl[i][j]) res.push([i, j])
  return res
}""",
"Reverse flow from oceans; intersect reachable sets.", "O(mn)", "O(mn)"))

items.append(P(91, "Longest Consecutive Sequence", "Medium", "HashSet",
"Unsorted array; longest consecutive elements sequence length. O(n) required.",
"""export function longestConsecutive(nums: number[]): number {
  const set = new Set(nums)
  let best = 0
  for (const x of set) {
    if (set.has(x - 1)) continue // not a start
    let len = 1
    let y = x
    while (set.has(y + 1)) { y++; len++ }
    best = Math.max(best, len)
  }
  return best
}""",
"Only start streaks at numbers with no predecessor.", "O(n)", "O(n)"))

items.append(P(92, "Encode and Decode Strings", "Medium", "Serialization",
"Design encode/decode for list of strings (may contain any UTF-8).",
"""export function encode(strs: string[]): string {
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
}""",
"Length-prefix framing avoids delimiter collision.", "O(n)", "O(n)"))

items.append(P(93, "Insert Delete GetRandom O(1)", "Medium", "Array + HashMap",
"set with insert, remove, getRandom all average O(1).",
"""export class RandomizedSet {
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
}""",
"Swap-with-last on delete to keep array dense for O(1) random.", "O(1) avg", "O(n)"))

items.append(P(94, "LRU Cache (Map-order)", "Hard", "Ordered Map",
"Implement LRU using JS Map insertion order (interview: still explain DLL).",
"""export class LRUCache {
  private map = new Map<number, number>()
  constructor(private capacity: number) {}

  get(key: number): number {
    if (!this.map.has(key)) return -1
    const v = this.map.get(key)!
    this.map.delete(key)
    this.map.set(key, v)
    return v
  }

  put(key: number, value: number): void {
    if (this.map.has(key)) this.map.delete(key)
    this.map.set(key, value)
    if (this.map.size > this.capacity) {
      const lru = this.map.keys().next().value!
      this.map.delete(lru)
    }
  }
}""",
"Re-insert moves key to MRU end; first key is LRU.", "O(1)", "O(capacity)"))

items.append(P(95, "Design Hit Counter", "Medium", "Queue / circular buf",
"hit(timestamp) and getHits(timestamp) = hits in past 300 seconds (inclusive).",
"""export class HitCounter {
  private q: number[] = []
  hit(timestamp: number): void {
    this.q.push(timestamp)
  }
  getHits(timestamp: number): number {
    while (this.q.length && this.q[0] <= timestamp - 300) this.q.shift()
    return this.q.length
  }
}""",
"Drop timestamps outside window; queue length is answer.", "O(1) amortized", "O(W)",
"For high QPS: 300 buckets of counts."))

items.append(P(96, "Logger Rate Limiter", "Medium", "HashMap",
"shouldPrintMessage(timestamp, message): true if same message not printed in last 10s.",
"""export class Logger {
  private last = new Map<string, number>()
  shouldPrintMessage(timestamp: number, message: string): boolean {
    const prev = this.last.get(message)
    if (prev !== undefined && timestamp - prev < 10) return false
    this.last.set(message, timestamp)
    return true
  }
}""",
"Store last print time per message.", "O(1)", "O(unique messages)"))

items.append(P(97, "Design Browser History", "Medium", "Two stacks / array",
"visit(url), back(steps), forward(steps) browser history.",
"""export class BrowserHistory {
  private hist: string[] = []
  private i = 0
  constructor(homepage: string) { this.hist = [homepage] }

  visit(url: string): void {
    this.hist = this.hist.slice(0, this.i + 1)
    this.hist.push(url)
    this.i++
  }

  back(steps: number): string {
    this.i = Math.max(0, this.i - steps)
    return this.hist[this.i]
  }

  forward(steps: number): string {
    this.i = Math.min(this.hist.length - 1, this.i + steps)
    return this.hist[this.i]
  }
}""",
"Array + pointer; visit truncates forward history.", "O(1) / O(n) visit trunc", "O(n)"))

items.append(P(98, "Flatten Nested List Iterator", "Medium", "Stack",
"Iterator over nested list of integers (NestedInteger API).",
"""export interface NestedInteger {
  isInteger(): boolean
  getInteger(): number | null
  getList(): NestedInteger[]
}

export class NestedIterator {
  private stack: NestedInteger[]
  constructor(nestedList: NestedInteger[]) {
    this.stack = [...nestedList].reverse()
  }
  next(): number {
    return this.stack.pop()!.getInteger()!
  }
  hasNext(): boolean {
    while (this.stack.length) {
      const top = this.stack[this.stack.length - 1]
      if (top.isInteger()) return true
      this.stack.pop()
      const list = top.getList()
      for (let i = list.length - 1; i >= 0; i--) this.stack.push(list[i])
    }
    return false
  }
}""",
"Lazy flatten with stack; expand lists only when needed.", "O(1) amortized next", "O(n)"))

items.append(P(99, "Implement Trie (Prefix Tree)", "Medium", "Trie",
"Trie with insert, search, startsWith.",
"""class TrieNode {
  children = new Map<string, TrieNode>()
  isEnd = false
}

export class Trie {
  private root = new TrieNode()

  insert(word: string): void {
    let node = this.root
    for (const ch of word) {
      if (!node.children.has(ch)) node.children.set(ch, new TrieNode())
      node = node.children.get(ch)!
    }
    node.isEnd = true
  }

  search(word: string): boolean {
    const node = this.walk(word)
    return !!node?.isEnd
  }

  startsWith(prefix: string): boolean {
    return this.walk(prefix) !== null
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
}""",
"Path of characters; terminal flag for full word.", "O(L)", "O(total chars)"))

items.append(P(100, "Word Search II", "Hard", "Trie + DFS backtracking",
"Given board and words, return all words present on the board (4-dir, no reuse).",
"""export function findWords(board: string[][], words: string[]): string[] {
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
    if (next.word) { res.push(next.word); next.word = null }
    board[r][c] = '#'
    dfs(r + 1, c, next); dfs(r - 1, c, next); dfs(r, c + 1, next); dfs(r, c - 1, next)
    board[r][c] = ch
  }
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++) dfs(i, j, root)
  return res
}""",
"Build trie of dictionary; DFS board while walking trie; dedupe by clearing word.", "O(m·n·4·L)", "O(total dict chars)"))

table = [
(76, "Connected Components", "Union-Find"),
(77, "Redundant Connection", "Union-Find"),
(78, "Accounts Merge", "Union-Find"),
(79, "Graph Valid Tree", "Union-Find"),
(80, "Network Delay Time", "Dijkstra"),
(81, "Cheapest Flights K Stops", "Bellman-Ford"),
(82, "Alien Dictionary", "Topo"),
(83, "Course Schedule II", "Topo"),
(84, "Word Ladder", "BFS"),
(85, "Clone Graph BFS", "BFS"),
(86, "Surrounded Regions", "DFS borders"),
(87, "Walls and Gates", "Multi BFS"),
(88, "Rotting Oranges", "Multi BFS"),
(89, "Shortest Path Binary Matrix", "BFS"),
(90, "Pacific Atlantic", "Multi DFS"),
(91, "Longest Consecutive", "HashSet"),
(92, "Encode/Decode Strings", "Serialization"),
(93, "Insert Delete GetRandom", "Array+Map"),
(94, "LRU (Map order)", "Ordered Map"),
(95, "Hit Counter", "Queue"),
(96, "Logger Rate Limiter", "HashMap"),
(97, "Browser History", "Array pointer"),
(98, "Nested List Iterator", "Stack"),
(99, "Implement Trie", "Trie"),
(100, "Word Search II", "Trie+DFS"),
]

header = """# Problems 76–100

Graphs, Union-Find, design problems, and Trie — the hard half of the grind set.

| # | Problem | Pattern |
| --- | --- | --- |
""" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in table) + "\n\n---\n\n"

out = header + "\n---\n\n".join(items)
Path("/Users/prajjwal/jvl/interview/docs/coding/14-problems-76-100.md").write_text(out)
print("wrote", len(items), "bytes", len(out))
