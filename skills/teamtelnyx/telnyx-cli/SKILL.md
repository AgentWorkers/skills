---
name: telnyx-cli
description: "Telnyx API集成用于Clawdbot：支持发送短信/电子邮件/WhatsApp消息、管理电话号码、查询通话记录、调试Webhook以及访问您的Telnyx账户。当您需要通过命令行界面（CLI）与Telnyx API进行交互、管理电话号码和消息发送、调试Webhook或访问账户数据时，可以使用该功能。"
metadata:
  clawdbot:
    emoji: "📞"
    requires:
      bins: ["telnyx"]
      env: []
    notes: "API key stored in ~/.config/telnyx/config.json after 'telnyx auth setup'"
---
# Telnyx CLI

Telnyx CLI 是用于与 Clawdbot 集成的工具，支持消息发送、电话号码管理、Webhook 配置以及账户信息查询等功能。

## 设置

### 1. 安装 CLI

```bash
npm install -g @telnyx/api-cli
```

### 2. 配置 API 密钥

```bash
telnyx auth setup
```

请从以下链接复制并粘贴您的 API 密钥：  
https://portal.telnyx.com/#/app/api-keys  
该密钥将保存在 `~/.config/telnyx/config.json` 文件中（永久保存）。

### 3. 验证配置

```bash
telnyx number list
```

## 命令

| 类别 | 命令          | 描述                                      |
|------|--------------|-----------------------------------------|
| **消息发送** | `telnyx message send` | 发送 SMS、电子邮件或 WhatsApp 消息           |
|        | `telnyx message list` | 查看已发送的消息列表                         |
|        | `telnyx message get` | 获取消息的状态                         |
| **电话号码** | `telnyx number list` | 查看您的电话号码列表                         |
|        | `telnyx number search` | 搜索可用的电话号码                         |
|        | `telnyx number buy` | 购买新的电话号码                         |
|        | `telnyx number release` | 释放现有的电话号码                         |
| **通话记录** | `telnyx call list` | 查看通话记录                         |
|        | `telnyx call get` | 获取通话详情                         |
| **Webhook** | `telnyx webhook list` | 查看已配置的 Webhook 列表                         |
|        | `telnyx debugger list` | 查看 Webhook 事件                         |
|        | `telnyx debugger retry` | 重试失败的 Webhook 请求                         |
| **账户信息** | `telnyx account get` | 获取账户信息和余额                         |

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

### 批量消息发送

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

### 数据导出

```bash
# CSV export
telnyx call list --limit 1000 --output csv > calls.csv

# JSON export
telnyx number list --output json > numbers.json
```

## 提示

- 请求速率限制：每秒 100 次请求——批量操作时请添加 `sleep 1` 以控制频率。
- 使用 `--output json` 或 `--output csv` 参数更改输出格式。
- 获取帮助：`telnyx COMMAND --help`（例如：`telnyx message --help`）
- API 密钥存储位置：`~/.config/telnyx/config.json`

## 与 Clawdbot 的集成

```bash
# In cron jobs
0 9 * * * telnyx call list --limit 10 > /tmp/daily-calls.txt

# In heartbeat
telnyx debugger list --status failed

# In scripts
BALANCE=$(telnyx account get --output json | jq '.balance')
echo "Balance: $BALANCE"
```

## 相关技能

Telnyx CLI 是主要的接口工具。还有两个辅助技能可以处理与账户生命周期相关的操作：

| 技能        | 功能                        | 安装方式                                      |
|-------------|------------------|-----------------------------------------|
| **telnyx-bot-signup** | 创建新账户或登录现有账户（生成 API 密钥）       | `clawhub install telnyx-bot-signup`                   |
| **telnyx-freemium-upgrade** | 将免费账户升级为专业账户             | `clawhub install telnyx-freemium-upgrade`                   |

> **注意：** `telnyx-bot-signup` 支持注册和新用户登录。`bot Signup` 端点可以处理新用户和现有用户的注册请求，它会发送一个登录链接。整个流程相同：完成验证 → 发送登录链接 → 获取会话令牌 → 生成 API 密钥。

### 使用前的准备

在执行任何 Telnyx CLI 命令之前，请先检查以下内容：

```
1. Is `telnyx` CLI installed?
   NO  → npm install -g @telnyx/api-cli

2. Does ~/.config/telnyx/config.json exist with an api_key?
   NO  → Hand off to **telnyx-bot-signup** (see below)
         Works for both new AND existing accounts.

3. Does `telnyx account get` succeed?
   NO (401 auth error)  → API key is invalid/expired.
                           Hand off to **telnyx-bot-signup** to generate a fresh key.
   NO (network error)   → Check connectivity.
   YES                  → Proceed with the requested operation.
```

### 何时使用 `telnyx-bot-signup`？

在以下情况下，请使用 `telnyx-bot-signup` 技能：

- 不存在 API 密钥（`~/.config/telnyx/config.json` 文件缺失或为空，或者环境变量 `TELNYX_API_KEY` 未设置）；
- API 密钥存在，但 `telnyx account get` 命令返回 401 错误（密钥无效/过期/被吊销）；
- 用户表示丢失了 API 密钥或无法访问 Telnyx 网站；
- 用户希望创建新的 Telnyx 账户。

**无需询问用户是否已有账户。** `botSignup` 端点会自动处理这两种情况，只需请求用户的电子邮件地址即可。

**`telnyx-bot-signup` 的工作流程：**  
- 完成验证流程 → 发送登录链接 → 用户点击链接获取会话令牌 → 向 `/v2/api_keys` 发送 POST 请求以获取新的 API 密钥。该流程对新用户和现有用户都适用。

**注册/登录完成后：**

1. 保存返回的 API 密钥；
2. 将密钥保存到当前会话中；
3. 如果是新账户，系统会将其设置为免费账户级别。之后可以继续执行原始操作；如果遇到免费账户的限制，系统会自动触发升级流程。

### 何时使用 `telnyx-freemium-upgrade`？

当 CLI 命令因免费账户的限制而失败时，使用 `telnyx-freemium-upgrade` 技能：

| 错误代码            | 错误原因                          | 示例                                      |
|------------------|----------------------------------|-----------------------------------------|
| **Error 10039**     | 发送 SMS 失败（目标地址未验证）          | `telnyx message send --to +39... --text "test"`            |
| **Error D60**     | 发起语音通话失败（目标地址未验证）          | 尝试拨打未验证的号码                         |
| **Error 10038**     | 某些功能受限（免费账户无法使用）          | 如号码转接、短码服务、托管账户等                   |
| **号码数量限制**     | 无法购买新号码（免费账户最多只能拥有一个号码）       | 已经拥有一个号码                         |
| **无法充值**       | 账户余额不足或支付方式被拒绝                | 免费账户无法充值                         |
| **账户被停用**       | 账户因余额为零而被停用                     | `telnyx account get` 显示账户状态为停用                   |

**在用户明确表示需要升级时，也可以主动触发升级：**

| 用户需求                | 升级原因                                      |
|------------------|-----------------------------------------|
| “需要向 +39... 发送短信”       | 目标地址未验证（导致 Error 10039）                     |
| “希望将号码从 AT&T 转接过来”     | 免费账户限制了号码转接功能                     |
| “购买 5 个电话号码”       | 免费账户最多只能购买一个号码                     |
| “设置 SIP 中继”         | 免费账户限制了 SIP 功能                     |
| “创建托管账户”         | 免费账户无法创建托管账户                     |
| “为账户充值 50 美元”       | 免费账户无法充值                         |

**在升级之前，请检查是否已经尝试过升级：**

```
1. Read ~/.telnyx/upgrade.json (cache from the upgrade skill)

2. If decision == "APPROVED"
   → Account is already upgraded. Do NOT hand off.
     Retry the operation directly. If it still fails, the API key
     may need to be refreshed: telnyx auth setup

3. If decision == "REJECTED" and used_methods includes "github_oauth"
   → GitHub method exhausted. Do NOT hand off.
     Tell the user: "Your upgrade was not approved. Contact
     support at https://support.telnyx.com or try LinkedIn
     verification when available."

4. If decision == "PASS_TO_HUMAN"
   → Under manual review. Do NOT hand off.
     Tell the user: "Your upgrade is under review. I'll check
     back periodically." (The upgrade skill's cron job handles this.)

5. If no cache or status is "failed" / "polling_timeout"
   → Hand off to **telnyx-freemium-upgrade**.
```

**升级完成后：**

1. 重试之前导致升级的命令。
2. 如果重试仍然失败，请重新生成 API 密钥以获取专业账户的权限。可以使用 `telnyx-bot-signup` 功能（使用相同的电子邮件地址和登录流程）来生成新的密钥。

### 完整的生命周期流程

```
User: "Send SMS to +393406879636"
│
├── telnyx CLI installed? ──NO──→ npm install -g @telnyx/api-cli
│
├── API key configured? ──NO──→ **telnyx-bot-signup** (ask for email)
│                                 → PoW → magic link → API key
│                                 → Store key → continue
│
├── API key valid? (`telnyx account get`)
│   └── NO (401) → **telnyx-bot-signup** (ask for email)
│                   → PoW → magic link → fresh API key
│                   → Store key → continue
│
├── telnyx message send --from ... --to +39... --text "..."
│   │
│   ├── Success → Done
│   │
│   └── Error 10039 (destination not verified)
│       │
│       ├── Check upgrade cache (~/.telnyx/upgrade.json)
│       │   ├── APPROVED → Retry (key may need refresh)
│       │   ├── REJECTED → Inform user, suggest support
│       │   ├── PASS_TO_HUMAN → Inform user, wait for review
│       │   └── No cache / failed → Continue to upgrade
│       │
│       └── **telnyx-freemium-upgrade** → GitHub verification → poll
│           │
│           ├── APPROVED → retry SMS (key may need refresh via bot-signup)
│           ├── REJECTED → Inform user
│           └── PASS_TO_HUMAN → Cron job polls, notify on resolution
```

### 如果相关技能未安装

如果需要使用相关功能但相关技能未安装，请按照以下步骤操作：

- 如果缺少 `telnyx-bot-signup`：
  > 需要设置您的 Telnyx API 密钥。请安装 `clawhub install telnyx-bot-signup`。
  > 或者从 https://portal.telnyx.com/#/app/api-keys 获取 API 密钥，并使用 `telnyx auth setup` 进行配置。
- 如果缺少 `telnyx-freemium-upgrade`：
  > 您的账户处于免费账户级别，该功能不可用。请安装 `clawhub install telnyx-freemium-upgrade`。
  > 或者通过 https://portal.telnyx.com/#/account/account-levels/upgrade 手动升级账户。

---

## 故障排除

### CLI 未找到
```bash
npm install -g @telnyx/api-cli
```

### API 密钥未配置
```bash
# Reconfigure
telnyx auth setup

# Or check existing config
cat ~/.config/telnyx/config.json
```

### 连接问题
```bash
# Test connection
telnyx account get
```

## 参考资源

- Telnyx 官方文档：https://developers.telnyx.com
- Telnyx API 网站：https://portal.telnyx.com
- Telnyx CLI 项目：https://github.com/team-telnyx/telnyx-api-cli