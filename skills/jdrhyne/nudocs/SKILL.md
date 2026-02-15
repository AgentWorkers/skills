---
name: nudocs
description: 通过 Nudocs.ai 上传、编辑和导出文档。该工具适用于创建可共享的文档链接以支持协作编辑，将 Markdown 格式的文档上传到 Nudocs 进行高级编辑，或检索已编辑的内容。相关操作包括：“发送到 Nudocs”、“上传到 Nudocs”、“在 Nudocs 中编辑”、“从 Nudocs 中获取内容”、“获取 Nudocs 文档链接”以及“显示我的 Nudocs 文档”。
homepage: https://nudocs.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires":
          {
            "bins": ["nudocs"],
            "env": ["NUDOCS_API_KEY"],
            "config": ["~/.config/nudocs/api_key"],
          },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@nutrient-sdk/nudocs-cli",
              "repo": "https://github.com/PSPDFKit/nudocs-cli",
              "bins": ["nudocs"],
              "label": "Install Nudocs CLI (npm)",
            },
          ],
      },
  }
---

# Nudocs

将文档上传到 Nudocs.ai 进行丰富的编辑，获取可分享的链接，并下载编辑后的结果。

## 设置

1. 安装命令行工具（CLI）：
```bash
npm install -g @nutrient-sdk/nudocs-cli
```

2. 从 https://nudocs.ai 获取您的 API 密钥（登录后点击“Integration”）

3. 配置 API 密钥：
```bash
# Option 1: Environment variable
export NUDOCS_API_KEY="nudocs_your_key_here"

# Option 2: Config file
mkdir -p ~/.config/nudocs
echo "nudocs_your_key_here" > ~/.config/nudocs/api_key
```

## 命令

```bash
nudocs upload <file>              # Upload and get edit link
nudocs list                       # List all documents
nudocs link [ulid]                # Get edit link (last upload if no ULID)
nudocs pull [ulid] [--format fmt] # Download document (default: docx)
nudocs delete <ulid>              # Delete a document
nudocs config                     # Show configuration
```

## 工作流程

### 上传流程
1. 创建/编写文档内容
2. 保存为 Markdown（或其他支持的格式）
3. 运行：`nudocs upload <文件路径>`
4. 将返回的编辑链接分享给用户

### 下载流程
1. 用户请求下载文档
2. 运行：`nudocs pull [ULID] --format <格式>`
3. 读取并展示下载的文件

### 格式选择

| 场景 | 推荐格式 |
|----------|-------------------|
| 用户使用富格式编辑文档 | `docx`（默认） |
| 简单文本/代码内容 | `md` |
| 最终交付/分享 | `pdf` |

有关完整的格式支持，请参阅 `references/formats.md`。

## 自然语言指令

识别以下用户指令：

**上传/发送：**
- “发送到 Nudocs”
- “上传到 Nudocs”
- “在 Nudocs 中打开”
- “在 Nudocs 中编辑这个文件”
- “让我在 Nudocs 中编辑这个文件”
- “将这个文件放入 Nudocs”

**下载/获取：**
- “下载文档”
- “从 Nudocs 下载文档”
- “获取那个文档”
- “从 Nudocs 获取更新版本”
- “我修改了什么”
- “获取我的编辑内容”

**链接：**
- “获取 Nudocs 的链接”
- “分享链接”
- “那个文档在哪里”
- “Nudocs 的网址”

**列表：**
- “显示我的文档”
- “列出我的文档”
- “我有哪些文档”
- “我的 Nudocs 文档”

## 文档最佳实践

上传前请确保文档结构良好：
- 使用清晰的标题层级（H1 → H2 → H3）
- 保持一致的间距
- 使用适当的列表格式
- 段落简洁（3-5 句）

有关模板和指南，请参阅 `references/document-design.md`。

## 示例会话

```
User: Write me a blog post about remote work and send it to Nudocs

Agent:
1. Writes blog-remote-work.md with proper structure
2. Runs: nudocs upload blog-remote-work.md
3. Returns: "Here's your Nudocs link: https://nudocs.ai/file/01ABC..."

User: *edits in Nudocs, adds formatting, images*
User: Pull that back

Agent:
1. Runs: nudocs pull --format docx
2. Reads the downloaded file
3. Returns: "Got your updated document! Here's what changed..."
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| “未找到 API 密钥” | 未提供凭据 | 设置 NUDOCS_API_KEY 或创建配置文件 |
| “达到文档数量限制” | 免费 tier 的文档数量限制（10 个） | 删除旧文档或升级到 Pro 版本 |
| “未经授权” | API 密钥无效 | 在 Nudocs 设置中重新生成密钥 |
| “未提供 ULID” | 未提供文档 ID | 指定 ULID 或先上传文档 |

## 链接

- 命令行工具：https://github.com/PSPDFKit/nudocs-cli（在 npm 上的别名为 `@nutrient-sdk/nudocs-cli`）
- MCP 服务器：https://github.com/PSPDFKit/nudocs-mcp-server
- Nudocs：https://nudocs.ai