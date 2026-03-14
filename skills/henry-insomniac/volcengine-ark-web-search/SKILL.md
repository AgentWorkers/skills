---
name: volcengine-ark-web-search
description: 当您需要通过 Volcengine 的 ARK Responses API 获取最新的网页内容时，请使用此方法。这适用于获取今日新闻、最新更新、事实核查结果、主题监控数据，或是使用 ARK_API_KEY 进行的中文语言搜索。
metadata:
  openclaw:
    requires:
      env:
        - ARK_API_KEY
      anyBins:
        - python3
    primaryEnv: ARK_API_KEY
    homepage: "https://www.volcengine.com/docs/82379/1783703?lang=zh"
---
# Volcengine Ark Web Search

## 概述

当任务需要获取最新的公共网页信息，并且运行时需要通过 Volcengine ARK Responses API 而不是模型内置的浏览功能时，可以使用此技能。该脚本将 ARK 的响应数据与 `web_search` 工具结合使用，输出结果默认为中文格式，适用于可重复的自动化操作或本地代理工作流程。

默认的 Markdown 输出结构包括三个部分：
- 标题（title）
- 摘要（summary）
- 来源（sources）

## 适用场景

- 用户请求获取当天的新闻、最新更新、当前的公开报道或实时事实核查内容。
- 需要获取最新的网页结果，但必须通过 `ARK_API_KEY` 通过 Volcengine ARK 来获取数据。
- 需要一个可复用的本地命令，以便在脚本、定时任务（cron jobs）或其他技能中调用。
- 答案应优先使用中文格式，包含明确的日期和来源链接。
- 在回答之前需要比较或验证公共网页信息。

## 不适用场景

- `ARK_API_KEY` 未设置。
- 任务内容是静态的，不需要最新的网页信息。
- 需要浏览器自动化操作、身份验证会话或特定网站的交互功能，而不是简单的搜索。
- 必须使用其他搜索服务提供商。

## 快速入门

1. 确保 `ARK_API_KEY` 已设置。
2. 运行捆绑好的脚本。
3. 使用中文格式总结返回的结果，并附上明确的日期和来源链接。

**基本用法：**

```bash
python3 scripts/ark_web_search.py "What are today's AI news headlines?"
```

**中文查询示例：**

```bash
python3 scripts/ark_web_search.py "今天有什么热点新闻"
```

**自定义模型示例：**

```bash
python3 scripts/ark_web_search.py "OpenAI latest announcements" \
  --model doubao-seed-1-6-250615
```

**结构化 JSON 输出示例：**

```bash
python3 scripts/ark_web_search.py "latest semiconductor policy news" \
  --format json
```

**设置较长的超时时间并启用快速重试：**

```bash
python3 scripts/ark_web_search.py "OpenAI latest news" \
  --timeout 90 \
  --retries 2
```

**无网络环境下的模拟运行：**

```bash
python3 scripts/ark_web_search.py "today's EV market news" \
  --dry-run
```

## 核心工作流程

1. 根据需要将用户请求转换为直接的搜索问题（应包含具体的实体、主题和时间范围）。
2. 除非任务要求原始的传递行为，否则使用系统的默认提示语。
3. 运行 `scripts/ark_web_search.py` 脚本。
4. 如果脚本返回了足够的信息，使用中文进行总结（除非用户要求使用其他语言）。
5. 对于“今天”或“最近”等相对时间范围的查询，应在最终答案中提供具体的日期。

## 输出要求

- 输出内容应简洁明了，并附有链接。
- 默认的 Markdown 格式应易于阅读：首先是标题，然后是摘要，最后是来源。
- 当搜索结果较少或存在冲突时，应保留不确定性。
- 如果有来源信息，应将其包含在内。
- 尽可能将相对日期转换为具体的日期格式。
- 如果 API 返回的信息不足，应如实说明，而不是编造事实。

## 相关文件

- `scripts/ark_web_search.py`：用于调用 ARK Responses API 的脚本，支持模拟运行、流式处理和提取来源信息。
- `references/ark-responses-api.md`：包含关于请求格式、模型变化、工具名称变更以及维护相关信息的说明。

## 维护说明

- 可以使用 `--model` 或 `ARK_MODEL` 参数来指定使用的模型。ARK 模型的可用性会随时间变化。
- `--timeout` 参数用于设置每次请求的超时时间。使用 `--retries` 参数可以在请求失败时自动重试。
- 有些 ARK 环境会因 `search_context_size` 参数而返回 HTTP 400 错误。如果服务器提示该参数不受支持，此脚本会自动忽略该参数并继续执行。
- 系统的默认提示语仅要求模型返回摘要内容。标题和来源部分由脚本添加，以保持输出的一致性。
- 过去 Volcengine 的文档中同时提到了 `web_search` 和 `web_search_preview` 两种方法。此技能默认使用 `web_search`，只有在目标环境的官方文档有明确要求时才需要更改。
- 如果上游 API 发生变化导致解析失败，需更新 `scripts/ark_web_search.py` 中的解析逻辑，并确保 `references/ark-responses-api.md` 的内容保持同步。