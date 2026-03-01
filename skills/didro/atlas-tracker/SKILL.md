---
name: atlas-tracker
description: 通过MCP工具与Atlas Tracker（RedForester）的思维导图进行交互。这些工具可用于读取、创建或更新Atlas Tracker中的节点和分支，包括导航思维导图结构、创建解决方案树、更新节点属性以及管理类型化的节点。需要使用`at_read_branch`、`at_create_branch`、`at_update_branch`、`at_get_node_types`和`at_readattachments`工具（这些工具由Atlas Tracker的OpenClaw插件提供）。
---
# Atlas Tracker 技能

Atlas Tracker（app.redforester.com）是一个基于图形的知识管理系统，结合了思维导图、看板（Kanban）和结构化属性的功能。本技能涵盖了如何通过 OpenClaw 的 AT 插件工具来使用该系统。

## 设置

使用此技能需要安装并运行两个组件：

### 1. AT MCP 服务器

一个本地 Node.js 服务器，用于代理对 Atlas Tracker REST API 的请求。

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

服务器默认监听 `http://localhost:3222` 端口。

所需的环境变量（在服务文件或 `.env` 文件中设置）：
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

OpenClaw 会自动重新加载插件。验证结果：
```bash
openclaw status
```
您应该能看到 `at_read_branch`、`at_create_branch`、`at_update_branch`、`at_get_node_types`、`at_readattachments` 等工具被列为可用选项。

---

## 核心概念

- **Map**（地图）——一个思维导图，通过 `mapId`（完整的 UUID）进行标识。
- **Node**（节点）——地图中的单个项目；包含 `id`、`title`（HTML 格式）、可选的 `typeId`、`typeProperties` 和 `children` 数组。
- **Branch**（分支）——一个节点及其所有后代节点的集合。
- **Node 类型**——定义可用属性的规范（例如：enum、text、htmltext、file、user、date 等）。
- **标题格式**——必须为 HTML 格式：`<p>我的标题</p>`，不能使用纯文本。

## 工具 URL

所有工具都接受一个 `nodeUrl` 参数：
```
https://app.redforester.com/mindmap?mapid=<UUID>&nodeid=<UUID>
```
`mapid` 和 `nodeId` 必须是 **完整的 UUID**（例如：`3d7340e8-c763-4c9e-b049-4e900b7cf565`），不能使用部分 UUID。

## 工作流程

### 阅读分支内容
在修改之前，请务必先读取分支内容——切勿假设结构已经已知：
```
at_read_branch(nodeUrl) → returns node tree with children, types, properties
```

### 查找正确的节点
如果您不知道节点的 `nodeId`，可以通过 AT REST API 进行搜索：
```bash
POST /api/search  body: {"query": "...", "map_ids": ["<mapId>"]}
# Returns hits[].id — then at_read_branch each candidate to verify title
```

### 创建分支
```
at_create_branch(parentNodeUrl, data)
```
即使对于叶子节点，`data` 对象中也必须包含 `children: []` 字段。

### 更新分支内容
```
at_update_branch(nodeUrl, delete[], update[], create[])
```
- 创建节点的请求格式：`{parentNodeId, data: {title, typeId?, typeProperties?, children: []}`
- 更新节点的请求格式：`{id, title?, typeProperties?, customProperties?}`
- 三个字段都是必填的（未使用的字段可以传递 `[]`）。

## 节点类型

每次使用 Atlas Tracker 时，都需要调用 `at_get_node_types(nodeUrl)` 来获取节点类型——不同地图的节点类型可能有所不同。
常见的节点类型包括：Идея（想法）、Задача（任务）、Заметка（备注）、Категория（类别）、Проект（项目）、Этап（阶段）、Заявка（申请）、Лид（负责人）。

对于具有类型信息的节点，`typeProperties` 的键必须与 `at_get_node_types` 返回的属性名称完全匹配。

## 重要规则

1. **仅使用完整的 UUID**——使用部分 UUID（例如 `b319f356`）会导致 404 错误。
2. **`children: []` 是必填项**——省略该字段会导致创建节点时出现验证错误。
3. **标题必须使用 HTML 格式**：使用 `<p>...</p>` 来显示文本；列表项使用 `<ul><li>...</li></ul>`。
4. **先读取再写入**——在修改任何节点之前，务必先使用 `at_read_branch` 获取当前状态和节点 ID。
5. **403 错误表示权限被拒绝**——您只能修改属于自己的节点；读取权限可能更宽松。
6. **大型地图加载速度较慢**——避免对大型地图进行全子树读取；建议使用搜索和针对性读取。

## 常用操作模式

### 为现有节点添加子节点
1. 使用 `at_read_branch` 获取父节点的 `nodeId` 并确认其存在。
2. 使用 `at_update_branch` 并传入：`{parentNodeId: "<id>", data: {..., children: []}`。

### 批量创建节点树
使用 `at_create_branch` 并传入嵌套的 `children` 数组，一次性创建完整的节点树。

### 更新节点内容
1. 使用 `at_read_branch` 获取当前节点的 ID 和属性。
2. 使用 `at_update_branch` 并传入：`{id, typeProperties: {key: "<html_value>"}`。

## 参考文件

- **[api-patterns.md](references/api-patterns.md)** — REST API 的搜索、认证和节点获取模式（在需要搜索节点或直接调用 AT API 时阅读）。
- **[node-types-guide.md](references/node-types-guide.md)** — 属性类型参考（htmltext、enum、file、user、date 等）以及如何设置这些属性（在创建/更新节点时阅读）。