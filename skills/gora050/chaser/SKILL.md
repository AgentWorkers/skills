---
name: chaser
description: >
  **Chaser集成：管理组织、用户和项目**  
  当用户需要与Chaser的数据进行交互时，可以使用此功能。
compatibility: Requires network access and a valid Membrane account (Free tier supported).
license: MIT
homepage: https://getmembrane.com
repository: https://github.com/membranedev/application-skills
metadata:
  author: membrane
  version: "1.0"
  categories: ""
---
# Chaser

Chaser 是一款销售流程管理和自动化工具，它帮助销售团队跟踪潜在客户（leads）、管理销售机会（deals），并自动化后续跟进（follow-ups）流程。该工具主要由销售人员和经理使用，旨在优化销售流程并促成更多交易。

**官方文档：** https://developer.chaser.io/

## Chaser 概述

- **Chase**：用于发送消息（Message）
- **Configuration**：用于配置系统设置（Configuration）
- **Notification**：用于设置通知机制（Notification）
- **User**：用于管理用户账户（User）

## 使用 Chaser

本技能通过 Membrane CLI 与 Chaser 进行交互。Membrane 负责处理身份验证和凭据刷新工作，因此您可以专注于集成逻辑，而无需担心身份验证的细节。

### 安装 Membrane CLI

请先安装 Membrane CLI，以便在终端中运行 `membrane` 命令：

```bash
npm install -g @membranehq/cli
```

### 首次设置

首次使用 Chaser 时，系统会弹出一个浏览器窗口进行身份验证。在无头环境（headless environment）中，运行相应命令后，复制浏览器中显示的 URL，然后使用 `membrane login complete <code>` 完成登录流程。

### 连接到 Chaser

1. **创建新连接：**
   ```bash
   membrane search chaser --elementType=connector --json
   ```
   从 `output.items[0].element?.id` 中获取连接器 ID（connector ID），然后执行后续操作：
   ```bash
   membrane connect --connectorId=CONNECTOR_ID --json
   ```
   用户在浏览器中完成身份验证，系统会返回新的连接 ID。

### 查看现有连接列表

如果您不确定某个连接是否存在，可以执行以下操作：
1. **检查现有连接：**
   ```bash
   membrane connection list --json
   ```
   如果存在 Chaser 连接，请记录其 `connectionId`。

### 查找所需操作

当您知道想要执行的操作类型，但不知道具体的操作 ID 时，可以执行以下命令：
```bash
membrane action list --intent=QUERY --connectionId=CONNECTION_ID --json
```
该命令会返回包含操作 ID 和输入参数格式（inputSchema）的操作对象，从而帮助您了解如何执行该操作。

## 常用操作

| 操作名称 | 键（Key） | 描述（Description） |
|---|---|---|
| 列出组织（List Organisations） | list-organisations | 无描述 |
| 列出联系人（List Contact Persons） | list-contact-persons | 无描述 |
| 列出超额付款（List Overpayments） | list-overpayments | 无描述 |
| 列出贷项通知（List Credit Notes） | list-credit-notes | 无描述 |
| 列出发票（List Invoices） | list-invoices | 无描述 |
| 列出客户（List Customers） | list-customers | 无描述 |
| 获取当前组织信息（Get Current Organisation） | get-current-organisation | 无描述 |
| 获取联系人信息（Get Contact Person） | get-contact-person | 无描述 |
| 获取超额付款信息（Get Overpayment） | get-overpayment | 无描述 |
| 获取贷项通知信息（Get Credit Note） | get-credit-note | 无描述 |
| 获取发票信息（Get Invoice） | get-invoice | 无描述 |
| 创建联系人（Create Contact Person） | create-contact-person | 无描述 |
| 创建超额付款记录（Create Overpayment） | create-overpayment | 无描述 |
| 创建贷项通知（Create Credit Note） | create-credit-note | 无描述 |
| 创建发票（Create Invoice） | create-invoice | 无描述 |
| 创建客户（Create Customer） | create-customer | 无描述 |
| 更新联系人信息（Update Contact Person） | update-contact-person | 无描述 |
| 更新超额付款记录（Update Overpayment） | update-overpayment | 无描述 |
| 更新贷项通知（Update Credit Note） | update-credit-note | 无描述 |
| 更新发票（Update Invoice） | update-invoice | 无描述 |
| 更新客户信息（Update Customer） | update-customer | 无描述 |
| 删除联系人（Delete Contact Person） | delete-contact-person | 无描述 |

### 执行操作

要传递 JSON 参数，请执行以下命令：
```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json --input "{ \"key\": \"value\" }"
```

### 通过代理发送请求

如果内置操作无法满足您的需求，您可以通过 Membrane 的代理直接发送请求到 Chaser API。Membrane 会自动在请求路径中添加基础 URL，并添加正确的身份验证头信息；如果凭据过期，系统会自动刷新凭据。

```bash
membrane request CONNECTION_ID /path/to/endpoint
```

**常用选项：**

| 选项 | 描述 |
|------|-------------|
| `-X, --method` | HTTP 方法（GET、POST、PUT、PATCH、DELETE，默认为 GET） |
| `-H, --header` | 添加请求头（可重复使用），例如 `-H "Accept: application/json"` |
| `-d, --data` | 请求体（字符串格式） |
| `--json` | 以 JSON 格式发送请求体，并自动设置 `Content-Type: application/json` |
| `--rawData` | 以原始格式发送请求体（不进行任何处理） |
| `--query` | 查询参数（可重复使用），例如 `--query "limit=10"` |
| `--pathParam` | 路径参数（可重复使用），例如 `--pathParam "id=123"` |

## 最佳实践：

- **优先使用 Membrane 与外部应用交互**：Membrane 提供了预构建的操作，支持身份验证、分页和错误处理功能，有助于减少令牌消耗并提高安全性。
- **先探索再开发**：在编写自定义 API 调用之前，先运行 `membrane action list --intent=QUERY`（将 `QUERY` 替换为实际需求）来查找现有的操作。预构建的操作能够处理分页、字段映射和边缘情况，而这些是原始 API 调用所无法处理的。
- **让 Membrane 管理凭据**：切勿要求用户提供 API 密钥或令牌。请通过 Membrane 创建连接，因为它会在服务器端管理整个身份验证生命周期，无需用户保存任何本地敏感信息。