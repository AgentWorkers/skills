---
name: coda-ai
description: 这是一个用于读取 Coda.io 文档和页面的命令行工具（CLI）。该工具可以列出所有文档和页面，并以 Markdown、JSON 或 HTML 格式显示内容。
homepage: https://www.npmjs.com/package/coda-ai
metadata: {"openclaw":{"requires":{"bins":["coda-ai"],"env":["CODA_API_TOKEN"]},"primaryEnv":"CODA_API_TOKEN","install":[{"id":"node","kind":"node","package":"coda-ai","bins":["coda-ai"],"label":"Install coda-ai (npm)"}]}}
---

# coda-ai

这是一个用于AI代理读取Coda.io内容的命令行工具（CLI）。

## 工作流程

1. **docs**：列出所有文档。
2. **pages**：列出文档中的所有页面。
3. **read**：获取页面内容。

## 设置（只需执行一次）

```bash
npm install -g coda-ai@0.2.2

# Auth (Coda API token)
echo "CODA_API_TOKEN=YOUR_TOKEN" > .env
coda-ai auth --from-file .env

coda-ai whoami # verify auth
```

## 凭据与存储
- 凭据存储位置：`~/.coda-ai/config.json`（文件权限设置为**0600**）
- 如需删除存储的凭据，请执行以下操作：

```bash
coda-ai logout
```

## 命令

### 列出文档

```bash
coda-ai docs --compact        # only id + name in toon format (recommended for AI Agents)
coda-ai docs                  # full data in toon format
coda-ai docs --format json    # full data in json
coda-ai docs --format table   # human-readable table
```

返回结果：按更新时间排序的所有文档。可以使用`id`字段进行后续操作。

### 列出页面

```bash
coda-ai pages --docId <docId> --compact        # only id + name, toon format (recommended for AI Agents)
coda-ai pages --docId <docId> --format json    # full data in json
coda-ai pages --docId <docId> --format tree    # visual tree
coda-ai pages --docId <docId>                  # full data in toon format (default)
```

返回结果：页面的层次结构。可以使用`pageId`字段进行后续操作。

### 获取页面内容

```bash
coda-ai read --docId <docId> --pageId <pageId>  # markdown (default, recommended for AI Agents)
coda-ai read --docId <docId> --pageId <pageId> --format json    # structured data in json
coda-ai read --docId <docId> --pageId <pageId> --format html    # html export
```


## 参考文档

完整文档：https://github.com/auniik/coda-ai#readme