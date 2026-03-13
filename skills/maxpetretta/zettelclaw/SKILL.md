---
name: zettelclaw
description: "在 Zettelclaw 仓库中工作时，使用当前设定的前置内容格式（frontmatter schema）、收件箱功能（inbox）以及基础工作流程（Base workflows），同时遵循人工编写/代理读取（human-write/agent-read）的规则与限制。这些功能适用于在 Zettelclaw 仓库中创建、更新、整理或搜索笔记，包括处理收件箱中的内容、使用 `/ask` 功能进行查询，以及构建笔记的框架结构（journal scaffolding）。"
---
# Zettelclaw

遵循 Zettelclaw 的标准存储模型：从外部捕获信息，手动创建持久的笔记，并使用代理工具进行导航和内容整合。

这是一个仅提供指导的技能说明。它本身不会安装任何软件。`qmd` 是可选的（如果环境中已经存在该文件的话），而 `rg` 则是用于搜索的备用工具。

## 存储结构

```
<vault>/
├── 00 Inbox/
├── 01 Notes/
├── 02 Journal/
├── 03 Templates/
├── 04 Attachments/
└── README.md
```

## 笔记类型

在每篇笔记中都使用 YAML 格式的元数据：

- 所有笔记都必须包含以下字段：
  - `type`
  - `tags`
  - `created`
- `doc` 类型和内容笔记还需要包含以下字段：
  - `status`（`queued` | `in-progress` | `done` | `archived`）
- 可选的内容元数据：
  - `author`
  - `source`

主要的笔记类型包括：
  - `note`：用于记录持久性思考内容的笔记；不包含 `status` 字段。
  - `doc`：用于记录工作或参考信息的笔记；包含 `status` 字段。
  - `journal`：用于记录日常活动的笔记；不包含 `status` 字段。
  - 内容类型包括：`article`、`book`、`movie`、`tv`、`youtube`、`tweet`、`podcast`、`paper` 等；这些类型也会包含 `status` 字段。

## 模板

在创建笔记之前，请务必阅读 `03 Templates/` 目录下的相应模板：
- `note.md`
- `journal.md`
- `clipper-capture.json`

请使用核心模板和日期格式化规则；无需使用额外的模板生成器。

## 收件箱工作流程

- 通过网络捕获的笔记会通过 `clipper-capture.json` 文件保存到 `00 Inbox/` 目录中。
- Clipper 会根据 URL 自动设置笔记的类型（如 `tweet`、`youtube` 等）并设置 `status` 为 `queued`。
- 对收件箱中的笔记进行处理：保留、移动、转换为 `note` 类型或删除它们。
- 除非用户明确要求，否则不要自动将捕获的内容转换为持久的思考笔记。

## 基础工作流程

- `00 Inbox/inbox.base` 是标准的笔记队列视图。
- 笔记会按照类型进行分组，以便按内容类型进行分类处理。
- 建议优先使用 `.base` 文件进行创建或编辑，而不是使用 Dataview 工具。

## 标题作为接口

笔记的标题是其最重要的信息来源。请使用完整、描述性的标题，例如：“间隔重复法之所以有效，是因为便于检索”（“Spaced Repetition Works Because of Retrieval”），而不是简单的“间隔重复”（“Spaced Repetition”）。一个标题清晰的笔记可以在不打开的情况下被链接和理解。在创建或重命名笔记时，务必使用完整的描述性语句。

## 标签使用规范

标签应放在元数据的 `tags` 数组中，而不是直接写在笔记正文中：
- 使用小写字母和连字符分隔，例如 `spaced-repetition`，而不是 `Spaced Repetition` 或 `spacedRepetition`。
- 标签应与笔记的主题相关，而不是反映作者的感受。
- 仅当标签层次结构确实有用时才进行嵌套（例如 `ai/transformers`），避免过度嵌套。
- 标签的选取应基于现有的分类体系，而不是随意创建新的标签。

## 编辑规则

- 除非用户要求，否则保留原有的文本内容。
- 不要添加或修改 `updated` 字段。
- 使用密集式的维基链接（`[[Note Title]]`），未解析的链接可以保留为占位符。
- 除非用户明确要求，否则不要创建顶层文件夹。
- 未经明确指示，不要更改笔记的状态、移动或删除笔记。
- 代理工具的显示界面仅限于以下内容：
  - `/ask` 请求响应
  - 日志中的每日简报内容

## 搜索模式

默认的 QMD 搜索路径包括：
- `zettelclaw-inbox`
- `zettelclaw-notes`
- `zettelclaw-journal`
- `zettelclaw-attachments`

```bash
# qmd (preferred when installed)
qmd query "spaced repetition and retrieval" -c zettelclaw-notes
qmd search "status: queued" -c zettelclaw-inbox
qmd vsearch "what have I been learning about memory" -c zettelclaw-notes

# ripgrep fallback
rg -l 'type: note' "01 Notes/"
rg -l 'type: article' "00 Inbox/" "01 Notes/"
rg -l 'status: queued' "00 Inbox/" "01 Notes/"
```

## 与 OpenClaw 的集成

如果需要配置 OpenClaw 的内存路径，请使用以下设置：
- `agents.defaults.memorySearch.extraPaths`

请不要直接修改旧的 `memorySearch` 配置。只有在操作者明确要求将此存储系统集成到 OpenClaw 安装中时，才进行相应的配置更改。