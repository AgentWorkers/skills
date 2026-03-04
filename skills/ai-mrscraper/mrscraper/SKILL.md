---
name: mrscraper
description: 通过 MrScraper API，您可以运行基于人工智能的、无法被阻止的网络爬虫程序，利用自然语言处理技术进行数据提取。
tags: [scraping, data-extraction, web-crawling, stealth-browser, web-automation]

homepage: https://mrscraper.com/
vendor: MrScraper
support_email: support@mrscraper.com

required_env_vars: [MRSCRAPER_API_TOKEN]
primary_credential: MRSCRAPER_API_TOKEN

metadata: {"openclaw":{"requires":{"env":["MRSCRAPER_API_TOKEN"]},"primaryEnv":"MRSCRAPER_API_TOKEN"}}

network: {"allowed_hosts":["api.mrscraper.com","api.app.mrscraper.com","sync.scraper.mrscraper.com"]}
---
# MrScraper

通过MrScraper API，利用人工智能技术执行无法被屏蔽的网络爬取和数据提取操作，支持自然语言指令。

## 功能支持

- 通过反屏蔽工具（隐身浏览器 + IP轮换）打开被屏蔽的页面
- 根据自然语言指令启动AI爬虫
- 重新运行一个或多个URL的现有爬虫配置
- 执行基于手动工作流的重新爬取操作
- 获取分页结果以及按ID获取详细结果

该技能仅通过API提供，不依赖于任何捆绑的本地脚本。

## 基础URL

- 反屏蔽工具API：`https://api.mrscraper.com`
- 平台API：`https://api.app.mrscraper.com`

## 认证

### 反屏蔽工具API认证

在反屏蔽工具的API端点使用查询参数进行认证：

- `token=<MRSCRAPER_API_TOKEN>`

### 平台API认证

在平台API的端点使用基于头部的认证方式：

```http
x-api-token: <MRSCRAPER_API_TOKEN>
accept: application/json
content-type: application/json
```

### 如何获取`MRSCRAPER_API_TOKEN`？

API令牌允许您的应用程序安全地与MrScraper API进行交互，并重新运行在控制台中创建的爬虫。

请按照以下步骤操作：

1. 在右上角点击您的**用户资料**。
2. 选择**API Tokens**。
3. 点击**New Token**。
4. 输入一个**名称**并设置一个**过期日期**。
5. 点击**Create**。
6. 复制新的令牌，并将其安全地保存为`MRSCRAPER_API_TOKEN`。
7. 在请求中通过`x-api-token`头部使用该令牌。

安全规则：

- 严禁在客户端代码（浏览器/移动应用包）中暴露令牌。
- 将令牌存储在环境变量或服务器端的秘密管理器中。

来自认证文档的注意事项：

- 该API密钥适用于所有V3平台端点。
- 同一个密钥也可以用于`sync.scraper.mrscraper.com`上的端点。
- 如需访问其他主机的端点，请联系`support@mrscraper.com`。

## 安装和运行时

- 本技能文档不需要任何本地安装步骤。
- 不需要任何捆绑的`scripts/`文件。
- 所有请求都是直接发送到上述两个基础URL的HTTPS请求。

## 数据和范围

- 数据仅发送到`api.app.mrscraper.com`和`api.mrscraper.com`。
- 响应可能包含提取的页面内容和爬取元数据。
- 该技能不支持隐藏数据的持久化或后台任务。
- 严禁在日志、提交内容或输出中暴露令牌。

## 端点

### 1. 反屏蔽工具

- 方法：`GET`
- URL：`https://api.mrscraper.com`
- 认证：`token`查询参数

通过隐身浏览和IP轮换打开目标URL，然后返回HTML。当直接访问被验证码或反机器人保护机制阻止时，可以使用此方法。

#### 查询参数：

| 参数            | 类型      | 是否必填 | 默认值 | 描述                                      |
| ---------------- | --------- | -------- | ------- | --------------------------------------- |
| `token`          | `string`  | 是      | —       | 反屏蔽工具令牌（`MRSCRAPER_API_TOKEN`）                     |
| `url`            | `string`  | 是      | —       | URL编码的目标URL                               |
| `timeout`        | `number`  | 否       | 60      | 最大等待时间（例如120秒）                         |
| `geoCode`        | `string`  | 否       | 无       | 地理路由代码（例如`SG`）                             |
| `blockResources` | `boolean` | 否       | false   | 是否屏蔽非必要资源                             |

#### 请求示例：

```bash
curl --location 'https://api.mrscraper.com?token=<MRSCRAPER_API_TOKEN>&timeout=120&geoCode=SG&url=https%3A%2F%2Fwww.lazada.sg%2Fproducts%2Fpdp-i111650098-s23209659764.html&blockResources=false'
```

#### 响应示例：

```html
<!doctype html>
<html>
  <head>...</head>
  <body>...</body>
</html>
```

#### 注意：

- 为了获得可重复的行为，请使用明确的`geoCode`和合适的超时设置。
- 仅当需要会话特定内容时才传递cookies。

### 2. 创建AI爬虫

- 方法：`POST`
- 主机：`https://api.app.mrscraper.com`
- 路径：`/api/v1/scrapers-ai`
- 认证：`x-api-token`

根据自然语言指令创建一个新的AI爬虫任务。

#### 请求参数（对于`agent`：`general`或`agent`：`listing`）：

| 参数          | 类型     | 是否必填 | 默认值 | 描述                                                    |
| -------------- | -------- | -------- | -------- | ---------------------------------------------------------- |
| `url`          | string   | 是      | —        | 目标URL                                               |
| `message`      | string   | 是      | —        | 提取指令                                      |
| `agent`        | string   | 否       | general  | 用于爬取的AI代理类型：`general`、`listing`或`map`           |
| `proxyCountry` | string   | 否       | 无       | 用于基于代理的爬取的ISO国家代码                         |

#### 请求参数（对于`agent`：`map`）：

| 参数             | 类型     | 是否必填 | 默认值 | 描述                                                                                                   |
| ----------------- | -------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| `url`             | string | 是      | —         | 目标URL                                           |
| `agent`           | string | 否       | map       | 用于爬取的AI代理类型（在这种情况下为`map`）                         |
| `maxDepth`        | number | 否       | 2         | 从起始URL开始爬取链接的最大深度。<br>0 = 仅爬取起始URL，1 = 包括直接链接         |
| `maxPages`        | number | 否       | 50        | 爬取过程中允许的最大页面数                          |
| `limit`           | number | 否       | 1000      | 每页提取的最大数据记录数。达到此限制时停止爬取                   |
| `includePatterns` | string | 否       | ""        | 要包含的正则表达式模式（用`||`分隔）                         |
| `excludePatterns` | string | 否       | ""        | 要排除的正则表达式模式（用`||`分隔）                         |

#### 请求示例：

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-ai" \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "message": "Extract title, price, stocks, and rating",
    "agent": "general"
  }'
```

#### 响应示例：

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "createdAt": "2019-08-24T14:15:22Z",
  "createdById": "e13e432a-5323-4484-a91d-b5969bc564d9",
  "updatedAt": "2019-08-24T14:15:22Z",
  "updatedById": "d8bc6076-4141-4a88-80b9-0eb31643066f",
  "deletedAt": "2019-08-24T14:15:22Z",
  "deletedById": "8ef578ad-7f1e-4656-b48b-b1b4a9aaa1cb",
  "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
  "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
  "type": "AI",
  "url": "http://example.com",
  "status": "Finished",
  "error": "string",
  "tokenUsage": 0,
  "runtime": 0,
  "data": {}, // MAIN SCRAPED DATA
  "htmlPath": "string",
  "recordingPath": "string",
  "screenshotPath": "string",
  "dataPath": "string"
}
```

#### 注意：

- 请正确选择代理类型，因为每种代理类型适用于特定的使用场景。对于大多数标准的网络爬取任务，使用`general`代理类型。如果用户未指定代理类型，或者连接的LLM无法确定页面类型，也可以使用`general`代理。`map`代理类型主要用于爬取产品页面，但也能很好地处理其他类型的页面。如果用户确认给定的URL是列表页面，可以选择`listing`代理类型。对于`map`代理类型，可以使用特定的参数来配置爬取过程：
- `maxDepth`（较低值1-2适用于针对性爬取，推荐使用最大值3），
- `maxPages`（限制总页面数），
- `limit`（限制提取的总记录数），
- `includePatterns`/`excludePatterns`（用`||`分隔的正则表达式模式，用于指定要爬取或跳过的URL）。

### 3. 重新运行AI爬虫

- 方法：`POST`
- 主机：`https://api.app.mrscraper.com`
- 路径：`/api/v1/scrapers-ai-rerun`
- 认证：`x-api-token`

在新的URL上重新运行现有的AI爬虫配置。

#### 请求参数：

| 参数        | 类型     | 是否必填 | 默认值 | 描述                                  |
| ------------ | -------- | -------- | ------- | -------------------------------------------- |
| `scraperId`  | `string` | 是      | —       | 从创建的AI爬虫中获取的ID                         |
| `url`        | `string` | 是      | —       | 目标URL                                   |

#### `map`代理的可选请求参数：

| 参数             | 类型   | 是否必填 | 默认值 | 描述                                                               |
|-------------------|--------|----------|---------|---------------------------------------------------------------------------|
| `maxDepth`        | number | 否       | 2       | 爬取深度                                               |
| `maxPages`        | number | 否       | 50      | 最大爬取页面数                                      |
| `limit`           | number | 否       | 1000    | 结果限制                                               |
| `includePatterns` | string | 否       | ""      | 要包含的正则表达式模式（用`||`分隔）                         |
| `excludePatterns` | string | 否       | ``      | 要排除的正则表达式模式（用`||`分隔）                         |

#### 请求示例：

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-ai-rerun" \
  -H "accept: application/json" \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "url": "https://shopee.sg/"
  }'
```

#### 响应示例：

```json
{
  "message": "Successful operation!",
  "data": {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "createdAt": "2019-08-24T14:15:22Z",
    "createdById": "e13e432a-5323-4484-a91d-b5969bc564d9",
    "updatedAt": "2019-08-24T14:15:22Z",
    "updatedById": "d8bc6076-4141-4a88-80b9-0eb31643066f",
    "deletedAt": "2019-08-24T14:15:22Z",
    "deletedById": "8ef578ad-7f1e-4656-b48b-b1b4a9aaa1cb",
    "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "type": "Rerun-AI",
    "url": "http://example.com",
    "status": "Finished",
    "error": "string",
    "tokenUsage": 0,
    "runtime": 0,
    "data": {}, // MAIN SCRAPED DATA
    "htmlPath": "string",
    "recordingPath": "string",
    "screenshotPath": "string",
    "dataPath": "string",
    "htmlContent": "string"
  }
}
```

### 4. 批量重新运行AI爬虫

- 方法：`POST`
- 主机：`https://api.app.mrscraper.com`
- 路径：`/api/v1/scrapers-ai-rerun/bulk`
- 认证：`x-api-token`

在多个URL上运行一个爬虫配置。

#### 请求参数：

| 参数       | 类型            | 是否必填 | 默认值 | 描述                       |
| ----------- | --------------- | -------- | ------- | --------------------------------- |
| `scraperId` | `string`        | 是      | —       | 现有的AI爬虫配置ID                         |
| `urls`      | `array[string]` | 是      | —       | 要运行的目标URL列表                               |

#### 请求示例：

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-ai-rerun/bulk" \
  -H "x-api-token: " \
  -H "Content-Type: application/json" \
  -d '{
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "urls": [
      "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
      "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
      "https://books.toscrape.com/catalogue/soumission_998/index.html"
    ]
  }'
```

#### 响应示例：

```json
{
  "message": "Bulk rerun started successfully",
  "data": {
    "bulkResultId": "f89f8f58-3c9a-42e5-a72e-59fa6c389f09",
    "status": "Running",
    "totalUrls": 3
  }
}
```

### 5. 重新运行手动爬虫

- 方法：`POST`
- 主机：`https://api.app.mrscraper.com`
- 路径：`/api/v1/scrapers-manual-rerun`
- 认证：`x-api-token`

使用手动浏览器工作流重新执行爬取任务。

#### 创建手动爬虫

在调用手动重新运行端点之前，您需要从控制台中创建并保存一个手动爬虫。请按照以下步骤操作：

1. 打开`MrScraper`控制台，然后进入`Scraper`。
2. 点击`New Manual Scraper +`。
3. 输入目标URL。
4. 添加与您的网站行为相匹配的工作流步骤（例如`Input`、`Click`、`Delay`、`Extract`、`Inject JavaScript`）。
5. 如有需要，配置分页（使用`QueryPagination`、`DirectoryPagination`或`Next Page Link`等选项）。
6. 测试并保存爬虫，然后复制其`scraperId`以在API请求中使用。

#### 请求参数：

| 参数        | 类型           | 是否必填 | 默认值 | 描述                                                                                                      |
|--------------|----------------|----------|---------|------------------------------------------------------------------------------------------------------------------|
| `scraperId`  | `string`       | 是      | —       | 要重新运行的手动爬虫的ID                         |
| `url`        | `string`       | 是      | —       | 重新运行的目标URL                               |
| `workflow`   | `array<object>`| 否       | 无       | 允许覆盖保存的工作流步骤。默认使用创建时保存的工作流。           |

#### 请求示例：

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-manual-rerun" \
  -H "accept: application/json" \
  -H "x-api-token: " \
  -H "Content-Type: application/json" \
  -d '{
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "url": "https://books.toscrape.com/",
    "workflow": [
      {
        "type": "extract",
        "data": {
          "extraction_type": "text",
          "attribute": null,
          "name": "book",
          "selector": "h3 a"
        }
      }
    ],
    "record": false,
    "paginator": {
      "type": "query_pagination",
      "max_page": 1,
      "enabled": false
    }
  }'
```

#### 响应示例：

```json
{
  "message": "Successful operation!",
  "data": {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "createdAt": "2019-08-24T14:15:22Z",
    "createdById": "e13e432a-5323-4484-a91d-b5969bc564d9",
    "updatedAt": "2019-08-24T14:15:22Z",
    "updatedById": "d8bc6076-4141-4a88-80b9-0eb31643066f",
    "deletedAt": "2019-08-24T14:15:22Z",
    "deletedById": "8ef578ad-7f1e-4656-b48b-b1b4a9aaa1cb",
    "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "type": "Rerun-AI",
    "url": "http://example.com",
    "status": "Finished",
    "error": "string",
    "tokenUsage": 0,
    "runtime": 0,
    "data": {}, // MAIN SCRAPED DATA
    "htmlPath": "string",
    "recordingPath": "string",
    "screenshotPath": "string",
    "dataPath": "string",
    "htmlContent": "string"
  }
}
```

### 6. 批量重新运行手动爬虫

- 方法：`POST`
- 主机：`https://api.app.mrscraper.com`
- 路径：`/api/v1/scrapers-manual-rerun/bulk`
- 认证：`x-api-token`

在多个URL上运行一个爬虫配置。

#### 请求参数：

| 参数       | 类型            | 是否必填 | 默认值 | 描述                       |
| ----------- | --------------- | -------- | ------- | --------------------------------- |
| `scraperId` | `string`        | 是      | —       | 现有的手动爬虫配置ID                         |
| `urls`      | `array[string]` | 是      | —       | 要运行的目标URL列表                               |

#### 请求示例：

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-manual-rerun/bulk" \
  -H "x-api-token: " \
  -H "Content-Type: application/json" \
  -d '{
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "urls": [
      "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
      "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
      "https://books.toscrape.com/catalogue/soumission_998/index.html"
    ]
  }'
```

#### 响应示例：

```json
{
  "message": "Bulk rerun started successfully",
  "data": {
    "bulkResultId": "f89f8f58-3c9a-42e5-a72e-59fa6c389f09",
    "status": "Running",
    "totalUrls": 3
  }
}
```

### 7. 获取结果

- 方法：`GET`
- 主机：`https://api.app.mrscraper.com`
- 路径：`/api/v1/results`
- 认证：`x-api-token`

返回分页的爬取结果。

#### 查询参数：

| 参数             | 类型   | 是否必填 | 默认值 | 描述               |
| -------------------|--------|----------|-------------|---------------------------|
| `sortField`       | string | 是      | `updatedAt` | 排序字段                               |
| `sortOrder`       | string | 是      | `DESC`      | 排序方向                               |
| `page`            | number | 是      | 1           | 页码                                      |
| `pageSize`        | number | 是      | 10          | 每页显示的记录数                               |
| `search`          | string | 否       | 无       | 搜索关键词                               |
| `dateRangeColumn` | string | 否       | `createdAt` | 过滤日期字段                             |
| `startAt`         | string | 否       | 无       | 开始日期范围（ISO格式）                         |
| `endAt`           | string | 否       | 结束日期范围（ISO格式）                         |

#### 注意：

- `sortField`选项：`createdAt`、`updatedAt`、`id`、`type`、`url`、`status`、`tokenUsage`、`runtime`
- `sortOrder`选项：`ASC`、`DESC`
- `dateRangeColumn`选项：`createdAt`、`updatedAt`

#### 请求示例：

```bash
curl -X GET "https://api.app.mrscraper.com/api/v1/results?sortField=updatedAt&sortOrder=DESC&pageSize=10&page=1" \
  -H "accept: application/json" \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

#### 响应示例：

```json
{
  "message": "Successful fetch",
  "data": [
    {
      "createdAt": "2025-11-11T09:50:09.722Z",
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
      "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
      "type": "AI",
      "url": "http://example.com",
      "status": "Finished",
      "error": "string",
      "tokenUsage": 5,
      "runtime": 0,
      "data": "{ \"title\": \"Product A\", \"price\": \"$10\" }",
      "htmlPath": "string",
      "recordingPath": "string",
      "screenshotPath": "string",
      "dataPath": "string"
    }
  ],
  "meta": {
    "page": 1,
    "pageSize": 10,
    "total": 1,
    "totalPage": 1
  }
}
```

### 8. 按ID获取详细结果

- 方法：`GET`
- 主机：`https://api.app.mrscraper.com`
- 路径：`/api/v1/results/{id}`
- 认证：`x-api-token`

根据特定的结果ID返回一个详细的结果对象。

#### 请求参数：

| 参数 | 类型     | 是否必填 | 默认值 | 描述                                 |
| ----- | -------- | -------- | ------- | ----------- |
| `id`  | `string` | 是      | —       | 结果ID                                   |

#### 请求示例：

```bash
curl -X GET "https://api.app.mrscraper.com/api/v1/results/497f6eca-6276-4993-bfeb-53cbbbba6f08" \
  -H "accept: application/json" \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

#### 响应示例：

```json
{
  "message": "Successful fetch",
  "data": [
    {
      "createdAt": "2025-11-11T09:50:09.722Z",
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
      "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
      "type": "AI",
      "url": "http://example.com",
      "status": "Finished",
      "error": "string",
      "tokenUsage": 5,
      "runtime": 0,
      "data": "string",
      "htmlPath": "string",
      "recordingPath": "string",
      "screenshotPath": "string",
      "dataPath": "string"
    }
  ]
}
```

## 错误

标准平台API错误：

| 状态码 | 错误含义                                      |
| ------ | ---------------------------------------- |
| `400`  | 请求参数无效                              |
| `401`  | API令牌缺失或无效                         |
| `404`  | 未找到爬虫或结果                         |
| `429`  | 超过速率限制                               |
| `500`  | 内部爬虫错误                               |

错误格式：

```json
{
  "message": "string",
  "error": "string",
  "statusCode": "number"
}
```

## 操作规则

- 在每次调用之前验证必填字段。
- 对于大量结果集，使用分页功能。
- 对于`429`错误，采用指数级退避策略进行重试。
- 严禁在输出中暴露任何认证信息。