# 竞争对手查找功能

## 目的  
通过使用 SerpAPI 在网络上搜索，为给定品牌识别出 3 至 5 个竞争对手；在必要时，会使用 OpenAI 进行补充查询。返回竞争对手的名称、网站信息，以及选择性地说明其被视为竞争对手的原因。该功能会将结果传递给营销审计流程，用于填充最终报告中的“竞争对手概况”部分。

## 输入数据结构  
```typescript
// Function signature
collectCompetitors(brandName: string, domain?: string): Promise<CompetitorData>

// brandName: The brand name to find competitors for (e.g. "Gymshark")
// domain: Optional domain for additional context (e.g. "gymshark.com").
// Helps refine competitor search and filter out the brand itself from results.
```

## 输出数据结构  
```typescript
interface CompetitorData {
 competitors: CompetitorEntry[]; // 3-5 competitor entries
 error?: string; // Present only when collector fails
}

interface CompetitorEntry {
 name: string; // e.g. "Nike"
 website: string; // e.g. "nike.com"
 reason?: string; // e.g. "Direct competitor in activewear market"
}
```

## 所依赖的 API  

### 主要依赖：SerpAPI  
- **API 名称：** SerpAPI（谷歌搜索服务）  
- **端点：** `https://serpapi.com/search.json`  
- **认证方式：** 使用 `SERPAPI_KEY` 环境变量  
- **费用估算：** 每次搜索约 0.005 美元  
- **请求限制：** 根据套餐不同而异；免费套餐每月允许 100 次搜索  

### 辅助依赖：DataForSEO  
- **API 名称：** DataForSEO 竞争对手域名 API  
- **端点：** `https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live`  
- **认证方式：** 使用 `DATAFORSEO_LOGIN` 和 `DATAFORSEO_PASSWORD` 环境变量  
- **费用估算：** 每次请求约 0.01 美元  
- **请求限制：** 根据套餐不同而异；免费套餐每月允许 100 次请求  

### 备用方案：OpenAI（简单查询）  
- **API 名称：** OpenAI API  
- **模型：** `gpt-4.1-mini`  
- **认证方式：** 使用 `OPENAI_API_KEY` 环境变量  
- **费用估算：** 每次查询约 0.001 美元  
- **使用场景：** 仅在 SerpAPI 和 DataForSEO 均失败或未返回结果时使用  

## 实现流程  

### 数据处理流程  
1. 从流程中接收 `brandName` 及可选的 `domain` 参数  
2. 尝试使用 SerpAPI 进行搜索  
3. 如果 SerpAPI 失败或返回的结果不足，尝试使用 DataForSEO  
4. 如果两种方法均失败，使用 OpenAI 进行简单查询  
5. 去重并过滤结果（排除品牌自身的信息）  
6. 返回 3 至 5 个竞争对手的信息（存储在 `CompetitorData` 对象中）  

### 方法 1：SerpAPI 搜索  
```typescript
// Query: "top competitors of {brandName}"
{
 api_key: process.env.SERPAPI_KEY,
 engine: "google",
 q: `top competitors of ${brandName}`,
 num: 10
}
```  
- 解析搜索结果，提取竞争对手的名称和域名  
- 寻找列表式文章（例如：“Gymshark 的前 10 个竞争对手...”）  
- 从结果链接中提取域名  
- 过滤掉非竞争对手的相关内容（如新闻文章或品牌自身的网站）  

### 方法 2：DataForSEO 竞争对手域名查询  
```typescript
[{
 target: domain, // e.g. "gymshark.com"
 language_code: "en",
 location_code: 2840, // United States
 limit: 5
}]
```  
- 返回与目标品牌竞争的域名  
- 该方法比 SerpAPI 更准确，但需要提供域名参数  

### 方法 3：OpenAI 备用查询（简单请求）  
```typescript
// ONLY used when Methods 1 and 2 both fail
// This is a MINIMAL prompt -- keep token usage as low as possible
const response = await openai.chat.completions.create({
 model: 'gpt-4.1-mini',
 max_tokens: 200,
 temperature: 0.3,
 messages: [
 {
 role: 'system',
 content: 'You are a marketing analyst. Return only a JSON array of competitor objects.'
 },
 {
 role: 'user',
 content: `List 5 direct competitors of "${brandName}"${domain ? ` (${domain})` : ''}. Return JSON: [{"name":"...","website":"...","reason":"..."}]`
 }
 ]
});
```  
- 解析 JSON 响应  
- 每次查询费用约为 0.001 美元，仅在 SerpAPI 和 DataForSEO 均无法使用时使用  
- 使用该方法时需记录警告信息，以便进行成本监控  

### 结果过滤  
- 删除名称或网站与输入品牌匹配的记录  
- 按网站域名进行去重（处理方式：去除 “www” 前缀及路径尾部的斜杠）  
- 确保每个记录都包含 `name` 和 `website` 两个字段  
- 最多返回 5 个结果；至少返回 3 个  

## 错误处理  
- 整个功能采用 `try/catch` 语句进行异常处理  
- 如果三种方法均失败，返回 `EMPTY_COMPETITOR_DATA` 对象，并设置 `error` 字段  
- 绝不抛出异常，始终返回有效的 `CompetitorData` 对象  
- 使用 Winston 日志记录错误信息，包括品牌名称和失败的方法名称  
- 在使用辅助/备用方法时记录警告信息  

### 常见错误场景：  
- SerpAPI 密钥无效或配额用尽  
- DataForSEO 的认证信息无效或余额不足  
- OpenAI API 密钥无效  
- 对于小众品牌或未知品牌，无法找到竞争对手  
- 任何 API 请求超时  

## 使用示例  
```typescript
import { collectCompetitors } from '../collectors/competitorCollector';

// Successful collection (via SerpAPI)
const data = await collectCompetitors('Gymshark', 'gymshark.com');
// Returns:
// {
// competitors: [
// { name: "Nike", website: "nike.com", reason: "Global leader in athletic apparel" },
// { name: "Lululemon", website: "lululemon.com", reason: "Premium activewear competitor" },
// { name: "Under Armour", website: "underarmour.com", reason: "Direct competitor in gym wear" },
// { name: "Alphalete", website: "alphalete.com", reason: "DTC fitness apparel brand" },
// { name: "Fabletics", website: "fabletics.com", reason: "Subscription-based activewear" },
// ],
// }

// Partial result (only OpenAI fallback worked)
const partial = await collectCompetitors('ObscureBrand');
// Returns:
// {
// competitors: [
// { name: "CompetitorA", website: "competitora.com", reason: "Similar product category" },
// { name: "CompetitorB", website: "competitorb.com", reason: "Same target market" },
// { name: "CompetitorC", website: "competitorc.com" },
// ],
// }

// Failed collection (graceful degradation)
const failedData = await collectCompetitors('UnknownBrand');
// Returns:
// {
// competitors: [],
// error: "Competitor data unavailable: All methods failed"
// }
```  

## 注意事项：  
- 该功能采用三层备用策略来确保数据的可用性。优先使用 SerpAPI（提供真实的搜索结果），其次使用 DataForSEO（根据关键词匹配筛选竞争对手），最后使用 OpenAI（作为备用方案）。  
- OpenAI 的使用仅限于 `reportGenerator.ts` 文件之外；请求长度应控制在 200 个字符以内，并需记录警告信息以监控成本。  
- 当输入类型为 `'instagram'`（无法获取域名）时，跳过方法 2（DataForSEO 需要域名参数），仅使用方法 1 和 3。  
- `EMPTY_COMPETITOR_DATA` 常量定义在 `src/types/audit.types.ts` 中，用于处理返回空结果的情况。  
- 竞争对手信息具有主观性；报告生成器（使用 GPT-4.1-mini 模型）会对原始列表进行进一步分析。  
- 该功能不能阻塞整个流程；即使完全失败，也应返回包含错误标志的有效数据。