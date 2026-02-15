---
name: silverbullet
description: MCP服务器用于SilverBullet笔记应用程序：支持读取、编写、搜索和管理Markdown页面
homepage: https://silverbullet.md
version: 1.0.0
metadata:
  clawdbot:
    requires:
      bins: ["python3", "uv"]
    install:
      - kind: script
        label: "Install SilverBullet MCP server"
        script: |
          cd "$SKILL_DIR"
          uv venv
          source .venv/bin/activate
          uv pip install -e .
allowed-tools: "mcporter(silverbullet:*)"
---

# SilverBullet MCP 服务器

本技能提供了一个用于与 [SilverBullet](https://silverbullet.md/) 交互的 MCP 服务器。SilverBullet 是一个基于 Markdown 的自托管笔记应用程序。

## 安装

### 通过 ClawdHub 安装

```bash
clawdhub install silverbullet
```

### 手动安装

```bash
cd ~/.clawdbot/skills/silverbullet
uv venv
source .venv/bin/activate
uv pip install -e .
```

## 配置

### 1. 设置 SilverBullet 的 URL

```bash
export SILVERBULLET_URL="http://localhost:3000"
```

或者将其添加到您的 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）中。

### 2. 配置 mcporter

将以下配置添加到 `~/.mcporter/mcporter.json` 文件中：

```json
{
  "servers": {
    "silverbullet": {
      "command": "python",
      "args": ["{baseDir}/server.py"],
      "transport": "stdio",
      "env": {
        "SILVERBULLET_URL": "http://localhost:3000"
      }
    }
  }
}
```

请将 `{baseDir}` 替换为实际的技能路径（例如：`~/.clawdbot/skills/silverbullet`）。

### 3. 验证安装

```bash
mcporter list silverbullet
```

系统应显示所有可用的工具。

## 可用工具

| 工具 | 描述 |
|------|-------------|
| `list_files` | 列出 SilverBullet 中的所有文件 |
| `read_page` | 从指定页面读取 Markdown 内容 |
| `write_page` | 创建或更新页面 |
| `delete_page` | 删除页面 |
| `append_to_page` | 向现有页面追加内容 |
| `search_pages` | 根据名称模式搜索页面 |
| `get_page_metadata` | 获取页面元数据（修改时间、创建时间、权限等） |
| `ping_server` | 检查 SilverBullet 服务器是否运行 |
| `get_server_config` | 获取服务器配置 |

## 使用示例

### 列出所有页面

```bash
mcporter call silverbullet.list_files
```

### 读取页面内容

```bash
mcporter call silverbullet.read_page path:"index.md"
mcporter call silverbullet.read_page path:"journal/2024-01-15.md"
```

### 创建或更新页面

```bash
mcporter call silverbullet.write_page path:"notes/meeting.md" content:"# Meeting Notes\n\n- Item 1\n- Item 2"
```

### 向页面追加内容

```bash
mcporter call silverbullet.append_to_page path:"journal/today.md" content:"## Evening Update\n\nFinished the project."
```

### 搜索页面

```bash
mcporter call silverbullet.search_pages query:"meeting"
```

### 删除页面

```bash
mcporter call silverbullet.delete_page path:"drafts/old-note.md"
```

### 检查服务器状态

```bash
mcporter call silverbullet.ping_server
```

## 自然语言示例

配置完成后，您可以这样使用 Moltbot：

- “列出我所有的 SilverBullet 页面”
- “从 SilverBullet 读取我的首页”
- “创建一个名为‘Project Ideas’的新页面，并列出其中的功能”
- “搜索名称中包含‘meeting’的页面”
- “将今天的笔记追加到我的日志中”
- “我的 TODO 页面的最后修改时间是什么？”
- “我的 SilverBullet 服务器是否正在运行？”

## 故障排除

### 服务器无响应

1. 检查 SilverBullet 是否正在运行：`curl http://localhost:3000/.ping`
2. 确保 `SILVERBULLET_URL` 设置正确
3. 检查防火墙/网络设置

### 出现“权限被拒绝”的错误

SilverBullet 的页面可能是只读的。请检查 `X-Permission` 头部信息，或使用 `get_page_metadata` 来验证权限。

### 工具未找到

1. 查看 mcporter 的配置文件：`cat ~/.mcporter/mcporter.json`
2. 直接测试服务器：`python {baseDir}/server.py`（应无错误地启动）
3. 检查 Python 和 uv 的安装情况：`which python3 uv`

## API 参考

有关底层 REST API 的完整文档，请参阅 [SilverBullet HTTP API](https://silverbullet.md/HTTP%20API)。