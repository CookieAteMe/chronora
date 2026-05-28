# Chronora

> 一个面向软件开发的 **AI IDE Continuity Layer**，用确定性的、文件驱动的方式维护长期项目状态。
>
> [English](README.md)

> **Coding agents do not primarily need better chat memory.**
>
> **They need deterministic project state.**

Chronora 不是一个只为某个模型准备的小脚本，而是一层面向 AI 编程场景的连续性基础设施。

它的核心目标，是把关键上下文从临时的聊天窗口里拿出来，落到显式、可检查、可版本化的项目状态文件中。当前仓库提供的是一个基于 Claude Code 的参考接入器，但这个系统本身并不依赖 Claude。Claude、Codex、OpenCode，甚至 IDE 内置 agent，本质上都只是前端；真正需要稳定的是背后的 continuity layer。

## 愿景

构建一层可落地的 AI 开发操作层，让长期软件工程中的上下文连续性变成显式状态，而不是对话残影。

长期来看，我们希望 AI 参与的软件开发，不再依赖“这次聊天窗口里还记得多少”，而是依赖一套稳定的项目状态模型：无论换模型、换终端、换 IDE，agent 都能从同一份确定性的项目状态继续工作。

## 为什么需要它

AI 编程工具在局部推理、代码生成、短链路执行上进步很快，但在“跨 session 的项目连续性”上仍然脆弱。

真实的软件工程里，真正难的通常不是“下一段代码怎么写”，而是以下这些东西如何持续保持一致：

- 当前的架构决策
- 现实存在的约束条件
- 尚未解决的问题
- 正在推进的任务
- 跨 session 的工作意图
- 历史记录与当前真实状态之间的边界

如果没有一层确定性的状态管理，用户就会被迫充当唯一的长期记忆系统。

## Chat 式 AI 开发的问题

随着项目周期变长、状态变复杂，纯聊天式开发会越来越不稳定。

常见问题包括：

- 架构决策在每次新会话里被重新讨论一遍
- 未完成的工作不能自然续接，只能重新摸索
- 重要信息被埋进超长对话里，难以编辑和维护
- 关键约束存在于 token 历史中，而不是存在于显式状态里
- 一旦切换模型、工具或上下文窗口，agent 行为就开始漂移

聊天记录适合作为执行痕迹，不适合作为主要状态存储。

## 确定性的项目状态

Chronora 把“AI 连续性”看成一个状态管理问题，而不是一个对话召回问题。

一个确定性的项目状态，应当具备四个特征：

1. **显式**：重要上下文被写下来，而不是依赖模型隐式记住。
2. **可检查**：人和 agent 读取的是同一份状态源。
3. **可编辑**：项目现实变化时，可以直接修正状态。
4. **可版本化**：状态变化可以归档、diff、审阅。

因此，这个系统从一开始就是 **file-driven state**。

在完整的概念模型里，项目连续性会被拆成几类状态对象：

- `CLAUDE.local.md` 或其他前端本地指令文件
- 作为项目当前真相的 `current.md`
- 用于持久任务拆解与归属的 `tasks/`
- 用于长期压缩摘要的 `summaries/`
- 作为追加写历史的 `sessions/`

当前参考实现已经落地了 `current.md` 和 `sessions/`，并且在架构上为更完整的状态图留好了扩展空间。

## 有状态 AI 开发

所谓 stateful AI development，不是让 agent “更会聊天”，而是让它每次进入项目时，都能进入一个已有运行上下文。

基本循环是：

1. 读取项目本地规则
2. 加载当前项目状态
3. 基于状态执行工作
4. 在持久事实变化时更新状态
5. 将 session 以追加写方式归档
6. 让下一次会话从更新后的状态继续

这更像系统运行，而不是聊天续接。它依赖的是文件状态、确定性上下文和清晰的归档边界。

## 架构

Chronora 的定位是一个 **AI IDE Continuity Layer**。

前端 agent 可以变化，但 continuity contract 不应该跟着变化。

### 逻辑状态流

```text
Claude Code / Codex / OpenCode / IDE Agent
                  |
                  v
             项目本地指令层
        (CLAUDE.local.md 等)
                  |
                  v
             项目当前状态层
               (current.md)
                  |
                  v
            结构化工作状态层
         (tasks/ 和 summaries/)
                  |
                  v
             追加写 session 历史
               (sessions/)
```

### 当前参考接入器

```text
cclaude
  -> 确保 .claude/ 存在
  -> 从模板生成 current.md 和 CLAUDE.local.md
  -> 创建根目录软链接
  -> 记录 session 开始前状态
  -> 启动编码前端
  -> 记录 session 结束后状态
  -> 追加写 metadata
```

### 架构立场

- continuity layer 持有状态，而不是 frontend 持有状态
- archive 是追加写历史，不是当前真相
- summary 的职责是压缩状态，不是替代状态
- 项目状态必须能穿越模型切换和进程重启
- 不应该污染目标项目已有的主 `CLAUDE.md`

## 目录结构

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
│   ├── workflow.md
│   └── migration.md
└── examples/
    └── project-example/
```

### 目标项目中的状态布局

```text
your-project/
├── .claude/
│   ├── current.md
│   ├── CLAUDE.local.md
│   ├── sessions/
│   ├── tasks/       # 可选 / 面向未来扩展
│   └── summaries/   # 可选 / 面向未来扩展
└── CLAUDE.local.md -> .claude/CLAUDE.local.md
```

当前实现会自动初始化 `current.md`、`CLAUDE.local.md` 和 `sessions/`。更完整的 `tasks/`、`summaries/` 状态域，则属于这个系统的自然演进方向。

## 工作流

整个工作流追求的是可预测、可恢复、可续接。

### 1. Bootstrap

从项目根目录启动 frontend adapter。若 continuity layer 不存在，就先完成初始化。

### 2. Load State

coding agent 在提出任何修改建议前，先读取项目本地规则与当前项目状态。

### 3. Execute

agent 在既有状态约束下完成实现、调试、研究或重构。

### 4. Update Durable State

当关键决策、阻塞项、下一步方向发生实质变化时，更新 `current.md`，而不是把希望寄托在聊天窗口上。

### 5. Compress

把高噪音对话压缩成低熵的长期状态。系统强调的是“有编辑意图的摘要”，不是“堆积 transcript”。

### 6. Archive

将 session 以 append-only 方式归档，既保留历史，又不让历史覆盖当前运行状态。

### 7. Resume

后续 session 即使发生在另一台机器、另一个模型、另一个时间点，也可以从同一份项目状态继续。

## Session Archive System

session archive 是一个 **append-only archive**，记录项目状态如何随时间演化。

每次调用都会在 `.claude/sessions/` 下生成一个带时间戳的目录，通常包含：

- `current.before.md`
- `current.after.md`
- `CLAUDE.local.before.md`
- `CLAUDE.local.after.md`
- `session.meta`

它的价值主要体现在三个方面：

1. **可审计**：你能看到状态是如何变化的。
2. **可调试**：你能知道 agent 在进入和退出 session 时分别相信什么。
3. **可恢复**：当 live state 需要修正时，你不会丢失历史轨迹。

archive 是历史证据，不是当前真相。

## Summary Compression Philosophy

长期运行的 AI 系统一定需要压缩，但压缩不能靠“自动记住一点”。压缩应该是一种明确的状态工程。

Chronora 区分三件事：

- **history**：发生过什么
- **summary**：什么仍然重要
- **current state**：下一次 agent 必须立即视为真相的是什么

摘要的目标，不是把聊天记录写得更好看，而是把长期有效的工程信息提炼出来。

好的压缩应该：

- 去掉对话噪音
- 保留决策与约束
- 保留可执行的下一步
- 降低下一次会话的歧义

坏的压缩则会：

- 把 transcript 直接塞进状态文件
- 不区分轻重，什么都存
- 把已经过时的讨论当成当前真相

随着系统演进，`summaries/` 应当成为位于原始 session 历史之上、live state 之下的一层正式压缩层。

## 任务连续性

coding agent 需要的，不只是“记住一些事实”，更是“把工作持续做下去”的能力。

这意味着系统要能保留：

- 当前在做什么
- 什么被阻塞了
- 依赖关系是什么
- 下一个 agent 应该接什么
- 什么已经完成，什么只是讨论过

在当前阶段，这些信息可以先通过 `current.md` 承载。更进一步的演进，则是形成显式的 `tasks/` 状态图，记录任务归属、依赖和执行元数据。

对于 long-running coding agents 来说，任务连续性是刚需，因为真实工作单元几乎从来都不是一个 prompt，而是一串跨 session 的执行链条。

## Comparison

确定性状态并不是给 AI 增加“记忆”的唯一方式，但它比多数基于召回的方案更适合软件工程。

| 方案 | 核心机制 | 优势 | 在 coding continuity 上的局限 |
| --- | --- | --- | --- |
| Chat history | 线性对话记录 | 零配置、天然存在 | 受 token 限制、隐式、难编辑、难区分历史与当前真相 |
| Cursor memory | 工具内管理的助手记忆 | 方便个性化与轻量提示 | 不是确定性的项目运行状态，可审计性有限 |
| Mem0 | 语义记忆召回 | 适合记事实、偏好、跨会话信息 | 核心仍是 retrieval，而不是 state；不适合表达精确项目真相 |
| Vector memory | embedding 检索 | 擅长大规模模糊召回 | 召回结果非确定、排序有歧义、天然不适合作为 source of truth |
| Chronora | 显式文件状态 + append-only archive | 确定、可检查、可编辑、可版本化 | 需要团队保持状态质量 |

为什么这对 coding 尤其重要？

因为软件项目首先是一个**协调系统**，不是一个“找回相似语义片段”的系统。它需要的是明确约束、当前真相、任务衔接和可追踪演化。

## 为什么不用 Vector Memory

Vector memory 在大规模、模糊、跨文档语义召回里很有价值。

但这不是这里的主要问题。

在 coding continuity 场景下，关键问题通常不是：

- “之前有没有人说过类似的话？”
- “哪个 chunk 排名最靠前？”

真正的问题是：

- “当前架构决策到底是什么？”
- “现在真正的阻塞项是什么？”
- “下一个 agent 应该把什么当成事实？”
- “这次 session 相比上次到底改了什么？”

这些都是 state 问题，不是 retrieval 问题。

Embedding recall 本质上是概率性的，而项目状态应该是确定性的。

## 为什么 `current.md` 是 Source of Truth

`current.md` 的职责，是承载“下一次编码 session 开始前必须先加载的那一小组关键事实”。

它之所以应该成为 source of truth，是因为它同时满足：

- 现实变化时可以直接更新
- 足够简洁，不会失去可读性
- 足够显式，可以被人类审阅
- 跨 session、跨 frontend 稳定存在

archive 负责回答“我们是怎么走到这里的”。

`current.md` 负责回答“这里现在到底是什么状态”。

这个边界非常关键。

如果聊天记录里的某个事实和 `current.md` 冲突，那么在状态文件未被修正之前，聊天记录只是历史上下文，`current.md` 才是运行真相。

## Philosophy

Chronora 背后是一套偏系统工程的理念，而不是一套偏 prompt engineering 的技巧。

### File-driven state

关键上下文必须落在普通文件里，这样用户才能直接查看、diff、修改、审阅、提交。

### Append-only archive

历史应该持续累积，而不是被改写。只有这样，调试和长期分析才有依据。

### Explicit state

系统不应该依赖隐式记忆、黑盒排序或“刚好想起来”来承载关键项目事实。

### Deterministic context

无论上下文窗口多大、聊天是否截断、前端来自哪个厂商，下一次 session 都应该加载到同一份运行状态。

这套理念看起来保守，但工程基础设施真正可靠，往往正是因为它足够显式，而不是因为它足够魔法。

## Installation

当前仓库提供的是一个基于 macOS zsh 的参考接入器 `cclaude`。

```bash
git clone <repo-url>
cd chronora
./install.sh
```

安装脚本会：

- 将 `cclaude` 复制到 `~/bin`
- 自动添加可执行权限
- 将默认模板安装到 `~/.local/share/chronora/templates`
- 如果 `~/bin` 不在 `PATH` 中，会给出提示

## Quick Start

在任意项目目录中执行：

```bash
cd ~/work/my-project
cclaude
```

首次运行时，adapter 会创建：

- `.claude/current.md`
- `.claude/CLAUDE.local.md`
- `.claude/sessions/`
- 根目录软链接 `CLAUDE.local.md`

随后你就拥有一个标准的 stateful workflow：

1. 启动 coding session
2. 读取确定性的项目状态
3. 执行工作
4. 当持久事实变化时更新 `current.md`
5. 让 append-only archive 记录整个 session

## Example Project

可以查看 `examples/project-example/` 了解最小参考布局。

这个示例展示了：

- 项目本地 `.claude/` 状态目录
- 根目录 `CLAUDE.local.md` 软链接
- 预置的 `current.md`
- 占位的 session archive 目录

## Multi-Agent Compatibility

这个项目在理念上并不绑定 Claude。

更准确地说，它是一层 **AI IDE Continuity Layer**：

- Claude Code 可以是一个 frontend
- Codex 可以是一个 frontend
- OpenCode 可以是一个 frontend
- IDE 内置 agent 也可以是 frontend

任何能够稳定读取、遵守、更新这套状态契约的 agent，都可以接入。

这点非常重要，因为未来的长期软件开发，几乎一定会同时涉及多个 agent、多个入口和多个工作界面。能够把它们协调起来的，不会是“它们共享同一个聊天记忆”，而会是“它们共享同一套确定性的项目状态”。

## Long-Term Vision

长期愿景，是把这个项目发展成一个面向软件工程的 AI operating workspace。

这意味着未来它应该支持：

- 跨长时间跨度的 summary compression
- 带依赖关系的 task graph
- 基于共享项目状态的 multi-agent coordination
- 状态校验与冲突检测
- 独立于任何单一 frontend 的项目连续性
- agent 可替换，但 state 保持稳定的运行模型

到了那个阶段，AI development infrastructure 的形态会更像一个 **project state engine**，而不再像聊天记录管理器。

## Future Roadmap

中短期可预期的方向包括：

- `tasks/` 的一等支持，用于真正的任务连续性
- `summaries/` 的一等支持，用于结构化压缩层
- 除 `cclaude` 外更多 frontend adapter
- `current.md` 的状态 lint 与质量检查
- archive 的可视化与 diff 工具
- 面向并发 agent 的状态合并语义
- 更高层级的 AI operating workspace 抽象

## Design Principles

1. **Determinism over recall**：精确状态优先于近似召回。
2. **Local-first operation**：连续性不应依赖外部基础设施才能成立。
3. **Human readability**：状态必须能被工程师直接理解。
4. **Append-only history**：迭代过程中不应该销毁历史证据。
5. **Frontend neutrality**：状态模型应该比单一工具活得更久。
6. **Minimal hidden behavior**：核心机制应当体现在文件和脚本里，而不是黑盒里。
7. **Disciplined compression**：摘要的目标是降熵，不是制造新的歧义。

## FAQ

### 这是 Claude 专属工具吗？

不是。当前仓库提供的是 Claude Code 的参考接入器，但架构本身是 frontend-agnostic 的。更准确的理解方式，是把它看成一层 AI IDE continuity layer。

### 为什么不能只依赖 chat history？

因为 chat history 是隐式的、受 token 限制的，也不擅长区分“旧讨论”和“当前真相”。软件开发需要的是可编辑状态。

### 为什么使用 Markdown 文件，而不是数据库或向量存储？

因为这里最核心的要求是确定性、可检查性和低运维复杂度。普通文件更容易审计和修正。

### `current.md` 里应该写什么？

只写持久有效的项目真相：架构选择、关键约束、当前阻塞、主要方向、下一步计划。不要把原始聊天记录直接塞进去。

### session archive 是 source of truth 吗？

不是。archive 是 append-only 的历史证据，`current.md` 才是 live operational state。

### 多个 agent 可以共享同一套状态吗？

可以，而且这正是把连续性从聊天记忆提升为显式状态的主要原因之一。

### 它会替代 issue tracker 或正式项目管理系统吗？

不会。它更像是仓库内部的一层 AI-native continuity layer，用来补上 agent 工作流里最缺的那部分状态连续性。

### 为什么这个项目看起来更像基础设施，而不是 wrapper？

因为 wrapper 只是入口，真正的系统是背后的状态模型：确定性上下文、append-only archive，以及面向 long-running coding agents 的显式连续性。
