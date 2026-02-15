---
name: monzo
description: **访问 Monzo 银行账户**  
- 查看余额  
- 查看交易记录  
- 管理资金  
- 发送交易通知  

适用于个人财务查询和银行自动化操作。
metadata: {"openclaw":{"emoji":"🏦","requires":{"env":["MONZO_KEYRING_PASSWORD"],"bins":["curl","jq","openssl","bc"]},"primaryEnv":"MONZO_KEYRING_PASSWORD"}}
---

# Monzo 银行业务技能

您可以使用此技能访问 Monzo 银行账户，查看余额、管理储蓄账户，并向 Monzo 应用程序发送通知。

## 先决条件

在设置此技能之前，您需要满足以下条件：

- **一个 Monzo 账户**（英国个人账户、联名账户或企业账户）
- 手机上安装了 Monzo 应用程序（用于 Strong Customer Authentication，SCA）
- OpenClaw 已安装并能够访问工作区
- 标准工具：`curl`、`jq`、`openssl`、`bc`（大多数 Linux 系统已预装）

## 快速入门（简而言之）

```bash
# 1. Set the MONZO_KEYRING_PASSWORD env var (see "Setting the Password" below)

# 2. Create OAuth client at https://developers.monzo.com/
#    - Set Confidentiality: Confidential
#    - Set Redirect URL: http://localhost

# 3. Run setup
scripts/setup.sh

# 4. Approve in Monzo app when prompted, then:
scripts/setup.sh --continue

# 5. Test it
scripts/balance.sh
```

---

## 详细设置指南

### 第 1 步：设置加密密码

`MONZO_KEYRING_PASSWORD` 环境变量用于在静态存储时加密您的 Monzo 凭据。请选择一个强大且唯一的密码，并确保不要丢失——如果您需要迁移或恢复此技能，将需要该密码。

有几种方法可以设置此变量。请选择适合您环境的方法：

**选项 A：OpenClaw 技能配置**（最简单）

在您的 OpenClaw 配置文件（例如 `openclaw.json`）中添加该密码：

```json5
{
  skills: {
    entries: {
      "monzo": {
        enabled: true,
        env: {
          "MONZO_KEYRING_PASSWORD": "choose-a-secure-password-here"
        }
      }
    }
  }
}
```

然后重启 OpenClaw：`openclaw gateway restart`

> **注意：** 这会将密码以明文形式存储在配置文件中。请确保文件具有严格的权限设置（`chmod 600`），并且不要将其提交到版本控制系统中。

**选项 B：Shell 环境变量**（将密码从配置文件中分离出来）

在您的 Shell 配置文件（`~/.bashrc`、`~/.zshrc` 等）中添加该密码：

```bash
export MONZO_KEYRING_PASSWORD="choose-a-secure-password-here"
```

然后重启 Shell 和 OpenClaw。

**选项 C：systemd 环境文件**（适用于服务器部署）

创建一个 secrets 文件（例如 `/etc/openclaw/monzo.env`）：

```
MONZO_KEYRING_PASSWORD=choose-a-secure-password-here
```

设置权限：`chmod 600 /etc/openclaw/monzo.env`

在 systemd 单元中引用该文件，使用 `EnvironmentFile=/etc/openclaw/monzo.env`。

**选项 D：密码管理器/secret 管理工具**

使用您喜欢的密码管理工具在运行时设置环境变量。任何能够在进程环境中设置 `MONZO_KEYRING_PASSWORD` 的方法都可以。

### 第 2 步：创建 Monzo OAuth 客户端

1. 访问 **https://developers.monzo.com/** 并使用您的 Monzo 账户登录
2. 点击 **“Clients”** → **“New OAuth Client”**
3. 填写以下信息：
   - **名称**：`OpenClaw`（或您喜欢的名称）
   - **Logo URL**：*留空*
   - **Redirect URLs**：`http://localhost`（必须精确输入，不要加斜杠）
   - **描述**：*留空*
   - **保密性**：**Confidential**（非常重要！启用刷新令牌）
4. 点击 **提交**
5. 记下您的 **客户端 ID**（`oauth2client_...`）和 **客户端密钥**（`mnzconf....`）

### 第 3 步：运行设置向导

```bash
scripts/setup.sh
```

向导将：
1. 请求您的客户端 ID 和客户端密钥
2. 提供一个授权 URL，让您在浏览器中打开
3. 要求您粘贴返回的 redirect URL
4. 交换代码以获取访问令牌
5. 保存加密后的凭据

**替代方案：非交互式模式**（适用于自动化或代理）：
```bash
scripts/setup.sh --non-interactive \
  --client-id oauth2client_xxx \
  --client-secret mnzconf.xxx \
  --auth-code eyJ...
```

### 第 4 步：在 Monzo 应用程序中批准（SCA）

⚠️ **此步骤是必需的！** Monzo 要求进行 Strong Customer Authentication（强客户身份验证）。

1. 打开手机上的 Monzo 应用程序
2. 查找关于“API 访问”的通知或新的连接请求
3. **点击批准**

如果您没有看到通知：
- 转到 **账户 → 设置 → 隐私与安全 → 管理已连接的应用程序**
- 找到并批准您的客户端

批准后，完成设置：
```bash
scripts/setup.sh --continue
```

### 第 5 步：验证功能是否正常

```bash
# Check authentication
scripts/whoami.sh

# Check your balance
scripts/balance.sh
```

您应该能够看到账户信息和当前余额。恭喜您！🎉

---

## 代理使用说明

本部分介绍了代理如何有效使用此技能。

### 何时使用此技能

当用户询问以下内容时，请使用此技能：
- **余额**：“我有多少钱？”、“我的余额是多少？”
- **交易记录**：“我在某项支出上花了多少钱？”、“显示最近的交易记录”
- **消费分析**：“我这个月花了多少钱在咖啡上？”
- **储蓄**：“我的储蓄账户里有多少钱？”、“将 £X 转到我的度假储蓄账户”
- **通知**：“向我的 Monzo 应用程序发送提醒”

### 常见使用场景

```bash
# "How much money do I have?"
scripts/balance.sh

# "Show me recent transactions" / "What did I spend?"
scripts/transactions.sh              # All available, newest first

# "Show me my last 5 transactions"
scripts/transactions.sh --limit 5    # 5 most recent

# "What did I spend this week?"
scripts/transactions.sh --since 7d

# "How much did I spend on coffee this month?"
scripts/transactions.sh --search coffee --since 30d

# "What are my savings pots?"
scripts/pots.sh

# "Put £50 in my holiday fund"
scripts/pots.sh deposit pot_XXXXX 5000  # Amount in pence!

# "Send a reminder to my phone"
scripts/feed.sh --title "Don't forget!" --body "Check the gas meter"
```

### 代理需要注意的事项

1. **金额单位为便士**：£50 = 5000，£1.50 = 150
2. **日期可以是相对的**：`--since 7d` 表示过去 7 天
3. **默认输出为人类可读格式**（不使用 `--json` 标志）
4. **储蓄账户 ID**：在存款/取款之前，请先使用 `scripts/pots.sh` 获取账户 ID
5. **多个账户**：用户可能拥有个人账户、联名账户和企业账户。默认使用个人账户。可以使用 `scripts/whoami.sh` 查看所有账户。

### 错误处理

- 如果出现 `forbidden.insufficient_permissions` 错误：
  - 告知用户检查他们的 Monzo 应用程序并批准 API 访问权限。
  - 然后运行 `scripts/setup.sh --continue`。

- 如果出现 `MONZO_KEYRING_PASSWORD not set` 错误：
  - 进程环境中没有该环境变量。
  - 指导用户按照设置指南中的第 1 步设置它。

---

## 脚本参考

### balance - 查看账户余额

```bash
scripts/balance.sh                 # Default account
scripts/balance.sh acc_...         # Specific account
scripts/balance.sh --json          # JSON output
```

**输出：**
```
Current Balance: £1,234.56
Total (with pots): £2,500.00
Spent today: £12.34
```

### transactions - 查看交易记录

获取 **所有可用的交易记录**（分页显示），最新的交易记录排在最前面。

```bash
scripts/transactions.sh                         # All transactions, newest first
scripts/transactions.sh --limit 10              # 10 most recent
scripts/transactions.sh --since 7d              # Last 7 days only
scripts/transactions.sh --since 2026-01-01      # Since specific date
scripts/transactions.sh --search coffee         # Search by merchant/description/notes
scripts/transactions.sh --search "Pret" --since 30d  # Combined filters
scripts/transactions.sh --id tx_...             # Get specific transaction
scripts/transactions.sh --json                  # JSON output
```

**输出：**
```
DATE         AMOUNT     DESCRIPTION                          CATEGORY
============ ========== =================================== ===============
2026-01-29  -£3.50     Pret A Manger                       eating_out
2026-01-29  -£12.00    TfL                                 transport
2026-01-28  -£45.23    Tesco                               groceries

Total: 3 transaction(s)
```

### pots - 管理储蓄账户

```bash
scripts/pots.sh                              # List all pots
scripts/pots.sh list --json                  # JSON output
scripts/pots.sh deposit pot_... 5000         # Deposit £50 (5000 pence)
scripts/pots.sh withdraw pot_... 2000        # Withdraw £20 (2000 pence)
```

**输出（列表格式）：**
```
NAME                      BALANCE      GOAL         ID
========================= ============ ============ ====================
Holiday Fund              £450.00      £1,000.00    pot_0000...
Emergency                 £2,000.00    £3,000.00    pot_0001...
```

### feed - 向应用程序发送通知

```bash
scripts/feed.sh --title "Reminder"                        # Simple notification
scripts/feed.sh --title "Alert" --body "Details here"    # With body
scripts/feed.sh --title "Link" --url "https://..."       # With tap action
```

### whoami - 检查认证状态

```bash
scripts/whoami.sh                  # Show auth status and accounts
scripts/whoami.sh --account-id     # Just the default account ID
scripts/whoami.sh --json           # JSON output
```

### receipt - 为交易附上收据

```bash
scripts/receipt.sh create tx_... --merchant "Shop" --total 1234 --item "Thing:1234"
scripts/receipt.sh get ext_...
scripts/receipt.sh delete ext_...
```

### webhooks - 管理 Webhook（高级功能）

```bash
scripts/webhooks.sh list
scripts/webhooks.sh create https://your-server.com/webhook
scripts/webhooks.sh delete webhook_...
```

---

## 故障排除

### “forbidden.insufficient_permissions”

**最常见的问题！** Monzo 要求应用进行 Strong Customer Authentication（SCA）。

**解决方法：**
1. 打开 Monzo 应用程序 → 检查通知 → 批准权限。
2. 或者：进入 **账户 → 设置 → 隐私与安全 → 管理已连接的应用程序** 并批准权限。
3. 运行：`scripts/setup.sh --continue`。

### “MONZO_KEYRING_PASSWORD not set”

环境变量在进程环境中不可用。

**解决方法：** 使用设置指南中的任意方法设置 `MONZO_KEYRING_PASSWORD`，然后重启 OpenClaw。

### “Authorization code has been used”

每个授权代码仅使用一次。请重新创建客户端：

```bash
scripts/setup.sh --reset
```

### “No refresh token received”

您的 OAuth 客户端未设置为“Confidential”模式。请创建一个新的客户端，并将保密性设置为 “Confidential”，然后重新尝试：

```bash
scripts/setup.sh --reset
```

### “Credentials file not found”

请先运行设置脚本：

```bash
scripts/setup.sh
```

### “Failed to decrypt credentials”

`MONZO_KEYRING_PASSWORD` 设置错误。请检查您的配置文件是否与设置时使用的密码一致。

---

## 安全注意事项

- 凭据在静态存储时被加密（使用 AES-256-CBC 算法）
- 加密密钥是您的 `MONZO_KEYRING_PASSWORD`
- 访问令牌会自动刷新（无需手动操作）
- 文件权限设置为 600（仅允许所有者访问）
- 所有 API 调用都使用 HTTPS 协议
- 不会记录任何敏感数据

---

## 相关文件

**凭据文件：** `~/.openclaw/credentials/monzo.json`（已加密；旧版本中位于 `~/.clawdbot/credentials/monzo.json`）

---

## API 覆盖范围

| 功能 | 使用的脚本 |
|---------|---------|
| 认证 | setup, whoami |
| 余额 | balance |
| 交易记录 | transactions |
| 储蓄账户 | pots |
| 通知发送 | feed |
| 收据管理 | receipt |
| Webhook 管理 | webhooks |