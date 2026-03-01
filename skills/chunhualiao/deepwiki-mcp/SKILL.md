---
name: deepwiki
description: 查询 DeepWiki MCP，以获取关于任何公共 GitHub 仓库的基于 AI 的答案。该功能可用于回答有关仓库源代码、架构、配置或内部实现的问题。适用于以下场景：询问“X 在 <仓库> 中是如何工作的？”、“在代码库中查找相关信息”、“向 DeepWiki 提问”或“查看源代码”等。
triggers:
  - deepwiki
  - look up in codebase
  - ask deepwiki
  - check the source
  - how does X work in
  - openclaw source
  - repo architecture
  - codebase question
---
# DeepWiki MCP

您可以使用 DeepWiki 的人工智能驱动的文档和问答服务来查询任何公开的 GitHub 仓库。无需 API 密钥或身份验证，完全免费。

**MCP 端点：** `https://mcp.deepwiki.com/mcp`

## 功能范围与限制

**本功能支持：**
- 用自然语言提问关于任何公开 GitHub 仓库的问题
- 列出 DeepWiki 索引的文档主题
- 获取仓库的完整 wiki 内容
- 通过内置的帮助脚本执行查询

**本功能不支持：**
- 访问私有仓库（需要付费的 Devin 账户）
- 修改仓库或提交 Pull Request（PR）
- 实时代码分析（DeepWiki 的数据可能会滞后几天）
- 本地代码搜索或 grep 操作（请使用标准的文件工具）

## 输入参数

| 参数 | 是否必填 | 说明 |
|-------|----------|-------------|
| 问题 | 是 | 关于某个仓库的自然语言问题 |
| 仓库地址 | 否 | 格式为 `owner/repo`，默认为 `openclaw/openclaw` |
| 操作类型 | 否 | `ask`（默认）、`topics` 或 `docs` |

## 输出结果

- 基于仓库实际源代码生成的 AI 答案（附带引用）
- 文档主题的结构化列表
- 仓库的完整 wiki 内容（输出量可能较大）

## 工作流程

### 第一步：运行帮助脚本

该脚本位于本技能的 `scripts/deepwiki.sh` 目录中。

```bash
# Ask a question (defaults to openclaw/openclaw)
<skill_dir>/scripts/deepwiki.sh ask "How does session compaction work?"

# Ask about a specific repo
<skill_dir>/scripts/deepwiki.sh ask facebook/react "How does concurrent mode work?"

# List documentation topics
<skill_dir>/scripts/deepwiki.sh topics openclaw/openclaw

# Get full wiki contents (large output — prefer ask for targeted queries)
<skill_dir>/scripts/deepwiki.sh docs openclaw/openclaw
```

请将 `<skill_dir>` 替换为包含此 SKILL.md 文件的目录。

### 第二步：解释并传递答案

DeepWiki 会返回基于仓库实际源代码生成的 AI 答案。响应通常包括：
- 对问题的直接回答
- 对特定文件和代码路径的引用
- 相关功能的背景信息

将答案传递给用户，并在您了解更多细节时添加自己的解释。

### 第三步：必要时进行跟进

如果答案不完整或引发新的问题：
- 提出更具体的问题
- 使用 `topics` 查找相关的文档部分
- 使用 `docs` 获取更广泛的背景信息（但请注意：输出量可能非常大）

## 直接使用 curl（备用方案）

如果帮助脚本无法使用：

```bash
curl -s -X POST https://mcp.deepwiki.com/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "ask_question",
      "arguments": {
        "repoName": "owner/repo",
        "question": "YOUR QUESTION"
      }
    }
  }' | grep '^data:' | grep '"id":1' | sed 's/^data: //' | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result']['content'][0]['text'])"
```

## MCP 工具参考

| 工具 | 用途 | 参数 |
|------|---------|-----------|
| `ask_question` | 提出任何问题并获取 AI 生成的答案 | `repoName`, `question` |
| `read_wiki_structure` | 列出仓库的文档主题 | `repoName` |
| `read_wiki_contents` | 获取仓库的完整 wiki 文档 | `repoName` |

## 错误处理

| 错误类型 | 检测方式 | 处理方式 |
|---------|-----------|--------|
| 超时（>60 秒） | curl 命令执行超时或无响应 | 重试一次；可能是 DeepWiki 正在处理大量请求 |
| 空响应 | SSE 数据流中缺少 `data:` 行 | 检查仓库是否存在且是否为公开仓库 |
| 仓库未索引 | 报告未知仓库的错误信息 | 重新尝试——DeepWiki 会在首次请求时进行索引 |
| 被限制访问 | HTTP 429 错误响应 | 等待 30 秒后重试 |
| 脚本未找到 | 脚本未位于指定路径 | 使用直接使用 curl 的备用方案 |

## 成功标准

- DeepWiki 返回有意义的答案（非错误信息或空响应）
- 答案中包含对仓库实际代码/文件的引用
- 用户的问题得到了基于事实的解答

## 配置要求

无需进行任何持久性配置。本功能依赖以下工具：
- `exec` 工具来运行帮助脚本（bash + curl + python3）
- 不需要 API 密钥或身份验证
- 适用于任何公开的 GitHub 仓库

## 系统依赖项

| 依赖项 | 用途 |
|------------|---------|
| bash | 脚本执行 |
| curl | 向 MCP 端点发送 HTTP 请求 |
| python3 | 解析 SSE 格式的响应数据 |

## 注意事项

- 回答生成需要 10-30 秒（AI 在服务器端生成答案）
- `ask_question` 是最常用的工具，请优先使用它
- DeepWiki 会定期爬取仓库数据；可能会滞后于最新的提交内容
- 适用于所有公开的 GitHub 仓库，而不仅仅是 OpenClaw 仓库
- 对于私有仓库，需要付费的 [Devin](https://devin.ai) 账户