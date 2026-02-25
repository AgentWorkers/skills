---
name: brain
version: 1.3.0
description: >
  这是一个用于捕获和检索关于人物、地点、餐厅、游戏、科技、事件、媒体、想法和组织的信息的个人知识库。  
  使用场景：当用户提到某个人物、地点、餐厅、地标、游戏、设备、事件、书籍/节目或公司时。  
  触发短语：「记得」、「请注意」、「我遇到过这个人」、「我去过那里」、「玩过这个游戏」、「我对……了解多少」等。  
  对于已命名的实体，知识库中的条目优先于日常日志中的记录。
setup: |
  This skill uses OpenClaw's built-in memory_search and memory_get tools for
  search and retrieval — no external dependencies required.

  Optional: For richer BM25 + vector + reranking search, enable the QMD backend:
    1. Install QMD CLI: bun install -g https://github.com/tobi/qmd
    2. Set memory.backend = "qmd" in openclaw.json
    3. Add brain/ to memory.qmd.paths in openclaw.json:
         paths: [{ name: "brain", path: "~/.openclaw/workspace/brain", pattern: "**/*.md" }]

  The skill degrades gracefully to OpenClaw's built-in search if QMD is not configured.
permissions:
  paths:
    - "~/.openclaw/workspace/brain/**"
  write: true
  attachments: true
---
# Brain Skill — 第二个知识管理系统

这是一个用于捕获和检索关于人物、地点、事物和想法的信息的个人知识管理系统。

## 何时使用此技能

在处理命名实体（如人名、地点、产品等）时，优先使用 Brain 技能而非日常日志。

在以下情况下触发此技能：
- 用户要求你记住某个人、某件事或某个地点
- 用户分享关于某个人、地点、游戏、技术、事件、媒体、想法或组织的信息
- 用户对某个实体表达偏好（例如：“我喜欢 Y 餐厅的 X 食物” → 更新该实体的信息）
- 用户询问可能存储在 Brain 中的内容（例如：“那个叫……的人是谁？”、“我之前想到什么了？”）
- 用户更新现有的知识（例如：“实际上，他现在 27 岁了”或“我玩完了那个游戏”）

**触发此技能的关键词：** “记住”、“记下来”、“遇到这个人”、“去过”、“玩过”、“看过”、“读过”、“想法”、“我知道什么”、“谁是……”、“在哪里”

**⚠️ 请勿将适合存储在 Brain 中的内容放入日常日志中。** 如果是命名实体（如人名、地点、餐厅、产品、游戏等），应将其保存在 `brain/` 目录下，而非 `memory/YYYY-MM-DD.md` 文件中。日常日志仅用于记录会话上下文和临时笔记。

**🚨 媒体文件必须保存。** 当用户发送与 Brain 条目相关的照片/音频/视频/PDF 文件时，必须将这些文件保存到 `attachments/` 目录中。仅仅转录内容是不够的，必须同时保存文件本身。

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

## 搜索与检索

此技能使用 OpenClaw 内置的 `memory_search` 和 `memory_get` 工具，这些工具可以与任何配置好的内存后端无缝配合使用。

### 搜索

使用 `memory_search` 进行所有 Brain 数据的搜索：

```
memory_search("Raven Duran")              # find a person
memory_search("Mamou Prime restaurant")   # find a place
memory_search("what games has Raven played") # natural language
```

无论后端是内置的 SQLite 索引器还是 QMD，`memory_search` 都能正常工作。无需直接调用 CLI 命令。

### 读取文件

在知道文件路径后，使用 `memory_get` 来读取特定的 Brain 文件：

```
memory_get("brain/people/raven-duran.md")
memory_get("brain/places/mamou-prime-sm-podium/mamou-prime-sm-podium.md")
```

### 直接使用 CLI（可选/仅限高级用户）

仅在搜索非工作空间集合（例如 `skills` 集合）时才直接使用 `qmd` CLI。对于所有 Brain 数据的搜索，建议使用 `memory_search`。

```bash
# Only for skills collection or non-workspace paths:
export PATH="$HOME/.bun/bin:$PATH"
qmd search "keyword" -c skills
```

## 操作规则

### 创建新条目

1. **先搜索** — 运行 `memory_search("<名称或主题>`) 以检查是否存在现有条目
2. **没有匹配结果** — 使用 `skills/brain/templates/` 目录中的相应模板创建新文件
3. **可能存在重复条目** — 列出所有匹配结果，让用户确认后再创建新条目

### 更新现有条目

1. **找到文件** — 使用 `memory_search` 或直接提供文件路径
2. **精确编辑** — 仅更新相关部分，不要重写整个文件
3. **记录日期** — 在“备注”或“互动记录”部分添加时间戳
4. **更新文件头信息** — 更新 `last_updated` 字段

### 搜索与检索

1. **使用 `memory_search` 进行查询** — 通过自然语言问题进行语义搜索
2. **结果不明确** — 将所有匹配结果展示给用户，让用户选择正确的条目
3. **没有找到结果** — 告诉用户未找到相关内容，并建议创建新条目

## 消歧义机制

当用户提到模糊的信息（例如：“John”）时：

1. 使用 `memory_search("John")` 在 Brain 中搜索所有匹配项
2. 如果有多个结果：列出所有结果并提供上下文信息
   ```
   Found 2 matches for "John":
   1. John Smith (Symph colleague, met 2024)
   2. John Doe (GeeksOnABeach speaker, met 2026)
   Which one?
   ```
3. 在更新条目之前等待用户的确认

## 模板

模板保存在 `skills/brain/templates/` 目录下。每个模板包含：
- 用 YAML 编写的结构化文件头
- 包含标准部分的 Markdown 正文

创建新条目时：
1. 读取相应的模板
2. 填写已知的信息
3. 未知字段保持空白或使用占位符
4. 将文件保存为 `brain/<类别>/<slug>.md` 格式

## 类别参考

| 类别 | 目录 | 用途 |
|----------|--------|---------|
| 人物 | `brain/people/` | 用户遇到或需要记住的人 |
| 地点 | `brain/places/` | 餐厅、地标、场所、位置 |
| 游戏 | `brain/games/` | 视频游戏——状态、评价、笔记 |
| 技术 | `brain/tech/` | 设备、产品、规格、特性 |
| 事件 | `brain/events/` | 会议、聚会、活动 |
| 媒体 | `brain/media/` | 书籍、节目、电影、播客 |
| 想法 | `brain/ideas/` | 商业想法、概念、随机思考 |
| 组织 | `brain/orgs/` | 公司、社区、团体 |

## 链接实体

使用维基链接风格来引用实体：
- `[[people/raven-duran]]` — 链接到一个人
- `[[events/geeksonabeach-2026]]` — 链接到一个事件
- `[[orgs/symph]]` — 链接到一个组织

这样可以明确表示实体之间的关系，并便于搜索。

## 示例工作流程

**用户说：** “嘿，我刚遇到一个叫 Raven Duran 的人。他在去年二月参加了 GeeksOnABeach PH 活动。”**

**助手操作：**
1. `memory_search("Raven Duran")` → 无结果
2. 读取 `skills/brain/templates/person.md` 模板
3. 使用模板创建 `brain/people/raven-duran.md` 文件
4. （可选）创建并链接 `brain/events/geeksonabeach-ph-2026.md` 文件

**用户说：** “Raven Duran 现在还是 26 岁。”

**助手操作：**
1. `memory_search("Raven Duran")` → 找到 `brain/people/raven-duran.md`
2. 通过 `memory_get("brain/people/raven-duran.md`) 读取文件，并在文件头信息中更新年龄为 26 岁
3. 添加备注：“- **2026-02-21**：确认年龄为 26 岁”
4. 更新 `last_updated` 字段

## 附件

Brain 条目可以包含附件：照片、PDF、视频、音频、转录文本等。

### 🚨 强制要求：保存所有媒体文件

**当用户发送与 Brain 条目相关的任何媒体文件（照片、音频、视频、PDF）时：**

1. **必须将文件本身保存到 `attachments/` 目录中** — 这是必须遵守的规定
2. **之后再将内容分析或转录到个人资料中**
3. **切勿仅因为处理了内容就忽略保存文件**

**“保存”意味着文件确实存在于 `attachments/` 目录中，而不仅仅是内容被转录了。**

```bash
# REQUIRED: Copy the file
cp /path/to/inbound/media.jpg brain/places/entry/attachments/descriptive-name.jpg
```

如果你转录了内容但未保存文件 → 说明你的操作有误。请返回并保存文件。

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

### 附件索引 (`attachments/index.md`)

**如果启用了 QMD，该文件会被索引，从而可以通过描述来搜索附件。**

### 添加附件

当用户提供关于某个实体的媒体文件时（例如：“这是 Mamou Prime 的菜单”）：

1. **找到相关条目** — `memory_search("Mamou Prime")` → 找到 `brain/places/mamou-prime-sm-podium.md`
2. **如果文件是纯文本格式，将其转换为文件夹结构：**
   ```bash
   # Create folder
   mkdir -p brain/places/mamou-prime-sm-podium/attachments
   # Move profile into folder
   mv brain/places/mamou-prime-sm-podium.md brain/places/mamou-prime-sm-podium/
   # Create attachments index
   touch brain/places/mamou-prime-sm-podium/attachments/index.md
   ```

3. **将媒体文件保存到 `attachments/` 目录中，并附上描述性文件名**
4. **更新 `attachments/index.md` 文件，添加文件描述**

### ⚠️ 必须同时保存原始文件

**必须同时完成以下两步：**
1. **分析/转录文件内容** — 将处理后的文本添加到个人资料中（例如菜单列表、名片信息、转录文本）
2. **保存原始文件** — 将原始文件保存在 `attachments/` 目录中**

文件内容可以被搜索和处理，原始文件也需要被保留。除非用户明确要求“清理”、“删除”这些文件，否则切勿删除它们。

**示例：** 用户发送菜单照片
- ✅ 将菜单内容转录为 Markdown 格式的表格并保存到个人资料中
- ✅ 将原始照片保存为 `attachments/menu-1.jpg`、`menu-2.jpg`
- ✅ 更新 `attachments/index.md`

**错误做法：** 仅转录内容而不保存原始文件

### 附件命名

附件文件名应具有描述性，以便索引能够正确识别文件内容：
- `menu-1.jpg`、`menu-2.jpg`
- `business-card.jpg`
- `product-demo.mp4`
- `meeting-transcript.md`
- `voice-memo-2026-02-21.mp3`

### 示例：添加菜单照片

**用户发送：** 两张菜单照片，并附上信息“Mamou Prime 的菜单”

**助手操作：**
1. 通过 `memory_search("Mamou Prime")` 找到相关条目
2. （如有需要）将文件转换为文件夹结构
3. **分析照片内容** — 将菜单项和价格信息转录为 Markdown 格式的表格
4. **更新个人资料中的菜单部分**
5. **将原始照片保存为 `attachments/menu-1.jpg`、`menu-2.jpg`
6. **更新 `attachments/index.md` 文件：**
   ```markdown
   # Attachments

   | File | Description | Added |
   |------|-------------|-------|
   | menu-1.jpg | Menu page 1 (transcribed to profile) | 2026-02-21 |
   | menu-2.jpg | Menu page 2 (transcribed to profile) | 2026-02-21 |
   ```
7. **告知用户：** “菜单内容已转录并保存为 `menu-1.jpg` 和 `menu-2.jpg`