---
name: daily-news
description: >
  **使用场景：**  
  当用户需要每日新闻摘要、时事资讯，或希望以中文形式了解世界新闻时，可以使用该功能。
---
# 每日新闻技能

该技能帮助AI代理从60s API获取并展示每日精选的新闻，该API提供15条精选新闻以及一句每日名言。

## 何时使用此技能

当用户以下情况时，可以使用此技能：
- 询问当天的新闻或时事
- 需要快速的每日简报
- 请求中文的新闻摘要
- 需要特定日期的历史新闻
- 希望以不同的格式（文本、markdown、图片）获取新闻

## 使用方法

执行相关的`scripts/news.sh`脚本来获取新闻。

```bash
./scripts/news.sh [options] [date]
```

### 选项

- `--encoding, -e <format>`：可选。指定输出响应的格式。有效选项包括`text`、`json`、`markdown`、`image`和`image-proxy`。如果未指定，API默认使用`json`格式。
- `--date, -d <YYYY-MM-DD>`：可选。用于获取特定日期的历史新闻。如果省略，则获取当天的新闻。注意：如果这是唯一提供的参数，可以完全省略`--date`标志。

### 返回值

脚本会安全地调用60s API，并将响应输出到`stdout`。根据`encoding`参数的不同，响应可能是JSON字符串、纯文本、markdown或图片URL。

### 使用示例

```bash
# Get today's news using default API encoding (json)
./scripts/news.sh

# Get today's news in plain text format
./scripts/news.sh --encoding text

# Get news for a specific date using flags
./scripts/news.sh --date 2024-03-01

# Get news for a specific date (simplified usage without flags)
./scripts/news.sh 2024-03-01

# Get news for a specific date in markdown format
./scripts/news.sh -e markdown -d 2024-03-01
```

## 响应格式

在需要基于文本的输出时，为了平衡信息深度和令牌消耗，必须遵循以下规则来设置`encoding`参数：
**注意：**即使请求图片输出，也应使用`image`或`image-proxy`。

1. **默认策略（`--encoding markdown`）**
   - **使用场景：**适用于标准的每日新闻查询。
   - **原因：**提供结构良好、易于阅读的信息，同时令牌消耗适中。

2. **简短信息（`--encoding text`）
   - **使用场景：**当用户明确请求简短或摘要新闻时。
   - **原因：**仅返回必要的详细信息，以节省最多的令牌。

3. **完整信息（`--encoding json`）
   - **使用场景：**仅当用户明确请求原始数据、详细字段或全面信息时。
   - **原因：**返回完整的API数据，但令牌消耗较高。

## 故障排除

### 问题：没有返回数据
- **解决方案：**尝试请求之前的日期（昨天或前一天）。
- 服务会自动尝试获取最近3天的数据。

### 问题：图片无法加载
- **解决方案：**使用`encoding=image-proxy`代替`encoding=image`。
- 代理端点直接返回图片的二进制数据。

### 问题：请求的日期过旧
- **解决方案：**数据仅适用于最近的日期。
- 请检查响应状态码。