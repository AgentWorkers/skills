---
name: bluebubbles-healthcheck
description: "**诊断并自动修复 BlueBubbles 与 OpenClaw 之间的 iMessage 连接问题**  
**适用场景：**  
- 当网关重启后 iMessage 无法送达；  
- Webhook 连接中断；  
- 用户反馈消息无法正常传输。  
**工作原理：**  
该工具会执行四步诊断流程，自动修复以下问题：  
1. Webhook 重试机制（backoff）异常；  
2. 过时的注册信息（stale registrations）；  
3. 网关（gateway）相关故障。"
homepage: https://github.com/amzzzzzzz/bluebubbles-healthcheck
metadata: { "openclaw": { "emoji": "🩺", "platform": "macOS", "requires": { "bins": ["curl", "python3", "nc", "openclaw"] }, "credentials": ["BB_PASSWORD"] } }
---
# BlueBubbles 健康检查技能

## 何时使用此技能

在以下情况下使用此技能：
- iMessages 无法发送到/从 OpenClaw；
- 重启 OpenClaw 网关后；
- 用户报告“消息无法送达”；
- 定期进行健康检查（可添加到 HEARTBEAT.md 文件中）；
- 调试 BlueBubbles 与 OpenClaw 之间的连接问题。

## 功能介绍

该技能用于诊断并自动修复 BlueBubbles 与 OpenClaw 之间的 Webhook 连接问题。这是一种常见的故障情况：在网关重启后，BlueBubbles 可能会丢失其 Webhook 或进入等待状态（backoff 状态）。

**诊断检查内容：**
1. BlueBubbles 服务器是否可访问；
2. 是否已注册指向 OpenClaw 的 Webhook；
3. OpenClaw 网关端点是否响应；
4. 最近的 Webhook 发送活动记录。

**自动修复步骤：**
- 如果端点不可用，重启 OpenClaw 网关；
- 删除过期的 Webhook 并重新注册新的 Webhook；
- 修复问题后再次进行诊断。

## 使用方法

### 快速检查（仅用于查看结果）

```bash
BB_URL="http://127.0.0.1:1234" \
BB_PASSWORD="your-password" \
~/.openclaw/workspace/skills/bluebubbles-healthcheck/scripts/diagnose.sh
```

**输出解释：**
- 所有内容均为 ✅ 表示系统正常，无需采取任何操作；
- 出现 ❌ 时表示检测到问题，建议运行修复脚本 `heal.sh`。

### 自动修复

```bash
BB_URL="http://127.0.0.1:1234" \
BB_PASSWORD="your-password" \
~/.openclaw/workspace/skills/bluebubbles-healthcheck/scripts/heal.sh
```

该脚本将执行以下操作：
1. 进行诊断；
2. 查明问题所在；
3. 尝试解决问题（例如重启网关或重置 Webhook）；
4. 重新运行诊断以确认问题是否已解决。

### 干运行（查看修复过程）

```bash
BB_URL="http://127.0.0.1:1234" \
BB_PASSWORD="your-password" \
~/.openclaw/workspace/skills/bluebubbles-healthcheck/scripts/heal.sh --dry-run
```

## 环境变量

| 变量        | 是否必需 | 默认值       | 说明                          |
|-------------|---------|-------------|--------------------------------------|
| `BB_URL`     | 是       | `http://127.0.0.1:1234`     | BlueBubbles 服务器地址                |
| `BB_PASSWORD` | 是       | —                          | BlueBubbles API 密码                        |
| `OPENCLAW_WEBHOOK_URL` | 否       | `http://127.0.0.1:18789/bluebubbles-webhook` | OpenClaw Webhook 端点地址             |

您也可以通过命令行参数传递这些值：`--bb-url`, `--password`, `--webhook-url`。

## 代理决策流程

```
User reports iMessage issue
         ↓
    Run diagnose.sh
         ↓
    ┌────┴────┐
    │ All ✅? │
    └────┬────┘
    Yes  │  No
    ↓    │  ↓
 Report  │  Run heal.sh
 healthy │      ↓
         │  ┌───┴───┐
         │  │Fixed? │
         │  └───┬───┘
         │  Yes │ No
         │  ↓   │ ↓
         │Report│ Escalate to user:
         │fixed │ - BB app not running?
         │      │ - Network issue?
         └──────┴─ Manual intervention needed
```

## 常见故障模式及解决方法

### 故障模式 1：网关重启导致 Webhook 中断
**症状：** 在重启 OpenClaw 网关后，消息发送失败。
**解决方法：** 运行 `heal.sh` 脚本以重置 Webhook。

### 故障模式 2：BlueBubbles 处于等待状态（backoff）
**症状：** Webhook 存在，但 BlueBubbles 停止尝试发送消息。
**解决方法：** 运行 `heal.sh` 脚本删除并重新注册 Webhook，清除等待状态。

### 故障模式 3：网关未运行
**症状：** 第 3 步诊断失败（端口 18789 未监听）。
**解决方法：** 运行 `heal.sh` 脚本重启 OpenClaw 网关。

### 故障模式 4：BlueBubbles 应用程序未运行
**症状：** 第 1 步诊断失败（HTTP 响应码为 000）。
**解决方法：** 需要用户手动启动 BlueBubbles 应用程序。

## 相关文件

```
skills/bluebubbles-healthcheck/
├── SKILL.md           ← You are here
├── README.md          ← GitHub docs
└── scripts/
    ├── diagnose.sh    ← Read-only diagnostics (exit 0 = healthy)
    ├── heal.sh        ← Auto-heal orchestrator
    └── reset-webhook.sh ← Atomic webhook delete+re-register
```

## 安全注意事项

### 为什么 Webhook URL 包含密码？

`reset-webhook.sh` 脚本在注册 Webhook 时会包含密码：
```
http://127.0.0.1:18789/bluebubbles-webhook?password=...
```

这是 BlueBubbles 与 OpenClaw 之间的认证要求，并非故意泄露敏感信息。当 BlueBubbles 触发 Webhook 事件时，它会调用该 URL。OpenClaw 的 BB 插件通过 `?password=` 参数来验证回调请求的来源是否可信。当前 BlueBubbles 与 OpenClaw 的集成机制中不存在其他用于验证 Webhook 请求的认证方式。

**已采取的安全措施：**
- 两个服务均运行在 `127.0.0.1`（仅限本地访问，不会对外公开）；
- 脚本会在所有日志输出中屏蔽密码；
- Webhook URL 仅存储在 BlueBubbles 的本地配置文件中，不会被传输到外部。

**安装前需要注意的事项：**
- `BB_PASSWORD` 会保存在 BlueBubbles 的本地配置文件中；
- 仅在该服务在本地运行且可信任的环境中使用此技能；
- 确保 `BB_URL` 指向的是本地的 BlueBubbles 实例，而非远程服务器。

## 所需的二进制文件

| 文件名       | 使用工具        | 说明                          |
|-------------|-------------|--------------------------------------|
| `curl`      | 所有脚本        | 用于发送 HTTP 请求到 BlueBubbles API            |
| `python3`     | diagnose.sh, reset-webhook.sh | 用于解析 JSON 数据                   |
| `nc`       | diagnose.sh, heal.sh | 用于检查端口 18789 的连通性                |
| `openclaw`     | heal.sh       | 用于重启 OpenClaw 网关                    |

除 `openclaw` 外，这些工具在 macOS 上均为标准工具。由于该技能属于 OpenClaw 生态系统的一部分，因此需要确保系统中安装了 `openclaw` 命令行工具。

## 如何将此技能添加到定期健康检查流程中

要将此技能添加到定期健康检查流程中，请将其内容添加到 `HEARTBEAT.md` 文件中：

```markdown
## BlueBubbles Health
Every 4 hours, run the BlueBubbles healthcheck skill.
If any checks fail, run heal and report results.
```