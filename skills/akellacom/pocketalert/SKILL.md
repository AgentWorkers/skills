---
name: Pocket Alert – Push Notifications for iOS and Android
description: OpenClaw 的 Pocket Alert (pocketalert.app) 技能允许 OpenClaw 代理和工作流程向 iOS 和 Android 设备发送推送通知。该功能用于从自动化任务、工作流程以及后台进程中传递警报和更新信息。
---

# Pocket Alert

该技能允许通过其命令行工具（CLI）与 [Pocket Alert](https://pocketalert.app) 服务进行交互。

## 先决条件

必须安装并完成 `pocketalert` CLI 的身份验证：

```bash
# Install (if not already installed)
# Download from https://info.pocketalert.app/cli.html and extract to /usr/local/bin/

# Authenticate with your API key
pocketalert auth <your-api-key>
```

## 快速参考

### 发送推送通知

```bash
# Basic notification
pocketalert send -t "Title" -m "Message"

# Full form
pocketalert messages send --title "Alert" --message "Server is down!"

# To specific application
pocketalert messages send -t "Deploy" -m "Build completed" -a <app-tid>

# To specific device
pocketalert messages send -t "Alert" -m "Check server" -d <device-tid>

# To all devices
pocketalert messages send -t "Alert" -m "System update" -d all
```

### 列出资源

```bash
# List last messages
pocketalert messages list
pocketalert messages list --limit 50
pocketalert messages list --device <device-tid>

# List applications
pocketalert apps list

# List devices
pocketalert devices list

# List webhooks
pocketalert webhooks list

# List API keys
pocketalert apikeys list
```

### 管理应用程序

```bash
# Create application
pocketalert apps create --name "My App"
pocketalert apps create -n "Production" -c "#FF5733"

# Get application details
pocketalert apps get <tid>

# Delete application
pocketalert apps delete <tid>
```

### 管理设备

```bash
# List devices
pocketalert devices list

# Get device details
pocketalert devices get <tid>

# Delete device
pocketalert devices delete <tid>
```

### 管理 Webhook

```bash
# Create webhook
pocketalert webhooks create --name "GitHub Webhook" --message "*"
pocketalert webhooks create -n "Deploy Hook" -m "Deployed %repository.name% by %sender.login%"
pocketalert webhooks create -n "CI/CD" -m "*" -a <app-tid> -d all

# List webhooks
pocketalert webhooks list

# Get webhook details
pocketalert webhooks get <tid>

# Delete webhook
pocketalert webhooks delete <tid>
```

## 消息模板变量

在创建 Webhook 时，可以使用来自传入数据的模板变量：

```bash
pocketalert webhooks create \
  --name "GitHub Push" \
  --message "Push to %repository.name%: %head_commit.message%"
```

## 配置

查看或修改配置：

```bash
# View config
pocketalert config

# Set API key
pocketalert config set api_key <new-api-key>

# Set custom base URL (for self-hosted)
pocketalert config set base_url https://your-api.example.com
```

配置文件存储在 `~/.pocketalert/config.json` 中。

## CI/CD 集成示例

```bash
# GitHub Actions / GitLab CI
pocketalert send -t "Build Complete" -m "Version $VERSION deployed"

# Server monitoring with cron
*/5 * * * * /usr/local/bin/pocketalert send -t "Server Health" -m "$(uptime)"

# Service check script
if ! systemctl is-active --quiet nginx; then
  pocketalert send -t "NGINX Down" -m "NGINX is not running on $(hostname)"
fi
```

## 错误处理

CLI 会返回相应的退出代码：
- `0` - 成功
- `1` - 身份验证或 API 错误
- `2` - 参数无效

请始终检查命令输出以获取错误详细信息。