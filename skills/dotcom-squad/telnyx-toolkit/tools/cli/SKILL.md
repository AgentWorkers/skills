---
name: telnyx-cli
description: 通过 CLI（命令行界面）集成 Telnyx API。您可以发送 SMS/MMS/WhatsApp 消息、管理电话号码、查询通话记录、调试 Webhook 以及访问您的 Telnyx 账户。该工具适用于与 Telnyx API 进行交互、管理消息发送或访问账户数据等场景。
metadata: {"openclaw":{"emoji":"🔧","requires":{"bins":["telnyx"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx CLI

Telnyx 提供了与 OpenClaw 的 API 集成功能，支持消息发送、电话号码管理、Webhook 配置以及账户信息查询等操作。

## 设置

### 1. 安装 Telnyx CLI

```bash
npm install -g @telnyx/api-cli
```

### 2. 配置 API 密钥

```bash
telnyx auth setup
```

请将您的 API 密钥从以下链接复制并粘贴：
https://portal.telnyx.com/#/app/api-keys

配置文件将保存在 `~/.config/telnyx/config.json` 中（该文件会持久保存）。

### 3. 验证配置

```bash
telnyx number list
```

## 命令列表

| 类别 | 命令            | 描述                                      |
|--------|-----------------------------|-----------------------------------------|
| **消息发送** | `telnyx message send`    | 发送 SMS、电子邮件或 WhatsApp 消息                |
|        | `telnyx message list`    | 查看已发送的消息列表                          |
|        | `telnyx message get`    | 获取消息的状态                              |
| **电话号码** | `telnyx number list`    | 查看您的电话号码列表                          |
|        | `telnyx number search`    | 搜索可用的电话号码                          |
|        | `telnyx number buy`    | 购买电话号码                              |
|        | `telnyx number release`    | 释放已购买的电话号码                          |
| **通话记录** | `telnyx call list`    | 查看通话记录                              |
|        | `telnyx call get`    | 获取通话详细信息                          |
| **Webhook** | `telnyx webhook list`    | 查看已配置的 Webhook 列表                         |
|        | `telnyx debugger list`    | 查看 Webhook 事件日志                         |
|        | `telnyx debugger retry`    | 重试失败的 Webhook 请求                         |
| **账户信息** | `telnyx account get`    | 查看账户信息和余额                          |

## 使用方法

### 消息发送

```bash
# Send SMS
telnyx message send --from +15551234567 --to +15559876543 --text "Hello!"

# List messages
telnyx message list

# Get status
telnyx message get MESSAGE_ID
```

### 电话号码管理

```bash
# List
telnyx number list

# Search
telnyx number search --country US --npa 415

# Buy
telnyx number buy --number "+15551234567"

# Release
telnyx number release "+15551234567"
```

### Webhook 与调试

```bash
# List webhooks
telnyx webhook list

# View failed deliveries
telnyx debugger list --status failed

# Retry failed
telnyx debugger retry EVENT_ID
```

### 账户管理

```bash
# Account info
telnyx account get

# Check balance
telnyx account get --output json | jq '.balance'
```

## 输出格式

```bash
# Table (default)
telnyx number list

# JSON
telnyx number list --output json

# CSV
telnyx number list --output csv
```

## 示例

### 批量发送消息

```bash
#!/bin/bash
while read phone; do
  telnyx message send --from +15551234567 --to "$phone" --text "Hello!"
  sleep 1  # Rate limiting
done < recipients.txt
```

### 监控 Webhook 事件

```bash
#!/bin/bash
while true; do
  FAILED=$(telnyx debugger list --status failed --output json | jq '.data | length')
  [ "$FAILED" -gt 0 ] && echo "⚠️  $FAILED failed webhooks"
  sleep 300
done
```

### 导出数据

```bash
# CSV export
telnyx call list --limit 1000 --output csv > calls.csv

# JSON export
telnyx number list --output json > numbers.json
```

## 使用提示

- 请求速率限制：每秒 100 次请求——批量操作时请添加 `sleep 1` 以控制频率
- 使用 `--output json` 或 `--output csv` 参数更改输出格式
- 获取帮助：`telnyx COMMAND --help`（例如：`telnyx message --help`）
- API 密钥存储位置：`~/.config/telnyx/config.json`

## 与 OpenClaw 的集成

```bash
# In cron jobs
0 9 * * * telnyx call list --limit 10 > /tmp/daily-calls.txt

# In heartbeat
telnyx debugger list --status failed

# In scripts
BALANCE=$(telnyx account get --output json | jq '.balance')
echo "Balance: $BALANCE"
```

## 常见问题解决方法

- **CLI 未找到**：确保 Telnyx CLI 已正确安装并添加到系统路径中。
- **API 密钥未配置**：检查 `~/.config/telnyx/config.json` 文件中是否包含有效的 API 密钥。
- **连接问题**：检查网络连接是否正常，以及 Telnyx 服务器是否可用。

## 资源链接

- Telnyx 官方文档：https://developers.telnyx.com
- Telnyx API 门户：https://portal.telnyx.com
- Telnyx CLI 项目仓库：https://github.com/team-telnyx/telnyx-api-cli