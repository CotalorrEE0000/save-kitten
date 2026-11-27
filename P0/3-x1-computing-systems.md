# 3-x1 How Computers Got Here

> This page teaches no command and sets no assignment. It answers a question you will ask sooner or later: why is the machine in front of you shaped the way it is? Why are there "Windows" and "Linux"? Why do phones and computers look alike and yet not alike?
>
> People memorise this to pass exams; we tell it so that the circuit page (3-x2), the shell (3-x3), Linux (3-x4) and assembly (3-x5) stop being words that appeared out of nowhere. Each of them is the mark left by a specific decision in history. See where they came from, and every later page costs you half the effort.

> 这一页不教你任何命令，也不布置作业。它回答一个你迟早会问的问题：你手上这台机器，为什么长成现在这个样子？为什么有「Windows」也有「Linux」？为什么手机和电脑看着一样又不一样？
>
> 别人背这些是要应付考试，我们讲这些，是为了让后面的电路（3-x2）、壳（3-x3）、Linux（3-x4）、汇编（3-x5）都不再是凭空冒出来的名词——它们每一个，都是一段历史里某个具体决定留下的痕迹。看懂了来路，后面每一页都能省一半力气。

---

## 3.1.1 One switch, two states

Everything starts with powered and not powered.

A logic gate — an AND, an OR, a NOT — can do only one small thing: given two inputs, produce one output. It knows nothing about numbers, let alone programs. Solder a few thousand of them together and you have a machine that can compute: feed voltages in at one end, and the voltage at the other end is the answer.

Today those gates are made small and fast by a device called **MOS** (Metal-Oxide-Semiconductor) transistor. It is, at heart, **a valve switched by an electric field**: put a voltage on one pin and the other two either conduct or stop conducting. That is the physical origin of "powered / not powered", the binary we keep talking about. Etch a few hundred million of them onto a sliver of silicon and you have an **integrated circuit**. Every one of the billions of switches in your CPU works the same way: a gate that an electric signal can push.

So "computers use binary" is not a preference anyone expressed. It is what the device naturally does.

> 一切从「有电 / 没电」开始。
>
> 一块逻辑门电路——与门、或门、非门——只能做一件小事：根据两个输入，给一个输出。它不知道什么是数字，更不知道什么是程序。但把它成千上万个焊在一起，就有了一台能「计算」的机器：你从一头喂进去高低电平，另一头出来的电平，就是答案。
>
> 今天这些门做得极小、极快，靠的是一种叫 **MOS（Metal-Oxide-Semiconductor，金属-氧化物-半导体）** 的晶体管。它本质就是一个**用电场开关的阀门**：给一个引脚加电压，另一个引脚之间就导通或截止——这就是「有电 / 没电」这个二进制的物理来源。把上百万个这样的管子刻在小块硅片上，就是「集成电路」。你 CPU 里几十亿个开关，每一个都是同一个原理：一个能被电信号拨动的门。所以「电脑用二进制」不是谁的偏好，是这种器件天然只认两个状态。
>
> 一句话先立住：**计算机 = 一堆只会「与或非」的开关，被「存储程序」这个想法组织起来，就能执行任意我们写下的指令。** 后面所有的事，都是在这个骨架上不断加层。

## 3.1.2 The idea came from a loom

"Use holes to encode information, and let the machine follow them" is a hundred years older than the electronic computer, and it came from a **loom**, not from mathematics.

In 1804, **Joseph Marie Jacquard** built a loom controlled by a **punched card**: which warp threads lift is decided by holes in the card, and the machine weaves the pattern by itself. Want a different pattern? Change the card, not the machine. **"Tell the machine what to do with a card"** — that is the single most important step in the history of automation.

In the following decades the English mathematician **Charles Babbage** tried to build a machine that computes on its own. His **Difference Engine** turned gears to evaluate polynomials, but far more radical was his design for the **Analytical Engine**: it already had the outline of a store, a mill, and execution in sequence — and it took its instructions from **punched cards**, borrowed straight from Jacquard's loom.

Babbage never finished it, but one young reader understood what it meant. **Ada Lovelace** — daughter of the poet Byron — published a set of notes on the Analytical Engine in 1843, including an algorithm for computing Bernoulli numbers. That algorithm is generally recognised as **the first program**. She also saw, earlier than Babbage, that such a machine was not limited to arithmetic: give it different rules and it could manipulate symbols, music included. **For the first time, a person had worked out how a human and a machine talk to each other** — not by flipping switches, but by writing down a set of rules the machine can read.

More than a century later, a programming language was named **Ada** in her honour.

> 这个「用孔表示信息、让机器照着执行」的想法，比电子计算机早了上百年，而且它来自**织布机**，不是数学。
>
> 1804 年，法国人 **约瑟夫·玛丽·雅卡尔（Joseph Marie Jacquard）** 发明了一种提花织布机：用一张**打孔卡**控制哪几根经线提起，机器照着卡上的孔自动织出花纹。想换图案？换一张卡就行，不用重造机器。**「用一张卡告诉机器该干什么」**——这是自动化史上最关键的一跳。
>
> 十九世纪，英国数学家 **查尔斯·巴贝奇（Charles Babbage）** 想造一台能自动算数的机器。他的**差分机（Difference Engine）**&#x7528;机械齿轮算多项式，但更超前的是他设计的**分析机（Analytical Engine）**：它已经有「存储」「运算」「按指令执行」的雏形，而且——它用**打孔卡**来输入指令，正是从雅卡尔织布机那里借来的灵感。
>
> 巴贝奇的机器没能造完，但有个年轻人看懂了它的全部意义。**阿达·洛芙莱斯（Ada Lovelace）**——诗人拜伦的女儿——在 1843 年为分析机写了一份笔记，里面包含一个计算伯努利数的**算法**。这份算法被后世公认为**第一个程序**。她甚至比巴贝奇更早看出：这台机器不仅能算数，只要给它不同的规则，它还能处理符号、甚至音乐。**人类第一次明白「人和机器怎么交流」**——不是靠拨开关，而是靠写下一串能被机器读懂的规则。
>
> 一百多年后，人们为了纪念她，把一门编程语言命名为 **Ada**。
>
> 一句话带走：**「程序」这个念头，是织布机先想出来的——用一张卡告诉机器该做什么；而「写程序」这件事，是一位夫人第一个做出来的。**

## 3.1.3 From ENIAC to the stored program

Back to the twentieth century. **ENIAC** (1945) was a machine of several tonnes packed with vacuum tubes, and it was "programmed" by **rewiring and flipping switches** — to solve a different problem you physically rebuilt the connections. In that era, writing a program was a job done with a wrench, inside the machine.

The decisive step was the idea of the **stored program**, set out systematically by **John von Neumann** in a 1945 report: treat the instructions themselves as data, and store them in the same memory as the numbers you want to compute. After that, changing a program no longer meant dismantling the machine — you changed what was in memory. Every program running on your computer today is a direct descendant of that idea.

Punched cards carry the story forward. Before keyboards and screens, a program was holes in stiff cardboard: a hole is one, no hole is zero, a stack of cards is a program, you feed the stack into a reader, and the machine executes the holes one by one. When you see programmers in an old film carrying a box of cards, that is not a prop. That was the source code.

> 回到二十世纪。1945 年的 **ENIAC** 是台几吨重、塞满电子管的大家伙，靠**插线和拨开关**来「编程」——想让它算另一道题，得物理上重新接线。那个年代，「写程序」是拿着扳手爬进机器里干的活。
>
> 关键的一跃是**存储程序（stored program）**&#x8FD9;个想法——它最早由 **约翰·冯·诺依曼（John von Neumann）** 在 1945 年的报告里系统阐述：把「要执行的指令」本身也当成数据，和要算的数字一起存进同一块存储器。这一下，改程序不用再拆机器了——换掉存储里的内容就行。今天你电脑里的每一个程序，都是这个想法的直接后代。
>
> 打孔卡则接续了这个故事：在键盘和屏幕出现之前，程序就是印在硬纸卡上的孔——有孔是一，没孔是零，一摞卡片就是一段程序，塞进读卡机，机器照着孔一个个执行。你会在老电影里看到程序员抱着一摞卡片——那不是道具，那是当时的「源代码」。

## 3.1.4 The operating system: clothes for a bare machine

Once a machine can execute instructions, the next questions arrive: who decides which program runs first? Who handles "program A wants the disk, so does program B"? Who turns a key press and a pixel into something a program can understand?

The answer is the **operating system (OS)**. It is the first program loaded at boot and the one that stays until shutdown. It does three things:

1. **It manages the hardware.** A program says "read this file"; it never touches the disk. The OS reads on its behalf and hands back the result.
2. **It manages programs.** Several run at once; the OS decides who goes first, and makes sure one crash does not take the others down with it.
3. **It gives each program a consistent illusion.** Every program believes the whole machine is its own. Underneath, the OS is switching between them.

Every command you type passes through the operating system before it reaches the actual machine. 3-x2 shows how a circuit is wired into a writable address; 3-x3 is about the shell, the layer that translates between you and the OS; 3-x4 is about the kernel, the part of the OS closest to the hardware.

> 有了能执行指令的机器，下一个问题是：谁来决定先跑哪个程序？谁来管「程序 A 要读盘，程序 B 也要读盘」？谁来把键盘的按键、屏幕的像素翻译成程序能懂的东西？
>
> 答案是**操作系统（Operating System，OS）**。它是开机后第一个被载入、又一直待到关机的那个程序。它做三件事：**管硬件**——程序说「我要读这个文件」，其实它碰不到磁盘，是操作系统替它去读、再把结果交回来；**管程序**——多个程序同时跑，操作系统决定谁先谁后，保证一个崩了不把别的也带崩；**给程序一个一致的假象**——每个程序都以为整台机器是它一个人的，其实底下是操作系统在切来切去。
>
> 你现在敲的每一条命令，都是先经过操作系统，才碰到真正的机器。3-x2 讲的是一个电路怎么被接成「可写的地址」；3-x3 讲的「壳」，就是人跟操作系统之间的一层翻译；3-x4 讲的内核，就是操作系统最核心、离硬件最近的那一部分。
>
> 为什么科学家会想到「给硬件封装一个系统」？因为**裸机太反人类**。每个程序员都得自己处理「怎么读盘、怎么显示字符、怎么在两个程序之间切换」，等于每个人重新发明轮子，而且换个型号的机器就全废。操作系统就是那个「一次写好、大家都用」的轮子——它把硬件最脏、最乱的细节藏起来，只给程序一个干净、稳定的接口。这一念之差，把「会摆弄机器的人」和「会写程序的人」分成了两种职业。

## 3.1.5 Before Unix: software was built for one machine

The computing world of the late 1960s looked nothing like today's. **"General purpose" barely existed:**

- Every computer was bought to **solve one organisation's particular problem** — trajectories for a rocket programme, hull lines for a shipyard, ledgers for a bank. Software was **commissioned machine by machine**.
- Change the machine and the software usually had to be **rewritten**, because every vendor's hardware and instruction set differed. A program could not move house.
- A system had to be **set up and maintained by a team, by hand**. You did not insert a disc and click twice.
- None of it was **aimed at the general public**. Machines and software were **extremely expensive**, and there was a wall between ordinary people and them.

The situation resembles **the early internet before HTTP**: many networks, each with its own protocols, unable to connect, let alone agree. The chaos only settled once someone published a common rule everyone could accept. Unix was to play exactly that role in the world of software.

> 1960 年代末的计算机世界，和今天完全不同。那时**几乎没有「通用」这回事**：
>
> 每一台计算机，都是为了**解决某一家单位的特定问题**而买来的——造火箭的算弹道、造船的算水线、银行算账。软件是跟着机器**一家一家定做**的。换一台机器，软件基本要**重写**，因为每家的硬件、每家的指令都不一样。程序没法「搬家」。一套系统要靠**一队人手动架设、手动维护**，不是装个光盘点两下就完事。这些东西**面向的不是普通大众**，是少数买得起的大机构——机器和软件都**极其昂贵**，普通人和它们之间隔着一道墙。
>
> 这个局面，很像**互联网早期、HTTP 协议出现之前**：一堆各自为政的网络，各有各的协议，连不起来，也谈不上「统一」。直到有人定出一个大家都能接受的公共规则，混乱才慢慢收束。Unix 要扮演的，正是计算机软件世界里那个「公共规则」的角色。

## 3.1.6 Bell Labs, Unix, and "everything is a file"

In the late 1960s a group at Bell Labs — **Ken Thompson, Dennis Ritchie** and others — joined **Multics**, a large time-sharing system project. Multics was too ambitious and did not go well; it never went far. But the people involved learned a great deal about how a system should be built, and how it should not.

When the project fell apart, Thompson wanted to play a game he had written on a small idle machine, and along the way wrote a compact, sufficient system. In 1971 it got a name: **Unix**.

Unix made several decisions that still shape your machine:


- **Everything is a file.** Keyboard, screen, disk, network connection — all treated as files. So "read from the keyboard" and "read from a disk file" are the same action. You will see in 3-x4 that even a directory is a kind of file.
|  |  |
| --- | --- |
- **Small tools, joined by pipes.** One program does one thing well; for anything complex, join several with `|`. The pipe you learn in 3-x4 is a rule settled more than fifty years ago.
- **Rewritten in C.** Ritchie invented C in order to write Unix, then rewrote Unix itself in C. That made Unix portable for the first time: change the hardware, and you did not rewrite the whole system. C is also the language this course uses.

Unix itself was commercial and not free. That is the seed of every fight that followed.

> 1960 年代末，贝尔实验室的一群人（**Ken Thompson、Dennis Ritchie** 等）参与了一个叫 **Multics** 的大型分时系统项目。Multics 野心太大、推进不顺，项目最终没走远，但参与者在里面学到了很多关于「系统该怎么搭、怎么不该搭」的教训。
>
> 项目散伙后，Thompson 想在一台闲置的小机器上玩一个自己写的游戏，顺手就写出了一个精简的、够用的系统。1971 年，它有了名字：**Unix**。
>
|  |  |
| --- | --- |
> Unix 做出几个影响至今的决定：**一切皆文件**——键盘、屏幕、硬盘、网络连接，在 Unix 里统统被当成「文件」来处理，所以「读键盘输入」和「读磁盘文件」用同一套动作，你会在 3-x4 看到，连目录都是文件的一种；**小而专的工具，用管道串起来**——一个程序只做好一件事，要复杂的活，就把几个程序用 `|` 接起来，你在 3-x4 学的管道，就是五十多年前定下的规矩；**用 C 语言重写**——Ritchie 为了写 Unix 发明了 C，后来又把 Unix 本身用 C 重写了一遍，这让 Unix 第一次能搬到别的机器上，换硬件不用重写整个系统。
>
> Unix 本身是商业的、不免费的。这就埋下了后面一切纷争的种子。

## 3.1.7 From Unix to Unix-like: a tree that keeps forking

Because Unix was good, and because C made it portable, a whole family grew around it. The forks of that tree are where the names you hear today come from:

- **BSD** — the version made at the University of California, Berkeley, from Unix source with its own additions. FreeBSD, NetBSD and OpenBSD descend from it.
- **System V** — the other commercial line of Unix.

**"Unix-like"** names the systems that look and behave like Unix without necessarily using that original source. The largest new branch on the tree is **Linux**.

Here is the distinction that matters most and gets mixed up most often:

- **The Linux kernel.** In 1991 a Finnish student, **Linus Torvalds**, wrote a working, free kernel — free to use, modify and redistribute. It is the core of the operating system, but **a kernel alone gives you nothing you can operate**: you face a pile of bare commands.
- **A Linux distribution.** A kernel is not enough. Someone has to package the kernel plus tools plus a package manager plus a desktop into one installable whole; that is a **distribution** (distro). Ubuntu, Debian, Mint and deepin are distributions — they run **the same Linux kernel** and differ in everything wrapped around it.

So "I installed Linux" is strictly incomplete: you installed **some distribution**, and the kernel inside it is the thing called Linux. 3-x4 uses this distinction constantly.

> 因为 Unix 好用、又因为 C 让它能移植，围绕它长出了一整个家族。这棵树的分叉，就是你今天听到各种名字的来源：**BSD**——加州大学伯克利分校拿 Unix 的源码做的一套，加了自己的东西，后来的 FreeBSD、NetBSD、OpenBSD 都是它的后代；**System V**——Unix 的另一条商业主线。
>
> 而「**类 Unix（Unix-like）**」这个词，指的是「长得像 Unix、行为像 Unix、但不一定真用过那套源码」的系统。这棵树最大的一根新枝，叫 **Linux**。
>
> 这里有个最关键、也最容易搞混的区分：**Linux 内核**——1991 年，芬兰学生 **Linus Torvalds** 写了一个能跑的、自由的（可自由使用、修改、再分发）内核，叫 Linux，它是操作系统最核心的那一块，但**光有内核你什么都干不了**；**Linux 发行版**——光有内核不行，得有人把内核 + 工具 + 包管理器 + 图形界面打包成一整套能装的东西，这就是**发行版（distribution，distro）**，Ubuntu、Debian、Mint、deepin 都是发行版，它们用的是**同一个 Linux 内核**，差别全在内核外面那一层。
>
> 所以「我装了 Linux」严格说是不完整的：你装的是「某个发行版」，它里面那个内核才叫 Linux。这个区分，3-x4 会反复用到。

## 3.1.8 Apple, iOS, and why it counts as Unix-like

Apple's macOS (earlier Mac OS X, earlier still NeXTSTEP) arrives by a different route from Linux: its core comes from the BSD branch. macOS is certified as a **Unix-like** system — its shell, filesystem and commands follow Unix rules, and you can type `ls`, `grep`, `ssh` in a macOS terminal.

**iOS** is the phone system, and it shares the same core (Darwin), so iOS is **Unix-like** underneath as well. But a phone has no full desktop command-line environment and will not run arbitrary programs — Apple keeps it far more locked down than a desktop. So: **iOS counts as Unix-like, but you are not using it as a Unix user**; same bloodline, different fence.

> 苹果的 macOS（早年的 Mac OS X、再早的 NeXTSTEP）有一条和 Linux 不同的来路：它的底层核心来自 BSD 那一支。macOS 在认证上是一个**类 Unix** 系统——它的壳、文件系统、命令，都遵循 Unix 那套规矩，你在 macOS 的终端里能敲 `ls`、`grep`、`ssh`。
>
> **iOS** 是给手机做的系统，它和 macOS 共享同一个底层核心（Darwin），所以 iOS 在骨子里也是**类 Unix**。只是手机上没有桌面电脑那一套完整的命令行环境、也不能随意装任意程序——苹果把它锁得比桌面系统严得多。所以结论是：**iOS 算类 Unix，但你不是以一个「Unix 用户」的方式在用它**；手机和电脑，同样的血统，不同的围栏。

## 3.1.9 Microsoft, Windows, and the other road

Microsoft took a road entirely parallel to Unix.

In 1981 IBM launched the personal computer (PC) and outsourced its operating system to Microsoft's **MS-DOS** — a single-user, single-task command line. You typed one command, it ran one thing; several programs at once did not exist.

Later Microsoft put a graphical layer on top of DOS: Windows 1.0 (which went nowhere), then Windows 3.0 / 3.1, then the hugely successful Windows 95, and the GUI became the main event. But the command-line habits underneath — drive letters (`C:`, `D:`), backslash paths (`C:\Windows`), `.exe` executables — all came down from DOS.

**Windows NT** (1993) is Microsoft's rewritten modern kernel, and every Windows still maintained today (Windows 10/11 included) descends from it. Windows and Unix are two independent bloodlines: **Windows is neither Unix nor Unix-like**. It has its own shell (`cmd.exe`, later PowerShell), its own path rules, its own permission model. That is why, in 3-x3 and 3-x4, the same job is written differently on Windows and Linux — they are not two accents, they are two languages.

> 微软走的是一条和 Unix 完全平行的路。
>
> 1981 年，IBM 推出个人电脑（PC），操作系统外包给了微软的 **MS-DOS**——一个单用户、单任务的命令行系统。你敲一条命令，它执行一条，没有「多个程序一起跑」这回事。
>
> 后来微软在 DOS 之上加了图形界面，先是 Windows 1.0（没火起来），到 Windows 3.0 / 3.1、再到大获成功的 Windows 95，图形界面成了主角。但底下那套命令行的习惯——盘符（`C:`、`D:`）、反斜杠路径（`C:\Windows`）、`.exe` 可执行文件——都还是 DOS 时代传下来的。
>
> **Windows NT**（1993）是微软重写的现代内核，今天所有还在维护的 Windows（包括 Windows 10/11）都是它的后代。Windows 和 Unix 是两条独立的血脉：**Windows 不是 Unix，也不是类 Unix**，它有自己的壳（`cmd.exe`、后来的 PowerShell）、自己的路径规则、自己的权限模型。这就是为什么 3-x3 和 3-x4 里，同一件事在 Windows 和 Linux 上写法不一样——它们不是两种口音，是两套语言。

## 3.1.10 Android: a Linux kernel you never see

Phones bring another branch: **Android**. Android's **kernel is Linux**, and you barely notice — because the framework apps run on is nothing like desktop Linux. You cannot open a full Linux command-line environment on Android without installing an extra terminal app.

So Android sits in an odd place: **the kernel is Linux, but it is not used as desktop Linux**. Which is why people say "Android uses the Linux kernel" and rarely say "Android is Linux".

One table to sort the family out:

| System | Underlying bloodline | Can you type Unix commands in a terminal? |
|:---|:---|:---|
| Linux distributions (Ubuntu etc.) | Linux kernel | Yes — that is what it is |
| macOS | BSD / Unix-like | Yes, terminal included |
| iOS | Same core as macOS (Darwin), Unix-like | Not freely; locked down |
| Windows | Independent (NT) | No (cmd/pwsh exist, different syntax) |
| Android | Linux kernel | Not directly; needs an extra terminal |

> 手机这边还有一支：**Android**。Android 的**内核就是 Linux**，但你在手机上几乎感觉不到——因为 Android 上面那套给 App 用的框架跟桌面 Linux 完全不是一回事。你没法在 Android 上直接敲一个 Linux 命令行的完整环境（得装额外的终端 App 才行）。
>
> 所以 Android 的处境很微妙：**内核是 Linux，但它通常不被当作「桌面 Linux」来用**。这也是为什么人们会说「Android 用了 Linux 内核」，却很少说「Android 就是 Linux」。
>
> 一句话理清这几家：

| 系统 | 底层血统 | 你能不能在终端里敲 Unix 命令 |
|:---|:---|:---|
| Linux 发行版（Ubuntu 等） | Linux 内核 | 能，这就是它的本来面目 |
| macOS | BSD / 类 Unix | 能，自带终端 |
| iOS | 与 macOS 同核心（Darwin），类 Unix | 不能随意，锁得严 |
| Windows | 独立血脉（NT） | 不能（有 cmd/pwsh，但语法不同） |
| Android | Linux 内核 | 不能直接，要装额外终端 |

## 3.1.11 The folders on your machine: three families, three homes

Each system organises "where things go" differently. You only need to recognise three homes:

- **Windows**: your personal files live under `C:\Users\<your name>\`, and the environment variable `%USERPROFILE%` points there. Programs and system files have their own split: `C:\Program Files\`, `C:\Windows\`.
- **Linux**: `/home/<you>` is your home, written `~` for short. `/etc` holds system configuration, `/usr/bin` holds programs (which is why PATH works), `/tmp` is scratch space.
- **macOS**: also `~` for home, with a path style almost identical to Linux.

The point is not to memorise the directories but to see the idea behind them: **your files and the system's files are separated from day one.** You write code and save documents in your own home; system programs and configuration you read, not edit. The permissions section of 3-x4 is exactly about which places you may touch and which need elevation.

> 不同系统把「东西放哪」这件事组织成了不同的样子。你只需要认三个「家」：**Windows**——你的个人文件默认在 `C:\Users\<你的用户名>\`，环境变量 `%USERPROFILE%` 就指它，程序装在哪、系统文件在哪，另有一套 `C:\Program Files\`、`C:\Windows\` 的分工；**Linux**——`/home/<你>` 是你的家，简写 `~`，`/etc` 是系统配置，`/usr/bin` 是程序（PATH 能用就靠它），`/tmp` 是草稿区；**macOS**——同样用 `~` 指家目录，路径风格和 Linux 几乎一样。
>
> 关键不是背全这些目录，而是看懂背后的思路：**你的文件，和「系统的东西」，从第一天起就被分开放。** 你写代码、存文档，永远在你自己的「家」里；系统自己的程序、配置，你平时只看、不改。3-x4 的权限那一节，讲的就是「哪些地方你能碰、哪些要提权」。

## 3.1.12 The circuit page became its own file

Up to here the story has been history. The next thing to explain is the present — what actually happens inside the machine after you press the power button.

It did not fit. To explain "how a circuit gets programmed" properly you have to start with why MOS beat the bipolar transistor, then how a latch holds one bit, how a decoder turns a set of voltages into one lit wire, how tri-state buffers let ten devices share one bus without a fight, how a single write splits into five bus phases, and what chip select and a stalled `READY` are each doing. That is not a section; it is a page.

So it became one: **3-x2, From a Circuit to a Programmable Device**. A detail manual, no assignment, slow reading allowed, skip what does not land.

One sentence to carry out of it:

> The number you write ends up as a voltage on some wire; and someone, beforehand, wired that wire into a meaningful place. **"Programming the circuit" = writing a number to an address, and an address is a set of voltages on a few wires.**

> 前面讲的是「历史」，本来该接着讲「此刻」——开机键按下之后，机器里到底发生了什么。
>
> 写到一半发现放不下。要让「一个电路怎么被编程」讲清楚，得从 MOS 管为什么赢过三极管讲起，然后是锁存器怎么咬住一个 bit、译码器怎么把一组电平变成一根被点亮的线、三态门怎么让十个设备共用一组线而不打架、一次写操作在导线上分成哪几个节拍、片选和被拖住的 `READY` 各是什么角色。一页纸塞不下，硬塞进去只会剩下一堆名词。
>
> 所以它单独成了一页：**3-x2《从一块电路到一个可编程的设备》**。那是纯细节手册，不布置作业，可以慢读，读不懂的地方先跳过。
>
> 这里只留一句话当路标：你写的那个数，最终变成了某根导线上的电压；而有人事先把那根导线接成了一个有意义的位置。**「对着电路编程」= 往一个地址写一个数，而这个地址，物理上是几根线上的电平组合。**


## 3.1.13 Registers and instruction sets: the CPU's dialect

One more piece of hardware background, so that 3-x5 does not read like a foreign language.

A CPU contains a set of **registers** — the smallest, fastest storage, right next to the arithmetic unit, and the only storage the CPU can compute on directly. Their names change with the architecture:

- **x86-64** (most likely your machine): `rax rbx rcx rdx rsi rdi rbp rsp r8–r15`.
- **ARM64** (phones, Apple Silicon): `x0`–`x30`, `sp`.
- **RISC-V** (teaching, embedded): `a0`–`a7` for arguments, `t0`–`t6` temporaries, `s0`–`s11` saved.

Different names mean a different **instruction set architecture (ISA)** — a different set of machine instructions the CPU recognises. x86 instructions and RISC-V instructions are not the same thing, so one action ("jump if equal") is `cmp` plus `je` on x86 and a single `beq` on RISC-V. Neither is wrong; they are two dialects. 3-x5 walks you through real x86 disassembly so you can see the dialect for yourself.

> 最后补一块硬件底子，好让 3-x5 读汇编时不陌生。
>
> CPU 里有一组**寄存器**——离它最近、最快的一小格存储，CPU 只能直接对寄存器里的值做运算。这些寄存器的名字，随 CPU 的架构而变：**x86-64**（你的电脑大概率是这个）`rax rbx rcx rdx rsi rdi rbp rsp r8–r15`；**ARM64**（手机、Apple Silicon）`x0`–`x30`、`sp`；**RISC-V**（教学、嵌入式常见）`a0`–`a7` 传参、`t0`–`t6` 临时、`s0`–`s11` 保存。
>
> 寄存器名字不一样，背后是**指令集架构（ISA）**不一样——CPU 认的那套机器指令不一样。x86 的指令跟 RISC-V 的指令不是一回事，所以同一个动作（比如「相等就跳」），x86 写成 `cmp` + `je` 两条，RISC-V 写成 `beq` 一条。这不是谁对谁错，是两套方言。3-x5 会带你读一段真实的 x86 反汇编，你会亲眼看到这套方言长什么样。
>
> 一句话带走：**操作系统是人给硬件定的规矩，指令集是硬件自己定的方言。** 你写的程序要跑，得先被翻译成 CPU 的方言，再被操作系统安排到 CPU 上去。

---

## 3.1.14 One paragraph

Compress the whole page into one:

> A pile of MOS switches that can only do AND, OR and NOT, organised by the idea of the stored program, becomes a machine that executes instructions. The operating system gives that bare machine rules and manages its hardware. Unix, in an age when software was bespoke, expensive and immovable, laid down a common law — everything is a file, tools joined by pipes — which later grew into the Linux kernel and a crowd of distributions, and reached macOS and iOS through BSD. Windows took an independent road. The home directory on your disk, the addresses on the bus, the register dialects inside the CPU: all of them are riverbed left by that same river. Every term in 3-x2 through 3-x5 is a splash in it.

> 一堆只会「与或非」的 MOS 开关，被「存储程序」的想法变成能执行指令的机器；操作系统给这台裸机定了规矩、管了硬件；Unix 在「软件各自为政、又贵又难搬」的年代，定了「一切皆文件、工具用管道串」的公共规则，后来长出了 Linux 内核和一堆发行版，也借着 BSD 传给了 macOS 和 iOS；Windows 则走了另一条独立的路；你机器上的「家目录」、总线上那些「地址」、CPU 的「寄存器方言」，都是这条长河留下的河床。后面 3-x2 到 3-x5 的每一个名词，都是这条河里的一个水花。

---

## 3.1.15 No hand-in, three questions

Nothing to submit. But if you can answer these three without notes, you have actually read it:

1. Where is "I installed Linux" imprecise? (Hint: kernel versus distribution.)
2. iOS or Windows — which one is Unix-like? Why?
3. In your own words, what is software really doing when it "controls" hardware? (Hint: address.)

> 这一页不交任何东西。但如果你能不看笔记回答这三个问题，就说明你真的读进去了：
>
> 1. 「我装了 Linux」这句话哪里不准确？（提示：内核 vs 发行版）
> 2. iOS 和 Windows，哪个算「类 Unix」？为什么？
> 3. 按你此刻的理解，软件要控制一个硬件，本质上是在做什么？（提示：地址）
