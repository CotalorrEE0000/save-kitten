# Git basics

## 1.  what is git?
    

> Git is a free and open source distributed version control system. It helps developers track changes to files, collaborate with others, and manage the full history of a project. Unlike simple file backups, Git records the state of a project at different points in time, so you can always go back, compare versions, or recover earlier work.
>
> Git was created by Linus Torvalds in 2005, originally to help manage the development of the Linux kernel. Before Git existed, many open source projects relied on centralized version control systems or proprietary tools. When the Linux kernel community lost free access to BitKeeper, Torvalds decided to build a new system that was fast, simple, fully distributed, and capable of handling very large projects with many parallel branches.
> 
> Traditional document workflows often rely on saving copies such as “report_v1.doc”, “report_v2.doc”, or sharing files through email and cloud drives. This works for small projects, but it quickly becomes messy when many people edit the same files. Git is different because it thinks of its data as a series of snapshots of a miniature filesystem rather than a list of file-based changes, keeps a clean history of every commit, and makes it easy to merge work from multiple people without losing context.
> 
> Git is distributed, which means every developer can have a complete copy of the repository on their own machine. This includes the full project history, all branches, and all commits. Because most operations run locally, developers can commit code, create branches, and review history even without an internet connection.
>
> The open source community uses Git because it is fast, reliable, and well suited to collaborative development. It allows teams to work in parallel through branches, review changes before merging, and roll back mistakes safely. Combined with platforms like GitHub and GitLab, Git has become the de facto standard for managing code in modern software projects.


> Git 是一个免费、开源的分布式版本控制系统。它帮助开发者追踪文件变化、与他人协作开发，并管理项目的完整历史。与简单的文件备份不同，Git 会记录项目在不同时间点的状态，因此你可以随时回退、比较版本，或恢复之前的工作内容。
>
> Git 由 Linus Torvalds 于 2005 年创建，最初是为了帮助管理 Linux 内核的开发。在 Git 出现之前，许多开源项目依赖集中式版本控制系统或专有工具。当 Linux 内核社区失去 BitKeeper 的免费使用权后，Torvalds 决定构建一个新的系统，要求它速度快、设计简单、完全分布式，并且能够高效管理拥有大量并行分支的大型项目。
>
> 传统文档工作流通常依赖保存多个副本，例如“报告_v1.doc”“报告_v2.doc”，或通过邮件、网盘分享文件。这种方式在小项目里还能工作，但当多人同时编辑同一批文件时，很快就会变得混乱。Git 的不同之处在于，它存的是一系列迷你文件系统的快照，而不是只追踪文件级的变更，保留每次提交的完整历史，并让多人协作合并变得更加清晰、可追溯。
>
> Git 是分布式的，这意味着每位开发者都可以在自己的机器上拥有仓库的完整副本。这个副本包含完整的项目历史、所有分支和所有提交记录。由于大多数操作都在本地运行，开发者即使没有网络连接，也可以提交代码、创建分支和查看历史记录。
>
> 开源社区选择 Git，是因为它快速、可靠，并且非常适合协作开发。它允许团队通过分支并行工作，在合并前审查变更，并能安全地回滚错误。配合 GitHub、GitLab 等平台，Git 已经成为现代软件项目中管理代码的事实标准。

## 2.  Remote Repositories and Basic Git Operations
    

> Remote repositories exist to make collaboration easier. They act as a shared copy of your project that multiple people can push to and pull from. Instead of sending files back and forth, developers can update a remote repository and let others fetch the latest changes.
> 
> Developers may use different code hosting services, such as GitHub, GitLab, or Gitee. Each service has its own account system, so you should configure your Git identity with the email linked to the account you actually use for pushing and reviewing code.
> 
> Git stores configuration in several places. The `--global` flag writes settings to your user-level config file, usually `~/.gitconfig`, and applies them to all repositories on your computer. Without `--global`, the setting is saved only for the current repository in `.git/config`.
> 
> Local repository settings have higher priority than global settings. This means a repository can override your default name or email when needed.
> 
> To set your default identity, run the following commands.
>
>```bash
>git config --global user.name "Your Name"
>git config --global user.email "your.email@example.com"
>```
>
>To check the current identity, run the following commands.
> 
>```bash
>git config user.name
>git config user.email
>```
>
> You can also store your name and email in a separate file, for example `git-identity.txt`, and read it when needed. This file is not used by Git automatically; it is just a convenient way to keep your account information in one place, especially if you manage multiple hosting accounts.
> 
>```bash
>cat git-identity.txt
>```
>
> To start a new local repository, use `git init`. This creates a hidden `.git` directory and begins tracking your project.
>
>```bash
>git init
>```
>
> To see which files have changed, run `git status`. It tells you what has been modified, what is staged, and what is not yet tracked.
> 
>```bash
>git status
>```
>
> To create a new branch, use `git branch <branch-name>`. To switch to an existing branch, use `git checkout <branch-name>`. Branches let you work on different ideas without changing the main code immediately.
> 
>```bash
>git branch <branch-name>
>git checkout <branch-name>
>```
>
> Before you can commit, you must stage your changes with `git add`. `git add <file>` stages one file, and `git add .` stages every change in the current directory. Staging builds a snapshot of exactly what you want to save.
>
> `git commit` records that snapshot into the project history. The `-m` flag lets you write the commit message inline:
>
>```bash
>git add <file>
>git add .
>git commit -m "docs: add first contribution"
>```
>
> If you pass `-m` twice, the first becomes the title and the second becomes the body:
>
>```bash
>git commit -m "fix(auth): clear local auth after token expires" -m "We now clear stored tokens before redirecting to login."
>```
>
> If you run `git commit` with no `-m`, Git opens your editor so you can write a longer message. The `-a` flag stages all *tracked* files automatically, but avoid it at first; explicit `git add` keeps you in control of what goes into each commit. To fix the most recent commit message or add a forgotten file, use `git commit --amend`.

> 远程仓库的存在是为了让协作更方便。它相当于项目的一份共享副本，多个开发者可以向它推送更新，也可以从中拉取最新内容。与其来回发送文件，开发者只需更新远程仓库，其他人就能获取最新代码。
>
> 开发者可能会使用不同的代码托管服务，例如 GitHub、GitLab 或 Gitee。每个服务都有自己的账号体系，因此你应该把 Git 身份配置为与你实际用于推送和审查代码的账号绑定的邮箱。
>
> Git 的配置会保存在不同位置。`--global` 会把设置写入用户级配置文件，通常是 `~/.gitconfig`，并对电脑上所有仓库生效。如果不加 `--global`，设置只会保存在当前仓库的 `.git/config` 中。
>
> 仓库级配置的优先级高于全局配置。也就是说，某个仓库可以在需要时覆盖你的默认用户名或邮箱。
 要设置默认身份，可以执行：
> 
>```bash
>git config --global user.name "Your Name"
>git config --global user.email "your.email@example.com"
>```
>
>要查看当前身份，可以执行：
> 
>```bash
>git config user.name
>git config user.email
>```
>
>你也可以把用户名和邮箱单独存进一个文件，例如 `git-identity.txt`，需要时再读取。这个文件不会被 Git 自动使用，它只是方便你把账号信息集中保存，尤其在你管理多个托管平台账号时比较有用。
>
>```bash
>cat git-identity.txt
>```
>
>要初始化一个新的本地仓库，可以执行 `git init`，这会在当前目录下创建一个隐藏的 `.git` 目录，并开始追踪项目。
>
>```bash
>git init
>```
>
>要查看哪些文件发生了变化，可以执行 `git status`，它会告诉你哪些文件被修改、哪些已暂存，以及哪些文件尚未被 Git 追踪。
>
>```bash
>git status
>```
>
> 要创建一个新分支，可以执行 `git branch <branch-name>`；要切换到已有分支，可以执行 `git checkout <branch-name>`。分支让你可以在不影响主代码的情况下，尝试不同的开发思路。
>
>```bash
>git branch <branch-name>
>git checkout <branch-name>
>```
>
> 提交之前必须先用 `git add` 暂存改动。`git add <file>` 暂存单个文件，`git add .` 暂存当前目录下的全部改动。暂存就是在组装一份"你到底想保存哪些内容"的快照。
>
> `git commit` 会把这份快照记录进项目历史。`-m` 参数让你直接在命令行写提交信息：
>
>```bash
>git add <file>
>git add .
>git commit -m "docs: add first contribution"
>```
>
> 如果写两次 `-m`，第一个会作为标题，第二个作为正文：
>
>```bash
>git commit -m "fix(auth): 修复 token 过期后的登录问题" -m "现在会在跳转登录页前清除已存储的 token。"
>```
>
> 如果运行 `git commit` 时不带 `-m`，Git 会打开编辑器让你写更长的信息。`-a` 参数会自动暂存所有*已被跟踪*的文件，但初学阶段先不要用它；显式地 `git add` 才能让你精确掌控每次提交包含什么。如果想修正最近一次提交的信息，或补上一个遗漏的文件，使用 `git commit --amend`。

## 3. Cloning Repositories and Command Line Basics

> Before interacting with remote repositories, you need to be comfortable with the command line. On Windows, you can use the traditional Command Prompt (cmd) or PowerShell (pwsh). The most modern and recommended way is to use Windows Terminal (wt), which allows you to open new tabs or split panes to manage multiple command line sessions at once. On macOS or Linux, you simply open the built-in Terminal application.
>
> The most essential commands for navigating the file system are `cd` (change directory) and `mkdir` (make directory). You use `mkdir` to create new folders and `cd` to move into them. Understanding relative paths is critical: `.` represents the current directory you are in, while `..` represents the parent directory (one level up). For example, running `cd ..` will take you back to the previous folder.
>
> ```bash
> mkdir my-repos
> cd my-repos
> cd ..
> cd .
> ```
>
> To get a local copy of a remote repository, you use the `git clone` command followed by the repository URL. It is a best practice to create a dedicated folder (like `my-repos`) specifically for cloning projects. Inside this folder, you can organize your account credential files (such as `.txt` files) based on the hosting service you use. A clean directory structure looks like this:
>
> ```text
> my-repos/
> ├── github-account.txt
> ├── gitlab-account.txt
> ├── project-alpha/      (cloned from GitHub)
> └── project-beta/       (cloned from GitLab)
> ```

> **WARNING: Read-Only Phase**
> After cloning a repository, you must first `cd` into the newly created project folder before running any Git commands. During this initial learning stage, treat the repository as strictly read-only. Do not modify any files or create commits on the `main` branch. Your only allowed synchronization command at this stage is `git fetch`, which safely downloads the latest remote changes without altering your local files. The next chapter will cover the proper workflow for making commits and collaborating with the community.



> 在与远程仓库交互之前，你需要熟悉命令行操作。在 Windows 上，你可以使用传统的命令提示符 (cmd) 或 PowerShell (pwsh)。最现代且推荐的方式是使用 Windows Terminal (wt)，它允许你打开新标签页或拆分窗格，以便同时管理多个命令行会话。在 macOS 或 Linux 上，你只需打开系统自带的终端应用程序即可。
>
> 文件系统导航中最核心的命令是 `cd`（切换目录）和 `mkdir`（创建目录）。你使用 `mkdir` 来创建新文件夹，使用 `cd` 进入它们。理解相对路径至关重要：`.` 代表你当前所在的目录，而 `..` 代表父目录（向上一级）。例如，运行 `cd ..` 就会让你返回到上一层文件夹。
>
> ```bash
> mkdir my-repos
> cd my-repos
> cd ..
> cd .
> ```
>
> 要获取远程仓库的本地副本，你需要使用 `git clone` 命令，后面跟上仓库的 URL。最佳实践是创建一个专门的文件夹（例如 `my-repos`）来存放克隆的项目。在这个文件夹内，你可以根据所使用的托管服务来分类存放你的账号凭证文件（如 `.txt` 文件）。一个整洁的目录结构如下所示：
>
> ```text
> my-repos/
> ├── github-account.txt
> ├── gitlab-account.txt
> ├── project-alpha/      (cloned from GitHub)
> └── project-beta/       (cloned from GitLab)
> ```

> **警告：只读阶段**
> 克隆仓库后，必须先 `cd` 进入新创建的项目文件夹，然后才能运行任何 Git 命令。在这个初始学习阶段，请将仓库视为严格的只读状态。不要修改任何文件，也不要在 `main` 分支上创建任何提交。在这一阶段，你唯一被允许的同步命令是 `git fetch`，它可以安全地下载远程的最新更改，而不会改变你的本地文件。下一章将讲解如何正确地进行提交以及社区协作的工作流规范。
