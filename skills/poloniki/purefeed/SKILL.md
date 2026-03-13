---
name: purefeed
description: "使用人工智能（AI）技术监控 Twitter/X 的动态。能够对推文进行语义分析，管理信号检测器（signal detectors），生成听起来像人类撰写的推文，检查 AI 检测的准确性，并通过 Typefully 将内容发布或安排到 X（Twitter 的简称）上。适用于用户想要浏览自己的 Twitter 动态、查找特定主题的推文、设置内容监控、根据精选内容起草推文，或向 X/Twitter 发布内容的情况。**请注意：在没有 Purefeed 账户的情况下，不得仅用于一般的 Twitter 浏览功能。**"
user-invocable: true
allowed-tools: ["bash"]
metadata: {"openclaw":{"requires":{"bins":["curl"],"env":["PUREFEED_API_KEY"]},"primaryEnv":"PUREFEED_API_KEY","emoji":"📡"}}
---
# Purefeed

**API 基础地址：** `https://www.purefeed.ai/api/v1`  
**认证方式：** `Authorization: Bearer $PUREFEED_API_KEY`  

## 输出规则  

对于所有包含推文数据的响应，请遵循以下规则：  
1. 将所有屏幕名称格式化为可点击链接：`[@screen_name](https://x.com/screen_name)`。切勿直接输出 `@screen_name`。  
2. 将所有推文引用格式化为可点击链接：`[推文](https://x.com/screen_name/status/tweet_id)`。  
3. 在推文数量前添加眼睛表情符号（表示观看次数）：`👁 81K`。  
4. 默认按观看次数或互动次数降序显示推文，除非用户另有要求。  

**示例输出格式：**  
```
[@CryptoAyor](https://x.com/CryptoAyor) 👁 81K — detailed thread about $JELLY manipulation
```  

## 设置步骤  

1. 在 **purefeed.ai/profile** → **Public API Keys** → **Create Key** 中获取 API 密钥。  
2. 将密钥设置到系统中：`openclaw config set skills.purefeed.env.PUREFEED_API_KEY "pf_live_YOUR_KEY"`。  
3. 验证密钥是否有效：`curl -s https://www.purefeed.ai/api/v1/auth/me -H "Authorization: Bearer $PUREFEED_API_KEY"`。  

## 工具依赖项  
```
list styles ──→ styleId ──→ generate post
list signals ──→ signal_id ──→ get/update/delete signal, get signal matches
list folders ──→ folder_id ──→ get folder tweets
get feed / search / signal matches ──→ tweet_ids ──→ generate post / get signal insights
generate post ──→ draft text ──→ humanize post ──→ publish / schedule / draft / queue
```  

在生成推文之前，务必先列出可使用的写作风格（styles）；在调用特定功能之前，务必先列出可用的信号（signals）。  

## 如何按主题查找推文  

当用户询问“关于 X 有什么新内容？”或“查找关于 Y 的推文”时，请按照以下步骤操作：  

### 第一步：查找匹配的活跃信号  
```
GET /signals?search=TOPIC&active=true
```  
`search` 参数支持语义搜索或向量搜索。例如，`search=ai` 可用于查找与“人工智能”或“AI 研究”相关的推文。如果未输入搜索词，可以尝试使用更宽泛的关键词，或通过 `GET /signals?active=true` 查看所有活跃的信号。  

### 第二步：从该信号中获取推文数据  
```
GET /signals/{id}/matches?limit=20
```  
信号（signals）是主要的数据来源，其中包含由 AI 生成的分析结果（如情感分析、分类信息等）。请勿跳过这一步，直接进行推文搜索。  

### 第三步：仅在未找到匹配的信号时才使用推文搜索  
```
GET /feed?limit=20&search=TOPIC
POST /search → {"query": "topic description", "limit": 20}
```  

### 第四步：根据信号 ID 过滤推文（可选）  
```
GET /feed?signal_ids=236,237&limit=20
```  

## 工作流程  

### 查找并分享推文  
1. 使用上述方法查找推文。  
2. `GET /styles`：选择所需的写作风格。  
3. `POST /studio/generate`：根据推文 ID 和选定的写作风格生成推文内容。  
4. `POST /studio/humanize`：如果推文的 AI 检测得分（score）≤ 30，则直接使用原始推文内容；否则对推文进行重写。  
5. `POST /studio/publish`：将生成的推文发布到目标平台（如 X）。  

### 设置监控规则  
1. `POST /signals`：创建新的信号，设置名称、描述、标签、颜色、触发条件（cron）和时区（系统会自动激活该信号）。  
2. 等待最多 6 小时，直到信号开始生效。  
3. `GET /signals/{id}/matches`：查看搜索结果。  
4. `PUT /signals/{id}`：如果搜索结果中包含过多无关内容，可修改信号的描述。  

### 首次使用前的准备工作  
1. `GET /auth/me`：验证 API 密钥。  
2. `GET /styles`：缓存可用的写作风格信息。  
3. `GET /signals`：查看已创建的信号配置。  
4. `GET /folders`：查看用户收藏的文件夹。  

## 关键概念  

- **信号（Signal）**：一种用于检测推文内容的 AI 工具，具有名称和描述。当 `signals_subscriptions` 不为空时，该信号处于活跃状态；否则处于非活跃状态。创建信号时，请务必设置 `tags` 和 `color`；除非用户特别要求，否则不要设置 `include_keywords`（因为这些设置可能会限制搜索范围）。  
- **写作风格（Writing Style）**：用于生成推文的规则或模板。在生成推文之前，必须先通过 `GET /styles` 获取有效的 `styleId`。  
- **Typefully**：这是一个后端服务，用于推文的发布、调度、草稿保存等功能。如果系统未连接到 Typefully，需让用户在 Purefeed 设置中配置该服务。  

## 错误处理  
| 错误代码 | 处理方式 |  
|-------|-------------|  
| 401 Unauthorized | 告知用户在 **purefeed.ai/profile** 创建新的 API 密钥。  
| 429 Too Many Requests | 等待一段时间后重试，并检查 `Retry-After` 头部字段中的提示。  
| “未连接到 Typefully” | 告知用户在 Purefeed 设置中配置 Typefully 服务。  
| “未配置 LLM API 密钥” | 告知用户在 Studio 设置中添加 LLM API 密钥。  
| “未找到相应的写作风格” | 通过 `GET /styles` 获取有效的写作风格 ID。  
| “未找到相应的信号” | 通过 `GET /signals` 获取相应的信号 ID。  

## API 参考文档  
请参阅 `API_REFERENCE.md`，以获取完整的端点文档、参数说明、curl 示例以及响应格式信息。  

所有 API 请求的成功响应格式为：`{"data": ..., "error": null}`；失败响应格式为：`{"data": null, "error": {"message": "...", "code": "..."}`。流式 API 的响应内容为纯文本（`text/plain`）。  

### 端点概述  
| 方法      | 路径                | 功能                          |  
|---------|------------------|-----------------------------|  
| GET      | /auth/me            | 验证 API 密钥                    |  
| GET      | /feed                | 按信号相关性排序的推文列表            |  
| POST      | /search             | 对匹配的推文进行全文搜索                |  
| GET      | /feed/signals          | 对指定推文 ID 进行 AI 分析            |  
| GET      | /folders             | 查看用户收藏的文件夹                |  
| GET      | /folders/:id/tweets       | 查看文件夹中的推文                  |  
| GET      | /signals             | 查看所有可用的信号                  |  
| POST      | /signals             | 创建并自动激活新的信号                |  
| GET      | /signals/:id           | 查看信号详细信息                  |  
| PUT      | /signals/:id           | 更新信号的配置                    |  
| DELETE     | /signals/:id           | 删除信号（操作不可撤销）                |  
| GET      | /signals/:id/matches       | 查看与该信号匹配的推文                |  
| GET      | /styles             | 查看所有可用的写作风格                |  
| POST      | /studio/generate       | 生成推文或帖子（支持流式输出）          |  
| POST      | /studio/humanize       | 对推文内容进行 AI 检测并重写（支持流式输出）    |  
| POST      | /studio/publish        | 立即将推文发布到目标平台            |  
| POST      | /studio/schedule        | 安排推文的发布时间                |  
| POST      | /studio/draft         | 将推文保存为草稿                  |  
| POST      | /studio/queue          | 将推文添加到发布队列                |  

## 请求限制  
- 每个 API 密钥每分钟的请求次数限制为 60 次。  
- 流式 API 请求被视为 1 次有效请求。  
- 错误响应中会包含 `Retry-After` 头部字段，用于提示用户稍后重试。