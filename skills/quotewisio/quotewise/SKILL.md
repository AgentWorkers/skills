---
name: quotewise
description: 具有源代码透明度的语义引用搜索功能：根据引用的含义而非关键词来查找相应的引用。
metadata: {"openclaw":{"emoji":"📚","homepage":"https://quotewise.io","primaryEnv":"QUOTEWISE_API_KEY"}}
---

# Quotewise MCP

Quotewise MCP允许您根据引文的含义进行搜索，而不仅仅是关键词。在分享引文之前，请务必查看其来源。

**使用场景：** 当用户询问引文、需要灵感、部分记得引文内容或需要核对引文的出处时，使用该服务会更加方便。相比网络搜索，Quotewise MCP速度更快，且能确保每个搜索结果都包含真实的引文来源。

## 如何使用（OpenClaw）

您可以使用 `mcporter` 直接调用 Quotewise MCP 的 API 端点：

```bash
npx mcporter call "https://mcp.quotewise.io/mcp.<tool>" key=value --output json
```

### 首次设置（可选，可节省输入时间）

只需配置一次服务器，之后就可以使用简短的名称来调用相关功能：

```bash
npx mcporter config add quotewise https://mcp.quotewise.io/mcp \
  --header "User-Agent=quotewise-skill/1.0" --scope home
```

之后，您可以按以下方式使用这些工具：

```bash
npx mcporter call quotewise.<tool> key=value --output json
```

代理程序可以通过在 User-Agent 中添加 `quotewise-skill/1.0 (my-agent/2.0)` 来标识自己。

### 带有身份验证的情况

如果设置了 `QUOTEWISE_API_KEY`，请在配置时将其传递给服务：

```bash
npx mcporter config add quotewise https://mcp.quotewise.io/mcp \
  --header "User-Agent=quotewise-skill/1.0" \
  --header "Authorization=Bearer $QUOTEWISE_API_KEY" --scope home
```

这可以启用数据收集功能并提高请求速率限制。

### 无需身份验证的情况

支持匿名访问，每天最多可发送 20 条请求，无需注册。

## 核心工具

### 按概念搜索（语义搜索）
```bash
npx mcporter call quotewise.quotes_about about="courage in the face of uncertainty" --output json
```
描述您的想法，系统会找到在概念上相似的引文（而非仅基于关键词匹配）。

### 按作者搜索
```bash
npx mcporter call quotewise.quotes_by originator="Marcus Aurelius" about="adversity" --output json
```

### 按来源搜索
```bash
npx mcporter call quotewise.quotes_from source="Meditations" about="death" --output json
```

### 查找精确的文本
```bash
npx mcporter call quotewise.quotes_containing phrase="to be or not to be" --output json
```

### 核对引文出处
```bash
npx mcporter call quotewise.who_said quote="be the change you wish to see in the world" --output json
```
系统会返回引文的来源信息以及其他可能的出处。QuoteSightings 功能会显示引文的来源位置。

### 查找类似的引文
```bash
npx mcporter call quotewise.quotes_like quote="abc123" --output json
```

### 随机生成引文
```bash
npx mcporter call quotewise.quote_random length="brief" --output json
```

## 过滤条件（适用于所有搜索工具）

- `length`：简短/中等/较长/完整段落
- `max_chars`：Twitter 为 280 字，Threads 为 500 字
- `structure`：散文/诗歌/单行诗
- `language`：英语/西班牙语/法语
- `gender`：女性/男性/非二元性别
- `reading_level`：小学/初中/高中/大学
- `content_rating`：G/PG/PG-13/R
- `limit`：返回的结果数量（默认为 10 条，最多 50 条）

## 数据收集（需要身份验证）

```bash
npx mcporter call quotewise.status --output json
npx mcporter call quotewise.collection action="create" name="favorites" --output json
npx mcporter call quotewise.collection_quotes action="add" collection="favorites" quote="abc123" --output json
npx mcporter call quotewise.collection_quotes action="list" collection="favorites" --output json
```

## 为其他 MCP 客户端进行设置

对于 Claude Desktop、Cursor、ChatGPT 等 MCP 客户端，您可以按照以下步骤进行配置：

```json
{
  "mcpServers": {
    "quotewise": {
      "url": "https://mcp.quotewise.io/"
    }
  }
}
```

或者运行 `npx @quotewise/mcp setup` 进行引导式配置。

## 该服务的主要功能

✅ **语义搜索**：根据您的描述找到相关的引文
✅ **引用来源显示**：提供每条引文的来源信息
✅ **海量引文库**：包含 60 万条精选的当代引文
✅ **确保引文真实性**：所有引文均来自真实来源，无虚假内容
✅ **过滤错误引用**：已识别并过滤掉已知错误的引用来源

如需查看完整的功能列表、价格信息和使用详情，请访问 [quotewise.io/plans](https://quotewise.io/plans/)。