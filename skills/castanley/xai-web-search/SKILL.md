---
name: xai-web-search
version: 1.0.0
description: 使用 xAI 的 Grok 在互联网上执行搜索，支持实时数据获取、引用功能，并可选地具备图像识别能力。
homepage: https://github.com/yourusername/xai-web-search
metadata:
  category: search
  api_base: https://api.x.ai/v1
  capabilities:
    - api
    - web-search
  dependencies: []
  interface: REST
  openclaw:
    emoji: "🔍"
    install:
      env:
        - XAI_API_KEY
author:
  name: Your Name
  colony: yourcolony
license: MIT
---

# xAI 网页搜索

使用 xAI 的 Grok API 进行网页搜索，支持实时互联网访问、引用功能以及可选的图像识别功能。

## 适用场景

当用户需要以下操作时，可以使用此技能：
- 搜索超出您知识范围的当前信息
- 获取实时数据（新闻、股票价格、天气、最新事件）
- 查找最新进展或突发新闻
- 验证当前事实或状态
- 通过最新来源研究主题

**不适用场景：**
- 不会改变的历史事实
- 您已经掌握的通用知识
- 数学计算
- 代码生成任务
- 创意写作

## 设置

### 必需的环境变量

```bash
export XAI_API_KEY="your-xai-api-key-here"
```

请从以下链接获取您的 API 密钥：https://console.x.ai/

### 安装

```bash
# Install via ClawHub CLI
openclaw skill install xai-web-search

# Or manually clone
git clone https://github.com/yourusername/xai-web-search.git ~/.openclaw/skills/xai-web-search
```

## 使用方法

### 基本搜索

当用户询问当前信息时：

**用户：**“关于 AI 监管的最新消息是什么？”

**您应该：**
1. 使用 `search_web` 函数并传入用户的查询内容
2. 返回包含引用的搜索结果
3. 在结果末尾列出信息来源

### 带有域名过滤的功能

仅搜索可信来源：

**用户：**“查找关于 `async/await` 的最新 Python 文档”

**您应该：**
1. 使用 `search_web` 并设置 `allowed_domains` 为 `["docs.python.org", "python.org"]`
2. 这将确保仅使用官方文档

### 带有图像识别的功能

当视觉内容很重要时：

**用户：**“展示新款特斯拉汽车的外观”

**您应该：**
1. 使用 `search_web` 并设置 `enable_image_understanding` 为 `true`
2. Grok 会分析搜索过程中找到的图像
3. 在响应中描述图像的视觉细节

## API 参考

### 函数：`search_web`

使用 xAI 的 Grok API 进行网页搜索。

**参数：**
- `query`（必填）：搜索查询字符串
- `model`（可选）：要使用的模型（默认：`grok-4-1-fast-reasoning`）
- `allowed_domains`（可选）：限制搜索的域名数组（最多 5 个）
- `excluded_domains`（可选）：需要排除的域名数组（最多 5 个）
- `enable_image_understanding`（可选）：启用图像分析（默认：`false`）
- `stream`（可选）：是否以流的形式返回结果（默认：`false`）

**返回值：**
- `content`：搜索结果文本
- `citations`：包含网址、标题和片段的信息来源数组
- `usage`：API 使用统计信息

**示例：**

```javascript
const result = await search_web({
  query: "Latest developments in quantum computing",
  allowed_domains: ["nature.com", "science.org"],
  enable_image_understanding: false
});

console.log(result.content);
result.citations.forEach(cite => {
  console.log(`Source: ${cite.title} - ${cite.url}`);
});
```

## 实现方式

此技能通过 HTTP 请求直接调用 xAI 的 `responses` API：

```javascript
async function search_web(options) {
  const {
    query,
    model = 'grok-4-1-fast-reasoning',
    allowed_domains = null,
    excluded_domains = null,
    enable_image_understanding = false
  } = options;

  // Build tool - exactly like the official curl example
  const tool = { type: 'web_search' };
  
  // Add optional parameters directly to the tool object
  if (allowed_domains) tool.allowed_domains = allowed_domains;
  if (excluded_domains) tool.excluded_domains = excluded_domains;
  if (enable_image_understanding) tool.enable_image_understanding = true;

  // Make API request - matches official curl example
  const response = await fetch('https://api.x.ai/v1/responses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.XAI_API_KEY}`
    },
    body: JSON.stringify({
      model,
      input: [
        {
          role: 'user',
          content: query
        }
      ],
      tools: [tool]
    })
  });

  const data = await response.json();
  const output = data.output || [];
  const lastMessage = output[output.length - 1] || {};

  return {
    content: lastMessage.content,
    citations: data.citations || []
  };
}
```

**重要提示：**
- 使用 `/v1/responses` 端点（而非 `/v1/chat/completions`）
- 使用 `input` 数组（而非 `messages` 数组）
- 工具类型为 `"web_search"`
- 可选参数直接传递给工具对象

## 示例

### 示例 1：当前事件

**用户：**“AI 监管的最新进展是什么？”

**智能助手：**
```
Uses: search_web({ query: "latest AI regulation developments" })
Returns response with current information and sources
```

### 示例 2：使用可信来源进行事实核查

**用户：**“联合国气候峰会发生了什么？仅使用可靠的新闻来源。”

**智能助手：**
```
Uses: search_web({
  query: "UN climate summit latest",
  allowed_domains: ["reuters.com", "apnews.com", "bbc.com"]
})
```

### 示例 3：技术文档查询

**用户：**“如何在 JavaScript 中使用 `async/await`？”

**智能助手：**
```
Uses: search_web({
  query: "JavaScript async await documentation",
  allowed_domains: ["developer.mozilla.org", "javascript.info"]
})
```

### 示例 4：视觉内容分析

**用户：**“极简主义建筑是什么样的？”

**智能助手：**
```
Uses: search_web({
  query: "brutalist architecture examples",
  enable_image_understanding: true
})
Analyzes architectural images to describe the style
```

## 结果展示格式

在展示搜索结果时：
1. **先给出答案**——不要以“根据我的搜索……”开头
2. **包含响应中的关键信息**
3. **在结果末尾以清晰的格式列出信息来源**

## 最佳实践

### 域名过滤
- 在高信任场景（医疗、金融、法律等领域）使用 `allowed_domains`
- 仅在已知存在问题的来源上谨慎使用 `excluded_domains`
- 两种过滤器不能同时使用
- 每个过滤器最多支持 5 个域名

### 图像识别
- 仅在相关视觉内容存在时启用
- 会增加延迟和 API 使用成本
- 适用于产品、地点、图表、信息图等的搜索
- 在 `server_side_tool_usage сервер_side_tool_view_image` 中记录使用情况

### 模型选择
- `grok-4-1-fast-reasoning`：最适合需要推理的搜索场景
- `grok-beta`：通用型模型，支持网页搜索
- `grok-2-1212`：生产级标准模型

### 错误处理
- 确保 `XAI_API_KEY` 已正确设置
- 采用指数退避策略处理请求速率限制
- 在解析 JSON 之前检查响应是否成功
- 提供优雅的错误处理方式

## 故障排除

### “未找到 XAI_API_KEY”
请设置您的 API 密钥：
```bash
export XAI_API_KEY="your-key-here"
```

### 请求速率限制
- 如果达到请求速率限制：
  - 采用指数退避策略
  - 缓存频繁的请求
 - 对于简单查询使用更快速的模型

### 结果质量不佳
- 通过添加域名过滤器来选择更可靠的来源
- 使查询更加具体
- 对于复杂主题尝试使用推理模型
- 对于需要视觉辅助的内容启用图像识别功能

## 安全注意事项
- 不要硬编码 API 密钥
- 将 `XAI_API_KEY` 存储在环境变量中
- 在搜索前验证用户输入的查询内容
- 在显示结果前对数据进行清洗
- 监控 API 使用情况和成本

## API 文档

完整的 xAI API 文档请参阅：https://docs.x.ai/developers/tools/web-search

## 许可证

MIT 许可证——详情请参见 LICENSE 文件

## 贡献方式

欢迎贡献！请在 GitHub 上提交问题或 Pull Request。

## 更新记录

### 1.0.0（2026-02-14）
- 首次发布
- 基本网页搜索功能
- 域名过滤支持
- 图像识别功能
- 引用处理
- 流式结果输出支持