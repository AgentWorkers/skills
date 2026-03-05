---
name: anytype
description: 您可以通过 `anytype-cli` 及其 HTTP API 与 Anytype 进行交互。该工具可用于读取、创建、更新或搜索 Anytype 空间中的对象/页面；管理这些空间；或自动化 Anytype 的工作流程。文档涵盖了首次设置（创建账户、启动服务、加入空间、获取 API 密钥）以及后续的 API 使用方法。
---
# Anytype 技能

二进制文件路径：`/root/.local/bin/anytype`（版本 0.1.9，已安装）
API 基址：`http://127.0.0.1:31012`
认证方式：`Authorization: Bearer <ANYTYPE_API_KEY>`（API 密钥存储在 `.env` 文件中，键名为 `ANYTYPE_API_KEY`）
API 文档：https://developers.anytype.io

## 先检查状态

```bash
anytype auth status     # is an account set up?
anytype space list      # is the service running + spaces joined?
```

如果上述步骤中的任何一项失败，请按照下面的 **设置** 指南进行操作；否则可以直接跳到 **API 使用** 部分。

## 设置（只需执行一次）

```bash
# 1. Create a dedicated bot account (generates a key, NOT mnemonic-based)
anytype auth create tippy-bot

# 2. Install and start as a user service
anytype service install
anytype service start

# 3. Have Tadas send an invite link from Anytype desktop, then join
anytype space join <invite-link>

# 4. Create an API key
anytype auth apikey create tippy

# 5. Store the key
echo "ANYTYPE_API_KEY=<key>" >> /root/.openclaw/workspace/.env
```

如果尚未获得空间邀请链接，请向 Tadas 请求。

## API 使用

首先加载 `.env` 文件：
```python
import json, os, urllib.request
env = dict(l.strip().split('=',1) for l in open('/root/.openclaw/workspace/.env') if '=' in l and not l.startswith('#'))
API_KEY = env.get('ANYTYPE_API_KEY', '')
BASE = 'http://127.0.0.1:31012'
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
```

有关所有 API 端点和请求格式的详细信息，请参阅 `references/api.md`。

### 常见操作模式

**列出空间中的内容：**
```
GET /v1/spaces
```

**全局搜索对象：**
```
POST /v1/search
{"query": "meeting notes", "limit": 10}
```

**列出空间中的对象：**
```
GET /v1/spaces/{space_id}/objects?limit=50
```

**创建对象：**
```
POST /v1/spaces/{space_id}/objects
{"type_key": "page", "name": "My Page", "body": "Markdown content here"}
```

**更新对象（修改对象体或属性）：**
```
PATCH /v1/spaces/{space_id}/objects/{object_id}
{"markdown": "Updated content"}
```
⚠️ 创建对象时使用 `body`，更新对象时使用 `markdown` — 两种方式用于表示相同的内容，但字段名称不同，容易混淆。
⚠️ **重要提示：** 使用 `PATCH` 方法无法更新对象的内容。即使发送了 `body` 或 `markdown` 数据，系统也会返回 200 状态码表示请求成功，但实际上对象内容并不会被更新。只有元数据字段（如 `name`）才会通过 `PATCH` 方法更新。
**唯一可靠的更新对象内容的方法是：先删除对象，然后重新创建它。**
```python
# Step 1: delete old object
requests.delete(f"{BASE}/v1/spaces/{space_id}/objects/{old_id}", headers=headers)

# Step 2: create new object with full updated content
resp = requests.post(f"{BASE}/v1/spaces/{space_id}/objects",
    json={"name": name, "type_key": "ot-note", "body": new_content},
    headers=headers)
new_id = resp.json()["object"]["id"]
```
这意味着在重新创建对象后，需要更新所有引用该对象 ID 的地方。

可以使用 `scripts/anytype_api.py` 作为现成的辅助工具来发起 API 请求。

## 关键限制（通过测试得出）

- `links` 属性是只读的，由桌面编辑器自动填充；尝试通过 API 设置该属性会返回 400 错误。
- 在创建集合时不能设置 `icon` 属性，否则会返回 500 错误。请先创建集合后再设置图标。
- 创建对象时使用 `body`，更新对象时使用 `markdown`。
- `PATCH` 方法无法更新对象内容：`body` 或 `markdown` 字段会被忽略，系统会返回 200 状态码但内容不变。要更新内容，请先删除对象，然后使用新内容重新创建它，并记录新的对象 ID。
- `related_pages` 是一个自定义属性（键：`related_pages`，格式：`objects`），用于在 API 中链接对象。

---

## 对象类型偏好设置

**所有内容的默认类型为 `page`。** 仅当内容属于非正式的临时记录且不需要链接到知识图谱时，才使用 `note` 类型。

所有有实际意义的内容（如会议记录、研究资料、中心页面、产品文档等）应设置为 `type_key: "page"`。

---

## 知识图谱原则（务必遵守）

Anytype 是一个 **链接型知识库**，而不是简单的文件存储系统。每次创建或更新内容时，都要思考：*这些内容如何与已有的内容关联？*

### 1. 链接所有内容
- 在 markdown 正文中使用 `[[页面名称]]` 格式的链接来引用相关对象。
- 创建新页面时，先搜索相关的现有页面并添加链接。
- 更新现有页面时，添加对新创建的相关页面的链接。

### 2. 将集合作为内容容器使用
- 对于任何主题集群，应创建一个 **集合**（`type_key: collection`），而不是简单的页面集合。
- 集合是 Anytype 的原生容器类型，可以在侧边栏中显示，并支持多种视图（网格、列表、看板）和查询功能。
- 使用 **Lists API** 将子对象添加到集合中。
- 在集合内还需要创建一个 **中心页面**，作为内容的概述（包含描述和链接）。
- 例如：
  - `Merkys — Healthcare Chatbot` → `bafyreicm3a7xj6zhq2l3ouuo74klcxixnvilo3xif24yoijb4wghjpepm4`
  - `Mercoder.ai` → `bafyreigvkwfrtbmrkureuoxfj4ewjrccvpla7dndd7d3ygsyjxuqzorgja`
  - `Vibe Coding Metrics` → `bafyreicejuvonwzo5sgjieana65l4pjbsrhlij5fpbjdrbjc5kdogwwalu`

**创建并填充集合：**
```python
# 1. Create (no icon on create — causes 500)
col = api('POST', f'/v1/spaces/{SPACE}/objects', {'type_key': 'collection', 'name': 'My Cluster'})
col_id = col['object']['id']

# 2. Add objects
api('POST', f'/v1/spaces/{SPACE}/lists/{col_id}/objects', {'objects': [id1, id2, id3]})
```

**侧边栏说明：** 侧边栏的固定显示功能需要手动操作，无法通过 API 实现。请让用户通过 Anytype 桌面应用来固定首页和集合的显示位置。

### 3. 双向链接机制
- Anytype 会自动显示反向链接，但你需要自己在正文中添加正向链接。
- 创建内容后，需要更新中心页面以包含对新对象的链接。

### 4. 创建页面前的注意事项

```
1. Search: POST /v1/spaces/{space_id}/search {"query": "<topic>", "limit": 10}
2. Check if a page already exists — update it rather than duplicate
3. Identify the parent hub page(s) this belongs to
4. Create the page with inline links to related pages in the body
5. Patch the hub page(s) to add a link to the new page
```

### 5. 中心页面模板

创建中心页面时，请使用以下结构：

```markdown
## Overview
<2-3 sentence summary>

## Pages
- [Child Page Name](anytype://object/<id>) — one-line description
- [Another Page](anytype://object/<id>) — one-line description

## Key Facts
- Fact 1
- Fact 2
```

### 6. 内置对象链接（Anytype 图谱功能）

Anytype 提供了两种链接机制，请同时使用这两种方式：

#### A. 系统提供的 `links` 属性（通过 API 只能读取）
当你使用 `@mention` 或 `[[]]` 语法在富文本编辑器中编写内容时，Anytype 桌面应用会自动填充 `links` 属性。**直接通过 API 设置该属性会返回 400 错误**，因为这是系统保留的属性。

#### B. 可自定义的 `related_pages` 属性（可以通过 API 设置）✅
在 Anytype 中定义了一个名为 `related_pages` 的属性（键：`related_pages`），它会在每个对象的侧边栏中显示，并用于表示对象之间的关系。**创建或更新对象时必须设置此属性。**

```json
// On create:
POST /v1/spaces/{space_id}/objects
{
  "type_key": "page",
  "name": "My Page",
  "body": "...",
  "properties": [
    {"key": "related_pages", "objects": ["<hub_id>", "<sibling_id>"]}
  ]
}

// On update:
PATCH /v1/spaces/{space_id}/objects/{object_id}
{
  "markdown": "...",
  "properties": [
    {"key": "related_pages", "objects": ["<hub_id>", "<sibling_id>"]}
  ]
}
```

**规则：** 中心页面必须将其所有子对象以及首页的 `related_pages` 属性设置为相应的值。子页面的 `related_pages` 属性也应指向其中心页面及所有直接相关的页面。这样可以在 Anytype 的图谱视图中看到这些链接关系。

### 7. 内联链接的语法

**使用 `anytype://` 格式的链接**，**不要使用 `object.any.coop` 格式的链接**。
在正文中使用的 `object.any.coop` 链接会被视为纯文本，无法在 Anytype 应用中点击。只有以下格式的链接才能作为可点击的内部链接显示：

```markdown
[Link Text](anytype://object?objectId=<object_id>&spaceId=<space_id>)
```

示例：
```markdown
[Vibe Coding Metrics — Hub](anytype://object?objectId=bafyreigkp2yirhk7epzialjvevnoh6l3wcsr2ifr4zl6umunzhhgspxetq&spaceId=bafyreial7tzkey5sntoizw7scv2lrywqdicd7m6ru2k6wae7w3z6igm5ke.1f4pitw5ca9gc)
```

**辅助函数：**
```python
def anytype_link(name, obj_id, space_id):
    return f"[→ Open: {name}](anytype://object?objectId={obj_id}&spaceId={space_id})"
```

**⚠️ **不要在 markdown 标题中添加链接（例如 `## [名称](anytype://...)`）** — Anytype 会删除链接内容，仅显示纯文本。链接只能在正文中作为内联文本使用，不能作为标题的一部分。**

**正确的链接格式：**
```markdown
## Speaker Name
[→ Open: Speaker Name](anytype://object?objectId=<id>&spaceId=<space_id>)

One-line summary here.

---
```

**仅在与外部用户共享内容时（例如在 Anytype 应用之外）使用 `object.any.coop` 格式的链接。**

### 9. 标签的使用

每个页面都必须通过 `tag` 属性设置标签（键：`tag`，格式：`multi_select`）。标签可用于在 Anytype 用户界面中进行搜索过滤和跨集合分组。

**标签 ID：** `bafyreicsoqz7qja7uqrpfvtub4c4gg7djsv24ojc42em6j3a2ctaeiy7r4`

**重要提示：** 使用标签时必须使用预定义的标签 ID，不能使用自由文本。可以使用下面的 ID，或者通过 Tags API 创建新的标签。

**创建新标签：**
```
POST /v1/spaces/{space_id}/properties/{TAG_PROP_ID}/tags
{"name": "my-tag", "color": "blue"}
→ returns tag.id — use that ID in multi_select
```

**为对象设置标签：**
```json
PATCH /v1/spaces/{space_id}/objects/{object_id}
{
  "properties": [
    {"key": "tag", "multi_select": ["<tag_id_1>", "<tag_id_2>"]}
  ]
}
```

**已定义的标签及其 ID：**

| 标签 | ID | 用途 |
|-----|----|---------|
| `merkys` | `bafyreiatxjki2c6zy6pyxf6e3xkfnjheqvfmajhqmtpyssiw6wvz3z4x3e` | Merkys 聊天机器人相关页面 |
| `mercoder` | `bafyreibmnkru5tu4ltfo6xwu5ijmzgt54dy5dsbekz7l7ppxqjrntgceam` | Mercoder.ai 相关页面 |
| `vibe-coding` | `bafyreib5fo4pfeq5s46akb6wqk4jufu3j63cp5ay5wrxn2hda2bbtdo3ou` | Vibe 编码指标相关页面 |
| `paceflow` | `bafyreicnhcmlzav2olnejjpgi6mznthckbheypbwddxtrrsekddmqojica` | Paceflow 产品相关页面 |
| `call-notes` | `bafyreicuka2zitbrqbae6khc7sse2mnwlcx3a3i2gig2jqvffknjyzt3fe` | 会议/通话记录相关页面 |
| `research` | `bafyreihhtobisskd2ctgs7r74k5gfa6tzejxdtf5qkbyvac6okdgj43uv4y` | 研究文档相关页面 |
| `product` | `bafyreib27tsqjemixmc76yam7ui66x4dsp2vncwbqd7ci7c7mwkqp7gvba` | 产品策略/路线图相关页面 |
| `hub` | `bafyreic2y3u3iai4z36wrnebj4pejstdkov7p3oj6dokho5xhmaog27jzi` | 中心页面/索引页面 |
| `healthcare` | `bafyreid3nw4casmj4obscsk53jwowbs7x2yjgsm6l4guivrr4nmts5r42i` | 医疗保健领域相关页面 |
| `devops` | `bafyreieqpordkymw7jo5lp3habdyqomytp7bvtpxvwt4m32zby3kcbs3au` | DevOps/基础设施相关页面 |
| `security` | `bafyreieazhkkfmtojxin6d35fh5kgfdkqb6t25d77p2i6dkixsj5ppaqii` | 安全相关页面 |
| `ai` | `bafyreieazhkkfmtojxin6d35fh5kgfdkqb6t25d77p2i6dkixsj5ppaqii` | 人工智能相关页面 |

**标签使用规则：**
- 必须为所有页面添加项目标签（`merkys`、`mercoder`、`vibe-coding`、`paceflow`）。
- 必须为所有内容类型添加相应的标签（`call-notes`、`research`、`product`、`hub`）。
- 根据内容相关性添加相应的领域标签（`healthcare`、`devops`、`security`、`ai`）。
- 中心页面必须添加 `hub` 标签。

### 10. 创建后的检查清单
执行任何写入操作后，请检查以下内容：
- [ ] 该主题是否有对应的中心页面？如果没有，请创建一个。
- [ ] 新创建或更新的页面是否已链接到中心页面？
- [ ] 新内容中是否链接了相关的页面？
- [ ] 是否有孤立页面（没有外部链接）需要添加链接？
- [ ] 新页面是否已设置正确的标签（项目标签、内容类型标签、领域标签）？
- [ ] 新页面的 `related_pages` 属性是否已正确设置为中心页面？

---

## 分享链接

**始终使用公开的网页链接格式，** **不要使用 `anytype://` 格式的链接。**

```
https://object.any.coop/{object_id}?spaceId={space_id}&inviteId={invite_id}#{hash}
```

`inviteId` 和 `#hash` 是空间级别的常量（存储在 `ANYtype` 的 `TOOLS.md` 文件中）。
每个对象的 `object_id` 是唯一的。

示例：
```
https://object.any.coop/bafyreigcwv5psopd27jcek5ba7if2lamskahwp7aylzsbw2aunibfr7kei?spaceId=bafyreial7tzkey5sntoizw7scv2lrywqdicd7m6ru2k6wae7w3z6igm5ke.1f4pitw5ca9gc&inviteId=bafybeifel75s42deh74lbjx3socdyung4ojspjgbr64jxrduf3dghlx35i#CvFB12csDDVDpYxi5J1FewXmdsLmifnLx4p3fBCRG6Jt
```