---
name: mews
description: Mews集成功能：支持管理客户、空间、产品、价格、预订、支付等数据。当用户需要与Mews系统进行数据交互时，可以使用该功能。
compatibility: Requires network access and a valid Membrane account (Free tier supported).
license: MIT
homepage: https://getmembrane.com
repository: https://github.com/membranedev/application-skills
metadata:
  author: membrane
  version: "1.0"
  categories: ""
---
# Mews

Mews 是一个物业管理系统（Property Management System, PMS），被酒店和青年旅社用于管理预订、客户服务以及日常运营。它有助于简化预订、入住/退房和支付等流程。

官方文档：https://developers.mews.com/

## Mews 概述

- **客户**  
  - **客户标识符**  
- **可用房间**  
- **房间类型**  
- **产品信息**  
- **预订信息**  
  - **预订标识符**  
- **支付信息**  
- **账单**  
- **账户信息**  
- **公司信息**  
- **房价信息**  
- **资源信息**  
- **付款人信息**  
- **文章/资料**  
- **外部服务**  
- **任务信息**  
- **市场信息**  
- **旅行社信息**  
- **用户信息**  
- **设备信息**  
- **邮政编码**  

根据需要使用相应的操作名称和参数。

## 使用 Mews

本技能使用 Membrane CLI 与 Mews 进行交互。Membrane 会自动处理身份验证和凭证更新，因此您可以专注于集成逻辑，而无需关注身份验证的细节。

### 安装 CLI

安装 Membrane CLI，以便在终端中运行 `membrane` 命令：

```bash
npm install -g @membranehq/cli
```

### 首次设置

```bash
membrane login --tenant
```

系统会打开一个浏览器窗口进行身份验证。

**无头环境（Headless environments）：** 运行该命令后，复制生成的 URL，让用户通过浏览器打开该链接，然后执行 `membrane login complete <code>` 完成登录。

### 连接 Mews

1. **创建新的连接：**
   ```bash
   membrane search mews --elementType=connector --json
   ```  
   从 `output.items[0].element?.id` 中获取连接器 ID，然后：  
   ```bash
   membrane connect --connectorId=CONNECTOR_ID --json
   ```  
   用户在浏览器中完成身份验证。输出中会包含新的连接 ID。

### 获取现有连接列表

如果您不确定连接是否已经存在：  
1. **检查现有连接：**
   ```bash
   membrane connection list --json
   ```  
   如果存在 Mews 连接，请记录其 `connectionId`。

### 查找操作

当您知道想要执行的操作但不知道具体的操作 ID 时：  
```bash
membrane action list --intent=QUERY --connectionId=CONNECTION_ID --json
```  
此命令会返回包含操作 ID 和输入格式（inputSchema）的操作对象，从而帮助您了解如何执行该操作。

## 常用操作

使用 `npx @membranehq/cli@latest action list --intent=QUERY --connectionId=CONNECTION_ID --json` 命令来查看可用的操作。

### 执行操作

```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json
```

### 传递 JSON 参数

```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json --input "{ \"key\": \"value\" }"
```

### 代理请求

当可用操作无法满足您的需求时，您可以通过 Membrane 的代理直接发送请求到 Mews API。Membrane 会自动在您提供的路径前加上基础 URL，并添加正确的身份验证头信息（包括在凭证过期时自动刷新凭证的功能）。

```bash
membrane request CONNECTION_ID /path/to/endpoint
```

**常用参数：**

| 参数 | 说明 |
|------|-------------|
| `-X, --method` | HTTP 方法（GET、POST、PUT、PATCH、DELETE）。默认为 GET |
| `-H, --header` | 添加请求头（可重复使用），例如 `-H "Accept: application/json"` |
| `-d, --data` | 请求体（字符串形式） |
| `--json` | 以 JSON 格式发送请求体，并设置 `Content-Type: application/json` |
| `--rawData` | 以原始形式发送请求体，不进行任何处理 |
| `--query` | 查询参数（可重复使用），例如 `--query "limit=10"` |
| `--pathParam` | 路径参数（可重复使用），例如 `--pathParam "id=123"` |

## 最佳实践：

- **优先使用 Membrane 与外部应用进行通信**：Membrane 提供了预构建的操作，具备内置的身份验证、分页和错误处理功能，这样可以减少令牌消耗并提高通信安全性。  
- **先探索再开发**：在编写自定义 API 调用之前，先运行 `membrane action list --intent=QUERY`（将 `QUERY` 替换为实际需求）来查找可用的操作。预构建的操作可以处理分页、字段映射和原始 API 调用可能遗漏的边缘情况。  
- **让 Membrane 处理凭证**：切勿要求用户提供 API 密钥或令牌。请创建连接，由 Membrane 在服务器端管理整个身份验证生命周期，无需保存任何本地敏感信息。