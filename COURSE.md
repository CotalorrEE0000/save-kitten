# Course map

English · [简体中文](COURSE.zh.md)

> The full plan for all five stages: what exists today, what each stage produces, and where the side tracks live. The lessons themselves are in `P0/` … `P4/`.

```text
save-kitten/
├── P0/   savefmt — save-format spec + C11 reference implementation (in progress)
│   ├── 1-git-basics.md                      what git actually stores; no hand-in
│   ├── 2-community-workflow.md              fork → branch → commit → PR
│   │                                        → submits/<handle>/P0/first-contribution.md
│   ├── 3-clean-submission.md                what a reviewable change looks like
│   │                                        → submits/<handle>/P0/CLEAN.md
│   ├── 4-byteorder-storage.md               the six sentences of a save spec
│   │                                        → submits/<handle>/P0/SPEC.md
│   ├── 5-memory-pointers-ub.md              memory, pointers, undefined behaviour
│   │                                        → submits/<handle>/P0/C11.md
│   ├── 6-conformance-vectors-and-fuzzing.md conformance vectors, fuzzing, ASan
│   │                                        → submits/<handle>/P0/CONFORMANCE.md
│   └── 7                                    release: a README that says why, v0.1.0 (not written)
│
├── P1/   save-rs — the engine's save subsystem in Rust (not started)
├── P2/   engine-pack — contract layer and packaging services, Go (not started)
├── P3/   story-studio — script and save editor, TypeScript (not started)
├── P4/   engine-sdk — template, guardrails, spec handbook (not started)
│
├── Algo/   side track: one problem set a week, published as it is written
└── Blog    side track: a personal site on AtomGit Pages, published when there is something to write
```

Each stage ends as its own public repository and plugs back into an existing engine. This repository never ships the engine; it ships the people and the artifacts.

## How the side tracks work

Side tracks are not tied to a chapter. They are published on their own schedule, and a set that lands late costs nothing.

> **Algo** — one set a week, written and published as it goes; you solve a set and hand it in while the main line keeps moving. The language follows the stage: C in P0, rewritten in Rust in P1, in Go in P2. Sets 1 and 2 are out; 3 and 4 are not written yet. Files live in `Algo/`, hand-ins in `submits/<handle>/algo/`. The rule inside a set is fixed: three lines before any code (approach, complexity, edge cases), and you explain the solution out loud before calling it done.
>
> **Blog** — also on its own schedule: start when you have shipped something worth writing about, not because a stage began. It is not graded and never blocks a lesson.

## How to read this map

- P0 is the only stage with lessons; the other four exist as commitments, not content.
- A side track never blocks a stage. If a set and a task pack collide, the task pack wins.
- P0 ends at lesson 7, where `savefmt/` becomes a public repository a stranger can read, build, and run the vectors against.
