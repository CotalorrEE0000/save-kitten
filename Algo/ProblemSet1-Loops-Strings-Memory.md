# Algo Problem Set · Set 1: Loops, Strings, and First Contact with Memory

> If you are new to writing code, do the first few main-course lessons first — get comfortable with how files are stored and handed in — then come back to this set.
>
> The problems below are ordered **by difficulty, not by problem number**; the right column gives the tier and what the problem practices. These tiers are relative inside this set, not LeetCode difficulty scores. If you cannot follow even the editorial, skip it and come back later.
>
> **This set covers only four things**: loops, two indices on one array, a lookup table, and strings. No pointers, structs, or recursion, and nothing from the memory model the main course covers later. Solve in **C**.

> **算法题单 · 第一组：循环、字符串与第一次撞内存（原地写 / 查表 / 返回数组）**
>
> 如果你刚开始写代码，先做主线前几讲，把「文件怎么存、怎么交」弄熟，再来做这一组。
>
> 下面的题目**按由易到难排，不按题号**，右侧是难度档和这一题的练点。这里不抄力扣难度分，档位是这一组内部的相对次序。遇到题解都看不懂的，先跳过，过段时间再回来。
>
> 这一组只覆盖四件事：**循环、一个数组上的两个下标、查一张表、字符串**。不引入指针、结构体、递归，也不涉及后面主线要讲的内存模型。用 **C** 解。

---

## 1. Two Indices on One Array

> **Why these two come first**: Lessons 1–3 were about handing things in; this is the first time you actually write a loop. Both are chosen to return **a single integer**, so your hands deal only with "two positions moving on one array" — no returned array, no memory yet.

| | | |
|---|---|---|
| [27](https://leetcode.cn/problems/remove-element/) | Remove Element | Starter · one read index, one write index; the return value is the new length |
| [283](https://leetcode.cn/problems/move-zeroes/) | Move Zeroes | Starter · the same two indices, plus "keep the non-zero elements in their original order" |

> **【Common point】** Do not allocate a second array — write forward in place. Then look back: does the read index always stay ahead of the write one?

> **为什么先出现这两道**：前三讲练的都是「把东西交上去」，这是第一次真的写循环。特意挑两道**只返回一个整数**的题，让手先只对付「同一个数组上同时走两个位置」，不碰返回数组、不碰内存。

| | | |
|---|---|---|
| [27](https://leetcode.cn/problems/remove-element/) | 移除元素 | 入门 · 一个读下标、一个写下标；返回值是留下来的长度 |
| [283](https://leetcode.cn/problems/move-zeroes/) | 移动零 | 入门 · 同样的两个下标，多一条「非零元素保持原有顺序」 |

> 【共同点】别开新数组，就在原数组上往前写。写完回头看：读的那个下标是不是永远跑在写的那个前面。

---

## 2. Numbers and a Lookup Table

> **Why next**: with no array to return, the loop itself has to be right; then one static lookup table is added. The edges are not in the normal input but in "negative / trailing 0 / a smaller value before a larger one" — exactly the **edge cases** line you write before coding.

| | | |
|---|---|---|
| [9](https://leetcode.cn/problems/palindrome-number/) | Palindrome Number | Basic · reverse only half and stop; negative numbers and a trailing 0 are the two edges |
| [13](https://leetcode.cn/problems/roman-to-integer/) | Roman to Integer | Basic · a lookup table; a smaller value before a larger one means subtract, so look back one character |

> **【Common point】** Both scan left to right, but the current cell has to be compared with the previous one. In 9 it is half a number; in 13 it is the adjacent character.

> **为什么接着出现**：没有数组要返回，逼着把循环本身写对；再加一张静态映射表。这两道的边界都不在「正常输入」，而在「负数 / 末尾 0 / 小值排在大值前面」——正好练动笔前那三行里的「边界」。

| | | |
|---|---|---|
| [9](https://leetcode.cn/problems/palindrome-number/) | 回文数 | 基础 · 反转一半就停；负数、以 0 结尾是两条边界 |
| [13](https://leetcode.cn/problems/roman-to-integer/) | 罗马数字转整数 | 基础 · 映射表；小值在大值前要减，得回看一眼前一个字符 |

> 【共同点】都是「从左到右扫一遍，但当前这一格要跟前一格比」。9 比的是半个数字，13 比的是相邻字符。

---

## 3. Returning an Array (First Contact with Manual Memory)

> **Why last**: both C functions must **return an array** — 1 returns `int*`, 412 an array of strings — so `malloc` and the `returnSize` pointer cannot be avoided. It is not just 412; both hit it. Manual memory management has not been taught yet, so for these two a three-line idea plus a partial attempt with question marks is an acceptable hand-in; it is met properly later. The loop itself is not the hard part — building a place to put the result and handing it back is.

| | | |
|---|---|---|
| [1](https://leetcode.cn/problems/two-sum/) | Two Sum | Advanced · nested loops first, then one-pass lookup; returns `int*` |
| [412](https://leetcode.cn/problems/fizz-buzz/) | Fizz Buzz | Advanced · the loop is trivial, but you must build n strings and pack them into `char**` |

> **【Common point】** The first four only *compute a number*; these two must *make a place to put the result*. First contact with `malloc` is nothing to fear — it is exactly that place.

> **为什么放在最后**：这两道的 C 函数都要**返回数组**——1 是 `int*`，412 是字符串数组——绕不开 `malloc` 和 `returnSize` 指针。不是 412 一道，两道都撞。主线还没教手动内存管理，所以这两道**允许交三行思路 + 一段带问号的半成品**，把卡住的地方如实写出来；后面会正式讲。循环本身并不难，难的是把结果装进内存再交出去。

| | | |
|---|---|---|
| [1](https://leetcode.cn/problems/two-sum/) | 两数之和 | 进阶 · 先写嵌套循环，再想怎么一次查找；返回 `int*` |
| [412](https://leetcode.cn/problems/fizz-buzz/) | Fizz Buzz | 进阶 · 循环最直白，但要造 n 个字符串再装进 `char**` |

> 【共同点】前面四道只「算出一个数」，这两道要「造出一块地方放结果」。第一次见到 `malloc` 不用慌，它就是要交的那块地方。

---

## 4. How to Use This Set

> - Any order, but work through the whole set before closing it. **No clock, no due date, no week to beat.**
> - Before any code, write three lines: **idea** (plain words), **complexity** (time / space, big-O is enough), **edge cases** (smallest, empty, the input that breaks the obvious loop). If you cannot write them, write them with question marks.
> - Keep an **honest status line** for each problem. `tried, stuck at the reversal loop` is worth more than a copied `AC`. You will be asked to explain one problem out loud without opening the file.
> - Write yours first, then read the C reference solutions in `solutions/`. Reading a solution before struggling is how practice quietly stops working.
> - Hand in one file, `submits/<handle>/algo/w1.md`; every other rule from Lessons 1–3 still applies.

> **怎么用这一组**
>
> - 顺序随意，收口前整组过一遍；**不计时、不设截止、不排到周**。
> - 每题动笔前写三行：**思路**（大白话）、**复杂度**（时间 / 空间，大 O 就够）、**边界**（最小、空、会让朴素循环出错的输入）。写不出来就带着问号写。
> - 每题留一行**如实的状态**。`试了，卡在反转循环` 比抄来的 `AC` 值钱；收口时会请你不打开文件脱稿讲其中一道。
> - 先写自己的，再看 `solutions/` 里的 C 参考题解。先看答案再挣扎，练手会悄悄失效。
> - 交一个文件 `submits/<handle>/algo/w1.md`，其余规矩同前三讲。

---

## Appendix: One Correction at Hand-in

> Assignment files use `submit(algo): ...`, kept apart from `docs:` (editing lessons, this problem set, or the reference solutions), so a human and a machine can both tell "repository-side update" from "learner handed in a file" at a glance. This is **not** a type in the general convention: an ordinary repository has no assignments to receive, so it has no `submit:`. Do not carry it outside this teaching repository.

> **附：提交时的一处修正**
>
> 作业文件用 `submit(algo): ...`，和 `docs:`（改讲义、题目单、参考题解）分开：人和机器都要一眼分清「仓库侧更新」和「学员交文件」。这不是通用提交规范里的类型，普通仓库没有收作业这件事，也就不会有它——出了这个教学仓库就不要再用。
