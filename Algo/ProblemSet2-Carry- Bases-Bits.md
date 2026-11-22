# Algo Problem Set · Set 2: Carry, Bases, and Bits

> Set 2 assumes Set 1 is submitted — or at least that its first two sections are. Everything here builds on "two indices on one array" and "a lookup table"; nothing here needs recursion, structs, or a data structure you have not met.
>
> Problems are ordered **by difficulty, not by problem number**. The right column gives the tier and what the problem practices. Tiers are relative inside this set, not LeetCode difficulty scores.
>
> **This set covers three things**: walking input **from the end** with a carry, splitting a number into digits in a **base other than ten**, and looking at an integer as **32 bits**. No pointers to pointers, no sorting, no dynamic programming.

> **算法题单 · 第二组：进位、进制与位（从末尾往前 / 拆数 / 第一次位运算）**
>
> 第二组默认第一组已经做完，至少前两节收口。这里全部建立在「一个数组上两个下标」和「查一张表」之上；不引入递归、结构体，也不用你没见过的数据结构。
>
> 题目**按由易到难排，不按题号**，右侧是难度档和练点。档位是这一组内部的相对次序，不抄力扣难度分。
>
> 这一组只覆盖三件事：**从末尾往前**带着进位走一遍、把数拆成**十进制以外**的位、把整数看成 **32 个 bit**。不碰指向指针的指针，不碰排序，不碰动态规划。

---

## 1. Carry, Walking from the End

> **Why these two in the set**: Set 1 walked arrays from the front. These walk **from the last character backwards**, because the carry is born at the end and travels left. Two problems, one loop — the only difference is the base. That is the point: the carry rule does not know whether you are in base 10 or base 2, so if your loop breaks when the base changes, the loop was wrong, not the problem.
>
> Both C functions return `char*`. This is the same "build a place, then hand it back" as Set 1 §3, one layer simpler: one string instead of an array of strings.

|                                                  |             |                                                                         |
| ------------------------------------------------ | ----------- | ----------------------------------------------------------------------- |
| [415](https://leetcode.cn/problems/add-strings/) | Add Strings | Starter · two indices from the end, one carry variable, write backwards |
| [67](https://leetcode.cn/problems/add-binary/)   | Add Binary  | Basic · the identical loop in base 2; nothing about the carry changes   |

> **【Common point】** `digit = a + b + carry; out = digit % base; carry = digit / base`. If you had to rewrite the loop for 67, you copied the problem instead of solving it.

> **为什么这两道一组**：第一组是从前往后走数组，这两道**从最后一个字符往前**走，因为进位从末尾产生、往左传。两道一个循环，只有进制不同——这才是重点：进位规则不知道你在十进制还是二进制，换了进制循环就崩，说明循环本来写错了，不是题变了。
>
> 两道的 C 函数都返回 `char*`，就是第一组第 3 节那个「造一块地方再交出去」，只是从「字符串数组」降成「一个字符串」，简单一层。

|                                                  |       |                             |
| ------------------------------------------------ | ----- | --------------------------- |
| [415](https://leetcode.cn/problems/add-strings/) | 字符串相加 | 入门 · 两个下标从末尾走，一个进位变量，倒着写结果  |
| [67](https://leetcode.cn/problems/add-binary/)   | 二进制求和 | 基础 · 同一个循环换成二进制；进位那套一个字都不用改 |

> 【共同点】`位值 = a + b + 进位`；`写下 位值 % 进制`；`进位 = 位值 / 进制`。如果 67 你重写了一遍循环，那是把题抄了一遍，不是解了一遍。

---

## 2. Taking a Number Apart

> **Why this one sits alone**: §1 builds a string out of digits; this does the inverse — takes a number apart into digits. It is the same `% base` idea running backwards, and it is where "ten" stops being special: ten is just the base you were born with. Two edges carry the whole difficulty: **zero** (the loop body never runs) and **a negative input** (the sign is not a digit).

|                                             |        |                                                                                       |
| ------------------------------------------- | ------ | ------------------------------------------------------------------------------------- |
| [504](https://leetcode.cn/problems/base-7/) | Base 7 | Basic · `% 7` and `/ 7` until zero; then reverse; handle `0` and negatives separately |

> **【Common point】** `n % 7` gives the last digit, `n / 7` drops it. Digits come out **backwards**, so either write them backwards or reverse at the end — the same orientation problem as §1, from the other side.

> **为什么单独一节**：第 1 节用数字拼出字符串，这一节反过来把数拆成数字。还是 `% 进制`，只是方向相反；也是在这一节，「十」第一次不再是特殊的——它只是你从小用惯的那个进制。整节的难点就两个边界：**0**（循环体一次都不进）和**负数**（负号不是一位数字）。

|                                             |      |                                       |
| ------------------------------------------- | ---- | ------------------------------------- |
| [504](https://leetcode.cn/problems/base-7/) | 七进制数 | 基础 · `% 7`、`/ 7` 直到为零；再反转；`0` 和负数单独处理 |

> 【共同点】`n % 7` 拿到最后一位，`n / 7` 把它扔掉。位是**倒着出来**的——要么倒着写，要么最后反转，和第 1 节是同一个方向问题，只是从另一边遇上。

---

## 3. Looking at an Integer as 32 Bits

> **Why last**: everything before this treated an integer as a **number**. Here it becomes **32 bits in memory** — the first time you look at the representation instead of the value. Both problems are short; both punish signedness. In C, `1 << 31` on `int` is undefined behaviour, and a right shift on a signed negative value is implementation-defined. Use `uint32_t` and the traps disappear.
>
> This is also the set's bridge to the main course: the next lesson is about memory, the stack, and undefined behaviour. Come back to this section after that lesson and re-read your own solution — you will see the traps you walked past.

|                                                       |                  |                                                                                         |
| ----------------------------------------------------- | ---------------- | --------------------------------------------------------------------------------------- |
| [191](https://leetcode.cn/problems/number-of-1-bits/) | Number of 1 Bits | Basic · `n & 1` then shift; then the `n & (n - 1)` trick that clears the lowest set bit |
| [190](https://leetcode.cn/problems/reverse-bits/)     | Reverse Bits     | Advanced · build the answer bit by bit into a `uint32_t`; no strings, no arrays         |

|   |   |
| - | - |

> **【Common point】** A number is a pattern, not a quantity. `&`, `|`, `^`, `<<`, `>>` act on the pattern; `%` and `/` act on the quantity. Both solve the same shapes — 191 can be written either way, and comparing the two is the exercise.

> **为什么放最后**：前面所有题都把整数当**数**看，这一节第一次把它当**内存里的 32 个 bit** 看，看的是表示而不是数值。两道都很短，两道都咬有符号性：C 里 `1 << 31` 在 `int` 上是未定义行为，对有符号负数右移是实现定义。用 `uint32_t` 这些坑就都不见了。
>
> 这一节也是通向主线的桥：下一讲讲内存、栈与未定义行为。那一讲上完再回来重读自己的解法，会看见当初踩过去的坑。

|                                                       |         |                                              |
| ----------------------------------------------------- | ------- | -------------------------------------------- |
| [191](https://leetcode.cn/problems/number-of-1-bits/) | 位 1 的个数 | 基础 · `n & 1` 再看移位；然后试 `n & (n - 1)` 消掉最低位的 1 |
| [190](https://leetcode.cn/problems/reverse-bits/)     | 颠倒二进制位  | 进阶 · 一位一位往 `uint32_t` 里装；不用字符串、不用数组          |

|   |   |
| - | - |

> 【共同点】数是一个图案，不是一个量。`&`、`|`、`^`、`<<`、`>>` 作用在图案上，`%` 和 `/` 作用在量上。两道题两种写法都通——191 用哪边写都行，把两种都写一遍，对比本身就是练习。

---

## 4. How to Use This Set

> - Any order, but work through the whole set before submit it. **No clock, no due date, no week to beat.**
> - Before any code, think three lines: **idea** (plain words), **complexity** (time / space, big-O is enough), **edge cases** (zero, negative, the input that makes your loop skip its body). If you cannot write them, bring them with question marks.
> - Keep an **honest status line** for each problem. `tried, carry loop runs but the result is reversed` is worth more than a copied `AC`. 
> - Write yours first, then read the C reference solutions. Reading a solution before struggling is how practice quietly stops working.
> - Hand in one source file for each task, `submits/<handle>/algo/Txx.c`; every other rule from Lessons 1–3 still applies. Commit type stays `submit(algo): ...` as in Set 1.

> **怎么用好这一组**
>
> - 顺序随意，提交前整组过一遍；**不计时、不设截止、不排到周**。
> - 每题动笔前想三行：**思路**（大白话）、**复杂度**（时间 / 空间，大 O 就够）、**边界**（0、负数、会让循环体一次都不进的输入）。想不出来就带着问号写。
> - 每题留一行**真实的状态**。`试了，进位循环通了但结果反了` 比抄来的 `AC` 值钱；
> - 先写自己的，再看参考题解。先看答案再挣扎，练手会悄悄失效。
> - 每道题交一个解决 `submits/<handle>/algo/Txxx.c`，其余规矩同前三讲；提交类型仍用第一组说明的 `submit(algo): ...`。
