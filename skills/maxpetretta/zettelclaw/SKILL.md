---
name: zettelclaw
description: "在 Zettelclaw 仓库中工作时，需要使用当前的前置内容（frontmatter）格式、收件箱（inbox）功能以及基础工作流程（Base workflows），同时遵循人工编写/代理读取（human-write/agent-read）的规则。这些功能适用于创建、更新、整理或搜索 Zettelclaw 仓库中的笔记，包括处理收件箱中的内容、使用 `/ask` 命令进行查询，以及构建笔记的框架结构（journal scaffolding）。"
---
# Zettelclaw

遵循 Zettelclaw 的标准存储模型：从外部捕获信息，手动创建持久性的笔记，并使用代理工具进行导航和内容整合。

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

在每条笔记中使用 YAML 标头信息：

- 所有笔记都必须包含的字段：
  - `type`
  - `tags`
  - `created`
- `doc` 类型和内容笔记还必须包含的字段：
  - `status`（`queued` | `in-progress` | `done` | `archived`）
- 可选的内容元数据：
  - `author`
  - `source`

主要的笔记类型包括：
- `note`：用于记录持久性思考内容的笔记；不包含 `status` 字段
- `doc`：用于记录工作或参考信息的笔记；包含 `status` 字段
- `journal`：用于记录日常活动的笔记；不包含 `status` 字段
- 可用的内容类型包括：`article`、`book`、`movie`、`tv`、`youtube`、`tweet`、`podcast`、`paper`（以及其他可扩展的内容类型）；这些类型都包含 `status` 字段

## 模板

在创建笔记之前，请务必阅读 `03 Templates/` 目录下的相应模板：
- `note.md`
- `journal.md`
- `clipper-capture.json`

请使用核心模板和日期格式化规则；无需使用额外的模板生成工具。

## 收件箱工作流程

- 通过 `clipper-capture.json` 将捕获的信息保存到 `00 Inbox/` 目录中。
- Clipper 会根据 URL 自动设置笔记的类型（如 `tweet`、`youtube` 等），并将状态设置为 `queued`。
- 对收件箱中的笔记进行处理：保留、移动、转换为 `note` 类型或删除。
- 除非用户明确要求，否则不要从捕获的内容自动生成持久性的思考笔记。

## 基础工作流程

- `00 Inbox/inbox.base` 是标准的笔记队列视图。
- 笔记按类型分组，以便按内容类型进行分类和管理。
- 建议直接创建或编辑 `.base` 文件，而不是使用 Dataview 工具。

## 标题的作用

笔记的标题就是它的“接口”。请使用完整、描述性的标题，例如：“间隔重复法之所以有效，是因为便于检索”（“Spaced Repetition Works Because of Retrieval”），而不是简单的“间隔重复”（“Spaced Repetition”）。一个标题清晰的笔记无需打开即可被链接和理解。在创建或重命名笔记时，始终使用完整的描述性语句。

## 标签使用规范

标签应放在标头信息中的 `tags` 数组里，而不是直接写在笔记正文中：
- 使用小写字母和连字符，例如：`spaced-repetition`，而不是 `Spaced Repetition` 或 `spacedRepetition`。
- 标签应与笔记的主题相关，而不是反映作者的感受。
- 仅在需要层次结构时才进行嵌套；例如 `ai/transformers` 是合适的，但深层嵌套并不推荐。
- 标签的选取应基于现有的分类系统，而不是随意发明新的标签。

## 编辑规则

- 除非用户要求，否则保持原有的文本内容不变。
- 不要添加或修改 `updated` 标头字段。
- 使用密集的维基链接（`[[Note Title]]`），并允许未解析的链接作为占位符。
- 除非用户明确要求，否则不要创建顶层文件夹。
- 未经明确指示，不要更改笔记的状态、移动或删除笔记。
- 代理工具的写入功能仅限于：
  - 发送请求（`/ask`）
  - 日志中的可选每日简报内容

## 搜索模式

默认的搜索路径包括：
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

## OpenClaw 集成

如果需要配置 OpenClaw 的内存路径，请使用以下设置：
- `agentsdefaults.memorySearch.extraPaths`

请不要使用旧的、顶层的 `memorySearch` 设置。