# 课程结构

[English](COURSE.md) · 简体中文

> 五个阶段的完整规划：现在有什么、每个阶段产出什么、支线放在哪。讲义本身在 `P0/` … `P4/`。

```text
save-kitten/
├── P0/   savefmt — 存档格式规范 + C11 参考实现（进行中）
│   ├── 1-git-basics.md                      git 到底存了什么，不交作业
│   ├── 2-community-workflow.md              fork → 分支 → 提交 → PR
│   │                                        → submits/<handle>/P0/first-contribution.md
│   ├── 3-clean-submission.md                什么样的改动可以被 review
│   │                                        → submits/<handle>/P0/CLEAN.md
│   ├── 3-x1-computing-systems.md            计算机怎么走到今天：逻辑门、Unix、各系统家族（不交作业）
│   ├── 3-x2-circuits-to-devices.md          从一颗管子到一个可寻址的设备（不交作业）
│   ├── 3-x3-shell-and-path.md               窗口、壳、PATH，以及你自己的一个命令
│   │                                        → submits/<handle>/P0/SHELL.md
│   ├── 3-x4-linux-and-toolchain.md          内核 vs 发行版、POSIX、权限、包管理（WSL 可选）
│   │                                        → submits/<handle>/P0/LINUX.md
│   ├── 3-x5-c-and-assembly.md               一条 C 语句变成了什么（不交作业）
│   ├── 4-byteorder-storage.md               一份存档规范的六句话
│   │                                        → submits/<handle>/P0/SPEC.md
│   ├── 5-memory-pointers-ub.md              内存、指针、未定义行为
│   │                                        → submits/<handle>/P0/C11.md
│   ├── 6-conformance-vectors-and-fuzzing.md 一致性向量、fuzzing、ASan
│   │                                        → submits/<handle>/P0/CONFORMANCE.md
│   └── 7                                    发布：写清「为什么」的 README、v0.1.0（尚未发布）
│
├── P1/   save-rs — 引擎的存档子系统（Rust，未开始）
├── P2/   engine-pack — 契约层与打包服务（Go，未开始）
├── P3/   story-studio — 剧本 / 存档编辑器（TypeScript，未开始）
├── P4/   engine-sdk — 接入模板、护栏、规约手册（未开始）
│
├── Algo/   支线：算法题，写一组发一组
└── Blog    支线：AtomGit Pages 上的个人站，有东西可写才发
```

每个阶段最后都独立成一个公开仓库，再挂回已有引擎。本仓库从不交付引擎，交付的是人和产物。

## 支线是怎么走的

支线不按章节排。它们各有自己的发布节奏，某一组晚几天发出来，也不影响任何一讲。

> **算法** — 每周一组，写完就发，主线的讲义照常往前走，题目不跟着讲义停下来等。语言跟着阶段换：P0 用 C，P1 用 Rust 重写，P2 用 Go。现在有 Set 1、Set 2，Set 3、Set 4 还没写。题目放在 `Algo/`，作业交到 `submits/<handle>/algo/`。一组题里的规矩不变：动手前先写三行（思路、复杂度、边界），能脱稿讲清楚才算做完。
>
> **博客** — 同样按自己的节奏：手上有交付物、值得写的时候再开站，不因为某个阶段开始了就硬写。不计分，也不阻塞讲义。

## 怎么读这张图

- 只有 P0 有讲义，另外四个阶段目前是承诺，不是内容。
- 支线永远不阻塞阶段。某一组题和任务包撞车时，任务包优先。
- P0 在第 7 讲结束，那时 `savefmt/` 是一个陌生人能读懂、能编译、能跑通一致性向量的公开仓库。
