---
name: rollbar
description: "监控和管理 Rollbar 错误跟踪功能。通过 Rollbar API 可以查看最近发生的错误记录、获取错误详情、解决错误问题或暂时屏蔽错误信息，以及跟踪应用程序的部署情况。"
homepage: https://github.com/vittor1o/rollbar-openclaw-skill
metadata:
  openclaw:
    emoji: "🐛"
    requires:
      env:
        - ROLLBAR_ACCESS_TOKEN
      bins:
        - curl
        - python3
---
# Rollbar 技能

直接通过 OpenClaw 监控和管理 Rollbar 中的错误。

## 设置

将您的 Rollbar 访问令牌设置为环境变量：

```bash
export ROLLBAR_ACCESS_TOKEN=your-token
```

> **⚠️ 安全提示：** 将令牌存储在环境变量或安全的密钥管理器中，切勿将其提交到仓库文件中。

**支持两种类型的令牌：**

- **项目级令牌**（推荐）——可在 Rollbar → 项目 → 设置 → 项目访问令牌中找到。使用具有 `read` 权限的令牌进行监控；仅在需要解决或屏蔽错误时添加 `write` 权限。这是针对单个项目使用的最严格且最安全的选项。
- **账户级令牌**（适用于多项目设置）——可在 Rollbar → 账户设置 → 账户访问令牌中找到。使用 `--project-id <id>` 来指定特定项目。此技能会自动从账户令牌中解析出项目访问令牌。注意：账户令牌授予更广泛的访问权限——仅在需要监控多个项目时使用。

## 命令

此技能中的所有命令都使用 `rollbar.sh` 辅助脚本。

### 列出项目（仅需要账户令牌）

```bash
./skills/rollbar/rollbar.sh projects
```

### 列出最近的事件（错误/警告）

```bash
./skills/rollbar/rollbar.sh items [--project-id <id>] [--status active|resolved|muted] [--level critical|error|warning|info] [--limit 20]
```

### 获取事件详情

```bash
./skills/rollbar/rollbar.sh item <item_id>
```

### 获取事件的重复出现次数

```bash
./skills/rollbar/rollbar.sh occurrences <item_id> [--limit 5]
```

### 解决事件

```bash
./skills/rollbar/rollbar.sh resolve <item_id>
```

### 屏蔽事件

```bash
./skills/rollbar/rollbar.sh mute <item_id>
```

### 激活（重新打开）事件

```bash
./skills/rollbar/rollbar.sh activate <item_id>
```

### 列出部署记录

```bash
./skills/rollbar/rollbar.sh deploys [--limit 10]
```

### 获取项目信息

```bash
./skills/rollbar/rollbar.sh project
```

### 最活跃的事件（摘要）

```bash
./skills/rollbar/rollbar.sh top [--limit 10] [--hours 24]
```

## 主动监控

为了在新出现的关键或错误事件时获得自动警报，请在 OpenClaw 中设置一个 cron 作业：

> “检查 Rollbar 中过去一小时内的新关键或错误事件。如果有新事件出现，请对其进行汇总并通知我。”

建议的调度时间：工作时间内每 30–60 分钟一次。

## 注意事项

- 所有输出均为 JSON 格式，便于解析。
- `top` 命令会根据事件的出现次数对活跃事件进行排序——适用于日常问题排查。
- Rollbar API 文档：https://docs.rollbar.com/reference