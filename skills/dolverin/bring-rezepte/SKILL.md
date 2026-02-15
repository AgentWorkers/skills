---
name: bring-rezepte
version: 1.2.0
description: **使用说明：**  
当运行 OpenClaw/ClawHub 的 “Bring!” 技能时，该功能可用于在网页上搜索食谱、解析食谱 URL 中的食材信息，并将这些食材添加到购物清单中。具体包括通过 `web_search` 功能进行食谱搜索、解析 URL 中的食材信息、批量添加食谱到购物清单、管理购物清单以及使用各种筛选器来获取灵感。
---

# Bring App

## 使用场景

- 用户请求食谱建议或季节性菜肴推荐（例如：“今天吃什么？”，“食谱推荐”，“季节性美食灵感”）
- 用户希望查看或更新购物清单（例如：“购物清单里有什么？”，“添加……到清单中”）
- 用户想要为某道食谱添加食材
- 用户询问购物清单的状态或食谱的标记信息
- 与购物计划和食谱选择相关的所有查询

## 概述

本技能专注于使用 `Bring!` CLI，通过更新的 `node-bring-api` 来获取食谱灵感、突出显示季节性菜肴，并将用户选定的食材添加到购物清单中。

## 快速上手流程

1. 列出灵感筛选条件并识别季节性标签。
2. 使用这些标签获取食谱推荐。
3. 概述3-7道季节性菜肴。
4. 询问用户希望将哪些菜肴添加到清单中，然后添加这些菜肴的食材（而非菜肴名称）。

请参考 `references/bring-inspirations.md` 以获取端点详情和头部信息。
这些脚本从以下位置加载 `node-bring-api`：
- `BRING_NODE_API_PATH`（如果已设置）
- 或者相对于本技能的 `../../node-bring-api/build/bring.js`
- 或者已安装的 `bring-shopping` 包。

## 任务

### 1) 查找可用的筛选条件（季节、饮食类型、菜系）

运行：

```
node scripts/bring_inspirations.js --filters
```

- 读取 JSON 数据并挑选出具有季节性特征的标签（例如：winter/summer/fruehling/herbst）。
- 如果不确定，让用户从筛选列表中选择。

### 2) 获取食谱推荐

运行：

```
node scripts/bring_inspirations.js --tags "<comma-separated-tags>" --limit 20
```

- 如果用户未指定标签，使用默认标签 `mine`。
- 查看 JSON 数据并提取一份包含元数据的推荐菜肴列表。
- 获取每道菜肴的 `content.contentSrcUrl`（用于加载食材信息）。

### 3) 推荐季节性菜肴

- 返回3-7个选项。
- 包括菜肴名称和简短的描述（如果 JSON 中有提供）。
- 询问用户希望将哪些菜肴添加到清单中。

### 4) 将选定的菜肴添加到清单中（仅添加食材）

如果用户确认，根据需要列出可用的清单：

```
node scripts/bring_list.js --lists
```

从选定的菜肴内容 URL 中获取食材信息：

```
node scripts/bring_list.js --list <list-uuid> --content-url "https://api.getbring.com/rest/v2/bringtemplates/content/<uuid>"
```

或者通过清单名称来添加食材：

```
node scripts/bring_list.js --list-name "Einkauf" --content-url "https://api.getbring.com/rest/v2/bringtemplates/content/<uuid>"
```

## 购物清单管理（v2.2.0）

创建一个新的购物清单：

```
node scripts/bring_list.js --create-list "Amazon"
```

返回新清单的 UUID 和名称。如果同名清单已存在，则返回现有清单的信息，避免重复创建。

注意：`Bring API` 不支持删除清单——清单只能通过 Bring 应用程序来删除。

## 环境配置

这些脚本默认使用以下环境变量：
- `BRING_EMAIL`
- `BRING_PASSWORD`
- `BRING_country`（默认为 `DE`）
- `BRING_NODE_API_PATH`（可选的 `build/bring.js` 路径）

如果环境变量未设置，请明确传递 `--email` 和 `--password`。

## 食谱标记（v2.1.0）

为食材添加食谱名称标签，以便追踪食材所属的食谱：

```
node scripts/bring_list.js --list-name "Einkauf" --add-recipe "Lasagne" --recipe-items "Nudeln,Hackfleisch,Tomaten"
```

这会将每个食材标记为 `[Rezept] Lasagne`，以此表示该食材属于某道食谱。

列出清单中的所有食谱标记：

```
node scripts/bring_list.js --list-name "Einkauf" --recipe-markers
```

返回当前清单中所有食谱名称的排序数组。

## 食谱搜索与 URL 解析（v2.2.0）

### 工作流程：生成食谱推荐

当用户请求食谱建议时（例如：“今天应该做什么菜？”，“夏季食谱推荐”）：

**步骤 1：搜索食谱**
使用 `web_search` 工具（Brave API）查找食谱 URL：

```
web_search("Sommer Rezepte vegetarisch site:chefkoch.de")
web_search("schnelle Abendessen Rezepte site:chefkoch.de OR site:lecker.de")
```

从搜索结果中挑选出3-5个有潜力的食谱 URL。

**步骤 2：解析食谱 URL 以获取结构化数据**

```
node scripts/bring_inspirations.js --parse-url "url1,url2,url3"
```

为每道食谱返回结构化的 JSON 数据：名称、食材（itemId + spec）、图片 URL、来源 URL。
对于单个 URL，返回一个对象；对于多个 URL，返回一个数组。

**步骤 3：向用户展示选项**
向用户展示解析后的食谱信息，包括：
- 食谱名称
- 食材数量
- 来源 URL
- 主要食材（前5-6种）

询问用户希望将哪些食谱添加到购物清单中。

**步骤 4：将选定的食谱添加到清单中**

```
node scripts/bring_list.js --list-name "Einkauf" --add-recipe-url "https://www.chefkoch.de/rezepte/123/lasagne.html"
```

解析食谱信息，创建相应的标记（例如：`=== LASAGNE ===`），将所有食材标记为相应的食谱名称，然后批量添加到清单中。

### 单独解析食谱 URL

```
node scripts/bring_inspirations.js --parse-url "https://www.chefkoch.de/rezepte/123/lasagne.html"
```

返回食材的结构化数据，但不将其添加到任何清单中。此功能用于预览食谱。

### 支持的食谱网站

`Bring` 解析器支持大多数主流食谱网站，包括：
- chefkoch.de
- lecker.de
- eatsmarter.de
- kitchenstories.com
- 以及更多提供结构化食谱数据的网站（支持 JSON-LD 格式的网站）

## 食谱图片

**重要提示：** **切勿自行生成食谱图片。** 食谱网站通常会提供图片，应直接使用这些图片。

### 从 URL 中提取食谱图片

**方法 1：使用 `--parse-url`（推荐方法）**

如果解析器支持该网站，图片 URL 会直接包含在 JSON 响应中：

```bash
node scripts/bring_inspirations.js --parse-url "https://www.chefkoch.de/rezepte/123/lasagne.html"
# Returns: { ..., "image": "https://img.chefkoch-cdn.de/rezepte/123/lasagne.jpg", ... }
```

**方法 2：备用方法（手动使用 `web_fetch`）**

如果 `--parse-url` 失败或未返回图片，可以使用 `web_fetch` 来提取 Open Graph 图片标签：

```javascript
// Use web_fetch tool to get HTML (no exec approval needed)
web_fetch("https://www.chefkoch.de/rezepte/123/lasagne.html")

// Parse the returned markdown/text for og:image meta tag
// Extract URL from: <meta property="og:image" content="https://...">
```

提取到的图片 URL 可以直接用于 Markdown 或 Discord 嵌入——**无需下载**：

```markdown
![Recipe Image](https://img.chefkoch-cdn.de/rezepte/123/lasagne.jpg)
```

### 带有图片的食谱推荐工作流程

1. 搜索食谱 URL（使用 `web_search`）
2. 解析食谱 URL（使用 `--parse-url` 或 `web_fetch` 作为备用方法）
3. **提取食谱图片 URL**（无需下载）
4. 向用户展示食谱信息，包括：
   - 食谱名称
   - 图片（通过 URL 嵌入：`![](image_url)`)
   - 主要食材
   - 来源 URL
5. 用户确认后，将食谱添加到购物清单中。

### 完整的食谱工作流程示例

```bash
# Step 1: Search
web_search("Lachs Honig Senf Rezept")

# Step 2: Parse via --parse-url (preferred)
node scripts/bring_inspirations.js --parse-url "https://www.eatclub.de/rezept/honig-senf-lachs/"
# → { ..., "image": "https://www.eatclub.de/wp-content/uploads/2023/09/shutterstock-416951386.jpg" }

# Step 2 (Fallback): Use web_fetch if parser fails
web_fetch("https://www.eatclub.de/rezept/honig-senf-lachs/")
# Parse HTML response for: <meta property="og:image" content="...">

# Step 3: Present to user with image URL embedded
# ![Honig-Senf-Lachs](https://www.eatclub.de/wp-content/uploads/2023/09/shutterstock-416951386.jpg)

# Step 4: Add to list on confirmation
```

**注意：**
- 食谱图片来自原始网站，切勿自行生成。
- 直接使用图片 URL——无需下载（平台会自动加载图片）。
- `web_fetch` 方法无需执行任何下载操作，且与 OpenClaw 兼容。

## 其他注意事项

- 本技能的输出默认使用德语（针对德国用户）。
- 未经用户明确确认，切勿添加任何项目到清单中。
- 使用食谱推荐功能时，始终添加食材名称，而非菜肴名称。

## 资源文件

### 脚本文件

- `scripts/bring_inspirations.js`：用于登录并调用食谱推荐和筛选相关端点。
- `scripts/bring_list.js`：用于列出可用的购物清单并添加食材。

### 参考文档

- `references/bring-inspirations.md`：端点详情和头部信息。