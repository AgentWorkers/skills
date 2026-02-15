# SKILL.md – 使用 Martian 库将 Markdown 内容转换为 Notion 格式

本工具使用 Martian 库将 Markdown 内容转换为 Notion 格式的块。

## 使用场景

- 从 Markdown 内容创建 Notion 页面  
- 转换日记条目、笔记或文档  
- 批量导入 Markdown 文件到 Notion  
- 为 Notion 数据库准备格式化内容  

## 安装  

```bash
cd ~/.openclaw/workspace/skills/notion-md-converter
npm install
```  

设置环境变量：  
```bash
export NOTION_TOKEN="ntn_your_token_here"
```  

## 使用方法  

### 方法 1：直接使用库  

```javascript
const { convertMarkdownToBlocks, createNotionPageFromMarkdown } = require('./skills/notion-md-converter/src/converter');

// Convert markdown to blocks
const { success, blocks, error, warning } = convertMarkdownToBlocks(`
## Today's Progress

Completed tasks:
- [x] Research complete
- [x] Design approved
- [ ] Implementation pending

> [!TIP]
> Remember to update the task plan!
`);

if (success) {
  // Use blocks with Notion API
  console.log(`Converted to ${blocks.length} blocks`);
}
```  

### 方法 2：直接创建页面  

```javascript
const result = await createNotionPageFromMarkdown({
  parentId: 'your-parent-page-id',
  title: 'Journal Entry - 2026-02-10',
  markdown: content,
  notionToken: process.env.NOTION_TOKEN
});

if (result.success) {
  console.log(`Created page: ${result.url}`);
}
```  

### 方法 3：使用 CLI 工具  

```bash
node tools/md2notion.js \
  --parent-id "abc123" \
  --title "My Page" \
  --file content.md \
  --token "ntn_xxx"
```  

## 支持的 Markdown 格式  

| Markdown 格式 | Notion 对应格式 |  
|------------|-----------------|  
| `# 标题`       | `heading_1`         |  
| `## 标题`       | `heading_2`         |  
| `### 标题`       | `heading_3`         |  
| `**粗体**       | `rich_textANNOTATION`    |  
| `*斜体*`       | `rich_textANNOTATION`    |  
| `` `代码` ``     | `inline_code`       |  
| `- 列表项`      | `bulleted_list_item`     |  
| `1. 编号项`      | `numbered_list_item`     |  
| `- [x] 任务`     | `to_do`          |  
| `- [ ] 任务`     | `to_do`          |  
| ````code```` | `code_block`       |  
| `> 引用`       | `quote`           |  
| `> [!注意]`      | `blue_callout`       |  
| `> [!警告]`      | `yellow_callout`       |  
| `> [!提示]`      | `red_callout`       |  
| `\| 表格`       | `table`           |  

## 错误处理  

本工具能优雅地处理以下常见问题：  
- **无效的 Markdown**：返回替代的纯文本块  
- **内容过长**：自动截断为 100 个块，并发出警告  
- **API 错误**：返回详细的错误信息  
- **缺少标记**：明确提示缺少 NOTION_TOKEN  

## 限制  

- Notion API 限制：每次请求最多只能转换 100 个块  
- 图片链接必须可公开访问  
- 表格的格式化选项有限  
- 超过 2 层的嵌套块会被扁平化  

## 与 Galatea 日记系统的集成  

本工具专为 Galatea 日记系统设计：  
```javascript
// In your Journal cron or automation
const { createNotionPageFromMarkdown } = require('./skills/notion-md-converter/src/converter');

async function createJournalEntry(date, content) {
  return await createNotionPageFromMarkdown({
    parentId: process.env.JOURNAL_DATABASE_ID,
    title: `Journal - ${date}`,
    markdown: content
  });
}
```  

## 测试  

```bash
npm test
```  

## 所需依赖库  

- `@tryfabric/martian`：用于将 Markdown 转换为 Notion 格式的库  
- `@notionhq/client`：官方的 Notion API 客户端  

## 许可证  

MIT