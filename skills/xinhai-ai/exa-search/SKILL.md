---
name: exa-search
description: 使用 Exa (exa.ai) 搜索 API 通过本地 Node 脚本在网页上进行搜索，并返回结构化的搜索结果（包括标题、网址、摘要和正文）。当用户请求启用 Exa 搜索功能、配置 Exa API 密钥或使用 Exa 进行网页搜索时，该脚本会被触发。
metadata: {"openclaw":{"emoji":"🔎","requires":{"bins":["node"],"env":["EXA_API_KEY"]},"primaryEnv":"EXA_API_KEY","homepage":"https://exa.ai/docs"}}
---

# Exa 搜索

通过捆绑的脚本使用 Exa 的搜索 API。

## 要求

- 在 Gateway 环境中设置 `EXA_API_KEY`（推荐），或者将其添加到 `~/.openclaw/.env` 文件中。

## 命令

- 运行搜索：
  - `node {baseDir}/scripts/exa_search.mjs "<query>" --count 5`

- 在搜索结果中包含页面文本（会增加成本）：
  - `node {baseDir}/scripts/exa_search.mjs "<query>" --count 5 --text`

- 按时间范围筛选：
  - `--start 2025-01-01 --end 2026-02-04`

## 注意

- 该功能不会修改 `web_search`；它提供了一个基于 Exa 的替代方案，当您特别需要使用 Exa 的功能时可以调用它。