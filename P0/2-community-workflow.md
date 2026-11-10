
# Git Guide — Collaborating with the Community

## 1. The Community Collaboration Workflow: Fork -> Branch -> Commit -> PR

> Contributing to someone else's project follows a standard path. First you **fork** the repository on GitHub, which copies the original repository into your own account. Then you **clone your fork** with `git clone <your-fork-url>`, so you are working on a copy you fully control. To keep your fork in sync with the original, you add it as a second remote called **upstream** using `git remote add upstream <original-url>`. From here on, all your work happens on a **new branch**, not on `main`.
>
> ```bash
> git clone <your-fork-url>
> cd <project-name>
> git remote add upstream <original-url>
> git checkout -b fix/login-error
> ```
>
> One branch should do exactly one thing. Before you start working, always sync first: run `git fetch upstream` and then `git merge upstream/main`, so your new branch begins from the latest upstream state. While developing, you commit in small steps instead of saving one giant batch at the end. Sync once more with the same two commands before opening a PR to reduce conflicts. When your work is ready, push the branch to your fork with `git push origin fix/login-error` and open a **Pull Request** from your fork's branch into the original repository's target branch.
>
> After the reviewer leaves comments, keep pushing new commits to the same branch to address them; do not force-push to a shared branch. Once the PR is merged, the temporary branch on both your local machine and your fork can be cleaned up.
>
> ```bash
> git fetch upstream
> git merge upstream/main
> git push origin fix/login-error
> ```

> 给别人项目做贡献遵循一条标准路径。首先在 GitHub 上 **fork** 仓库，把原仓库复制一份到你自己的账号下。然后 **克隆你的 fork**，使用 `git clone <你的fork地址>`，这样你操作的是一份完全由自己控制的副本。为了让 fork 与原仓库保持同步，你把原仓库作为第二个远程仓库加进来，命名为 **upstream**，使用 `git remote add upstream <原仓库地址>`。从这里开始，你的所有工作都在 **新分支** 上进行，而不是在 `main` 上。
>
> ```bash
> git clone <你的fork地址>
> cd <项目名>
> git remote add upstream <原仓库地址>
> git fetch upstream
> git merge upstream/main
> git checkout -b fix/login-error
> ```
>
> 一个分支只做一件事。动手开发之前必须先同步：运行 `git fetch upstream`，再运行 `git merge upstream/main`，让你的新分支从上游最新状态开始。开发过程中要小步提交，而不是最后攒成一大坨。发起 PR 之前再用同样这两条命令同步一次，以减少冲突。当工作完成后，用 `git push origin fix/login-error` 把分支推送到你的 fork，并从你 fork 的分支向原仓库的目标分支发起 **Pull Request**。
>
> 审查者留下评论后，继续在同一个分支上推送新的提交来回应意见；不要对共享分支执行强制推送。PR 合并之后，本地和你 fork 上的临时分支都可以清理掉。
>
> ```bash
> git fetch upstream
> git merge upstream/main
> git push origin fix/login-error
> ```

## 2. Writing Good Commits: Small, Atomic, Explainable

> The problem with "one big commit" is that it is hard to review, hard to roll back, and hard to locate bugs. A good commit does exactly one thing: fixing a bug, refactoring, adding a feature, or editing docs should each be its own commit. The project must still run after each commit, so never commit half-finished work.
>
> Write a short title and a body that explains the reason: the title tells others what was done, the body explains why. Use the Conventional Commits style so history stays machine-readable and consistent: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`.
>
> ```text
> fix(auth): clear local auth so login works after the token expires
>
> The token used to expire without clearing local storage, so a new login
> still carried the old token. We now clear all local auth data before
> redirecting to the login page.
>
> Closes #123
> ```
>
> If you already accumulated a pile of messy commits, you can tidy and squash them with `git rebase -i` before pushing to the remote.
>
> ```bash
> git rebase -i HEAD~5
> ```

> "每次提交一大坨"的问题在于：难以审查、难以回滚、难以定位 bug。一个好的提交只做一件事：修复 bug、重构、加功能、改文档，应该各自独立成一次提交。每次提交后项目仍要能运行，所以永远不要提交半成品。
>
> 标题要简短，正文说明原因：标题告诉别人"做了什么"，正文说明"为什么这么做"。使用 Conventional Commits 风格，让历史保持一致、便于机器读取：`feat: ...`、`fix: ...`、`docs: ...`、`refactor: ...`。
>
> ```text
> fix(auth): 修复 token 过期后无法重新登录的问题
>
> 之前 token 过期时没有清除本地存储，导致重新登录后仍携带旧 token。
> 现在在跳转登录页前先清除所有本地认证信息。
>
> Closes #123
> ```
>
> 如果你已经攒了一堆乱提交，可以在推送到远程之前用 `git rebase -i` 整理、squash。
>
> ```bash
> git rebase -i HEAD~5
> ```

## 3. How to Reply to Issues Properly

> The core principles of replying to an issue are: respectful, clear, reproducible, and focused on the problem rather than the person. If you are the one asking, you should provide: the project version, the operating system and runtime environment, the steps to reproduce, expected result versus actual result, a minimal reproduction or log, and what you have already tried.
>
> If you are the maintainer, you should: first confirm whether the issue can be reproduced; if it cannot, say clearly what information is missing; if it is confirmed as a bug, give a fix plan or a PR link; if it is not a bug, reference the documentation or design spec; when closing an issue, state the reason, for example "Close as cannot reproduce" or "Close as duplicate".
>
> In open source collaboration, clarity and respect matter far more than winning one argument.

> 回复 Issue 的核心原则是：尊重、清晰、可复现、对事不对人。如果你是提问者，应该提供：项目版本、操作系统和运行环境、复现步骤、预期结果 vs 实际结果、最小复现代码或日志，以及你已经尝试过的排查方法。
>
> 如果你是维护者，回复时应：先确认是否能复现；不能复现时说明缺少哪些信息；确认是 bug 时给出修复计划或 PR 链接；不是 bug 时引用文档或设计规范；关闭 issue 时说明理由，例如 Close as cannot reproduce 或 Close as duplicate。
>
> 在开源协作里，清晰和尊重比"赢一次对话"更重要。

## 4. Using .gitignore

> A `.gitignore` file tells Git which files should never be tracked. Common things to ignore are dependency directories (`node_modules/`, `vendor/`), build artifacts (`dist/`, `build/`, `out/`), environment config (`.env`, `*.local`), logs (`*.log`), system files (`.DS_Store`, `Thumbs.db`), IDE config (`.idea/`, `.vscode/`, depending on team convention), and any secrets such as passwords, tokens, or private keys.
>
> ```gitignore
> # ignore all .log files
> *.log
>
> # ignore the node_modules directory
> node_modules/
>
> # ignore .env only at the repository root
> /.env
>
> # ignore any cache folder in any directory
> **/cache/
>
> # exception: do NOT ignore important.log
> !important.log
> ```
>
> Three rules matter most: `.gitignore` only affects files that are not yet tracked; if a file was already committed, you must first stop tracking it with `git rm --cached <file>` and then add it to `.gitignore`; and `.gitignore` is case-sensitive. For cross-project rules such as `.DS_Store`, you can use a global ignore file.

> `.gitignore` 文件的作用是告诉 Git：哪些文件永远不要纳入版本控制。常见需要忽略的有：依赖目录（`node_modules/`、`vendor/`）、构建产物（`dist/`、`build/`、`out/`）、环境配置（`.env`、`*.local`）、日志（`*.log`）、系统文件（`.DS_Store`、`Thumbs.db`）、IDE 配置（`.idea/`、`.vscode/`，视团队约定），以及任何密钥，比如密码、token、私钥。
>
> ```gitignore
> # 忽略所有 .log 文件
> *.log
>
> # 忽略 node_modules 目录
> node_modules/
>
> # 只忽略仓库根目录下的 .env
> /.env
>
> # 忽略任意目录下的 cache 文件夹
> **/cache/
>
> # 例外：不忽略 important.log
> !important.log
> ```
>
> 最重要的三条规则：`.gitignore` 只对尚未被跟踪的文件生效；如果文件已经被提交过，必须先用 `git rm --cached <文件>` 停止跟踪，再写入 `.gitignore`；并且 `.gitignore` 区分大小写。对于 `.DS_Store` 这类跨项目通用规则，可以使用全局忽略文件。

## 5. Installing and Using GitHub Desktop

> GitHub Desktop is an official graphical Git client from GitHub, suited to people who do not want to type commands all the time. To install it, download from desktop.github.com, then after installing choose Sign in to GitHub, finish authorization in the browser, set your username and email, and manage repositories through Clone, Create, or Add.
>
> Common operations are: Clone to clone a repository from GitHub; Changes to view file changes; Commit to fill in a message and commit; Push origin to push to the remote; Pull origin to pull remote updates; Branch to create, switch, or merge branches; and Create Pull Request to open a PR directly from the client.
>
> Keep in mind that GitHub Desktop is fine for everyday work, but for advanced operations such as rebase, cherry-pick, patch commits, and complex conflict handling, the command line is still more flexible.

> GitHub Desktop 是 GitHub 官方提供的图形化 Git 客户端，适合不想频繁敲命令的人。安装步骤是：访问 desktop.github.com 下载；安装后选择 Sign in to GitHub；在浏览器中完成授权；设置用户名和邮箱；通过 Clone、Create 或 Add 管理仓库。
>
> 常用操作包括：Clone 从 GitHub 克隆仓库；Changes 查看文件改动；Commit 填写提交信息并提交；Push origin 推送到远程；Pull origin 拉取远程更新；Branch 创建、切换、合并分支；Create Pull Request 直接从客户端发起 PR。
>
> 需要注意的是：GitHub Desktop 适合日常操作，但 rebase、cherry-pick、patch 提交、复杂冲突处理等高级操作，命令行仍然更灵活。

## 6. Your First Contribution: The Practice Folder

> All the lessons in this course live in one repository. To let everyone practice without touching the lesson files, there is a dedicated folder for student submissions, in the same spirit as GitHub's own `first-contributions` project. Open that folder, read the practice notes inside, and complete your very first contribution by applying everything from this chapter. In this guide the folder is written as `*1xxxxx`; replace it with the real folder name used in your course repository.
>
>
> ```bash
> # 1. fork the course repository on GitHub, then clone your own fork
> git clone <your-fork-url>
> cd <course-repo>
>
> # 2. keep the original as upstream so you can stay in sync
> git remote add upstream <original-url>
>
> # 3. do all your work on a new branch, never on main
> git checkout -b my-first-contribution
>
> # 4. add your own file inside the practice folder, then commit
> cd <practice-folder>        # the folder referenced as *1xxxxx
> # create your-name.md here and write a short text inside it
> git add your-name.md
> git commit -m "docs: add first writing contribution by Your Name"
>
> # 5. push your branch and open a Pull Request from it
> git push origin my-first-contribution
> ```

> 本课程的所有讲义都放在同一个仓库里。为了让大家安全地练习而不去改动讲义本身，仓库中专门有一个存放学生提交的目录，思路和 GitHub 官方的 `first-contributions` 项目一样。请打开那个目录，阅读里面的实践说明，然后用本章学到的全部内容完成你的第一次贡献。本指南中该目录记作 `*1xxxxx`，请把它替换为你所在课程仓库里实际使用的目录名。
