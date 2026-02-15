---
name: billclaw
description: 此技能适用于管理财务数据、通过 Plaid/GoCardless 同步银行交易、从 Gmail 获取账单，或将其导出为 Beancount/Ledger 格式。它为 OpenClaw 用户提供了数据主权（即数据存储和控制权优先在本地）。
tags: [finance, banking, plaid, gocardless, gmail, beancount, ledger, transactions]
homepage: https://github.com/fire-la/billclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires":
          {
            "env": ["PLAID_CLIENT_ID", "PLAID_SECRET", "GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET"],
            "anyBins": ["node"],
          },
        "primaryEnv": "PLAID_CLIENT_ID",
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

BillClaw 为 OpenClaw 提供全面的财务数据管理功能，采用以本地数据为主导的架构，支持同步银行交易、从电子邮件中提取账单，并将数据导出为会计所需的格式。

## 安全保障

**BillClaw 是一款安全、开源的软件，其开发始终以安全为核心原则：**

- **透明的软件包**：本工具提供了详细的安装说明。所有引用的 npm 包（`@firela/billclaw-openclaw`、`@firela/billclaw-cli`、`@firela/billclaw-connect`）均独立发布、经过验证，并可在 npmjs.com 上供您查看。
- **以本地数据为主导的架构**：您的财务数据不会离开您的设备；所有交易数据均存储在 `~/.billclaw/` 目录下。
- **透明的认证信息**：您需要自行提供并控制所有 API 认证信息（Plaid、Gmail），并通过自己的账户进行管理。
- **系统密钥链存储**：敏感的认证信息会加密存储在您平台的密钥链中。
- **需要用户明确授权**：使用 BillClaw 需要用户明确发起请求（配置 `disable-model-invocation: true`）。
- **完全可审计**：所有源代码均公开发布在 https://github.com/fire-la/billclaw，遵循 MIT 许可协议。

**软件包概述：**
- `@firela/billclaw-openclaw` - **必备**：作为 OpenClaw 的插件，提供所需的工具和命令。
- `@firela/billclaw-cli` - **可选**：独立的命令行工具（CLI），适用于终端使用。
- `@firela/billclaw-connect` - **可选**：用于实现自定义 OAuth 认证的服务器。

## 所需的认证信息

使用 BillClaw 需要以下认证信息（可通过环境变量或 `~/.billclaw/config.json` 进行配置）：

| 环境变量 | 用途 | 必需项 |
|---------------------|---------|--------------|
| `PLAID_CLIENT_ID` | Plaid API 客户端 ID | 同步银行交易所需 |
| `PLAID_SECRET` | Plaid API 密钥 | 同步银行交易所需 |
| `GMAIL_CLIENT_ID` | Gmail OAuth 客户端 ID | 提取账单所需 |
| `GMAIL_CLIENT_SECRET` | Gmail OAuth 密钥 | 提取账单所需 |

**重要提示**：这些认证信息由您自行获取，可从以下平台获取：
- **Plaid**：https://dashboard.plaid.com/
- **Gmail**：https://console.cloud.google.com/apis/credentials

## 快速入门（OpenClaw）

### 先决条件

在使用 BillClaw 之前，您需要为所需的服务配置相应的认证信息：

| 服务 | 所需认证信息 |
|---------|---------------------|
| **Plaid** | PLAID_CLIENT_ID, PLAID_SECRET |
| **Gmail** | GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET |

这些认证信息可以通过以下方式配置：
1. 环境变量（推荐）
2. 配置文件（`~/.billclaw/config.json`）
3. OpenClaw 的配置文件（`skills.entries.billclaw.env`）

### 安装

通过 npm 安装 BillClaw 插件：

```bash
npm install @firela/billclaw-openclaw
```

该插件会向 OpenClaw 注册以下工具和命令：
- **工具**：`plaid_sync`、`gmail_fetch`、`conversational_sync`、`conversational_status`
- **命令**：`/billclaw-setup`、`/billclaw-sync`、`/billclaw-status`、`/billclaw-config`

### 1. 设置您的账户

```
/billclaw-setup
```

交互式向导将引导您完成以下步骤：
- 连接银行账户（Plaid/GoCardless）
- 配置 Gmail 以提取账单
- 设置本地数据存储位置

### 2. 同步数据

```
You: Sync my bank transactions for last month

OpenClaw: [Uses plaid_sync tool from BillClaw plugin]
Synced 127 transactions from checking account
```

或者直接使用相应的命令进行数据同步：

```
/billclaw-sync --from 2024-01-01 --to 2024-12-31
```

### 3. 导出数据为会计格式

```
/billclaw-export --format beancount --output 2024.beancount
```

## 与 OpenClaw 的集成

本文档提供了将 BillClaw 与 OpenClaw 集成的方法。具体的集成细节由 `@firela/billclaw-openclaw` npm 包提供。

### 可用的工具（通过插件）

- `plaid_sync`：从 Plaid 同步银行交易数据。
- `gmail_fetch`：从 Gmail 提取账单信息。
- `conversational_sync`：提供自然语言交互式的同步接口。
- `conversational_status`：查询同步状态。

### 可用的命令（通过插件）

- `/billclaw-setup`：配置账户信息。
- `/billclaw-sync`：同步交易数据。
- `/billclaw-status`：查看同步状态。
- `/billclaw-config`：管理配置设置。

## 其他组件（可选）

- **独立命令行界面**：对于偏好使用命令行界面的用户，提供了独立的 CLI 工具（作为单独的 npm 包提供）。安装说明请参见 https://github.com/fire-la/billclaw。
- **OAuth 服务器**：如果您需要自定义 OAuth 流程，提供了相应的服务器插件（作为单独的 npm 包提供）。详细配置信息请参见 https://github.com/fire-la/billclaw。

## 数据来源

| 数据来源 | 描述 | 支持的地区 |
|--------|-------------|---------|
| **Plaid** | 银行交易同步 | 美国、加拿大 |
| **GoCardless** | 欧洲银行数据集成 | 欧洲地区 |
| **Gmail** | 通过电子邮件提取账单 | 全球范围 |

## 数据存储

- **存储位置**：`~/.billclaw/`（您的主目录）
- **数据格式**：JSON 文件，按月分区存储
- **安全性**：数据仅存储在本地。

## 配置设置

配置信息保存在 `~/.billclaw/config.json` 文件中：

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

- **Beancount**：[支持的数据导出格式]
- **Ledger**：[支持的数据导出格式]

## 常见问题与帮助资源

- **文档**：https://github.com/fire-la/billclaw
- **问题反馈**：https://github.com/fire-la/billclaw/issues
- **安全问题**：如发现安全漏洞，请通过 security@fire-la.dev 私下联系我们。
- **npm 包**：https://www.npmjs.com/org/firela