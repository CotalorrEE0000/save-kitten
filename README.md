# save-kitten

[![stage: P0 in progress](https://img.shields.io/badge/stage-P0%20in%20progress-yellow)](#roadmap)
[![engine: Rust](https://img.shields.io/badge/engine-Rust-orange)](#t-shaped-skill-map)
[![lessons: P0-P4](https://img.shields.io/badge/lessons-P0--P4-blue)](#roadmap)
[![PRs: welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)
[![license: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

English · [简体中文](README.zh.md) · Contributing

**A game-engine engineering course you actually submit homework to.** Lectures live in `P0/` … `P4/`; coursework goes in `submits/<handle>/`.
The loop: `read → build → open a PR → get reviewed → turn the feedback into a principle`.

---

> **This repository is not a product.** The goal is people you can collaborate with, not repo counts or downloads: the five stages are training vehicles that each become a separate repo and plug back into an existing engine as subsystems you progressively take over. This repo holds only the course, the coursework, and the review trail.

## Quick start

```bash
git clone <your-fork>
git remote add upstream <this-repo>
git fetch upstream && git merge upstream/main   # before every session
```

1. Fork, clone, and configure `upstream`.
2. Change only `submits/<your handle>/`; lecture directories are read-only.
3. Before submitting, run `git diff --name-only upstream/main...HEAD` and paste the output **verbatim** into the PR description.

---

## Five things you should be able to do

| Ability | Evidence |
|:---|:---|
| Turn constraints into machine rules | "must / must not" is a decidable, testable, auditable policy — not good intentions in a prompt |
| Explain it without AI | Walk through any finished subsystem from first principles, and name one judgement you got wrong |
| Review others | Give a senior engineer substantive feedback and abstract it into a "never again" principle |
| Ship the whole chain | Build a playable demo from zero and say who checks each invariant |
| Reverse review | Move from being evaluated to co-authoring the evaluation criteria |

---

## T-shaped skill map

**Crossbar = breadth** (cross-language contracts and delivery), **stem = depth** (down into the Rust engine core); the `core` junction is the existing engine.
These are not five syntax courses: each language carries exactly one "who checks the invariant". Progress is measured by where you are on the map, not by how many languages you have touched.

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

| Language / tool | Stage | What it carries | Depth |
|:---|:---:|:---|:---:|
| C / C++ | P0 | Machine model, byte order, UB; spec before implementation | deep |
| Rust | end of P0–P1 | Ownership / typestate push invariants into the compiler; engine mainline | deep (stem) |
| Go | P2 | CSP concurrency, packaging service, landing end of cross-language contracts | deep |
| TypeScript | P3 | discriminated union / reducer, UI for non-developers | deep |
| schema (protobuf / CUE) + Rego | P2 / P4 | Declarative specs and decidable policy: read and write, not "master" | read & write |
| Elm / OCaml / Dafny / Datalog / Lean / Verus | — | Horizon index: named only, no stage, no acceptance | not taught |

---

## Roadmap

Status: `✓` done ｜ `○` in progress ｜ `—` not started. A task pack is about half a day; `time / due` is in relative months, never scheduled by week.

| Stage | Project | What | Real consumer | Time / due | Status |
|:---:|:---|:---|:---|:---:|:---:|
| P0 | `savefmt` | Save-format spec + C11 reference implementation | Engine read/write side, future you | month 1 | `○` |
| P1 | `save-rs` | Rust implementation of the engine's save subsystem (no generality chase) | The engine itself (a real dependency) | months 2–3 | `—` |
| P2 | `engine-pack` | Contract layer and toolchain services (Go) | Engine build chain, CI | months 3.5–5 | `—` |
| P3 | `story-studio` | Script / save editor for the engine (Web) | People making content with the engine | months 5–6.5 | `—` |
| P4 | `engine-sdk` | Integration template + agent guardrails + spec handbook | The next person taking over the engine | months 6.5–8 | `—` |

Every task pack includes one fixed exercise: **read existing engine code → write down assumptions → ask questions**. The point is reading other people's code and asking about what you don't understand, not doing a single reverse review only in P4.

> Before publishing, prefix all five names (e.g. `celestforge-*`): `story-studio` and `engine-sdk` already name active GitHub projects, and the exact npm name `engine-sdk` is taken by a placeholder package.

---

### Glossary

| Term | One-line explanation |
|:---|:---|
| PR / merge request | Submit your changes to the main repo and wait for review before merge |
| upstream | The course's main repository; sync from it before you start |
| UB (undefined behavior) | The standard defines no result; code may "improvise" |
| fuzz | Coverage-guided input mutation that forces boundary crashes |
| ASan | clang's memory error detector; uninitialized reads belong to MSan |
| conformance vector | A fixed set of "input → expected byte stream" answers every implementation is graded against |
| Property testing (Proptest) | Generate thousands of inputs to verify a rule instead of hand-writing cases |
| ADR | A team decision record capturing why a choice was made at the time |
| Rego / guardrails | Constrain AI or tools with policy code, not verbal promises |
| semver | major.minor.patch; `0.y.z` is initial development, any interface may change |
| breaking change | Invalidates existing user files / interfaces and requires a migration note |

---

## Contributors

Full list in [CONTRIBUTORS.md](CONTRIBUTORS.md).
