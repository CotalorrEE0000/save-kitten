# 3-x3 Shell, PATH, and What a Command Really Is

**Before you start.** Three things get called "the terminal" and they are not the same: the window (Windows Terminal, Ghostty, iTerm2), the program that reads your line (PowerShell, cmd.exe, zsh, bash), and the prompt string itself. This page takes them apart, then walks down the one mechanism behind almost every "command not found" you will ever see: PATH. At the end you write a program of your own and make it callable from any directory.

> **开始之前。** 有三样东西都被叫做「终端」，其实不是一回事：窗口（Windows Terminal、Ghostty、iTerm2）、读你那一行的程序（PowerShell、cmd.exe、zsh、bash）、以及提示符那串字符本身。这一页把它们拆开，然后一路走到底下那个机制——PATH，几乎所有「命令找不到」都出在这里。最后你自己写一个程序，让它从任何目录都能被调用。

**You do not need admin rights for this page.** Only §3.3.4 touches privileges, and it only asks you to *check* whether you have them.

> **这一页不需要管理员权限。** 只有 §3.3.4 碰到权限，而且只是让你**判断**自己有没有。

**One page before this one.** 3-x2 stopped at the wire: address bus, decoder, chip select, a byte finally landing in a latch. This page climbs back up to what you type at. You do not need 3-x2 to follow it — but if you read that page, the sentence "a program is a file the shell finds and the kernel loads" will have a floor under it.

> **上一页停在那根导线上。** 3-x2 讲到地址总线、译码器、片选，一个字节最后落进锁存器为止。这一页爬回你手边：你敲的那一行。没读 3-x2 也能跟上——但读过之后，「程序就是一个文件，壳负责找到它、内核负责加载它」这句话底下就有地板了。

---

## 3.3.1 Three things people call "the terminal"

A terminal emulator draws characters and forwards your keystrokes. It has no idea what `git` is. Close the window and you kill whatever was running inside it — that is the only relationship it has with your work.

> **终端模拟器**负责画字符、把你的按键转给里面跑的程序。它不知道 `git` 是什么。关掉窗口就等于杀掉里面正在跑的东西——它和你的工作只有这一层关系。

A shell is the program inside the window. It reads one line, decides what to run, starts it, waits, and hands you back an exit code. `pwsh`, `cmd.exe`, `zsh`, `bash`, `fish` are all shells; they disagree about syntax, which is why a command that works in one can fail in another.

> **壳**是窗口里那个程序。它读一行、决定跑什么、启动它、等它结束、把退出码还给你。`pwsh`、`cmd.exe`、`zsh`、`bash`、`fish` 都是壳；它们的语法彼此不同，所以在一个壳里能跑的命令，换个壳就可能失败。

The prompt is just a string the shell prints before it waits. The default is deliberately plain: on a Unix shell it usually shows two facts, the current user and the current directory (`user@host`), and a marker that changes when you are root (`$` becomes `#`). Fancier prompts — colours, the last exit code, the current git branch — are additions people install on top, like Oh My Posh or Starship; the stock shell does none of that. What the prompt shows is customisable, which is why one person's terminal and another's can look nothing alike yet be the same shell.

> 提示符只是壳在等待输入前打印的一串字符。原版故意做得朴素：Unix 壳上通常只有两个事实——当前用户和当前目录（`用户@主机`），以及一个换身份时会变的标记（root 时 `$` 变 `#`）。更花哨的提示符——配色、上一条命令的退出码、当前 git 分支——都是人们额外装上去的（如 Oh My Posh、Starship），原版壳一概不做。提示符能自定义，所以两个人终端长得天差地别，可能用的是同一个壳。

One naming trap is worth a sentence. On a **Chinese** Windows, the shortcut that launches `cmd.exe` is labelled "命令提示符", so "命令提示符" can mean both "the prompt string" and "that specific program `cmd.exe`". The two senses are different things. On an **English** Windows the same shortcut is called "Command Prompt", and Windows will have already picked the matching language for you — what matters is not the label but which program that label starts.

> 这里有个命名坑值得说一句。在**中文** Windows 上，启动 `cmd.exe` 的那个图标就叫「命令提示符」，于是「命令提示符」既可以指「提示符那串字符」，又可以指「`cmd.exe` 这个具体程序」，两个意思不是一回事。在**英文** Windows 上同一个图标叫 "Command Prompt"——Windows 会按你的系统语言自动配对好，要紧的不是那个标签叫什么，而是它启动的到底是哪个程序。

Find out where you are before reading any further. Run the line for the shell you think you are in:

```powershell
$PSVersionTable.PSVersion          # PowerShell 7 -> prints 7.x
```

```bash
echo "$0"; echo "$SHELL"           # bash/zsh -> prints the shell's path
```

> 往下读之前先确认自己在哪个壳里。按你以为的那个壳，跑上面那一行。

In PowerShell, `cmd.exe` and Git Bash all three can be open at once in Windows Terminal, in three tabs, on the same machine, with different `PATH` inherited at different moments. "It worked a second ago" usually means "it worked in the other tab".

> 在 Windows Terminal 里，PowerShell、`cmd.exe`、Git Bash 可以同时开着三个标签页，同一台机器、不同时刻继承的 `PATH`。所谓「刚才还能跑」，十次有八次是「刚才在另一个标签页里跑」。

---

## 3.3.2 Anatomy of one command

Take a command you have already typed:

```bash
git commit -m "fix: stage only one file"
```

Four different things live in that line, and only the first is a program:

1. `git` — a **program name**. The shell has to find the file.
2. `commit` — a **sub-command**. It is not a program; it is a string handed to `git`, which dispatches on it itself.
3. `-m` — an **option**, also just a string for `git`.
4. `"fix: stage only one file"` — **one argument**. The quotes exist to keep the spaces inside it; remove them and `git` receives five arguments and fails.

> 这一行里有四样东西，只有第一个是程序：`git` 是**程序名**，壳得先找到这个文件；`commit` 是**子命令**，它不是程序，只是传给 `git` 的一个字符串，由 `git` 自己分派；`-m` 是**选项**；`"fix: ..."` 是**一个参数**，引号的作用就是让空格留在里面，去掉引号 `git` 会收到五个参数然后失败。

Now the part that matters. Type a sub-command wrong, and a program name wrong, and compare the two errors:

```bash
git comit -m x
# git: 'comit' is not a git command. See 'git --help'.
# The most similar command is
#         commit
```

```bash
git-xxx
# bash: git-xxx: command not found
```

Same machine, same second, two different errors from two different layers. The first one is `git` talking: it was found, it ran, and it did not recognise its own argument. The second one is the shell talking: it never found anything to run.

> 同一台机器、同一秒，两个不同的错误，来自两个不同的层。第一条是 `git` 在说话：它被找到了、跑起来了，只是不认自己这个参数。第二条是壳在说话：它根本没找到东西可跑。

This is the general shape of every "not found" you will ever see. When the shell cannot find the name, it does not guess and it does not fall back to something similar — it stops and says so. That is why typing `clang` on a Windows machine where no C compiler is installed prints an error, and typing `rm` on Windows prints an error too: those are not Windows commands, and the shell reports "not recognized" without running anything. The same three causes sit behind all of them: the name is not on PATH at all, a file exists but cannot run, or the thing you are calling needs an interpreter that is not there. Ask which layer is complaining before changing anything.

> 这就是你今后会见到的所有「找不到」的共同形状。壳找不到名字时，它不会瞎猜、也不会退回某个相近的东西——它停下来，告诉你没找到。所以在一台没装 C 编译器的 Windows 上敲 `clang` 会报错，在 Windows 上敲 `rm` 也会报错：那些都不是 Windows 的命令，壳只会回一句「无法识别」，什么都不会执行。它们背后都是同一个原因的三张脸：这个名字根本不在 PATH 里、文件在但跑不起来、或者你要调的东西需要一个解释器而解释器不在。动手之前先问：这句话是哪一层在说。

---

## 3.3.3 PATH is a list, and the first hit wins

PATH is not a folder. It is a **list of folders**, separated by `;` on Windows and `:` on Unix. When you type a name, the shell walks that list from left to right and runs the first match it finds. Nothing else is consulted.

> PATH 不是一个目录，是一**串**目录：Windows 用 `;` 分隔，Unix 用 `:`。你敲一个名字，壳从左到右走过去，跑第一个命中的，别处一律不看。

Watch the order decide the winner. Two folders, same file name, different output:

```powershell
$env:PATH = "J:\tmp\shelltest\a;J:\tmp\shelltest\b;$env:PATH"
hi                 # hello from A
$env:PATH = "J:\tmp\shelltest\b;J:\tmp\shelltest\a;$env:PATH"
hi                 # hello from B
```

> 顺序决定谁赢：同一个文件名放在两个目录里，谁在 PATH 里靠前，跑的就是谁。（`a`、`b` 是随手建的两个目录，各放一个同名的 `hi.cmd`，一个打印 `hello from A`，一个打印 `hello from B`；路径换成你自己机器上任意两个目录就行。）

The current directory is **not** on that list — this surprises everyone once. PowerShell says so in its own words:

```powershell
local-hello
# local-hello: The term 'local-hello' is not recognized as a name of a cmdlet,
# function, script file, or executable program.
# Check the spelling of the name, or if a path was included, verify that the
# path is correct and try again.
```

Add `.\` and it runs. On Unix the same rule with a different prefix: `./local-hello`, otherwise `command not found`. The reason is old and still good: if the current directory were searched, opening a folder someone sent you and typing `ls` could execute their `ls`.

> 当前目录**不在**这个列表里——这条每个人都会栽一次。加 `.\` 就能跑；Unix 上是 `./`。原因很老但成立：如果当前目录参与查找，你打开别人发来的文件夹、敲一个 `ls`，跑的就是他的 `ls`。

Windows adds one more step: the extension. `PATHEXT` lists what counts as runnable — `.COM;.EXE;.BAT;.CMD;...` — so `.\local-hello` finds `local-hello.cmd` without you typing the extension, and `hello.exe` can be called as `hello`. That is why the same name behaves differently in PowerShell and in Bash: one appends extensions, the other does not.

> Windows 还多一步：扩展名。`PATHEXT` 列出什么算可执行（`.COM;.EXE;.BAT;.CMD;...`），所以 `.\local-hello` 找不到 `local-hello.cmd` 也会补上，`hello.exe` 也能用 `hello` 调。这就是同一个名字在 PowerShell 和 Bash 里表现不同的原因：一个会补扩展名，一个不补。

Three ways to ask "where does this name point":

```powershell
where.exe hello         # cmd + PowerShell; lists every match in PATH order
(Get-Command hello).Source
```

```bash
command -v ls           # /usr/bin/ls
```

> 三种问法，问的是同一件事：这个名字指向哪。`where.exe` 会把所有命中都列出来，第一行就是将来会跑的那个。

The four failures you will actually meet, in order of frequency: the file sits in `Downloads` and no folder on PATH contains it; you installed something but did not reopen the terminal, so the new PATH never reached your process; two copies exist and the older one is earlier in the list; the name is a typo. One sentence covers all four: **the name must match, a folder on PATH must contain it, and the extension must be one the shell accepts.**

> 真正会遇到的四种失败，按频率排：文件躺在下载目录，PATH 里没有任何一项包含它；装完了没重开终端，新 PATH 没进到你当前这个进程；机器上有两份，靠前的是旧的那份；名字拼错。四种都能被一句话覆盖：**名字得对、PATH 里得有一个目录装着它、扩展名得是壳认的。**

A change to PATH only affects processes started after it. `$env:PATH = "..."` changes the current window only; `setx PATH ...` changes it for future windows but not this one — and `setx` truncates at 1024 characters, which is a real way to break a Windows install. Set it through the system dialog unless you have a reason not to.

> 改 PATH 只影响之后启动的进程。`$env:PATH = "..."` 只改当前窗口；`setx PATH ...` 改的是以后的新窗口，当前这个不算——而 `setx` 会在 1024 字符处截断，这是真能把 Windows 环境改坏的一种方式。没有特别理由就用系统设置里那个对话框。

---

## 3.3.4 Administrator is a property of one process, not of you

On Windows, "running as administrator" means this one process asked for elevation and got it. It does not make the machine yours, and it does not carry over to the next window you open. Check it instead of guessing:

```powershell
net session
# System error 5 has occurred.        -> not elevated
# (no output, exit 0)                 -> elevated
```

> 在 Windows 上，「以管理员身份运行」指的是**这一个进程**申请了提权并且拿到了。它不会让这台机器变成你的，也不会传给你下一个打开的窗口。与其猜，不如查：`net session` 报 `System error 5` 就是没提权，没有输出、退出码 0 就是提权了。

What actually needs it: writing under `C:\Program Files` or `C:\Windows`, installing a driver, machine-wide environment variables (`setx /M`), anything touching `HKLM`. What does not: `git`, `pip install --user`, running a program you compiled, editing files in your own home directory. If a tutorial tells you to open an elevated shell for `git`, the tutorial is wrong.

> 真正需要提权的：往 `C:\Program Files`、`C:\Windows` 里写，装驱动，改机器级环境变量（`setx /M`），动 `HKLM`。不需要的：`git`、`pip install --user`、跑自己编译的程序、改自己家目录里的文件。哪个教程让你用管理员窗口跑 `git`，那个教程是错的。

On Unix the equivalent is `sudo`, which means "run this one command as root". `sudo -v` refreshes the credential cache and tells you whether you are allowed to. Do not run a root shell for a whole session; elevate per command, and let the prompt show you when you are root (`#` instead of `$`).

> Unix 上对应的是 `sudo`，意思是「这一条命令以 root 跑」。`sudo -v` 刷新凭据缓存，并告诉你有没有这个资格。不要整场都待在 root 壳里；按条提权，并且让提示符提醒你当前是 root（`#` 而不是 `$`）。

---

## 3.3.5 The assignment: write a program, put it on PATH, then get three things wrong

You are going to build the thing you have been calling "a command" all along. First as a script, then as a compiled binary, then you will remove each of the three conditions in §3.3.3 and read the error that comes back.

> 你要亲手造出那个一直被叫做「命令」的东西：先做成脚本，再做成编译好的二进制，然后把 §3.3.3 那三个条件一个一个拿掉，看清各自回来的错误。

**Step 1 — a script.** Windows, save as `hello.cmd`:

```bat
@echo off
echo hello %*
```

Unix, save as `hello.sh`, then `chmod +x hello.sh`:

```sh
#!/bin/sh
echo hello "$@"
```

The `%*` / `"$@"` part is what makes it behave like a command instead of a fixed string: it passes your arguments through. Try `hello world` and `hello "two words"` and see what each prints.

> **第 1 步——写个脚本。** Windows 存成 `hello.cmd`，Unix 存成 `hello.sh` 再 `chmod +x`。`%*` / `"$@"` 是让它像个命令而不像一句固定台词的关键：把你给的参数原样传出去。跑 `hello world` 和 `hello "two words"`，看两者各打印什么。

**Step 2 — give it a home.** Make one folder meant for your own tools. It can live on **any drive**, not just `C:` — `D:\tools`, `E:\bin`, whatever you like; the only thing that matters is that you add that folder to PATH, because the shell does not care where a program sits, only whether a folder on PATH contains it. This is exactly how every installer works: when you install a program and can then call it from the command line, the installer has silently added its install directory to PATH for you. Now you are doing the same thing by hand, for your own file. Put `hello.cmd` (or `hello.sh`) inside the folder, then add the folder to PATH for the current window first, so a mistake costs nothing:

```powershell
$env:PATH = "D:\tools;$env:PATH"     # your own directory
```

```bash
export PATH="$HOME/bin:$PATH"
```

> **第 2 步——给它一个家。** 先建一个只属于你自己的工具目录，放**哪个盘都行**，不一定非得 `C:`——`D:\tools`、`E:\bin` 随便你；唯一要紧的是把它加进 PATH，因为壳不在乎程序在哪个盘，只在乎 PATH 里有没有一个目录装着它。这正是每个安装程序都在做的事：你装完一个软件、接着就能在命令行里调用它，就是因为安装程序已经悄悄把它的安装目录写进了 PATH。现在你只是把这件事替自己的文件手动做一遍。把文件放进去，然后**先只改当前窗口**的 PATH——错了不花钱。

**Step 3 — call it from somewhere else.** `cd` to any other directory, run `hello shell`, then ask where it came from:

```powershell
where.exe hello
# D:\tools\hello.cmd
```

> **第 3 步——换个地方调它。** 换个目录调用，再问它从哪来。`where.exe` 的第一行就是答案。

**Step 4 — the same thing as a compiled program.** If you have a C compiler, this is the version that will matter for the rest of the course:

```c
#include <stdio.h>

int main(int argc, char **argv) {
    printf("hello");
    for (int i = 1; i < argc; i++) printf(" %s", argv[i]);
    printf("\n");
    return 0;
}
```

```bash
gcc -Wall -Wextra -o hello.exe hello.c
hello.exe world "two words"      # hello world two words
```

Copy `hello.exe` into the same `bin` folder and call it as `hello`. Now `where.exe hello` may list both `hello.exe` and `hello.cmd` — read the order and work out which one runs. If you have no compiler yet, skip this step; 3-x4 makes you install one and build for real.

> **第 4 步——做成编译好的程序。** 有 C 编译器的话，这就是剩下的课程里真正用得上的那个版本。把 `hello.exe` 拷进同一个 `bin` 目录，用 `hello` 调。这时 `where.exe hello` 可能同时列出 `hello.exe` 和 `hello.cmd`——读顺序，判断哪一个会跑。还没有编译器就跳过这一步，3-x4 会让你真的装一个、跑一遍。

**Step 5 — deliberately get three things wrong.** Each one breaks one condition from §3.3.3. Run all three, copy the error text verbatim.

1. **Wrong name** — `helo shell`. The shell looks, finds nothing, says so.
2. **Right name, folder not on PATH** — remove the folder from PATH in this window, run `hello shell` again.
3. **Right name, right folder, wrong extension** — on Windows, rename `hello.cmd` to `hello.txt` and run `hello`. Watch what `PATHEXT` does and does not rescue.

> **第 5 步——故意写错三处情况。** 每一处都恰好打掉 §3.3.3 里的一个条件，三处全跑，错误原文一字不改地抄下来：**名字错**（`helo shell`，壳找了一圈没找到，如实说）；**名字对但目录不在 PATH**（把目录从当前窗口的 PATH 里去掉，再跑 `hello shell`）；**名字和目录都对但扩展名不对**（Windows 上把 `hello.cmd` 改名成 `hello.txt` 再跑 `hello`，看 `PATHEXT` 能救什么、不能救什么）。

**Step 6 — write down which layer spoke.** For each of the three errors, one sentence: was it the shell that could not find the name, or a program that ran and complained? This is the whole point of the page; everything later — `clang-format`, `fuzz`, `cargo` — is the same question with different names.

> **第 6 步——写清是哪一层在说话。** 三处错误各写一句：是壳没找到名字，还是某个程序跑起来之后在抱怨。这一页的全部意义就在这里；后面所有 `clang-format`、`fuzz`、`cargo` 的报错，都是同一个问题换了名字。

---

## 3.3.6 What counts as done

- You can say, without notes, what the window does, what the shell does, and what the prompt is showing — and why the name "命令提示符" can mean two different things.
- You can take `git commit -m "..."` apart and name which token is a program, which is a sub-command, which is an option, which is an argument.
- You can explain the lookup rule in one sentence, including why the current directory is not searched, and what `.\` and `./` are for.
- You have a `hello` of your own that runs from any directory, and `where.exe hello` (or `command -v hello`) shows where it lives.
- You have all three wrong calls recorded with their original error text, each labelled with the layer that produced it.
- You can find PATH on your own machine and say whether the change you made was for this window or for every window.

> - 不看笔记能说清窗口干什么、壳干什么、提示符在显示什么，以及「命令提示符」这个名字为什么容易混。
> - 能把 `git commit -m "..."` 拆开，指出哪个是程序、哪个是子命令、哪个是选项、哪个是参数。
> - 能用一句话说出查找规则，包括为什么当前目录不参与查找、`.\` 和 `./` 是干什么的。
> - 手上有一个能从任何目录跑起来的 `hello`，`where.exe hello` 或 `command -v hello` 能指出它在哪。
> - 三处写错都有原文，并且每种都标了是哪一层在说话。
> - 能在自己机器上找到 PATH，并说清你这次改的是当前窗口还是所有窗口。

**Hand in one file**: `submits/<handle>/P0/SHELL.md`, using the template at the end of this page. No code file this time — the program lives on your machine, and what matters is whether you can tell the three layers apart.

> **交一个文件**：`submits/<handle>/P0/SHELL.md`，用本页末尾的模板。这次不收代码文件——程序活在你机器上，要看的是你能不能分清那三层。

**Keep one sentence**: a command is not a name you remember, it is a file the shell can find. When it fails, ask which of the three conditions broke — and then ask which layer is speaking.

> **记住一句**：命令不是你记住的一个名字，是壳能找到的一个文件。它失败的时候，先问三个条件里坏了哪一个，再问这句话是哪一层在说。

---

## 3.3.7 Where this leads

With the shell and PATH out of the way, 3-x4 asks the same questions again on Linux: a second shell, a different set of defaults, and the line between "works on my machine" and "works on the machine that checks your code". Nothing new to learn — the values change, not the concepts.

> 壳和 PATH 交代清楚之后，3-x4 把同一组问题搬到 Linux 上再问一遍：第二个壳、另一套默认值，以及「在我机器上能跑」和「在检查你代码的那台机器上能跑」之间那条线。没有新东西要学——变的是默认值，不是道理。

See you there.

> 那一页见。

---

## Hand-in template (English)

```text
# Shell and PATH — self check

- Shell and version I actually used (pwsh / cmd / bash / zsh):
- Where I found it (Windows Terminal tab / VS Code / other):
- One command taken apart: program / sub-command / option / argument
- The folder I created for my own tools:
- What I added to PATH, and whether it was this window or every window:
- Output of `where.exe hello` (or `command -v hello`), verbatim:
- My hello program: script / compiled binary / both
- Break 1 (wrong name) — error verbatim, and which layer said it:
- Break 2 (folder not on PATH) — error verbatim, and which layer said it:
- Break 3 (wrong extension) — error verbatim, and which layer said it:
- Am I elevated in this window, and how I checked:
- Before this page I thought ..., now I know ...:
- Commit message (course format):
- Entries in git status that are not mine (none, or list them):
```

## 提交模板（中文）

```text
# 壳层与 PATH 自检

- 我实际用的壳和版本（pwsh / cmd / bash / zsh）：
- 我从哪里打开的（Windows Terminal 标签页 / VS Code / 其他）：
- 拆开的一条命令：程序 / 子命令 / 选项 / 参数
- 我给自己的工具建的目录：
- 我往 PATH 里加了什么，改的是当前窗口还是所有窗口：
- `where.exe hello`（或 `command -v hello`）的原样输出：
- 我的 hello：脚本 / 编译出的二进制 / 两个都有
- 失败一（名字错）——错误原文，以及是哪一层在说：
- 失败二（目录不在 PATH）——错误原文，以及是哪一层在说：
- 失败三（扩展名不对）——错误原文，以及是哪一层在说：
- 当前窗口是否已提权，我怎么判断的：
- 这一页之前我以为……，现在我知道……：
- 本次提交信息（课程格式）：
- git status 里不是我写的条目（无，或写具体名字）：
```
