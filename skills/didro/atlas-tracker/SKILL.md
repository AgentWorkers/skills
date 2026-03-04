---
name: atlas-tracker
description: 通过 MCP 工具与 Atlas Tracker（RedForester）的思维导图进行交互。这些工具可用于读取、创建或更新 Atlas Tracker 中的节点和分支，包括导航思维导图结构、创建解决方案树、更新节点属性、管理类型化节点、创建链接节点、将文件上传到节点以及处理节点注释。需要使用以下插件提供的工具：at_read_branch、at_create_branch、at_update_branch、at_get_node_types、at_readattachments、at_create_link_node、at_upload_file、at_get_comments、at_add_comment、at_delete_comment 和 at_update_comment。
---
# Atlas Tracker 技能

Atlas Tracker（app.redforester.com）是一个基于图谱的知识管理系统，它结合了思维导图、看板（Kanban）和结构化属性的功能。本技能涵盖了如何通过 OpenClaw 的 AT 插件来使用该系统。

## 设置

使用该技能需要安装并运行两个组件：

### 1. AT MCP 服务器

一个本地的 Node.js 服务器，用于代理对 Atlas Tracker REST API 的请求。

> AT MCP 服务器由 Atlas Tracker/RedForester 团队维护。
> 如需获取访问权限，请联系 **@gmdidro**（Telegram）或访问 [app.redforester.com](https://app.redforester.com)。

获取服务器文件后：

```bash
cd at-mcp/
yarn install
yarn build

# Run directly
node build/index.js

# Or run as a systemd user service (recommended)
cp at-mcp.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now at-mcp
```

该服务器默认监听 `http://localhost:3222` 端口。

所需的环境变量（在服务文件或 `.env` 中设置）：
```
AT_BASE_URL=https://app.redforester.com/api
AUTH_HEADER=Basic <base64(username:md5(password))>
API_KEY=<your-local-api-key>
PORT=3222
```

### 2. OpenClaw 插件

将插件文件复制到您的 OpenClaw 扩展目录中：

```bash
mkdir -p ~/.openclaw/extensions/atlas-tracker/
cp index.ts ~/.openclaw/extensions/atlas-tracker/
cp openclaw.plugin.json ~/.openclaw/extensions/atlas-tracker/
```

然后在 `openclaw.json` 文件中配置该插件：

```json
{
  "plugins": {
    "atlas-tracker": {
      "serverUrl": "http://localhost:3222",
      "apiKey": "<your-local-api-key>"
    }
  }
}
```

OpenClaw 会自动重新加载插件。验证方法如下：
```bash
openclaw status
```
您应该会看到 `at_read_branch`、`at_create_branch`、`at_update_branch`、`at_get_node_types`、`at_readattachments` 等工具被列为可用工具。

---

## 核心概念

- **Map**（图谱）——由 `mapId`（完整的 UUID）标识
- **Node**（节点）——图谱中的单个条目；包含 `id`、`title`（HTML 格式）、可选的 `typeId`、`typeProperties`、`children[]`
- **Branch**（分支）——一个节点及其所有后代节点
- **Node 类型**——定义可用属性的架构（例如：enum、text、htmltext、file、user、date 等）
- **标题格式**——始终使用 HTML 格式：`<p>我的标题</p>`，不能使用纯文本

## 工具 URL

所有工具都需要一个 `nodeUrl`，格式如下：
```
https://app.redforester.com/mindmap?mapid=<UUID>&nodeid=<UUID>
```
`mapid` 和 `nodeId` 必须是 **完整的 UUID**（例如：`3d7340e8-c763-4c9e-b049-4e900b7cf565`），不能使用部分 UUID。

## 工作流程

### 阅读分支内容
在修改之前务必先阅读内容——切勿假设结构已经正确：
```
at_read_branch(nodeUrl) → returns node tree with children, types, properties
```

### 查找正确的节点
如果您不知道 `nodeId`，可以通过 AT REST API 进行搜索：
```bash
POST /api/search  body: {"query": "...", "map_ids": ["<mapId>"]}
# Returns hits[].id — then at_read_branch each candidate to verify title
```

### 创建分支
```
at_create_branch(parentNodeUrl, data)
```
即使对于叶子节点，`data` 中也必须包含 `children: []`——这是一个必填字段。

### 更新分支内容
```
at_update_branch(nodeUrl, delete[], update[], create[])
```
- 创建节点的格式：`{parentNodeId, data: {title, typeId?, typeProperties?, children: []}`
- 更新节点的格式：`{id, title?, typeProperties?, customProperties?}`
- 三个字段都是必填的（如果不需要某个字段，则传递 `[]`）

## 节点类型

每次使用 Atlas Tracker 时，都需要调用 `at_get_node_types(nodeUrl)`——不同图谱的节点类型可能有所不同。
常见的节点类型包括：Идея（想法）、Задача（任务）、Заметка（备注）、Категория（类别）、Проект（项目）、Этап（阶段）、Заявка（请求）、Лид（负责人）。

对于具有类型的节点，`typeProperties` 的键必须与 `at_get_node_types` 中定义的属性名称完全匹配。

## 重要规则

1. **仅使用完整的 UUID**——使用部分 UUID（例如 `b319f356`）会导致 404 错误
2. **`children: []` 是必填项**——省略该字段会导致创建节点时出现验证错误
3. **标题必须使用 HTML 格式**——使用 `<p>...</p>`；列表项使用 `<ul><li>...</li></ul>` 格式
4. **先读取再写入**——在写入之前务必先使用 `at_read_branch` 获取当前状态和节点 ID
5. **403 错误表示权限被拒绝**——您只能修改属于自己的节点；读取权限可能更广泛
6. **大型图谱加载速度较慢**——避免读取大型图谱的整个子树结构；建议使用搜索和针对性地读取节点内容

## 常见操作模式

### 为现有节点添加子节点
1. 使用 `at_read_branch` 获取父节点的 `nodeId` 并确认其存在
2. 使用 `at_update_branch` 并传入：`{parentNodeId: "<id>", data: {..., children: []}}`

### 批量创建节点树
使用 `at_create_branch` 并传入嵌套的 `children[]`，一次性创建完整的节点树。

### 更新节点内容
1. 使用 `at_read_branch` 获取当前节点的 ID 和属性
2. 使用 `at_update_branch` 并传入：`{id, typeProperties: {key: "<html_value>"}`

### 创建链接节点（快捷方式/引用）
链接节点是对现有节点的引用——它在图谱中显示为对该节点的快捷链接。这有助于在不重复节点的情况下在多个位置显示同一节点。
```
at_create_link_node(nodeUrl, originalNodeId)
```
- `nodeUrl`——链接节点应显示在其中的父节点的 URL
- `originalNodeId`——要引用的现有节点的 UUID

示例：在父节点 `def-456` 下创建一个指向节点 `abc-123` 的链接：
```
at_create_link_node(
  "https://app.redforester.com/mindmap?mapid=<mapId>&nodeid=def-456",
  "abc-123"
)
```

### 向节点上传文件
可以将任何文件（PDF、Excel、Word、图片）附加到 Atlas Tracker 的节点上：
```
at_upload_file(nodeUrl, filePath)
```
- `filePath`——文件的绝对本地路径
- 通过 `PUT /api/files` 进行上传，然后将其作为类型 ID 为 10 的属性附加到节点上
- 该操作会添加到现有文件中，而不会覆盖原有文件

### 处理注释
```
at_get_comments(nodeUrl)           → list all comments (with thread structure)
at_add_comment(nodeUrl, text, replyToCommentId?)  → add comment or reply to thread
at_update_comment(nodeUrl, commentId, text)       → edit comment text
at_delete_comment(nodeUrl, commentId)             → delete comment
```

---

## 参考文件

- **[api-patterns.md](references/api-patterns.md)** — REST API 搜索、认证、节点获取的模式（在需要搜索节点或直接调用 AT API 时阅读）
- **[node-types-guide.md](references/node-types-guide.md)** — 属性类型参考（htmltext、enum、file、user、date 等）以及如何设置这些属性（在创建/更新具有类型的节点时阅读）