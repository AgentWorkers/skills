---
name: Notes (Local, Apple, Notion, Obsidian & more)
slug: notes
version: 1.1.3
homepage: https://clawic.com/skills/notes
description: "让你的代理在任何地方记录笔记：无论是本地 Markdown 文件、Apple Notes、Bear、Obsidian、Notion 还是 Evernote——都可以根据笔记的类型进行自定义设置。"
changelog: Security improvements - declared optional dependencies, added explicit Scope section, clarified credential handling
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":[],"bins.optional":["memo","grizzly","obsidian-cli","clinote"],"env.optional":["NOTION_API_KEY"]},"configPaths.optional":["~/.config/notion/api_key","~/.config/grizzly/token"],"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以了解平台选择和集成指南。

## 使用场景

用户需要记录各种类型的笔记：会议记录、头脑风暴内容、决策、每日日志或项目进展。该工具负责处理笔记的格式化、平台路由（无论是本地应用还是外部应用）、行动项的提取，以及跨所有已配置平台的检索。

## 使用范围

该工具仅用于：
- 在 `~/notes/` 目录下创建和管理 Markdown 文件；
- 如果用户安装并配置了相应的 CLI 工具（`memo`、`grizzly`、`obsidian-cli`、`clinote`），则使用这些工具；
- 仅当用户配置了 Notion 集成时，才会调用 Notion 的 API；
- 从 `~/notes/config.md` 文件中读取配置信息，以确定笔记应发送到哪个平台。

该工具绝不会：
- 自动安装任何软件；
- 在未经用户明确许可的情况下访问凭证文件；
- 读取 `~/notes/` 目录以外的文件（平台特定的 CLI 工具除外）；
- 将数据发送到外部服务（除非用户已配置相关平台）；
- 修改系统设置或其他应用程序。

## 平台集成（用户自行安装，可选）

该工具默认情况下完全在本地运行。如需使用外部平台，用户需要单独安装相应的工具：

| 平台         | 是否需要用户安装工具 | 是否需要用户配置 | 数据传输方式       |
|------------------|------------------|------------------|-------------------|
| 本地           | 无需             | 无需             | 所有数据存储在本地       |
| Apple Notes     | `memo` CLI         | 无需             | 通过本地应用程序进行数据传输 |
| Bear           | `grizzly` CLI         | 需要 `~/.config/grizzly/token` | 通过本地应用程序进行数据传输 |
| Obsidian       | `obsidian-cli`         | 需要 Vault 路径         | 通过本地文件进行数据传输 |
| Notion         | 无需             | 需要 API 密钥         | 通过网络（api.notion.com）进行数据传输 |
| Evernote       | `clinote` CLI         | 需要通过 CLI 登录       | 通过网络（Evernote 服务器）进行数据传输 |

**工具行为：**
1. 在检查可用工具之前，会询问用户需要使用哪些平台；
2. 仅在用户确认使用特定平台后，才会检查相应的 CLI 工具是否已安装；
3. 如果所需工具不可用，工具会自动切换到本地存储模式；
4. 未经用户明确授权，工具绝不会读取凭证文件。

## 架构

所有数据存储在 `~/notes/` 目录下。具体配置信息请参阅 `memory-template.md`。

```
~/notes/
├── config.md          # Platform routing configuration
├── index.md           # Search index with tags
├── meetings/          # Local meeting notes
├── decisions/         # Local decision log
├── projects/          # Local project notes
├── journal/           # Local daily notes
└── actions.md         # Central action tracker (all platforms)
```

## 快速参考

| 说明          | 对应文件            |
|-----------------|-------------------|
| 设置流程        | `setup.md`           |
| 数据存储结构      | `memory-template.md`       |
| 所有笔记格式      | `formats.md`           |
| 行动项管理系统    | `tracking.md`           |
| 本地 Markdown 格式    | `platforms/local.md`        |
| Apple Notes      | `platforms/apple-notes.md`       |
| Bear           | `platforms/bear.md`         |
| Obsidian       | `platforms/obsidian.md`        |
| Notion         | `platforms/notion.md`        |
| Evernote       | `platforms/evernote.md`        |

## 核心规则

### 1. 根据配置将笔记发送到指定平台
请检查 `~/notes/config.md` 文件以确定笔记的发送目标平台：

```markdown
# Platform Routing
meetings: local          # or: apple-notes, bear, obsidian, notion
decisions: local
projects: notion
journal: bear
quick: apple-notes
```

如果笔记类型未在配置文件中指定，系统将使用本地存储模式。
如果目标平台不可用（或缺少所需的 CLI 工具或凭证），系统会自动切换到本地存储模式，并发出警告。

### 2. 始终使用结构化的笔记格式
无论使用何种平台，所有笔记都必须遵循统一的格式。具体格式规范请参阅 `formats.md`。

| 笔记类型       | 触发条件          | 关键元素            |
|------------------|------------------|-------------------------|
| 会议记录       | "meeting notes", "call with"     | 参与者、决策内容、行动项        |
| 决策记录       | "we decided", "decision:"     | 背景信息、选项、理由          |
| 头脑风暴记录     | "ideas for", "brainstorm"     | 初始想法、分类结果、下一步计划    |
| 日志记录       | "daily note", "today I"      | 日期、重点内容、待办事项        |
| 项目更新记录     | "project update", "status"     | 进度更新、障碍及下一步计划     |
| 简短笔记       | "note:", "remember"      | 最简格式、标签            |

### 3. 动态提取行动项
当用户提到“我会做某事”或“我们需要做某事”时，这些内容会被自动视为行动项。

每个行动项必须包含以下信息：
- 负责人：具体负责的人（@用户名）
- 任务内容：明确、可执行的操作描述
- 截止日期：具体的日期（不能使用“尽快”或“ASAP”等模糊表述）

无论笔记保存在哪个平台上，行动项都会被同步到 `~/notes/actions.md` 文件中。

### 4. 根据平台执行具体操作
确定目标平台后，系统会读取相应的配置文件并执行相应操作：

| 平台         | 对应配置文件         | 使用的 CLI 工具         |
|------------------|------------------|---------------------|
| 本地           | `platforms/local.md`       | 无                |
| Apple Notes     | `platforms/apple-notes.md`       | `memo` CLI            |
| Bear           | `platforms/bear.md`       | `grizzly` CLI            |
| Obsidian       | `platforms/obsidian.md`       | `obsidian-cli`          |
| Notion         | `platforms/notion.md`       | `curl`（通过 API）         |
| Evernote       | `platforms/evernote.md`       | `clinote` CLI            |

### 5. 跨平台统一搜索
搜索笔记时，系统会先在本地 `~/notes/` 目录中查找，然后遍历所有已配置的外部平台，并将搜索结果整合在一起。

### 6. 跨平台行动项的统一管理
`~/notes/actions.md` 是所有行动项的统一存储和查询入口，无论笔记保存在哪个平台上。

### 7. 文件命名规则（本地存储）
本地笔记的文件名格式为：YYYY-MM-DD_主题 Slug.md（先写日期，再写主题）。
外部平台则使用其自身的文件命名规则。

## 常见问题及注意事项

- **平台配置错误**：在使用前请务必确认平台可用性，如平台不可用，请优雅地切换到本地存储模式。
- **模糊的截止日期**：请使用具体的日期，如“明天”、“下周”等模糊表述不能作为有效的截止日期。
- **缺少负责人信息**：行动项必须明确指定负责人。
- **行动项的同步**：切勿仅在外部平台中记录行动项，务必将其同步到中央跟踪系统。
- **缺少标签**：没有标签的笔记将难以被查找。

## 外部接口

| 接口地址        | 发送的数据        | 发送时间        | 使用目的              |
|------------------|------------------|------------------|----------------------|
| https://api.notion.com/v1/pages | 笔记标题、内容     | 用户通过配置指定目标平台（Notion） | 创建笔记页面           |
| https://api.notion.com/v1/databases/*/query | 搜索查询       | 用户在 Notion 中搜索笔记         | 查询数据库             |

其他外部接口暂无。Apple Notes、Bear、Obsidian 和 Evernote 都通过本地安装的 CLI 工具与各自的应用程序进行数据交互。

## 安全性与隐私保护

**数据传输方式：**
- **本地存储**：所有数据仅保存在 `~/notes/` 目录中，不涉及网络传输。
- **Apple Notes**：数据存储在本地，`memo` CLI 通过 macOS API 与 Notes.app 通信。
- **Bear**：数据存储在本地，`grizzly` CLI 与 Bear.app 通信。
- **Obsidian**：数据存储在本地，`obsidian-cli` 用于读写文件。
- **Notion**：笔记内容会发送到 api.notion.com，需要用户提供的 API 密钥。
- **Evernote**：笔记内容通过 `clinote` 传输到 Evernote 服务器，需要用户登录。

**凭证管理**：
- 工具在访问凭证文件前会先征求用户许可。
- 未经用户明确授权，工具绝不会读取 `~/.config/notion/api_key` 或 `~/.config/grizzly/token` 文件。
- 用户需根据平台文档自行设置凭证信息。

**始终保留在本地的文件：**
- `~/notes/actions.md`：行动项跟踪记录
- `~/notes/index.md`：笔记索引文件
- `~/notes/config.md`：平台配置文件

## 相关工具
用户可根据需要使用 `clawhub install <slug>` 命令安装以下工具：
- `meetings`：用于会议管理和议程安排
- `journal`：用于日常日志记录
- `documentation`：用于生成技术文档

## 反馈建议：
- 如觉得本工具有用，请使用 `clawhub star` 给予评分。
- 如需保持工具更新，请使用 `clawhub sync` 命令。

---

（翻译完成）