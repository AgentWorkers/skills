# Instagram 数据采集器（Skill）

## 目的  
使用 Apify 的 Instagram 个人资料抓取工具，收集指定 Instagram 账号的详细信息。该工具可提取粉丝数量、互动指标、发布频率以及热门标签。收集到的数据会被导入到营销审计流程中，用于生成最终报告的 Instagram 绩效部分。

## 输入数据结构  
```typescript
// Function signature
collectInstagram(handle: string): Promise<InstagramData>

// The handle parameter is the Instagram username without the @ symbol.
// Example: "gymshark" (not "@gymshark")
```

## 输出数据结构  
```typescript
interface InstagramData {
 followers: number;
 posts: number;
 engagementRate: number; // Calculated: (avgLikes + avgComments) / followers * 100
 postingFrequency: string; // e.g. "1.2 posts/day", "3 posts/week", "unknown"
 avgLikes: number;
 avgComments: number;
 topHashtags: string[]; // Up to 10 most-used hashtags from recent posts
 error?: string; // Present only when collector fails
}
```

## 所依赖的 API  
- **API 名称：** Apify Instagram 个人资料抓取工具  
- **Actor ID：** `apify~instagram-profile-scraper`  
- **端点：** `https://api.apify.com/v2/acts/apify~instagram-profile-scraper/runs`  
- **认证方式：** 使用环境变量 `APIFY_API_TOKEN`  
- **费用估算：** 在 Apify 的免费/付费计划中，每次运行费用约为 0.005 美元  
- **速率限制：** 取决于 Apify 的使用计划；免费计划允许的并发运行次数有限  

## 实现模式  

### 数据流  
1. 从流程中接收 `handle` 字符串（即 Instagram 账号）。  
2. 调用 `apifyService.scrapeInstagramProfile(handle)` 来启动 Apify 的相关操作。  
3. Apify 以异步方式执行任务；系统会定期检查任务是否完成（超时时间为 60 秒）。  
4. 任务完成后，获取 Apify 返回的数据集结果。  
5. 将原始数据转换为 `InstagramData` 数据结构。  

### 互动率计算  
```typescript
engagementRate = ((avgLikes + avgComments) / followers) * 100;
```  
- 如果 `followers` 的值为 0，则将 `engagementRate` 设置为 0，以避免除以零的错误。  
- 互动率以百分比表示（例如：3.5% 表示每天的互动次数为 3.5 次）。  

### 发布频率计算  
- 分析 Apify 返回的最近 30 条帖子的时间戳。  
- 计算这些帖子之间的时间间隔。  
- 将帖子数量除以该时间间隔内的天数，结果以易于阅读的格式显示：  
  - 每天至少发布 1 条帖子：`"X.X 条帖子/天"`  
  - 每周至少发布 1 条帖子：`"X 条帖子/周"`  
  - 每月发布少于 1 条帖子：`"X 条帖子/月"`  
  - 如果没有时间戳数据：`"未知"`  

### 热门标签提取  
- 遍历最近帖子的标题（caption），使用正则表达式 `/#(\w+)/g` 提取所有标签。  
- 统计每个标签的出现频率，并返回出现频率最高的 10 个标签。  

### Apify 响应数据映射  
Apify 返回的原始数据中的关键字段：  
- `followersCount` -> 对应 `followers`  
- `postsCount` -> 对应 `posts`  
- `latestPosts[].likesCount` -> 用于计算 `avgLikes`  
- `latestPosts[].commentsCount` -> 用于计算 `avgComments`  
- `latestPosts[].caption` -> 用于提取标签  
- `latestPosts[].timestamp` -> 用于计算发布频率  

## 错误处理  
- 整个函数被包裹在 `try/catch` 块中。  
- 在发生错误时，返回一个包含错误信息的 `EMPTY_INSTAGRAM_DATA` 对象：  
```typescript
 return { ...EMPTY_INSTAGRAM_DATA, error: 'Instagram data unavailable: <reason>' };
 ```  
- 绝不抛出异常，始终返回一个有效的 `InstagramData` 对象。  
- 使用 Winston 日志库记录错误信息，包括账号信息和错误详情：  
```typescript
 logger.error('Instagram collector failed', { handle, err });
 ```  
- 常见错误情况：  
  - Apify 的 API 令牌无效或已过期  
  - 任务超时（账号信息量过大或 Apify 系统过载）  
  - 账号设置为私密状态或不存在  
  - 超过了 Apify 的速率限制  

## 使用示例  
```typescript
import { collectInstagram } from '../collectors/instagramCollector';

// Successful collection
const data = await collectInstagram('gymshark');
// Returns:
// {
// followers: 6800000,
// posts: 4520,
// engagementRate: 1.85,
// postingFrequency: "1.3 posts/day",
// avgLikes: 120000,
// avgComments: 5800,
// topHashtags: ["gymshark", "fitness", "gym", "workout", "fitnessmotivation", ...],
// }

// Failed collection (graceful degradation)
const failedData = await collectInstagram('nonexistent_handle_12345');
// Returns:
// {
// followers: 0,
// posts: 0,
// engagementRate: 0,
// postingFrequency: "unknown",
// avgLikes: 0,
// avgComments: 0,
// topHashtags: [],
// error: "Instagram data unavailable: Profile not found"
// }
```  

## 注意事项  
- 该数据采集器依赖于 `apifyService.ts` 来处理与 API 的通信。它仅负责数据映射和计算工作。  
- Apify 的任务是异步执行的；系统会定期检查任务进度。如果任务在 60 秒内未完成，则视为超时错误。  
- 该数据采集器可以独立进行测试；在测试中，可以通过模拟 `apifyService.scrapeInstagramProfile` 来返回预设数据。  
- Instagram 数据可能存在延迟（因为 Apify 抓取的是公开数据，这些数据可能已被缓存），但这对于审计目的来说是可接受的。  
- `EMPTY_INSTAGRAM_DATA` 常量定义在 `src/types/audit.types.ts` 中，需要导入以便在返回空数据时使用。  
- 该数据采集器绝不能阻塞整个流程；即使任务失败，也应返回包含错误信息的有效数据，以便其他数据采集器能够继续执行。