# Problems 26–50

Trees, heaps, windows, and monotonic stacks. Assume `TreeNode` from problem 26 where needed.

| # | Problem | Pattern |
| --- | --- | --- |
| 26 | Level Order | BFS |
| 27 | Validate BST | DFS bounds |
| 28 | LCA of BST | BST walk |
| 29 | LCA of BT | DFS |
| 30 | Serialize BT | Preorder |
| 31 | Max Path Sum | Tree DP |
| 32 | Build Tree Pre/In | Divide |
| 33 | Subtree | DFS match |
| 34 | House Robber III | Tree DP |
| 35 | Diameter | DFS |
| 36 | Task Scheduler | Greedy |
| 37 | Design Twitter | Heap merge |
| 38 | Median Stream | Two heaps |
| 39 | Sliding Window Max | Deque |
| 40 | Min Window Substring | Window |
| 41 | Char Replacement | Window |
| 42 | Permutation in String | Fixed window |
| 43 | Trapping Rain Water | Two pointers |
| 44 | Largest Rectangle | Mono stack |
| 45 | Daily Temperatures | Mono stack |
| 46 | Next Greater II | Mono stack |
| 47 | Asteroid Collision | Stack |
| 48 | Basic Calculator II | Stack |
| 49 | Simplify Path | Stack |
| 50 | Eval RPN | Stack |

---

> [!NOTE]
> Problems 27–35 reuse the `TreeNode` class defined in problem 26.

## 26. Binary Tree Level Order Traversal

**Difficulty:** Medium · **Pattern:** BFS

Return level-order (BFS) values of a binary tree.

### Solution

```ts
class TreeNode {
  val: number
  left: TreeNode | null
  right: TreeNode | null
  constructor(val = 0, left: TreeNode | null = null, right: TreeNode | null = null) {
    this.val = val
    this.left = left
    this.right = right
  }
}

export function levelOrder(root: TreeNode | null): number[][] {
  if (!root) return []
  const res: number[][] = []
  const q: TreeNode[] = [root]
  while (q.length) {
    const size = q.length
    const level: number[] = []
    for (let i = 0; i < size; i++) {
      const n = q.shift()!
      level.push(n.val)
      if (n.left) q.push(n.left)
      if (n.right) q.push(n.right)
    }
    res.push(level)
  }
  return res
}
```

### Explanation

Process the queue in level-sized batches.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 27. Validate Binary Search Tree

**Difficulty:** Medium · **Pattern:** DFS bounds

Determine if a binary tree is a valid BST.

### Solution

```ts
export function isValidBST(root: TreeNode | null): boolean {
  const dfs = (node: TreeNode | null, lo: number, hi: number): boolean => {
    if (!node) return true
    if (node.val <= lo || node.val >= hi) return false
    return dfs(node.left, lo, node.val) && dfs(node.right, node.val, hi)
  }
  return dfs(root, -Infinity, Infinity)
}
```

### Explanation

Each node must lie strictly inside (lo, hi) from ancestors.

### Complexity

- **Time:** O(n)
- **Space:** O(h)


---

## 28. Lowest Common Ancestor of a BST

**Difficulty:** Medium · **Pattern:** BST walk

Find LCA of nodes `p` and `q` in a BST.

### Solution

```ts
export function lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode): TreeNode {
  let cur: TreeNode | null = root
  while (cur) {
    if (p.val < cur.val && q.val < cur.val) cur = cur.left
    else if (p.val > cur.val && q.val > cur.val) cur = cur.right
    else return cur
  }
  throw new Error('unreachable')
}
```

### Explanation

Walk down until the path splits between p and q.

### Complexity

- **Time:** O(h)
- **Space:** O(1)


---

## 29. Lowest Common Ancestor of a Binary Tree

**Difficulty:** Medium · **Pattern:** DFS

Find LCA in a general binary tree.

### Solution

```ts
export function lowestCommonAncestorBT(
  root: TreeNode | null,
  p: TreeNode,
  q: TreeNode
): TreeNode | null {
  if (!root || root === p || root === q) return root
  const L = lowestCommonAncestorBT(root.left, p, q)
  const R = lowestCommonAncestorBT(root.right, p, q)
  if (L && R) return root
  return L ?? R
}
```

### Explanation

If found in different subtrees, root is LCA; else bubble the non-null side.

### Complexity

- **Time:** O(n)
- **Space:** O(h)


---

## 30. Serialize and Deserialize Binary Tree

**Difficulty:** Hard · **Pattern:** Preorder encoding

Serialize a binary tree to a string and deserialize it back.

### Solution

```ts
export function serialize(root: TreeNode | null): string {
  if (!root) return 'null'
  return `${root.val},${serialize(root.left)},${serialize(root.right)}`
}

export function deserialize(data: string): TreeNode | null {
  const vals = data.split(',')
  let i = 0
  const build = (): TreeNode | null => {
    const v = vals[i++]
    if (v === 'null') return null
    const node = new TreeNode(Number(v))
    node.left = build()
    node.right = build()
    return node
  }
  return build()
}
```

### Explanation

Preorder with explicit null markers uniquely reconstructs shape.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 31. Binary Tree Maximum Path Sum

**Difficulty:** Hard · **Pattern:** Tree DP

A path may start and end at any node. Return the maximum path sum.

### Solution

```ts
export function maxPathSum(root: TreeNode | null): number {
  let best = -Infinity
  const dfs = (node: TreeNode | null): number => {
    if (!node) return 0
    const L = Math.max(0, dfs(node.left))
    const R = Math.max(0, dfs(node.right))
    best = Math.max(best, node.val + L + R)
    return node.val + Math.max(L, R)
  }
  dfs(root)
  return best
}
```

### Explanation

Contribution upward uses one child; path through node may use both.

### Complexity

- **Time:** O(n)
- **Space:** O(h)


---

## 32. Construct Binary Tree from Preorder and Inorder

**Difficulty:** Medium · **Pattern:** Divide & conquer

Build a tree from `preorder` and `inorder` (unique values).

### Solution

```ts
export function buildTree(preorder: number[], inorder: number[]): TreeNode | null {
  const idx = new Map(inorder.map((v, i) => [v, i]))
  let p = 0
  const build = (lo: number, hi: number): TreeNode | null => {
    if (lo > hi) return null
    const val = preorder[p++]
    const mid = idx.get(val)!
    const node = new TreeNode(val)
    node.left = build(lo, mid - 1)
    node.right = build(mid + 1, hi)
    return node
  }
  return build(0, inorder.length - 1)
}
```

### Explanation

Preorder gives root; inorder index splits left/right sizes.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 33. Subtree of Another Tree

**Difficulty:** Medium · **Pattern:** DFS match

Return true if `subRoot` is a subtree of `root`.

### Solution

```ts
function same(a: TreeNode | null, b: TreeNode | null): boolean {
  if (!a && !b) return true
  if (!a || !b || a.val !== b.val) return false
  return same(a.left, b.left) && same(a.right, b.right)
}

export function isSubtree(root: TreeNode | null, subRoot: TreeNode | null): boolean {
  if (!subRoot) return true
  if (!root) return false
  return same(root, subRoot) || isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot)
}
```

### Explanation

Try a full match at each node; else recurse. Merkle hashing optimizes to O(n).

### Complexity

- **Time:** O(m·n)
- **Space:** O(h)


---

## 34. House Robber III

**Difficulty:** Medium · **Pattern:** Tree DP

Binary tree of values; cannot rob parent and child. Maximize loot.

### Solution

```ts
export function rob(root: TreeNode | null): number {
  const dfs = (node: TreeNode | null): [number, number] => {
    if (!node) return [0, 0]
    const L = dfs(node.left)
    const R = dfs(node.right)
    const take = node.val + L[1] + R[1]
    const skip = Math.max(L[0], L[1]) + Math.max(R[0], R[1])
    return [take, skip]
  }
  const [a, b] = dfs(root)
  return Math.max(a, b)
}
```

### Explanation

State per node: [rob this, skip this].

### Complexity

- **Time:** O(n)
- **Space:** O(h)


---

## 35. Diameter of Binary Tree

**Difficulty:** Medium · **Pattern:** DFS heights

Return the length (edges) of the longest path between any two nodes.

### Solution

```ts
export function diameterOfBinaryTree(root: TreeNode | null): number {
  let best = 0
  const height = (node: TreeNode | null): number => {
    if (!node) return 0
    const L = height(node.left)
    const R = height(node.right)
    best = Math.max(best, L + R)
    return 1 + Math.max(L, R)
  }
  height(root)
  return best
}
```

### Explanation

Diameter through a node is leftHeight + rightHeight.

### Complexity

- **Time:** O(n)
- **Space:** O(h)


---

## 36. Task Scheduler

**Difficulty:** Medium · **Pattern:** Greedy counting

Tasks with cooldown `n` between identical letters. Min time units (idles allowed).

### Solution

```ts
export function leastInterval(tasks: string[], n: number): number {
  const freq = Array(26).fill(0)
  for (const t of tasks) freq[t.charCodeAt(0) - 65]++
  freq.sort((a, b) => a - b)
  const maxf = freq[25]
  let idle = (maxf - 1) * n
  for (let i = 24; i >= 0 && idle > 0; i--) idle -= Math.min(maxf - 1, freq[i])
  return tasks.length + Math.max(0, idle)
}
```

### Explanation

Frame around most frequent task; fill idle slots with other tasks.

### Complexity

- **Time:** O(n)
- **Space:** O(1)


---

## 37. Design Twitter

**Difficulty:** Medium · **Pattern:** Heap merge

postTweet, getNewsFeed (10 most recent from self+followees), follow, unfollow.

### Solution

```ts
export class Twitter {
  private time = 0
  private tweets = new Map<number, Array<[number, number]>>()
  private follows = new Map<number, Set<number>>()

  postTweet(userId: number, tweetId: number): void {
    if (!this.tweets.has(userId)) this.tweets.set(userId, [])
    this.tweets.get(userId)!.push([this.time++, tweetId])
  }

  getNewsFeed(userId: number): number[] {
    const users = new Set(this.follows.get(userId) ?? [])
    users.add(userId)
    type Item = { time: number; id: number; user: number; idx: number }
    const heap: Item[] = []
    for (const u of users) {
      const list = this.tweets.get(u)
      if (!list?.length) continue
      const idx = list.length - 1
      heap.push({ time: list[idx][0], id: list[idx][1], user: u, idx })
    }
    const res: number[] = []
    while (res.length < 10 && heap.length) {
      heap.sort((a, b) => b.time - a.time)
      const top = heap.shift()!
      res.push(top.id)
      if (top.idx > 0) {
        const prev = this.tweets.get(top.user)![top.idx - 1]
        heap.push({ time: prev[0], id: prev[1], user: top.user, idx: top.idx - 1 })
      }
    }
    return res
  }

  follow(followerId: number, followeeId: number): void {
    if (!this.follows.has(followerId)) this.follows.set(followerId, new Set())
    this.follows.get(followerId)!.add(followeeId)
  }

  unfollow(followerId: number, followeeId: number): void {
    this.follows.get(followerId)?.delete(followeeId)
  }
}
```

### Explanation

Merge recent tweets like K-way merge by timestamp.

### Complexity

- **Time:** O(F log F) per feed
- **Space:** O(total tweets)


---

## 38. Find Median from Data Stream

**Difficulty:** Hard · **Pattern:** Two heaps

Support `addNum` and `findMedian` for a stream.

### Solution

```ts
class Heap {
  constructor(private cmp: (a: number, b: number) => number, public data: number[] = []) {}
  size() { return this.data.length }
  peek() { return this.data[0] }
  push(x: number) {
    const a = this.data
    a.push(x)
    let i = a.length - 1
    while (i > 0) {
      const p = (i - 1) >> 1
      if (this.cmp(a[p], a[i]) <= 0) break
      ;[a[p], a[i]] = [a[i], a[p]]
      i = p
    }
  }
  pop(): number {
    const a = this.data
    const top = a[0]
    const last = a.pop()!
    if (a.length) {
      a[0] = last
      let i = 0
      while (true) {
        let s = i
        const l = i * 2 + 1, r = l + 1
        if (l < a.length && this.cmp(a[l], a[s]) < 0) s = l
        if (r < a.length && this.cmp(a[r], a[s]) < 0) s = r
        if (s === i) break
        ;[a[i], a[s]] = [a[s], a[i]]
        i = s
      }
    }
    return top
  }
}

export class MedianFinder {
  private lo = new Heap((a, b) => b - a) // max-heap
  private hi = new Heap((a, b) => a - b) // min-heap

  addNum(num: number): void {
    this.lo.push(num)
    this.hi.push(this.lo.pop())
    if (this.hi.size() > this.lo.size()) this.lo.push(this.hi.pop())
  }

  findMedian(): number {
    if (this.lo.size() > this.hi.size()) return this.lo.peek()
    return (this.lo.peek() + this.hi.peek()) / 2
  }
}
```

### Explanation

Lower half in max-heap, upper in min-heap; balance sizes so median is peek(s).

### Complexity

- **Time:** O(log n) add
- **Space:** O(n)


---

## 39. Sliding Window Maximum

**Difficulty:** Hard · **Pattern:** Monotonic deque

Return max of each contiguous window of size `k`.

### Solution

```ts
export function maxSlidingWindow(nums: number[], k: number): number[] {
  const dq: number[] = []
  const res: number[] = []
  for (let i = 0; i < nums.length; i++) {
    while (dq.length && dq[0] <= i - k) dq.shift()
    while (dq.length && nums[dq[dq.length - 1]] <= nums[i]) dq.pop()
    dq.push(i)
    if (i >= k - 1) res.push(nums[dq[0]])
  }
  return res
}
```

### Explanation

Deque stores candidate indices in decreasing value order; front is max.

### Complexity

- **Time:** O(n)
- **Space:** O(k)


---

## 40. Minimum Window Substring

**Difficulty:** Hard · **Pattern:** Sliding window

Smallest substring of `s` that covers all of `t` (with counts).

### Solution

```ts
export function minWindow(s: string, t: string): string {
  const need = new Map<string, number>()
  for (const c of t) need.set(c, (need.get(c) ?? 0) + 1)
  let missing = need.size
  let left = 0
  let best = ''
  const win = new Map<string, number>()
  for (let right = 0; right < s.length; right++) {
    const c = s[right]
    win.set(c, (win.get(c) ?? 0) + 1)
    if (need.has(c) && win.get(c) === need.get(c)) missing--
    while (missing === 0) {
      if (!best || right - left + 1 < best.length) best = s.slice(left, right + 1)
      const d = s[left++]
      win.set(d, win.get(d)! - 1)
      if (need.has(d) && win.get(d)! < need.get(d)!) missing++
    }
  }
  return best
}
```

### Explanation

Expand until valid, shrink while valid, track minimum length.

### Complexity

- **Time:** O(|s| + |t|)
- **Space:** O(Σ)


---

## 41. Longest Repeating Character Replacement

**Difficulty:** Medium · **Pattern:** Sliding window

You may replace at most `k` chars. Longest substring of identical chars.

### Solution

```ts
export function characterReplacement(s: string, k: number): number {
  const freq = Array(26).fill(0)
  let left = 0
  let maxf = 0
  let best = 0
  for (let right = 0; right < s.length; right++) {
    maxf = Math.max(maxf, ++freq[s.charCodeAt(right) - 65])
    while (right - left + 1 - maxf > k) freq[s.charCodeAt(left++) - 65]--
    best = Math.max(best, right - left + 1)
  }
  return best
}
```

### Explanation

Window valid iff `len - maxFreq ≤ k`.

### Complexity

- **Time:** O(n)
- **Space:** O(1)


---

## 42. Permutation in String

**Difficulty:** Medium · **Pattern:** Fixed window

Does `s2` contain any permutation of `s1` as a substring?

### Solution

```ts
export function checkInclusion(s1: string, s2: string): boolean {
  if (s1.length > s2.length) return false
  const need = Array(26).fill(0)
  const win = Array(26).fill(0)
  for (let i = 0; i < s1.length; i++) {
    need[s1.charCodeAt(i) - 97]++
    win[s2.charCodeAt(i) - 97]++
  }
  const same = () => need.every((v, i) => v === win[i])
  if (same()) return true
  for (let i = s1.length; i < s2.length; i++) {
    win[s2.charCodeAt(i) - 97]++
    win[s2.charCodeAt(i - s1.length) - 97]--
    if (same()) return true
  }
  return false
}
```

### Explanation

Slide a window of length |s1| and compare frequency vectors.

### Complexity

- **Time:** O(n)
- **Space:** O(1)


---

## 43. Trapping Rain Water

**Difficulty:** Hard · **Pattern:** Two pointers

Elevation map heights; how much water can be trapped?

### Solution

```ts
export function trap(height: number[]): number {
  let lo = 0
  let hi = height.length - 1
  let leftMax = 0
  let rightMax = 0
  let water = 0
  while (lo < hi) {
    if (height[lo] < height[hi]) {
      leftMax = Math.max(leftMax, height[lo])
      water += leftMax - height[lo]
      lo++
    } else {
      rightMax = Math.max(rightMax, height[hi])
      water += rightMax - height[hi]
      hi--
    }
  }
  return water
}
```

### Explanation

Process the side with smaller height; water = running max − height.

### Complexity

- **Time:** O(n)
- **Space:** O(1)


---

## 44. Largest Rectangle in Histogram

**Difficulty:** Hard · **Pattern:** Monotonic stack

Bars of width 1; return largest rectangle area in the histogram.

### Solution

```ts
export function largestRectangleArea(heights: number[]): number {
  const stack: number[] = [-1]
  let best = 0
  const hs = [...heights, 0]
  for (let i = 0; i < hs.length; i++) {
    while (stack.length > 1 && hs[stack[stack.length - 1]] > hs[i]) {
      const h = hs[stack.pop()!]
      const w = i - stack[stack.length - 1] - 1
      best = Math.max(best, h * w)
    }
    stack.push(i)
  }
  return best
}
```

### Explanation

Increasing stack of indices; pop when a shorter bar bounds width.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 45. Daily Temperatures

**Difficulty:** Medium · **Pattern:** Monotonic stack

For each day, days until a warmer temperature (0 if none).

### Solution

```ts
export function dailyTemperatures(temperatures: number[]): number[] {
  const n = temperatures.length
  const ans = Array(n).fill(0)
  const stack: number[] = []
  for (let i = 0; i < n; i++) {
    while (stack.length && temperatures[i] > temperatures[stack[stack.length - 1]]) {
      const j = stack.pop()!
      ans[j] = i - j
    }
    stack.push(i)
  }
  return ans
}
```

### Explanation

Decreasing stack; resolve waiting colder days when warmer arrives.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 46. Next Greater Element II

**Difficulty:** Medium · **Pattern:** Monotonic stack

Circular array: next greater for each element, or -1.

### Solution

```ts
export function nextGreaterElements(nums: number[]): number[] {
  const n = nums.length
  const ans = Array(n).fill(-1)
  const stack: number[] = []
  for (let i = 0; i < 2 * n; i++) {
    const x = nums[i % n]
    while (stack.length && x > nums[stack[stack.length - 1]]) {
      ans[stack.pop()!] = x
    }
    if (i < n) stack.push(i)
  }
  return ans
}
```

### Explanation

Traverse twice to simulate circular wrap.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 47. Asteroid Collision

**Difficulty:** Medium · **Pattern:** Stack simulation

Positive = right, negative = left. Same size both explode; else smaller dies.

### Solution

```ts
export function asteroidCollision(asteroids: number[]): number[] {
  const stack: number[] = []
  for (const a of asteroids) {
    let alive = true
    while (alive && a < 0 && stack.length && stack[stack.length - 1] > 0) {
      if (stack[stack.length - 1] < -a) {
        stack.pop()
        continue
      }
      if (stack[stack.length - 1] === -a) stack.pop()
      alive = false
    }
    if (alive) stack.push(a)
  }
  return stack
}
```

### Explanation

Collisions only when top moves right and current moves left.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 48. Basic Calculator II

**Difficulty:** Medium · **Pattern:** Stack

Evaluate `+ - * /` on non-negative integers (no parentheses). Truncate toward zero.

### Solution

```ts
export function calculate(s: string): number {
  let num = 0
  let sign = '+'
  const stack: number[] = []
  const apply = (op: string, n: number) => {
    if (op === '+') stack.push(n)
    else if (op === '-') stack.push(-n)
    else if (op === '*') stack.push(stack.pop()! * n)
    else stack.push(Math.trunc(stack.pop()! / n))
  }
  for (let i = 0; i < s.length; i++) {
    const c = s[i]
    if (c >= '0' && c <= '9') num = num * 10 + Number(c)
    if (('+-*/'.includes(c) && c !== ' ') || i === s.length - 1) {
      if (c === ' ') continue
      apply(sign, num)
      sign = c
      num = 0
    }
  }
  return stack.reduce((a, b) => a + b, 0)
}
```

### Explanation

* / fold into stack top immediately; + − push signed terms; sum at end.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 49. Simplify Path

**Difficulty:** Medium · **Pattern:** Stack

Simplify a Unix absolute path (`/a/./b/../../c/`).

### Solution

```ts
export function simplifyPath(path: string): string {
  const stack: string[] = []
  for (const part of path.split('/')) {
    if (!part || part === '.') continue
    if (part === '..') stack.pop()
    else stack.push(part)
  }
  return '/' + stack.join('/')
}
```

### Explanation

Stack of directory names; `..` pops when possible.

### Complexity

- **Time:** O(n)
- **Space:** O(n)


---

## 50. Evaluate Reverse Polish Notation

**Difficulty:** Medium · **Pattern:** Stack

Evaluate RPN tokens with `+ - * /` (truncate toward zero).

### Solution

```ts
export function evalRPN(tokens: string[]): number {
  const st: number[] = []
  for (const t of tokens) {
    if (t === '+' || t === '-' || t === '*' || t === '/') {
      const b = st.pop()!
      const a = st.pop()!
      if (t === '+') st.push(a + b)
      else if (t === '-') st.push(a - b)
      else if (t === '*') st.push(a * b)
      else st.push(Math.trunc(a / b))
    } else st.push(Number(t))
  }
  return st[0]
}
```

### Explanation

Push operands; on operator pop two and push result.

### Complexity

- **Time:** O(n)
- **Space:** O(n)

