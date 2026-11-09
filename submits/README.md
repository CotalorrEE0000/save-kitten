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
