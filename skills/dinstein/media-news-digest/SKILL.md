---
name: media-news-digest
description: 生成媒体与娱乐行业的新闻摘要。涵盖好莱坞行业动态（如 THR、Deadline、Variety 等媒体报道）、票房数据、流媒体服务、颁奖季信息、电影节资讯以及电影制作相关新闻。系统采用 RSS、Twitter、X（Facebook）和网络搜索作为信息来源，具备新闻质量评分、去重处理以及多格式输出功能。
version: "1.6.1"
env:
  - name: X_BEARER_TOKEN
    required: false
    description: Twitter/X API bearer token for KOL monitoring
  - name: BRAVE_API_KEY
    required: false
    description: Brave Search API key for web search layer
---
# 媒体新闻摘要系统

这是一个自动化的媒体与娱乐行业新闻摘要系统，涵盖了好莱坞的交易动态、票房数据、流媒体平台、颁奖季、电影节、制作新闻以及行业内的各种合作信息。

## 快速入门

1. **生成新闻摘要**：
   ```bash
   python3 scripts/fetch-rss.py --config workspace/config
   python3 scripts/fetch-twitter.py --config workspace/config
   python3 scripts/fetch-web.py --config workspace/config
   python3 scripts/merge-sources.py --rss rss.json --twitter twitter.json --web web.json
   ```

2. **使用模板**：可以将生成的摘要通过 Discord 或电子邮件模板进行发送。

## 数据来源（共28个）

- **RSS源（15个）**：THR、Deadline、Variety、Screen Daily、IndieWire、The Wrap、Collider、Vulture、Awards Daily、Gold Derby、Screen Rant、Empire、The Playlist、Entertainment Weekly、/Film
- **Twitter/X平台上的KOLs（13个）**：@THR、@DEADLINE、@Variety、@FilmUpdates、@DiscussingFilm、@ScottFeinberg、@kristapley、@BoxOfficeMojo、@GiteshPandya、@MattBelloni、@Borys_Kit 等

## 主要主题（7个部分）

- 🎟️ 票房 — 北美/全球票房数据、首映周末票房
- 📺 流媒体 — Netflix、Disney+、Apple TV+、HBO的观众数据
- 🎬 制作 — 新项目、演员阵容、拍摄进展
- 🏆 颁奖 — 奥斯卡奖、金球奖、艾美奖、英国电影学院奖（BAFTAs）及相关宣传活动
- 💰 合作与商业 — 并购、版权交易、人才签约、企业重组
- 🎪 电影节 — 戛纳电影节、威尼斯电影节、多伦多国际电影节（TIFF）、圣丹斯电影节、柏林电影节
- ⭐ 评论与反响 — 专业评论家的评价、RT/Metacritic网站上的评分

## 脚本流程

所有脚本均基于 `tech-news-digest` 架构设计：

1. `fetch-rss.py` — 用于获取RSS源数据的脚本，支持重试和并行下载
2. `fetch-twitter.py` — 监控Twitter和X平台上的KOLs发布的动态（需要 `$X_BEARER_TOKEN`）
3. `fetch-web.py` — 通过Brave API或备用方式获取网页内容
4. `merge-sources.py` — 对获取的数据进行质量评估和去重处理
5. `validate-config.py` — 验证配置文件的有效性

## Cron任务集成

有关Cron任务的配置信息，请参考 `references/digest-prompt.md` 文件。更多详细文档请查看 `digest-prompt.md`。

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

所有脚本仅支持Python 3.8及以上版本的标准库。建议使用 `feedparser` 库（虽然非必需）。