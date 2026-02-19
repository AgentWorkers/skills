---
name: media-news-digest
description: 生成媒体与娱乐行业的新闻摘要。涵盖好莱坞行业动态（如 THR、Deadline、Variety 等媒体报道）、票房数据、流媒体服务、颁奖季信息、电影节资讯以及电影制作相关新闻。数据收集渠道包括 RSS 源、Twitter/X 社交平台上的意见领袖（KOLs）、Reddit 网站以及网络搜索结果。采用基于管道（pipeline-based）的脚本处理方式，具备重试机制和去重功能。支持通过 Discord、电子邮件以及 Markdown 格式发送新闻摘要。
version: "1.7.1"
homepage: https://github.com/draco-agent/media-news-digest
source: https://github.com/draco-agent/media-news-digest
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    optionalBins: ["gog"]
    credentialAccess: >
      This skill does NOT read, store, or manage any platform credentials itself.
      Email delivery uses the external `gog` CLI (Google Workspace CLI) which manages
      its own OAuth tokens separately. Twitter and Brave API keys are passed via
      environment variables and used only for outbound API calls within fetch scripts.
      No credentials are written to disk by this skill.
env:
  - name: X_BEARER_TOKEN
    required: false
    description: Twitter/X API bearer token for KOL monitoring
  - name: BRAVE_API_KEY
    required: false
    description: Brave Search API key for web search layer
---
# 媒体新闻摘要系统

这是一个自动化的媒体与娱乐行业新闻摘要系统，涵盖好莱坞交易、票房数据、流媒体平台、颁奖季、电影节、制作动态以及行业合作信息。

## 快速入门

1. **生成新闻摘要**（统一处理流程——并行执行所有步骤）：
   ```bash
   python3 scripts/run-pipeline.py \
     --defaults <SKILL_DIR>/config/defaults \
     --hours 48 --freshness pd \
     --output /tmp/md-merged.json --verbose --force
   ```

2. **使用模板**：将处理后的内容应用到 Discord 或电子邮件模板中。

## 数据来源（共 44 个，其中 35 个已启用）

- **RSS 源（15 个）**：THR、Deadline、Variety、Screen Daily、IndieWire、The Wrap、Collider、Vulture、Awards Daily、Gold Derby、Screen Rant、Empire、The Playlist、Entertainment Weekly、/Film
- **Twitter/X 社交媒体意见领袖（13 个）**：@THR、@DEADLINE、@Variety、@FilmUpdates、@DiscussingFilm、@ScottFeinberg、@kristapley、@BoxOfficeMojo、@GiteshPandya、@MattBelloni、@Borys_Kit 等

## 主题分类（7 个部分）

- 🎟️ 票房 — 北美/全球票房、首映周末票房数据
- 📺 流媒体 — Netflix、Disney+、Apple TV+、HBO 的观众数据
- 🎬 制作 — 新项目、演员阵容、拍摄进展
- 🏆 颁奖 — 奥斯卡奖、金球奖、艾美奖、英国电影学院奖等相关活动
- 💰 合作与商业 — 并购、版权交易、人才签约、企业重组
- 🎪 电影节 — 戛纳电影节、威尼斯电影节、多伦多国际电影节、圣丹斯电影节、柏林电影节
- ⭐ 评论与反响 — 专业评论家的评价、RT/Metacritic 的评分

## 脚本处理流程

所有脚本均遵循以下技术架构：

1. `fetch-rss.py` — RSS 源数据抓取工具，支持重试和并行下载
2. `fetch-twitter.py` — 监控 Twitter/X 社交媒体意见领袖的动态（需要 `$X_BEARER_TOKEN`）
3. `fetch-web.py` — 通过 Brave API 或其他代理进行网页数据抓取
4. `merge-sources.py` — 数据质量评估与去重处理
5. `validate-config.py` — 配置文件验证工具

## Cron 任务集成

请参考 `references/digest-prompt.md` 了解如何配置 Cron 任务。更多详细信息请参阅 `digest-prompt.md`。

### 每日新闻摘要
```
读取 <SKILL_DIR>/references/digest-prompt.md，按照其中的完整流程生成日报。
- MODE = daily, FRESHNESS = pd, RSS_HOURS = 48
- DISCORD_CHANNEL_ID = <channel_id>
- EMAIL = <email>
- LANGUAGE = Chinese
```

### 每周新闻摘要
```
读取 <SKILL_DIR>/references/digest-prompt.md，按照其中的完整流程生成周报。
- MODE = weekly, FRESHNESS = pw, RSS_HOURS = 168
- DISCORD_CHANNEL_ID = <channel_id>
- EMAIL = <email>
- LANGUAGE = Chinese
```

## 所需依赖库

```bash
pip install -r requirements.txt
```

所有脚本仅支持 Python 3.8 及更高版本的标准库。推荐使用 `feedparser` 库，但非必需。