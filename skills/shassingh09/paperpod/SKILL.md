---
name: paperpod
description: **隔离式代理运行时环境：**  
支持代码执行、实时预览功能、浏览器自动化操作，以及集成50多种工具（如ffmpeg、sqlite、pandoc、imagemagick）；同时具备大规模语言模型（LLM）推理能力，并支持持久化内存管理。所有功能均通过命令行界面（CLI）或HTTP协议实现，无需使用任何软件开发工具包（SDK）或API密钥。
metadata:
  author: PaperPod
  version: "2.0.3"
  homepage: https://paperpod.dev
---

# PaperPod

PaperPod 提供了隔离的、基于代理的沙箱环境，支持代码执行、实时预览功能、浏览器自动化操作，以及超过 50 种工具（如 ffmpeg、sqlite、pandoc、imagemagick）的使用。此外，它还支持大语言模型（LLM）的推理，并提供持久化存储功能。所有这些功能均可通过命令行界面（CLI）或 HTTP 请求实现，无需安装任何 SDK 或使用 API 密钥。计费方式基于每秒的计算使用量，支持通过 Stripe 或 x402 进行充值。

## 快速入门

```bash
curl -X POST https://paperpod.dev/login -d '{"email":"you@email.com"}'  # Verify and get token
npm install -g @paperpod/cli
ppod login <token> && ppod help
```

## 认证

**步骤 1：获取令牌**
```bash
curl -X POST https://paperpod.dev/login -d '{"email":"you@email.com"}'
# Check email → click magic link → copy token (pp_sess_...)
```

**步骤 2：使用令牌**（选择一种方法）

| 方法 | 使用方式 | 适用场景 |
|--------|---------|----------|
| **CLI 登录** | `ppod login ppsess_...` | 日常交互式使用 |
| **环境变量** | `export PAPERPOD_TOKEN=ppsess_...` | 脚本、持续集成/持续部署（CI/CD） |
| **每次请求** | `-H "Authorization: Bearer ppsess_..."` | 单次 HTTP 请求 |

令牌的有效期为 **15 天**。如果遇到 `EXPIRED_TOKEN` 错误，请通过 `POST /login` 重新认证。

---

## 建议使用 CLI

CLI 是使用 PaperPod 的最简单方式，它可以自动处理数据流、会话管理及重新连接等操作。

### CLI 命令

| 分类 | 命令 | 描述 |
|----------|---------|-------------|
| **沙箱** | `ppod exec <cmd>` | 运行 shell 命令 |
| | `ppod write <path> [file]` | 写入文件（若未提供文件，则使用标准输入） |
| | `ppod read <path>` | 读取文件 |
| | `ppod ls <path>` | 列出目录内容 |
| **进程** | `ppod start <cmd>` | 启动后台进程 |
| | `ppod ps` | 列出所有进程 |
| | `ppod kill <id>` | 终止进程 |
| **端口** | `ppod expose <port>` | 获取公共访问 URL（-q 仅输出 URL） |
| **浏览器** | `ppod browser:screenshot <url>` | 截取网页截图 |
| | `ppod browser:pdf <url>` | 生成 PDF 文件 |
| | `ppod browser:scrape <url> [sel]` | 抓取网页元素（默认为页面正文） |
| | `ppod browser:markdown <url>` | 提取页面中的 Markdown 内容 |
| | `ppod browser:content <url>` | 获取渲染后的 HTML 内容 |
| | `ppod browser:test <url> '<json>'` | 使用 Playwright 运行测试 |
| | `ppod browser:acquire` | 获取可重用的浏览器会话 |
| | `ppod browser:connect <id>` | 连接到现有会话 |
| | `ppod browser:sessions` | 列出所有活跃会话 |
| | `ppod browser:limits` | 查看浏览器使用限制 |
| **AI** | `ppod ai <prompt>` | 生成文本 |
| | `ppod ai:embed <text>` | 生成嵌入内容 |
| | `ppod ai:image <prompt>` | 生成图片 |
| | `ppod ai:transcribe <audio>` | 语音转文字 |
| | `ppod ai:models` | 查看可用 AI 模型 |
| **代码解析** | `ppod interpret <code>` | 代码解析（包含图表输出） |
| **数据存储** | `ppod mem:write <path>` | 保存数据 |
| | `ppod mem:read <path>` | 读取保存的数据 |
| | `ppod mem:ls` | 列出所有数据文件 |
| | `ppod mem:rm <path>` | 从内存中删除文件 |
| | `ppod mem:usage` | 查看内存使用情况 |
| **账户** | `ppod balance` | 查看剩余信用额度 |
| | `ppod status` | 查看连接状态 |
| | `ppod help` | 显示所有可用命令 |
| | `ppod <cmd> --help` | 查看特定命令的用法 |

**更新 CLI：** `npm update -g @paperpod/cli`

### CLI 示例

```bash
# Execute code
ppod exec "python -c 'print(2+2)'"
ppod exec "npm init -y && npm install express"
# Start server + expose (--bind 0.0.0.0 required for public access)
ppod start "python -m http.server 8080 --bind 0.0.0.0"
ppod expose 8080  # → https://8080-{sandbox-id}-p8080_v1.paperpod.work (stable URL)
# Browser with tracing
ppod browser:screenshot https://example.com --trace debug.zip
# Persistent storage (survives sandbox reset)
echo '{"step":3}' | ppod mem:write state.json
# Built-in tools (50+ available: ffmpeg, sqlite3, pandoc, imagemagick, git, jq, ripgrep...)
ppod exec "ffmpeg -i input.mp4 -vf scale=640:480 output.mp4"  # Video processing
ppod exec "sqlite3 data.db 'SELECT * FROM users'"             # Database queries
ppod exec "convert image.png -resize 50% thumbnail.png"       # Image manipulation
```
---

## HTTP 端点

当无法使用 CLI 时，可以使用 HTTP 进行一次性操作。完整 API 参考请访问：`curl https://paperpod.dev/docs` 或访问 [PaperPod 文档页面](https://paperpod.dev/docs)。

### 快速参考

| 端点 | 功能 |
|----------|---------|
| `POST /execute` | 运行代码（Python、JavaScript、Shell） |
| `POST /execute/stream` | 流式输出（SSE 格式） |
| `POST /files/write` | 写入文件 |
| `POST /files/read` | 读取文件 |
| `POST /files/list` | 列出目录内容 |
| `POST /process/start` | 启动后台进程 |
| `POST /process/list` | 列出所有进程 |
| `POST /expose` | 获取端口的预览 URL |
| `POST /memory/write` | 保存数据 |
| `POST /memory/read` | 读取保存的数据 |
| `POST /browser/screenshot` | 截取网页截图 |
| `POST /browser/pdf` | 生成 PDF 文件 |
| `POST /browser/markdown` | 提取 Markdown 内容 |
| `POST /ai/generate` | 生成文本 |
| `POST /ai/embed` | 生成嵌入内容 |
| `POST /ai/image` | 生成图片 |
| `GET /ai/models` | 查看可用 AI 模型 |

### HTTP 示例

```bash
# Execute shell command
curl -X POST https://paperpod.dev/execute \
  -H "Authorization: Bearer $PAPERPOD_TOKEN" \
  -d '{"code": "ls -la", "language": "shell"}'
```
---

## 主要功能

| 分类 | 功能描述 |
|----------|-----------------|
| **代码执行** | 支持 Python、JavaScript 和 Shell 命令的执行 |
| **进程管理** | 支持后台进程的启动和停止 |
| **预览功能** | 可通过端口（如 `https://8080-{sandbox-id}-p8080_v1.paperpod.work`）查看预览结果 |
| **持久化存储** | 提供 10MB 的持久化存储空间（R2 级别） |
| **浏览器功能** | 支持截图、PDF 生成和网页内容抓取（使用 Playwright） |
| **AI 模型** | 提供文本生成、嵌入内容生成、图片生成和语音转文字等服务 |
| **文件操作** | 支持文件的读写操作，以及 Git 和批量文件处理 |

### 预装工具（超过 50 种）

| 分类 | 工具名称 |
|----------|-------|
| **运行时环境** | Python、Node.js、npm、bun、pip |
| **版本控制** | git、gh（GitHub 命令行工具） |
| **网络工具** | curl、httpie、jq、dig、ss |
| **搜索与文本处理** | ripgrep、find、sed、awk、tree |
| **媒体与文档处理** | ffmpeg、imagemagick、pandoc |
| **构建与数据处理** | make、sqlite3、tar、gzip、zip、unzip |

## 重要说明

- **沙箱环境是隔离的**：每个用户拥有独立的 Linux 环境，只能影响自己的沙箱；
- **数据持久化**：使用代理提供的持久化存储空间（`/memory/*`）；
- **工作目录**：所有相对路径均以 `/workspace` 为基准；
- **服务器配置**：服务器必须绑定到 `0.0.0.0` 地址以实现公共访问；
- **端口分配**：端口 3000-3010 被预留，建议使用其他端口（如 8080、5000、4000 等）；
- **浏览器会话**：每个命令都会创建一个新的临时会话。使用 `browser:acquire` 可重复使用会话，`--trace` 可用于记录操作日志。

## 计费规则

计算费用为 **0.0001 美元/秒**（包含浏览器使用费用），AI 服务费用为 **0.02 美元/1000 个神经元**。新账户可享受 **5 美元免费额度**（约 14 小时），无需信用卡。

## 常用操作

- `ppod help`：查看 CLI 命令参考；
- `GET https://paperpod.dev/`：获取 API 接口规范（JSON 格式）；
- `GET https://paperpod.dev/docs`：查看完整文档。

---

## 高级功能：WebSocket（不推荐用于常规工作流程）

对于需要编程集成或自定义应用程序的场景，可以通过 WebSocket 进行连接。详情请访问 [PaperPod 文档页面](https://paperpod.dev/docs)。

---

（注：由于文档内容较长，部分详细信息在翻译时进行了简化处理，以确保简洁性和准确性。）