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

items.append(P(51, "Combination Sum", "Medium", "Backtracking",
"Candidates (distinct positives); return unique combinations that sum to `target` (reuse allowed).",
"""export function combinationSum(candidates: number[], target: number): number[][] {
  const res: number[][] = []
  candidates.sort((a, b) => a - b)
  const dfs = (start: number, remain: number, path: number[]) => {
    if (remain === 0) { res.push([...path]); return }
    for (let i = start; i < candidates.length; i++) {
      if (candidates[i] > remain) break
      path.push(candidates[i])
      dfs(i, remain - candidates[i], path) // reuse i
      path.pop()
    }
  }
  dfs(0, target, [])
  return res
}""",
"Backtrack with start index; reuse same index to allow unlimited picks.", "O(2^{t/min})", "O(target/min)"))

items.append(P(52, "Combination Sum II", "Medium", "Backtracking",
"Candidates may contain duplicates; each number used once; unique combinations summing to target.",
"""export function combinationSum2(candidates: number[], target: number): number[][] {
  const res: number[][] = []
  candidates.sort((a, b) => a - b)
  const dfs = (start: number, remain: number, path: number[]) => {
    if (remain === 0) { res.push([...path]); return }
    for (let i = start; i < candidates.length; i++) {
      if (i > start && candidates[i] === candidates[i - 1]) continue
      if (candidates[i] > remain) break
      path.push(candidates[i])
      dfs(i + 1, remain - candidates[i], path)
      path.pop()
    }
  }
  dfs(0, target, [])
  return res
}""",
"Skip duplicate picks at the same depth after sorting.", "O(2^n)", "O(n)"))

items.append(P(53, "Permutations", "Medium", "Backtracking",
"Return all permutations of distinct integers.",
"""export function permute(nums: number[]): number[][] {
  const res: number[][] = []
  const used = Array(nums.length).fill(false)
  const dfs = (path: number[]) => {
    if (path.length === nums.length) { res.push([...path]); return }
    for (let i = 0; i < nums.length; i++) {
      if (used[i]) continue
      used[i] = true
      path.push(nums[i])
      dfs(path)
      path.pop()
      used[i] = false
    }
  }
  dfs([])
  return res
}""",
"Choose unused indices; swap-based in-place also works.", "O(n·n!)", "O(n)"))

items.append(P(54, "Subsets", "Medium", "Backtracking / bitmasks",
"Return all subsets (power set) of distinct integers.",
"""export function subsets(nums: number[]): number[][] {
  const res: number[][] = []
  const dfs = (i: number, path: number[]) => {
    if (i === nums.length) { res.push([...path]); return }
    dfs(i + 1, path)
    path.push(nums[i])
    dfs(i + 1, path)
    path.pop()
  }
  dfs(0, [])
  return res
}""",
"Include/exclude each element. Bitmask loop is equivalent.", "O(n·2^n)", "O(n)"))

items.append(P(55, "Subsets II", "Medium", "Backtracking",
"Power set with duplicates in input; result must not contain duplicate subsets.",
"""export function subsetsWithDup(nums: number[]): number[][] {
  nums.sort((a, b) => a - b)
  const res: number[][] = []
  const dfs = (start: number, path: number[]) => {
    res.push([...path])
    for (let i = start; i < nums.length; i++) {
      if (i > start && nums[i] === nums[i - 1]) continue
      path.push(nums[i])
      dfs(i + 1, path)
      path.pop()
    }
  }
  dfs(0, [])
  return res
}""",
"Sort + skip equal values at same depth.", "O(n·2^n)", "O(n)"))

items.append(P(56, "Word Break", "Medium", "DP",
"Can `s` be segmented into a space-separated sequence of dictionary words?",
"""export function wordBreak(s: string, wordDict: string[]): boolean {
  const set = new Set(wordDict)
  const dp = Array(s.length + 1).fill(false)
  dp[0] = true
  for (let i = 1; i <= s.length; i++) {
    for (let j = 0; j < i; j++) {
      if (dp[j] && set.has(s.slice(j, i))) { dp[i] = true; break }
    }
  }
  return dp[s.length]
}""",
"`dp[i]` = true if prefix `s[0..i)` can be segmented.", "O(n²·L)", "O(n)"))

items.append(P(57, "Word Break II", "Hard", "DP + DFS",
"Return all sentences where `s` is segmented using dictionary words.",
"""export function wordBreakII(s: string, wordDict: string[]): string[] {
  const set = new Set(wordDict)
  const memo = new Map<number, string[]>()
  const dfs = (start: number): string[] => {
    if (memo.has(start)) return memo.get(start)!
    if (start === s.length) return ['']
    const res: string[] = []
    for (let end = start + 1; end <= s.length; end++) {
      const word = s.slice(start, end)
      if (!set.has(word)) continue
      for (const tail of dfs(end)) {
        res.push(tail ? `${word} ${tail}` : word)
      }
    }
    memo.set(start, res)
    return res
  }
  return dfs(0)
}""",
"Memoized DFS from each index; concatenate valid prefixes.", "O(n·2^n) worst", "O(n·2^n)")

)

# Fix last - I accidentally closed wrong. Let me continue carefully in the file.

items[-1] = P(57, "Word Break II", "Hard", "DP + DFS",
"Return all sentences where `s` is segmented using dictionary words.",
"""export function wordBreakII(s: string, wordDict: string[]): string[] {
  const set = new Set(wordDict)
  const memo = new Map<number, string[]>()
  const dfs = (start: number): string[] => {
    if (memo.has(start)) return memo.get(start)!
    if (start === s.length) return ['']
    const res: string[] = []
    for (let end = start + 1; end <= s.length; end++) {
      const word = s.slice(start, end)
      if (!set.has(word)) continue
      for (const tail of dfs(end)) {
        res.push(tail ? `${word} ${tail}` : word)
      }
    }
    memo.set(start, res)
    return res
  }
  return dfs(0)
}""",
"Memoized DFS from each index; concatenate valid prefixes.", "O(n·2^n) worst", "O(n·2^n)")

items.append(P(58, "Palindrome Partitioning", "Medium", "Backtracking",
"Partition `s` so every substring is a palindrome; return all partitions.",
"""export function partition(s: string): string[][] {
  const res: string[][] = []
  const isPal = (l: number, r: number) => {
    while (l < r) if (s[l++] !== s[r--]) return false
    return true
  }
  const dfs = (start: number, path: string[]) => {
    if (start === s.length) { res.push([...path]); return }
    for (let end = start; end < s.length; end++) {
      if (!isPal(start, end)) continue
      path.push(s.slice(start, end + 1))
      dfs(end + 1, path)
      path.pop()
    }
  }
  dfs(0, [])
  return res
}""",
"Try every palindromic prefix cut; recurse on remainder.", "O(n·2^n)", "O(n)"))

items.append(P(59, "N-Queens", "Hard", "Backtracking",
"Place `n` queens so none attack; return all distinct board configurations.",
"""export function solveNQueens(n: number): string[][] {
  const res: string[][] = []
  const board = Array.from({ length: n }, () => Array(n).fill('.'))
  const cols = new Set<number>()
  const diag1 = new Set<number>()
  const diag2 = new Set<number>()
  const dfs = (r: number) => {
    if (r === n) {
      res.push(board.map((row) => row.join('')))
      return
    }
    for (let c = 0; c < n; c++) {
      if (cols.has(c) || diag1.has(r - c) || diag2.has(r + c)) continue
      board[r][c] = 'Q'
      cols.add(c); diag1.add(r - c); diag2.add(r + c)
      dfs(r + 1)
      board[r][c] = '.'
      cols.delete(c); diag1.delete(r - c); diag2.delete(r + c)
    }
  }
  dfs(0)
  return res
}""",
"Place row by row; track columns and both diagonals.", "O(n!)", "O(n)"))

items.append(P(60, "Sudoku Solver", "Hard", "Backtracking",
"Solve a 9×9 Sudoku board in-place (`'.'` empty).",
"""export function solveSudoku(board: string[][]): void {
  const row = Array.from({ length: 9 }, () => new Set<string>())
  const col = Array.from({ length: 9 }, () => new Set<string>())
  const box = Array.from({ length: 9 }, () => new Set<string>())
  const empty: Array<[number, number]> = []
  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const v = board[r][c]
      if (v === '.') empty.push([r, c])
      else {
        row[r].add(v); col[c].add(v); box[Math.floor(r / 3) * 3 + Math.floor(c / 3)].add(v)
      }
    }
  }
  const dfs = (i: number): boolean => {
    if (i === empty.length) return true
    const [r, c] = empty[i]
    const b = Math.floor(r / 3) * 3 + Math.floor(c / 3)
    for (let d = 1; d <= 9; d++) {
      const ch = String(d)
      if (row[r].has(ch) || col[c].has(ch) || box[b].has(ch)) continue
      board[r][c] = ch
      row[r].add(ch); col[c].add(ch); box[b].add(ch)
      if (dfs(i + 1)) return true
      board[r][c] = '.'
      row[r].delete(ch); col[c].delete(ch); box[b].delete(ch)
    }
    return false
  }
  dfs(0)
}""",
"Try digits 1–9 with row/col/box sets; backtrack on failure.", "O(9^{empty})", "O(1)"))

items.append(P(61, "Letter Combinations of a Phone Number", "Medium", "Backtracking",
"Digits 2–9 map to letters like a phone keypad; return all combinations.",
"""const MAP: Record<string, string> = {
  '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
  '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz',
}
export function letterCombinations(digits: string): string[] {
  if (!digits) return []
  const res: string[] = []
  const dfs = (i: number, path: string) => {
    if (i === digits.length) { res.push(path); return }
    for (const ch of MAP[digits[i]]) dfs(i + 1, path + ch)
  }
  dfs(0, '')
  return res
}""",
"Cartesian product via DFS over digit mappings.", "O(4^n·n)", "O(n)"))

items.append(P(62, "Search a 2D Matrix", "Medium", "Binary search",
"Matrix rows sorted left→right; first of each row > last of previous. Search target.",
"""export function searchMatrix(matrix: number[][], target: number): boolean {
  const m = matrix.length, n = matrix[0].length
  let lo = 0, hi = m * n - 1
  while (lo <= hi) {
    const mid = (lo + hi) >> 1
    const v = matrix[Math.floor(mid / n)][mid % n]
    if (v === target) return true
    if (v < target) lo = mid + 1
    else hi = mid - 1
  }
  return false
}""",
"Treat as virtual 1D sorted array of size m·n.", "O(log(mn))", "O(1)"))

items.append(P(63, "Search a 2D Matrix II", "Medium", "Staircase search",
"Rows and columns individually sorted. Efficiently search target.",
"""export function searchMatrixII(matrix: number[][], target: number): boolean {
  let r = 0, c = matrix[0].length - 1
  while (r < matrix.length && c >= 0) {
    const v = matrix[r][c]
    if (v === target) return true
    if (v > target) c--
    else r++
  }
  return false
}""",
"Start top-right; move left if too big, down if too small.", "O(m+n)", "O(1)"))

items.append(P(64, "Find First and Last Position in Sorted Array", "Medium", "Binary search bounds",
"Sorted array; return starting and ending position of target, else [-1,-1].",
"""function lowerBound(nums: number[], target: number): number {
  let lo = 0, hi = nums.length
  while (lo < hi) {
    const mid = (lo + hi) >> 1
    if (nums[mid] < target) lo = mid + 1
    else hi = mid
  }
  return lo
}
export function searchRange(nums: number[], target: number): [number, number] {
  const left = lowerBound(nums, target)
  if (left === nums.length || nums[left] !== target) return [-1, -1]
  const right = lowerBound(nums, target + 1) - 1
  return [left, right]
}""",
"Lower bound of target and of target+1.", "O(log n)", "O(1)"))

items.append(P(65, "Search in Rotated Sorted Array", "Medium", "Binary search",
"Distinct values, rotated sorted array; find target index or -1.",
"""export function search(nums: number[], target: number): number {
  let lo = 0, hi = nums.length - 1
  while (lo <= hi) {
    const mid = (lo + hi) >> 1
    if (nums[mid] === target) return mid
    if (nums[lo] <= nums[mid]) {
      if (nums[lo] <= target && target < nums[mid]) hi = mid - 1
      else lo = mid + 1
    } else {
      if (nums[mid] < target && target <= nums[hi]) lo = mid + 1
      else hi = mid - 1
    }
  }
  return -1
}""",
"One half is always sorted; decide which half can contain target.", "O(log n)", "O(1)"))

items.append(P(66, "Find Minimum in Rotated Sorted Array", "Medium", "Binary search",
"Rotated sorted distinct array; find minimum.",
"""export function findMin(nums: number[]): number {
  let lo = 0, hi = nums.length - 1
  while (lo < hi) {
    const mid = (lo + hi) >> 1
    if (nums[mid] > nums[hi]) lo = mid + 1
    else hi = mid
  }
  return nums[lo]
}""",
"If mid > hi, min is right of mid; else min in left including mid.", "O(log n)", "O(1)"))

items.append(P(67, "Time Based Key-Value Store", "Medium", "Binary search / map",
"set(key,value,timestamp) and get(key,timestamp) → value with largest ts ≤ query.",
"""export class TimeMap {
  private store = new Map<string, Array<[number, string]>>()
  set(key: string, value: string, timestamp: number): void {
    if (!this.store.has(key)) this.store.set(key, [])
    this.store.get(key)!.push([timestamp, value])
  }
  get(key: string, timestamp: number): string {
    const arr = this.store.get(key)
    if (!arr?.length) return ''
    let lo = 0, hi = arr.length - 1, ans = -1
    while (lo <= hi) {
      const mid = (lo + hi) >> 1
      if (arr[mid][0] <= timestamp) { ans = mid; lo = mid + 1 }
      else hi = mid - 1
    }
    return ans === -1 ? '' : arr[ans][1]
  }
}""",
"Timestamps increase per key; binary search last ≤ timestamp.", "O(log n) get", "O(n)"))

items.append(P(68, "Koko Eating Bananas", "Medium", "Binary search on answer",
"Piles of bananas; finish within `h` hours eating speed `k` (ceil). Minimize k.",
"""export function minEatingSpeed(piles: number[], h: number): number {
  let lo = 1, hi = Math.max(...piles)
  const hours = (k: number) => piles.reduce((s, p) => s + Math.ceil(p / k), 0)
  while (lo < hi) {
    const mid = (lo + hi) >> 1
    if (hours(mid) <= h) hi = mid
    else lo = mid + 1
  }
  return lo
}""",
"Monotonic feasibility on speed k.", "O(n log M)", "O(1)"))

items.append(P(69, "Capacity To Ship Packages Within D Days", "Medium", "Binary search on answer",
"Packages in order; ship with capacity; minimize capacity to finish in `days`.",
"""export function shipWithinDays(weights: number[], days: number): number {
  let lo = Math.max(...weights)
  let hi = weights.reduce((a, b) => a + b, 0)
  const ok = (cap: number) => {
    let d = 1, load = 0
    for (const w of weights) {
      if (load + w > cap) { d++; load = 0 }
      load += w
    }
    return d <= days
  }
  while (lo < hi) {
    const mid = (lo + hi) >> 1
    if (ok(mid)) hi = mid
    else lo = mid + 1
  }
  return lo
}""",
"Lower bound = max package; upper = sum; binary search capacity.", "O(n log S)", "O(1)"))

items.append(P(70, "Split Array Largest Sum", "Hard", "Binary search on answer",
"Split array into `m` non-empty continuous subarrays; minimize largest subarray sum.",
"""export function splitArray(nums: number[], m: number): number {
  let lo = Math.max(...nums)
  let hi = nums.reduce((a, b) => a + b, 0)
  const need = (limit: number) => {
    let parts = 1, sum = 0
    for (const x of nums) {
      if (sum + x > limit) { parts++; sum = 0 }
      sum += x
    }
    return parts
  }
  while (lo < hi) {
    const mid = (lo + hi) >> 1
    if (need(mid) <= m) hi = mid
    else lo = mid + 1
  }
  return lo
}""",
"Same pattern as ship capacity: minimize bottleneck sum.", "O(n log S)", "O(1)"))

items.append(P(71, "Median of Two Sorted Arrays", "Hard", "Binary search partitions",
"Two sorted arrays; find median in O(log(m+n)).",
"""export function findMedianSortedArrays(a: number[], b: number[]): number {
  if (a.length > b.length) return findMedianSortedArrays(b, a)
  const m = a.length, n = b.length
  let lo = 0, hi = m
  const half = Math.floor((m + n + 1) / 2)
  while (lo <= hi) {
    const i = (lo + hi) >> 1
    const j = half - i
    const aLeft = i === 0 ? -Infinity : a[i - 1]
    const aRight = i === m ? Infinity : a[i]
    const bLeft = j === 0 ? -Infinity : b[j - 1]
    const bRight = j === n ? Infinity : b[j]
    if (aLeft <= bRight && bLeft <= aRight) {
      if ((m + n) % 2) return Math.max(aLeft, bLeft)
      return (Math.max(aLeft, bLeft) + Math.min(aRight, bRight)) / 2
    }
    if (aLeft > bRight) hi = i - 1
    else lo = i + 1
  }
  throw new Error('unreachable')
}""",
"Binary search cut on smaller array so left halves have correct count.", "O(log(min(m,n)))", "O(1)"))

items.append(P(72, "Longest Increasing Subsequence", "Medium", "Patience sorting",
"Length of longest strictly increasing subsequence.",
"""export function lengthOfLIS(nums: number[]): number {
  const tails: number[] = []
  for (const x of nums) {
    let lo = 0, hi = tails.length
    while (lo < hi) {
      const mid = (lo + hi) >> 1
      if (tails[mid] < x) lo = mid + 1
      else hi = mid
    }
    tails[lo] = x
  }
  return tails.length
}""",
"`tails[i]` = smallest tail of all LIS length i+1.", "O(n log n)", "O(n)"))

items.append(P(73, "Russian Doll Envelopes", "Hard", "Sort + LIS",
"Envelopes `[w,h]`; nest if both strictly smaller. Max chain length.",
"""export function maxEnvelopes(envelopes: number[][]): number {
  envelopes.sort((a, b) => (a[0] === b[0] ? b[1] - a[1] : a[0] - b[0]))
  const tails: number[] = []
  for (const [, h] of envelopes) {
    let lo = 0, hi = tails.length
    while (lo < hi) {
      const mid = (lo + hi) >> 1
      if (tails[mid] < h) lo = mid + 1
      else hi = mid
    }
    tails[lo] = h
  }
  return tails.length
}""",
"Sort width asc, height desc on ties; LIS on heights.", "O(n log n)", "O(n)"))

items.append(P(74, "Maximum Product Subarray", "Medium", "DP running min/max",
"Contiguous subarray with largest product.",
"""export function maxProduct(nums: number[]): number {
  let maxEnding = nums[0], minEnding = nums[0], best = nums[0]
  for (let i = 1; i < nums.length; i++) {
    const x = nums[i]
    const candidates = [x, maxEnding * x, minEnding * x]
    maxEnding = Math.max(...candidates)
    minEnding = Math.min(...candidates)
    best = Math.max(best, maxEnding)
  }
  return best
}""",
"Track max and min products ending here (sign flips from negatives).", "O(n)", "O(1)"))

items.append(P(75, "Coin Change", "Medium", "DP unbounded knapsack",
"Fewest coins to make `amount` (unlimited supply); else -1.",
"""export function coinChange(coins: number[], amount: number): number {
  const dp = Array(amount + 1).fill(Infinity)
  dp[0] = 0
  for (let a = 1; a <= amount; a++) {
    for (const c of coins) {
      if (c <= a) dp[a] = Math.min(dp[a], dp[a - c] + 1)
    }
  }
  return dp[amount] === Infinity ? -1 : dp[amount]
}""",
"`dp[a] = min over coins of dp[a-c]+1`.", "O(amount · |coins|)", "O(amount)"))

table = [
(51, "Combination Sum", "Backtracking"),
(52, "Combination Sum II", "Backtracking"),
(53, "Permutations", "Backtracking"),
(54, "Subsets", "Backtracking"),
(55, "Subsets II", "Backtracking"),
(56, "Word Break", "DP"),
(57, "Word Break II", "DP+DFS"),
(58, "Palindrome Partition", "Backtracking"),
(59, "N-Queens", "Backtracking"),
(60, "Sudoku Solver", "Backtracking"),
(61, "Letter Combinations", "Backtracking"),
(62, "Search 2D Matrix", "Binary search"),
(63, "Search 2D Matrix II", "Staircase"),
(64, "First/Last Position", "Bounds"),
(65, "Search Rotated", "Binary search"),
(66, "Min in Rotated", "Binary search"),
(67, "Time Map", "Binary search"),
(68, "Koko Bananas", "BS on answer"),
(69, "Ship Within Days", "BS on answer"),
(70, "Split Array Largest Sum", "BS on answer"),
(71, "Median Two Sorted", "Partition BS"),
(72, "LIS", "Patience"),
(73, "Russian Doll", "Sort+LIS"),
(74, "Max Product Subarray", "DP"),
(75, "Coin Change", "DP"),
]

# Fix item 67 missing closing - check
# items.append(P(67, ... "O(n)")  - need ))

# Looking at 67 - ends with `"O(n)")` - missing one paren for append!
# Let me fix:
for i, it in enumerate(items):
    pass

# Rebuild 67 if broken - actually looking at the source, line ends:
# `"Timestamps increase per key; binary search last ≤ timestamp.", "O(log n) get", "O(n)")`
# That's missing closing for append. But then items.append(P(68... would be syntax error.

# Wait I see - item 67 ends with `"O(n)")` without second `)`. That would be SyntaxError when running.
# Fix by rewriting 67:

# Find and fix - I'll replace items that might be wrong after building by re-assigning

header = """# Problems 51–75

Backtracking, binary search (including on answer), and DP classics.

| # | Problem | Pattern |
| --- | --- | --- |
""" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in table) + "\n\n---\n\n"

out = header + "\n---\n\n".join(items)
Path("/Users/prajjwal/jvl/interview/docs/coding/13-problems-51-75.md").write_text(out)
print("wrote", len(items), "problems", len(out), "bytes")
