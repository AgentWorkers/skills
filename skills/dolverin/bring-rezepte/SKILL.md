---
name: bring-rezepte
version: 1.3.0
description: **使用说明：**  
当运行 OpenClaw/ClawHub 的 “Bring!” 技能时，该功能可用于在网页上搜索食谱，解析食谱 URL 中的食材信息，并将这些食材添加到购物清单中。具体包括通过 `web_search` 功能进行食谱搜索、解析 URL 中的食材信息、批量添加食谱到购物清单、管理购物清单以及使用各种筛选器来获取灵感。
metadata:
  openclaw:
    emoji: "🛒"
    requires:
      bins: ["node"]
      env:
        - name: BRING_EMAIL
          description: "Bring! account email address"
          required: true
        - name: BRING_PASSWORD
          description: "Bring! account password"
          required: true
        - name: BRING_COUNTRY
          description: "Country code for Bring! (e.g. DE, AT, CH)"
          required: false
          default: "DE"
---

# Bring App

## 使用场景

- 用户请求食谱建议或季节性菜肴（例如：“我们今天吃什么？”，“食谱推荐”，“季节性美食灵感”）
- 用户希望查看或更新购物清单（例如：“购物清单里有什么？”，“添加……到清单中”）
- 用户想要为某道食谱添加食材
- 用户询问购物清单的状态或食谱的标记信息
- 与购物计划和食谱选择相关的所有查询

## 概述

本技能主要基于 Bring! CLI 构建，利用更新的 `node-bring-api` 来获取食谱灵感、突出显示季节性菜肴，并将用户选择的食材添加到购物清单中。

**重要提示：** 在将任何食材添加到清单之前，务必先获得用户的明确确认！

## 快速启动工作流程

1. 列出灵感筛选条件并识别季节性标签。
2. 使用这些标签获取食谱建议。
3. 显示 3-7 道季节性菜肴。
4. **务必询问**：“我是否应该将 [食谱名称] 的食材添加到购物清单中？”
5. 仅在用户明确确认后，才添加相应的食材（而非菜肴名称）。

请参考 `references/bring-inspirations.md` 以获取端点详情和头部信息。
这些脚本从以下位置加载 `node-bring-api`：
- `BRING_NODE_API_PATH`（如果已设置）
- 或者相对于当前技能目录的 `../../node-bring-api/build/bring.js`
- 或者已安装的 `bring-shopping` 包。

## 任务

### 1) 查找可用的筛选条件（季节、饮食类型、菜系）

运行：

```
node scripts/bring_inspirations.js --filters
```

- 读取 JSON 数据并筛选出具有季节性标签的选项（例如：winter/summer/fruehling/herbst）。
- 如果不确定，让用户从筛选列表中选择。

### 2) 获取食谱建议

运行：

```
node scripts/bring_inspirations.js --tags "<comma-separated-tags>" --limit 20
```

- 如果用户未指定筛选条件，使用默认值 `mine`。
- 遍历 JSON 数据，提取建议的菜肴列表及其元数据。
- 获取每道菜肴的 `content.contentSrcUrl`（用于加载食材信息）。

### 3) 推荐季节性菜肴

- 返回 3-7 道菜肴选项。
- 包括菜肴名称和简短的描述（如果 JSON 中有提供）。
**重要提示**：务必询问：“您希望将哪些食谱的食材添加到购物清单中？”
- 等待用户的明确确认。

### 4) 将选定的菜肴添加到清单中（仅添加食材）

**仅在用户明确确认后**，如果需要，列出可用的清单：

```
node scripts/bring_list.js --lists
```

从选定的菜肴内容 URL 中提取食材：

```
node scripts/bring_list.js --list <list-uuid> --content-url "https://api.getbring.com/rest/v2/bringtemplates/content/<uuid>"
```

或者通过清单名称来添加食材：

```
node scripts/bring_list.js --list-name "Einkauf" --content-url "https://api.getbring.com/rest/v2/bringtemplates/content/<uuid>"
```

## 购物清单管理（v2.2.0）

创建新的购物清单：

```
node scripts/bring_list.js --create-list "Amazon"
```

返回新清单的 UUID 和名称。如果已存在同名清单，则返回现有清单的信息，避免重复创建。

**注意：** Bring API 不支持删除清单——清单只能通过 Bring 应用程序来删除。

## 环境配置

这些脚本使用以下环境变量：
- `BRING_EMAIL`
- `BRING_PASSWORD`
- `BRING_country`（默认为 `DE`）
- `BRING_NODE_API_PATH`（可选路径，指向 `build/bring.js`）

如果环境变量未设置，请通过 `--email` 和 `--password` 参数明确传递。

## 食谱标记（v2.1.0）

为食材添加食谱名称标签，以便追踪哪些食材属于哪道食谱：

```
node scripts/bring_list.js --list-name "Einkauf" --add-recipe "Lasagne" --recipe-items "Nudeln,Hackfleisch,Tomaten"
```

这样每个食材都会被标记为 `[Rezept] Lasagne`，表示它属于某道特定的食谱。

列出清单上的所有食谱标记：

```
node scripts/bring_list.js --list-name "Einkauf" --recipe-markers
```

返回当前清单上所有食谱名称的排序数组。

## 食谱搜索与 URL 解析（v2.2.0）

### 工作流程：提供食谱建议

当用户请求食谱建议时（例如：“我今天想做什么菜？”，“夏季食谱推荐”）：

**步骤 1：搜索食谱**
使用 `web_search` 工具（Brave API）查找食谱 URL：

```
web_search("Sommer Rezepte vegetarisch site:chefkoch.de")
web_search("schnelle Abendessen Rezepte site:chefkoch.de OR site:lecker.de")
```

从搜索结果中挑选 3-5 道合适的食谱 URL。

**步骤 2：解析食谱 URL 以获取结构化数据**

```
node scripts/bring_inspirations.js --parse-url "url1,url2,url3"
```

为每道食谱返回结构化的 JSON 数据：名称、食材（itemId + spec）、图片 URL、来源 URL。
对于单个 URL，返回一个对象；对于多个 URL，返回一个数组。

**步骤 3：向用户展示解析后的结果**
向用户展示解析后的食谱信息，包括：
- 食谱名称
- 食材数量
- 来源 URL
- 主要食材（前 5-6 种）

**务必询问**：“您是否希望将 [食谱名称] 的食材添加到购物清单中？”
**步骤 4：将选定的食谱添加到清单中（仅在用户确认后）**

```
node scripts/bring_list.js --list-name "Einkauf" --add-recipe-url "https://www.chefkoch.de/rezepte/123/lasagne.html"
```

解析食谱信息后，为每道食谱添加标记（例如：`=== LASAGNE ===`），并将所有相关食材标记为该食谱的标签，然后批量添加到清单中。

### 独立解析食谱 URL

```
node scripts/bring_inspirations.js --parse-url "https://www.chefkoch.de/rezepte/123/lasagne.html"
```

单独解析食谱 URL，但不将其添加到任何清单中。此功能用于预览食谱信息。

### 支持的食谱网站

Bring 解析器支持大多数主流食谱网站，包括：
- chefkoch.de
- lecker.de
- eatsmarter.de
- kitchenstories.com
- 以及更多提供结构化食谱数据的网站（支持 JSON-LD 格式的网站）

## 食谱图片

**重要提示：** **切勿自行生成食谱图片**。食谱网站通常会提供图片，应直接使用这些图片。

### 从 URL 中提取食谱图片

**方法 1：使用 `--parse-url`（推荐方法）**

如果解析器支持该网站，图片 URL 会直接包含在 JSON 响应中：

```bash
node scripts/bring_inspirations.js --parse-url "https://www.chefkoch.de/rezepte/123/lasagne.html"
# Returns: { ..., "image": "https://img.chefkoch-cdn.de/rezepte/123/lasagne.jpg", ... }
```

**方法 2：备用方案（手动使用 `web_fetch`）**

如果 `--parse-url` 失败或未找到图片，可以使用 `web_fetch` 功能提取 Open Graph 图片标签：

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

### 带图片的食谱建议工作流程

1. 搜索食谱 URL（使用 `web_search`）
2. 解析食谱 URL（使用 `--parse-url` 或 `web_fetch`）
3. **提取食谱图片 URL**（无需下载）
4. 向用户展示食谱信息，包括：
   - 食谱名称
   - 图片（通过 URL 嵌入：`![](image_url)`）
   - 主要食材
   - 来源 URL
5. **务必询问**：“您是否希望将此食谱的食材添加到购物清单中？”
6. **仅在用户确认后**，将食材添加到清单中

### 示例：完整的食谱处理流程

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
# Zutaten: Lachs, Honig, Senf, Olivenöl, Knoblauch...

# Step 4: IMMER FRAGEN
# "Soll ich die Zutaten für Honig-Senf-Lachs zur Bring-Liste hinzufügen?"
# Warte auf: Ja / Nein / Bestätigung

# Step 5: NUR BEI BESTÄTIGUNG hinzufügen
# node scripts/bring_list.js --list-name "Zuhause" --add-recipe "Honig-Senf-Lachs" --recipe-items "..."
```

### 示例对话

**助手**：“我找到了 3 道美味的食谱：
1. 🍝 碳ara 意面（5 种食材）
2. 🍛 鸡咖喱（9 种食材）
3. 🥗 希腊沙拉（7 种食材）
**您希望将哪些食谱添加到购物清单中？**

**用户**：“咖喱听起来不错。”

**助手**：“我是否应该将鸡咖喱的食材添加到名为 ‘Zuhause’ 的购物清单中？（共 9 种食材：鸡肉、椰奶、咖喱……）”

**用户**：“是的。”

**助手**：“✅ 已将鸡咖喱的食材添加到购物清单中！”

### 多个食谱的处理

当用户选择多道食谱时，务必逐一确认或再次询问：
- “我是否要将所有 3 道食谱都添加到清单中？”
- “您想添加哪道或哪些食谱？（1 道、2 道、3 道还是全部？”

**注意事项：**
- 食谱图片来自原始网站，切勿自行生成。
- 直接使用图片 URL——无需下载（平台会自动加载图片）。
- `web_fetch` 功能无需执行任何下载操作，且与 OpenClaw 兼容良好。

## 其他注意事项

- 本技能的输出默认使用德语（针对德国用户）。
- **重要提示**：**绝对不要在未经用户确认的情况下添加任何食材！**
- **务必询问**：“您是否希望将食材添加到购物清单中？”
- **仅在用户确认后**，才将食材添加到清单中。
- 使用食谱建议时，始终添加食材名称，而非菜肴名称。
- 当用户选择多道食谱时，需逐一确认或一次性全部确认。

## 资源文件

### 脚本文件

- `scripts/bring_inspirations.js`：用于登录并调用食谱建议和筛选相关端点。
- `scripts/bring_list.js`：用于列出可用的购物清单并添加食材。

### 参考文档

- `references/bring-inspirations.md`：包含端点详情和头部信息。