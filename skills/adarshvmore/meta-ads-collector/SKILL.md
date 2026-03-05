# Meta Ads Collector 能力

## 目的
扫描 Meta Ad Library API，以查找指定品牌的活跃广告。提取活跃广告的数量、使用的广告格式、广告类型以及广告的最长运行时间。该收集器将数据传递给营销审计流程，用于填充最终报告中的“付费广告策略”部分。

## 输入数据结构
```typescript
// Function signature
collectMetaAds(brandName: string, domain?: string): Promise<MetaAdsData>

// brandName: The brand name to search for in the Ad Library (e.g. "Gymshark")
// domain: Optional domain to refine search (e.g. "gymshark.com"). Used to filter
// results and improve relevance when the brand name is ambiguous.
```

## 输出数据结构
```typescript
interface MetaAdsData {
 activeAds: number; // Total count of currently active ads
 formatsUsed: string[]; // e.g. ["image", "video", "carousel"]
 longestRunningAdDays: number; // Days the longest-running active ad has been live
 adTypes: string[]; // e.g. ["POLITICAL_AND_ISSUE_ADS", "HOUSING_ADS", "OTHER"]
 estimatedSpend?: string; // e.g. "$10,000 - $50,000" (if available from API)
 error?: string; // Present only when collector fails
}
```

## API 依赖项
- **API 名称：** Meta Ad Library API
- **端点：** `https://graph.facebook.com/v19.0/ads_archive`
- **认证：** `META_ACCESS_TOKEN` 环境变量（需要一个具有 Ad Library API 访问权限的 Facebook 应用）
- **其他环境变量：** `META_APP_ID`、`META_APP_SECRET`（如需生成令牌时使用）
- **费用估算：** 免费（无请求费用）
- **速率限制：** 遵循 Meta 的标准 Graph API 速率限制（约 200 次调用/小时）

## 实现模式

### 数据流
1. 从流程中接收 `brandName` 和可选的 `domain`
2. 调用 `metaAdsService.getMetaAds(brandName, domain)` 来查询 Ad Library API
3. 处理返回的广告数组以提取指标
4. 将处理后的数据映射到 `MetaAdsData` 接口中

### API 查询参数
```typescript
{
 access_token: process.env.META_ACCESS_TOKEN,
 search_terms: brandName,
 ad_reached_countries: "['US']", // Default to US; can be expanded
 ad_active_status: "ACTIVE", // Only fetch currently active ads
 ad_type: "ALL", // Include all ad types
 fields: "id,ad_creation_time,ad_creative_bodies,ad_creative_link_captions,ad_creative_link_titles,ad_delivery_start_time,ad_snapshot_url,page_name",
 limit: 100 // Max results per page
}
```

### 指标计算

**活跃广告数量：**
- 计算 API 响应中返回的广告总数

**格式检测：**
- 分析 `ad_snapshot_url` 或创意字段以确定广告格式
- 类别：`"image"`、`"video"`、`"carousel"`、`"dynamic"`、`"collection"`
- 将结果去重并生成唯一列表

**最长运行时间的广告：**
```typescript
const now = new Date();
const longestRunningAdDays = Math.max(
 ...ads.map(ad => {
 const startDate = new Date(ad.ad_delivery_start_time);
 return Math.floor((now.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24));
 })
);
```

**广告类型：**
- 从响应中提取唯一的 `ad_type` 值
- 常见类型：`"POLITICAL_AND_ISSUE_ADS"`、`"HOUSING_ADS"`、`"CREDIT_ADS"`、`EMPLOYMENT_ADS"`、其他/未分类

**预估花费：**
- 仅适用于政治/议题广告（Meta 的要求）
- 对于其他广告类型，此字段将为 `undefined`
- 如果可用，格式化为范围字符串：`"$10,000 - $50,000"`

### 域名过滤
当提供 `domain` 时：
- 仅过滤出创意内容、链接标题或链接描述中包含该域名的广告
- 这有助于提高名称相似品牌的准确性

## 错误处理
- 整个函数使用 `try/catch` 语句进行异常处理
- 发生错误时，返回包含 `error` 字段的 `EMPTY_META_ADS_DATA` 对象：
```typescript
 return { ...EMPTY_META_ADS_DATA, error: 'Meta Ads data unavailable: <reason>' };
 ```
- 绝不抛出异常——始终返回有效的 `MetaAdsData` 对象
- 使用 Winston 日志记录器记录错误，包括 `brandName` 和错误详情：
```typescript
 logger.error('Meta Ads collector failed', { brandName, domain, err });
 ```
- 常见错误场景：
  - 访问令牌无效、过期或缺少 Ad Library 权限
  - 品牌名称未返回任何结果（不一定表示错误——返回空数据但不会设置错误标志）
  - 超过速率限制（Meta Graph API 的限制）
  - 网络超时

## 使用示例
```typescript
import { collectMetaAds } from '../collectors/metaAdsCollector';

// Successful collection
const data = await collectMetaAds('Gymshark', 'gymshark.com');
// Returns:
// {
// activeAds: 47,
// formatsUsed: ["image", "video", "carousel"],
// longestRunningAdDays: 182,
// adTypes: ["OTHER"],
// estimatedSpend: undefined,
// }

// No ads found (not an error)
const noAds = await collectMetaAds('TinyLocalShop');
// Returns:
// {
// activeAds: 0,
// formatsUsed: [],
// longestRunningAdDays: 0,
// adTypes: [],
// }

// Failed collection (graceful degradation)
const failedData = await collectMetaAds('Gymshark');
// Returns:
// {
// activeAds: 0,
// formatsUsed: [],
// longestRunningAdDays: 0,
// adTypes: [],
// error: "Meta Ads data unavailable: Access token expired"
// }
```

## 注意事项
- 该收集器依赖于 `metaAdsService.ts` 来进行实际的 API 通信。它仅负责数据聚合和指标计算。
- Meta Ad Library API 需要一个已注册并具有 Ad Library 访问权限的 Facebook 应用。该应用必须经过 Meta 的审核才能在生产环境中使用。
- API 仅返回公开可用的广告数据。根据 Meta 的透明度政策，花费数据仅适用于政治/议题广告。
- 没有活跃广告也是有效结果（小型或新品牌可能未投放 Meta 广告），应返回空数据且不设置错误标志。
- `EMPTY_META_ADS_DATA` 常量定义在 `src/types/audit.types.ts` 中，应在需要时导入以作为备用返回值。
- 该收集器绝不能阻塞整个流程。即使完全失败，也应返回包含错误标志的有效数据。
- 分页：Meta API 每页最多返回 100 条结果。对于广告数量较多的品牌，可能需要通过 `after` 游标进行分页。出于审计目的，第一页（100 条广告）已经足够。