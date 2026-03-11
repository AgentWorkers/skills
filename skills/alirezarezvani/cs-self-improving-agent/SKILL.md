---
name: "self-improving-agent"
description: "将 Claude Code 自动记录的代码信息整理成可长期使用的项目知识。分析 MEMORY.md 文件中的模式和规律，将经过验证的学习成果整合到 CLAUDE.md 以及 .claude/rules/ 文件中，并将重复出现的解决方案提取为可复用的技能。这些功能可用于以下场景：  
(1) 查看 Claude 对您项目的学习成果；  
(2) 将某些模式从临时笔记提升为正式的规则；  
(3) 将调试方法转化为可复用的技能；  
(4) 检查代码库的运行状态和容量。"
---
# 自我提升代理（Self-Improving Agent）

> 该插件负责自动捕获并整理 Claude Code 学习到的内容。

Claude Code 的自动记忆系统（v2.1.32 及以上版本）会自动将项目中的模式、调试技巧以及用户的偏好设置记录到 `MEMORY.md` 文件中。此插件为这一系统添加了智能处理功能：它分析 Claude 学到的内容，将经过验证的模式提升为项目规则，并将重复出现的解决方案提取为可重用的技能。

## 快速参考

| 命令 | 功能 |
|---------|-------------|
| `/si:review` | 分析 `MEMORY.md` 文件，找出需要提升的内容、过时的条目以及整合的机会 |
| `/si:promote` | 将某个模式从 `MEMORY.md` 提升到 `CLAUDE.md` 或 `.claude/rules/` 文件中 |
| `/si:extract` | 将经过验证的模式转换为独立的技能文件 |
| `/si:status` | 显示记忆系统的健康状况（包括文件数量、主题文件列表及建议） |
| `/si:remember` | 显式地将重要知识保存到自动记忆系统中 |

## 各组件之间的协作方式

```
┌─────────────────────────────────────────────────────────┐
│                  Claude Code Memory Stack                │
├─────────────┬──────────────────┬────────────────────────┤
│  CLAUDE.md  │   Auto Memory    │   Session Memory       │
│  (you write)│   (Claude writes)│   (Claude writes)      │
│  Rules &    │   MEMORY.md      │   Conversation logs    │
│  standards  │   + topic files  │   + continuity         │
│  Full load  │   First 200 lines│   Contextual load      │
├─────────────┴──────────────────┴────────────────────────┤
│              ↑ /si:promote        ↑ /si:review          │
│         Self-Improving Agent (this plugin)               │
│              ↓ /si:extract    ↓ /si:remember            │
├─────────────────────────────────────────────────────────┤
│  .claude/rules/    │    New Skills    │   Error Logs     │
│  (scoped rules)    │    (extracted)   │   (auto-captured)│
└─────────────────────────────────────────────────────────┘
```

## 安装

### Claude Code（插件）
```
/plugin marketplace add alirezarezvani/claude-skills
/plugin install self-improving-agent@claude-code-skills
```

### OpenClaw
```bash
clawhub install self-improving-agent
```

### Codex CLI
```bash
./scripts/codex-install.sh --skill self-improving-agent
```

## 记忆系统架构

### 文件及其来源与用途

| 文件 | 编写者 | 作用范围 | 加载方式 |
|------|-----------|-------|--------|
| `./CLAUDE.md` | 用户（通过 `/si:promote` 命令） | 项目规则 | 每次会话都会加载完整文件 |
| `~/.claude/CLAUDE.md` | 用户 | 全局偏好设置 | 每次会话都会加载完整文件 |
| `~/.claude/projects/<path>/memory/MEMORY.md` | Claude 自动生成 | 项目学习内容（前 200 行） |
| `~/.claude/projects/<path>/memory/*.md` | Claude 自动生成 | 与特定主题相关的笔记 | 按需加载 |
| `.claude/rules/*.md` | 用户（通过 `/si:promote` 命令） | 仅适用于特定文件类型的规则 | 在相关文件被打开时加载 |

### 提升内容的生命周期

```
1. Claude discovers pattern → auto-memory (MEMORY.md)
2. Pattern recurs 2-3x → /si:review flags it as promotion candidate
3. You approve → /si:promote graduates it to CLAUDE.md or rules/
4. Pattern becomes an enforced rule, not just a note
5. MEMORY.md entry removed → frees space for new learnings
```

## 核心概念

### 自动记忆系统仅负责数据的捕获，而非内容的筛选

自动记忆系统擅长记录 Claude 学到的内容，但它无法判断：
- 哪些学习内容是临时的，哪些是永久性的；
- 哪些模式应该被提升为项目规则；
- 当文件超过 200 行时，哪些内容属于过时的条目；
- 哪些解决方案足够优秀，可以成为可重用的技能。

而这正是该插件所负责的任务。

### 提升内容的流程

当你将某个学习内容提升为规则时，它就会从 Claude 的临时存储区（`MEMORY.md`）转移到项目的规则系统中（`CLAUDE.md` 或 `.claude/rules/`）。两者之间的区别很重要：
- **`MEMORY.md`**：记录的是“我注意到这个项目使用了 pnpm”这样的背景信息；
- **`CLAUDE.md`**：则记录的是“请使用 pnpm，而不是 npm”这样的强制性指令。

被提升的规则具有更高的优先级，并且会以完整的形式加载（不会被截断为 200 行）。

### 用于特定场景的规则目录

并非所有内容都适合保存在 `CLAUDE.md` 中。对于仅适用于特定文件类型的规则，可以使用 `.claude/rules/` 目录：

```yaml
# .claude/rules/api-testing.md
---
paths:
  - "src/api/**/*.test.ts"
  - "tests/api/**/*"
---
- Use supertest for API endpoint testing
- Mock external services with msw
- Always test error responses, not just happy paths
```

该目录仅在 Claude 处理 API 测试文件时才会被加载，否则不会产生任何额外开销。

## 相关组件

### `memory-analyst`  
分析 `MEMORY.md` 文件和主题文件，以识别：
- 在多次会话中重复出现的条目（需要提升的内容）；
- 引用已删除文件或过时模式的条目；
- 需要整合的相关条目；
- `MEMORY.md` 与 `CLAUDE.md` 之间的信息差异。

### `skill-extractor`  
将经过验证的模式转换为完整的技能文件，包括：
- 带有适当前言的 `SKILL.md` 文件；
- 参考文档；
- 示例代码及边缘情况；
- 可以通过 `/plugin install` 命令安装或通过 `clawhub publish` 发布。

## 钩子（Hooks）

### `error-capture`（`PostToolUse → Bash`）  
监控命令执行过程中的错误。一旦检测到错误，会向自动记忆系统添加一条结构化的记录，其中包含：
- 失败的命令；
- 错误输出（经过截断）；
- 时间戳和上下文信息；
- 建议的分类。

**性能开销**：成功时没有额外开销；仅在检测到错误时才会消耗约 30 个系统令牌。

## 平台支持

| 平台 | 记忆系统 | 该插件是否可用？ |
|----------|--------------|---------------|
| Claude Code | 自动记忆系统（`MEMORY.md`） | ✅ 完全支持 |
| OpenClaw | `workspace/MEMORY.md` | ✅ 支持（可读取工作区中的记忆数据） |
| Codex CLI | `AGENTS.md` | ✅ 支持（可读取 `AGENTS.md` 中的模式） |
| GitHub Copilot | `.github/copilot-instructions.md` | ⚠️ 仅支持手动提升规则 |

## 相关资源

- [Claude Code 的记忆系统文档](https://code.claude.com/docs/en/memory)  
- [pskoett/self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) — 设计灵感来源 |
- [playwright-pro](../playwright-pro/) — 本仓库中的另一个相关插件