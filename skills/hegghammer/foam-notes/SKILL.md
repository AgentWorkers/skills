---
name: foam-notes
version: 1.0.2
description: **操作说明：**

- **与 Foam 笔记仓库协作**：您可以创建、编辑、链接和标记笔记。
- **智能推荐功能**：系统会提供相关的维基链接和标签建议。
- **高级功能**：支持反向链接的查找、每日笔记的生成、模板的使用、笔记的可视化展示以及笔记的删除和重命名。
- **详尽的文档支持**：提供了完整的 Foam 文档，便于您快速了解和使用该工具。

**主要功能包括：**

1. **创建和编辑笔记**：您可以轻松地创建新的笔记，并对现有笔记进行编辑。
2. **链接和标签管理**：您可以方便地为笔记添加链接和标签，以便更好地组织和查找信息。
3. **智能推荐**：系统会根据您的使用习惯，智能地推荐相关的笔记和标签。
4. **高级功能**：提供强大的功能，如反向链接的查找、每日笔记的生成、笔记的可视化展示等。
5. **文档支持**：附带详细的 Foam 文档，帮助您快速上手和使用该工具。

请注意：以上内容是根据您提供的 SKILL.md 文件内容翻译的。如果您需要进一步的帮助或修改，请随时告知！
---

# Foam Notes

在 VS Code 中使用 Foam 笔记工作区。[Foam](https://foamnotes.com) 是一个免费、开源的个人知识管理系统，它使用标准的 Markdown 文件和维基链接。

## 快速参考

- **维基链接**：`[[note-name]]` — 实现笔记之间的双向链接
- **嵌入内容**：`![[note-name]]` — 从其他笔记中插入内容
- **回链**：自动发现与当前笔记的关联
- **标签**：`#tag` 或在文档开头添加 `tags: [tag1, tag2]`
- **每日笔记**：使用快捷键 `Alt+D` 或命令 `Foam: Open Daily Note`

## 配置

在 `config.json` 中设置您的 Foam 工作区路径：

```json
{
  "foam_root": "/home/thomas/foam-notes",
  "default_template": "new-note",
  "default_notes_folder": "notes",
  "daily_note_folder": "journals"
}
```

**位置**：`~/.openclaw/workspace/skills/foam-notes/config.json`

**优先级顺序**（从高到低）：
1. `--foam-root` 命令行参数
2. `FOAM_WORKSPACE` 环境变量
3. `config.json` 中的 `foam_root` 设置
4. 通过查找 `.foam` 或 `.vscode` 目录自动检测
5. 当前工作目录

请参阅 `references/configuration.md` 以获取完整文档。

## 脚本

所有脚本都支持使用 `--foam-root` 来覆盖工作区路径。

### init_templates.py

使用官方提供的模板初始化 `.foam/templates/` 目录：

```bash
python3 scripts/init_templates.py              # Copy to current workspace
python3 scripts/init_templates.py --foam-root ~/notes
python3 scripts/init_templates.py --list      # Show available templates
python3 scripts/init_templates.py --force     # Overwrite existing
python3 scripts/init_templates.py --dry-run   # Preview what would be copied
```

**包含的模板**：
- `new-note.md` — 新笔记的默认模板
- `daily-note.md` — 每日笔记模板
- `your-first-template.md` — 显示 VS Code 代码片段的示例模板

### create_note.py

根据模板创建新笔记：

```bash
python3 scripts/create_note.py "My New Idea"
python3 scripts/create_note.py "Meeting Notes" --template meeting
python3 scripts/create_note.py "Research Topic" --dir research/
```

### find_backlinks.py

查找所有链接到指定笔记的笔记：

```bash
python3 scripts/find_backlinks.py "Machine Learning"
python3 scripts/find_backlinks.py "ml-basics" --format json
```

### search_tags.py

根据标签查找笔记：

```bash
python3 scripts/search_tags.py "#research"
python3 scripts/search_tags.py machine-learning --include-frontmatter
```

### list_tags.py

列出所有标签及其使用频率：

```bash
python3 scripts/list_tags.py
python3 scripts/list_tags.py --hierarchy --min-count 3
```

### graph_summary.py

分析知识图谱：

```bash
python3 scripts/graph_summary.py
python3 scripts/graph_summary.py --format json
```

### daily_note.py

创建每日笔记：

```bash
python3 scripts/daily_note.py
python3 scripts/daily_note.py --yesterday
python3 scripts/daily_note.py --template custom-daily
python3 scripts/daily_note.py --print-path   # Just output the path
```

### suggest_wikilinks.py

通过在笔记中查找与现有笔记标题匹配的文本来建议维基链接：

```bash
python3 scripts/suggest_wikilinks.py my-note.md              # Interactive mode
python3 scripts/suggest_wikilinks.py my-note.md --apply 1,3,5  # Auto-apply
python3 scripts/suggest_wikilinks.py my-note.md --auto-apply   # Apply all
python3 scripts/suggest_wikilinks.py my-note.md --dry-run      # Preview only
python3 scripts/suggest_wikilinks.py my-note.md --with-aliases # Create [[target|text]] format
```

该脚本会扫描笔记内容，并识别出与档案中现有笔记标题匹配的单词或短语，并将它们以编号列表的形式呈现：

```
1. Line 12, col 8
   Text: "machine learning"
   Link to: [[machine-learning]]
   Context: ...working on machine learning projects...
```

**维基链接格式**：
- **默认**：`[[target]]` — 简洁的链接
- **使用 `--with-aliases` 选项**：`[[target|display text]]` — 保留原始文本作为别名

响应方式：
- 输入数字（例如 `1 3 5`）来应用建议
- 输入 `all` 来应用所有建议
- 输入 `none` 来取消建议

### suggest_tags.py

根据笔记内容和档案中的现有标签来建议标签：

```bash
python3 scripts/suggest_tags.py my-note.md              # Interactive mode
python3 scripts/suggest_tags.py my-note.md --apply all  # Add all suggested
python3 scripts/suggest_tags.py my-note.md --apply existing  # Only existing tags
python3 scripts/suggest_tags.py my-note.md --frontmatter     # Add to frontmatter
```

该脚本：
1. 从笔记内容中提取关键词
2. 查找匹配的现有标签（包括使用频率）
3. 根据内容分析建议新标签

结果以编号列表的形式呈现，分为两部分：
- **现有标签** — 已在您的档案中使用的标签
- **新建议** — 从当前笔记内容中提取的标签

响应方式：
- 输入数字（例如 `1 3 5`）来选择标签
- 输入 `all` 来选择所有建议
- 输入 `existing` 仅选择现有标签
- 输入 `new` 仅选择新建议
- 输入 `none` 来取消建议
- 或输入自定义标签，例如 `#mytag #project`

### delete_note.py

删除笔记（可选备份和自动处理回链）：

```bash
python3 scripts/delete_note.py "Old Note"                    # Interactive deletion
python3 scripts/delete_note.py "Old Note" --force          # Skip confirmation
python3 scripts/delete_note.py "Old Note" --backup         # Move to .foam/trash/
python3 scripts/delete_note.py "Old Note" --fix-links      # Remove wikilinks from other notes
```

**功能**：
- **备份模式**：将笔记移动到 `.foam/trash/` 而不是永久删除
- **回链检测**：显示哪些笔记链接到被删除的笔记
- **链接修复**：自动从其他笔记中移除维基链接
- **确认**：删除前会提示用户（使用 `--force` 可跳过此步骤）

### rename_note.py

重命名笔记并自动更新所有维基链接：

```bash
python3 scripts/rename_note.py "Old Name" "New Name"       # Interactive rename
python3 scripts/rename_note.py "Old Name" "New Name" --force  # Skip confirmation
```

**功能**：
- **自动更新维基链接**：找到并更新所有 `[[old-name]]` 的引用
- **文件重命名**：将文件名从 `old-name.md` 更改为 `new-name.md`
- **保留标题**：保持笔记内容不变，仅更新链接
- **确认**：删除前会显示受影响的笔记

## 何时使用此技能

在以下情况下使用此技能：
- 在 Foam 工作区创建或编辑笔记
- 处理维基链接、回链或知识图谱
- 分析笔记之间的关系和联系
- 设置或配置 Foam 模板
- 使用每日笔记或标签
- 将 Foam 工作区发布到静态网站

## Foam 工作区结构

```
foam-workspace/
├── .vscode/
│   ├── extensions.json      # Recommended extensions
│   └── settings.json        # VS Code settings
├── .foam/
│   └── templates/           # Note templates (.md and .js)
├── journals/                # Daily notes (default location)
├── attachments/             # Images and files
├── *.md                     # Your notes
└── foam.json (optional)     # Foam configuration
```

## 核心概念

### 维基链接

使用双括号创建笔记之间的链接：

```markdown
See also [[related-concept]] for more information.
```

- 使用 `[[` + 输入笔记名称进行自动补全
- 通过 `Ctrl+Click`（或在 Mac 上使用 `Cmd+Click`）导航
- 点击不存在的链接可以创建新笔记
- 链接到笔记的特定部分：`[[note-name#Section Title]]`

请参阅 `references/wikilinks.md` 以获取完整文档。

### 回链

回链显示哪些笔记引用了当前笔记——由 Foam 自动检测。

**访问方式**：
- 命令面板：选择 “Explorer: Focus on Connections”
- 可以查看前向链接、回链或两者

**使用回链的方式**：
- 发现想法之间的意外关联
- 识别核心概念（具有许多回链的笔记）
- 在不同领域之间构建想法的上下文

请参阅 `references/backlinks.md` 以获取完整文档。

### 标签

**通过标签进一步组织笔记**：

```markdown
# Inline tags
#machine-learning #research #in-progress

# Frontmatter tags
---
tags: [machine-learning, research, in-progress]
---
```

- 分层结构：`#programming/python`
- 在标签浏览器面板中浏览
- 使用命令 `Foam: Search Tag` 进行搜索

请参阅 `references/tags.md` 以获取完整文档。

### 每日笔记

**快速创建每日日志**：
- **快捷键**：`Alt+D`
- **命令**：`Foam: Open Daily Note`
- **模板**：`.foam/templates/daily-note.md`

请参阅 `references/daily-notes.md` 以获取完整文档。

### 模板

自定义笔记创建方式。Foam 会在 `.foam/templates/` 目录中查找模板。

**初始化模板的方法**：

```bash
python3 scripts/init_templates.py
```

这将官方的 Foam 模板复制到您的工作区：
- `new-note.md` — 默认模板
- `daily-note.md` — 每日笔记模板
- `your-first-template.md` — 包含 VS Code 代码片段的示例模板

**Markdown 模板**（`.md` 文件）：
```markdown
---
foam_template:
  filepath: '$FOAM_CURRENT_DIR/$FOAM_SLUG.md'
---

# $FOAM_TITLE

Created: $FOAM_DATE_YEAR-$FOAM_DATE_MONTH-$FOAM_DATE_DATE

$FOAM_SELECTED_TEXT
```

**JavaScript 模板**（`.js` 文件）——用于创建智能、上下文相关的模板。

请参阅 `references/templates.md` 以获取完整文档。

## 常见任务

### 创建新笔记

1. 使用 “Foam: Create New Note” 创建新笔记（使用默认模板）
2. 使用 “Foam: Create New Note From Template” 选择模板
3. 或者点击不存在的维基链接 `[[new-note]]`

### 查找笔记之间的关系

1. **回链**：在 “Connections” 面板中查看关联的笔记
2. **图形视图**：使用命令 “Foam: Show Graph” 查看笔记之间的网络关系
3. **标签浏览器**：按标签浏览笔记

### 使用嵌入内容

从其他笔记中插入内容：

```markdown
![[glossary]]

See the full definition above.
```

### 发布

Foam 可以将笔记发布到静态网站：
- GitHub Pages（内置模板）
- Netlify
- Vercel
- GitLab Pages
- 自定义静态网站生成器（如 Gatsby、MkDocs 等）

请参阅 Foam 文档中的发布选项。

## Foam 与 Obsidian 的比较

| 特性 | Foam | Obsidian |
|---------|------|----------|
| 维基链接 | `[[note]]` | `[[note]]` |
| 嵌入内容 | `![[note]]` | `![[note]]` |
| 平台 | VS Code | 专用应用程序 |
| 插件生态系统 | 基础（VS Code 扩展） | 丰富 |
| 文件格式 | 标准 Markdown | 带有扩展的 Markdown |
| 配置 | `.vscode/settings.json` | `.obsidian/` 文件夹 |
| 价格 | 免费 | 奉献版 |

两者都使用相同的链接语法。Foam 更注重简洁性和标准格式。

## 配置

**重要的 `.vscode/settings.json` 选项**：

```json
{
  "foam.openDailyNote.onStartup": true,
  "foam.dateSnippets.format": "yyyy-mm-dd",
  "markdown.styles": [".foam/css/custom.css"]
}
```

## Foam 命令行接口（CLI）命令

**重要的 VS Code 命令**：
- `Foam: Open Daily Note` — 创建/打开今天的笔记
- `Foam: Create New Note` — 使用默认模板创建新笔记
- `Foam: Create New Note From Template` — 选择模板创建新笔记
- `Foam: Create New Template` — 创建新模板
- `Foam: Show Graph` — 可视化知识图谱
- `Foam: Search Tag` — 搜索带有标签的笔记
- `Explorer: Focus on Connections` — 显示回链面板

## 参考文档

- **foam-overview.md** — Foam 的概述和理念
- **wikilinks.md** — 维基链接的完整指南
- **backlinks.md** — 回链和知识发现
- **tags.md** — 标签的组织和过滤
- **daily-notes.md** — 每日笔记的工作流程
- **templates.md** — 模板的创建（Markdown 和 JavaScript）

请阅读这些文件以获取有关特定功能的详细信息。

## 外部资源

- **官方网站**：https://foamnotes.com
- **GitHub**：https://github.com/foambubble/foam
- **Discord**：https://foambubble.github.io/join-discord/w

## 提示

1. **从小处开始**：Foam 在您养成一致的笔记习惯时效果最佳
2. **自由使用链接**：即使是对不存在的笔记，也要创建维基链接
3. **利用知识图谱**：可视化您的知识网络以发现不足之处
4. **信任这个过程**：回链会揭示您未预料到的关联
5. **保持标准**：Foam 使用标准 Markdown — 您的笔记具有可移植性