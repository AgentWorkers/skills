---
name: obsidian
description: >
  Work with Obsidian vaults as a knowledge base. Features: fuzzy/phonetic search across all notes,
  auto-folder detection for new notes, create/read/edit notes with frontmatter, manage tags and wikilinks.
  Use when: querying knowledge base, saving notes/documents, editing existing notes by user instructions.
---

# Obsidian 知识库

Obsidian 知识库由 Markdown 文件组成的文件夹以及位于 `.obsidian/` 目录下的配置文件构成。

## 配置

- **知识库路径：** `/home/ruslan/webdav/data/ruslain`
- **环境变量：** `OBSIDIAN_VAULT=/home/ruslan/webdav/data/ruslain`

## 命令行工具使用方法

脚本位于：`/home/ruslan/.openclaw/workspace/skills/obsidian/scripts`

注意：全局参数（`--vault`、`--json`）必须放在命令之前使用。

```bash
export OBSIDIAN_VAULT=/home/ruslan/webdav/data/ruslain
cd /home/ruslan/.openclaw/workspace/skills/obsidian/scripts

# Search (fuzzy/phonetic) - uses ripgrep for speed
python3 obsidian_search.py "$OBSIDIAN_VAULT" "query" --limit 10 --json

# List notes
python3 obsidian_cli.py --json list                    # all notes
python3 obsidian_cli.py --json list "Projects"         # in folder

# List folders
python3 obsidian_cli.py --json folders

# Read note
python3 obsidian_cli.py --json read "Note Name"

# Create note
python3 obsidian_cli.py --json create "Title" -c "Content" -f "Folder" -t tag1 tag2
python3 obsidian_cli.py --json create "Title" -c "Content" --auto-folder  # auto-detect folder

# Edit note
python3 obsidian_cli.py --json edit "Note" append -c "Text to append"
python3 obsidian_cli.py --json edit "Note" prepend -c "Text at start"
python3 obsidian_cli.py --json edit "Note" replace -c "New full content"
python3 obsidian_cli.py --json edit "Note" replace-section -s "Summary" -c "New section text"

# Tags
python3 obsidian_cli.py --json tags

# Links (incoming/outgoing)
python3 obsidian_cli.py --json links "Note Name"

# Suggest folder for content
python3 obsidian_cli.py --json suggest-folder "content text" --title "Note Title"
```

## 工作流程：查询知识库

1. 运行 `obsidian_search.py` 并输入用户查询内容。
2. 如有需要，可查看搜索结果的前几条内容以获取上下文信息。
3. 根据搜索结果生成答案。
4. 引用来源：`[[Note Name]]`

## 工作流程：保存笔记

1. 如果未指定文件夹，则运行 `suggest-folder` 或使用 `--auto-folder` 命令创建文件夹。
2. 使用 `create` 命令创建新笔记。
3. 根据笔记内容添加合适的标签。
4. 将笔记的保存路径告知用户。

## 工作流程：通过提示编辑笔记

用户可以输入如下命令来编辑笔记：
- “在笔记 X 的末尾添加摘要” → `edit X append -c “...”`
- “将笔记 Y 重新编写得更简洁” → 读取笔记内容后重新编写，然后使用 `edit Y replace -c “...”`
- “在笔记 Z 中添加一个名为‘结果’的部分” → `edit Z replace-section -s “结果” -c “...”`

## 笔记格式

```markdown
---
created: 2024-01-15T10:30:00
modified: 2024-01-15T12:00:00
tags:
  - project
  - work
---

# Title

Content with [[wikilinks]] and #inline-tags.
```

## 维基链接

- `[[Note Name]]` — 链接到该笔记。
- `[[Note Name|显示文本]]` — 使用别名链接到该笔记。
- `[[Note Name#章节]]` — 链接到该笔记的特定章节。

## 前言字段

标准字段包括：
- `created` — 创建时间戳
- `modified` — 最后修改时间戳
- `tags` — 标签列表
- `aliases` — 可用于链接的别名

## 搜索机制

`obsidian_search.py` 使用以下方法进行搜索：
- 使用 `ripgrep` 进行快速初步过滤。
- 根据标题进行匹配（权重最高）。
- 根据标签进行匹配。
- 支持基于音译的模糊内容搜索（俄文 ↔ 英文）。
- 返回结果包括：笔记路径、标题、匹配度以及相关上下文信息。