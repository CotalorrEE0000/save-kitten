## How to Submit Your First Contribution

> This folder is **submission-only**. You do not edit files outside of it. Your task is to create your own subfolder here, then create chapter folders inside it, and finally place your submission file (for example, `first-contribution.md`) inside the appropriate chapter.
>
> ```text
> submits/
> ├── alice/
> │   ├── P0/
> │   │   └── first-contribution.md
> │   └── P1/
> │       └── ...
> ├── bob/
> │   └── P0/
> │       └── first-contribution.md
> └── README.md          (this file)
> ```
>
> Steps:
> 1. Fork this repository and clone your fork.
> 2. Inside `submits/`, create a folder named after yourself (lowercase, no spaces).
> 3. Inside your folder, create a chapter folder such as `P0`.
> 4. Add your submission file, e.g. `first-contribution.md`, inside `P0/`.
> 5. Commit, push, and open a PR from your fork into the original repository.
>
> Do not modify anyone else's folder. Do not submit directly to `main` on the original repo.

> 这个文件夹是**提交专用**的。你不需要改动它之外的任何文件。你需要做的是在这里创建以自己名字命名的子文件夹，然后在里面创建对应的章节文件夹，最后把你的提交文件（例如 `first-contribution.md`）放进相应的章节目录。
>
> ```text
> submits/
> ├── alice/
> │   ├── P0/
> │   │   └── first-contribution.md
> │   └── P1/
> │       └── ...
> ├── bob/
> │   └── P0/
> │       └── first-contribution.md
> └── README.md          (本文件)
> ```
>
> 操作步骤：
> 1. Fork 本仓库并克隆你的 fork。
> 2. 在 `submits/` 下，创建一个以你名字命名的文件夹（小写、不含空格）。
> 3. 在你的文件夹内，创建一个章节文件夹，例如 `P0`。
> 4. 在 `P0/` 里放入你的提交文件，例如 `first-contribution.md`。
> 5. 提交、推送，并从你的 fork 向原仓库发起 PR。
>
> 不要修改其他人的文件夹。不要直接向原仓库的 `main` 分支提交。




## Authentication: Use a Personal Access Token (PAT)

> Git over HTTPS no longer accepts your account **password** on AtomGit, Gitee, or GitHub. If a command fails with a message such as *"password authentication is disabled, use a Personal Access Token (PAT)"*, this is not a bug — those platforms have removed password login for Git, and you must use a **token** in place of the password. A token is a replaceable, revocable credential with limited scope, so it is safer than a real password.
>
> Create a token on AtomGit (the path is almost the same on Gitee and GitHub):
> 1. Sign in to **atomgit.com** → click your **avatar** (top-right) → **Settings**.
> 2. Open **Private Tokens** (sometimes under *Security → Access Tokens).
> 3. **Create** a new token, tick the **`projects` (read/write repositories)** permission, then **copy it immediately** — the full token is shown only once.
>
> When Git asks for a password during `clone` or `push`, **paste the token into the password field**; your username stays the same. The token is used only for authentication and never appears inside your commits.
>
> ```bash
> # you will be prompted for credentials on the first HTTPS push
> Username: your-username
> Password: <paste your Personal Access Token here>
> ```
>
> To avoid pasting the token on every push, let Git remember it:
>
> ```bash
> # cache in memory for a while (safer)
> git config --global credential.helper "cache --timeout=3600"
>
> # OR store on disk in plain text (convenient, only on your own machine)
> git config --global credential.helper store
> ```

> 通过 HTTPS 使用 Git 时，AtomGit、Gitee、GitHub 都已经**不再接受账号密码**。如果命令报错「密码认证已被禁用，需改用个人访问令牌（Personal Access Token，简称 PAT）」，这不是故障——这些平台已下线 Git 的密码登录，你必须用 **Token** 替代密码。令牌是一个可以随时吊销、权限可控的凭证，比真实密码更安全。
>
> 在 AtomGit 上生成令牌（Gitee、GitHub 路径基本相同）：
> 1. 登录 **atomgit.com** → 点击右上角**头像** → **设置 / Settings**。
> 2. 找到 **私人令牌 / Access Tokens**（或在「安全设置 → 访问令牌」下）。
> 3. **新建**令牌，勾选 **`projects`（读写仓库）** 权限，然后**立即复制**——完整令牌只显示这一次。
>
> 当 Git 在 `clone` 或 `push` 时要求输入密码，把**令牌粘贴到密码那一栏**即可，用户名保持不变。令牌只用于身份认证，绝不会出现在你的提交内容里。
>
> ```bash
> # 第一次 HTTPS 推送时会提示输入凭据
> Username: your-username
> Password: <在这里粘贴你的 Personal Access Token>
> ```
>
> 如果不想每次推送都粘贴令牌，可以让 Git 记住它：
>
> ```bash
> # 只在内存里缓存一段时间（更安全）
> git config --global credential.helper "cache --timeout=3600"
>
> # 或者明文存到磁盘上（方便，仅建议在个人电脑上用）
> git config --global credential.helper store
> ```




## Troubleshooting: When `.gitignore` Does Not Work

> **What happened.** In an earlier submission, an editor folder (`.idea/`) ended up inside a merge request even though `.gitignore` already had a line for it. The file looked fine on your machine, but the repository web page rendered it as garbled text. The root `.gitignore` has since been rewritten as clean plain text, with the hidden bytes stripped out, so there is nothing for you to repair. What matters is **how these files are edited**: do not open plain-text or config files in an IDE. Use **Notepad**, or append one line from Git Bash / WSL:
>
> ```bash
> echo ".idea/" >> .gitignore
> ```
>
> `>>` appends a single line, and the shell writes plain bytes — no BOM, no hidden characters. An IDE is exactly what caused the problem above: it may silently change the encoding, the line endings, or add a BOM. The line above shows the correct way to write such a rule; it is not a file to add to this merge request — your PR always contains only your own submission file.
>
> **Why a rule that looks correct can still fail.** Git matches ignore rules exactly. A text file saved as **UTF-8 with a BOM** carries an invisible `\ufeff` at the very beginning; left-over Windows CRLF line endings or other invisible characters do the same. Git then reads the rule as `[hidden bytes].idea/` instead of `.idea/`, so it matches nothing. Those same bytes are why the web page shows gibberish. There is a second cause with exactly the same symptom, already stated in Lesson 2 §4: **`.gitignore` only affects files that are not yet tracked**. If a folder was committed once, adding a line will not remove it — it has to be untracked first. `.gitignore` is also case-sensitive. In all of these cases the symptom is identical: *the line is there, but the folder still shows up*.
>
> **What you should do.** Before every commit, open **Changes** in GitHub Desktop (Lesson 2 §5) or run the command below, and tick only your own file:
>
> ```bash
> git status
> ```
>
> Write and edit plain-text files with **Notepad or `echo >>`**, never with an IDE, and **never copy configuration text out of a web page** — the invisible characters travel with the paste. Notepad and the terminal do not create `.idea/` or `.vscode/`; an IDE does, which is why switching from VS Code to IntelliJ IDEA brought the folder back every time — deleting it once is not a fix. If something you did not write still appears in `Changes`, **do not commit it** — copy that one line from `git status` and include it when you ask for help.
>
> ```text
> === BEFORE YOU OPEN A PR — three lines to tick =================
>
> [ ] Changes / git status shows ONLY my own submission file
> [ ] No .idea/  .vscode/  caches  *.swp  or any folder I did not write
> [ ] I wrote plain-text files with Notepad or echo >> (never an IDE), and did not paste from a web page
>
> If any line fails: do not commit, include the git status line when
> you ask for help.
> ================================================================
> ```

> **出了什么事。** 之前有一次提交，`.gitignore` 里明明写了 `.idea/`，结果编辑器文件夹还是被交进了合并请求；文件在自己电脑上看着正常，仓库网页上却显示成乱码。根目录的 `.gitignore` 已用纯文本重新覆写过一遍，隐藏字符已剥掉，不需要你再修。真正要改的是**编辑方式**：**纯文本文件和配置文件不要用 IDE 打开编辑。用记事本，或者在 Git Bash / WSL 里用 `echo >>` 追加一行：**
>
> ```bash
> echo ".idea/" >> .gitignore
> ```
>
> `>>` 是追加一行，终端写出的是纯字节，不带 BOM、不带隐藏字符；IDE 恰恰是上面那个问题的来源——它可能悄悄改掉编码、换行符，或加上 BOM。上面那行示范的是正确写法，不是让你把根目录文件交进这次合并请求——PR 里始终只放你自己那一个提交文件。
>
> **为什么一行看着对的规则会失效。** Git 匹配忽略规则是逐字严格比对的。文件若存成了**带 BOM 的 UTF-8**，开头会多一个看不见的 `\ufeff`；残留的 Windows CRLF 换行符或其他不可见字符也一样。于是 Git 读到的规则变成 `[隐藏字节].idea/`，而不是 `.idea/`，自然谁都匹配不上；网页显示乱码，也是这批字节造成的。还有一个**症状完全相同**的原因，第 2 讲第 4 节已经写过：**`.gitignore` 只对尚未被跟踪的文件生效**。某个文件夹一旦被提交过，光加一行是删不掉它的，得先取消跟踪；另外 `.gitignore` 区分大小写。这几种情况的共同表现都是同一句话：**「那行在，可文件夹还在」**。
>
> **你该怎么做。** 每次提交前，用 GitHub Desktop 的 **Changes** 页（第 2 讲第 5 节）或下面这条命令看一眼，只勾自己那个文件：
>
> ```bash
> git status
> ```
>
> 纯文本文件一律用**记事本或 `echo >>`** 写和改，**不要用 IDE**；也**不要从网页上复制配置内容再粘贴进本地文件**——看不见的字符会跟着一起过来。记事本和终端不会生成 `.idea/`、`.vscode/`，IDE 才会；所以从 VS Code 换成 IntelliJ IDEA 时那个文件夹每次都回来，删一次没有用。如果 `Changes` 里还是冒出你没写过的东西，**不要提交**，把 `git status` 里那一行原样附在提问里。
>
> ```text
> === 每次发 PR 前 —— 勾这三条 ===================================
>
> [ ] Changes / git status 里只有我自己的那一个提交文件
> [ ] 没有 .idea/  .vscode/  缓存  *.swp  或任何我没写过的目录
> [ ] 我的纯文本文件是用记事本或 echo >> 写的，没用 IDE，也没从网页复制粘贴
>
> 任何一条没过：不要提交，把 git status 那一行原样附在提问里。
> ================================================================
> ```
