---
name: daily-ai-news
description: >
  **适用场景：**  
  当用户需要每日获取关于人工智能（AI）、大型模型及相关领域的全面新闻时。
---
# 每日AI新闻技能

该技能帮助AI代理从60s API获取并展示每日精选的AI新闻，该API提供有关AI、大型语言模型及相关技术的最新更新。

## 何时使用此技能

当用户执行以下操作时，可以使用此技能：
- 询问当天的AI新闻或大型语言模型的更新情况
- 希望快速获取每日的人工智能简报
- 请求AI新闻摘要
- 需要特定日期的历史AI新闻
- 希望以不同的格式（文本、JSON、markdown）获取AI新闻

## 使用方法

执行关联的`scripts/news.sh`脚本来获取AI新闻。

```bash
./scripts/news.sh [options] [date]
```

### 选项

- `--encoding, -e <format>`：可选。指定输出响应的格式。有效选项为`text`、`json`和`markdown`。如果未指定，默认使用`json`格式。
- `--date, -d <YYYY-MM-DD>`：可选。为特定日期获取历史AI新闻。如果省略，则获取当天的新闻。注意：如果这是唯一提供的参数，可以完全省略`--date`标志。

### 返回值

该脚本会安全地调用60s AI新闻API，并将响应输出到`stdout`。根据`encoding`参数的不同，响应可能是JSON字符串、纯文本或markdown格式。

### 使用示例

```bash
# Get today's AI news using default API encoding (json)
./scripts/news.sh

# Get today's AI news in plain text format
./scripts/news.sh --encoding text

# Get AI news for a specific date using flags
./scripts/news.sh --date 2024-03-01

# Get AI news for a specific date (simplified usage without flags)
./scripts/news.sh 2024-03-01

# Get AI news for a specific date in markdown format
./scripts/news.sh -e markdown -d 2024-03-01
```

## 响应格式

为了在信息深度和Token消耗之间取得平衡，必须遵循以下规则来使用`encoding`参数：

1. **默认策略（`--encoding markdown`）**
   - **使用场景：**适用于标准的AI新闻查询。
   - **原因：**提供结构清晰、易于阅读的信息，同时控制Token的使用量。

2. **简短信息（`--encoding text`）
   - **使用场景：**当用户明确请求简短或摘要形式的AI新闻时。
   - **原因：**仅返回必要的详细信息，以最少的Token消耗实现。

3. **完整信息（`--encoding json`）
   - **使用场景：**仅当用户明确要求原始数据、详细字段或全面信息时。
   - **原因：**返回完整的API响应内容，但会消耗较多的Token。