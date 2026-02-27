---
name: pain-point-finder
description: 使用 PullPush API，您可以在 Reddit 上发现用户的痛点、不满情绪以及未被满足的需求。无需使用 API 密钥。该工具可以帮助您找到那些基于真实用户反馈的创业点子。
  Discover pain points, frustrations, and unmet needs on Reddit using PullPush API.
  No API keys required. Use to find startup ideas backed by real user complaints.
metadata: {"clawdbot":{"emoji":"🔬","requires":{"bins":["node"]}}}
---
# 痛点发现工具

该工具用于在 Reddit 上发现经过验证的痛点，包括用户的困扰、投诉以及未满足的需求。它通过分析评论帖子来识别用户的一致性意见及现有解决方案的不足之处。该工具由 PullPush API 提供支持，无需使用 API 密钥。

## 工作流程

请按照以下 4 个阶段依次操作，每个阶段都基于前一个阶段的结果进行进一步分析。

### 第 1 阶段：查找相关子版块

根据用户所处的领域，找到合适的子版块。

```bash
node {baseDir}/scripts/pain-points.mjs discover --domain "<user's domain>" --limit 8
```

示例：
```bash
node {baseDir}/scripts/pain-points.mjs discover --domain "project management" --limit 8
```

从搜索结果中选取排名前 3-5 个子版块，用于第 2 阶段的分析。

### 第 2 阶段：扫描痛点

在找到的子版块中进行广泛搜索。

```bash
node {baseDir}/scripts/pain-points.mjs scan \
  --subreddits "<sub1>,<sub2>,<sub3>" \
  --domain "<domain>" \
  --days 90 \
  --limit 20
```

示例：
```bash
node {baseDir}/scripts/pain-points.mjs scan \
  --subreddits "projectmanagement,SaaS,smallbusiness" \
  --domain "project management" \
  --days 90 \
  --limit 20
```

查看评分较高的帖子。`painScore` 和 `num_comments` 值都较高的帖子是进一步分析的理想对象。

### 第 3 阶段：深入分析

分析排名靠前的帖子的评论内容，以判断用户的一致性意见及现有解决方案的不足之处。

**单个帖子分析：**
```bash
node {baseDir}/scripts/pain-points.mjs deep-dive --post <post_id>
```

**扫描结果中的前 N 条帖子：**
```bash
node {baseDir}/scripts/pain-points.mjs deep-dive --from-scan <scan_output.json> --top 5
```

请注意 `validationStrength` 字段的含义：
- **strong**：痛点被广泛认可（`agreementRatio` > 0.20，且有 10 条以上用户表示认同）
- **moderate**：痛点较为明显，但认可度有限
- **weak**：仅有部分用户表达类似意见
- **anecdotal**：仅是某个人的投诉，需要更多证据支持

### 第 4 阶段：制定解决方案

对于每个经过验证的痛点，需提交一份结构化的提案，内容包括：
1. **问题描述**：用一句话概括该痛点
2. **证据**：相关帖子的引用内容、用户认同的数量以及所属子版块
3. **受影响群体**：受该问题影响的人群或行业类型
4. **现有解决方案及不足**：用户尝试过的解决方法及其失败原因
5. **竞争格局**：相关工具的列表
6. **市场机会**：现有解决方案中存在的不足之处
7. **产品/服务构想**：简要说明你的解决方案方案
8. **验证程度**：根据 `validationStrength` 的评分（strong/moderate/weak）及数据支持情况

## 参数参考

### discover 参数
| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `--domain` | 必填 | 需要搜索的领域 |
| `--limit` | 10 | 返回的子版块数量上限 |

### scan 参数
| 参数 | 默认值 | 说明 |
| `--subreddits` | 必填 | 以逗号分隔的子版块列表 |
| `--domain` | 可选 | 用于进一步搜索的特定领域 |
| `--days` | 365 | 搜索时间范围（天） |
| `--minScore` | 1 | 帖子评分最低阈值 |
| `--minComments` | 3 | 评论数量最低阈值 |
| `--limit` | 30 | 返回的帖子数量上限 |
| `--pages` | 2 | 每次查询显示的页面数（页数越多，搜索越深入，但速度越慢） |

### deep-dive 参数
| 参数 | 默认值 | 说明 |
| `--post` | 可选 | 单个帖子的 ID 或 Reddit URL |
| `--from-scan` | 可选 | 扫描结果的 JSON 文件路径 |
| `--stdin` | 可选 | 从标准输入（stdin）读取扫描结果 JSON |
| `--top` | 10 | 分析的帖子数量 |
| `--maxComments` | 200 | 每条帖子允许获取的最大评论数 |

## 速率限制

该脚本的请求频率限制为：每秒 1 次、每分钟 30 次、每次运行最多 300 次请求。如果 PullPush API 响应缓慢或出现错误，系统会采用指数级退避策略进行重试。所有操作进度会记录到标准错误输出（stderr）中。

## 使用建议：
- 先使用 `--days 90` 进行广泛搜索，再缩小范围至 `--days 30` 以获取最新趋势
- `num_comments` 和 `score` 值都较高的帖子代表被广泛认可的痛点
- `painScore` 高但 `num_comments` 较低的帖子属于小众痛点，值得深入研究
- `mentionedTools` 参数可帮助了解市场竞争情况
- `validationStrength` 为 **strong** 的帖子是最适合开发的创业项目目标