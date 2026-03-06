---
name: anytype
description: 您可以通过 `anytype-cli` 及其 HTTP API 与 Anytype 进行交互。该工具可用于读取、创建、更新或搜索 Anytype 空间中的对象/页面；管理这些空间；或自动化 Anytype 的工作流程。文档涵盖了初次使用时的设置步骤（创建账户、启动服务、加入空间、获取 API 密钥），以及后续的 API 使用方法。
metadata:
  openclaw:
    requires:
      env:
        - ANYTYPE_API_KEY
    primaryEnv: ANYTYPE_API_KEY
---
# Anytype 技能

**二进制版本：** `anytype`（通过 https://github.com/anyproto/anytype-cli 安装）  
**API 基础地址：** `http://127.0.0.1:31012`  
**认证方式：** `Authorization: Bearer <ANYTYPE_API_KEY>`（密钥存储在 `.env` 文件中，名为 `ANYTYPE_API_KEY`）  
**API 文档：** https://developers.anytype.io  

> **实例配置：** 空间 ID、标签 ID、集合 ID 和共享链接的信息请参阅 `SETUP.md`（位于同一目录下）。请结合此文件一起阅读。  

## 先检查状态  

```bash
anytype auth status     # is an account set up?
anytype space list      # is the service running + spaces joined?
```  

如果上述步骤中有任何一步失败，请按照下面的 **设置指南** 进行操作；否则可以直接跳到 **API 使用** 部分。  

## 设置（仅一次性操作）  

```bash
# 1. Create a dedicated bot account (generates a key, NOT mnemonic-based)
anytype auth create my-bot

# 2. Install and start as a user service
anytype service install
anytype service start

# 3. Have the space owner send an invite link from Anytype desktop, then join
anytype space join <invite-link>

# 4. Create an API key
anytype auth apikey create my-key

# 5. Store the key
echo "ANYTYPE_API_KEY=<key>" >> ~/.openclaw/workspace/.env
```  

## API 使用  

加载 API 密钥（仅从环境变量或 `.env` 文件中读取 `ANYTYPE_API_KEY`）：  
```python
import os, requests

def load_api_key():
    if "ANYTYPE_API_KEY" in os.environ:
        return os.environ["ANYTYPE_API_KEY"]
    env_path = os.path.expanduser("~/.openclaw/workspace/.env")
    if os.path.exists(env_path):
        for line in open(env_path):
            if line.strip().startswith("ANYTYPE_API_KEY="):
                return line.strip().split("=", 1)[1]
    return ""

API_KEY = load_api_key()
BASE = 'http://127.0.0.1:31012'
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
```  

有关所有 API 端点和请求格式的详细信息，请参阅 `references/api.md`。  

### 常用操作模式  

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

**更新对象（修改对象内容/属性）：**  
```
PATCH /v1/spaces/{space_id}/objects/{object_id}
{"markdown": "Updated content"}
```  

⚠️ **创建对象时使用 `body`，更新对象时使用 `markdown` — 两种方式使用不同的字段名，容易混淆。**  
⚠️ **重要提示：** `PATCH` 操作不会更新对象的内容字段。即使发送了 `body` 或 `markdown` 数据，系统也会返回 200 状态码（表示操作成功），但实际上对象内容并不会被更新。只有元数据字段（如 `name`）才会被更新。  
**唯一可靠的更新对象内容的方法是：先删除对象，再重新创建。**  
⚠️ **此操作具有破坏性。** 在删除对象之前，请务必保存其原始内容：  
```python
# Step 0: fetch and save existing content before deleting
old = requests.get(f"{BASE}/v1/spaces/{space_id}/objects/{old_id}", headers=headers).json()
old_content = old.get("object", {}).get("snippet", "")  # keep a local copy

# Step 1: delete old object (irreversible via API — confirm before running)
requests.delete(f"{BASE}/v1/spaces/{space_id}/objects/{old_id}", headers=headers)

# Step 2: create new object with full updated content
resp = requests.post(f"{BASE}/v1/spaces/{space_id}/objects",
    json={"name": name, "type_key": "page", "body": new_content},
    headers=headers)
new_id = resp.json()["object"]["id"]
```  

更新对象后，需要更新所有引用该对象的链接（例如 `related_pages`）。被删除的对象可以通过桌面应用程序中的 Anytype 工具进行恢复。  

可以使用 `scripts/anytype_api.py` 作为辅助工具来发起 API 请求。  

## 关键限制（根据测试结果得出）  

- **`links` 属性是只读的** — 由桌面应用程序系统管理，用户无法直接设置；尝试设置该属性会导致 400 错误。  
- **创建集合时不能设置 `icon` 属性** — 会导致 500 错误；建议先创建集合，之后再添加图标。  
- **创建对象时使用 `body`，更新对象时使用 `markdown`。**  
- **`PATCH` 操作无法更新对象内容** — `body` 或 `markdown` 字段会被忽略；系统会返回 200 状态码，但内容不会被更新。要更新内容，请先删除对象再重新创建。  
- **`related_pages` 是一个自定义属性**（键：`related_pages`，格式：`objects`）——可以通过 API 设置对象之间的链接关系；如果该属性不存在，需要先在空间中创建相应的对象。  

---

## 对象类型偏好设置  

**所有内容的默认类型为 `page`。** 但 **笔记（note 类型）** 是例外——仅用于非正式或临时性的内容，不需要将其链接到知识图谱中。**  
所有具有实际意义的内容（如会议记录、研究资料、中心页面、产品文档等）应设置为 `type_key: "page"`。  

---

## 知识图谱使用原则（务必遵守）  

Anytype 是一个 **链接型知识库**，而非简单的文件存储系统。每次创建或更新内容时，都需要思考：**“这些内容如何与现有内容关联？”**  

### 1. 将所有内容链接起来**  
- 在 markdown 正文中使用 `[[Page Name]]` 格式创建内联链接，以引用相关对象。  
- 创建新页面时，先搜索相关的现有页面并添加链接。  
- 更新现有页面时，添加对新创建的相关页面的链接。  

### 2. 将集合作为内容组织单元  
- 对于任何主题相关的内容，应创建一个 **集合**（`type_key: collection`），而不是简单的页面集合。  
- 集合是 Anytype 的原生数据结构，支持多种展示方式（网格、列表、看板），并且可以对其进行查询。  
- 使用 **Lists API** 向集合中添加子对象。  
- 在集合内创建一个 **中心页面**，作为内容的概览（包含描述和链接）。  

**创建并填充集合：**  
```python
# 1. Create (no icon on create — causes 500)
col = api('POST', f'/v1/spaces/{SPACE}/objects', {'type_key': 'collection', 'name': 'My Cluster'})
col_id = col['object']['id']

# 2. Add objects
api('POST', f'/v1/spaces/{SPACE}/lists/{col_id}/objects', {'objects': [id1, id2, id3]})
```  

**注意：** 在桌面应用程序中，集合的固定显示位置需要手动设置，无法通过 API 完成。  

### 3. 实现双向链接**  
- Anytype 会自动显示反向链接，但用户需要手动在正文中添加正向链接。  
- 创建内容后，务必更新中心页面以包含对新对象的链接。  

### 4. 创建页面前的准备工作  

```
1. Search: POST /v1/spaces/{space_id}/search {"query": "<topic>", "limit": 10}
2. Check if a page already exists — update it rather than duplicate
3. Identify the parent hub page(s) this belongs to
4. Create the page with inline links to related pages in the body
5. Update the hub page(s) to add a link to the new page
```  

### 5. 中心页面模板**  
创建中心页面时，请使用以下结构：  
```markdown
## Overview
<2-3 sentence summary>

## Pages
- [Child Page Name](anytype://object?objectId=<id>&spaceId=<space_id>) — one-line description
- [Another Page](anytype://object?objectId=<id>&spaceId=<space_id>) — one-line description

## Key Facts
- Fact 1
- Fact 2
```  

### 6. 自定义对象链接（Anytype 的图谱功能）  
Anytype 支持两种链接方式：  

#### A. 系统提供的 `links` 属性（通过 API 无法直接设置）  
当在富文本编辑器中使用 `@mention` 或 `[]` 语法时，Anytype 会自动填充 `links` 属性。尝试直接通过 API 设置该属性会导致 400 错误。  

#### B. 可自定义的 `related_pages` 属性（可通过 API 设置）  
在空间中创建一个名为 `related_pages` 的属性（键：`related_pages`），该属性会显示在每个对象的侧边栏中，用于展示对象之间的关系。  
```json
// On create:
{
  "type_key": "page",
  "name": "My Page",
  "body": "...",
  "properties": [
    {"key": "related_pages", "objects": ["<hub_id>", "<sibling_id>"]}
  ]
}
```  

**规则：**  
- 中心页面的 `related_pages` 应指向其所有子页面；子页面的 `related_pages` 应指向它们的中心页面。这样可以在图谱中看到这些链接关系。  

### 7. 内联链接的编写规则  
- 在应用内部使用 `anytype://` 格式的链接；**不要使用 `object.any.coop` 格式的链接**。  
`object.any.coop` 格式的链接在页面文本中会显示为纯文本，无法在 Anytype 应用中点击。  

**提示：** **不要在 markdown 标题中添加链接**——Anytype 会删除链接内容，仅显示纯文本。**  
仅在与外部用户共享内容时使用 `object.any.coop` 格式的链接。  

### 8. 标签的使用**  
使用标签时，需要确保空间中已经存在相应的标签 ID；不能直接输入文本字符串。  

**创建新标签：**  
```
POST /v1/spaces/{space_id}/properties/{tag_property_id}/tags
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

> 有关此实例的标签 ID 和所有定义好的标签信息，请参阅 `SETUP.md`。  

### 9. 创建后的检查流程  
每次进行写入操作后，请检查以下内容：  
- [ ] 该主题是否有对应的中心页面？如果没有，请创建一个。  
- [ ] 新创建/更新的页面是否已链接到中心页面？  
- [ ] 新内容中的相关页面是否已添加链接？  
- [ ] 是否有孤立页面（没有外部链接）需要添加链接？  
- [ ] 新页面是否已设置正确的标签（项目名称 + 内容类型 + 域名）？  
- [ ] 新页面的 `related_pages` 是否已正确指向中心页面？  

---

## 外部共享链接  
**外部共享时，请使用以下格式的链接：**  
```
https://object.any.coop/{object_id}?spaceId={space_id}&inviteId={invite_id}#{hash}
```  

`inviteId` 和 `#hash` 是与空间相关的常量；`object_id` 则因对象而异。  
> 有关此实例的 `spaceId`、`inviteId` 和 `hash` 的详细信息，请参阅 `SETUP.md`。