---
name: scribe
description: >
  **自主会话记录器**  
  该工具会读取当天的 OpenClaw 会话日志，提取其中的决策内容、用户偏好设置、框架相关的语句以及项目更新信息，随后生成一份结构化的每日记录文件。适用于为 AI 代理设置自动化的日志提取功能，或在需要时手动触发日志整合操作。该工具既可作为 Cron 作业（独立运行）使用，也可按需手动调用。
---
# Scribe

这是一个自主的“速记”代理，它会监控您的 OpenClaw 会话历史记录，并将重要的信息提取到持久化的、结构化的记忆文件中——这样您的代理就能在不同会话之间保持记忆，而无需依赖上下文窗口的压缩功能。

## 安装与设置

**1. 将该技能复制到您的工作空间：**
```bash
cp -r skills/public/scribe ~/.openclaw/workspace/skills/public/scribe
```

**2. 注册夜间定时任务（一个命令即可）：**
```bash
python3 skills/public/scribe/scripts/setup-cron.py
```

就这样。Scribe 每晚 23:30 会运行，并将 `memory/YYYY-MM-DD.md` 文件写入您的工作空间。

**3. 需要时也可以手动运行：**
```bash
python3 skills/public/scribe/scripts/scribe.py
```

## 工作原理

1. 从 `~/.openclaw/agents/main/sessions/` 目录中扫描当天的会话 JSONL 文件。
2. 过滤掉心跳信号、系统消息和无关信息。
3. 通过 OpenRouter 将用户消息发送给大型语言模型（LLM），并读取您现有的 OpenClaw API 密钥。
4. 提取关键信息，包括决策、偏好设置、框架相关的语句以及项目更新内容。
5. 将处理后的数据写入 `{workspace}/memory/YYYY-MM-DD.md` 文件中。

## 输出格式

```markdown
# YYYY-MM-DD Memory (Scribe)

## 🔑 Decisions Made
## 💡 Preferences & Rules
## 🗣️ Framework Sentences
## 📦 Project Updates
## ✅ Todos / Follow-ups
```

## 配置

环境变量（均为可选，默认值即可满足基本需求）：

| 变量            | 默认值            | 说明                          |
|-----------------|-----------------|-------------------------------------------|
| `SCRIBE_SESSION_DIR` | `~/.openclaw/agents/main/sessions` | 会话 JSONL 文件的存储路径                |
| `SCRIBE_WORKSPACE` | `~/.openclaw/workspace` | 记忆文件的保存路径                     |
| `SCRIBE_DAYS` | `1`              | 需要扫描的会话天数                      |
| `SCRIBE_MODEL` | `anthropic/claude-haiku-4-5` | 使用的大型语言模型（OpenRouter ID）             |
| `SCRIBE_APPEND_LONGTERM` | `false`            | 是否将数据追加到现有的 `MEMORY.md` 文件中           |
| `OPENROUTER_API_KEY` | *(来自 OpenClaw 配置文件)* | 可覆盖的 API 密钥                        |

## 参考资料

- **定时任务设置详情**：`references/cron-setup.md` — 手动配置、launchd 的使用方法以及时区设置调整
- **信号分类规则**：`references/signal-guide.md` — 大型语言模型如何判断哪些信息值得提取