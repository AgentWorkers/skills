---
name: apix
description: 使用 `apix` 可以从本地的 Markdown 文件库中搜索、浏览和执行 API 端点。通过这项技能，您可以发现 REST API 端点，查看请求/响应的架构，并直接在终端中发起 HTTP 请求，而无需离开当前的工作环境。
---
# apix — 代理的 API 探索器

`apix` 是一个命令行工具（CLI），用于导入、浏览、搜索以及调用存储为本地 Markdown 文件的 API 端点文档。

## 先决条件与安装

在使用 `apix` 之前，请确认它是否已经安装：

```bash
apix --version
```

如果尚未安装，可以使用 Homebrew（macOS/Linux）进行安装：

```bash
brew tap apix-sh/tap
brew install apix
```

或者通过 curl 安装器进行安装：

```bash
curl -fsSL https://apix.sh/install | sh
```

## 代理工作流程指南

当请求 API 任务时，请遵循以下通用工作流程：

1. **发现**：找到相关的端点路由。
   ```bash
   apix search "create pet"
   # Or list available APIs: apix ls
   ```

2. **检查**：简要查看端点参数和规范，以便于理解上下文。
   ```bash
   apix peek petstore/v1/pets/{petId}/GET
   ```

   _注意：仅当需要完整的详细文档时才使用 `apix show <route>`，因为这些文档可能很长。_

3. **执行**：使用找到的路由发起 HTTP 请求。
   ```bash
   apix call demo/v1/items/{id}/POST -p id=item_123 -d '{"name":"item"}'
   ```

## 核心命令

### 搜索与发现

- **搜索所有索引的 API**：`apix search <查询>`
- **列出命名空间**：`apix ls`
- **列出命名空间中的端点**：`apix ls <命名空间>/<版本>`（例如：`apix ls petstore/v1`)
- **在命名空间内进行全文搜索**：`apix grep <命名空间> <查询>`

### 检查端点

端点的格式为：`<命名空间>/<版本>/<路径段>/<方法>`（例如：`petstore/v1/pets/GET`）。

- **预览（推荐给代理使用）**：`apix peek <路由>` — 输出 YAML 格式的文档以及必要的输入字段。
- **显示**：`apix show <路由>` — 输出该端点的完整 Markdown 文档。

### 执行 HTTP 请求

`apix call` 会自动从端点的 Markdown 文档中解析 URL、方法和认证信息。

- **使用固定路径段的简单请求**：

  ```bash
  apix call demo/v1/items/item_123/GET
  ```

  _(如果定义的路由是 `demo/v1/items/{id}/GET`，`apix` 会自动将 `item_123` 映射到 `{id}` 参数。)_

- **显式参数**：

  ```bash
  apix call demo/v1/items/{id}/POST \
    -p id=item_123 \
    -q expand=full \
    -H "Authorization: Bearer <token>" \
    -d '{"name":"item"}'
  ```

  - `-p <键>=<值>`：路径参数
  - `-q <键>=<值>`：查询参数
  - `-H "<头部>: <值>"`：HTTP 头部信息
  - `-d '<数据>'` 或 `-d @file.json`：请求体

### 导入自定义规范

如果所需的 API 不在公共注册表中，您可以将其 OpenAPI 3.x 规范导入到本地：

```bash
apix import /path/to/openapi.json --name myapi
```

## 代理使用说明

- 当您通过 shell 执行 `apix` 命令时，`apix` 会检测到标准输出（stdout）被重定向到其他位置，并自动输出结构清晰的原始 Markdown 文档，方便您阅读。
- `apix` 的路由是标准字符串格式。如果一个路由匹配多个来源，`apix` 会抛出歧义错误。在这种情况下，需要在路由前加上来源名称（例如：`core/petstore/v1/pets/GET`）。
- 建议优先使用 `peek` 而不是 `show`，以避免在上下文窗口中显示重复的规范信息。