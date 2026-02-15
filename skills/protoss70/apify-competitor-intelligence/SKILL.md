---
name: apify-competitor-intelligence
description: 分析竞争对手在 Google Maps、Booking.com、Facebook、Instagram、YouTube 和 TikTok 上的策略、内容、定价、广告以及市场定位。
version: 1.0.1
source: https://github.com/apify/agent-skills
homepage: https://apify.com
metadata:
  openclaw:
    requires:
      env:
        - APIFY_TOKEN
      bins:
        - node
        - mcpc
    primaryEnv: APIFY_TOKEN
    install:
      - kind: node
        package: "@apify/mcpc"
        bins: [mcpc]
---

# 竞争对手分析

使用 Apify Actors 从多个平台提取数据，以分析竞争对手的信息。

## 先决条件

- 在 OpenClaw 设置中配置了 `APIFY_TOKEN`
- Node.js 20.6 或更高版本
- `mcpc` CLI（通过技能元数据自动安装）

## 输入数据清洗规则

在将任何值替换到 bash 命令中之前，请确保：
- **ACTOR_ID**：必须是技术名称（例如 `owner/actor-name`，由字母、数字、连字符和点组成）或原始 ID（恰好 17 个字母数字字符，例如 `oeiQgfg5fsmIJB7Cn`）。拒绝包含 shell 元字符（`; | & $ ` ( ) { } < > ! \n`）的值。
- **SEARCH_KEYWORDS**：仅允许纯文本单词。拒绝包含 shell 元字符的输入。
- **JSON_INPUT**：必须是有效的 JSON 格式，并且不能包含单引号（请使用转义的双引号）。在使用前请验证其结构。
- **输出文件名**：必须符合 `YYYY-MM-DD_descriptive-name.{csv,json}` 的格式。文件名中不能包含路径分隔符（`/`、`..`）或空格，也不能包含元字符。

## 工作流程

请复制此检查表并跟踪进度：

```
Task Progress:
- [ ] Step 1: Identify competitor analysis type (select Actor)
- [ ] Step 2: Fetch Actor schema via mcpc
- [ ] Step 3: Ask user preferences (format, filename)
- [ ] Step 4: Run the analysis script
- [ ] Step 5: Summarize findings
```

### 第一步：确定竞争对手分析类型

根据分析需求选择合适的 Actor：

| 用户需求 | Actor ID | 适用场景 |
|-----------|----------|----------|
| 竞争对手的业务数据 | `compass/crawler-google-places` | 地理位置分析 |
| 竞争对手联系方式获取 | `poidata/google-maps-email-extractor` | 电子邮件提取 |
| 功能基准测试 | `compass/google-maps-extractor` | 详细业务数据 |
| 竞争对手评论分析 | `compass/Google-Maps-Reviews-Scraper` | 评论对比 |
| 酒店竞争对手数据 | `voyager/booking-scraper` | 酒店性能分析 |
| 酒店评论对比 | `voyager/booking-reviews-scraper` | 评论分析 |
| 竞争对手广告策略 | `apify/facebook-ads-scraper` | 广告创意分析 |
| 竞争对手页面指标 | `apify/facebook-pages-scraper` | 页面性能分析 |
| 竞争对手内容分析 | `apify/facebook-posts-scraper` | 帖子策略分析 |
| 竞争对手视频内容分析 | `apify/facebook-reels-scraper` | 视频内容分析 |
| 竞争对手受众分析 | `apify/facebook-comments-scraper` | 评论情感分析 |
| 竞争对手活动监控 | `apify/facebook-events-scraper` | 活动跟踪 |
| 竞争对手受众重叠分析 | `apify/facebook-followers-following-scraper` | 关注者分析 |
| 竞争对手评论基准测试 | `apify/facebook-reviews-scraper` | 评论对比 |
| 竞争对手广告监控 | `apify/facebook-search-scraper` | 广告内容分析 |
| 竞争对手个人资料分析 | `apify/instagram-profile-scraper` | 个人资料分析 |
| 竞争对手内容监控 | `apify/instagram-post-scraper` | 帖子跟踪 |
| 竞争对手互动分析 | `apify/instagram-comment-scraper` | 互动分析 |
| 竞争对手视频内容分析 | `apify/instagram-reel-scraper` | 视频指标分析 |
| 竞争对手增长趋势分析 | `apify/instagram-followers-count-scraper` | 关注者增长分析 |
| 全面竞争对手数据 | `apify/instagram-scraper` | 全面分析 |
| 基于 API 的竞争对手分析 | `apify/instagram-api-scraper` | API 访问 |
| 竞争对手视频分析 | `streamers/youtube-scraper` | 视频指标分析 |
| 竞争对手情感分析 | `streamers/youtube-comments-scraper` | 评论情感分析 |
| 竞争对手频道分析 | `streamers/youtube-channel-scraper` | 频道分析 |
| TikTok 竞争对手分析 | `clockworks/tiktok-scraper` | TikTok 数据分析 |
| 竞争对手视频策略 | `clockworks/tiktok-video-scraper` | 视频策略分析 |
| TikTok 竞争对手个人资料 | `clockworks/tiktok-profile-scraper` | TikTok 个人资料分析 |

### 第二步：获取 Actor 的输入格式

使用 `mcpc` 动态获取 Actor 的输入格式和详细信息：

```bash
mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为选定的 Actor（例如 `compass/crawler-google-places`）。

这将返回：
- Actor 的描述和 README 文件
- 必需和可选的输入参数
- 可用的输出字段

### 第三步：询问用户偏好

在运行之前，请询问用户以下信息：
1. **输出格式**：
   - **快速响应**：在聊天中显示前几条结果（不保存文件）
   - **CSV**：包含所有字段的完整导出
   - **JSON**：以 JSON 格式完整导出
2. **结果数量**：根据使用场景的需求确定

### 第四步：运行脚本

**快速响应（在聊天中显示，不保存文件）：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT'
```

**CSV 格式输出：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT' \
  --output 'YYYY-MM-DD_OUTPUT_FILE.csv' \
  --format csv
```

**JSON 格式输出：**
```bash
node {baseDir}/reference/scripts/run_actor.js \
  --actor 'ACTOR_ID' \
  --input 'JSON_INPUT' \
  --output 'YYYY-MM-DD_OUTPUT_FILE.json' \
  --format json
```

### 第五步：总结分析结果

完成分析后，报告以下内容：
- 分析的竞争对手数量
- 文件的位置和名称
- 主要的竞争洞察
- 建议的下一步行动（进一步分析、基准测试等）

## 安全性与数据隐私

该技能指导代理选择一个 Apify Actor，通过 `mcpc` 获取其输入格式，并运行相应的抓取脚本。脚本仅与 `api.apify.com` 通信，并将输出结果写入当前工作目录下的文件；它不会访问无关的系统文件或其他环境变量。

Apify Actors 仅抓取公开可用的数据，不会收集目标平台上公开可见之外的私人或个人身份信息。为确保额外的安全性，您可以通过查询 `https://api.apify.com/v2/acts/:actorId` 来检查 Actor 的权限级别：`LIMITED_PERMISSIONS` 表示在受限的沙箱环境中运行，而 `FULL_PERMISSIONS` 表示具有更广泛的系统访问权限。有关详细信息，请参阅 [Apify 的通用条款和条件](https://docs.apify.com/legal/general-terms-and-conditions)。

## 错误处理

- **APIFY_TOKEN 未找到**：请用户在 OpenClaw 设置中配置 `APIFY_TOKEN`。
- **mcpc 未找到**：运行 `npm install -g @apify/mcpc`。
- **Actor 未找到**：检查 Actor ID 的拼写是否正确。
- **运行失败**：请用户查看错误输出中的 Apify 控制台链接。
- **超时**：减小输入数据量或增加 `--timeout` 参数的值。