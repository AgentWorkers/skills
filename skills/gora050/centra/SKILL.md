---
name: centra
description: Centra集成功能：支持管理组织（Organizations）、项目（Projects）、流水线（Pipelines）、用户（Users）、目标（Goals）以及各种过滤器（Filters）。当用户需要与Centra的数据进行交互时，可以使用此功能。
compatibility: Requires network access and a valid Membrane account (Free tier supported).
license: MIT
homepage: https://getmembrane.com
repository: https://github.com/membranedev/application-skills
metadata:
  author: membrane
  version: "1.0"
  categories: ""
---
# Centra

Centra 是一个专为面向消费者的时尚和生活方式品牌设计的平台。它提供了电子商务、批发和零售管理的工具，帮助品牌简化运营流程并提升客户体验。

官方文档：https://developer.centra.com/

## Centra 概述

- **产品**  
  - **产品变体**  
- **订单**  
- **Webhook**

根据需要使用相应的操作名称和参数。

## 使用 Centra

本技能使用 Membrane CLI 与 Centra 进行交互。Membrane 会自动处理身份验证和凭证更新，因此您可以专注于集成逻辑，而无需关注身份验证的细节。

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

**无头环境（Headless environments）：** 运行该命令，复制生成的 URL 并在浏览器中打开，然后执行 `membrane login complete <code>` 完成登录。

### 连接 Centra

1. **创建新连接：**
   ```bash
   membrane search centra --elementType=connector --json
   ```
   从 `output.items[0].element?.id` 中获取连接器 ID，然后：
   ```bash
   membrane connect --connectorId=CONNECTOR_ID --json
   ```
   用户在浏览器中完成身份验证。输出中会包含新的连接 ID。

### 查看现有连接列表

当不确定连接是否存在时：
1. **检查现有连接：**
   ```bash
   membrane connection list --json
   ```
   如果存在 Centra 连接，请记录其 `connectionId`。

### 查找操作

当您知道需要执行的操作类型但不知道具体的操作 ID 时：
```bash
membrane action list --intent=QUERY --connectionId=CONNECTION_ID --json
```
这会返回包含操作 ID 和输入格式（inputSchema）的操作对象，从而帮助您了解如何执行该操作。

## 常用操作

| 操作名称 | 关键参数 | 描述 |
| --- | --- | --- |
| 取消订单 | cancel-order | 在 Centra 中取消 DTC（Direct to Consumer）订单 |
| 列出文件夹 | list-folders | 列出用于产品管理的所有文件夹 |
| 列出系列 | list-collections | 列出 Centra 中的所有系列（季节） |
| 创建产品变体 | create-product-variant | 为现有产品创建新的变体 |
| 列出仓库 | list-warehouses | 列出 Centra 中的所有仓库 |
| 列出市场 | list-markets | 列出 Centra 中的所有市场 |
| 列出店铺 | list-stores | 列出 Centra 中配置的所有店铺 |
| 列出类别 | list-categories | 列出 Centra 中的所有类别 |
| 创建品牌 | create-brand | 在 Centra 中创建新品牌 |
| 列出品牌 | list-brands | 列出 Centra 中的所有品牌 |
| 更新客户信息 | update-customer | 更新 Centra 中的现有客户信息 |
| 创建客户 | create-customer | 在 Centra 中创建新客户 |
| 获取客户信息 | get-customer | 通过 ID 获取客户的完整信息 |
| 列出客户 | list-customers | 列出 Centra 中的所有客户 |
| 获取订单信息 | get-order | 通过 ID 获取订单的完整信息 |
| 列出订单 | list-orders | 列出 Centra 中的所有订单（DTC 类型） |
| 更新产品信息 | update-product | 更新 Centra 中的现有产品信息 |
| 创建产品 | create-product | 在 Centra 中创建新产品 |
| 获取产品信息 | get-product | 通过 ID 获取产品的完整信息 |
| 列出产品 | list-products | 列出 Centra 中的产品（支持可选过滤条件） |

### 执行操作

```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json
```

要传递 JSON 参数，请使用以下方式：

```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json --input "{ \"key\": \"value\" }"
```

### 代理请求

如果可用操作无法满足您的需求，您可以通过 Membrane 的代理直接向 Centra API 发送请求。Membrane 会自动在您提供的路径后添加基础 URL，并插入正确的身份验证头信息；如果凭证过期，系统会自动进行刷新。

```bash
membrane request CONNECTION_ID /path/to/endpoint
```

常用选项：

| 选项 | 描述 |
|------|-------------|
| `-X, --method` | HTTP 方法（GET、POST、PUT、PATCH、DELETE）。默认为 GET |
| `-H, --header` | 添加请求头（可重复使用），例如 `-H "Accept: application/json"` |
| `-d, --data` | 请求体（字符串形式） |
| `--json` | 以 JSON 格式发送请求体，并设置 `Content-Type: application/json` |
| `--rawData` | 以原始格式发送请求体，不进行任何处理 |
| `--query` | 查询参数（可重复使用），例如 `--query "limit=10"` |
| `--pathParam` | 路径参数（可重复使用），例如 `--pathParam "id=123"` |

## 最佳实践

- **始终优先使用 Membrane 与外部应用进行交互**：Membrane 提供了预构建的操作，具备内置的身份验证、分页和错误处理功能，这样可以减少令牌消耗并提高通信安全性。
- **先探索再开发**：在编写自定义 API 调用之前，运行 `membrane action list --intent=QUERY`（将 `QUERY` 替换为您的实际需求）来查找现有的操作。预构建的操作能够处理分页、字段映射以及原始 API 调用可能遗漏的特殊情况。
- **让 Membrane 处理凭证**：切勿要求用户提供 API 密钥或令牌。请创建连接，Membrane 会在服务器端管理整个身份验证流程，无需用户保存任何本地敏感信息。