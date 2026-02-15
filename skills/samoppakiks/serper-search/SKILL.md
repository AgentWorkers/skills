# Serper Google Search 插件

这是一个专为通过 [Serper.dev](https://serper.dev) API 进行 Google 搜索而设计的原生 Clawdbot 插件。它能够通过一次调用返回真实的 Google 搜索结果，包括自然搜索结果、知识图谱、新闻以及“人们也在问”的相关问题。

## 使用场景

- 当您需要获取带有链接和摘要的 **真实 Google 结果**（而非 AI 合成的答案）时；
- 当您希望获取关于某个主题的 Google 新闻文章时；
- 当您需要知识图谱数据（如快速事实、实体信息）时；
- 该插件可以与 AI 搜索工具（如 Perplexity、Brave）结合使用，提供原始的 Google 数据。

## 设置方法

1. 在 [serper.dev](https://serper.dev) 获取免费的 API 密钥（每月 2,500 次搜索次数，无需信用卡）；
2. 在您的 Clawdbot 配置文件中设置相应的环境变量：

```json
{
  "env": {
    "vars": {
      "SERPER_API_KEY": "your-api-key-here"
    }
  }
}
```

或者直接在插件配置中设置：

```json
{
  "plugins": {
    "entries": {
      "serper-search": {
        "enabled": true,
        "config": {
          "apiKey": "your-api-key-here",
          "defaultNumResults": 5
        }
      }
    }
  }
}
```

## 使用方法

该插件会注册一个名为 `serper_search` 的工具，该工具接受三个参数：

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `query` | 字符串 | 必填 | 搜索查询内容 |
| `num` | 数字 | 5 | 结果数量（1-100） |
| `searchType` | 字符串 | "search" | 用于普通搜索；"news" 用于新闻搜索 |

### 普通搜索

> 输入 “best rust web frameworks 2026” 进行搜索

系统将返回包含标题、链接、摘要和排名信息的自然搜索结果，同时还会提供相关知识图谱和常见问题。

### 新闻搜索

> 输入 “AI regulation Europe” 进行搜索

系统将返回包含标题、链接、摘要、日期和来源的新闻文章。

## 插件结构

```
serper-search/
  clawdbot.plugin.json   # Plugin manifest with configSchema
  package.json            # NPM package config
  index.ts                # Plugin implementation
  SKILL.md                # This file
```

## 关键实现细节

- **导出函数**：`export default function register(api)` — 不是一个对象；
- **工具注册方式**：`api.registerTool TOOLObject)` — 直接注册，无需回调函数；
- **返回格式**：`{ content: [{ type: "text", text: JSON.stringify(results) }] }`；
- **依赖项**：从 Clawdbot 的 `node_modules` 中引入 `@sinclair/typebox` 库。

## 开发者

该插件由 [@Samoppakiks](https://github.com/Samoppakiks) 使用 Claude Code 开发。