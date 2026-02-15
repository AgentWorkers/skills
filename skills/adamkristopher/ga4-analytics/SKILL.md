---
name: ga4-analytics
description: "Google Analytics 4、Search Console 以及索引管理 API 工具包。这些工具可用于分析网站流量、页面性能、用户统计数据、实时访客信息、搜索查询以及 SEO 指标。当用户需要以下功能时，可以使用这些工具：查看网站流量、分析页面浏览量、了解流量来源、查看用户统计数据、获取实时访客数据、检查 Search Console 的搜索记录、分析 SEO 表现、请求 URL 重新索引、检查索引状态、比较不同时间段的流量数据、查看跳出率、查看转化数据或获取电子商务收入。使用这些工具前，需要拥有具备 Google Analytics 4 和 Search Console 访问权限的 Google Cloud 服务账户。"
---

# GA4 分析工具包

## 设置

安装依赖项：

```bash
cd scripts && npm install
```

通过在项目根目录下创建一个 `.env` 文件来配置凭据：

```
GA4_PROPERTY_ID=123456789
GA4_CLIENT_EMAIL=service-account@project.iam.gserviceaccount.com
GA4_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
SEARCH_CONSOLE_SITE_URL=https://your-domain.com
GA4_DEFAULT_DATE_RANGE=30d
```

**前提条件**：需要一个已启用 Analytics Data API、Search Console API 和 Indexing API 的 Google Cloud 项目。同时，需要一个具有访问您的 GA4 账户和 Search Console 权限的服务账户。

## 快速入门

| 用户请求 | 调用的函数 |
|-----------|-----------------|
| “显示过去 30 天的网站流量” | `siteOverview("30d")` |
| “我的热门搜索查询是什么？” | `searchConsoleOverview("30d")` |
| “当前有哪些用户访问网站？” | `liveSnapshot()` |
| “重新索引这些 URL” | `reindexUrls(["https://example.com/page1", ...])` |
| “比较本月和上月的数据” | `compareDateRanges({startDate: "30daysAgo", endDate: "today"}, {startDate: "60daysAgo", endDate: "31daysAgo"})` |
| “哪些页面的流量最多？” | `contentPerformance("30d")` |

通过导入 `scripts/src/index.ts` 文件来执行这些函数：

```typescript
import { siteOverview, searchConsoleOverview } from './scripts/src/index.js';

const overview = await siteOverview('30d');
```

或者直接使用 tsx 运行：

```bash
npx tsx scripts/src/index.ts
```

## 工作流程模式

每次分析都遵循三个阶段：

### 1. 分析
调用 API 函数。每次调用都会与 Google API 进行交互并返回结构化数据。

### 2. 自动保存
所有结果会自动保存为带有时间戳的 JSON 文件，文件保存在 `results/{category}/` 目录下。文件命名格式为：`YYYYMMDD_HHMMSS__operation__extra_info.json`

### 3. 总结
分析完成后，读取保存的 JSON 文件，并在 `results/summaries/` 目录下生成一个包含数据表、趋势和推荐的 markdown 总结报告。

## 高级功能

### GA4 分析

| 函数 | 功能 | 收集的数据 |
|----------|---------|----------------|
| `siteOverview(dateRange?)` | 全面网站概览 | 页面浏览量、流量来源、用户统计、事件记录 |
| `trafficAnalysis(dateRange?)` | 流量详细分析 | 来源、按来源/媒介划分的会话数、新用户与回访用户 |
| `contentPerformance(dateRange?)` | 页面性能分析 | 最热门页面、着陆页、退出页 |
| `userBehavior(dateRange?)` | 用户行为分析 | 用户统计、事件记录、每日参与度指标 |
| `compareDateRanges(range1, range2)` | 时期对比 | 两个日期范围的指标对比 |
| `liveSnapshot()` | 实时数据 | 当前活跃用户、当前页面、当前事件 |

### Search Console

| 函数 | 功能 | 收集的数据 |
|----------|---------|----------------|
| `searchConsoleOverview(dateRange?)` | SEO 概览 | 热门搜索词、页面、设备类型、国家分布 |
| `keywordAnalysis(dateRange?)` | 关键词分析 | 带设备类型的搜索词统计 |
| `seoPagePerformance(dateRange?)` | 页面 SEO 指标 | 点击量最高的页面、国家分布 |

### 索引

| 函数 | 功能 |
|----------|---------|
| `reindexUrls(urls)` | 请求对多个 URL 重新进行索引 |
| `checkIndexStatus(urls)` | 检查 URL 是否已索引 |

### 实用工具

| 函数 | 功能 |
|----------|---------|
| `getAvailableFields()` | 列出所有可用的 GA4 维度和指标 |

### 单个 API 函数

如需更细粒度的控制，可以从相应的 API 模块中导入特定函数。请参阅 [references/api-reference.md](references/api-reference.md)，以获取包含参数、类型和示例的 30 多个 API 函数的完整列表。

## 日期范围

所有函数都支持灵活的日期范围格式：

| 格式 | 例子 | 说明 |
|--------|---------|-------------|
| 简写格式 | `"7d"`、`"30d"`、`"90d"` | 从几天前到今天 |
| 明确格式 | `{startDate: "2024-01-01", endDate: "2024-01-31"}` | 具体日期 |
| GA4 相对格式 | `{startDate: "30daysAgo", endDate: "today"}` | GA4 相对日期格式 |

默认日期范围为 `"30d"`（可通过 `.env` 文件中的 `GA4_DEFAULT_DATE_RANGE` 配置）。

## 结果存储

结果会自动保存到 `results/` 目录中，采用以下结构：

```
results/
├── reports/          # GA4 standard reports
├── realtime/         # Real-time snapshots
├── searchconsole/    # Search Console data
├── indexing/         # Indexing API results
└── summaries/        # Human-readable markdown summaries
```

### 结果管理

```typescript
import { listResults, loadResult, getLatestResult } from './scripts/src/index.js';

// List recent results
const files = listResults('reports', 10);

// Load a specific result
const data = loadResult(files[0]);

// Get most recent result for an operation
const latest = getLatestResult('reports', 'site_overview');
```

## 常见维度和指标

### 维度
`pagePath`、`pageTitle`、`sessionSource`、`sessionMedium`、`country`、`deviceCategory`、`browser`、`date`、`eventName`、`landingPage`、`newVsReturning`

### 指标
`screenPageViews`、`activeUsers`、`sessions`、`newUsers`、`bounceRate`、`averageSessionDuration`、`engagementRate`、`conversions`、`totalRevenue`、`eventCount`

## 提示

1. **指定日期范围** — 使用 “过去 7 天” 或 “过去 90 天” 可以获得与默认的 30 天不同的分析结果。
2. **请求总结报告** — 获取数据后，可以请求包含表格和洞察的 markdown 总结报告。
3. **比较时期** — 使用 `compareDateRanges()` 来对比不同时期的数据趋势。
4. **查看实时数据** — `liveSnapshot()` 可以显示当前访问网站的用户情况。
5. **结合使用 GA4 和 Search Console** — 结合流量数据和搜索查询数据可以获得更全面的分析结果。