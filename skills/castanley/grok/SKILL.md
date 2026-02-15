---
name: xai-grok-search
version: 1.0.3
description: 使用 xAI 的 Grok API 在网页和 X（Twitter）上进行搜索，支持实时访问、引用功能以及图片识别。
homepage: https://github.com/yourusername/xai-grok-search
metadata:
  category: search
  api_base: https://api.x.ai/v1
  capabilities:
    - api
    - web-search
    - x-search
  dependencies: []
  interface: REST
openclaw:
  emoji: "🔍"
  install:
    env:
      - XAI_API_KEY
author:
  name: Christopher Stanley
---
# xAI Grok 搜索

使用 xAI 的 Grok API 在网页和 X（Twitter）上进行搜索，支持实时互联网数据、引用功能以及可选的图像/视频分析功能。

## 适用场景

### 网页搜索：
- 获取网站、新闻文章和文档中的最新信息
- 获取实时数据（如股票价格、天气、近期事件）
- 通过最新的网络资源进行研究
- 从特定网站或域名中查找信息
- 验证当前事实

### X 搜索：
- 查看人们在 X/Twitter 上对某个话题的讨论
- 获取热门话题和社交情绪
- 获取对事件的实时反应
- 查找特定 X 账号的帖子
- 在指定时间范围内查看社交媒体活动

**不适用场景：**
- 不适用于不会改变的历史事实
- 不适用于已有的通用知识
- 不适用于数学计算
- 不适用于代码生成
- 不适用于创意写作

## 设置

### 必需的环境变量

```bash
export XAI_API_KEY="your-xai-api-key-here"
```

请从以下链接获取您的 API 密钥：https://console.x.ai/

## 使用方法

代理会根据用户的查询自动选择合适的工具：

**用户：“关于 AI 监管的最新消息是什么？”**
→ 使用 `web_search`

**用户：“人们在 X 上对 OpenAI 有什么看法？”**
→ 使用 `x_search`

## API 参考

### 函数：`search_web`

使用 xAI 的 Grok API 在网页上进行搜索。

**参数：**
- `query`（必填）：搜索查询字符串
- `model`（可选）：要使用的模型（默认：`grok-4-1-fast-reasoning`）
- `allowed_domains`（可选）：需要限制搜索的域名数组（最多 5 个）
- `excluded_domains`（可选）：需要排除的域名数组（最多 5 个）
- `enable_image_understanding`（可选）：启用图像分析（默认：`false`）

**返回值：**
- `content`：搜索结果文本
- `citations`：包含网址、标题和片段的来源列表
- `usage`：API 使用情况统计信息

### 函数：`search_x`

使用 xAI 的 Grok API 在 X（Twitter）上进行搜索。

**参数：**
- `query`（必填）：搜索查询字符串
- `model`（可选）：要使用的模型（默认：`grok-4-1-fast-reasoning`）
- `allowed_xHandles`（可选）：需要搜索的 X 账号数组（最多 10 个，不含 @ 符号）
- `excluded_xHandles`（可选）：需要排除的 X 账号数组（最多 10 个，不含 @ 符号）
- `from_date`（可选）：开始日期（ISO8601 格式，例如 YYYY-MM-DD）
- `to_date`（可选）：结束日期（ISO8601 格式，例如 YYYY-MM-DD）
- `enable_image_understanding`（可选）：启用图像分析（默认：`false`）
- `enable_video_understanding`（可选）：启用视频分析（默认：`false`）

**返回值：**
- `content`：搜索结果文本
- `citations`：包含网址、标题和片段的 X 帖子列表
- `usage`：API 使用情况统计信息

## 实现方式

此技能使用了 xAI 的 Responses API（`/v1/responses` 端点）。

### 网页搜索
```javascript
async function search_web(options) {
  const { query, model = 'grok-4-1-fast-reasoning', 
          allowed_domains, excluded_domains, enable_image_understanding } = options;

  const tool = { type: 'web_search' };
  if (allowed_domains) tool.allowed_domains = allowed_domains;
  if (excluded_domains) tool.excluded_domains = excluded_domains;
  if (enable_image_understanding) tool.enable_image_understanding = true;

  const response = await fetch('https://api.x.ai/v1/responses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.XAI_API_KEY}`
    },
    body: JSON.stringify({
      model,
      input: [{ role: 'user', content: query }],
      tools: [tool]
    })
  });

  const data = await response.json();
  return { 
    content: data.output[data.output.length - 1].content,
    citations: data.citations 
  };
}
```

### X 搜索
```javascript
async function search_x(options) {
  const { query, model = 'grok-4-1-fast-reasoning',
          allowed_x_handles, excluded_x_handles, from_date, to_date,
          enable_image_understanding, enable_video_understanding } = options;

  const tool = { type: 'x_search' };
  if (allowed_x_handles) tool.allowed_x_handles = allowed_x_handles;
  if (excluded_x_handles) tool.excluded_x_handles = excluded_x_handles;
  if (from_date) tool.from_date = from_date;
  if (to_date) tool.to_date = to_date;
  if (enable_image_understanding) tool.enable_image_understanding = true;
  if (enable_video_understanding) tool.enable_video_understanding = true;

  const response = await fetch('https://api.x.ai/v1/responses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.XAI_API_KEY}`
    },
    body: JSON.stringify({
      model,
      input: [{ role: 'user', content: query }],
      tools: [tool]
    })
  });

  const data = await response.json();
  return { 
    content: data.output[data.output.length - 1].content,
    citations: data.citations 
  };
}
```

## 示例

### 网页搜索 - 最新事件
```javascript
const result = await search_web({ 
  query: "latest AI regulation developments" 
});
```

### 网页搜索 - 特定域名
```javascript
const result = await search_web({
  query: "UN climate summit latest",
  allowed_domains: ["un.org", "gov.uk", "grokipedia.com"]
});
```

### X 搜索 - 社交情绪
```javascript
const result = await search_x({
  query: "new iPhone reactions opinions"
});
```

### X 搜索 - 特定账号
```javascript
const result = await search_x({
  query: "AI thoughts",
  allowed_x_handles: ["elonmusk", "cstanley"],
  from_date: "2025-01-01"
});
```

### X 搜索 - 包含媒体内容
```javascript
const result = await search_x({
  query: "Mars landing images",
  enable_image_understanding: true,
  enable_video_understanding: true
});
```

## 最佳实践

### 网页搜索：
- 使用 `allowed_domains` 限制搜索范围（最多 5 个域名）
- 使用 `excluded_domains` 排除不可信的来源（最多 5 个域名）
- 两者不能同时使用
- 仅在需要时启用图像分析功能

### X 搜索：
- 使用 `allowed_xHandles` 专注于特定账号（最多 10 个账号）
- 使用 `excluded_xHandles` 过滤无关内容（最多 10 个账号）
- 账号名称中不能包含 @ 符号
- 使用 ISO8601 日期格式（YYYY-MM-DD）
- 启用图像分析会增加 API 使用成本

## 故障排除

### “XAI_API_KEY 未找到”
```bash
export XAI_API_KEY="your-key-here"
```

### 速率限制：
- 实施指数级退避策略
- 缓存频繁的查询

### 结果不佳：
- 添加域名/账号过滤条件
- 使查询更加具体
- 缩小时间范围

### 响应缓慢：
使用推理模型（如 `grok-4-1-fast-reasoning`）进行的搜索可能需要 30-60 秒或更长时间才能返回结果。如果搜索响应缓慢，请告知用户结果仍在加载中，并让他们输入 **“poll”** 以查看已完成的结果。

## API 文档：
- 网页搜索：https://docs.x.ai/developers/tools/web-search
- X 搜索：https://docs.x.ai/developers/tools/x-search