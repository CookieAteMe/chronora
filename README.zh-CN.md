# Chronora

面向 AI 编程工具的持久上下文与连续性工作流。

> Coding agents need deterministic state, not probabilistic recall.

[English](README.md) · [Getting Started](docs/getting-started.md) · [Workflow](docs/workflow.md) · [Philosophy](docs/philosophy.md) · [Architecture](docs/architecture.md) · [Example](examples/basic-project/README.md)

Chronora 是一个面向长期 AI coding workflow 的 Claude-first continuity layer。

它把持久 project context 放在普通项目文件里，让 coding agents 能从显式状态继续工作，而不是每次都从聊天记录里重新拼接上下文。它的架构是 AI-tool agnostic 的；当前实现路径则首先面向 Claude Code。

## Why Chronora

聊天记录不等于项目状态。

在真实开发工作流里，长时间运行的 coding session 很容易发生 context drift：

- 架构决策会被反复重谈
- 未解决的阻塞会沉进 transcript 历史
- 做到一半的实现会被重新发现，而不是自然续接
- 当前真相和过去推理会混在一起
- 人类操作员会被迫成为唯一可靠的长期记忆层

Chronora 把连续性当作一个确定性的状态问题来处理：

- 用 **explicit state** 表达现在什么是真的
- 用 **append-only history** 记录发生了什么变化
- 用 **compact handoff structure** 指明下一次 session 该接什么
- 用 **workflow continuity** 抵抗 context window 带来的漂移

当工作跨越多天、多分支、以及多次 agent session 时，deterministic continuity 会比 probabilistic recall 更可靠。

## What Chronora Provides

Chronora v0.1 提供了一个刻意保持很小的 continuity layer：

- `current.md` 作为 canonical mutable project state
- `CLAUDE.local.md` 作为项目本地 agent instructions
- `.claude/sessions/` 作为 append-only state history
- `cclaude` 作为当前的 Claude Code entrypoint
- 模板与示例，帮助你稳定复现这套 workflow

当前实现有意保持为 file-driven、shell-based。它不依赖数据库、embeddings、vector memory，也不依赖隐藏式 orchestration service。

## Support Status

当前支持：

- Claude Code（完全支持）

计划中的集成：

- Codex CLI
- OpenCode
- Aider
- Cursor agents

这些 planned integrations 在当前版本里都还没有 shipped。Chronora 今天在实现上是 Claude-first，但 continuity model 本身被设计成可以在未来扩展到单一 coding agent 之外。

## Installation

Chronora 当前主要在 **macOS 和 Linux** 上验证，并要求已安装 [Claude Code CLI](https://claude.ai/code)。

```bash
git clone https://github.com/CookieAteMe/chronora.git
cd chronora
./install.sh
```

如果检测到的脚本安装目录还不在 `PATH` 中，`install.sh` 会尽量把正确的 export 行自动写入兼容的 shell profile，并告诉你更新了哪个文件。脚本安装路径会因 Python 发行版和平台不同而变化，所以不同机器上看到的目录可能不同。

安装脚本会：

- 通过 `python3 -m pip install --user .` 安装 Python `chronora` CLI
- 在可行时把 `cclaude` 安装到同一个用户级脚本目录
- 把默认模板安装到 `~/.local/share/chronora/templates`
- 确保安装后的 entrypoint 具有可执行权限
- 检查 Claude Code CLI 是否可用
- 在所选安装目录当前不在 `PATH` 中时进行提示或自动写入 profile

例如常见的 PATH 行可能是：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

但在某些系统上，安装器也可能检测到类似 macOS 的 `~/Library/Python/<version>/bin` 这类 Python 管理的用户脚本目录，并为当前机器写入对应的准确 export 行。

## Usage

### 1. 初始化项目

在任意项目根目录运行 `cclaude`：

```bash
cd ~/work/my-project
cclaude
```

首次运行时，Chronora 会创建：

```text
my-project/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   └── sessions/
└── CLAUDE.local.md -> .claude/CLAUDE.local.md
```

### 2. 计算 restore plan

Chronora v0.2 Core 引入了一个用于 restore planning 的 Python CLI 入口：

```bash
chronora restore
```

这个第一版 **不会** 启动或控制任何 AI agent。
它只会检查当前项目状态，并输出：

- 检测到的 Chronora 状态文件
- restore 加载顺序
- 建议读取的文件
- 可直接粘贴到 agent session 的推荐 Prompt
- 当核心状态缺失或退化时给出的 warnings

输出示例大致如下：

```text
Chronora Restore Plan
=====================
Project Root: /path/to/project
State Directory: /path/to/project/.claude

Detected State
--------------
- current: /path/to/project/.claude/current.md (Canonical live truth)
- archive: /path/to/project/.claude/sessions/2026-05-28_09-00-00-99999 (Latest archive evidence fallback)

Restore Order
-------------
1. /path/to/project/.claude/current.md — Canonical live truth
2. /path/to/project/.claude/sessions/2026-05-28_09-00-00-99999 — Latest archive evidence fallback
```

当前 `chronora restore` 主要面向现有的 Claude-first 状态布局：

```text
your-project/
└── .claude/
    ├── current.md
    ├── handoff.md        # optional
    ├── tasks.md          # optional
    ├── summaries/        # optional
    └── sessions/
```

restore planner 遵循当前文档中的连续性加载顺序：

1. `current.md`
2. `handoff.md`（如果存在）
3. `tasks.md`（如果存在）
4. 最高价值 summary（如果存在）
5. 最新 archive evidence（如有需要）

### 3. 启动 continuity-aware coding session

`cclaude` 会完成本地状态初始化、记录 before-state，然后在项目上下文中启动 Claude Code。

这仍然是当前唯一 fully supported 的 frontend path。

推荐的 session 循环是：

1. 运行 `cclaude`
2. 加载 `.claude/current.md`
3. 延续既有架构与约束条件
4. 当持久事实变化时更新 `current.md`
5. 退出并让 Chronora 归档本次 session

### 4. 把 `current.md` 当作 live project truth

一个健康的 `current.md` 应该保持紧凑、可执行、可续接。它记录的是下一次 session 必须立即当成真相的内容：

```md
# Current Project

## Project Status

Login flow MVP is working locally. Registration is partially implemented.

## Architecture

FastAPI backend with a single entry point in `src/main.py`.

## Active Problems

No rate limiting on `/login` yet.

## Important Decisions

Keep auth logic in one module until the API stabilizes.

## Next Steps

1. Add email validation to registration.
2. Add integration coverage for happy-path login.
```

### 5. 查看 session archive

每次运行都会在 `.claude/sessions/` 下创建一个 append-only archive。

一个典型的 archive 目录包含：

```text
.claude/sessions/2026-05-27_10-00-00-12345/
├── current.before.md
├── current.after.md
├── CLAUDE.local.before.md
├── CLAUDE.local.after.md
└── session.meta
```

这让你可以轻量追踪 project state 如何演化，而不必把聊天记录当成主状态系统。

### 6. 在下一次 session 里继续，而不是重新拼接上下文

第二天，或者下一次打开终端时，直接再运行：

```bash
cclaude
```

Chronora 会从显式状态继续，而不是依赖模型去“刚好记得”上一次会话里的正确架构背景。

## Project Structure

### 仓库结构

```text
chronora/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── install.sh
├── bin/
│   └── cclaude
├── templates/
│   ├── current.md
│   └── CLAUDE.local.md
├── docs/
│   ├── architecture.md
│   ├── current-md-guide.md
│   ├── migration.md
│   ├── philosophy.md
│   ├── session-archive.md
│   └── workflow.md
└── examples/
    ├── basic-project/
    └── project-example/
```

### 目标项目中的状态布局

```text
your-project/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   └── sessions/
└── CLAUDE.local.md -> .claude/CLAUDE.local.md
```

当前磁盘布局是 Claude-first 的，但 continuity model 的目标不是被某一个 frontend 永久绑定。

## Docs

- [Workflow](docs/workflow.md) — long-running AI coding workflow 的操作循环
- [current.md Guide](docs/current-md-guide.md) — live project state 应该写什么
- [Session Archive](docs/session-archive.md) — 如何检查 append-only state history
- [Philosophy](docs/philosophy.md) — 为什么 deterministic state 比 probabilistic recall 更可靠
- [Architecture](docs/architecture.md) — continuity primitives、Claude-first entrypoint 与 failure model
- [Migration Guide](docs/migration.md) — 如何从 ad hoc AI coding workflows 迁移过来

## Examples

- [examples/basic-project/](examples/basic-project/README.md) — 更贴近真实使用的 onboarding 示例，包含填充好的状态与 sample archive
- [examples/project-example/](examples/project-example/README.md) — 最小结构示例

## Current Scope

Chronora 当前有意保持范围收敛。

它现在是：

- AI coding workflow continuity infrastructure
- 面向 long-running development 的 deterministic state layer
- Claude-first in implementation
- AI-tool agnostic in architecture
- 默认 local、file-based、且可检查

它目前还不是：

- multi-frontend runtime support
- 已交付的 summary layer
- 跨 agent 的 task orchestration
- 面向所有 coding tool 的 unified runtime
- 完整的 AI workspace orchestration

## Roadmap

Chronora 的近期方向包括：

- summary layer
- task continuity
- multi-agent adapters
- unified runtime layer
- AI workspace orchestration

这些 roadmap 项目描述的是方向，不是当前已经交付的功能。当前生产路径仍然是 Claude Code。

## License

Chronora 基于 [MIT License](LICENSE) 发布。
