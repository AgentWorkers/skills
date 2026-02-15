---
name: notion
version: 0.1.0
description: **与 Notion 工作区集成**  
您可以利用该功能读取页面内容、查询数据库、创建新条目以及管理各类内容。这一集成方案非常适合用于构建知识库、项目跟踪系统、内容日程管理工具、客户关系管理系统（CRM）以及协作式文档系统。它支持与任何您明确共享给该集成服务的 Notion 页面或数据库进行交互。
---

# Notion 集成

将您的 Notion 工作区与 OpenClaw 连接起来，实现无缝的知识管理和项目跟踪。

## 何时使用此功能

当用户需要执行以下操作时，可以使用 Notion：
- **向数据库中添加项目**（待办事项、任务列表等）
- **在数据库中创建新页面** 或将新页面设置为现有页面的子页面
- **查询/搜索** 自己的 Notion 工作区中的信息
- **更新现有页面**（状态、备注、属性等）
- **读取页面内容** 或数据库条目

## 设置

### 1. 创建 Notion 集成
1. 访问 [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. 点击 **新建集成**
3. 为其命名（例如：“OpenClaw”）
4. 选择您的工作区
5. 复制 **内部集成令牌**（以 `secret_` 开头）
6. 将此令牌安全地保存在 OpenClaw 的配置文件或环境变量中：`NOTION_TOKEN=secret_...`

### 2. 通过集成共享页面
**重要提示：** 默认情况下，Notion 集成没有访问权限。您必须明确共享页面：
1. 进入 Notion 中的任意页面或数据库
2. 点击 **共享** → **添加连接**
3. 选择您的 “OpenClaw” 集成
4. 之后，该功能就可以读取/写入该特定页面/数据库了

### 3. 获取数据库/页面 ID

**通过 URL 获取：**
- 数据库：`https://www.notion.so/workspace/XXXXXXXX?v=...` → ID 为 `XXXXXXXX`（32 个字符）
- 页面：`https://www.notion.so/workspace/XXXXXXXX` → ID 为 `XXXXXXXX`

**注意：** 使用 ID 时请删除连字符，仅使用 32 个字符的字符串。

## 核心操作

### 查询数据库

从您共享的任何数据库中检索条目。

```typescript
// Using the Notion skill via exec
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js query-database ${databaseId}`
});

// With filters (example: status = "In Progress")
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js query-database ${databaseId} --filter '{"property":"Status","select":{"equals":"In Progress"}}'`
});
```

**返回值：** 包含数据库中配置的属性的页面数组。

### 添加数据库条目

在数据库中创建新行。

```typescript
// Add entry with multiple properties
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js add-entry ${databaseId} \
    --title "My New Content Idea" \
    --properties '${JSON.stringify({
      "Status": { "select": { "name": "Idea" } },
      "Platform": { "multi_select": [{ "name": "X/Twitter" }] },
      "Tags": { "multi_select": [{ "name": "3D Printing" }, { "name": "AI" }] },
      "Priority": { "select": { "name": "High" } }
    })}'`
});
```

### 获取页面内容

读取任何页面的内容（包括数据库条目）。

```typescript
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js get-page ${pageId}`
});
```

**返回值：** 页面标题、属性以及块内容（文本、标题、列表等）。

### 更新页面

修改现有页面的属性或添加内容。

```typescript
// Update properties
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js update-page ${pageId} \
    --properties '${JSON.stringify({
      "Status": { "select": { "name": "In Progress" } }
    })}'`
});

// Append content blocks
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js append-body ${pageId} \
    --text "Research Notes" --type h2`
});
```

### 在 Notion 中搜索

在整个共享的工作区中查找页面。

```typescript
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js search "content ideas"`
});
```

## 常见用例

### 内容处理流程（内容创建者工作流程）

**数据库结构：**
- 标题（title）
- 状态（可选：想法 → 草稿 → 计划中 → 已发布）
- 平台（多选：X/Twitter、YouTube、MakerWorld、博客）
- 发布日期（date）
- 标签（多选）
- 草稿内容（rich_text）

**OpenClaw 集成：**
```typescript
// Research scout adds findings to Notion
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js add-entry ${contentDbId} \
    --title "New 3D Print Technique" \
    --properties '${JSON.stringify({
      "Status": { "select": { "name": "Idea" } },
      "Platform": { "multi_select": [{ "name": "YouTube" }] },
      "Tags": { "multi_select": [{ "name": "3D Printing" }] }
    })}'`
});

// Later: Update when drafting
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js update-page ${entryId} \
    --properties '${JSON.stringify({
      "Status": { "select": { "name": "Draft" } },
      "Draft Content": { "rich_text": [{ "text": { "content": "Draft text here..." } }] }
    })}'`
});
```

### 项目管理（个体创业者）

**数据库结构：**
- 名称（title）
- 状态（可选：未开始 → 进行中 → 已阻止 → 完成）
- 优先级（可选：低 → 中等 → 高 → 关键）
- 截止日期（date）
- 预计耗时（number）
- 实际耗时（number）
- 链接（url）
- 备注（rich_text）

**每周回顾集成：**
```typescript
// Query all "In Progress" projects
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js query-database ${projectsDbId} --filter '{"property":"Status","select":{"equals":"In Progress"}}'`
});
```

### 客户/报价 CRM（3D 打印业务）

**数据库结构：**
- 客户名称（title）
- 状态（可选：潜在客户 → 发送报价 → 下单 → 打印 → 已发货）
- 电子邮件（email）
- 报价金额（number）
- 线材类型（可选）
- 截止日期（date）
- Shopify 订单 ID（rich_text）

**Shopify 集成：**
```typescript
// New order → create CRM entry
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js add-entry ${crmDbId} \
    --title "${customerName}" \
    --properties '${JSON.stringify({
      "Status": { "select": { "name": "Ordered" } },
      "Email": { "email": customerEmail },
      "Shopify Order ID": { "rich_text": [{ "text": { "content": orderId } }] }
    })}'`
});
```

### 知识库（替代 MEMORY.md 的 Wiki）

**结构：** 包含嵌套页面的 Hub 页面：
- 🏠 首页（通过集成共享）
  - 标准操作流程（SOPs）
  - 故障排除
  - 设计模式
  - 资源链接

**快速查询：**
```typescript
// Search for "stringing" to find 3D print troubleshooting
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js search "stringing"`
});
```

## 属性类型参考

在创建/更新数据库条目时，请使用以下属性值格式：

```typescript
// Title (always required for new pages)
{ "title": [{ "text": { "content": "Page Title" } }] }

// Select (single choice)
{ "select": { "name": "Option Name" } }

// Multi-select (multiple choices)
{ "multi_select": [{ "name": "Tag 1" }, { "name": "Tag 2" }] }

// Status (for new Status property type)
{ "status": { "name": "In progress" } }

// Text / Rich text
{ "rich_text": [{ "text": { "content": "Your text here" } }] }

// Number
{ "number": 42 }

// Date
{ "date": { "start": "2026-02-15" } }
{ "date": { "start": "2026-02-15T10:00:00", "end": "2026-02-15T12:00:00" } }

// Checkbox
{ "checkbox": true }

// Email
{ "email": "user@example.com" }

// URL
{ "url": "https://example.com" }

// Phone
{ "phone_number": "+1-555-123-4567" }

// Relation (link to another database entry)
{ "relation": [{ "id": "related-page-id-32chars" }] }
```

## 安全性与权限

**关键安全模型：**
- ✅ 集成仅能访问您明确共享的页面
- ✅ 您可以控制每个页面/数据库的访问权限
- ✅ 令牌安全存储在 `~/.openclaw/.env` 中（切勿写入代码）
- ❌ 绝不要将 `NOTION_TOKEN` 提交到 git
- ❌ 集成无法访问私有团队空间或其他用户的私有页面

**最佳实践：**
1. 使用专用的集成（不要重复使用个人集成）
2. 仅共享必要的页面（精确控制权限）
3. 如果集成令牌被泄露，请通过 Notion 集成设置重新生成令牌
4. 定期检查共享的连接

## 环境设置

将以下内容添加到 `~/.openclaw/.env` 文件中：
```bash
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

或者通过命令行设置：
```bash
NOTION_TOKEN=secret_xxx node notion-cli.js ...
```

## 错误处理

常见错误及解决方法：

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| “API 令牌无效” | 令牌错误或集成已被删除 | 在 [notion.so/my-integrations] 中检查令牌 |
| “对象未找到” | 页面未与集成共享 | 共享页面：选择 “共享” → “添加连接” |
| “验证错误” | 属性格式不正确 | 检查数据库中的属性类型 |
| “请求次数过多” | 请求次数过多 | 在请求之间添加延迟 |

## 快速安装（一个命令）

```bash
cd ~/.agents/skills/notion
./install.sh
```

**如果上述方法失败，请手动安装：**
```bash
cd ~/.agents/skills/notion
npm install
```

独立版本无需构建步骤。

## 快速测试

```bash
# After setting NOTION_TOKEN in ~/.openclaw/.env
node notion-cli.js test
```

## 智能 ID 解决方案

可以通过 **Notion 自动 ID**（例如 `#3`）或 **直接 UUID** 来引用条目。

### 通过 Notion ID（推荐手动使用）

使用数据库 ID 列中显示的数字：

```bash
# Get entry #3
node notion-cli.js get-page '#3' DATABASE_ID

# Add content to entry #3
node notion-cli.js append-body '#3' --database DATABASE_ID \
  --text "Research notes" --type h2

# Add bullet to entry #3
node notion-cli.js append-body '#3' --database DATABASE_ID \
  --text "Key finding" --type bullet
```

### 通过直接 UUID（用于自动化）

```bash
# Using full UUID from Notion URL
node notion-cli.js get-page 2fb3e4ac...
node notion-cli.js append-body 2fb3e4ac... \
  --text "Content" --type paragraph
```

**自动检测：** 以 `#` 开头的为 Notion ID；32 个字符的十六进制字符串为直接 UUID。

**专业提示：** 为条目添加一个 `ID` 属性（类型：唯一 ID），例如 #1、#2、#3 等。

## 页面内容编辑

除了属性外，还可以向页面主体中添加富文本内容。

### 添加内容块

```bash
# Add heading
node notion-cli.js append-body PAGE_ID --text "Research Summary" --type h2

# Add paragraph (default)
node notion-cli.js append-body PAGE_ID --text "Detailed findings go here..."

# Add bullet list item
node notion-cli.js append-body PAGE_ID --text "First key finding" --type bullet

# Add numbered list item
node notion-cli.js append-body PAGE_ID --text "Step one description" --type numbered

# Add TODO checkbox
node notion-cli.js append-body PAGE_ID --text "Create video script" --type todo

# Add quote
node notion-cli.js append-body PAGE_ID --text "Important quote from source" --type quote

# Add code block
node notion-cli.js append-body PAGE_ID --text "const result = optimizeSupports();" --type code --lang javascript
```

### 支持的块类型

| 类型 | 描述 | 使用示例 |
|------|-------------|-------------|
| `paragraph` | 普通文本（默认） | 用于描述或解释 |
| `h1`, `h2`, `h3` | 标题 | 用于组织内容结构 |
| `bullet` | 列表 | 用于列出关键内容 |
| `numbered` | 编号列表 | 用于逐步说明 |
| `todo` | 复选框项 | 用于标记待办事项 |
| `quote` | 引用块 | 用于插入来源引用 |
| `code` | 代码块 | 用于插入代码片段 |
| `divider` | 水平线 | 用于分隔不同部分 |

### 获取包含内容的页面

```bash
# Get full page including formatted body
node notion-cli.js get-page PAGE_ID
```

返回值：
- 页面属性
- 格式化的块内容（类型 + 内容预览）
- 块的数量

### 高级：原始 JSON 块

对于复杂的布局，可以使用原始的 Notion 块 JSON 格式：

```bash
node notion-cli.js append-body PAGE_ID --blocks '[
  {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Research Notes"}}]}},
  {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"Finding 1"}}]}},
  {"object":"block","type":"code","code":{"rich_text":[{"text":{"content":"console.log(1)"}}],"language":"javascript"}}
]'
```

## 高级：Webhook 同步

实现双向同步（Notion 的更改 → OpenClaw）：
1. 设置 Notion 的 webhook 集成（需要 Notion 合作伙伴账户）
2. 将 webhook 端点配置到您的 OpenClaw Gateway
3. 该功能会处理传入的 webhook 并更新内存文件

详细信息请参阅 [references/webhooks.md](references/webhooks.md)。

---

**需要帮助？** 请查看您的 Notion 集成设置：[https://www.notion.so/my-integrations]

## 在 OpenClaw 中使用

### 快速设置

```bash
# 1. Install
cd ~/.agents/skills/notion
npm install

# 2. Configure token
echo "NOTION_TOKEN=secret_xxxxxxxxxx" >> ~/.openclaw/.env

# 3. Test connection
node notion-cli.js test
```

### 通过 OpenClaw Agent 使用

```typescript
// Query database
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js query-database YOUR_DB_ID`
});

// Add entry
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js add-entry YOUR_DB_ID \\
    --title "New Content Idea" \\
    --properties '{"Status":{"select":{"name":"Idea"}}}'`
});

// Search
await exec({
  command: `node ~/.agents/skills/notion/notion-cli.js search "tree support"`
});
```

### 使用 Cron 作业

更新您的 Research Topic Scout 以将数据推送到 Notion：

```typescript
"message": "Research trends and add to Notion: 
  node ~/.agents/skills/notion/notion-cli.js add-entry DB_ID 
    --title '<title>' 
    --properties '{...,\"Platform\":{\"multi_select\":[{\"name\":\"X\"}]}}'"
```