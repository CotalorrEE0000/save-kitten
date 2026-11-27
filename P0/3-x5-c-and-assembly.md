# 3-x5 What One C Statement Becomes

**Optional reading, twenty minutes, no assignment.** This page answers one question: what does the C you write actually look like to the CPU? By the end you should be able to open a binary you compiled yourself and say what the first five lines are doing.

> **一条 C 语句变成了什么（可选读物，20 分钟，不做作业）。** 这一页只回答一个问题：你写的 C，CPU 真正拿到的东西长什么样。看完你应该能打开自己编译出来的二进制，指着前五行说出它们在干什么。

It sets no assignment and is not part of acceptance. **When to read it**: after you have a binary you compiled yourself — those `objdump` lines need a real program before they move. Reading it now is fine too, just leave the two commands in §3.5.1 for later.

> 这一页不布置作业，也不进验收。**什么时候读**：等你手上有一个自己编出来的二进制之后再读最顺——那几行 `objdump` 输出，要有一个真实程序才跑得动。现在读也行，只是 §3.5.1 的两条命令先搁着。

Its only use: next time someone says "the compiler optimised it" or "that is UB", you know which lines to go and look at.

> 它的用处只有一个：以后再有人说「编译器优化了」「这是 UB」，你知道该去看哪几行。

As for what a register is, what an instruction set is, and how x86 differs from ARM — those are told as history on the systems page (3-x1) and at the circuit level in 3-x2. This page only uses them to read a real disassembly.

> 至于「寄存器是什么、指令集是什么、x86 和 ARM 差在哪」这些底层的来龙去脉，它们在系统那一页（3-x1）里讲过来历，在 3-x2 里讲到电路层——这一页只拿它们来读真实的反汇编。

---

## 3.5.1 Several roads to the assembly

From C to "the instructions the CPU really runs" there are two roads, one forwards and one backwards:

```bash
gcc -S hello.c -o hello.s      # assembly text the compiler emits, human-readable (forwards)
objdump -d hello.exe           # disassemble an existing binary, what actually landed in the file (backwards)
```

> 从 C 到「CPU 真正执行的指令」有两条路，一顺一逆：`gcc -S` 顺着编译方向，给你编译器输出的、人能读的汇编文本；`objdump -d` 逆着往回读，从已有二进制反汇编出最终真正进文件的东西。

`-S` gives you what the compiler *intends* to emit; `objdump -d` gives you what ended up in the file. They agree most of the time and stop agreeing once optimisation is turned up — that difference is itself a lesson.

> `-S` 给你编译器**想**生成的；`objdump -d` 给你最终进文件的。两者大多数时候一样，优化开高之后不一定——这个差别本身就是一课。

But both of those borrow the compiler's hands. If you are not starting from C but **writing assembly directly**, you use the system's own commands and never touch gcc:

```powershell
# Windows (needs MASM / ml64, shipped with Visual Studio or installed separately)
ml64 /c hello.asm
link hello.obj /subsystem:console
```

```bash
# Linux (GNU binutils, present on almost every distribution)
as hello.s -o hello.o        # as = assembler
ld hello.o -o hello          # ld = linker
```

> 但这两条都是「借编译器的手」。如果你不是从 C 出发，而是**直接手写汇编**，那就得用系统的原生命令自己编，不经过 gcc 这套外挂：Windows 上是 `ml64` 汇编、`link` 链接（随 Visual Studio 或单独安装）；Linux 上是 GNU binutils 的 `as`（assembler，汇编器）和 `ld`（linker，链接器），几乎每个发行版都自带。

Notice the division of labour: `gcc` is not "the tool that assembles". It is a **driver** that runs four stages in one go — preprocess, compile, assemble, link. At the assembling stage gcc calls exactly `as` on Linux or `ml64` on Windows behind your back. So when you write assembly by hand, `as` / `ld` and `ml64` / `link` are the native tools of that layer; gcc is only a wrapper around them. The disassembly below reads the same either way.

> 注意这一层的分工：`gcc` 不是「编汇编」的工具，它是把「预处理 → 编译 → 汇编 → 链接」四步一口气做完的**驱动**。真到汇编那一步，gcc 在幕后调用的正是 `as`（Linux）或 `ml64`（Windows）。所以手写汇编时你看到的 `as` / `ld`、`ml64` / `link`，才是这一层最原生的工具，gcc 只是把它们包起来。这一页后面的反汇编，读法对两条路都适用。

## 3.5.2 Registers: the few cells the CPU works in

A register is the only storage the CPU can compute on directly. The names change with the architecture — x86-64 has `rax rbx rcx rdx rsi rdi rbp rsp`, ARM64 has `x0–x30`, RISC-V has `a0–a7` / `t0–t6` / `s0–s11`. Where that arrangement came from, and why the architectures disagree, was covered on the systems page (3-x1); here they are only labels for reading the listing below.

> 寄存器是 CPU 唯一能直接参与运算的存储，它们的名字随架构而变（x86-64 用 `rax rbx rcx rdx rsi rdi rbp rsp`，ARM64 用 `x0–x30`，RISC-V 用 `a0–a7` / `t0–t6` / `s0–s11`）。这一套的由来、为什么不同架构长得不一样，系统那一页（3-x1）讲过了；这一页只拿它们来读下面这段真实的反汇编。

---

## 3.5.3 Instructions come in four families

Four families cover almost everything you will read: move (`mov`, `lea`), arithmetic (`add`, `sub`, `imul`), compare (`cmp`, `test`), and jump (`jmp`, `je`, `jne`, `jl`, `call`, `ret`). Everything else in C eventually lands in one of them.

> 四类指令覆盖你几乎会读到的全部：搬（`mov`、`lea`）、算（`add`、`sub`、`imul`）、比（`cmp`、`test`）、跳（`jmp`、`je`、`jne`、`jl`、`call`、`ret`）。C 里的一切最终都落在这四类里。

---

## 3.5.4 A real disassembly: the first lines of `main`

This is disassembled from the course's `hello` program and copied verbatim (your addresses and offsets will differ; the shape will not):

> 下面这段是从本课 `hello` 程序反汇编出来的，原样抄的（你的地址和偏移会不一样，形状一样）：

```asm
0000000140001380 <main>:
  140001380:  55                    push   %rbp
  140001381:  48 89 e5              mov    %rsp,%rbp
  140001384:  48 83 ec 30           sub    $0x30,%rsp
  140001388:  89 4d 10              mov    %ecx,0x10(%rbp)      # argc
  14000138b:  48 89 55 18           mov    %rdx,0x18(%rbp)      # argv
  14000138f:  e8 d8 00 00 00        call   14000146c <__main>
  140001394:  48 8d 05 65 5c 00 00  lea    0x5c65(%rip),%rax    # "hello"
  14000139b:  48 89 c1              mov    %rax,%rcx
  14000139e:  e8 6d 0c 00 00        call   140002010 <__mingw_printf>
  1400013a3:  c7 45 fc 01 00 00 00  movl   $0x1,-0x4(%rbp)      # i = 1
  1400013aa:  eb 2a                 jmp    1400013d6
  1400013ac:  8b 45 fc              mov    -0x4(%rbp),%eax      # load i
  1400013bd:  48 01 d0              add    %rdx,%rax            # pointer plus offset
  1400013d6:  8b 45 fc              mov    -0x4(%rbp),%eax
  1400013d9:  3b 45 10              cmp    0x10(%rbp),%eax      # i against argc
  1400013dc:  7c ce                 jl     1400013ac            # i < argc -> back to the loop body
```

Read only the first three lines and you already know where you are: they build the stack frame. `push %rbp` saves the caller's frame pointer, `mov %rsp,%rbp` marks this frame's bottom, `sub $0x30,%rsp` makes room for locals. Every local variable in that function lives somewhere in those 0x30 bytes.

> 只读前三行就知道自己在哪：它们在搭栈帧。`push %rbp` 保存调用者的帧指针，`mov %rsp,%rbp` 标出这一帧的底，`sub $0x30,%rsp` 为局部变量腾地方。这个函数里每个局部变量都住在那 0x30 个字节里。

Then notice the loop: `cmp` compares, `jl` jumps if less. Two instructions, one decision. The exit is `add $0x30,%rsp` at the end, undoing the `sub` — the frame is a stack in the literal sense, and leaving a function is popping it.

> 再看循环：`cmp` 比较，`jl` 小于则跳。两条指令，一个判断。函数末尾是 `add $0x30,%rsp`，把开头那个 `sub` 抵掉——栈帧字面意义上是个栈，离开函数就是把它弹出去。

---

## 3.5.5 Reading a disassembly takes three questions

1. Where does this value come from? (the source of a `mov`, the address of a `lea`)
2. Where is it going? (which register or which piece of memory it is written back to)
3. Which jump decides it? (`cmp` plus a `j*`, or a plain `call`)

> 1. 这个值从哪来？（`mov` 的源、`lea` 的地址）
> 2. 它到哪去？（写回哪个寄存器或哪块内存）
> 3. 哪个跳转决定它？（`cmp` + `j*`，或者直接 `call`）

Answer those three and you have read a stretch of assembly. No instruction table to memorise, and no need to know how many bytes each one takes — unless you are working on binary formats or security, in which case you will need exactly that.

> 三个问题答完，一段反汇编就读完了。不用背指令表，也不用数每条指令几个字节——除非你以后做二进制格式或安全方向，那时才需要。

**One thing to take away**: the C you write and the instructions that run are two different texts with a translation in between. UB is exactly where that translation is allowed to stop being faithful.

> **带走一句**：你写的 C 和真正跑的指令是两份不同的文本，中间隔着一次翻译。UB 就是这次翻译被允许不忠实的地方。
