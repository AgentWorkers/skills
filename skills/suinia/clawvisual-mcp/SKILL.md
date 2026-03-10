---
name: clawvisual
description: 通过本地 CLI 和 MCP 端点，将 URL 或长文本转换为适用于社交媒体的轮播图生成器所需的格式。
metadata: {"clawdbot":{"emoji":"🖼️","requires":{"bins":["clawvisual"]},"install":[{"id":"npm","kind":"npm","package":"clawvisual","bins":["clawvisual"],"label":"Install clawvisual (npm)"}]}}
---
# clawvisual

`clawvisual` 可以作为代理工作流程中的一个可调用技能（callable skill）来使用。它能够自动启动本地的 Web/MCP 服务，并提供稳定的命令行接口（CLI）用于生成内容以及查询作业状态。

## 快速入门

```bash
npm install -g clawvisual
clawvisual set CLAWVISUAL_LLM_API_KEY "your_openrouter_key"
clawvisual initialize
clawvisual convert --input "https://example.com/article" --slides auto
clawvisual status --job <job_id>
```

对于本地仓库的使用，您还可以运行：

```bash
npm run skill:clawvisual -- initialize
```

## 功能介绍

- 将 URL 或长文本转换为适合社交媒体的轮播图格式。
- 支持基于作业的异步工作流程（例如：`convert` -> `status --job`）。
- 提供用于 OpenClaw 及其他代理运行环境的 MCP JSON-RPC 工具。

## 命令列表

- `clawvisual initialize`：启动本地服务并打印 Web URL。
- `clawvisual status`：检查服务身份（必须为 `clawvisual-mcp`）。
- `clawvisual tools`：列出所有可用的 MCP 工具。
- `clawvisual convert --input <text_or_url> [--slides auto|1-8] [--ratio 4:5|1:1|9:16|16:9] [--lang <code>]`：将输入内容转换为轮播图格式。
- `clawvisual status --job <job_id>`：查询指定作业的状态和结果。
- `clawvisual revise --job <job_id> --instruction <text> [--intent rewrite_copy_style|regenerate_cover|regenerate_slides]`：修改作业内容或重新生成封面图片。
- `clawvisual regenerate-cover --job <job_id> [--instruction <text>] | --prompt <text>) [--ratio 4:5|1:1|9:16|16:9]`：重新生成作业的封面图片。
- `clawvisual call --name <tool_name> --args <json>`：直接调用指定的 MCP 工具。

## 配置

可选的本地配置文件：

- `~/.clawvisual/config.json`

通过命令行管理配置：

```bash
clawvisual set CLAWVISUAL_LLM_API_KEY "your_key"
clawvisual get CLAWVISUAL_LLM_API_KEY
clawvisual config
clawvisual unset CLAWVISUAL_LLM_API_KEY
```

支持的配置键包括：

- `CLAWVISUAL_LLM_API_KEY`（别名：`LLM_API_KEY`）
- `CLAWVISUAL_LLM_API_URL`（别名：`LLM_API_URL`）
- `CLAWVISUAL_LLM_MODEL`（别名：`LLM_MODEL`）
- `CLAWVISUAL_MCP_URL`（别名：`MCP_URL`）
- `CLAWVISUAL_API_KEY`

在自动启动本地服务时，`CLAWVISUAL_LLM_*` 的配置值会映射到运行环境的 `LLM_*` 环境变量中。

## 工作流程示例

1. 调用 `initialize` 启动服务。
2. 使用 `convert` 函数转换内容。
3. 使用 `status --job <job_id>` 命令持续查询作业状态，直到作业完成。
4. （可选）使用 `revise` 或 `regenerate-cover` 修改作业内容。
5. 再次使用 `status --job <job_id>` 命令查询修改后的作业状态。

## 输出格式

所有命令的输出都是 JSON 格式，便于上游代理进行解析。