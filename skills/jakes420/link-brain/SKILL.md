---
name: link-brain
version: 4.3.0
description: "本地知识库用于管理链接。您可以保存带有摘要和标签的URL，之后通过自然语言进行搜索，创建收藏夹，并通过间隔重复的方式回顾待办事项。该知识库还提供独立的HTML图形视图。"
---
# Link Brain

这是一个个人书签管理工具，不过与传统的书签管理工具不同的是：被删除的书签会自动重新出现在系统中。

## 快速入门

```bash
python3 scripts/brain.py quickstart           # auto-imports browser bookmarks + opens GUI
python3 scripts/brain.py save "https://example.com" --auto
python3 scripts/brain.py search "that article about sqlite"
```

### 首次使用

首次使用时，请使用 `quickstart` 而不是 `setup`。它会：
1. 创建数据库；
2. 扫描 Chrome、Safari 和 Firefox 中的书签；
3. 导入所有找到的书签（会忽略重复项）；
4. 生成可视化的 GUI 控制台；
5. 返回包含导入统计信息的 JSON 数据。

`setup` 也会检测浏览器中的书签并显示相关信息，但不会自动导入书签。如果用户希望快速建立可用的知识库，建议使用 `quickstart`。

## 主要功能

- 保存带有标题、摘要、标签和元数据的链接；
- 支持基于自然语言过滤器的全文搜索；
- 可以在本地自动获取并汇总页面内容（无需使用 API 密钥）；
- 采用间隔重复学习机制，防止书签被遗忘；
- 提供集合功能，便于整理阅读列表；
- 支持知识图谱可视化展示；
- 提供阅读统计信息、阅读进度记录以及每周阅读摘要；
- 支持从 Chrome、Safari、Firefox、Pocket、YouTube 和 Reddit 导入书签；
- 所有数据都存储在 SQLite 数据库中（无需登录账号或发送任何遥测数据）。

数据存储路径为 `~/.link-brain/`。你可以通过设置 `LINK_BRAIN_DIR=/your/path` 来更改存储目录。

## 保存书签

### 手动方式

只需提供链接的标题和简要描述即可。

```bash
python3 scripts/brain.py save "https://docs.python.org" \
  --title "Python docs" \
  --summary "Standard library reference." \
  --tags "python, docs"
```

### 自动方式

只需提供一个链接，程序会自动获取页面内容、生成摘要，并根据用户现有的收藏标签来建议标签。无需使用任何大型语言模型（LLM）。

```bash
python3 scripts/brain.py auto-save "https://example.com"
```

或者使用以下命令：

```bash
python3 scripts/brain.py save "https://example.com" --auto
```

这是唯一一个需要发起网络请求的命令；其他所有操作都在本地完成。

## 查找书签

- **搜索**：内部使用 SQLite 的 FTS5 查询引擎，用户可以像编写普通 SQL 语句一样编写搜索查询。

```bash
python3 scripts/brain.py search "last week unread from github"
python3 scripts/brain.py search "best rated rust"
python3 scripts/brain.py search "unrated videos from youtube"
python3 scripts/brain.py search "oldest unread" --limit 10
```

### 标签管理

```bash
python3 scripts/brain.py tags                    # list all tags
python3 scripts/brain.py tags python             # links tagged "python"
```

### 相关链接

查找与指定标签相关的其他链接。

```bash
python3 scripts/brain.py related 42
```

### 标签推荐

根据用户的阅读习惯，为某个链接推荐合适的标签。

```bash
python3 scripts/brain.py suggest-tags "https://example.com"
```

## 提供阅读建议

- `digest`：批量展示待阅读的链接；
- `recommend`：根据用户最常使用的标签推荐新链接；
- `gems`：展示评分最高的链接或被忽略的优质内容；
- `random`：从待处理列表中随机选取一个链接。

```bash
python3 scripts/brain.py digest
python3 scripts/brain.py recommend
python3 scripts/brain.py gems
python3 scripts/brain.py random
```

## 阅读跟踪

- `streak`：记录用户连续阅读的日期；
- `insights`：显示用户的活跃阅读时间以及最常访问的网站域名；
- `weekly`：生成格式化的阅读摘要，可以直接发送到聊天工具中。

## 阅读列表（Collections）

用户可以创建阅读列表来组织自己的书签。

```bash
python3 scripts/brain.py collection create "Rust" --description "Systems stuff"
python3 scripts/brain.py collection add "Rust" 42
python3 scripts/brain.py collection show "Rust"
python3 scripts/brain.py collection list
python3 scripts/brain.py collection remove "Rust" 42
python3 scripts/brain.py collection export "Rust"            # markdown
python3 scripts/brain.py collection export "Rust" --html     # standalone HTML
```

## 书签复习机制

系统会为每个保存的链接设置复习间隔（1 天、3 天、7 天等）。

```bash
python3 scripts/brain.py review                  # next due item
python3 scripts/brain.py review done 42          # reviewed, advance interval
python3 scripts/brain.py review skip 42          # not now
python3 scripts/brain.py review reset 42         # back to 1-day interval
python3 scripts/brain.py review stats            # queue overview
```

## 自动保存

使用 `--auto` 标志（或 `auto-save` 快捷键）可以一次性完成链接的获取、汇总和标签添加。程序会使用 `urllib` 获取页面内容，并根据用户的标签习惯自动生成标签。整个过程不依赖任何外部服务。

## 知识图谱

```bash
python3 scripts/brain.py graph --open
```

程序会在 `~/.link-brain/graph.html` 文件中生成一个交互式的知识图谱。链接表示节点，共享的标签表示连接。无需额外的 JavaScript 库，直接在浏览器中打开即可查看。

## GUI 控制台

```bash
python3 scripts/brain.py gui
```

在浏览器中打开 `~/.link-brain/console.html` 文件。这是一个独立的 HTML 文件，不依赖任何外部资源，包含搜索功能、标签云、知识图谱、阅读列表、阅读时间线以及暗光/亮光模式。

如果不想启动 GUI 控制台，可以使用 `--no-open` 选项。

## 导入书签

### 从浏览器中导入

- 直接从浏览器的本地书签存储中导入书签。

```bash
python3 scripts/brain.py scan chrome
python3 scripts/brain.py scan safari
python3 scripts/brain.py scan firefox
```

### 从其他平台导入

- 从 Pocket、YouTube 和 Reddit 等平台导出的文件中导入书签。

**如何获取这些导出文件：**
- **Pocket**：访问 getpocket.com/export，会得到一个 HTML 文件；
- **YouTube**：使用 Google Takeout 功能，选择 YouTube 然后选择观看历史记录，会得到一个 JSON 文件；
- **Reddit**：访问 reddit.com/prefs/data-request 或 old.reddit.com 并导出保存的帖子。

## 同步书签

检查是否有书签从浏览器中被删除。

```bash
python3 scripts/brain.py sync chrome
python3 scripts/brain.py sources              # see connected sources and sync status
```

## 反馈

```bash
python3 scripts/brain.py feedback "your message"
python3 scripts/brain.py feedback --bug "something broke"
python3 scripts/brain.py feedback --idea "wouldn't it be cool if..."
python3 scripts/brain.py debug                # system info for bug reports
```

## 配置设置

所有数据存储在 `~/.link-brain/` 目录下：
- `brain.db`（SQLite 数据库）
- `graph.html`（知识图谱文件）
- `console.html`（GUI 控制台文件）
- `collection-*.md` 和 `collection-*.html`（导出的阅读列表文件）

你可以自定义数据存储目录：

```bash
LINK_BRAIN_DIR=/tmp/test-brain python3 scripts/brain.py setup
```

## 使用技巧：
- `search` 支持时间过滤（如“上周”）和阅读状态过滤（如“未读”或“评分最高”）；
- 除非你有特定的摘要需求，否则建议每次保存时都使用 `--auto` 选项。这种方式快速且效果不错；
- `review stats` 可以显示哪些链接需要尽快阅读；
- `gems` 功能有助于重新发现你曾经喜欢但后来忘记的链接；
- 可以将阅读列表导出为 HTML 文件与他人分享；
- 当书签数量达到 50 个左右时，知识图谱会变得更加丰富和有趣；
- `random` 功能适合在无聊时随机选择阅读内容；
- 结合使用 `scan` 和 `sync` 命令，可以确保书签与浏览器中的内容保持同步。