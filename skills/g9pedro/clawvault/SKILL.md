---
name: clawvault
version: "2.5.11"
description: Agent memory system with memory graph, context profiles, checkpoint/recover, structured storage, semantic search, and observational memory. Use when: storing/searching memories, preventing context death, graph-aware context retrieval, repairing broken sessions. Don't use when: general file I/O.
author: Versatly
repository: https://github.com/Versatly/clawvault
homepage: https://clawvault.dev
user-invocable: true
always: false
openclaw: {"emoji":"🐘","requires":{"bins":["clawvault","qmd"]}}
requires: {"bins":["clawvault","qmd"],"env_optional":["CLAWVAULT_PATH","OPENCLAW_HOME","OPENCLAW_STATE_DIR","GEMINI_API_KEY"]}
install: [{"id":"node","kind":"node","package":"clawvault","bins":["clawvault"],"label":"Install ClawVault CLI (npm)"},{"id":"qmd","kind":"node","package":"github:tobi/qmd","bins":["qmd"],"label":"Install qmd backend (required for query/context workflows)"}]
metadata: {"openclaw":{"emoji":"🐘","requires":{"bins":["clawvault","qmd"]},"install":[{"id":"node","kind":"node","package":"clawvault","bins":["clawvault"],"label":"Install ClawVault CLI (npm)"},{"id":"qmd","kind":"node","package":"github:tobi/qmd","bins":["qmd"],"label":"Install qmd backend (required for query/context workflows)"}],"env_optional":["CLAWVAULT_PATH","OPENCLAW_HOME","OPENCLAW_STATE_DIR","GEMINI_API_KEY"],"homepage":"https://clawvault.dev"}}
---

# ClawVault 🐘

大象永远不会忘记。专为 OpenClaw 代理设计的结构化存储解决方案。

> **专为 [OpenClaw](https://openclaw.ai) 开发**。标准安装方式：通过 npm CLI 安装后，再使用相应的钩子（hook）进行配置。

## 安全性与透明度

**该工具的功能：**
- 读写存储在 `CLAWVAULT_PATH` 目录中的 Markdown 文件（该路径可自动检测）；
- `repair-session` 功能会读取并修改 OpenClaw 会话记录（位于 `~/.openclaw/agents/` 目录下），并在写入前创建备份；
- 提供一个 OpenClaw 钩子包（`hooks/clawvault/handler.js`），包含多种生命周期事件处理逻辑（如 `gateway:startup`、`gateway:heartbeat`、`command:new`、`session:start`、`compaction:memoryFlush`、`cron.weekly`）。该钩子为可选配置，需手动安装并启用；
- `observe --compress` 功能会通过 LLM API（默认使用 Gemini Flash）对会话记录进行压缩。

**使用的环境变量：**
- `CLAWVAULT_PATH`：存储目录（可选，若未设置则自动检测）；
- `OPENCLAW_HOME` / `OPENCLAW_STATE_DIR`：`repair-session` 功能用于查找会话记录的路径；
- `GEMINI_API_KEY`：`observe` 功能在压缩会话记录时使用（仅限启用相关功能时）。

**注意：** 所有数据均存储在本地，除用于压缩的 LLM API 调用外，不进行任何网络传输。

**说明：** 这是一个完整的命令行工具，不仅提供指令，还能实际执行文件写入、钩子注册和代码运行等操作。

**审计性：** 发布的 ClawHub 工具包包含 `SKILL.md`、`HOOK.md` 和 `hooks/clawvault/handler.js` 文件，用户可在启用钩子前查看其具体行为。

## 安装（标准方式）

使用 `clawhub install clawvault` 可以获取安装指南，但该命令不会自动安装钩子包。

### 推荐的安装流程

#### 设置流程

#### 新代理的快速入门指南

#### 使用前的注意事项

**当前功能说明：**

ClawVault 需依赖 `qmd` 来处理核心的存储和查询逻辑。

### 功能概述

- **知识图谱构建：** 从 Markdown 文件中的链接、标签和前置内容构建类型化的知识图谱（存储路径为 `.clawvault/graph-index.json`，支持版本控制和增量重建）；
- **上下文检索：** 根据不同的需求（如 `default`、`planning`、`incident`、`handoff`、`auto` 等配置文件）提供相应的上下文检索功能；
- **兼容性诊断：** 提供 OpenClaw 的兼容性检查工具。

## 核心命令

- **唤醒/休眠会话：** 控制会话的启动和结束；
- **按类型存储数据：** 实现数据的分类存储；
- **快速将数据发送到收件箱：** 提供便捷的数据传输机制；
- **搜索功能：** 需要先安装 `qmd` 才能使用。

### 使用前的检查事项

ClawVault 目前依赖 `qmd` 来处理核心的存储和查询逻辑。

## 现有功能列表

### 知识图谱构建

ClawVault 可从 Markdown 文件中的链接、标签和前置内容构建类型化的知识图谱。

### 钩子配置

### 文件夹结构

#### 最佳实践

1. 会话开始时唤醒系统：使用 `clawvault wake` 恢复上下文；
2. 在高负载工作时每 10-15 分钟创建一个检查点；
3. 会话结束时进入休眠状态：使用 `clawvault sleep` 保存后续操作所需的上下文；
4. 明确数据存储类型：了解数据的用途有助于选择合适的存储位置；
5. 大量使用 Wiki 链接：`[[person-name]]` 格式可以帮助构建知识图谱。

#### AGENTS.md 的检查清单

请将此清单添加到现有的代理配置文件中。除非有特殊需求，否则不要替换原有的配置。

## 会话记录修复（v1.5.0 及以上版本）

当 Anthropic API 返回 “unexpected tool_use_id found in tool_result blocks” 错误时，请使用以下命令：

**修复内容：**
- 修复引用不存在的 `tool_use` ID 的孤立 `tool_result` 块；
- 修复因 JSON 数据不完整导致的工具调用异常；
- 修复损坏的父链引用问题。

系统会自动创建备份（使用 `--no-backup` 可跳过备份操作）。

### 常见问题解决方法：

- **未安装 qmd**：请先安装 qmd，然后使用 `qmd --version` 确认版本；
- **未找到 ClawVault**：运行 `clawvault init` 或设置 `CLAWVAULT_PATH`；
- **CLAWVAULT_PATH 未配置**：运行 `clawvault shell-init` 并将其添加到 shell 配置文件中；
- **存在过多孤立链接**：运行 `clawvault link --orphans` 修复问题；
- **收件箱积压**：处理或归档收件箱中的数据；
- **出现 “unexpected tool_use_id” 错误**：运行 `clawvault repair-session`；
- **OpenClaw 集成问题**：运行 `clawvault compat` 检查兼容性；
- **钩子配置失败/未找到**：运行 `openclaw hooks install clawvault`，然后 `openclaw hooks enable clawvault`，重启 OpenClaw 服务，并通过 `openclaw hooks list --verbose` 验证钩子状态；
- **知识图谱过时**：运行 `clawvault graph --refresh` 更新图谱；
- **上下文错误**：根据需要使用 `clawvault context --profile incident` 或 `--profile planning` 调用相应功能。

## 稳定性测试

- 代码类型检查通过（`npm run typecheck`）；
- 测试套件全部通过（449 项测试全部通过）；
- 对 Windows 平台进行了路径处理的优化：
  - `qmd` 的 URI 和文档路径规范化；
  - WebDAV 路径的安全性和文件系统解析；
  - `shell-init` 的输出格式符合预期；
- 通过 `clawvault compat --strict` 验证了 OpenClaw 的运行时兼容性（需安装本地 `openclaw` 可执行文件）。

## 与 qmd 的集成

ClawVault 使用 [qmd](https://github.com/tobi/qmd) 来支持搜索功能。

## 环境变量配置

- `CLAWVAULT_PATH`：默认的存储目录路径（未设置时自动检测）；
- `OPENCLAW_HOME`：OpenClaw 的主目录；
- `OPENCLAW_STATE_DIR`：OpenClaw 的状态目录；
- `GEMINI_API_KEY`：用于 LLM 压缩功能的配置项（可选）。

## 其他信息

- **npm 包下载地址：** https://www.npmjs.com/package/clawvault
- **GitHub 仓库：** https://github.com/Versatly/clawvault
- **问题反馈：** https://github.com/Versatly/clawvault/issues