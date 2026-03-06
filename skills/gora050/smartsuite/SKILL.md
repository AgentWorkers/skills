---
name: smartsuite
description: >
  **Smartsuite集成：组织管理**  
  当用户需要与Smartsuite的数据进行交互时，请使用此功能。
compatibility: Requires network access and a valid Membrane account (Free tier supported).
license: MIT
homepage: https://getmembrane.com
repository: https://github.com/membranedev/application-skills
metadata:
  author: membrane
  version: "1.0"
  categories: "CRM, Sales"
---
# Smartsuite

Smartsuite 是一个工作管理平台，集成了项目管理、客户关系管理（CRM）和数据库功能。它被各种规模的团队用来组织工作流程、跟踪进度以及集中管理数据。

官方文档：https://developers.smartsuite.com/

## Smartsuite 概述

- **解决方案**  
  - **表格**  
    - **记录**  
      - **评论**  
- **视图**

**何时使用相应的操作**：根据需要使用操作名称和参数。

## 使用 Smartsuite

本技能使用 Membrane CLI 与 Smartsuite 进行交互。Membrane 会自动处理身份验证和凭证更新，因此您可以专注于集成逻辑，而无需关心身份验证的细节。

### 安装 CLI

请安装 Membrane CLI，以便在终端中运行 `membrane` 命令：

```bash
npm install -g @membranehq/cli
```

### 首次设置

```bash
membrane login --tenant
```

系统会打开一个浏览器窗口进行身份验证。

**无头环境**：运行该命令后，复制生成的 URL，让用户通过浏览器打开该链接，然后执行 `membrane login complete <code>` 完成登录。

### 连接到 Smartsuite

1. **创建新的连接**：
   ```bash
   membrane search smartsuite --elementType=connector --json
   ```
   从 `output.items[0].element?.id` 中获取连接器 ID，然后：
   ```bash
   membrane connect --connectorId=CONNECTOR_ID --json
   ```
   用户在浏览器中完成身份验证。输出中会显示新的连接 ID。

### 获取现有连接列表

如果您不确定连接是否已经存在：
1. **检查现有连接**：
   ```bash
   membrane connection list --json
   ```
   如果存在 Smartsuite 连接，请记录其 `connectionId`。

### 查找操作

当您知道想要执行的操作但不知道具体的操作 ID 时：
```bash
membrane action list --intent=QUERY --connectionId=CONNECTION_ID --json
```
这将返回包含操作 ID 和输入格式（inputSchema）的操作对象，从而帮助您了解如何执行该操作。

## 常用操作

| 名称 | 关键字 | 描述 |
| --- | --- | --- |
| 列出成员 | list-members | 列出工作空间成员（用户），支持可选过滤和分页 |
| 获取表格 | get-table | 根据 ID 获取表格（应用）的结构，包括字段定义 |
| 列出所有表格 | list-tables | 列出工作空间中的所有表格（应用） |
| 获取解决方案 | get-solution | 根据 ID 获取解决方案 |
| 列出所有解决方案 | list-solutions | 列出工作空间中的所有解决方案 |
| 删除记录 | delete-record | 从表格中删除记录 |
| 更新记录 | update-record | 更新表格中的现有记录（部分更新） |
| 创建记录 | create-record | 在表格中创建新记录 |
| 获取记录 | get-record | 根据 ID 从表格中检索单个记录 |
| 列出记录 | list-records | 列出表格中的记录，支持可选过滤、排序和分页 |

### 运行操作

```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json
```

**传递 JSON 参数**：

```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json --input "{ \"key\": \"value\" }"
```

### 代理请求

当现有操作无法满足您的需求时，您可以通过 Membrane 的代理直接发送请求到 Smartsuite API。Membrane 会自动在您提供的路径后添加基础 URL，并插入正确的身份验证头信息（包括在凭证过期时自动刷新凭证）。

```bash
membrane request CONNECTION_ID /path/to/endpoint
```

**常用选项**：

| 标志 | 描述 |
|------|-------------|
| `-X, --method` | HTTP 方法（GET、POST、PUT、PATCH、DELETE）。默认为 GET |
| `-H, --header` | 添加请求头（可重复使用），例如 `-H "Accept: application/json"` |
| `-d, --data` | 请求体（字符串） |
| `--json` | 用于发送 JSON 请求体并设置 `Content-Type: application/json` |
| `--rawData` | 以原始格式发送请求体，不进行任何处理 |
| `--query` | 查询字符串参数（可重复使用），例如 `--query "limit=10"` |
| `--pathParam` | 路径参数（可重复使用），例如 `--pathParam "id=123"` |

## 最佳实践

- **始终优先使用 Membrane 与外部应用进行交互**：Membrane 提供了预构建的操作，内置了身份验证、分页和错误处理功能，这样可以减少令牌消耗并提高通信安全性。
- **先探索再开发**：在编写自定义 API 调用之前，先运行 `membrane action list --intent=QUERY`（将 `QUERY` 替换为您的实际需求）来查找现有的操作。预构建的操作可以处理分页、字段映射以及原始 API 调用可能忽略的边缘情况。
- **让 Membrane 处理凭证**：切勿要求用户提供 API 密钥或令牌。请创建连接，Membrane 会在服务器端管理整个身份验证生命周期，无需存储任何本地密钥。