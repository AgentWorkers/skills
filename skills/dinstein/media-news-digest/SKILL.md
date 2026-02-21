---
name: media-news-digest
description: Generate media & entertainment industry news digests. Covers Hollywood trades (THR, Deadline, Variety), box office, streaming, awards season, film festivals, and production news. Four-layer data collection from RSS feeds, Twitter/X KOLs, Reddit, and web search. Pipeline-based scripts with retry mechanisms and deduplication. Supports Discord, email, and markdown templates.
version: "1.8.0"
homepage: https://github.com/draco-agent/media-news-digest
source: https://github.com/draco-agent/media-news-digest
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

这是一个自动化的媒体与娱乐行业新闻摘要系统，涵盖了好莱坞的交易动态、票房数据、流媒体平台、颁奖季、电影节、制作新闻以及行业内的各种合作与交易。

## 快速入门

1. **生成新闻摘要**（统一处理流程——同时并行执行所有步骤）：
   ```bash
   python3 scripts/run-pipeline.py \
     --defaults <SKILL_DIR>/config/defaults \
     --hours 48 --freshness pd \
     --output /tmp/md-merged.json --verbose --force
   ```

2. **使用模板**：将处理后的内容应用到 Discord 或电子邮件模板中。

## 数据来源（共 44 个，其中 35 个已启用）

- **RSS 源（15 个）**：THR、Deadline、Variety、Screen Daily、IndieWire、The Wrap、Collider、Vulture、Awards Daily、Gold Derby、Screen Rant、Empire、The Playlist、Entertainment Weekly、/Film
- **Twitter/X 社交媒体上的意见领袖（13 个）**：@THR、@DEADLINE、@Variety、@FilmUpdates、@DiscussingFilm、@ScottFeinberg、@kristapley、@BoxOfficeMojo、@GiteshPandya、@MattBelloni、@Borys_Kit 等

## 主要分类（7 个板块）

- 🎟️ 票房 — 美国/全球票房数据、新片首映周末票房
- 📺 流媒体 — Netflix、Disney+、Apple TV+、HBO 的观众数据
- 🎬 制作 — 新项目、演员选角、拍摄进展
- 🏆 颁奖 — 奥斯卡奖、金球奖、艾美奖、英国电影学院奖等相关活动
- 💰 合作与商业 — 并购、版权交易、人才签约、公司重组
- 🎪 电影节 — 戛纳电影节、威尼斯电影节、多伦多国际电影节、圣丹斯电影节、柏林电影节
- ⭐ 评论与反响 — 专业评论家的评价、RT/Metacritic 的评分

## 脚本处理流程

所有脚本均遵循以下技术架构进行开发：

1. `fetch-rss.py` — RSS 源数据获取工具，支持重试机制和并行下载
2. `fetch-twitter.py` — 监控 Twitter 和 X 社交媒体上的意见领袖动态（需要 `$X_BEARER_TOKEN`）
3. `fetch-web.py` — 通过 Brave API 或备用方式获取网页内容
4. `merge-sources.py` — 对数据源进行质量评估和去重处理
5. `validate-config.py` — 配置文件验证工具

## Cron 任务集成

有关 Cron 任务设置的详细信息，请参考 `references/digest-prompt.md` 文件。更多模板文档请查看 `digest-prompt.md`。

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

所有脚本仅支持 Python 3.8 及更高版本的标准库。建议使用 `feedparser` 库（虽然非强制要求）。