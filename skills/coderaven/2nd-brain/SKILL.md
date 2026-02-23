---
name: brain
version: 1.2.1
description: >
  这是一个用于捕获和检索关于人物、地点、餐厅、游戏、科技、事件、媒体、想法和组织的信息的个人知识库。  
  使用场景：当用户提到某个人物、地点、餐厅、地标、游戏、设备、事件、书籍/节目或公司时。  
  触发短语：「记得」、「注意」、「遇到这个人」、「去过」、「玩过」、「我对……了解多少」等。  
  对于已命名的实体，知识库中的条目优先于日常记录。
---
# Brain Skill — 第二个知识管理系统

这是一个个人知识管理系统，用于捕获和检索关于人物、地点、事物和想法的信息。

## 何时使用此技能

在处理命名实体（如人名、地名等）时，优先使用“Brain”技能，而非日常日志。

在以下情况下触发此技能：
- 用户请求你记住某个人、某件事或某个地点；
- 用户分享关于某个人、某个地点、某款游戏、某项技术、某个事件、某种媒体、某个想法或某个组织的信息；
- 用户对某个实体表达偏好（例如：“我喜欢Y餐厅的X” → 需要更新该实体的信息）；
- 用户询问可能存储在“Brain”中的内容（例如：“那个叫……的人是谁？”、“我之前想到什么了？”）；
- 用户更新现有的知识（例如：“其实他现在27岁了”或“我玩完了那款游戏”）。

**触发该技能的关键词：** “记住”、“记下来”、“遇到这个人”、“访问过”、“玩过”、“看过”、“读过”、“想法”、“我对……了解多少”、“谁是……”、“在哪里”。

**⚠️ 请勿将适合存储在“Brain”中的内容放入日常日志中。** 如果是命名实体（如人名、地名、餐厅名称、产品名称、游戏名称等），应将其保存在`brain/`文件夹中，而非`memory/YYYY-MM-DD.md`文件中。日常日志仅用于记录会话上下文和临时笔记。

**🚨 媒体文件必须保存。** 当用户发送与“Brain”条目相关的照片、音频、视频或PDF文件时，你必须将这些文件保存到`attachments/`文件夹中。仅仅转录内容是不够的，必须同时保存原始文件。

## 数据存储位置

所有“Brain”数据都存储在：`~/.openclaw/workspace/brain/`文件夹中。

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

- 文件名采用小写形式，并使用连字符进行分隔（例如：`raven-duran.md`、`house-of-lechon-cebu.md`）；
- 为避免名称冲突，在创建文件前请务必询问用户是否需要添加区分符（例如：`john-smith-symph.md` vs `john-smith-ateneo.md`）。

## 操作规则

### 创建新条目

1. **先搜索** — 使用`qmd search "<名称或主题>"`来检查是否存在现有条目；
2. **没有匹配结果** — 使用`skills/brain/templates/`中的相应模板创建新文件；
3. **可能存在名称冲突** — 列出所有可能的匹配结果，并在创建前征求用户确认。

### 更新现有条目

1. **找到文件** — 使用`qmd search`或直接路径找到文件；
2. **精确修改** — 仅修改相关部分，不要重写整个文件；
3. **记录日期** — 在“备注”或“互动记录”部分添加时间戳；
4. **更新文件头信息** — 更新`last_updated`字段。

### 搜索/检索

1. **使用QMD查询** — 输入`qmd query "<自然语言问题>"`进行语义搜索；
2. **结果不明确** — 将所有匹配结果展示给用户，并询问用户具体需要哪个条目；
3. **没有找到结果** — 告诉用户未找到相关条目，并建议创建新条目。

## 名称冲突处理机制

当用户提及某个不确定的名称（例如“John”）时：
1. 在“Brain”中搜索所有匹配结果；
2. 如果有多个结果，列出所有结果并附上上下文信息；
3. 在更新条目前等待用户的确认。

## 模板

所有模板都保存在`skills/brain/templates/`文件夹中。每个模板包含：
- 用YAML格式编写的文件头（包含结构化字段）；
- 使用Markdown格式编写的正文（包含标准章节）。

创建新条目时：
1. 阅读相应的模板；
2. 填写已知字段；
3. 未知字段保持空白或使用占位符；
4. 将文件保存为`brain/<类别>/<slug>.md`格式。

## 类别参考

| 类别 | 文件夹 | 适用范围 |
|--------|---------|---------|
| 人物 | `brain/people/` | 用户遇到过或需要记住的人 |
| 地点 | `brain/places/` | 餐厅、地标、场所、位置 |
| 游戏 | `brain/games/` | 视频游戏——状态、评价、笔记 |
| 技术 | `brain/tech/` | 设备、产品、规格、特性 |
| 活动 | `brain/events/` | 会议、聚会、活动 |
| 媒体 | `brain/media/` | 书籍、节目、电影、播客 |
| 想法 | `brain/ideas/` | 商业想法、概念、随机思考 |
| 组织 | `brain/orgs/` | 公司、社区、团体 |

## 实体链接

使用维基链接（wikilink）格式来引用实体：
- `[[people/raven-duran]]` — 链接到一个人物；
- `[[events/geeksonabeach-2026]]` — 链接到一个活动；
- `[[orgs/symph]]` — 链接到一个组织。

这样可以明确表示实体之间的关系，并便于搜索。

## 示例工作流程

**用户说：** “嘿，我刚遇到一个叫Raven Duran的人。他自称是一名‘Agentic coder’，我们在GeeksOnABeach PH会议上见过他。”
**助手操作：**
1. 使用`qmd search "Raven Duran"` — 没有找到匹配结果；
2. 阅读`skills/brain/templates/person.md`模板；
3. 使用模板创建`brain/people/raven-duran.md`文件；
4. （可选）创建`brain/events/geeksonabeach-ph-2026.md`文件并添加链接。

**用户说：** “Raven Duran现在还是26岁。”
**助手操作：**
1. 使用`qmd search "Raven Duran"` — 找到`brain/people/raven-duran.md`文件；
2. 在文件头信息中更新年龄字段为26岁；
3. 添加备注：`- **2026-02-21**: 确认他现在26岁；
4. 更新`last_updated`字段。

## 附件

“Brain”条目可以包含附件（如照片、PDF文件、视频、音频文件等）。

### 🚨 强制要求：保存所有媒体文件

**当用户发送与“Brain”条目相关的任何媒体文件（照片、音频、视频、PDF）时：**
1. **必须将原始文件保存到`attachments/`文件夹中**；
2. **之后再分析/转录文件内容到数据库中**；
3. **切勿仅因为处理了文件内容就忽略保存原始文件**。

**“保存”意味着文件实际存在于`attachments/`文件夹中，而不仅仅是内容被转录了。**

```bash
# REQUIRED: Copy the file
cp /path/to/inbound/media.jpg brain/places/entry/attachments/descriptive-name.jpg
```

如果你转录了内容但未保存原始文件，那么你的操作是错误的。请返回并保存原始文件。

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

`attachments/index.md`文件用于索引所有附件，便于按描述内容进行搜索。

### 添加附件

当用户提供关于某个实体的媒体文件时（例如：“这是Mamou Prime餐厅的菜单”）：
1. **找到相关条目** — 使用`qmd search "Mamou Prime"`；
2. （如果文件是纯文本格式）将其转换为文件夹结构；
3. 将媒体文件保存到`attachments/`文件夹中，并为文件添加描述性名称；
4. 更新`attachments/index.md`文件，其中包含文件描述。

### ⚠️ 必须同时保存原始文件

**必须同时完成以下两步：**
1. **分析/转录文件内容** — 将处理后的文本添加到数据库中；
2. **保存原始文件** — 将原始文件保存在`attachments/`文件夹中。

这些文件可以被搜索和进一步处理。原始文件应被妥善保存。

**除非用户明确要求“清理”、“删除”文件，否则切勿删除附件。**

**示例：** 用户发送菜单照片：
- ✅ 将菜单内容转录为Markdown格式的表格并保存到数据库中；
- ✅ 将原始照片保存为`attachments/menu-1.jpg`、`menu-2.jpg`；
- ✅ 更新`attachments/index.md`文件。

**错误做法：** 仅转录内容而未保存原始文件。

### 附件命名规则

附件文件名应具有描述性，以便索引系统能够正确识别文件内容：
- `menu-1.jpg`、`menu-2.jpg`
- `business-card.jpg`
- `product-demo.mp4`
- `meeting-transcript.md`
- `voice-memo-2026-02-21.mp3`

### 示例：添加菜单照片

**用户发送：** 两张菜单照片，并附上说明：“这是Mamou Prime餐厅的菜单。”

**助手操作：**
1. 找到`brain/places/mamou-prime-sm-podium.md`条目；
2. （如有需要）将文件转换为文件夹结构；
3. 将菜单内容转录为Markdown表格并保存到数据库中；
4. 在数据库中更新菜单信息；
5. 将原始照片保存为`attachments/menu-1.jpg`、`menu-2.jpg`；
6. 更新`attachments/index.md`文件：
   ```markdown
   # Attachments

   | File | Description | Added |
   |------|-------------|-------|
   | menu-1.jpg | Menu page 1 (transcribed to profile) | 2026-02-21 |
   | menu-2.jpg | Menu page 2 (transcribed to profile) | 2026-02-21 |
   ```
7. 告知用户：“菜单内容已转录并保存为`menu-1.jpg`和`menu-2.jpg`。”