---
name: foam-notes
description: >
  **使用 Foam 笔记库**  
  您可以创建、编辑、链接和标记笔记；系统会提供智能的维基链接和标签建议。该技能还支持反向链接的检测、每日笔记的生成、模板的应用、笔记的可视化展示以及笔记的删除和重命名功能。完整的 Foam 文档可供查阅，便于您快速了解使用方法。
---
# Foam 文本编辑器使用指南

在 VS Code 中使用 Foam 文本编辑器进行笔记管理。[Foam](https://foamnotes.com) 是一个免费、开源的个人知识管理系统，它使用标准的 Markdown 文件格式，并支持wikilinks（超链接）。

## 快速参考

- **Wikilinks**：`[[note-name]]` — 实现笔记之间的双向链接
- **嵌入内容**：`![[note-name]]` — 在当前笔记中嵌入其他笔记的内容
- **回链**：自动检测并显示当前笔记被引用的其他笔记
- **标签**：`#tag` 或在文档开头添加 `tags: [tag1, tag2]`
- **每日笔记**：使用快捷键 `Alt+D` 或命令 `Foam: Open Daily Note` 创建每日笔记

## 配置

将 `config.json.template` 复制到 `config.json` 中，并根据需要进行修改：

**配置文件位置**：位于 `skill` 目录下的 `config.json` 文件中（与 `SKILL.md` 文件在同一目录下）。

### 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|---------|-------------|
| `foam_root` | 字符串 | `""`（自动检测） | 指定你的 Foam 工作区的路径 |
| `default_template` | 字符串 | `"new-note"` | 新笔记的模板文件名 |
| `default_notes_folder` | 字符串 | `"notes"` | 新笔记的存储文件夹 |
| `daily_note_folder` | 字符串 | `"journals"` | 日记笔记的存储文件夹 |
| `author` | 字符串 | `""` | 创建笔记时的作者名称 |
| `wikilinks.title_stopwords` | 列表 | `[]` | 避免将某些文件名（如 `"home"`、`index`、`todo`）识别为 wikilinks |
| `wikilinks.suffixes` | 列表 | `[]` | 文件名后缀，这些后缀也应被视为有效的链接键（例如，如果你的 hub/MOC 笔记文件名为 `docker-hub.md`，则在此添加 `-hub`） |
| `wikilinks.min_length` | 整数 | `3` | 用于匹配 wikilinks 的最小键长度 |
| `tags.editorial_stopwords` | 列表 | `[]` | 需要排除的特定领域词汇（除了常见的英文停用词） |

### Foam 工作区的路径优先级（从高到低）

1. 命令行参数 `--foam-root`
2. 环境变量 `FOAM_WORKSPACE`
3. `config.json` 中的 `foam_root` 设置
4. 通过查找 `.foam` 或 `.vscode` 目录自动检测
5. 当前工作目录

更多详细信息请参阅 `references/configuration.md`。

## 脚本

所有脚本都支持使用 `--foam-root` 参数来指定工作区路径。

### init_templates.py

用于初始化 `/.foam/templates/` 目录中的模板文件：

- `new-note.md` — 新笔记的默认模板
- `daily-note.md` — 日记笔记的模板
- `your-first-template.md` — 示例模板，包含 VS Code 代码片段

### create_note.py

根据模板创建新笔记：

### find_backlinks.py

查找所有引用给定笔记的笔记：

### search_tags.py

根据标签查找笔记：

### list_tags.py

列出所有标签及其使用频率：

### graph_summary.py

分析知识图谱：

### daily_note.py

创建每日笔记：

### suggest_wikilinks.py

通过分析笔记内容，建议与现有笔记标题匹配的 wikilinks：

该脚本会扫描笔记内容，找出与现有笔记标题匹配的词汇，并以编号列表的形式显示这些建议：

**Wikilink 格式：**
- **默认**：`[[target]]` — 简单的链接格式
- **使用 `--with-aliases` 选项**：`[[target|display text]]` — 保留原始文本作为链接的别名

响应方式：
- 输入数字（如 `1 3 5`）来选择建议的 wikilinks
- 输入 `all` 来应用所有建议
- 输入 `none` 来取消建议

### suggest_tags.py

根据笔记内容和现有标签建议标签：

该脚本会：
1. 从笔记内容中提取关键词
2. 查找匹配的现有标签及其使用频率
3. 根据内容分析建议新标签

结果以编号列表的形式显示：
- **Existing Tags** — 已经在笔记中使用的标签
- **New Suggestions** — 从当前笔记内容中提取的新标签

响应方式：
- 输入数字（如 `1 3 5`）来选择标签
- 输入 `all` 来查看所有建议
- 输入 `existing` 来仅查看已有的标签
- 输入 `new` 来仅查看新建议
- 输入 `none` 来取消建议
- 或者输入自定义标签（如 `#mytag #project`）

### delete_note.py

删除笔记，支持可选的备份和自动处理回链：

**功能：**
- **备份模式**：将笔记移动到 `.foam/trash/` 目录而非永久删除
- **回链处理**：显示被删除笔记引用的其他笔记
- **链接修复**：自动移除其他笔记中的相关链接
- **确认提示**：删除前会显示确认提示（使用 `--force` 可跳过此步骤）

### rename_note.py

重命名笔记并自动更新所有关联的 wikilinks：

**功能：**
- **自动更新链接**：找到并更新所有 `[[old-name]]` 格式的引用
- **文件重命名**：将文件名从 `old-name.md` 更改为 `new-name.md`
- **标题保留**：保持笔记内容不变，仅更新链接
- **确认提示**：删除前会显示受影响的笔记列表

## 适用场景

- 在 Foam 工作区创建或编辑笔记
- 处理 wikilinks、回链和知识图谱
- 分析笔记之间的关系和联系
- 配置 Foam 模板
- 管理每日笔记和标签
- 将 Foam 工作区发布到静态网站

## Foam 工作区结构

## 核心概念

### Wikilinks

使用双括号 `[[...]]` 在笔记之间创建链接：

- 使用 `[[` + 笔记名称`` 进行自动补全
- 通过 `Ctrl+Click`（Mac 上为 `Cmd+Click`）导航
- 点击不存在的链接可以创建新笔记
- 可以通过 `[[note-name#Section Title]]` 链接到笔记的特定部分

更多详细信息请参阅 `references/wikilinks.md`。

### 回链

回链显示当前笔记被哪些笔记引用，这些链接由 Foam 自动检测。

- 通过命令面板中的 “Explorer: Focus on Connections” 功能访问
- 可以查看正向链接、回链或两者

回链的用途包括：
- 发现不同想法之间的关联
- 识别核心概念（被多个笔记引用的笔记）
- 在不同领域之间建立内容联系

更多详细信息请参阅 `references/backlinks.md`。

### 标签

标签用于更细致地组织笔记内容：

- **层次结构**：例如 `#programming/python`
- 可以在 “Tag Explorer” 面板中浏览标签
- 使用命令 `Foam: Search Tag` 进行搜索

更多详细信息请参阅 `references/tags.md`。

### 日记笔记

- 快捷键：`Alt+D`
- 命令：`Foam: Open Daily Note`
- 提供预定义的模板文件：`/today`、`/yesterday`、`/tomorrow`

模板文件：`.foam/templates/daily-note.md`

更多详细信息请参阅 `references/daily-notes.md`。

### 模板

可以自定义笔记的创建方式。Foam 会在 `/.foam/templates/` 目录中查找模板文件。

**初始化模板的方法：**

将官方提供的模板文件复制到工作区：
- `new-note.md` — 新笔记的默认模板
- `daily-note.md` — 日记笔记模板
- `your-first-template.md` — 包含 VS Code 代码片段的示例模板

**Markdown 模板**（`.md` 格式）和 **JavaScript 模板**（`.js` 格式）用于自定义模板设计。

更多详细信息请参阅 `references/templates.md`。

## 常见操作

### 创建新笔记

在程序化创建笔记时（非通过 VS Code），请先阅读 `/.foam/templates/new-note.md` 中的模板文件，并严格按照其结构进行操作。

在 VS Code 中：
- 使用 “Foam: Create New Note” 创建新笔记
- 使用 “Foam: Create New Note From Template” 选择模板
- 或者点击不存在的 wikilink `[[new-note]]` 创建新笔记

### 查找笔记之间的关系

- 通过 “Connections” 面板查看笔记之间的链接关系
- 使用命令 `Foam: Show Graph` 查看笔记之间的可视化网络关系
- 使用 “Tag Explorer” 按标签浏览笔记

### 嵌入内容

可以在当前笔记中嵌入其他笔记的内容：

### 发布笔记

Foam 支持将笔记发布到静态网站：
- GitHub Pages（内置模板）
- Netlify
- Vercel
- GitLab Pages
- 其他自定义静态网站生成工具（如 Gatsby、MkDocs 等）

具体发布方法请参考 Foam 的官方文档。

## Foam 与 Obsidian 的比较

| 特性 | Foam | Obsidian |
|---------|------|----------|
| Wikilinks | `[[note]]` | `[[note]]` |
| 嵌入内容 | `![[note]]` | `![[note]]` |
| 平台 | VS Code | 专用应用程序 |
| 插件生态系统 | 简单（依赖 VS Code 扩展） | 丰富 |
| 文件格式 | 标准 Markdown | 带有扩展的 Markdown 格式 |
| 配置文件 | `.vscode/settings.json` | `.obsidian/` 文件夹 |
| 价格 | 免费 | 商业版（Freemium） |

两者都支持相同的链接语法。Foam 更注重简洁性和标准性。

## VS Code 配置选项

请参阅 `config.json` 文件中的相关设置。

## Foam 的命令行工具

- `Foam: Open Daily Note` — 打开今天的笔记
- `Foam: Create New Note` — 使用默认模板创建新笔记
- `Foam: Create New Note From Template` — 选择模板创建新笔记
- `Foam: Create New Template` — 创建新模板
- `Foam: Show Graph` — 可视化知识图谱
- `Foam: Search Tag` — 搜索带有标签的笔记
- `Explorer: Focus on Connections` — 显示回链信息

## 参考文档

- `foam-overview.md` — Foam 的概述和设计理念
- `wikilinks.md` — Wikilinks 的使用指南
- `backlinks.md` — 回链和知识发现功能
- `tags.md` — 标签的组织和管理
- `daily-notes.md` — 日记笔记的使用方法
- `templates.md` — 模板的创建方法（包括 Markdown 和 JavaScript 模板）

这些文档提供了关于 Foam 各项功能的详细信息。

## 外部资源

- **官方网站**：https://foamnotes.com
- **GitHub 仓库**：https://github.com/foambubble/foam
- **Discord 社区**：https://foambubble.github.io/join-discord/w

## 使用建议

- **从小处开始**：养成一致的笔记记录习惯
- **广泛使用链接**：即使是对不存在的笔记也要创建 wikilinks
- **利用知识图谱**：通过可视化了解知识结构中的空白部分
- **信任这个过程**：回链会揭示你未预料到的联系
- **保持格式统一**：Foam 使用标准 Markdown，确保笔记的便携性