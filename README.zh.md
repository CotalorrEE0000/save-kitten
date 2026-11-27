# save-kitten

[![stage: P0 in progress](https://img.shields.io/badge/stage-P0%20in%20progress-yellow)](#路线图)
[![engine: Rust](https://img.shields.io/badge/engine-Rust-orange)](#t-型技能地图)
[![lessons: P0-P4](https://img.shields.io/badge/lessons-P0--P4-blue)](#路线图)
[![PRs: welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTORS.md)
[![license: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
![star](https://atomgit.com/klions/save-kitten/star/badge.svg)

简体中文 · [English](README.md) · [课程结构](COURSE.zh.md) · 贡献指南

**一门可以交作业的游戏引擎工程课** — 讲义在 `P0/` … `P4/`，五个阶段的详细课程规划见[课程结构](COURSE.zh.md)，作业交在 `submits/<handle>/`。
闭环：`读讲义 → 动手做 → 发 PR → 被 review → 把意见抽象成原则`。

---

> **这个仓库不是产品。** 目标是能一起协作的人，不是仓库数量或下载量：五个阶段是训练载体，
> 各自独立成仓库后都挂回已有引擎，作为逐步接手的子系统；本仓库只承载课程、作业与互动记录。

## 快速开始

```bash
git clone <your-fork>
git remote add upstream https://atomgit.com/klions/save-kitten.git
git fetch upstream && git merge upstream/main   # 每次动手前
```

1. Fork 后克隆，配置 `upstream`。
2. 只改 `submits/<你的 handle>/`，讲义目录只读。
3. 提交前跑 `git diff --name-only upstream/main...HEAD`，把输出**原样**贴进 PR 描述。

---

## 学完应当能做到的 5 件事

| 能力 | 判据 |
|:---|:---|
| 把约束写成机器规则 | 「必须 / 不许」是可判定、可单测、可审计的策略，不是提示词里的自觉 |
| 不用 AI 也能讲明白 | 任一已完成的子系统，能脱稿讲清原理，并指出自己当初的一个错判 |
| 会 review 别人 | 能给资深者提实质意见，并抽象成「下次不再犯」的原则 |
| 交付完整链路 | 从零做到可玩 demo，说清每处规约分别由谁检查 |
| 反向 review | 从「被评价」走到「参与制定评价标准」 |

---

## T 型技能地图

**横杠 = 广度**（跨语言契约与交付），**竖杠 = 深度**（往 Rust 引擎内核里扎），交点 `core` 是已有引擎。
语言不是五份语法课，每门只承载一种「不变量由谁检查」；进度只看在坐标系里走到哪，不看学了几门语言。

```text
   BREADTH ────────── cross-language contracts & delivery ─────────►
   ┌───────────────┬───────────────┬───────────────┬───────────────┐
   │    C/C++      │  schema+Rego  │      Go       │  TypeScript   │
   │     P0        │    P2 / P4    │      P2       │      P3       │
   └───────────────┴───────────────┼───────────────┴───────────────┘
                                   │  core
                                   │
                                   │  DEPTH · toward the engine core
                                   ▼
                     ┌───────────────────────────┐
                     │      Rust · engine        │
                     │     P0 ─ P1 ─ core        │
                     └───────────────────────────┘
```

| 语言 / 工具 | 阶段 | 承担什么 | 程度 |
|:---|:---:|:---|:---:|
| C / C++ | P0 | 机器模型、字节序、UB；规范先于实现 | 深做 |
| Rust | P0 末–P1 | 所有权 / typestate 把不变量交给编译器；引擎主线 | 深做（竖轴） |
| Go | P2 | CSP 并发、打包服务、跨语言契约的落地端 | 深做 |
| TypeScript | P3 | discriminated union / reducer、面向非开发者的界面 | 深做 |
| schema（protobuf / CUE）+ Rego | P2 / P4 | 声明式规格与可判定策略，会读会写 | 会读会写 |
| Elm / OCaml / Dafny / Datalog / Lean / Verus | — | 视野索引，只列名、不设阶段、不验收 | 不教 |

---

## 路线图

状态：`✓` 已完成 ｜ `○` 进行中 ｜ `—` 未开始。任务包按「半天」计，`时间 / due` 是相对月，不排到周。

| 阶段 | 项目 | 做什么 | 真实消费者 | 时间 / due | 状态 |
|:---:|:---|:---|:---|:---:|:---:|
| P0 | `savefmt` | 存档格式规范 + C11 参考实现 | 引擎读写端、未来的自己 | 第 1 月 | `○` |
| P1 | `save-rs` | 引擎存档子系统的 Rust 实现（不追通用性） | 引擎本体（真实依赖） | 第 2–3 月 | `—` |
| P2 | `engine-pack` | 契约层与工具链服务（Go） | 引擎构建链、CI | 第 3.5–5 月 | `—` |
| P3 | `story-studio` | 引擎的剧本 / 存档编辑器（Web） | 用引擎做内容的人 | 第 5–6.5 月 | `—` |
| P4 | `engine-sdk` | 整合模板 + agent 护栏 + 规约手册 | 想接手引擎的下一个人 | 第 6.5–8 月 | `—` |

每个任务包固定包含一次「**读引擎现有代码 → 写下假设 → 提问**」——练的是读懂别人的代码、对不懂处发问，而不是只在 P4 做一次反向 review。

---

### 术语速查

| 术语 | 一句话解释 |
|:---|:---|
| PR / 合并请求（MR） | 同一件事的两个平台叫法：GitHub 叫 pull request（`#12`），AtomGit 叫合并请求（`!12`）。把改动提交给主仓库，等检查通过后合入 |
| upstream | 本课程的「上游」主仓库，动手前先同步 |
| UB（未定义行为） | 标准没规定结果，代码可能「随机发挥」 |
| fuzz | 覆盖率引导的变异输入测试，逼出边界崩溃 |
| ASan | clang 内存错误检测器；未初始化读取归 MSan |
| conformance 向量 | 「输入 → 期望字节流」的标准答案集，所有实现照同一套考 |
| 性质测试（Proptest） | 机器生成上千输入验证规则，不逐条手写用例 |
| ADR | 存档「当时为什么这么选」的决策记录 |
| Rego / 护栏 | 用策略代码而非口头承诺约束 AI 或工具 |
| semver | 主.次.补丁；`0.y.z` 处于初始开发，接口都可能变 |
| breaking change | 让老用户文件 / 接口失效，必须配迁移说明 |

---

## 贡献者

完整名单见 [CONTRIBUTORS.md](CONTRIBUTORS.md)。
