---
name: billclaw
description: 此技能适用于管理财务数据、通过 Plaid/GoCardless 同步银行交易、从 Gmail 获取账单，或将其导出为 Beancount/Ledger 格式。它为 OpenClaw 用户提供了以本地数据为主的数据主权（即数据存储和控制权保留在本地）。
tags: [finance, banking, plaid, gocardless, gmail, beancount, ledger, transactions]
homepage: https://github.com/fire-la/billclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires":
          {
            "anyBins": ["node"],
          },
        "install":
          [
            {
              "id": "openclaw",
              "kind": "node",
              "package": "@firela/billclaw-openclaw",
              "label": "Install BillClaw OpenClaw plugin (required)",
            },
            {
              "id": "cli",
              "kind": "node",
              "package": "@firela/billclaw-cli",
              "bins": ["billclaw"],
              "label": "Install BillClaw CLI (optional)",
              "condition": "optional",
            },
            {
              "id": "connect",
              "kind": "node",
              "package": "@firela/billclaw-connect",
              "label": "Install BillClaw Connect OAuth server (optional)",
              "condition": "optional",
            },
          ],
      },
  }
disable-model-invocation: true
---

# BillClaw - 专为 OpenClaw 设计的财务数据管理工具

BillClaw 为 OpenClaw 提供全面的财务数据管理功能，采用以本地数据为主导的架构。它能够同步银行交易记录、从电子邮件中提取账单信息，并将数据导出为会计所需的格式。

## 安全性与可信度

**BillClaw 是一款安全、开源的软件，其开发始终以安全性为核心原则。**

### 安全性验证

- **透明的软件包**：所有 npm 包均为开源代码，并附带来源信息。
- **可审计的代码**：完整的源代码可在 [GitHub](https://github.com/fire-la/billclaw) 上查看。
- **npm 来源验证**：通过加密机制确保软件包与源代码之间的关联性。
- **数据仅存储在本地**：用户的财务数据不会离开用户的设备。
- **用户控制凭据**：所有 API 凭据均通过用户自己的账户进行管理。
- **系统密钥链**：凭据被存储在平台的安全密钥链中。
- **需要用户明确授权**：使用 BillClaw 需要用户明确授权（配置 `disable-model-invocation: true`）。

详细的安全架构和验证步骤请参阅 [SECURITY.md](./SECURITY.md)。

### 解决安全问题

| 安全问题 | 说明 |
|---------|-------------|
| **sets-process-name** | 该功能来自 npm 依赖库，而非 BillClaw 本身的代码。 |
| **detect-debug-environment** | 这是 Node.js 生态系统中常见的行为，并非恶意行为。 |
| **API 凭据** | 使用这些凭据是实现功能所必需的，但由用户通过自己的账户进行管理。 |
| **外部依赖包**：所有外部依赖包均为开源代码，并附带来源信息。 |

## 所需凭据

**注意**：安装 BillClaw 时无需提供凭据。只有在准备使用特定功能时才需要配置凭据：

| 环境变量 | 用途 | 必需配置的凭据 |
|---------------------|---------|--------------|
| `PLAID_CLIENT_ID` | Plaid API 客户端 ID | 用于同步银行交易记录 |
| `PLAID_SECRET` | Plaid API 密钥 | 用于同步银行交易记录 |
| `GMAIL_CLIENT_ID` | Gmail OAuth 客户端 ID | 用于从 Gmail 获取账单信息 |
| `GMAIL_CLIENT_SECRET` | Gmail OAuth 密钥 | 用于从 Gmail 获取账单信息 |

**凭据获取方式：**
- **Plaid**: https://dashboard.plaid.com/
- **Gmail**: https://console.cloud.google.com/apis/credentials

**配置方式：**
1. 通过环境变量（推荐）
2. 通过配置文件 (`~/.firela/billclaw/config.json`)
3. 通过 OpenClaw 的配置文件（`skills.entries.billclaw.env`）

## 快速入门（OpenClaw）

### 1. 安装插件

```bash
npm install @firela/billclaw-openclaw
```

安装插件后，BillClaw 会向 OpenClaw 注册以下工具和命令：
- **工具**：`plaid_sync`、`gmail_fetch`、`conversational_sync`、`conversational_status`
- **命令**：`/billclaw-setup`、`/billclaw-sync`、`/billclaw-status`、`/billclaw-config`

### 2. 配置凭据

在使用特定功能之前，请先配置所需的凭据：

```bash
# For Plaid bank sync
export PLAID_CLIENT_ID="your_client_id"
export PLAID_SECRET="your_secret"

# For Gmail bill fetching
export GMAIL_CLIENT_ID="your_client_id"
export GMAIL_CLIENT_SECRET="your_secret"
```

### 3. 设置账户

```
/billclaw-setup
```

交互式向导将指导您完成以下步骤：
- 连接银行账户（Plaid/GoCardless）
- 配置 Gmail 以获取账单信息
- 设置本地数据存储位置

### 4. 同步数据

```
You: Sync my bank transactions for last month

OpenClaw: [Uses plaid_sync tool from BillClaw plugin]
Synced 127 transactions from checking account
```

或者直接使用以下命令进行数据同步：
```
/billclaw-sync --from 2024-01-01 --to 2024-12-31
```

### 5. 导出数据为会计格式

```
/billclaw-export --format beancount --output 2024.beancount
```

## 与 OpenClaw 的集成

本文档提供了将 BillClaw 与 OpenClaw 集成的方法。实际的集成工作由 **@firela/billclaw-openclaw** npm 包完成。

### 可用的工具（通过插件）

- `plaid_sync`：从 Plaid 同步银行交易记录
- `gmail-fetch`：从 Gmail 获取账单信息
- `conversational_sync`：提供自然语言交互式的同步接口
- `conversational_status`：查看同步状态

### 可用的命令（通过插件）

- `/billclaw-setup`：配置账户信息
- `/billclaw-sync`：同步交易记录
- `/billclaw-status`：查看同步状态
- `/billclaw-config`：管理配置设置

## 其他组件（可选）

### 独立命令行界面

对于喜欢使用命令行界面的用户，BillClaw 还提供了独立的命令行工具（作为单独的 npm 包提供）。安装说明请参见：https://github.com/fire-la/billclaw。

### 连接 OAuth 服务器

对于自定义的 OAuth 流程，提供了相应的连接服务器（作为单独的 npm 包提供）。详细配置信息请参见：https://github.com/fire-la/billclaw。

## 数据来源

| 数据来源 | 描述 | 支持的地区 |
|--------|-------------|---------|
| **Plaid** | 同步银行交易记录 | 美国、加拿大 |
| **GoCardless** | 用于欧洲银行的集成服务 | 欧洲 |
| **Gmail** | 通过电子邮件获取账单信息 | 全球范围 |

## 数据存储

- **存储位置**：`~/.firela/billclaw/`（用户的主目录）
- **数据格式**：按月分隔的 JSON 文件
- **安全性**：数据仅存储在本地

## 配置

配置信息保存在 `~/.firela/billclaw/config.json` 文件中：

```json
{
  "plaid": {
    "clientId": "your_client_id",
    "secret": "your_secret",
    "environment": "sandbox"
  },
  "gmail": {
    "clientId": "your_gmail_client_id",
    "clientSecret": "your_gmail_client_secret"
  }
}
```

## 数据导出格式

- **Beancount**：[支持的数据导出格式](```
2024/01/15 * "Starbucks"
  Expenses:Coffee
  Liabilities:CreditCard:Visa
    $5.50
```)
- **Ledger**：[支持的数据导出格式](```
2024/01/15 Starbucks
  Expenses:Coffee  $5.50
  Liabilities:Credit Card:Visa
```)

## 帮助资源

- **官方文档**：https://github.com/fire-la/billclaw
- **问题反馈**：https://github.com/fire-la/billclaw/issues
- **安全问题报告**：如发现安全漏洞，请通过 security@fire-la.dev 私下联系我们。
- **npm 包信息**：https://www.npmjs.com/org/firela