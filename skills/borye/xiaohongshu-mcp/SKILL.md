---
name: xiaohongshu-mcp
description: >
  Automate Xiaohongshu (RedNote) content operations using a Python client for the xiaohongshu-mcp server.
  Use for: (1) Publishing image, text, and video content, (2) Searching for notes and trends,
  (3) Analyzing post details and comments, (4) Managing user profiles and content feeds.
  Triggers: xiaohongshu automation, rednote content, publish to xiaohongshu, xiaohongshu search, social media management.
---

# 小红书 MCP 技能（使用 Python 客户端）

使用一个捆绑的 Python 脚本自动化小红书上的内容操作，该脚本可与 `xpzouying/xiaohongshu-mcp` 服务器（拥有 8.4k 多个星的评价）进行交互。

**项目链接：** [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp)

## 1. 本地服务器设置

使用此技能之前，需要确保 `xiaohongshu-mcp` 服务器已在您的本地机器上运行。

### 第 1 步：下载二进制文件

从 [GitHub 发布页面](https://github.com/xpzouying/xiaohongshu-mcp/releases) 下载适用于您系统的二进制文件。

| 平台 | MCP 服务器 | 登录工具 |
| -------- | ---------- | ---------- |
| macOS (Apple Silicon) | `xiaohongshu-mcp-darwin-arm64` | `xiaohongshu-login-darwin-arm64` |
| macOS (Intel) | `xiaohongshu-mcp-darwin-amd64` | `xiaohongshu-login-darwin-amd64` |
| Windows | `xiaohongshu-mcp-windows-amd64.exe` | `xiaohongshu-login-windows-amd64.exe` |
| Linux | `xiaohongshu-mcp-linux-amd64` | `xiaohongshu-login-linux-amd64` |

为下载的文件授予执行权限：
```shell
chmod +x xiaohongshu-mcp-darwin-arm64 xiaohongshu-login-darwin-arm64
```

### 第 2 步：登录（仅首次需要）

运行登录工具。它将打开一个包含 QR 码的浏览器窗口。使用您的小红书移动应用扫描该 QR 码。

```shell
./xiaohongshu-login-darwin-arm64
```

> **重要提示**：请勿在其他网页浏览器中使用相同的小红书账号登录，否则会导致服务器会话失效。

### 第 3 步：启动 MCP 服务器

在另一个终端窗口中运行 MCP 服务器。服务器将在后台运行。

```shell
# Run in headless mode (recommended)
./xiaohongshu-mcp-darwin-arm64

# Or, run with a visible browser for debugging
./xiaohongshu-mcp-darwin-arm64 -headless=false
```

服务器的访问地址为 `http://localhost:18060`。

## 2. 使用该技能

此技能包含一个 Python 客户端（`scripts/xhs_client.py`），用于与本地服务器进行交互。您可以直接从 shell 中使用它。

### 可用命令

| 命令 | 描述 | 示例 |
| --- | --- | --- |
| `status` | 检查登录状态 | `python scripts/xhs_client.py status` |
| `search <关键词>` | 搜索笔记 | `python scripts/xhs_client.py search "咖啡"` |
| `detail <id> <token>` | 获取笔记详情 | `python scripts/xhs_client.py detail "note_id" "xsec_token"` |
| `feeds` | 获取推荐内容 | `python scripts/xhs_client.py feeds` |
| `publish <标题> <内容> <图片>` | 发布笔记 | `python scripts/xhs_client.py publish "标题" "内容" "url1,url2"` |

### 示例工作流程：市场研究

1. **检查状态**：首先确保服务器正在运行并且您已登录。
    ```shell
    python ~/clawd/skills/xiaohongshu-mcp/scripts/xhs_client.py status
    ```

2. **搜索关键词**：查找与您的研究主题相关的笔记。搜索结果将包含下一步所需的 `feed_id` 和 `xsec_token`。
    ```shell
    python ~/clawd/skills/xiaohongshu-mcp/scripts/xhs_client.py search "户外电源"
    ```

3. **获取笔记详情**：使用搜索结果中的 `feed_id` 和 `xsec_token` 来获取特定笔记的完整内容和评论。
    ```shell
    python ~/clawd/skills/xiaohongshu-mcp/scripts/xhs_client.py detail "64f1a2b3c4d5e6f7a8b9c0d1" "security_token_here"
    ```

4. **分析**：查看笔记的内容、评论和互动数据以收集见解。