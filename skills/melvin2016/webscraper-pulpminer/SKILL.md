---
name: pulpminer
description: "使用人工智能将任何网页转换为结构化的 JSON 数据。可以抓取网站内容，将数据提取到自定义的 JSON 模式中，并通过编程方式调用已保存的 API。该技术适用于网页抓取、数据提取、内容监控、潜在客户生成、价格跟踪以及构建数据管道等场景。"
emoji: ⛏️
homepage: https://pulpminer.com
metadata: {"clawdbot":{"requires":{"env":["PULPMINER_API_KEY"]},"config":["pulpminer_api_key"]}}
---

# PulpMiner — 人工智能网页抓取与JSON API

PulpMiner能够利用人工智能将任何网页转换为结构化的JSON数据。您只需提供一个URL，可选地提供一个JSON模板，PulpMiner会抓取该网页内容，通过大型语言模型（LLM）进行处理，然后返回格式清晰的结构化数据。

## 认证

所有API调用都需要在请求头中包含`apikey`：

```
apikey: <PULPMINER_API_KEY>
```

您可以从https://pulpminer.com/api获取API密钥。如果没有密钥，请点击“Regenerate Key”进行生成。

## 核心工作流程

PulpMiner分为两个阶段：

1. **创建保存的API**：通过https://pulpminer.com/api的仪表板配置URL、抓取工具、LLM以及可选的JSON模板。
2. **调用保存的API**：使用您的API密钥通过外部端点获取结构化JSON数据。

## 调用保存的API

### 静态API（固定URL）

```bash
curl -X GET "https://api.pulpminer.com/external/<apiId>" \
  -H "apikey: <PULPMINER_API_KEY>"
```

返回从配置的网页中提取的JSON数据。

### 动态API（包含变量的URL）

对于使用模板URL保存的API（例如：`https://example.com/search?q={{query}}&page={{page}}`）：

```bash
curl -X POST "https://api.pulpminer.com/external/<apiId>" \
  -H "apikey: <PULPMINER_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"query": "javascript frameworks", "page": "1"}'
```

保存在URL中的`{{variable}}`占位符会被您提供的值替换。

## 响应格式

成功响应会返回如下格式的数据：

```json
{
  "data": { ... },
  "errors": null
}
```

错误响应会返回如下格式的数据：

```json
{
  "data": null,
  "errors": "Error message describing what went wrong"
}
```

## 缓存

- API响应默认会被缓存24小时。
- 如果缓存数据超过15分钟，PulpMiner会优先提供缓存版本，并在后台进行数据更新。
- 您可以在仪表板设置中针对每个API禁用缓存功能。

## 配置选项（在仪表板中设置）

在https://pulpminer.com/api创建保存的API时，您可以配置以下选项：

| 选项          | 描述                                      |
|----------------|-----------------------------------------|
| **URL**         | 需要抓取的网页地址                              |
| **JSON模板**       | 供LLM使用的JSON结构（示例：`{"name": "", "price": ""}`）         |
| **渲染JavaScript**   | 适用于单页应用程序（SPA）和JavaScript较多的页面（使用无头浏览器）     |
| **CSS选择器**       | 仅提取页面的特定部分（例如：`.product-list`, `#main-content`）     |
| **额外指令**       | 给AI的额外指示（例如：“仅提取价格高于50美元的项”）         |
| **动态URL**        | 在URL中使用`{{variable}}`语法支持变量                |
| **缓存**         | 开启/关闭响应缓存功能                         |

## 与Zapier集成

在Zapier工作流程中实现异步抓取时：

```bash
# Static API
curl -X POST "https://api.pulpminer.com/external/zapier/get/<apiId>" \
  -H "apikey: <PULPMINER_API_KEY>" \
  -d '{"callbackURL": "https://hooks.zapier.com/..."}'

# Dynamic API
curl -X POST "https://api.pulpminer.com/external/zapier/post/<apiId>" \
  -H "apikey: <PULPMINER_API_KEY>" \
  -d '{"callbackURL": "https://hooks.zapier.com/...", "query": "value"}'
```

系统会立即返回`201`状态码，并在抓取完成后将数据发送到回调URL。

## 与n8n集成

验证认证后，可以使用标准的`/external/<apiId>`端点来获取数据。

## 费用说明

- 每次API调用费用为0.25–0.4信用点（credits）。
- 如果需要渲染JavaScript，额外收取0.1信用点。
- 新用户可免费获得5个信用点。
- 更多信用点可在https://pulpminer.com/credits购买。

## 使用建议

- 使用CSS选择器来精确筛选抓取内容，提高抓取准确性。
- 提供JSON模板以确保输出数据结构的一致性和可预测性。
- 仅在必要时启用JavaScript渲染——静态页面抓取速度更快，且费用更低。
- 通过额外指令指导AI的行为（例如：“以ISO 8601格式返回日期”）。
- 对于监控场景，建议保持缓存功能开启以减少信用点消耗。
- 在保存API配置之前，先使用“playground”功能验证URL是否可抓取。
- 动态API适用于搜索页面、分页内容和参数化URL。

## 链接

- 官网：https://pulpminer.com
- API仪表板：https://pulpminer.com/api