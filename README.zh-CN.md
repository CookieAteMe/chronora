# Chronora

面向 AI 编程工具的持久上下文与 session 连续性工作流。

> Coding agents need deterministic state, not probabilistic recall.

[English](README.md) · [Workflow](docs/workflow.md) · [Philosophy](docs/philosophy.md) · [Example](examples/basic-project/README.md)

Chronora 是一个面向长期 coding session 的 v0.1 基础设施层。

它用普通项目文件为 AI 编程工具提供一层确定性的连续性机制：以 `current.md` 作为当前项目真相，以项目本地指令文件约束 agent 行为，并用 append-only session archive 保留状态演化轨迹。目标不是做一个更花哨的聊天包装器，而是让项目状态变得显式、可检查、可编辑、可持续。

## Why Chronora

聊天记录可以作为执行痕迹，但它不适合做软件工程的主状态系统。

在一次性的小任务里，对话上下文通常够用；但在真实仓库中，它很快会失效：

- 架构决策会在每次新会话里被重新讨论
- 尚未解决的阻塞会埋进 token 历史里
- 未完成的工作会被重新发现，而不是被自然续接
- 当前真相与历史推理会混在一起
- 用户会被迫成为唯一可靠的长期记忆系统

Chronora 通过把连续性从隐藏的聊天召回里移出来，落到确定性的项目状态中，来解决这个问题。

对于 coding agents，这意味着：

- 用**显式项目状态**替代推测出来的上下文
- 用 **`current.md` continuity** 替代每次从 prompt 重新拼装背景
- 用 **append-only session history** 保留状态是如何变化的
- 用 **summary-friendly state** 支持压缩，而不是把 transcript 当 source of truth
- 用 **deterministic continuity** 支撑长期 coding session

## What Chronora Provides

Chronora 在 v0.1 中刻意保持范围克制，只提供一个聚焦的工作流层：

- `current.md` 作为可变的 canonical project state
- `CLAUDE.local.md` 作为项目本地 agent 指令
- `.claude/sessions/` 作为 append-only session archive
- `cclaude` 作为 Claude Code 的启动 wrapper
- 可复用的模板与示例，帮助你复现实践方式

当前实现有意保持为 file-driven、shell-based。它不会引入数据库、vector store、embeddings，也不会引入新的 runtime orchestration 层。

## Installation

Chronora v0.1 当前主要面向 **macOS + zsh**，并要求已安装 [Claude Code CLI](https://claude.ai/code)。

```bash
git clone https://github.com/CookieAteMe/chronora.git
cd chronora
./install.sh
```

安装脚本会：

- 将 `cclaude` 复制到 `~/bin`
- 将默认模板安装到 `~/.local/share/chronora/templates`
- 确保安装后的 wrapper 具有可执行权限
- 检查 Claude Code CLI 是否可用
- 在 `~/bin` 不在 `PATH` 中时给出提示

如果需要，请将下面这行加入 `~/.zshrc`，然后重新加载 shell：

```bash
export PATH="$HOME/bin:$PATH"
```

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

### 2. 启动一个 continuity-aware coding session

`cclaude` 会先完成本地状态初始化、记录 before-state，然后在项目上下文中启动 Claude Code。

推荐的 session 循环是：

1. 运行 `cclaude`
2. 加载 `.claude/current.md`
3. 延续既有架构与约束条件
4. 当持久事实变化时更新 `current.md`
5. 退出后让 Chronora 自动归档本次 session

### 3. 把 `current.md` 当作 live project truth

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

### 4. 查看 session archive

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

这让你可以轻量地追踪项目状态如何演化，而不需要把聊天记录当作主状态系统。

### 5. 在下一次 session 里继续，而不是重新拼接上下文

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

## Docs

- [Workflow](docs/workflow.md) — session lifecycle 在实际项目中如何运作
- [current.md Guide](docs/current-md-guide.md) — canonical state file 应该写什么
- [Session Archive](docs/session-archive.md) — 如何阅读 append-only archive
- [Philosophy](docs/philosophy.md) — deterministic state 的设计理由
- [Architecture](docs/architecture.md) — 组件概览与 failure model
- [Migration Guide](docs/migration.md) — 如何从 ad hoc 工作流迁移过来

## Examples

- [examples/basic-project/](examples/basic-project/README.md) — 更贴近真实使用的 v0.1 onboarding 示例，包含填充好的状态与 sample archive
- [examples/project-example/](examples/project-example/README.md) — 最小结构示例

## Current Scope

Chronora 在 v0.1 中有意保持范围收敛。

它当前是：

- 面向 Claude Code 用户的持久工作流基础设施
- 面向 long-running coding sessions 的确定性状态层
- 围绕 `.claude/` 构建的 file-based continuity mechanism
- 一个严肃的 shell workflow，而不是完整 runtime 平台

它目前还不是：

- 数据库驱动的 state engine
- vector-memory 产品
- multi-agent orchestrator
- 面向所有 coding frontend 的通用 runtime

## Why Deterministic State Matters

Chronora 把项目连续性视为一个状态管理问题。

这意味着系统会明确区分：

- **history** —— 发生过什么
- **current state** —— 现在什么是真的
- **future work** —— 下一次 session 应该接什么

这条边界正是长期 coding session 能保持稳定的关键。历史很重要，但它不能替代 source-of-truth state。

## Roadmap

Chronora 的近期方向包括：

- 为新仓库提供更好的 onboarding
- 提供更强的 `current.md` 指南与示例
- 提升 archive 的检查体验
- 为不同类型项目提供更多 examples
- 在当前 Claude Code 参考工作流之外提供更多 adapter
- 为 summaries 与 task continuity 预留兼容的状态域

## License

Chronora 采用 [MIT License](LICENSE)。
