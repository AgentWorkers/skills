---
name: antigravity-quota
version: 1.1.0
description: 检查 Claude 和 Gemini 模型的 Antigravity 账户配额。显示剩余配额以及重置时间，并具备禁用用户的功能。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["node"]}}}
---

# Antigravity 配额管理技能

用于查询 Clawdbot 中配置的所有 Antigravity 账户的配额状态。

## 前提条件

- 已配置 Antigravity 账户的 Clawdbot
- 运行 `clawdbot configure` 命令以添加 Antigravity 账户

## 配额信息

- **Claude (Opus/Sonnet)** — 共享的 5 小时配额池
- **Gemini Pro** — 独立的 5 小时配额
- **Gemini Flash** — 独立的 5 小时配额

每种模型类型的配额每 5 小时会为每个账户重新计算。

## 使用方法

### 文本输出（默认格式）
```bash
node check-quota.js
```

### Markdown 表格（适用于 tablesnap）
```bash
node check-quota.js --table
node check-quota.js --table | tablesnap --theme light -o /tmp/quota.png
```

### JSON 输出
```bash
node check-quota.js --json
```

### 自定义时区
```bash
node check-quota.js --tz America/New_York
TZ=Europe/London node check-quota.js
```

## 输出结果

### 文本模式
```
📊 Antigravity Quota Check - 2026-01-08T07:08:29.268Z
⏰ Each model type resets every 5 hours
🌍 Times shown in: Asia/Kolkata

Found 9 account(s)

🔍 user@gmail.com (project-abc123)
   claude-opus-4-5-thinking: 65.3% (resets 1:48 PM)
   gemini-3-flash: 95.0% (resets 11:41 AM)
```

### 表格模式 (`--table`)
按照剩余配额量排序，使用表情符号表示：
- 🟢 剩余 80% 以上
- 🟡 剩余 50-79%
- 🟠 剩余 20-49%
- 🔴 剩余 <20%

## 与 tablesnap 的集成

对于不支持渲染 Markdown 表格的消息平台：
```bash
node check-quota.js --table | tablesnap --theme light -o /tmp/quota.png
# Then send the image
```

需要安装 `tablesnap`：
```bash
go install github.com/joargp/tablesnap/cmd/tablesnap@latest
```