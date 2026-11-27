# Git Guide — Making a Clean Submission

## 1. Before You Start: Things a Computer Does Without Asking

> This lesson teaches **no new Git command**. It teaches you to see what you are about to hand in.
>
> Before you start, make sure you recognise four things. A folder holds files. A path tells you where a file is. A name beginning with a dot is a hidden file or folder — it is still there even if you cannot see it. And your editor quietly creates its own folders inside your project, such as `.idea/` or `.vscode/`, without asking you. You did not write those files, but Git notices them.
>
> Lesson 1 said this: `git add <file>` stages one file, while `git add .` stages **every change in the current directory**. Lesson 2 explained what `.gitignore` does and named editor folders such as `.idea/` and `.vscode/`. In the last practice run, an editor folder ended up inside a merge request. Those two earlier sentences are the whole fix. Nothing new needs to be learned — only used.
>
> If something on your screen looks wrong, the first question is never "did I break Git". It is "what did the computer put here that I did not write".

> 这一讲**不教新命令**，只教你「看清自己到底要交什么」。
>
> 开工前先认得四件事：文件夹里装文件；路径说明文件在哪；点号开头的名字是隐藏文件或隐藏文件夹，看不见不等于不存在；还有，编辑器会悄悄在项目里建自己的文件夹，例如 `.idea/`、`.vscode/`，不会问你。这些不是你写的文件，但 Git 会看见它们。
>
> 第一讲说过：`git add <文件>` 只暂存一个文件，`git add .` 会暂存**当前目录下全部改动**。第二讲讲过 `.gitignore` 的作用，也提到 `.idea/`、`.vscode/` 这类编辑器文件夹。上一次练习里，有人的合并请求里带进了一个编辑器自动生成的文件夹。把前面这两句话真正用一次，就是这一讲全部的内容——不用学新东西，只用把学过的用上。
>
> 屏幕上出现看不懂的东西时，先别问「我是不是把 Git 弄坏了」，先问「电脑在这里放了什么我没写过的东西」。

> **The setup I recommend / 我推荐的组合**: For this course, use **GitHub Desktop** from Lesson 2 §5 to look at your changes, and **Notepad** (or `echo >>` in Git Bash / WSL) to write the file. Do not write these files in an IDE: it creates `.idea/` / `.vscode/` folders and can save the file in the wrong encoding (see the Troubleshooting section of `submits/README.md`). I personally pair GitHub Desktop with `nvim`, but that is my own habit, not a requirement — `nvim` is not friendly to beginners, and this lesson neither teaches nor asks for it. Whichever tool you write with, open **Changes** in GitHub Desktop (or run `git status`) and look at what is ticked. That ticked list is exactly what you are about to hand in; the two views show the same thing.
>
> Editor shortcuts and the like do not belong in the lessons. Later in the course an `ultra/` folder will hold this kind of optional reading — look it up whenever you like, nothing here depends on it.

> **推荐组合**：本讲用第 2 讲第 5 节装好的 **GitHub Desktop** 看改动，用**记事本**（或 Git Bash / WSL 里的 `echo >>`）写文件。**不要用 IDE 写这些文件**：它会生成 `.idea/`、`.vscode/`，还可能把文件存成错误的编码（见 `submits/README.md` 的排查一节）。我自己日常是 GitHub Desktop 配 `nvim`，但那只是我的个人习惯，不是本课要求——`nvim` 对新手并不友好，本讲不教、也不要求用它。不管用什么工具写，都要在 GitHub Desktop 的 **Changes** 页（或跑一次 `git status`）看一眼被勾上了哪些文件；被勾上的那几行就是你要交出去的东西，两个界面看的是同一件事。
>
> 编辑器快捷键这类东西不进讲义。课程后段会有一个 `ultra/` 文件夹统一放这种可选读物，想看随时看，本讲不依赖它。

> **How to read and write a `.md` file / md 文件怎么读怎么写**: `.md` means Markdown. It is a **plain text file**, not a Word document — no fonts, no bold button, no hidden formatting. Notepad or the terminal can open it. Lesson 1 already used `cat <file>`; it prints the file exactly as it is stored, so it is the simplest way to check your work. A line starting with `# ` is a title; every other line is just a sentence. That is the only syntax this assignment needs. Do not paste from Word.
>
> Open the file with Notepad, type the text, save it, then run `cat <file>` again and read the lines on screen. If what you see is not what you meant, fix the file before you touch Git.

> `.md` 就是 Markdown，是**纯文本文件**，不是 Word 文档——没有字体、没有加粗按钮、没有隐藏格式，记事本或终端都能打开。第 1 讲已经用过 `cat <文件>`，它把文件里真正存着的内容原样打印出来，是复查最省事的办法。`# ` 开头的一行是标题，其余每行就是一句普通的话；这次作业用到的语法只有这两条。不要从 Word 里复制粘贴。
>
> 用记事本打开文件 → 打字 → 保存 → 再跑一次 `cat <文件>`，盯着屏幕确认内容真的存进去了。看到的和想写的不一样，先回去改文件，别急着碰 Git。

> **WARNING: Do not use `git add .` here**
> It is convenient, and it is exactly how a folder you never wrote gets into a commit. Name the file you mean, one by one.

> **警告：这次不要用 `git add .`**
> 它很省事，也正因如此，一个你根本没写过的文件夹会被一起交上去。这次请一个一个写出你要交的文件名。

---

## 2. The Assignment

> Submit **one file**: `submits/<handle>/P0/CLEAN.md`. Follow the layout in `submits/README.md`: your own folder, then a chapter folder (`P0` here), then the file — **three levels, do not skip one**. Replace `<handle>` with your own submission folder name. If the task post gives another file name, change only the name and keep every step below the same.
>
> The content is **not three sentences**. It is a filled-in checklist: §3 gives two complete templates, one in English and one in Chinese — copy either one into the file and write your answer on every underline. What is graded is the path list and the record, not the prose.

> 交**一个文件**：`submits/<handle>/P0/CLEAN.md`。按 `submits/README.md` 的目录结构：自己的文件夹 → 章节文件夹（这里是 `P0`）→ 文件，**一共三层，别少一层**。把 `<handle>` 换成你自己的提交目录名。任务发布里若指定了别的名字，只换名字，下面步骤一律不变。
>
> 这次**不是写三句话**，而是交一张**填好的自检表**：第 3 节有两份完整模板，英文一份、中文一份，任选一份整段复制进文件，在每条横线上写自己的答案。看的是那份路径清单和记录，不是文笔。

> Work through these in order:
>
> 1. Sync before you start, as Lesson 2 taught:
>
>    ```bash
>    git fetch upstream && git merge upstream/main
>    ```
>
> 2. Make a new branch. Never work on `main`.
> 3. Write your file with Notepad (or `echo >>`), then run `git status` and **read the whole output**. Anything you did not write yourself does not belong in this submission.
> 4. Open the repository's `.gitignore` and **read which lines it actually has** — never assume what is inside. That file was committed in the last merge, so this time you change nothing and do not put it in this merge request. Copy the lines you see into the checklist. If you think a line is missing, say so when you ask for help; do not edit the file yourself.
> 5. Stage by name, then commit with a **conventional commit message** (see the block at the end of this section):
>
>    ```bash
>    git add submits/<handle>/P0/CLEAN.md
>    git commit -m "docs: add submission check note"
>    ```
>
> 6. Sync once more before opening the merge request. Then list the paths your branch adds:
>
>    ```bash
>    git diff --name-only upstream/main...HEAD
>    ```
>
> 7. Paste that output **verbatim** into the merge request description — no deleting, no reformatting, no summarising. Then add one sentence saying **which rule made you exclude what**.
>
> A clean result is exactly one line: your `CLEAN.md`. If you see anything else, fix the branch first, then paste. The three-dot form compares against the point where your branch diverged from `upstream/main`, so this list is proof, not a summary.
>
> If the merge request is sent back, do not rewrite everything and hope. Look at **which path is wrong**, fix that one path, and paste the output again.

> 按顺序做：
>
> 1. 动手前先同步（第二讲教过）：`git fetch upstream && git merge upstream/main`
> 2. 建新分支，绝不在 `main` 上改
> 3. 用记事本（或 `echo >>`）写完文件，跑一次 `git status`，**把输出整段读完**。凡不是你亲手写的，都不属于这次提交
> 4. 打开仓库里的 `.gitignore`，**看清楚它实际有哪几行**，不要凭想象填。这份文件在上一次合并里已经交进仓库了，所以这次**什么都不用改**，也不要把它放进这次的合并请求；把实际看到的行抄进自检表。觉得少了哪一行，就写在提问里，不要自己改这个文件
> 5. 按名字暂存，然后用**规范提交信息**提交（格式见本节末尾那一整块）：
>
>    `git add submits/<handle>/P0/CLEAN.md`
>
>    `git commit -m "docs: add submission check note"`
>
> 6. 发合并请求前再同步一次，然后跑 `git diff --name-only upstream/main...HEAD`
> 7. 把输出**原样**贴进合并请求描述：不删行、不重排、不改写、不替它做总结。最后补一句「我按哪条规矩排除了什么」
>
> 干净的结果只有一行，就是那个 `CLEAN.md`。出现别的东西，先修分支再贴。三点语法比的是「你的分支从 `upstream/main` 分叉之后多出来的东西」，所以这份清单是证据，不是摘要。
>
> 被打回时不要整篇重写碰运气：**看具体是哪条路径不对**，只改那一条，再把输出贴一遍。

> **Commit messages must be conventional / 提交信息要规范**
>
> A commit message has two parts: a **type** and a **short description**, written as `type: description`. The type is not a label you pick by mood — it says what kind of change this commit makes, and later CI reads it to decide which checks to run. A Chinese title, a made-up type, or an empty `type()` makes that automatic check useless. Both of those appeared in the last practice run. So, from this submission onward: **lowercase, English, no name, and only the six types below**.
>
> - `docs:` — documentation only. A lesson note, a README edit, this `CLEAN.md` checklist. **This is the one you need this time.**
> - `feat:` — a new capability a user can see or call. Adding a function, a command, a screen.
> - `fix:` — repairing something that already exists but behaves wrong. A wrong result, a crash, a broken link.
> - `refactor:` — changing the shape of the code without changing what it does. Renaming, splitting a file, simplifying a branch.
> - `test:` — adding or changing tests only. A test case, a fixture, a conformance vector.
> - `chore:` — housekeeping that touches neither behaviour nor docs. Dependency bumps, `.gitignore`, CI config, build scripts.
>
> If one change fits two types, it is probably two commits — split it. The scope in brackets is optional and only worth writing when it means something (`fix(auth): ...`); when you have nothing to put there, drop the brackets entirely and write `feat: ...`, **never `feat(): ...`**. Keep the description short and in the imperative: `docs: add submission check note`, not `docs: I added a note`.
>
> **Why this is worth a whole block**: the type is the only part of a commit a machine can read. Once CI starts gating on it, `docs：添加说明` and `update stuff` are invisible — the check cannot tell whether to run. Write the type correctly now, and every later stage of this course keeps working automatically.

> **提交信息写规范**
>
> 一条提交信息分两部分：**类型**和**一句简述**，写成 `类型: 简述`。类型不是按心情挑的标签，它说明这次提交改的是哪一类东西；后面的 CI 会读它，决定该跑哪些检查。中文标题、自造类型、空着括号的 `type()`，都会让自动检查直接失效——上次练习里这几种都出现过。所以从这次起：**英文、小写、不带姓名，只用下面六类**。
>
> - `docs:` —— 只改文档。讲义笔记、README、这次的 `CLEAN.md` 自检表。**本次就用这个。**
> - `feat:` —— 新增一个用户能看到或能调用的能力：加函数、加命令、加界面。
> - `fix:` —— 修好本来就有、但行为不对的东西：算错、崩溃、链接失效。
> - `refactor:` —— 只改代码长相、不改行为：改名、拆文件、简化分支。
> - `test:` —— 只加或只改测试：用例、fixture、conformance 向量。
> - `chore:` —— 既不改行为也不改文档的杂务：依赖升级、`.gitignore`、CI 配置、构建脚本。
>
> 一次改动同时像两类，通常说明它该拆成两次提交。括号里的范围只在真有含义时才写（`fix(auth): ...`）；没内容就把括号整个去掉，写 `feat: ...`，**不要写 `feat(): ...`**。简述要短、用动词原形：`docs: add submission check note`，不写 `docs: I added a note`。
>
> **为什么这一整块值得单独讲**：类型是一条提交里唯一能被机器读懂的部分。等 CI 开始按类型分流，`docs：添加说明`、`update stuff` 这类写法等于不存在——机器判断不了该跑什么。现在把类型写对，后面每个阶段的自动检查才一直有效。

---

## 3. What Counts as Done

> - You can say, in your own words, what `git add .` does differently from `git add <file>`, and what it can accidentally bring along.
> - You can look at `git status` or the **Changes** page and point out which entries you wrote and which ones the computer created.
> - You can open, write, save and re-read a `.md` file without asking anyone.
> - You can pick the right commit type for a change and write a conventional English message.
> - You can open one merge request that contains only one task — a single file, or the set of files that belong to the same piece of coursework — with a path list anyone can re-run.

> - 能用自己的话说清 `git add .` 和 `git add <文件>` 的差别，以及它会顺手带进来什么。
> - 看着 `git status` 或 GitHub Desktop 的 **Changes** 页，能指出哪些是我写的、哪些是电脑自己生成的。
> - 能自己打开、写、保存、再读一遍一个 `.md` 文件，不用问人。
> - 能按改动性质选对提交类型，写出全英文的规范提交信息。
> - 能交一个只装一件事的合并请求——一份文件，或同属一次作业的一组文件——并附上别人能重跑的路径清单。

> **Why one task rather than one file**: the test is not the count, it is whether the change can be sent back on its own. A merge request that carries two unrelated pieces of work — a self-check sheet and another set of exercises, say — cannot be rejected without also stopping the part that was right, and a reviewer cannot quote half of it. Five problems from one set, by contrast, are accepted or returned together by definition, so they are one task.
>
> **为什么是「一件事」，不是「一份文件」**：判据不是数量，是**能不能被单独退回**。一个合并请求如果同时装了两件互不相干的事——比如一份作业的自检表和另一组练习的题解——退回就等于把做对的那部分也一起停在门口，review 的人也没法只引用其中一半。反过来，五道题同属一组练习，本来就该一起收、一起退，那就是一件事。

> **Keep one sentence**: submitting is not the same as proving what you submitted.
>
> **记住一句**：交上去了，和能证明自己交对了，是两件事。
>
> 这一关过了，下一讲才轮到字节、十六进制和格式规范。

> **Before you hand in.** Two conventions live side by side from here on. This course writes the commit message as `submit(folder): what you did`, so every hand-in can be found by the folder it lives in. Real projects write it the other way: a short lowercase type, a colon, a short description — `docs: add submission check note` — and the type is one of the six from §2. The two rules that survive in both: **one merge request carries one task**, and **the merge request description says which rule made you exclude what**. Both templates below keep one `docs:` line as a sample of the community convention; it is not the format for this hand-in. Know both — one hands work in here, the other is how you will talk to people in a real repository.
>
> **交之前，先说清两条并存的写法。** 本课程的提交信息写成 `submit(提交的文件夹): 做了什么事情`，这样每份作业都能按文件夹找到人。真实项目里是另一套：一个英文小写的类型、冒号、一句简短说明——`docs: add submission check note`——类型就是 §2 那六类里挑一个。两种写法共享同两条规矩：**一个合并请求只装一件事**，**合并请求描述里写清你按哪条规矩排除了什么**。下面两份表单各留了一条 `docs:` 样例，那是社区写法，**不是这次要交的格式**。两种都要认得：一种在课堂里交作业，一种在真实仓库里跟人协作。

> **Hand-in checklist — English template / 英文模板**
> Copy the whole block into the hand-in file. Each answer blank is a bare underline, with no square brackets: write over it and leave none behind, so the file stays easy to read when you come back to it.

```text
=== WHAT TO HAND IN ===========================================

1. The only path allowed in this merge request
    submits/<handle>/P0/CLEAN.md

2. Content of the hand-in file
    Copy everything between the two dashed lines into the file.
    The underlines are blanks; no square brackets go into the file.
    Answer in English only, one line per blank. No Chinese, no brackets.
    Commit format here: submit(folder): what you did — one line, English.
    The docs: line below shows the real-community convention; both are kept.
    Write your own in the course format.
------------------------------------------------------------
# Submission Check

- File I changed:
  ____

- What I left out:
  ____

- Which rule made me exclude it:
  ____

- .gitignore lines I actually saw (copy them, do not guess):
  ____

- Commit message format for this course:
  submit(folder): what you did

- Community convention, kept as a sample (not the format for this hand-in):
  docs: add submission check note

- Commit message I used (write in the course format, do not copy the sample):
  ____

- Unexpected entries in git status (none, or list them):
  ____

- Output of git diff --name-only upstream/main...HEAD (verbatim):
  ____

- One sentence for the merge request description:
  ____
------------------------------------------------------------

3. Also paste into the merge request description
    - the diff output above, verbatim
    - the one sentence above

4. NOT in this PR
    .gitignore        <- already committed in the last merge; only checked now
    .idea/  .vscode/  caches, generated files, editor folders
    anything outside submits/<handle>/
============================================================
```

> **交什么，照着填 — 中文模板**
> 整段复制进本次要交的文件。每条横线是填空处，直接把答案写在横线上，**不要留中括号**，以后回头读更清楚。

```text
=== 本次要交的东西 ==========================================

1. 合并请求里只允许出现的路径
    submits/<handle>/P0/CLEAN.md
    （干净结果只有这一行）

2. 本次文件的内容
    把下面两条虚线之间整段复制进文件
    横线是填空处，文件里不要留下中括号
    每条横线只写一行，不要中英混填
    提交信息只写一行英文，类型和说明里都不要出现中文
    提交信息格式：submit(提交的文件夹): 做了什么事情
    表里那条 docs: 是真实社区写法的样例，两种都留着
    本次按课程格式写自己的那一条
------------------------------------------------------------
# 提交自检

- 我改的文件：
  ____

- 我排除了什么：
  ____

- 排除依据（哪条规矩）：
  ____

- .gitignore 里实际看到的行（照抄，不要凭想象填）：
  ____

- 本课程的提交信息格式：
  submit(提交的文件夹): 做了什么事情

- 真实社区里的写法，留作样例（不是这次要交的格式）：
  docs: add submission check note

- 本次提交信息（按课程格式写自己的，不要照抄样例）：
  ____

- git status 里不是我写的条目（无，或写具体名字）：
  ____

- git diff --name-only upstream/main...HEAD 的输出（原样）：
  ____

- 我按哪条规矩排除了什么（贴进合并请求描述）：
  ____
------------------------------------------------------------

3. 合并请求描述里另外要贴
    · 上面 diff 那一项的输出，原样
    · 上面「我按哪条规矩排除了什么」那一句话

4. 这次明确不交
    .gitignore        ← 上一次合并已进仓库，这次只核对
    .idea/  .vscode/  缓存、生成物、编辑器目录
    submits/<handle>/ 以外的任何文件
============================================================
```
