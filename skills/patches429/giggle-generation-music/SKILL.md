---
name: giggle-generation-music
description: Use when the user wants to create, generate, or compose music—whether from text description, custom lyrics, or instrumental background music. Triggers: generate music, write a song, compose, create music, AI music, background music, instrumental, beats.
version: "0.0.7"
license: MIT
author: storyclaw-official
homepage: https://github.com/storyclaw-official/storyclaw-skills
requires:
  bins: [python3]
  env: [GIGGLE_API_KEY]
  pip: [requests]
metadata:
  openclaw:
    emoji: "📂"
    requires:
      bins: [python3]
      env: [GIGGLE_API_KEY]
      pip: [requests]
    primaryEnv: GIGGLE_API_KEY
    runtimeBehaviors:
      writes: ["~/.openclaw/skills/giggle-generation-music/logs/"]
      cron: "Registers polling job (2min interval) when user initiates music generation"
    installNotice: "Requires user acceptance. Writes to logs/; registers Cron; forwards raw stdout. See SKILL.md before installing."
---

# Giggle Music

**来源**: [storyclaw-official/storyclaw-skills](https://github.com/storyclaw-official/storyclaw-skills) · API: [giggle.pro](https://giggle.pro/)

通过 giggle.pro 生成 AI 音乐，支持简化模式和自定义模式。

---

## ⚠️ 安装前须知 — 您必须接受以下条款

本技能使用 **异步轮询** 功能。安装即表示您同意以下规则：

| 行为 | 详情 |
|----------|---------|
| **写入文件** | 将日志写入 `~/.openclaw/skills/giggle-generation-music/logs/` — 用于 Cron 任务去重 |
| **Cron 任务** | 每 2 分钟执行一次轮询；任务完成后自动停止 |
| **标准输出** | 脚本输出将原样发送给用户（不进行任何过滤） |

**系统要求**: `python3`, `GIGGLE_API_KEY`（环境变量），`requests`（依赖库）。**安装前请仔细阅读并同意这些条款。**

---

## 环境配置

**API 密钥**: 设置系统环境变量 `GIGGLE_API_KEY`。详情请参阅 [SETUP.md](SETUP.md)。

---

## 使用指南

### 模式选择（优先级从高到低）

| 用户输入 | 模式 | 说明 |
|------------|------|-------------|
| 用户提供完整的 **歌词** | 自定义模式 (B) | 必须是歌词，不能是描述 |
| 用户请求纯器乐/背景音乐 | 纯器乐模式 (C) | 无人声 |
| 其他需求（如风格、人声等） | 简化模式 (A) | 使用用户提供的描述作为提示；AI 会根据描述生成音乐 |

> **重要规则**: 如果用户未提供歌词，必须使用 **简化模式 A**。请严格按照用户提供的描述来设置 `--prompt` 参数；**不要添加或修改任何内容**。例如，用户请求“女性人声，1 分钟，古风浪漫曲”，则应输入 `--prompt "female voice, 1 min, ancient romance"`。

### 缺少信息时的处理方式

仅当用户输入非常模糊（例如仅输入“生成音乐”而未提供任何描述）时，才需要进一步询问：

```
Question: "What type of music would you like to generate?"
Options: AI compose (describe style) / Use my lyrics / Instrumental
```

---

## 执行流程（第 1 阶段：提交任务 + 第 2 阶段：Cron 轮询）

音乐生成通常需要 1–3 分钟。系统采用“快速提交 + Cron 轮询”的两阶段架构。

> **重要提示**: **绝对不要** 将 `GIGGLE_API_KEY` 作为参数传递给执行脚本。API 密钥会从系统环境变量中读取。请直接运行以下命令。

---

### 第 1 阶段：提交任务（执行耗时约 10 秒）

**首先向用户发送消息**: “音乐生成中，通常需要 1–3 分钟。结果会自动发送给您。”

#### 简化模式 (A)
```bash
python3 scripts/giggle_music_api.py --prompt "user description" --no-wait
```

#### 自定义模式 (B)
```bash
python3 scripts/giggle_music_api.py --custom \
  --prompt "lyrics content" \
  --style "pop, ballad" \
  --title "Song Title" \
  --vocal-gender female \
  --no-wait
```

#### 纯器乐模式 (C)
```bash
python3 scripts/giggle_music_api.py --prompt "user description" --instrumental --no-wait
```

**示例响应**:
```json
{"status": "started", "task_id": "xxx", "log_file": "/path/to/log"}
```

**立即将任务 ID 存储在内存中** (`addMemory`):
```
giggle-generation-music task_id: xxx (submitted: YYYY-MM-DD HH:mm)
```

---

### 第 2 阶段：注册 Cron 任务（每 2 分钟执行一次）

使用 `cron` 工具注册轮询任务。**请严格遵循参数格式；不要修改字段名称或添加额外字段**:

```json
{
  "action": "add",
  "job": {
    "name": "giggle-generation-music-<first 8 chars of task_id>",
    "schedule": {
      "kind": "every",
      "everyMs": 120000
    },
    "payload": {
      "kind": "systemEvent",
      "text": "Music task poll: exec python3 scripts/giggle_music_api.py --query --task-id <full task_id>, handle stdout per Cron logic. If stdout is non-JSON plain text, forward to user as-is and remove Cron. If stdout is JSON, do not send message, keep waiting. If stdout is empty, remove Cron immediately."
    },
    "sessionTarget": "main"
  }
}
```

每次 Cron 任务触发时，执行以下操作:
```bash
python3 scripts/giggle_music_api.py --query --task-id <task_id>
```

**音频链接的返回规则**: 标准输出中的链接必须是 **完整的签名 URL**（包含 Policy、Key-Pair-Id 和 Signature 参数）。正确格式示例：`https://assets.giggle.pro/...?Policy=...&Key-Pair-Id=...&Signature=...`。错误格式：不要返回仅包含基础路径的未签名链接（缺少查询参数）。脚本会将 `~` 替换为 `%7E`；在转发链接时保持原格式。

**Cron 任务触发处理**（根据标准输出判断结果）:

| 标准输出内容 | 处理方式 |
|----------------|--------|
| 非空纯文本（不以 `{` 开头） | **将标准输出原样发送给用户**（不添加前缀），**取消 Cron 任务** |
| 标准输出为空 | 任务已发送完毕，**立即取消 Cron 任务，无需再次发送通知** |
| JSON 格式（以 `{` 开头且包含 `"status"` 字段） | 不发送通知，继续等待下一次轮询 |

---

## 网关重启后的恢复方式

当用户询问之前的音乐生成进度时：

1. **如果任务 ID 存储在内存中**，直接执行 `--query --task-id xxx` 命令。**无需重新提交任务** |
2. **如果内存中不存在任务 ID**，告知用户是否需要重新生成音乐。

---

## 参数说明

| 参数 | 说明 |
|-----------|-------------|
| `--prompt` | 音乐描述或歌词（简化模式必填） |
| `--custom` | 启用自定义模式 |
| `--style` | 音乐风格（自定义模式必填） |
| `--title` | 歌曲标题（自定义模式必填） |
| `--instrumental` | 生成纯器乐 |
| `--vocal-gender` | 人声性别（仅限自定义模式） |
| `--query` | 查询任务状态（用于 Cron 轮询或手动查询） |
| `--task-id` | 任务 ID（与 `--query` 一起使用） |