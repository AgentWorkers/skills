---
name: logseq
description: 提供用于通过 Logseq 的插件 API 与本地 Logseq 实例交互的命令。这些命令可用于创建页面、插入内容块、查询图数据库、管理任务、检索数据，以及自动化 Logseq 中的工作流程。请确保使用的是已启用 API 的本地运行实例；默认端口或路径适用于 [$API accessible skill]。
---

# Logseq插件API

您可以通过JavaScript插件API与本地的Logseq实例进行交互。该插件API支持读取、写入、查询以及自动化处理Logseq图中的工作流程。

## 先决条件

**Logseq必须在本机运行**，并且需要安装一个能够暴露API的插件。常见的实现方式如下：

1. **安装桥接插件**：通过HTTP接口（例如自定义插件或本地端点）暴露`logseq` API。
2. **另一种方式**：使用Node.js和`@logseq/libs`包来编写脚本，以与正在运行的Logseq实例进行交互。

该API主要针对浏览器插件设计，因此从外部脚本访问它需要借助桥接插件或代理服务器。

## 核心API命名空间

Logseq插件API主要分为以下几个命名空间：

### `logseq.App`
- 应用层操作：获取应用信息、用户配置、当前图谱、命令、UI状态、外部链接等。
  - **关键方法**：
    - `getInfo()`：获取应用版本和信息
    - `getUserConfigs()`：获取用户偏好设置（主题、格式、语言等）
    - `getCurrentGraph()`：获取当前图谱的信息（名称、路径、URL）
    - `registerCommand(type, opts, action)`：注册自定义命令
    - `pushState(route, params, query)`：导航到指定路径

### `logseq.Editor`
- 块和页面编辑操作：创建、更新、移动、查询内容等。
  - **关键方法**：
    - `getBlock(uuid)`：根据UUID获取块
    - `getCurrentPage()`：获取当前页面的实体
    - `getCurrentPageBlocksTree()`：获取当前页面上的所有块
    - `getPageBlocksTree(page)`：获取特定页面的所有块
    - `insertBlock(target, content, opts)`：插入新块
    - `updateBlock(uuid, content)`：更新块内容
    - `createPage(pageName, properties, opts)`：创建新页面
    - `deletePage(pageName)`：删除页面
    - `getPageLinkedReferences(page)`：获取页面的引用链接
    - `registerSlashCommand(tag, action)`：添加自定义的斜杠命令

### `logseq.DB`
- 使用Datalog进行数据库查询。
  - **关键方法**：
    - `q(query, ...inputs)`：执行Datalog查询
    - `datascriptQuery(query, ...inputs)`：直接执行Datascript查询

### `logseq.UI`
- UI操作：显示消息、对话框、控制主UI的可见性等。
  - **关键方法**：
    - `showMsg(content, status)`：显示提示通知
    - `queryElementById(id)`：查询DOM元素

### `logseq.Git`
- 对当前图谱进行Git操作。
  - **关键方法**：
    - `execCommand(args)`：执行Git命令

### `logseq.Assets`
- 资产管理相关操作。

## 常见工作流程

### 读取内容
```javascript
// Get current page
const page = await logseq.Editor.getCurrentPage();

// Get all blocks on a page
const blocks = await logseq.Editor.getPageBlocksTree('Daily Notes');

// Get a specific block
const block = await logseq.Editor.getBlock('block-uuid-here');

// Query with Datalog
const results = await logseq.DB.q(`
  [:find (pull ?b [*])
   :where [?b :block/marker "TODO"]]
`);
```

### 写入内容
```javascript
// Create a new page
await logseq.Editor.createPage('Project Notes', {
  tags: 'project',
  status: 'active'
}, { redirect: false });

// Insert a block
const block = await logseq.Editor.insertBlock(
  'target-block-uuid',
  '- New task item',
  { before: false, sibling: true }
);

// Update a block
await logseq.Editor.updateBlock('block-uuid', 'Updated content');

// Batch insert multiple blocks
const blocks = [
  { content: 'First item' },
  { content: 'Second item', children: [
    { content: 'Nested item' }
  ]}
];
await logseq.Editor.insertBatchBlock('parent-uuid', blocks, { sibling: false });
```

### 任务管理
```javascript
// Find all TODO items
const todos = await logseq.DB.q(`
  [:find (pull ?b [*])
   :where
   [?b :block/marker ?marker]
   [(contains? #{"TODO" "DOING"} ?marker)]]
`);

// Mark task as DONE
await logseq.Editor.updateBlock('task-uuid', 'DONE Task content');

// Get tasks on current page
const page = await logseq.Editor.getCurrentPage();
const blocks = await logseq.Editor.getPageBlocksTree(page.name);
const tasks = blocks.filter(b => b.marker === 'TODO' || b.marker === 'DOING');
```

### 导航和UI
```javascript
// Navigate to a page
logseq.App.pushState('page', { name: 'Project Notes' });

// Show notification
logseq.UI.showMsg('✅ Task completed!', 'success');

// Get app config
const configs = await logseq.App.getUserConfigs();
console.log('Theme:', configs.preferredThemeMode);
console.log('Format:', configs.preferredFormat);
```

## 实现方式

由于Logseq的插件API是基于浏览器的，您有以下几种实现选择：

### 选项1：桥接插件
- 创建一个简单的Logseq插件，通过HTTP接口暴露API调用：
```javascript
// In Logseq plugin (index.js)
logseq.ready(() => {
  // Expose API endpoints
  logseq.provideModel({
    async handleAPICall({ method, args }) {
      return await logseq.Editor[method](...args);
    }
  });
});

// Then call from external script via HTTP POST
```

### 选项2：使用`@logseq/libs`的Node.js脚本
- 对于自动化脚本，可以使用`@logseq/libs`包：
```bash
npm install @logseq/libs
```

**注意**：这需要一个正在运行的Logseq实例以及正确的连接配置。

### 选项3：直接开发插件
- 可以参考以下链接开发完整的Logseq插件：
https://github.com/logseq/logseq-plugin-samples

## API参考

完整的API文档请参阅：
- **API文档**：https://logseq.github.io/plugins/
- **插件示例**：https://github.com/logseq/logseq-plugin-samples
- **类型定义**：`references/api-types.md`（来自`@logseq/libs`）

## 关键数据结构

### BlockEntity
```typescript
{
  id: number,           // Entity ID
  uuid: string,         // Block UUID
  content: string,      // Block content
  format: 'markdown' | 'org',
  page: { id: number }, // Parent page
  parent: { id: number }, // Parent block
  left: { id: number }, // Previous sibling
  properties: {},       // Block properties
  marker?: string,      // TODO/DOING/DONE
  children?: []         // Child blocks
}
```

### PageEntity
```typescript
{
  id: number,
  uuid: string,
  name: string,              // Page name (lowercase)
  originalName: string,       // Original case
  'journal?': boolean,
  properties: {},
  journalDay?: number,       // YYYYMMDD for journals
}
```

## 提示与最佳实践

1. **始终检查`null`：**如果实体不存在，API方法可能会返回`null`。
2. **优先使用UUID**：块的UUID是稳定的，而实体ID可能会发生变化。
3. **批量操作**：使用`insertBatchBlock`进行多次插入。
4. **高效查询**：Datalog查询功能强大，但在大型图谱上可能会比较慢。
5. **属性访问方式**：使用`block.properties.propertyName`来访问属性。
6. **注意格式**：尊重用户选择的格式（Markdown或Org Mode）。
7. **所有API调用都是异步的**：所有API调用都会返回Promise。

## 常见问题

- **页面名称为小写**：在查询时请使用小写的页面名称。
- **日志页面**：使用`journalDay`格式（YYYYMMDD），而不是日期字符串。
- **块层次结构**：插入块时请注意父节点和子节点的关系。
- **格式差异**：Markdown使用`-`作为项目符号，Org Mode使用`*`。
- **属性语法**：Markdown使用`prop::`，Org Mode使用`:PROPERTIES:`。