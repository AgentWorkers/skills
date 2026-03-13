---
name: backlog
description: **待办事项集成（Backlog Integration）**：用于管理项目。当用户需要与待办事项（Backlog）数据交互时可以使用该功能。
compatibility: Requires network access and a valid Membrane account (Free tier supported).
license: MIT
homepage: https://getmembrane.com
repository: https://github.com/membranedev/application-skills
metadata:
  author: membrane
  version: "1.0"
  categories: ""
---
# Backlog

Backlog 是一个项目与任务管理工具，开发团队使用它来跟踪问题（bug）、管理代码以及协作完成项目。

**官方文档：** https://developer.backlog.com/

## Backlog 概述

- **Backlog 界面**  
  - **项目（Project）**  
    - **问题（Issue）**  
      - **评论（Comment）**  
- **用户（User）**  

根据需要使用相应的操作名称和参数。

## 使用 Backlog

本技能通过 Membrane CLI 与 Backlog 进行交互。Membrane 会自动处理身份验证和凭证更新，因此您可以专注于集成逻辑，而无需关心身份验证的细节。

### 安装 CLI

请安装 Membrane CLI，以便您可以在终端中运行 `membrane` 命令：

```bash
npm install -g @membranehq/cli
```

### 首次设置

```bash
membrane login --tenant
```

系统会打开一个浏览器窗口进行身份验证。

**无头环境（Headless environments）：** 运行该命令后，复制显示的 URL，让用户通过浏览器打开该链接，然后执行 `membrane login complete <code>` 完成登录。

### 连接 Backlog

1. **创建新连接：**
   ```bash
   membrane search backlog --elementType=connector --json
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
   如果存在 Backlog 连接，请记录其 `connectionId`。

### 查找操作

当您知道想要执行的操作但不知道具体的操作 ID 时：

```bash
membrane action list --intent=QUERY --connectionId=CONNECTION_ID --json
```
这将返回包含操作 ID 和输入参数格式（inputSchema）的操作对象，从而帮助您知道如何执行该操作。

## 常用操作

| 操作名称 | 关键字 | 描述 |
| --- | --- | --- |
| 获取问题类型 | get-issue-types |  |
| 删除问题 | delete-issue |  |
| 添加评论 | add-comment |  |
| 获取用户信息 | get-users |  |
| 列出评论 | list-comments |  |
| 获取当前用户 | get-current-user |  |
| 更新问题 | update-issue |  |
| 创建问题 | create-issue |  |
| 列出问题 | list-issues |  |
| 获取项目列表 | get-projects |  |
| 获取具体项目 | get-project |  |
| 获取问题详情 | get-issue |  |

### 执行操作

```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json
```

**传递 JSON 参数：**

```bash
membrane action run --connectionId=CONNECTION_ID ACTION_ID --json --input "{ \"key\": \"value\" }"
```

### 代理请求

当现有操作无法满足您的需求时，您可以通过 Membrane 的代理直接发送请求到 Backlog API。Membrane 会自动在您提供的路径前添加基础 URL，并插入正确的身份验证头信息；如果凭证过期，系统会自动进行刷新。

```bash
membrane request CONNECTION_ID /path/to/endpoint
```

**常用选项：**

| 选项 | 描述 |
|------|-------------|
| `-X, --method` | HTTP 方法（GET、POST、PUT、PATCH、DELETE）。默认为 GET |
| `-H, --header` | 添加请求头（可重复使用），例如 `-H "Accept: application/json"` |
| `-d, --data` | 请求体（字符串） |
| `--json` | 以 JSON 格式发送请求体，并设置 `Content-Type: application/json` |
| `--rawData` | 以原始格式发送请求体，不进行任何处理 |
| `--query` | 查询参数（可重复使用），例如 `--query "limit=10"` |
| `--pathParam` | 路径参数（可重复使用），例如 `--pathParam "id=123"` |

## 最佳实践

- **优先使用 Membrane 与外部应用交互**：Membrane 提供了预构建的操作，支持内置的身份验证、分页和错误处理功能，这样既能节省令牌，又能提高通信安全性。
- **先探索再开发**：在编写自定义 API 调用之前，先运行 `membrane action list --intent=QUERY`（将 `QUERY` 替换为您的实际操作意图），以查找现有的操作。预构建的操作能够处理分页、字段映射以及原始 API 调用可能忽略的边缘情况。
- **让 Membrane 处理凭证**：切勿要求用户提供 API 密钥或令牌。请创建连接，Membrane 会在服务器端全程管理身份验证流程，无需用户保存任何本地凭证信息。