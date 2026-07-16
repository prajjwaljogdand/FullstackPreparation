# Problems 1–25

Medium/hard TypeScript drills. Say the **pattern** before coding.

| # | Problem | Pattern |
| --- | --- | --- |
| 1 | Two Sum | HashMap |
| 2 | Longest Substring Without Repeating | Sliding window |
| 3 | Longest Palindromic Substring | Expand center |
| 4 | 3Sum | Two pointers |
| 5 | Container With Most Water | Two pointers |
| 6 | Group Anagrams | HashMap |
| 7 | Product Except Self | Prefix/suffix |
| 8 | Generate Parentheses | Backtracking |
| 9 | Merge Intervals | Intervals |
| 10 | Insert Interval | Intervals |
| 11 | Rotate Image | Matrix |
| 12 | Spiral Matrix | Simulation |
| 13 | Set Matrix Zeroes | Markers |
| 14 | Word Search | Backtracking |
| 15 | Number of Islands | DFS |
| 16 | Course Schedule | Topo |
| 17 | Clone Graph | Graph clone |
| 18 | Pacific Atlantic | Multi-source DFS |
| 19 | Kth Largest | Quickselect |
| 20 | Top K Frequent | Buckets |
| 21 | Merge K Sorted Lists | Heap |
| 22 | LRU Cache | DLL+Map |
| 23 | Decode Ways | DP |
| 24 | Unique Paths II | DP |
| 25 | Jump Game II | Greedy |

---

## 1. Two Sum (return indices)

**Difficulty:** Medium · **Pattern:** HashMap

Given `nums` and `target`, return indices of two numbers that add to `target`. Assume exactly one solution; cannot reuse same element.

### Solution

```ts
export function twoSum(nums: number[], target: number): [number, number] {
  const map = new Map<number, number>()
  for (let i = 0; i < nums.length; i++) {
    const need = target - nums[i]
    if (map.has(need)) return [map.get(need)!, i]
    map.set(nums[i], i)
  }
  throw new Error('No solution')
}
```

### Explanation

Store value→index while scanning. For each `x`, check if `target-x` already seen. One pass.

### Complexity

- **Time:** O(n)
- **Space:** O(n)

**Follow-up:** What if multiple pairs? Return all unique pairs of values — sort + two pointers.


---

## 2. Longest Substring Without Repeating Characters

**Difficulty:** Medium · **Pattern:** Sliding window

Given string `s`, find length of longest substring without repeating characters.

### Solution

```ts
export function lengthOfLongestSubstring(s: string): number {
  const last = new Map<string, number>()
  let left = 0, best = 0
  for (let right = 0; right < s.length; right++) {
    const c = s[right]
    if (last.has(c) && last.get(c)! >= left) left = last.get(c)! + 1
    last.set(c, right)
    best = Math.max(best, right - left + 1)
  }
  return best
}
```

### Explanation

Maintain window `[left,right]` with unique chars via last-seen index. On duplicate inside window, jump `left`.

### Complexity

- **Time:** O(n)
- **Space:** O(min(n, Σ))


---

## 3. Longest Palindromic Substring

**Difficulty:** Medium · **Pattern:** Expand around center

Return the longest palindromic substring of `s`.

### Solution

```ts
export function longestPalindrome(s: string): string {
  let start = 0, end = 0
  const expand = (l: number, r: number) => {
    while (l >= 0 && r < s.length && s[l] === s[r]) { l--; r++ }
    return [l + 1, r - 1] as const
  }
  for (let i = 0; i < s.length; i++) {
    for (const [l, r] of [expand(i, i), expand(i, i + 1)]) {
      if (r - l > end - start) { start = l; end = r }
    }
  }
  return s.slice(start, end + 1)
}
```

### Explanation

Every palindrome expands from a center (odd) or between two chars (even). Track max.

### Complexity

- **Time:** O(n²)
- **Space:** O(1)

**Follow-up:** Manacher O(n) for hard follow-up.


---

## 4. 3Sum

**Difficulty:** Medium · **Pattern:** Sort + two pointers

Return all unique triplets that sum to 0.

### Solution

```ts
export function threeSum(nums: number[]): number[][] {
  nums.sort((a, b) => a - b)
  const res: number[][] = []
  for (let i = 0; i < nums.length - 2; i++) {
    if (i > 0 && nums[i] === nums[i - 1]) continue
    let lo = i + 1, hi = nums.length - 1
    while (lo < hi) {
      const sum = nums[i] + nums[lo] + nums[hi]
      if (sum === 0) {
        res.push([nums[i], nums[lo], nums[hi]])
        while (lo < hi && nums[lo] === nums[lo + 1]) lo++
        while (lo < hi && nums[hi] === nums[hi - 1]) hi--
        lo++; hi--
      } else if (sum < 0) lo++
      else hi--
    }
  }
  return res
}
```

### Explanation

Fix `i`, two-sum on sorted remainder. Skip duplicates at all three pointers.

### Complexity

- **Time:** O(n²)
- **Space:** O(1) extra (ignoring output)


---

## 5. Container With Most Water

**Difficulty:** Medium · **Pattern:** Two pointers

Heights array forms vertical lines; max water area between two lines.

### Solution

```ts
export function maxArea(height: number[]): number {
  let lo = 0, hi = height.length - 1, best = 0
  while (lo < hi) {
    best = Math.max(best, Math.min(height[lo], height[hi]) * (hi - lo))
    if (height[lo] < height[hi]) lo++
    else hi--
  }
  return best
}
```

### Explanation

Width starts max. Move the shorter side inward — only way to possibly improve area.

### Complexity

- **Time:** O(n)
- **Space:** O(1)


---

## 6. Group Anagrams

**Difficulty:** Medium · **Pattern:** HashMap + signature

Group strings that are anagrams of each other.

### Solution

```ts
export function groupAnagrams(strs: string[]): string[][] {
  const map = new Map<string, string[]>()
  for (const s of strs) {
    const key = s.split('').sort().join('')
    if (!map.has(key)) map.set(key, [])
    map.get(key)!.push(s)
  }
  return [...map.values()]
}
```

### Explanation

Canonical key = sorted chars (or 26-count tuple). Bucket by key.

### Complexity

- **Time:** O(n · k log k)
- **Space:** O(n · k)

**Follow-up:** Count-array key is O(n·k) and better for long strings.


---

## 7. Product of Array Except Self

**Difficulty:** Medium · **Pattern:** Prefix / suffix

Return array `answer` where `answer[i]` is product of all elements except `nums[i]`. O(n) without division.

### Solution

```ts
export function productExceptSelf(nums: number[]): number[] {
  const n = nums.length
  const ans = Array(n).fill(1)
  let pref = 1
  for (let i = 0; i < n; i++) { ans[i] = pref; pref *= nums[i] }
  let suff = 1
  for (let i = n - 1; i >= 0; i--) { ans[i] *= suff; suff *= nums[i] }
  return ans
}
```

### Explanation

Left pass stores prefix products; right pass multiplies suffix products in place.

### Complexity

- **Time:** O(n)
- **Space:** O(1) extra


---

## 8. Valid Parentheses / Generate Parentheses

**Difficulty:** Medium · **Pattern:** Stack / Backtracking

Generate all combinations of `n` pairs of well-formed parentheses.

### Solution

```ts
export function generateParenthesis(n: number): string[] {
  const res: string[] = []
  const dfs = (s: string, open: number, close: number) => {
    if (s.length === 2 * n) { res.push(s); return }
    if (open < n) dfs(s + '(', open + 1, close)
    if (close < open) dfs(s + ')', open, close + 1)
  }
  dfs('', 0, 0)
  return res
}
```

### Explanation

Never add `)` if it would exceed `(`. Catalan-number count of solutions.

### Complexity

- **Time:** O(4^n / √n)
- **Space:** O(n) recursion


---

## 9. Merge Intervals

**Difficulty:** Medium · **Pattern:** Intervals

Merge all overlapping intervals.

### Solution

```ts
export function merge(intervals: number[][]): number[][] {
  intervals.sort((a, b) => a[0] - b[0])
  const out: number[][] = []
  for (const [s, e] of intervals) {
    if (!out.length || out[out.length - 1][1] < s) out.push([s, e])
    else out[out.length - 1][1] = Math.max(out[out.length - 1][1], e)
  }
  return out
}
```

### Explanation

Sort by start. Overlap iff `start ≤ lastEnd`; extend end.

### Complexity

- **Time:** O(n log n)
- **Space:** O(n)


---

## 10. Insert Interval

**Difficulty:** Medium · **Pattern:** Intervals

Insert `newInterval` into sorted non-overlapping intervals and merge if needed.

### Solution

```ts
export function insert(intervals: number[][], newInterval: number[]): number[][] {
  const res: number[][] = []
  let i = 0
  const n = intervals.length
  while (i < n && intervals[i][1] < newInterval[0]) res.push(intervals[i++])
  while (i < n && intervals[i][0] <= newInterval[1]) {
    newInterval[0] = Math.min(newInterval[0], intervals[i][0])
    newInterval[1] = Math.max(newInterval[1], intervals[i][1])
    i++
  }
  res.push(newInterval)
  while (i < n) res.push(intervals[i++])
  return res
}
```

### Explanation

Three phases: before, merge-overlapping, after. Linear since input sorted.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 11. Rotate Image (matrix 90°)

**Difficulty:** Medium · **Pattern:** Matrix

Rotate n×n matrix 90° clockwise in-place.

### Solution

```ts
export function rotate(matrix: number[][]): void {
  const n = matrix.length
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      [matrix[i][j], matrix[j][i]] = [matrix[j][i], matrix[i][j]]
    }
  }
  for (const row of matrix) row.reverse()
}
```

### Explanation

Transpose then reverse each row. Equivalent layer-cycle swaps.

### Complexity

- **Time:** O(n²)
- **Space:** O(1)


---

## 12. Spiral Matrix

**Difficulty:** Medium · **Pattern:** Simulation

Return all elements of matrix in spiral order.

### Solution

```ts
export function spiralOrder(matrix: number[][]): number[] {
  const res: number[] = []
  let top = 0, bottom = matrix.length - 1, left = 0, right = matrix[0].length - 1
  while (top <= bottom && left <= right) {
    for (let c = left; c <= right; c++) res.push(matrix[top][c])
    top++
    for (let r = top; r <= bottom; r++) res.push(matrix[r][right])
    right--
    if (top <= bottom) {
      for (let c = right; c >= left; c--) res.push(matrix[bottom][c])
      bottom--
    }
    if (left <= right) {
      for (let r = bottom; r >= top; r--) res.push(matrix[r][left])
      left++
    }
  }
  return res
}
```

### Explanation

Shrink bounds after each side. Guard single row/col double-count.

### Complexity

- **Time:** O(m·n)
- **Space:** O(1) extra


---

## 13. Set Matrix Zeroes

**Difficulty:** Medium · **Pattern:** Matrix markers

If an element is 0, set its entire row and column to 0. In-place O(1) extra space.

### Solution

```ts
export function setZeroes(matrix: number[][]): void {
  const m = matrix.length, n = matrix[0].length
  let firstRow = false, firstCol = false
  for (let j = 0; j < n; j++) if (matrix[0][j] === 0) firstRow = true
  for (let i = 0; i < m; i++) if (matrix[i][0] === 0) firstCol = true
  for (let i = 1; i < m; i++) {
    for (let j = 1; j < n; j++) {
      if (matrix[i][j] === 0) { matrix[i][0] = 0; matrix[0][j] = 0 }
    }
  }
  for (let i = 1; i < m; i++)
    for (let j = 1; j < n; j++)
      if (matrix[i][0] === 0 || matrix[0][j] === 0) matrix[i][j] = 0
  if (firstRow) for (let j = 0; j < n; j++) matrix[0][j] = 0
  if (firstCol) for (let i = 0; i < m; i++) matrix[i][0] = 0
}
```

### Explanation

Use first row/col as markers; remember if they themselves need zeroing.

### Complexity

- **Time:** O(m·n)
- **Space:** O(1)


---

## 14. Word Search

**Difficulty:** Medium · **Pattern:** Backtracking on grid

Does `word` exist in grid by adjacent (4-dir) cells without reuse?

### Solution

```ts
export function exist(board: string[][], word: string): boolean {
  const m = board.length, n = board[0].length
  const dfs = (r: number, c: number, i: number): boolean => {
    if (i === word.length) return true
    if (r < 0 || c < 0 || r >= m || c >= n || board[r][c] !== word[i]) return false
    const tmp = board[r][c]
    board[r][c] = '#'
    const found =
      dfs(r + 1, c, i + 1) || dfs(r - 1, c, i + 1) ||
      dfs(r, c + 1, i + 1) || dfs(r, c - 1, i + 1)
    board[r][c] = tmp
    return found
  }
  for (let r = 0; r < m; r++)
    for (let c = 0; c < n; c++)
      if (dfs(r, c, 0)) return true
  return false
}
```

### Explanation

DFS + mark visited in-place, restore on backtrack.

### Complexity

- **Time:** O(m·n·4^L)
- **Space:** O(L)


---

## 15. Number of Islands

**Difficulty:** Medium · **Pattern:** DFS/BFS grid

Count islands of `'1'` in grid (4-connected).

### Solution

```ts
export function numIslands(grid: string[][]): number {
  let count = 0
  const m = grid.length, n = grid[0].length
  const dfs = (r: number, c: number) => {
    if (r < 0 || c < 0 || r >= m || c >= n || grid[r][c] !== '1') return
    grid[r][c] = '0'
    dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)
  }
  for (let r = 0; r < m; r++)
    for (let c = 0; c < n; c++)
      if (grid[r][c] === '1') { count++; dfs(r, c) }
  return count
}
```

### Explanation

Each unvisited land starts a component; flood fill marks the island.

### Complexity

- **Time:** O(m·n)
- **Space:** O(m·n) worst recursion


---

## 16. Course Schedule

**Difficulty:** Medium · **Pattern:** Topo / cycle detection

`numCourses` courses, `prerequisites[i] = [a,b]` means b→a. Return true if you can finish all.

### Solution

```ts
export function canFinish(numCourses: number, prerequisites: number[][]): boolean {
  const g: number[][] = Array.from({ length: numCourses }, () => [])
  const indeg = Array(numCourses).fill(0)
  for (const [a, b] of prerequisites) { g[b].push(a); indeg[a]++ }
  const q: number[] = []
  for (let i = 0; i < numCourses; i++) if (indeg[i] === 0) q.push(i)
  let taken = 0
  for (let i = 0; i < q.length; i++) {
    const u = q[i]; taken++
    for (const v of g[u]) if (--indeg[v] === 0) q.push(v)
  }
  return taken === numCourses
}
```

### Explanation

Kahn topological sort; leftover nodes with indegree > 0 ⇒ cycle.

### Complexity

- **Time:** O(V+E)
- **Space:** O(V+E)


---

## 17. Clone Graph

**Difficulty:** Medium · **Pattern:** BFS/DFS + HashMap

Deep clone a connected undirected graph of nodes with `val` and `neighbors`.

### Solution

```ts
class Node { val: number; neighbors: Node[]; constructor(val = 0, neighbors: Node[] = []) { this.val = val; this.neighbors = neighbors } }

export function cloneGraph(node: Node | null): Node | null {
  if (!node) return null
  const map = new Map<Node, Node>()
  const dfs = (n: Node): Node => {
    if (map.has(n)) return map.get(n)!
    const copy = new Node(n.val)
    map.set(n, copy)
    copy.neighbors = n.neighbors.map(dfs)
    return copy
  }
  return dfs(node)
}
```

### Explanation

Map original→clone to break cycles; clone neighbors recursively.

### Complexity

- **Time:** O(V+E)
- **Space:** O(V)


---

## 18. Pacific Atlantic Water Flow

**Difficulty:** Medium · **Pattern:** Multi-source BFS/DFS

Heights matrix; rain flows to equal/lower neighbors. Return cells that can flow to both Pacific (top/left) and Atlantic (bottom/right).

### Solution

```ts
export function pacificAtlantic(heights: number[][]): number[][] {
  const m = heights.length, n = heights[0].length
  const pac = Array.from({ length: m }, () => Array(n).fill(false))
  const atl = Array.from({ length: m }, () => Array(n).fill(false))
  const dfs = (r: number, c: number, seen: boolean[][], h: number) => {
    if (r < 0 || c < 0 || r >= m || c >= n || seen[r][c] || heights[r][c] < h) return
    seen[r][c] = true
    dfs(r+1,c,seen,heights[r][c]); dfs(r-1,c,seen,heights[r][c])
    dfs(r,c+1,seen,heights[r][c]); dfs(r,c-1,seen,heights[r][c])
  }
  for (let i = 0; i < m; i++) { dfs(i, 0, pac, 0); dfs(i, n - 1, atl, 0) }
  for (let j = 0; j < n; j++) { dfs(0, j, pac, 0); dfs(m - 1, j, atl, 0) }
  const res: number[][] = []
  for (let i = 0; i < m; i++)
    for (let j = 0; j < n; j++)
      if (pac[i][j] && atl[i][j]) res.push([i, j])
  return res
}
```

### Explanation

Flow reverse: from oceans uphill. Intersection of reachable sets.

### Complexity

- **Time:** O(m·n)
- **Space:** O(m·n)


---

## 19. Kth Largest Element in an Array

**Difficulty:** Medium · **Pattern:** Quickselect / Heap

Find the k-th largest element (1-indexed from largest).

### Solution

```ts
export function findKthLargest(nums: number[], k: number): number {
  const target = nums.length - k // kth largest = index in ascending
  const swap = (i: number, j: number) => { [nums[i], nums[j]] = [nums[j], nums[i]] }
  const partition = (lo: number, hi: number) => {
    const pivot = nums[hi]
    let i = lo
    for (let j = lo; j < hi; j++) if (nums[j] <= pivot) swap(i++, j)
    swap(i, hi)
    return i
  }
  let lo = 0, hi = nums.length - 1
  while (true) {
    const p = partition(lo, hi)
    if (p === target) return nums[p]
    if (p < target) lo = p + 1
    else hi = p - 1
  }
}
```

### Explanation

Quickselect average O(n). Min-heap of size k is alternative O(n log k).

### Complexity

- **Time:** O(n) average
- **Space:** O(1)


---

## 20. Top K Frequent Elements

**Difficulty:** Medium · **Pattern:** Heap / Bucket

Return k most frequent elements.

### Solution

```ts
export function topKFrequent(nums: number[], k: number): number[] {
  const freq = new Map<number, number>()
  for (const x of nums) freq.set(x, (freq.get(x) ?? 0) + 1)
  const buckets: number[][] = Array.from({ length: nums.length + 1 }, () => [])
  for (const [num, f] of freq) buckets[f].push(num)
  const res: number[] = []
  for (let f = buckets.length - 1; f >= 0 && res.length < k; f--) {
    for (const num of buckets[f]) {
      res.push(num)
      if (res.length === k) return res
    }
  }
  return res
}
```

### Explanation

Frequency → bucket index. Scan high frequencies down.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 21. Merge K Sorted Lists

**Difficulty:** Hard · **Pattern:** Heap

Merge k sorted linked lists into one sorted list.

### Solution

```ts
class ListNode { val: number; next: ListNode | null; constructor(val = 0, next: ListNode | null = null) { this.val = val; this.next = next } }

class MinHeap {
  data: ListNode[] = []
  push(n: ListNode) {
    this.data.push(n)
    let i = this.data.length - 1
    while (i > 0) {
      const p = (i - 1) >> 1
      if (this.data[p].val <= this.data[i].val) break
      ;[this.data[p], this.data[i]] = [this.data[i], this.data[p]]
      i = p
    }
  }
  pop(): ListNode | undefined {
    if (!this.data.length) return undefined
    const top = this.data[0]
    const last = this.data.pop()!
    if (this.data.length) {
      this.data[0] = last
      let i = 0
      while (true) {
        let s = i
        const l = i * 2 + 1, r = l + 1
        if (l < this.data.length && this.data[l].val < this.data[s].val) s = l
        if (r < this.data.length && this.data[r].val < this.data[s].val) s = r
        if (s === i) break
        ;[this.data[i], this.data[s]] = [this.data[s], this.data[i]]
        i = s
      }
    }
    return top
  }
}

export function mergeKLists(lists: Array<ListNode | null>): ListNode | null {
  const heap = new MinHeap()
  for (const node of lists) if (node) heap.push(node)
  const dummy = new ListNode()
  let cur = dummy
  while (heap.data.length) {
    const n = heap.pop()!
    cur.next = n
    cur = n
    if (n.next) heap.push(n.next)
  }
  return dummy.next
}
```

### Explanation

Min-heap of current heads. Always pop smallest; push its next.

### Complexity

- **Time:** O(N log k)
- **Space:** O(k)


---

## 22. LRU Cache

**Difficulty:** Hard · **Pattern:** HashMap + DLL

Design LRU with O(1) `get` and `put`.

### Solution

```ts
class Node { key: number; val: number; prev: Node | null = null; next: Node | null = null
  constructor(key: number, val: number) { this.key = key; this.val = val } }

export class LRUCache {
  private map = new Map<number, Node>()
  private head = new Node(0, 0)
  private tail = new Node(0, 0)
  constructor(private capacity: number) {
    this.head.next = this.tail; this.tail.prev = this.head
  }
  get(key: number): number {
    const node = this.map.get(key)
    if (!node) return -1
    this.moveToHead(node)
    return node.val
  }
  put(key: number, value: number): void {
    const existing = this.map.get(key)
    if (existing) { existing.val = value; this.moveToHead(existing); return }
    const node = new Node(key, value)
    this.map.set(key, node)
    this.addToHead(node)
    if (this.map.size > this.capacity) {
      const lru = this.tail.prev!
      this.remove(lru)
      this.map.delete(lru.key)
    }
  }
  private addToHead(n: Node) {
    n.prev = this.head; n.next = this.head.next
    this.head.next!.prev = n; this.head.next = n
  }
  private remove(n: Node) { n.prev!.next = n.next; n.next!.prev = n.prev }
  private moveToHead(n: Node) { this.remove(n); this.addToHead(n) }
}
```

### Explanation

MRU at head; evict tail. Map for O(1) lookup.

### Complexity

- **Time:** O(1)
- **Space:** O(capacity)


---

## 23. Decode Ways

**Difficulty:** Medium · **Pattern:** DP

A message containing digits is encoded `1→A` … `26→Z`. Count ways to decode.

### Solution

```ts
export function numDecodings(s: string): number {
  if (!s.length || s[0] === '0') return 0
  let prev2 = 1, prev1 = 1 // dp[i-2], dp[i-1]
  for (let i = 1; i < s.length; i++) {
    let cur = 0
    if (s[i] !== '0') cur += prev1
    const two = Number(s.slice(i - 1, i + 1))
    if (two >= 10 && two <= 26) cur += prev2
    prev2 = prev1; prev1 = cur
    if (cur === 0) return 0
  }
  return prev1
}
```

### Explanation

`dp[i] = (single digit ok ? dp[i-1] : 0) + (two-digit ok ? dp[i-2] : 0)`.

### Complexity

- **Time:** O(n)
- **Space:** O(1)


---

## 24. Unique Paths II

**Difficulty:** Medium · **Pattern:** DP grid

Robot from top-left to bottom-right; obstacles marked 1. Count paths.

### Solution

```ts
export function uniquePathsWithObstacles(obstacleGrid: number[][]): number {
  const m = obstacleGrid.length, n = obstacleGrid[0].length
  if (obstacleGrid[0][0] === 1) return 0
  const dp = Array(n).fill(0)
  dp[0] = 1
  for (let i = 0; i < m; i++) {
    for (let j = 0; j < n; j++) {
      if (obstacleGrid[i][j] === 1) dp[j] = 0
      else if (j > 0) dp[j] += dp[j - 1]
    }
  }
  return dp[n - 1]
}
```

### Explanation

1D DP: cell gets left + up; obstacle zeroes contribution.

### Complexity

- **Time:** O(m·n)
- **Space:** O(n)


---

## 25. Jump Game II

**Difficulty:** Medium · **Pattern:** Greedy BFS levels

Each index has jump length; return minimum jumps to last index. Guaranteed reachable.

### Solution

```ts
export function jump(nums: number[]): number {
  let jumps = 0, curEnd = 0, farthest = 0
  for (let i = 0; i < nums.length - 1; i++) {
    farthest = Math.max(farthest, i + nums[i])
    if (i === curEnd) { jumps++; curEnd = farthest }
  }
  return jumps
}
```

### Explanation

Treat as BFS by jump range. When finishing current level, jump++ and expand end.

### Complexity

- **Time:** O(n)
- **Space:** O(1)

