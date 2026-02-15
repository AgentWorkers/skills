---
name: youtube-analytics
description: "YouTube Data API v3 分析工具包：用于分析 YouTube 频道、视频和搜索结果。适用于以下场景：查看 YouTube 频道统计数据、分析视频表现、比较不同频道、搜索视频、获取订阅者数量、查看用户互动数据、查找热门视频、获取频道上传内容，以及分析 YouTube 上的竞争情况。使用该工具包需要从 Google Cloud Console 获取 YouTube Data API v3 的密钥。"
---

# YouTube 分析工具包

## 设置

安装依赖项：

```bash
cd scripts && npm install
```

通过在项目根目录下创建一个 `.env` 文件来配置凭据：

```
YOUTUBE_API_KEY=AIzaSy...your-api-key
YOUTUBE_DEFAULT_MAX_RESULTS=50
```

**先决条件**：需要一个已启用 YouTube Data API v3 的 Google Cloud 项目。请从 [Google Cloud 控制台](https://console.cloud.google.com/apis/credentials) 获取您的 API 密钥。

## 快速入门

| 用户操作 | 要调用的函数 |
|-----------|-----------------|
| “分析这个 YouTube 频道” | `analyzeChannel(channelId)` |
| “比较这两个频道” | `compareChannels([id1, id2])` |
| “这个视频的表现如何？” | `analyzeVideo(videoId)` |
| “在 YouTube 上搜索 [主题]” | `searchAndAnalyze(query)` |
| “获取这个频道的统计数据” | `getChannelStats(channelId)` |
| “获取这个视频的观看次数” | `getVideoStats(videoId)` |
| “查找关于 [主题] 的频道” | `searchChannels(query)` |
| “显示这个频道的最新上传内容” | `getChannelVideos(channelId)` |

通过导入 `scripts/src/index.ts` 来执行这些函数：

```typescript
import { analyzeChannel, searchAndAnalyze } from './scripts/src/index.js';

const analysis = await analyzeChannel('UCxxxxxxxx');
```

或者直接使用 tsx 运行：

```bash
npx tsx scripts/src/index.ts
```

## 工作流程模式

每次分析都遵循三个阶段：

### 1. 分析
调用 API 函数。每次调用都会访问 YouTube Data API 并返回结构化数据。

### 2. 自动保存
所有结果会自动保存为 JSON 文件，文件路径为 `results/{category}/`。文件命名规则如下：
- 有名称的结果文件：`{sanitized_name}.json`
- 自动生成的文件：`YYYYMMDD_HHMMSS__{operation}.json`

### 3. 总结
分析完成后，读取保存的 JSON 文件，并在 `results/summaries/` 目录下生成一个 Markdown 总结文件，其中包含数据表、对比结果和洞察。

## 高级函数

| 函数 | 功能 | 收集的数据 |
|----------|---------|----------------|
| `analyzeChannel(channelId)` | 完整的频道分析 | 频道信息、最新视频、每视频的平均观看次数 |
| `compareChannels(channelIds)` | 比较多个频道 | 订阅者数量、观看次数、视频数量 |
| `analyzeVideo(videoId)` | 视频性能分析 | 观看次数、点赞数、评论数、点赞率、评论率 |
| `searchAndAnalyze(query, maxResults?)` | 搜索 + 统计 | 带有完整视频统计信息的搜索结果 |

## 单个 API 函数

如需更细粒度的控制，可以从相应的 API 模块中导入特定函数。请参阅 [references/api-reference.md](references/api-reference.md)，以获取包含参数、类型和示例的 13 个 API 函数的完整列表。

### 频道相关函数

| 函数 | 功能 |
|----------|---------|
| `getChannel(channelId)` | 获取完整的频道详情 |
| `getChannelStats(channelId)` | 获取简化后的统计数据（订阅者数量、观看次数、视频数量） |
| `getMultipleChannels(channelIds)` | 批量获取多个频道的信息 |

### 视频相关函数

| 函数 | 功能 |
|----------|---------|
| `getVideo(videoId)` | 获取完整的视频详情 |
| `getVideoStats(videoId)` | 获取简化后的统计数据（观看次数、点赞数、评论数） |
| `getMultipleVideos(videoIds)` | 批量获取多个视频的信息 |
| `getChannelVideos(channelId)` | 获取某个频道的最新上传内容 |

### 搜索相关函数

| 函数 | 功能 |
|----------|---------|
| `searchVideos(query, options?)` | 搜索视频 |
| `searchChannels(query, options?)` | 搜索频道 |

## 结果存储

结果会自动保存到 `results/` 目录中，采用以下结构：

```
results/
├── channels/       # Channel data and comparisons
├── videos/         # Video data and analyses
├── search/         # Search results
└── summaries/      # Human-readable markdown summaries
```

### 管理结果

```typescript
import { listResults, loadResult, getLatestResult } from './scripts/src/index.js';

// List recent results
const files = listResults('channels', 10);

// Load a specific result
const data = loadResult(files[0]);

// Get most recent result for an operation
const latest = getLatestResult('channels', 'channel_analysis');
```

## 提示

1. **使用频道 ID** — 频道 ID 以 `UC` 开头（例如 `UCxxxxxxxx`）。您可以在频道 URL 或页面源代码中找到它们。
2. **请求总结** — 在获取数据后，请求包含表格和洞察的 Markdown 总结。
3. **比较频道** — 使用 `compareChannels()` 来对比不同频道的各项数据。
4. **批量请求** — 使用 `getMultipleChannels()` 或 `getMultipleVideos()` 进行高效的批量查询。
5. **搜索 + 分析** — `searchAndAnalyze()` 可以在一次调用中同时完成搜索和视频统计分析。