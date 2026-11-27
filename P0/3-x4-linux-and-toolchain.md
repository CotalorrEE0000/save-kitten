# 3-x4 Linux, and a Toolchain Like the CI's

**Before you start.** This is not a "learn Linux" page. It exists for one concrete reason inside this course: the machine that will judge your code runs Linux, so you need to understand the environment your work will be tested in — its shell, its filesystem, its permissions, its packages. You are not collecting an operating system. You are removing a difference between your machine and the machine that checks your work.

> **开始之前。** 这一页不是「学 Linux」，它存在的原因只有一条，就在这门课里：将来判定你代码的那台机器跑的是 Linux，所以你得看懂你的作业将来会在什么样的环境里被检验——它的壳、文件系统、权限、包管理。你不是在收集一个操作系统，你是在消掉「你机器」和「检查你机器的机器」之间的差异。

**What "POSIX shell" means.** You will keep seeing this phrase in tutorials and READMEs. POSIX is a standard that describes, among many other things, how a shell should behave: how it splits a line into words, what `$PATH` means, what exit codes are, how `|` and `>` work. A shell that follows it is a "POSIX shell" — `bash`, `zsh`, `dash` all are. Windows has its own, different rules, which is why a script written for a POSIX shell does not run on Windows unchanged. The rest of this page shows the POSIX side; a later page tells you what you actually have to run on it.

> **「POSIX 壳」是什么意思。** 你在教程和 README 里会反复看到这个词。POSIX 是一套标准，规定了（除了别的很多事之外）一个壳该怎么表现：怎么把一行拆成词、`$PATH` 是什么意思、退出码是什么、`|` 和 `>` 怎么工作。遵守它的壳就叫「POSIX 壳」——`bash`、`zsh`、`dash` 都是。Windows 有自己一套不同的规则，所以给 POSIX 壳写的脚本拿到 Windows 上不能原样跑。这一页接下来展示 POSIX 这一侧；后面某一页会告诉你，你真正需要在这上面跑的是什么。

**Carry-over from 3-x3.** The rules you just learned do not change here — shell, PATH, how a name resolves. Only the defaults change: `;` becomes `:`, `C:\Users\<you>` becomes `~`, and "executable" stops being a file extension and becomes a permission bit. Nothing on this page re-teaches 3-x3; it re-runs it with different values.

> **从 3-x3 带过来的东西。** 你刚学的规则在这里一条都不改——壳、PATH、一个名字怎么被解析。变的只是默认值：`;` 变 `:`，`C:\Users\<你>` 变 `~`，「可执行」从文件扩展名变成一个权限位。这一页不重讲 3-x3，只是换一套值再跑一遍。

**Windows is enough for this page.** Most of what follows is reading, not running: a filesystem layout, permissions, a package manager. You can read all of it on your Windows machine. Only §3.4.7 wants a real Linux to run on, and it is deliberately deferred to a later page — skip it for now. If you *do* want a Linux of your own on this machine, §3.4.8 points you at the one optional way to get it; nothing else depends on it.

> **这一页只用 Windows 就够了。** 下面大部分是「读懂」，不是「跑起来」：一套文件系统布局、一套权限、一个包管理器，在你的 Windows 机器上就能读完。只有 §3.4.7 需要一台真的 Linux 来跑，而它被故意推迟到后面某一页——现在先跳过。如果你确实想在这台机器上装一个自己的 Linux，§3.4.8 会指给你那唯一一条可选的路，其余内容都不依赖它。

---

## 3.4.1 Two words people mix up: kernel and distribution

"Linux" is two different things that share a name, and the confusion starts on day one. The **kernel** is the core program that talks to the hardware: it schedules processes, moves data to and from disk, hands out memory. A **distribution** (distro) is a complete, installable system built *around* that kernel: the kernel plus a set of programs, a package manager, a default shell, and a look-and-feel. Ubuntu, Debian, Mint and deepin are all distributions; they all run the same Linux kernel, and they differ in everything wrapped around it. When a CI says it "runs Ubuntu", that tells you the kernel is Linux and the surrounding tools are Ubuntu's particular set. The fuller history — where this kernel came from and how it differs from other operating systems — is its own page (3-x1).

> 「Linux」是两样共用一个名字的东西，混乱从第一天就开始。**内核（kernel）**是那个跟硬件打交道的核心程序：它调度进程、在磁盘和内存之间搬运数据、分配内存。**发行版（distro）**是围绕这个内核搭起来的一整套可安装系统：内核加上一批程序、一个包管理器、一个默认壳、一套外观。Ubuntu、Debian、Mint、deepin 都是发行版；它们跑的是同一个 Linux 内核，差别全在内核外面包的那一层。CI 说它「跑 Ubuntu」，意思是内核是 Linux、外围工具是 Ubuntu 那一套。更完整的历史——这个内核从哪来、和别的操作系统差在哪——是单独的一页（3-x1）。

## 3.4.2 What "running on Linux" looks like from the outside

You do not need a Linux machine to read this page, but you will need one eventually, and there are three ways to get there:

- **The CI already is one.** When you push code, a Linux runner checks it. That is the machine this page is describing; you are reading its manual before you use it.
- **A cloud machine.** A virtual server you rent or a free CI account also runs Linux. Again, no install on your machine.
- **A Linux on your own computer.** This is the only one that touches your machine, and it is **optional** — see §3.4.8. It is not required for anything before a later page, and it is a real commitment (a second operating system to keep updated). Do not feel you have to install it to follow along.

> 读这一页不需要一台 Linux，但你迟早要有一台，路有三条：**CI 本身就是一台**——你推代码时，是某个 Linux runner 在检查，这一页描述的就是那台机器，你是在用它之前先读它的说明书；**云上的机器**——租一台虚拟服务器或用一个免费 CI 账号，同样是 Linux，还是不用在你机器上装；**你自己电脑上的一个 Linux**——只有这一条碰你的机器，而它是**可选**的，见 §3.4.8。它在后面某一页之前都不需要，而且是一笔真投入（第二个要持续维护的操作系统），不必为了跟上进度就非装不可。

---

## 3.4.3 Where things live

A Linux filesystem is one tree with everything mounted into it — no drive letters. The directory-by-directory tour (what `/etc`, `/usr/bin`, `/home`, `~/` each mean, and how Windows' `C:\Users\<you>` maps to the same idea) is part of the systems page (3-x1); here it is enough to know two of them for the commands below: `/home/<you>` is your files (where `~` points), and `/usr/bin` plus `/bin` are where programs live, which is why PATH works at all.

> Linux 的文件系统是一棵树，所有东西挂进去，没有盘符。逐个目录的巡礼（`/etc`、`/usr/bin`、`/home`、`~/` 各是什么，以及 Windows 的 `C:\Users\<你>` 怎么对应同一件事）放在系统那一页（3-x1）里；这里只要认得下面命令用到的两个：`/home/<你>` 是你的文件（`~` 就指它），`/usr/bin` 和 `/bin` 是程序住的地方，PATH 之所以能用，正是因为这些目录在它里面。

## 3.4.4 Permissions: three questions per file

Every file answers three questions: **who** may read it, **who** may write it, **who** may execute it. The answer is expressed for three audiences: the owner, the group, everyone else. `rw-r--r--` is `rw-` / `r--` / `r--`: owner reads and writes, group and others only read.

> 每个文件回答三个问题：**谁**能读、**谁**能写、**谁**能执行。答案按三种身份给出：属主、属组、其他人。`rw-r--r--` 就是 `rw-` / `r--` / `r--`：属主读写，属组和其他人只读。

Numbers are just the same thing in binary: `r=4, w=2, x=1`, added per audience. `chmod 644 file` is `rw-r--r--`; `chmod 755 prog` is `rwxr-xr-x`. Two cases that actually bite:

- A **directory** needs `x` to be entered at all. `chmod 644 somedir` makes it unreadable *and* unusable, and the error says "Permission denied" when you `cd`, not when you `ls`.
- A **script** needs `x` to run as `./name`. Without it the shell says "Permission denied", which is a *different* error from "command not found" — that distinction is the whole of 3-x3.

> 数字只是同一件事的二进制写法：`r=4、w=2、x=1`，按身份相加。`chmod 644` 就是 `rw-r--r--`，`chmod 755` 就是 `rwxr-xr-x`。真正会咬人的是两种情况：**目录**必须有 `x` 才能进，`chmod 644` 一个目录会让它既不能读也不能用，报错还出现在 `cd` 而不是 `ls`；**脚本**必须有 `x` 才能 `./名字` 跑，没有就报 "Permission denied"，而这和 "command not found" 是两个不同的错误——这个区别就是 3-x3 的全部内容。

`sudo` means "run this one command as root". It is not a mode you stay in. The habit that keeps a machine alive: read the command, decide whether it touches system paths, and only then add `sudo`. `sudo rm -rf /` is not a meme, it is a working command.

> `sudo` 的意思是「这一条命令以 root 跑」，不是一种你可以待着的模式。能保命的习惯：先读完命令，判断它有没有碰系统路径，再决定加不加 `sudo`。`sudo rm -rf /` 不是梗，它真能跑。

---

## 3.4.5 Processes, pipes, and exit codes

A shell is a process launcher. Everything else is plumbing: `|` pipes the output of one program into the input of the next, `>` overwrites a file and `>>` appends, `&&` runs the next command only if this one succeeded, `||` only if it failed. The same idea exists on every system; only the spelling changes. Here it is in the two Windows shells, then the POSIX shell:

```powershell
# PowerShell (pwsh) — recommended over cmd.exe
Get-Process | Where-Object Name -like 'svf*'     # pipe + filter
(Get-ChildItem).Count                            # count files without reading them all
./run_vectors tests/vectors.txt > out.txt 2> err.txt
./run_vectors tests/vectors.txt; if ($?) { "passed" } else { "failed" }
$LASTEXITCODE                                    # exit code of the last command: 0 means success
```

```bat
:: cmd.exe — old syntax; pipes and redirection work, but many jobs need another tool
dir /b | find /c /v ""                            :: count files
run_vectors tests\vectors.txt > out.txt 2> err.txt
run_vectors tests\vectors.txt && echo passed || echo failed
echo %errorlevel%                                 :: exit code
```

```bash
# POSIX shell (bash/zsh) — for comparison; you will need to actually use it on a later page
ps aux | grep svf
ls | wc -l
./run_vectors tests/vectors.txt > out.txt 2> err.txt
./run_vectors tests/vectors.txt && echo passed || echo failed
echo $?
```

> 壳就是个进程启动器，其余都是管道：`|` 把一个程序的输出接到下一个程序的输入；`>` 覆盖、`>>` 追加；`&&` 只在成功时继续、`||` 只在失败时继续。同样的道理每个系统都有，只是写法不同——上面依次是 PowerShell、cmd.exe、POSIX 壳三种写法。如果你在用 Windows 10，别守着 `cmd.exe`：装 **Windows Terminal（wt）** 配 **PowerShell（pwsh）**，比 cmd 好用得多，管道和对象的配合也更顺手。

Two keys, two different signals, and beginners press the wrong one: `Ctrl-C` interrupts the running process (exit code 130 on POSIX), `Ctrl-D` sends end-of-input and closes the shell, `Ctrl-Z` suspends and leaves a job behind — `jobs` lists it, `fg` brings it back.

> 两个键，两种信号，新手常按错：`Ctrl-C` 打断正在跑的进程（POSIX 上退出码 130），`Ctrl-D` 送输入结束、关掉壳，`Ctrl-Z` 是挂起，留下一个作业——`jobs` 列出来，`fg` 把它叫回来。

This is the same exit code the CI reads. When a workflow goes red, it is not "the computer is angry"; it is a number that was not zero, and the log tells you which command produced it.

> CI 读的就是这个退出码。流水线变红不是「电脑生气了」，是一个不为零的数字，日志里写着是哪一条命令给出的。

---

## 3.4.6 Packages: how tools get installed

Every Linux distribution installs programs through a **package manager** that keeps a central list of what is installed and upgrades it for you. The one you will most likely meet — and the one the CI uses — is `apt`, on Debian, Mint, Ubuntu and their relatives; deepin and other Debian-family systems use the same underlying `dpkg` packaging. The rule is simple: install **tools** through the package manager (`sudo apt install clang`), not by copying binaries into random folders — that keeps PATH honest and lets `apt` upgrade them later. Do not chase an exotic distro for this course; `apt` on Ubuntu or Mint is the boring, well-trodden choice, and that is exactly what you want while learning.

> 每个 Linux 发行版都用**包管理器**装程序，它维护一张「装了什么」的清单并替你升级。你最可能遇到、也是 CI 用的那个是 `apt`，跑在 Debian、Mint、Ubuntu 这一族上；deepin 等 Debian 家族的系统底层用的是同一套 `dpkg` 打包。规矩很简单：**工具**用包管理器装（`sudo apt install clang`），别把二进制拷进莫名其妙的目录——这样 PATH 才是诚实的，`apt` 以后也能替你升级。这门课别去追冷门发行版，Ubuntu 或 Mint 上的 `apt` 是无聊但被千万人踩平的路，而学习阶段你恰恰要的就是这种。

**Python's `pip` deserves a paragraph, because it is where people go wrong.** `pip` is not a system package manager; it installs Python libraries, and *where* it puts them differs by system:

- **Windows** — `pip install <pkg>` installs into the Python you ran it with, under `%APPDATA%\Python\PythonXX\site-packages` (or the install's own `site-packages`). The practical upshot: if you have two Pythons, `pip` and `python` must be the same one, or the package lands somewhere the interpreter never looks. `python -m pip install <pkg>` removes the guesswork by always using the `python` you named.
- **Linux** — the system Python is owned by the package manager, so `pip install` into it is refused or fights the next `apt` upgrade. The fix is a **venv**: `python3 -m venv .venv` creates a project-local Python, and `pip install` inside it goes to `.venv/`, touching nothing system-wide. Never `sudo pip install` on either system.
- **The mirror** — on a slow or blocked connection, pip's default index (`pypi.org`) can be painfully slow; pointing `pip` at a mirror (a `-i https://.../simple` argument, or an `index-url` in `pip.conf`) is the standard fix. It changes *where packages are fetched from*, not where they are installed.

> **Python 的 `pip` 值得单独说一段，因为错大多出在这里。** `pip` 不是系统包管理器，它装的是 Python 库，而装到**哪**因系统而异：**Windows** 上 `pip install <包>` 装进你运行它的那个 Python，落在 `%APPDATA%\Python\PythonXX\site-packages`（或该安装自己的 `site-packages`）里，实际后果是：如果你有两个 Python，`pip` 和 `python` 必须是同一个，否则包装到解释器永远不去找的地方；`python -m pip install <包>` 因为总是用你点名的那个 `python`，能免掉这种猜。**Linux** 上系统 Python 归包管理器管，直接 `pip install` 会被拒绝、或跟下次 `apt` 升级打架，正解是 **venv**：`python3 -m venv .venv` 建一个项目本地的 Python，在里面 `pip install` 装到 `.venv/`，不碰系统。两个系统都永远别 `sudo pip install`。**更新源**：网络慢或被墙时，pip 默认的 `pypi.org` 可能慢得难受，给 `pip` 指一个镜像（例如加 `-i https://.../simple` 参数，或在 `pip.conf` 里配 `index-url`）是标准解法——它改的是「从哪下载」，不是「装到哪」。

After installing anything, `command -v <name>` (POSIX) or `where.exe <name>` (Windows) is the check. If it prints nothing, PATH has not seen the new directory yet — reopen the shell before concluding the install failed.

> 装完任何东西，`command -v <名字>`（POSIX）或 `where.exe <名字>`（Windows）就是验收。什么都不打印，说明 PATH 还没看到新目录——先重开壳，再下结论说装失败。

---

## 3.4.7 What you will run on Linux — but later

The one thing this page cannot show you on Windows is a memory-error report: it needs a real Linux to run on, and the tool that produces it is the subject of a later page. That page will come back here and give you the exact commands. For now, the point of *this* page is to make sure that when you see those commands you already know what they are standing on: a kernel, a filesystem of directories, permissions, pipes, exit codes, and a package manager. All of that you can learn and check today, on Windows, with nothing installed.

> 这一页唯一没法在 Windows 上演示的，是一份内存错误报告：它需要一台真的 Linux 来跑，而造出它的那个工具是后面某一页的正题。那一页会回到这里，把确切命令给你。而现在，这一页的意义是：等你看到那些命令时，你已经知道它们站在什么上面了——一个内核、一套目录文件系统、权限、管道、退出码、一个包管理器。这些今天在 Windows 上、什么都不装，就能读懂并核对。

## 3.4.8 Optional: a Linux of your own (WSL)

If you want to *run* Linux on this Windows machine rather than just read about it, the lowest-friction way is **WSL** (Windows Subsystem for Linux): it runs a real Linux kernel inside a lightweight virtual machine that Windows manages for you. But be honest about the cost before you start — it is a second operating system to install, update and occasionally debug, and it is **not required** for this course; the CI already provides the Linux your code will be judged on. If you are a beginner and your machine is your only computer, the safe call is to skip this and use the CI when the later page needs it.

> 如果你想在这台 Windows 上真的**跑** Linux、而不只是读读它，最省事的路是 **WSL**（Windows Subsystem for Linux）：它在 Windows 替你管理的一台轻量虚拟机里跑一个真正的 Linux 内核。但动手前先把成本说清楚——它是第二个要安装、更新、偶尔还要排查的操作系统，而且**不是这门课的必需**；判定你代码的那台 Linux，CI 已经替你备好了。如果你是新手、这台机器又是你唯一的电脑，稳妥的选择是跳过它，等后面那一页需要时直接用 CI。

The short version, if you decide you want it:

```powershell
wsl --install -d Ubuntu      # install once
wsl --list --verbose          # distro, WSL version, whether it is running
```

Then from any shell: `wsl` drops you in, `exit` comes back. Two things to remember, both covered above: Windows disks appear under `/mnt/` (so `C:\` is `/mnt/c/`), and a repository copied across that boundary can show phantom "modified" files because of line endings — keep repositories you compile on the Linux side, not on `C:`.

> 简短版，如果你决定要：`wsl --install -d Ubuntu` 装一次，`wsl --list --verbose` 看状态；之后在任何壳里敲 `wsl` 进去、`exit` 回来。两件事要记住（上面都讲过）：Windows 的盘挂在 `/mnt/` 下（`C:\` 就是 `/mnt/c/`）；跨这个边界拷仓库可能因为行尾出现幽灵「已修改」文件——要编译的仓库放 Linux 侧，别放 `C:`。

---

## 3.4.9 What counts as done

- You can say the difference between a kernel and a distribution in one sentence, and name at least two distributions.
- You can read an `ls -l` line and a `chmod` number and say who may do what.
- You can predict, before running it, whether `chmod 644 dir` will break `cd` or `ls`.
- You can tell "Permission denied" from "command not found" from "No such file or directory", and say which layer produced each.
- You can write the pipe / redirect / short-circuit idiom in PowerShell, in cmd.exe, and in a POSIX shell, and say what each one does.
- You can say why `pip` on Windows and on Linux land packages in different places, and what a venv is for.

> - 能用一句话说清内核和发行版的区别，并至少说出两个发行版的名字。
> - 能读一条 `ls -l` 和一个 `chmod` 数字，说出谁可以对它做什么。
> - 跑之前就能判断 `chmod 644` 一个目录会先坏在 `cd` 还是 `ls`。
> - 能分清 "Permission denied"、"command not found"、"No such file or directory"，并说出各自是哪一层给的。
> - 能用 PowerShell、cmd.exe、POSIX 壳各写一遍管道/重定向/短路那句，并说清每个在做什么。
> - 能说清为什么 `pip` 在 Windows 和 Linux 上把包装进不同的地方，以及 venv 是干嘛的。

**Hand in one file**: `submits/<handle>/P0/LINUX.md`, using the template below. No repository change this time; the evidence is your understanding and your terminal output on Windows.

> **交一个文件**：`submits/<handle>/P0/LINUX.md`，用下面的模板。这次不改仓库，证据是你在 Windows 上的理解和终端输出。

**Keep one sentence**: the same code behaves differently on two systems not because the code changed, but because the defaults did — path, permission, line ending. Learn the defaults, and half of your "weird bugs" stop being weird.

> **记住一句**：同一份代码在两个系统上表现不同，不是代码变了，是默认值变了——路径、权限、换行。把默认值认下来，一半的「玄学 bug」就不再玄。

---

## 3.4.10 What comes next

One page of optional reading follows. 3-x5 takes a single C statement and follows it down to the instructions your CPU actually runs — no assignment, twenty minutes. It is the shortest honest answer to "what does the compiler do", and it is what makes the word "undefined" stop being abstract.

> 接下来是一页可选读物。3-x5 拿一条 C 语句，一路跟到 CPU 真正执行的指令——不布置作业，二十分钟。那是「编译器到底做了什么」最短的、不糊弄人的答案，也是让「未定义」这个词不再抽象的东西。

After that, lesson 4 goes back to the file itself: bytes, byte order, and the specification your C code will have to satisfy.

> 再往后，第 4 讲回到文件本身：字节、字节序，以及你的 C 代码将来要满足的那份规范。

See you there.

> 到时见。

---

## Hand-in template (English)

```text
# Linux and toolchain — self check

- Kernel vs distribution, in one sentence, plus two distribution names:
- One `ls -l` line I read out loud, and what each column means:
- One `chmod` number, and who may do what as a result:
- The pipe / redirect / short-circuit idiom, written in PowerShell, cmd.exe, and a POSIX shell:
- What `pip` installs where on Windows, and what a venv is for:
- One error I met that was "command not found", and one that was "Permission denied", with which layer said each:
- Something that behaved differently between two shells, and my explanation:
- (Optional) Did I install WSL? If yes, the `uname -a` line; if no, why I skipped it:
- Before this page I thought ..., now I know ...:
- Commit message (course format):
- Entries in git status that are not mine (none, or list them):
```

## 提交模板（中文）

```text
# Linux 与工具链自检

- 内核和发行版的区别（一句话），加两个发行版名字：
- 我读出的一条 `ls -l`，以及每一列是什么意思：
- 一个 `chmod` 数字，以及它带来「谁可以做什么」：
- 管道/重定向/短路那句，分别用 PowerShell、cmd.exe、POSIX 壳写一遍：
- `pip` 在 Windows 上装到哪，venv 是干嘛的：
- 一个我遇到的 "command not found"，一个 "Permission denied"，各自是哪一层在说：
- 一件事在两个壳之间表现不同，以及我的解释：
- （可选）我装 WSL 了吗？装了贴 `uname -a`；没装写为什么跳过：
- 这一页之前我以为……，现在我知道……：
- 本次提交信息（课程格式）：
- git status 里不是我写的条目（无，或写具体名字）：
```
