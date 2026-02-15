---
name: link-brain
version: 4.2.0
description: "本地知识库用于管理链接：您可以保存带有摘要和标签的URL，之后使用自然语言进行搜索，创建链接集合，并通过间隔重复的方式复习待办事项。该知识库还提供独立的HTML图形视图。"
---
# Link Brain

Link Brain 是一个本地命令行工具（CLI），它将带有标题、摘要、标签和元数据的 URL 保存到 SQLite 数据库中。

该工具设计得易于使用且非常可靠：

- 无需注册账户
- 无需 API 密钥
- 不会发送任何遥测数据
- 数据存储在 `~/.link-brain/` 目录下

## 快速入门

```bash
python3 scripts/brain.py setup

# Manual save
python3 scripts/brain.py save "https://example.com" \
  --title "Example" \
  --summary "A short note about what this page is." \
  --tags "reference, example"

# Auto save (fetches the page with urllib, then summarizes and tags locally)
python3 scripts/brain.py save "https://example.com" --auto

# Search
python3 scripts/brain.py search "that article about sqlite"

# Make a graph
python3 scripts/brain.py graph --open
```

## 数据存储位置

默认情况下，Link Brain 将所有数据存储在以下位置：

- `~/.link-brain/brain.db`（SQLite 数据库）
- `~/.link-brain/graph.html`（可选的输出文件）
- `~/.link-brain/collection-*.md` 和 `collection-*.html`（可选的导出文件）

对于测试或临时使用，您可以自定义数据存储目录：

```bash
LINK_BRAIN_DIR=/tmp/my-link-brain python3 scripts/brain.py setup
```

## 保存链接

### 手动保存

当您已经知道链接的标题、标签和摘要时，可以使用手动保存功能。

```bash
python3 scripts/brain.py save "https://docs.python.org" \
  --title "Python docs" \
  --summary "Reference docs for the Python standard library." \
  --tags "python, docs"
```

### 自动保存

自动保存功能会使用 `urllib` 获取 URL，然后执行以下操作：
- 从 HTML 中提取可读文本
- 生成摘要
- 根据关键词和您已有的标签推荐合适的标签

**注意：** 自动保存功能会向目标 URL 发送网络请求。其他所有命令都在本地执行。

## 搜索

Link Brain 使用 SQLite 的 FTS5 支持进行搜索，并且还支持自然语言过滤。

示例：

```bash
python3 scripts/brain.py search "last week unread from github"
python3 scripts/brain.py search "best rated rust"
python3 scripts/brain.py search "unrated videos from youtube"
python3 scripts/brain.py search "oldest unread" --limit 10
```

## 收藏夹

收藏夹是用于管理已保存链接的列表。

```bash
python3 scripts/brain.py collection create "Rust" --description "Things to read and revisit"
python3 scripts/brain.py collection add "Rust" 42
python3 scripts/brain.py collection show "Rust"
python3 scripts/brain.py collection export "Rust"          # markdown
python3 scripts/brain.py collection export "Rust" --html   # html
```

## 审查流程

每个保存的链接都会被添加到审查队列中。您可以查看下一个待处理的链接并标记为已审查。

```bash
python3 scripts/brain.py review next
python3 scripts/brain.py review done 42
python3 scripts/brain.py review skip 42
```

## GUI 控制台

Link Brain 提供了一个图形用户界面（GUI），该界面会生成一个独立的 HTML 文件（`~/.link-brain/console.html`），其中包含了所有功能。该界面无需依赖任何外部资源或 CDN，也不需要进行网络请求。功能包括搜索、标签云、知识图谱、收藏夹管理、阅读时间线以及明暗模式切换。

## 图表生成

`graph` 命令会生成一个独立的 HTML 文件，其中包含交互式的图表视图。

**注意：** 该功能不需要任何外部 JavaScript 库。

## 命令列表

所有可用命令的列表如下：

```bash
python3 scripts/brain.py help
```

## 反馈

如果您发现了漏洞或有任何建议，请告诉我们！

```bash
brain.py feedback "your message"
brain.py feedback --bug "something broke"
brain.py feedback --idea "wouldn't it be cool if..."
```

如果您需要提交详细的漏洞报告，请运行 `brain.py debug` 以获取系统信息，这些信息可以直接用于问题报告。