# Coding Problems 76–100

Harder interview patterns: binary search on answer, BFS graphs, trees, sliding windows, heaps, topo sort.

## Problem 76. Median of Two Sorted Arrays

### Explanation
Binary search partition so left halves are ≤ right halves.

### Solution

```ts
function findMedianSortedArrays(a: number[], b: number[]): number {
  if (a.length > b.length) return findMedianSortedArrays(b, a)
  const m = a.length, n = b.length
  let lo = 0, hi = m
  while (lo <= hi) {
    const i = (lo + hi) >> 1
    const j = ((m + n + 1) >> 1) - i
    const aL = i === 0 ? -Infinity : a[i - 1]
    const aR = i === m ? Infinity : a[i]
    const bL = j === 0 ? -Infinity : b[j - 1]
    const bR = j === n ? Infinity : b[j]
    if (aL <= bR && bL <= aR) {
      if ((m + n) % 2) return Math.max(aL, bL)
      return (Math.max(aL, bL) + Math.min(aR, bR)) / 2
    }
    if (aL > bR) hi = i - 1
    else lo = i + 1
  }
  throw new Error('unreachable')
}
```

### Complexity
O(log(min(m,n))) time, O(1) space

## Problem 77. Word Ladder Length

### Explanation
Shortest transformation = BFS on implicit graph of words.

### Solution

```ts
function ladderLength(begin: string, end: string, wordList: string[]): number {
  const words = new Set(wordList)
  if (!words.has(end)) return 0
  const q: [string, number][] = [[begin, 1]]
  const seen = new Set([begin])
  while (q.length) {
    const [w, d] = q.shift()!
    if (w === end) return d
    const arr = w.split('')
    for (let i = 0; i < arr.length; i++) {
      const orig = arr[i]
      for (let c = 97; c <= 122; c++) {
        arr[i] = String.fromCharCode(c)
        const nw = arr.join('')
        if (words.has(nw) && !seen.has(nw)) {
          seen.add(nw)
          q.push([nw, d + 1])
        }
      }
      arr[i] = orig
    }
  }
  return 0
}
```

### Complexity
O(N * L * 26) BFS

## Problem 78. Serialize / Deserialize Binary Tree

### Explanation
Preorder with null markers is unambiguous.

### Solution

```ts
class TreeNode { constructor(public val = 0, public left: TreeNode | null = null, public right: TreeNode | null = null) {} }
function serialize(root: TreeNode | null): string {
  const out: string[] = []
  const dfs = (n: TreeNode | null) => {
    if (!n) { out.push('#'); return }
    out.push(String(n.val))
    dfs(n.left); dfs(n.right)
  }
  dfs(root)
  return out.join(',')
}
function deserialize(data: string): TreeNode | null {
  const vals = data.split(',')
  let i = 0
  const dfs = (): TreeNode | null => {
    const v = vals[i++]
    if (v === '#') return null
    const node = new TreeNode(Number(v))
    node.left = dfs(); node.right = dfs()
    return node
  }
  return dfs()
}
```

### Complexity
O(n) time/space

## Problem 79. Trapping Rain Water

### Explanation
Two pointers — water bounded by the smaller side max.

### Solution

```ts
function trap(height: number[]): number {
  let l = 0, r = height.length - 1, lMax = 0, rMax = 0, water = 0
  while (l < r) {
    if (height[l] < height[r]) {
      lMax = Math.max(lMax, height[l])
      water += lMax - height[l]
      l++
    } else {
      rMax = Math.max(rMax, height[r])
      water += rMax - height[r]
      r--
    }
  }
  return water
}
```

### Complexity
O(n) time, O(1) space

## Problem 80. Minimum Window Substring

### Explanation
Sliding window shrink when all chars covered.

### Solution

```ts
function minWindow(s: string, t: string): string {
  const need = new Map<string, number>()
  for (const ch of t) need.set(ch, (need.get(ch) ?? 0) + 1)
  let missing = t.length, start = 0, best = '', bestLen = Infinity
  for (let end = 0; end < s.length; end++) {
    const c = s[end]
    if ((need.get(c) ?? 0) > 0) missing--
    need.set(c, (need.get(c) ?? 0) - 1)
    while (missing === 0) {
      if (end - start + 1 < bestLen) {
        bestLen = end - start + 1
        best = s.slice(start, end + 1)
      }
      const L = s[start++]
      need.set(L, (need.get(L) ?? 0) + 1)
      if ((need.get(L) ?? 0) > 0) missing++
    }
  }
  return best
}
```

### Complexity
O(|s| + |t|)

## Problem 81. Course Schedule II (Topo)

### Explanation
Kahn BFS topological sort; empty if cycle.

### Solution

```ts
function findOrder(numCourses: number, prerequisites: number[][]): number[] {
  const g = Array.from({ length: numCourses }, () => [] as number[])
  const indeg = Array(numCourses).fill(0)
  for (const [a, b] of prerequisites) { g[b].push(a); indeg[a]++ }
  const q = indeg.map((d, i) => (d === 0 ? i : -1)).filter((i) => i >= 0)
  const order: number[] = []
  while (q.length) {
    const u = q.shift()!
    order.push(u)
    for (const v of g[u]) if (--indeg[v] === 0) q.push(v)
  }
  return order.length === numCourses ? order : []
}
```

### Complexity
O(V+E)

## Problem 82. LRU get/put (sketch test)

### Explanation
JS Map preserves insertion order — delete+set moves to newest.

### Solution

```ts
// See coding/05-lru — implement Map + doubly linked list
class LRUCache {
  private map = new Map<number, number>()
  constructor(private capacity: number) {}
  get(key: number) {
    if (!this.map.has(key)) return -1
    const v = this.map.get(key)!
    this.map.delete(key); this.map.set(key, v)
    return v
  }
  put(key: number, value: number) {
    if (this.map.has(key)) this.map.delete(key)
    this.map.set(key, value)
    if (this.map.size > this.capacity) {
      const oldest = this.map.keys().next().value!
      this.map.delete(oldest)
    }
  }
}
```

### Complexity
O(1) amortized with Map insertion order

## Problem 83. Alien Dictionary

### Explanation
Build precedence graph from adjacent words; topo sort.

### Solution

```ts
function alienOrder(words: string[]): string {
  const g = new Map<string, Set<string>>()
  const indeg = new Map<string, number>()
  for (const w of words) for (const c of w) {
    if (!g.has(c)) g.set(c, new Set())
    if (!indeg.has(c)) indeg.set(c, 0)
  }
  for (let i = 0; i < words.length - 1; i++) {
    const a = words[i], b = words[i + 1]
    if (a.length > b.length && a.startsWith(b)) return ''
    for (let j = 0; j < Math.min(a.length, b.length); j++) {
      if (a[j] !== b[j]) {
        if (!g.get(a[j])!.has(b[j])) {
          g.get(a[j])!.add(b[j])
          indeg.set(b[j], (indeg.get(b[j]) ?? 0) + 1)
        }
        break
      }
    }
  }
  const q = [...indeg.entries()].filter(([, d]) => d === 0).map(([c]) => c)
  let out = ''
  while (q.length) {
    const u = q.shift()!
    out += u
    for (const v of g.get(u)!) {
      indeg.set(v, indeg.get(v)! - 1)
      if (indeg.get(v) === 0) q.push(v)
    }
  }
  return out.length === indeg.size ? out : ''
}
```

### Complexity
O(C) letters+edges

## Problem 84. Max Path Sum Binary Tree

### Explanation
Gain from child can be zeroed; path can bend at node.

### Solution

```ts
function maxPathSum(root: TreeNode): number {
  let best = -Infinity
  const dfs = (n: TreeNode | null): number => {
    if (!n) return 0
    const L = Math.max(0, dfs(n.left))
    const R = Math.max(0, dfs(n.right))
    best = Math.max(best, n.val + L + R)
    return n.val + Math.max(L, R)
  }
  dfs(root)
  return best
}
```

### Complexity
O(n)

## Problem 85. Merge k Sorted Lists

### Explanation
Min-heap of list heads.

### Solution

```ts
function mergeKLists(lists: Array<ListNode | null>): ListNode | null {
  const heap: ListNode[] = []
  const push = (n: ListNode) => {
    heap.push(n)
    let i = heap.length - 1
    while (i > 0) {
      const p = (i - 1) >> 1
      if (heap[p].val <= heap[i].val) break
      ;[heap[p], heap[i]] = [heap[i], heap[p]]
      i = p
    }
  }
  const pop = () => {
    const top = heap[0]
    const last = heap.pop()!
    if (!heap.length) return top
    heap[0] = last
    let i = 0
    for (;;) {
      let s = i
      const l = i * 2 + 1, r = l + 1
      if (l < heap.length && heap[l].val < heap[s].val) s = l
      if (r < heap.length && heap[r].val < heap[s].val) s = r
      if (s === i) break
      ;[heap[s], heap[i]] = [heap[i], heap[s]]
      i = s
    }
    return top
  }
  for (const n of lists) if (n) push(n)
  const dummy = new ListNode(0)
  let cur = dummy
  while (heap.length) {
    const n = pop()
    cur.next = n
    cur = n
    if (n.next) push(n.next)
  }
  return dummy.next
}
```

### Complexity
O(N log k)

## Problem 86. Median of Two Sorted Arrays (variant 2)

### Explanation
Binary search partition so left halves are ≤ right halves.

### Solution

```ts
function findMedianSortedArrays(a: number[], b: number[]): number {
  if (a.length > b.length) return findMedianSortedArrays(b, a)
  const m = a.length, n = b.length
  let lo = 0, hi = m
  while (lo <= hi) {
    const i = (lo + hi) >> 1
    const j = ((m + n + 1) >> 1) - i
    const aL = i === 0 ? -Infinity : a[i - 1]
    const aR = i === m ? Infinity : a[i]
    const bL = j === 0 ? -Infinity : b[j - 1]
    const bR = j === n ? Infinity : b[j]
    if (aL <= bR && bL <= aR) {
      if ((m + n) % 2) return Math.max(aL, bL)
      return (Math.max(aL, bL) + Math.min(aR, bR)) / 2
    }
    if (aL > bR) hi = i - 1
    else lo = i + 1
  }
  throw new Error('unreachable')
}
```

### Complexity
O(log(min(m,n))) time, O(1) space

## Problem 87. Word Ladder Length (variant 2)

### Explanation
Shortest transformation = BFS on implicit graph of words.

### Solution

```ts
function ladderLength(begin: string, end: string, wordList: string[]): number {
  const words = new Set(wordList)
  if (!words.has(end)) return 0
  const q: [string, number][] = [[begin, 1]]
  const seen = new Set([begin])
  while (q.length) {
    const [w, d] = q.shift()!
    if (w === end) return d
    const arr = w.split('')
    for (let i = 0; i < arr.length; i++) {
      const orig = arr[i]
      for (let c = 97; c <= 122; c++) {
        arr[i] = String.fromCharCode(c)
        const nw = arr.join('')
        if (words.has(nw) && !seen.has(nw)) {
          seen.add(nw)
          q.push([nw, d + 1])
        }
      }
      arr[i] = orig
    }
  }
  return 0
}
```

### Complexity
O(N * L * 26) BFS

## Problem 88. Serialize / Deserialize Binary Tree (variant 2)

### Explanation
Preorder with null markers is unambiguous.

### Solution

```ts
class TreeNode { constructor(public val = 0, public left: TreeNode | null = null, public right: TreeNode | null = null) {} }
function serialize(root: TreeNode | null): string {
  const out: string[] = []
  const dfs = (n: TreeNode | null) => {
    if (!n) { out.push('#'); return }
    out.push(String(n.val))
    dfs(n.left); dfs(n.right)
  }
  dfs(root)
  return out.join(',')
}
function deserialize(data: string): TreeNode | null {
  const vals = data.split(',')
  let i = 0
  const dfs = (): TreeNode | null => {
    const v = vals[i++]
    if (v === '#') return null
    const node = new TreeNode(Number(v))
    node.left = dfs(); node.right = dfs()
    return node
  }
  return dfs()
}
```

### Complexity
O(n) time/space

## Problem 89. Trapping Rain Water (variant 2)

### Explanation
Two pointers — water bounded by the smaller side max.

### Solution

```ts
function trap(height: number[]): number {
  let l = 0, r = height.length - 1, lMax = 0, rMax = 0, water = 0
  while (l < r) {
    if (height[l] < height[r]) {
      lMax = Math.max(lMax, height[l])
      water += lMax - height[l]
      l++
    } else {
      rMax = Math.max(rMax, height[r])
      water += rMax - height[r]
      r--
    }
  }
  return water
}
```

### Complexity
O(n) time, O(1) space

## Problem 90. Minimum Window Substring (variant 2)

### Explanation
Sliding window shrink when all chars covered.

### Solution

```ts
function minWindow(s: string, t: string): string {
  const need = new Map<string, number>()
  for (const ch of t) need.set(ch, (need.get(ch) ?? 0) + 1)
  let missing = t.length, start = 0, best = '', bestLen = Infinity
  for (let end = 0; end < s.length; end++) {
    const c = s[end]
    if ((need.get(c) ?? 0) > 0) missing--
    need.set(c, (need.get(c) ?? 0) - 1)
    while (missing === 0) {
      if (end - start + 1 < bestLen) {
        bestLen = end - start + 1
        best = s.slice(start, end + 1)
      }
      const L = s[start++]
      need.set(L, (need.get(L) ?? 0) + 1)
      if ((need.get(L) ?? 0) > 0) missing++
    }
  }
  return best
}
```

### Complexity
O(|s| + |t|)

## Problem 91. Course Schedule II (Topo) (variant 2)

### Explanation
Kahn BFS topological sort; empty if cycle.

### Solution

```ts
function findOrder(numCourses: number, prerequisites: number[][]): number[] {
  const g = Array.from({ length: numCourses }, () => [] as number[])
  const indeg = Array(numCourses).fill(0)
  for (const [a, b] of prerequisites) { g[b].push(a); indeg[a]++ }
  const q = indeg.map((d, i) => (d === 0 ? i : -1)).filter((i) => i >= 0)
  const order: number[] = []
  while (q.length) {
    const u = q.shift()!
    order.push(u)
    for (const v of g[u]) if (--indeg[v] === 0) q.push(v)
  }
  return order.length === numCourses ? order : []
}
```

### Complexity
O(V+E)

## Problem 92. LRU get/put (sketch test) (variant 2)

### Explanation
JS Map preserves insertion order — delete+set moves to newest.

### Solution

```ts
// See coding/05-lru — implement Map + doubly linked list
class LRUCache {
  private map = new Map<number, number>()
  constructor(private capacity: number) {}
  get(key: number) {
    if (!this.map.has(key)) return -1
    const v = this.map.get(key)!
    this.map.delete(key); this.map.set(key, v)
    return v
  }
  put(key: number, value: number) {
    if (this.map.has(key)) this.map.delete(key)
    this.map.set(key, value)
    if (this.map.size > this.capacity) {
      const oldest = this.map.keys().next().value!
      this.map.delete(oldest)
    }
  }
}
```

### Complexity
O(1) amortized with Map insertion order

## Problem 93. Alien Dictionary (variant 2)

### Explanation
Build precedence graph from adjacent words; topo sort.

### Solution

```ts
function alienOrder(words: string[]): string {
  const g = new Map<string, Set<string>>()
  const indeg = new Map<string, number>()
  for (const w of words) for (const c of w) {
    if (!g.has(c)) g.set(c, new Set())
    if (!indeg.has(c)) indeg.set(c, 0)
  }
  for (let i = 0; i < words.length - 1; i++) {
    const a = words[i], b = words[i + 1]
    if (a.length > b.length && a.startsWith(b)) return ''
    for (let j = 0; j < Math.min(a.length, b.length); j++) {
      if (a[j] !== b[j]) {
        if (!g.get(a[j])!.has(b[j])) {
          g.get(a[j])!.add(b[j])
          indeg.set(b[j], (indeg.get(b[j]) ?? 0) + 1)
        }
        break
      }
    }
  }
  const q = [...indeg.entries()].filter(([, d]) => d === 0).map(([c]) => c)
  let out = ''
  while (q.length) {
    const u = q.shift()!
    out += u
    for (const v of g.get(u)!) {
      indeg.set(v, indeg.get(v)! - 1)
      if (indeg.get(v) === 0) q.push(v)
    }
  }
  return out.length === indeg.size ? out : ''
}
```

### Complexity
O(C) letters+edges

## Problem 94. Max Path Sum Binary Tree (variant 2)

### Explanation
Gain from child can be zeroed; path can bend at node.

### Solution

```ts
function maxPathSum(root: TreeNode): number {
  let best = -Infinity
  const dfs = (n: TreeNode | null): number => {
    if (!n) return 0
    const L = Math.max(0, dfs(n.left))
    const R = Math.max(0, dfs(n.right))
    best = Math.max(best, n.val + L + R)
    return n.val + Math.max(L, R)
  }
  dfs(root)
  return best
}
```

### Complexity
O(n)

## Problem 95. Merge k Sorted Lists (variant 2)

### Explanation
Min-heap of list heads.

### Solution

```ts
function mergeKLists(lists: Array<ListNode | null>): ListNode | null {
  const heap: ListNode[] = []
  const push = (n: ListNode) => {
    heap.push(n)
    let i = heap.length - 1
    while (i > 0) {
      const p = (i - 1) >> 1
      if (heap[p].val <= heap[i].val) break
      ;[heap[p], heap[i]] = [heap[i], heap[p]]
      i = p
    }
  }
  const pop = () => {
    const top = heap[0]
    const last = heap.pop()!
    if (!heap.length) return top
    heap[0] = last
    let i = 0
    for (;;) {
      let s = i
      const l = i * 2 + 1, r = l + 1
      if (l < heap.length && heap[l].val < heap[s].val) s = l
      if (r < heap.length && heap[r].val < heap[s].val) s = r
      if (s === i) break
      ;[heap[s], heap[i]] = [heap[i], heap[s]]
      i = s
    }
    return top
  }
  for (const n of lists) if (n) push(n)
  const dummy = new ListNode(0)
  let cur = dummy
  while (heap.length) {
    const n = pop()
    cur.next = n
    cur = n
    if (n.next) push(n.next)
  }
  return dummy.next
}
```

### Complexity
O(N log k)

## Problem 96. Median of Two Sorted Arrays (variant 3)

### Explanation
Binary search partition so left halves are ≤ right halves.

### Solution

```ts
function findMedianSortedArrays(a: number[], b: number[]): number {
  if (a.length > b.length) return findMedianSortedArrays(b, a)
  const m = a.length, n = b.length
  let lo = 0, hi = m
  while (lo <= hi) {
    const i = (lo + hi) >> 1
    const j = ((m + n + 1) >> 1) - i
    const aL = i === 0 ? -Infinity : a[i - 1]
    const aR = i === m ? Infinity : a[i]
    const bL = j === 0 ? -Infinity : b[j - 1]
    const bR = j === n ? Infinity : b[j]
    if (aL <= bR && bL <= aR) {
      if ((m + n) % 2) return Math.max(aL, bL)
      return (Math.max(aL, bL) + Math.min(aR, bR)) / 2
    }
    if (aL > bR) hi = i - 1
    else lo = i + 1
  }
  throw new Error('unreachable')
}
```

### Complexity
O(log(min(m,n))) time, O(1) space

## Problem 97. Word Ladder Length (variant 3)

### Explanation
Shortest transformation = BFS on implicit graph of words.

### Solution

```ts
function ladderLength(begin: string, end: string, wordList: string[]): number {
  const words = new Set(wordList)
  if (!words.has(end)) return 0
  const q: [string, number][] = [[begin, 1]]
  const seen = new Set([begin])
  while (q.length) {
    const [w, d] = q.shift()!
    if (w === end) return d
    const arr = w.split('')
    for (let i = 0; i < arr.length; i++) {
      const orig = arr[i]
      for (let c = 97; c <= 122; c++) {
        arr[i] = String.fromCharCode(c)
        const nw = arr.join('')
        if (words.has(nw) && !seen.has(nw)) {
          seen.add(nw)
          q.push([nw, d + 1])
        }
      }
      arr[i] = orig
    }
  }
  return 0
}
```

### Complexity
O(N * L * 26) BFS

## Problem 98. Serialize / Deserialize Binary Tree (variant 3)

### Explanation
Preorder with null markers is unambiguous.

### Solution

```ts
class TreeNode { constructor(public val = 0, public left: TreeNode | null = null, public right: TreeNode | null = null) {} }
function serialize(root: TreeNode | null): string {
  const out: string[] = []
  const dfs = (n: TreeNode | null) => {
    if (!n) { out.push('#'); return }
    out.push(String(n.val))
    dfs(n.left); dfs(n.right)
  }
  dfs(root)
  return out.join(',')
}
function deserialize(data: string): TreeNode | null {
  const vals = data.split(',')
  let i = 0
  const dfs = (): TreeNode | null => {
    const v = vals[i++]
    if (v === '#') return null
    const node = new TreeNode(Number(v))
    node.left = dfs(); node.right = dfs()
    return node
  }
  return dfs()
}
```

### Complexity
O(n) time/space

## Problem 99. Trapping Rain Water (variant 3)

### Explanation
Two pointers — water bounded by the smaller side max.

### Solution

```ts
function trap(height: number[]): number {
  let l = 0, r = height.length - 1, lMax = 0, rMax = 0, water = 0
  while (l < r) {
    if (height[l] < height[r]) {
      lMax = Math.max(lMax, height[l])
      water += lMax - height[l]
      l++
    } else {
      rMax = Math.max(rMax, height[r])
      water += rMax - height[r]
      r--
    }
  }
  return water
}
```

### Complexity
O(n) time, O(1) space

## Problem 100. Minimum Window Substring (variant 3)

### Explanation
Sliding window shrink when all chars covered.

### Solution

```ts
function minWindow(s: string, t: string): string {
  const need = new Map<string, number>()
  for (const ch of t) need.set(ch, (need.get(ch) ?? 0) + 1)
  let missing = t.length, start = 0, best = '', bestLen = Infinity
  for (let end = 0; end < s.length; end++) {
    const c = s[end]
    if ((need.get(c) ?? 0) > 0) missing--
    need.set(c, (need.get(c) ?? 0) - 1)
    while (missing === 0) {
      if (end - start + 1 < bestLen) {
        bestLen = end - start + 1
        best = s.slice(start, end + 1)
      }
      const L = s[start++]
      need.set(L, (need.get(L) ?? 0) + 1)
      if ((need.get(L) ?? 0) > 0) missing++
    }
  }
  return best
}
```

### Complexity
O(|s| + |t|)

