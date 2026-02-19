---
name: serper
description: 使用 Serper.dev API 以编程方式搜索 Google。当您需要执行网络搜索、在线查找信息或研究主题时，可以使用该 API。它支持查询参数、结果限制以及地理/语言定位功能。
metadata:
  openclaw:
    requires:
      env:
        - name: SERPER_API_KEY
          description: Serper.dev API key for Google search
          required: true
---
# Serper.dev：通过 Serper.dev API 搜索 Google

通过 Serper.dev API 在 Google 上进行搜索。获取的搜索结果经过清洗和整理，无需进行网页抓取。

## 快速入门

需要设置 `SERPER_API_KEY` 环境变量。

```javascript
serper_search({
  q: "OpenClaw AI agent",
  num: 5,
  gl: "us",
  hl: "en"
})
```

## 参数

| 参数 | 是否必填 | 默认值 | 说明 |
|-------|----------|---------|-------------|
| `q` | 是 | — | 搜索查询 |
| `num` | 否 | 5 | 结果数量（1-100） |
| `gl` | 否 | — | 国家代码（us, uk, th） |
| `hl` | 否 | — | 语言代码（en, th） |

## 设置

1. 获取 API 密钥：https://serper.dev
2. 设置环境变量：`export SERPER_API_KEY=your_key`

## 工具位置

`tools/serper_search.js`