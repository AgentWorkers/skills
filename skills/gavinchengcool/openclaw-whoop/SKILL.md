---
name: whoop
description: Official WHOOP Developer Platform integration for OpenClaw: OAuth connect/authorize, local token storage + refresh, and WHOOP v2 metric fetch (recovery, sleep, strain/cycle, workouts, profile, body measurements). Use when users say: connect WHOOP, authorize WHOOP, pull WHOOP data, get today/yesterday recovery/sleep/strain, generate daily/weekly WHOOP summaries, or push WHOOP updates to any chat channel (TUI/webchat/Slack/Discord/WhatsApp/Telegram/etc.).
---

# WHOOP（官方API）

使用此技能可以**连接WHOOP → 获取数据指标 → 生成消息**。

**功能范围：** WHOOP仅作为数据源使用。传输渠道不受限制：可以生成文本或Markdown格式的消息，并将其回复到当前聊天窗口中，或通过OpenClaw的`message`工具发送到其他渠道。

## 快速入门（最简步骤）

1) 设置环境变量：
   - `WHOOP_CLIENT_ID`
   - `WHOOP_CLIENT_SECRET`
   - `WHOOP_REDIRECT_URI`

2) 连接WHOOP（选择一种方式）：
   - **手机/远程模式（推荐）：** 运行相关命令后，将重定向URL或代码复制并粘贴回聊天窗口中。

   ```bash
python3 scripts/whoop_oauth_login.py
```

   **桌面快速连接方式（可选）：** 如果您在运行OpenClaw的同一台机器上的浏览器中进行授权，请将`WHOOP_REDIRECT_URI`设置为回环地址（例如`http://127.0.0.1:58539/callback`），然后运行相应命令：

   ```bash
python3 scripts/whoop_oauth_login.py --loopback
```

3) 获取并渲染当天的数据：

   ```bash
python3 scripts/whoop_fetch.py --date today --out /tmp/whoop_raw_today.json
python3 scripts/whoop_normalize.py /tmp/whoop_raw_today.json --out /tmp/whoop_today.json
python3 scripts/whoop_render.py /tmp/whoop_today.json --format markdown --channel generic
```

## 配置（必填）

请通过环境变量或直接在脚本中使用以下参数进行配置：
- `WHOOP_CLIENT_ID`
- `WHOOP_CLIENT_SECRET`
- `WHOOP_REDIRECT_URI`（必须与WHOOP开发者控制面板中的值完全一致）

**可选参数：**
- `WHOOP_TOKEN_PATH`（默认路径：`~/.config/openclaw/whoop/token.json`）
- `WHOOP_TZ`（默认时区：`Asia/Shanghai`）

## 工作流程1 — 连接WHOOP（使用OAuth登录）

1) 选择以下方式之一进行连接：
   - **手机/远程模式（推荐）：**

   ```bash
python3 scripts/whoop_oauth_login.py
```

   然后在任意设备上打开生成的URL，完成授权流程后，将重定向URL或代码复制并粘贴回聊天窗口中。

   - **桌面回环模式（可选）：**

   ```bash
python3 scripts/whoop_oauth_login.py --loopback
```

   仅当您的浏览器授权操作在运行OpenClaw的同一台机器上进行，并且`WHOOP_REDIRECT_URI`为回环地址（如`http://127.0.0.1:<port>/callback`）时，才使用此模式。

2) 脚本会将生成的访问令牌存储在`WHOOP_TOKEN_PATH`路径下。
   如需后续撤销令牌，请使用`delete /v2/user/access`命令（详情请参阅`references/whoop_api.md`）。

## 工作流程2 — 获取数据指标（当天/昨天）

1) 获取WHOOP API的原始数据：
   ```bash
python3 scripts/whoop_fetch.py --date today --out /tmp/whoop_raw_today.json
python3 scripts/whoop_fetch.py --date yesterday --out /tmp/whoop_raw_yday.json

Tip: `whoop_fetch.py` uses WHOOP’s `start`/`end` query params + `nextToken` pagination. Use `--tz` to control which local day is fetched (default from `WHOOP_TZ`).
```

2) 将数据转换为统一的JSON格式：
   ```bash
python3 scripts/whoop_normalize.py /tmp/whoop_raw_today.json --out /tmp/whoop_today.json
```

3) 生成适合人类阅读的消息：
   ```bash
python3 scripts/whoop_render.py /tmp/whoop_today.json --format markdown --channel generic

Channel formatting presets:
- `--channel discord` (uses **bold**)
- `--channel slack` / `--channel whatsapp` (uses *bold*, avoids fancy markup)
- `--channel telegram` (plain text)
```

   然后可以选择：
   - 将渲染后的消息直接回复到当前聊天窗口中，
   - 或通过OpenClaw的`message`工具将其发送到其他渠道。

## 工作流程3 — 日常/每周自动推送（使用cron任务）

如果用户需要定期接收推送消息，可以创建一个OpenClaw的cron任务，该任务会依次执行以下操作：
   - 调用`scripts/whoop_fetch.py`、`scripts/whoop_normalize.py`和`scripts/whoop_render.py`脚本
   - 将渲染后的消息发送到指定的目标渠道

**注意：** cron任务的发送渠道不受限制；目标渠道信息应作为cron任务参数传递。

**关于API的详细说明：**
- 有关API的权限范围、端点、分页规则和速率限制，请参阅`references/whoop_api.md`。
- 有关数据格式的规范（JSON格式），请参阅`references/output_schemas.md`。
- 如果OAuth授权失败（例如重定向地址不匹配、权限范围错误、收到401/429错误代码），请参阅`references/troubleshooting.md`。