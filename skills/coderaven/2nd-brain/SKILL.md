---
name: brain
version: 1.2.0
description: >
  这是一个用于捕获和检索关于人物、地点、餐厅、游戏、科技、事件、媒体、想法及组织信息的个人知识库。  
  使用场景：当用户提到某个人物、地点、餐厅、地标、游戏、设备、事件、书籍/节目或公司时。  
  触发短语：「记得」、「注意」、「遇到这个人」、「去过」、「玩过」、「我对……了解多少」等。  
  对于已命名的实体，知识库中的条目优先于日常记录。
---
# Brain Skill — 第二个知识管理系统

这是一个个人知识管理系统，用于记录和检索关于人物、地点、事物和想法的信息。

## 何时使用此技能

在处理命名实体（如人名、地名等）时，优先使用 Brain 而不是日常日志。

以下情况下应触发此技能：
- 用户请求您记住某个人、某件事或某个地点；
- 用户分享关于某个人、地点、游戏、技术、事件、媒体、想法或组织的信息；
- 用户对某个实体表示偏好（例如：“我喜欢 Y 餐厅的……” → 需要更新该实体的信息）；
- 用户询问可能存储在 Brain 中的内容（例如：“那个人是谁？”，“我之前想到什么了？”）；
- 用户更新现有的知识（例如：“其实他现在 27 岁了”，“我玩完了那个游戏”）。

**触发此技能的关键词：** “记住”、“记下来”、“遇到这个人”、“去过”、“玩过”、“看过”、“读过”、“想法”、“我知道什么”、“谁是……”、“在哪里”。

**⚠️ 请勿将适合存储在 Brain 中的内容放入日常日志中。** 如果是命名实体（如人名、地名、餐厅名称、产品名称、游戏名称等），应将其保存在 `brain/` 目录下，而非 `memory/YYYY-MM-DD.md` 文件中。日常日志仅用于记录会话内容和临时笔记。

## 数据存储位置

所有 Brain 数据都存储在：`~/.openclaw/workspace/brain/` 目录下。

```
brain/
  people/       # Contacts, people you've met
  places/       # Restaurants, landmarks, venues
  games/        # Video games and interactions
  tech/         # Devices, products, specs, gotchas
  events/       # Conferences, meetups, gatherings
  media/        # Books, shows, films, podcasts
  ideas/        # Business ideas, concepts, thoughts
  orgs/         # Companies, communities, groups
```

## 文件命名规则

- 使用小写字母和短横线（slug）来命名文件，例如：`raven-duran.md`、`house-of-lechon-cebu.md`；
- 为避免命名冲突，在创建文件前请向用户建议使用适当的区分符（例如：`john-smith-symph.md` 与 `john-smith-ateneo.md`）。

## 操作规则

### 创建新条目

1. **先搜索** — 使用 `qmd search "<名称或主题>"` 来检查是否已有条目；
2. **没有匹配结果** — 使用 `skills/brain/templates/` 目录下的相应模板创建新文件；
3. **可能存在命名冲突** — 列出所有可能的匹配项，并在创建前请用户确认。

### 更新现有条目

1. **找到文件** — 使用 `qmd search` 或直接访问文件路径；
2. **仅修改相关内容** — 不要重写整个文件；
3. **记录更新时间** — 在 “备注” 或 “交互记录” 部分添加时间戳；
4. **更新文件头信息** — 更新 `last_updated` 字段。

### 搜索/检索

1. **使用 QMD 进行查询** — 输入自然语言问题进行语义搜索；
2. **结果不明确** — 将所有匹配项展示给用户，并询问用户具体需要哪个条目；
3. **没有找到结果** — 告知用户未找到相关内容，并建议创建新条目。

## 名称冲突处理机制

当用户提到某个不明确的实体（例如 “John”）时：
1. 在 Brain 中搜索所有匹配项；
2. 如果有多个结果，列出所有结果并附上上下文信息；
3. 等待用户确认后再进行更新。

## 模板

所有模板都保存在 `skills/brain/templates/` 目录下。每个模板包含：
- 使用 YAML 格式的文件头（包含结构化字段）；
- 使用 Markdown 编写的正文（包含标准章节）。

创建新条目时：
1. 阅读相应的模板；
2. 填写已知的信息；
3. 将未知字段留空或使用占位符；
4. 将文件保存为 `brain/<类别>/<slug>.md` 格式。

## 类别参考

| 类别 | 目录 | 适用范围 |
|--------|---------|---------|
| 人物 | `brain/people/` | 用户遇到过或需要记住的人 |
| 地点 | `brain/places/` | 餐厅、地标、场所、位置 |
| 游戏 | `brain/games/` | 视频游戏——状态、评价、笔记 |
| 技术 | `brain/tech/` | 设备、产品、规格、特性 |
| 事件 | `brain/events/` | 会议、聚会、活动 |
| 媒体 | `brain/media/` | 书籍、节目、电影、播客 |
| 想法 | `brain/ideas/` | 商业想法、概念、随机思考 |
| 组织 | `brain/orgs/` | 公司、社区、团队 |

## 实体链接

使用维基链接（wikilink）格式来关联实体：
- `[[people/raven-duran]]` — 链接到一个人物；
- `[[events/geeksonabeach-2026]]` — 链接到一个事件；
- `[[orgs/symph]]` — 链接到一个组织。

这样可以使实体之间的关系清晰可见且可搜索。

## 示例工作流程

**用户说：** “嘿，我刚遇到一个叫 Raven Duran 的人。他在 GeeksOnABeach PH 上自我介绍是一名开发人员。”
**助手操作：**
1. 使用 `qmd search "Raven Duran"` — 没有找到匹配结果；
2. 阅读 `skills/brain/templates/person.md` 模板；
3. 使用模板创建 `brain/people/raven-duran.md` 文件；
4. （可选）创建并链接 `brain/events/geeksonabeach-ph-2026.md` 文件。

**用户说：** “Raven Duran 现在还是 26 岁。”
**助手操作：**
1. 使用 `qmd search "Raven Duran"` — 找到 `brain/people/raven-duran.md` 文件；
2. 在文件头信息中更新年龄为 26 岁；
3. 添加备注：“2026-02-21：确认他现在 26 岁”；
4. 更新 `last_updated` 字段。

## 附件

Brain 条目可以包含附件（如照片、PDF、视频、音频文件等）。

### 文件结构

- **纯文本文件（无附件）：**  
```
brain/places/manam.md
```

- **包含附件的文件夹结构：**  
```
brain/places/mamou-prime-sm-podium/
  mamou-prime-sm-podium.md      # Profile (keeps original name)
  attachments/
    index.md                    # Describes each attachment
    menu-page-1.jpg
    menu-page-2.jpg
    receipt.pdf
    storefront.mp4
```

### 附件索引（`attachments/index.md`）

`attachments/index.md` 文件用于索引附件，方便用户根据描述搜索附件。

### 添加附件

当用户提供关于某个实体的媒体文件时（例如：“这是 Mamou Prime 的菜单”）：
1. **找到相关条目** — 使用 `qmd search "Mamou Prime"`；
2. （如果文件是纯文本格式）将其转换为文件夹结构；
3. 将媒体文件保存在 `attachments/` 目录下，并为文件添加描述性名称；
4. 更新 `attachments/index.md` 文件以记录文件信息。

### 注意事项：** 请务必保存原始文件**

**请同时执行以下操作：**
1. **分析/转录文件内容** — 将处理后的内容添加到个人资料中（例如菜单列表、名片信息、会议记录）；
2. **保存原始文件** — 将原始文件保存在 `attachments/` 目录下。

文件内容可被搜索和进一步处理，原始文件需要保留。

**除非用户明确要求“清理”、“删除”文件，否则切勿删除附件。**

**示例：** 用户发送菜单照片：
- ✅ 将菜单内容转录为 Markdown 表格并保存到个人资料中；
- ✅ 将原始照片保存为 `attachments/menu-1.jpg`、`menu-2.jpg`；
- ✅ 更新 `attachments/index.md` 文件。

**错误做法：** 仅转录内容而不保存原始文件。

### 附件命名规则

附件文件名应具有描述性，以便索引系统能够识别其内容：
- `menu-1.jpg`、`menu-2.jpg`；
- `business-card.jpg`；
- `product-demo.mp4`；
- `meeting-transcript.md`；
- `voice-memo-2026-02-21.mp3`。

### 示例：添加菜单照片

**用户发送：** 两张菜单照片，并附上说明：“这是 Mamou Prime 的菜单。”

**助手操作：**
1. 找到 `brain/places/mamou-prime-sm-podium.md` 文件；
2. （如有需要）将文件转换为文件夹结构；
3. 将菜单内容转录为 Markdown 表格并保存到个人资料中；
4. 将原始照片保存为 `attachments/menu-1.jpg`、`menu-2.jpg`；
5. 更新 `attachments/index.md` 文件：
   ```markdown
   # Attachments

   | File | Description | Added |
   |------|-------------|-------|
   | menu-1.jpg | Menu page 1 (transcribed to profile) | 2026-02-21 |
   | menu-2.jpg | Menu page 2 (transcribed to profile) | 2026-02-21 |
   ```；
6. 告知用户：“已转录菜单内容并将两张照片保存到 Mamou Prime 文件夹中”。