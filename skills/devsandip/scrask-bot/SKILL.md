---
name: scrask-bot
version: 3.0.0
description: 当用户通过 Telegram 发送截图时，使用 Gemini（快速且为默认选择）进行解析；如果解析的置信度较低，则会自动切换到 Claude 进行解析。解析结果会保存到 Google 日历（作为事件）或 Google 任务（作为提醒和任务）。如果解析的置信度较高，则会静默地完成保存；如果存在不确定性，则会请求用户确认。
author: your-name
metadata:
  openclaw:
    emoji: "🦞"
    primaryEnv: GEMINI_API_KEY
    requires:
      env:
        - GOOGLE_CREDENTIALS
        - GEMINI_API_KEY         # required for auto and gemini modes
        # - ANTHROPIC_API_KEY   # optional — enables Claude fallback in auto mode
      bins:
        - python3
    config:
      vision_provider:
        type: string
        description: >
          Vision model provider.
          'auto' = Gemini first, Claude fallback if any item confidence < fallback_threshold.
          'gemini' = Gemini only. 'claude' = Claude only.
        default: auto
      fallback_threshold:
        type: number
        description: "Confidence floor for auto mode. If any item is below this, Claude reruns the parse."
        default: 0.60
      timezone:
        type: string
        description: "User's IANA timezone. Used when none is detected in the screenshot."
        default: "UTC"
      confidence_threshold:
        type: number
        description: "0.0–1.0. Items below this score ask for confirmation. Items above save silently."
        default: 0.75
      reminder_minutes_before:
        type: integer
        description: "Popup reminder lead time in minutes for Google Calendar events."
        default: 30
---
# Scrask Bot

## 概述

当用户通过 **Telegram** 发送截图时，该技能会被激活。它利用视觉人工智能从图片中提取可操作的信息，然后执行以下操作：

- **高置信度（≥ 0.75）**：立即保存截图并回复简短的确认信息。
- **低置信度（< 0.75）**：在 Telegram 中显示截图的预览内容，并在保存前请求用户确认。

**提供者行为（自动模式，默认设置）：**

| 步骤 | 操作内容 |
|---|---|
| 1 | Gemini 2.0 Flash 快速解析截图 |
| 2 | 如果有任何项目的置信度低于 0.60，Claude Opus 会重新解析该项目 |
| 3 | 选择平均置信度较高的提供者来处理该项目 |
| 4 | 输出结果中包含 `provider`（提供者名称）、`fallback_triggered`（触发备用提供者的原因）以及置信度变化量 |

将 `vision_provider` 设置为 `"claude"` 或 `"gemini"` 可以锁定特定的提供者。

**输出目的地（由 AI 根据内容类型决定）：**

| 检测到的内容类型 | 输出目的地 |
|---|---|
| 事件（包含日期、时间、地点或邀请链接） | Google 日历 |
| 提醒事项（截止日期、到期日或个人任务） | Google 任务（带有到期日期） |
| 任务（无日期，仅包含行动项） | Google 任务（无到期日期） |

---

## 触发条件

在以下情况下激活该技能：
1. 用户在 Telegram 中发送包含 **图片附件** 的消息。
2. 该图片为 **截图**（而非人物、地点或实物照片）。
3. 没有其他技能已处理该图片。

**不适用于以下情况：**
- 人物、地点、食物的照片。
- 代码截图、错误信息或用户界面错误的截图（请交给其他技能处理）。
- 用户明确要求编辑、描述或分析其他用途的图片。

---

## 分步说明

### 第一步：立即回复

立即在 Telegram 中回复用户，让用户知道技能正在运行：

> “📸 收到啦——正在分析您的截图……”

不要让用户等待太久。

---

### 第二步：运行解析器

```bash
python3 ~/.openclaw/skills/scrask-bot/scripts/scrask_bot.py \
  --image-path "<path-to-temp-image>" \
  --provider "$CONFIG_VISION_PROVIDER" \
  --timezone "$CONFIG_TIMEZONE" \
  --google-credentials "$GOOGLE_CREDENTIALS"

The script auto-resolves the API key from ANTHROPIC_API_KEY or GEMINI_API_KEY
depending on the provider — no need to pass it explicitly.
```

脚本返回一个 JSON 对象，其中包含以下信息：
- `success`：解析是否成功。
- `no_actionable_content`：如果未找到可操作的信息，则值为 `true`。
- `results[]`：每个检测到的项目都包含 `confidence`（置信度）、`type`（类型）、`destination`（输出目的地）、`needsconfirmation`（是否需要确认）和 `action_taken`（已执行的操作）。
- `telegram_reply`：预先格式化好的回复消息，用于发送给用户。

---

### 第三步：处理输出结果

**如果 `no_actionable_content` 为 `true`：**
回复：“🤷 我在截图中未找到任何事件、提醒事项或任务信息。您能描述一下您想添加的内容吗？”

**如果 `success` 为 `true`：**
直接将 `telegram_reply` 的内容发送回用户。脚本已经完成了以下操作：
- 保存了置信度较高的项目。
- 为置信度较低的项目准备了确认提示。

**请不要重新组织或格式化 `telegram_reply`，直接原样发送。**

---

### 第四步：处理用户的确认回复

如果脚本返回了 `needsconfirmation` 为 `true` 的项目，请等待用户的回复：
- 如果用户回复 “yes”/“save”/“add”，则重新运行脚本以处理该项目（此时 `needsconfirmation` 应设置为 `true`）；或者直接使用 `calendar_create`/`tasks_create` 工具来处理该项目。
- 如果用户回复 “edit”，询问需要修改的内容，更新相关字段后保存。
- 如果用户回复 “skip”/“no”，回复：“明白了，已跳过该项目 ✓”。

---

### 第五步：确认保存结果

对于置信度较高、被自动保存的项目，脚本中的 `telegram_reply` 已经包含了确认信息。例如：
- `📅 已添加到日历：**团队站会** — 2026-03-01 09:00`
- `🔔 已添加到任务：**支付电费**（截止日期：2026-02-28）`
- `✅ 已添加到任务：**审核 Arjun 的代码提交**`

---

## 特殊情况处理

| 情况 | 处理方式 |
|---|---|
| 截图使用的是印地语、泰米尔语或其他语言 | 静默提取并翻译内容；将标题翻译成英语后保存 |
| 循环事件（如“每周一”） | 在日历事件中设置重复规则；并在回复中提及 |
| 日期已经过去 | 在回复中提示：“⚠️ 该日期已经过去（2月10日）。仍要保存吗？” |
- 一张截图中包含多个项目 | 分别处理每个项目；如有需要，逐个确认 |
- 如果截图是某人的日历内容 | 检测 `already_in_calendar_hint` 标志；回复：“看起来这个事件已经在您的日历中了 🗓️”
- Google API 认证失败 | 回复具体的错误信息，并建议用户重新检查 GOOGLE_CREDENTIALS |
- 如果截图中包含 Zoom/Meet 链接 | 将链接同时添加到日历中（作为地点和描述） |

---

## 配置设置

```json
{
  "skills": {
    "entries": {
      "scrask-bot": {
        "enabled": true,
        "env": {
          "GEMINI_API_KEY": "AIza-your-gemini-key",
          "ANTHROPIC_API_KEY": "sk-ant-your-key-here",
          "GOOGLE_CREDENTIALS": "/home/user/.openclaw/google-creds.json"
        },
        "config": {
          "vision_provider": "auto",
          "fallback_threshold": 0.60,
          "timezone": "Asia/Kolkata",
          "confidence_threshold": 0.75,
          "reminder_minutes_before": 30
        }
      }
    }
  }
}
```

---

## 所需权限

- `image:read`：用于从 Telegram 中获取截图。
- `network:outbound`：用于调用 Anthropic API 和 Google API。
- `telegram:reply`：用于向用户发送确认消息。