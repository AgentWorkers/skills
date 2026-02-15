---
name: savestate
description: **AI领域的“时间机器”：** 为你的AI代理提供加密备份、数据恢复以及跨平台迁移功能，保护其记忆数据和身份信息。支持OpenClaw、ChatGPT、Claude、Gemini等多种AI模型。采用AES-256-GCM加密算法，并允许用户自行控制加密密钥。
user-invocable: true
metadata: {"openclaw":{"emoji":"💾","primaryEnv":"SAVESTATE_API_KEY"}}
---

# SaveState — 专为 AI 设计的时间机器工具

SaveState 可为您的 AI 代理创建加密的、基于时间点的快照，涵盖其状态、身份信息、对话记录及配置设置。与实时同步工具不同，SaveState 提供可版本控制的备份数据，支持数据恢复、对比以及跨平台迁移。

**主要特点：**
- 🔐 使用用户自控密钥的 AES-256-GCM 加密技术
- 🔄 支持跨平台迁移（例如：ChatGPT → Claude → OpenClaw 等）
- 📊 提供增量式快照及差异对比功能
- ⏰ 提供定时自动备份功能（Pro/Team 版）
- ☁️ 支持零知识加密的云存储服务（Pro/Team 版）

## 安装

```bash
# npm
npm install -g @savestate/cli

# Homebrew
brew tap savestatedev/tap && brew install savestate

# Direct install
curl -fsSL https://savestate.dev/install.sh | sh
```

## 快速入门

### 初始化（首次使用）
```bash
savestate init
```

系统会创建一个包含您加密密钥的 `.savestate/` 目录。**请务必备份您的密钥**——这是解密快照的唯一方式。

### 创建快照
```bash
savestate snapshot
```

系统会将当前代理的状态捕获并保存为加密文件。

### 列出所有快照
```bash
savestate list
# or
savestate ls
```

### 从快照中恢复数据
```bash
# Restore latest
savestate restore

# Restore specific snapshot
savestate restore ss-2026-02-01T12-00-00
```

### 比较不同快照
```bash
savestate diff ss-2026-01-15 ss-2026-02-01
```

## 平台适配器

SaveState 支持多种 AI 平台：

| 平台 | 适配器 | 功能 |
|----------|---------|--------------|
| **OpenClaw** | `openclaw` | 完整备份与恢复 |
| **Claude Code** | `claude-code` | 完整备份与恢复 |
| **OpenAI Assistants** | `openai-assistants` | 完整备份与恢复 |
| **ChatGPT** | `chatgpt` | 数据导出及内存恢复 |
| **Claude.ai** | `claude` | 数据导出及内存恢复 |
| **Gemini** | `gemini` | 数据导出（通过 Takeout 功能） |

可用的适配器列表：
```bash
savestate adapters
```

## 跨平台迁移

您可以在不同平台之间迁移 AI 代理的身份信息：

```bash
# Migrate from ChatGPT to Claude
savestate migrate --from chatgpt --to claude

# Restore a ChatGPT snapshot to OpenClaw
savestate restore ss-chatgpt-2026-01-15 --to openclaw
```

## 云存储（Pro/Team 版）

如果您购买了 Pro（每月 9 美元）或 Team（每月 29 美元）订阅服务，即可使用云存储功能：

```bash
# Login to SaveState cloud
savestate login

# Push snapshots to cloud
savestate cloud push

# Pull from cloud on new device
savestate cloud pull

# Schedule automatic backups
savestate schedule --every 6h
```

请访问 [https://savestate.dev](https://savestate.dev) 进行注册。

## 备份内容

### OpenClaw/Clawdbot
- `SOUL.md`, `IDENTITY.md`, `USER.md` — 身份相关文件
- `MEMORY.md`, `memory/*.md` — 内存数据及每日日志
- `TOOLS.md`, `HEARTBEAT.md` — 配置信息
- `skills/` — 已安装的技能及自定义设置
- 会话记录（可选）

### Claude Code
- `CLAUDE.md` — 系统提示信息
- `.claude/` — 设置及内存数据
- 项目清单及待办事项

### ChatGPT/Claude.ai/Gemini
- 对话历史记录
- 自定义指令/系统提示
- 内存数据

## 自动化示例

### 使用 Cron 任务进行定期备份（以 OpenClaw 为例）
您可以在 `HEARTBEAT.md` 文件中添加相应的脚本来实现自动备份：

```
## SaveState backup check
- If more than 24h since last snapshot, run: savestate snapshot
- Check with: savestate ls --json | jq '.[0].timestamp'
```

### 迁移前的准备工作
在更换平台之前，请执行以下操作：
1. 使用 `savestate snapshot` 命令创建最新备份。
2. （Pro 版用户）使用 `savestate cloud push` 将备份同步到云端。
3. 使用 `savestate migrate --from X --to Y` 命令执行平台迁移。

## 安全性
- **加密方式**：采用 AES-256-GCM 加密算法，并结合 Argon2id 算法生成密钥。
- **云存储安全**：仅存储加密后的数据。
- **密钥控制**：您拥有自己的加密密钥。
- **无数据泄露风险**：该工具不会向第三方发送任何数据。

## API 参考

```bash
savestate --help              # Show all commands
savestate <command> --help    # Command-specific help
savestate --version           # Show version (currently 0.4.2)
```

## 链接
- **官方网站**：[https://savestate.dev](https://savestate.dev)
- **GitHub 仓库**：[https://github.com/savestatedev/savestate](https://github.com/savestatedev/savestate)
- **npm 包**：[https://npmjs.com/package/@savestate/cli](https://npmjs.com/package/@savestate/cli)
- **支持邮箱**：[hello@savestate.dev](hello@savestate.dev)

## 与实时同步工具的对比

| 功能 | SaveState | 实时同步工具 |
|---------|-----------|-----------------|
| 基于时间点的数据恢复 | ✅ | ❌ |
| 版本历史记录 | ✅ | ❌ |
| 跨平台迁移 | ✅ | ❌ |
| 快照对比 | ✅ | ❌ |
| 多平台支持 | ✅（支持 6 个平台） | 通常仅支持 1 个平台 |
| 持续同步 | ❌（仅定期备份） | ✅ |

SaveState 与实时同步工具相辅相成——结合使用可提供更全面的数据保护。