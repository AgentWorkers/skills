---
name: sentiment-radar
description: "多平台情感监测与分析工具，适用于产品/品牌/话题的分析。该工具可从中文平台（如小红书，通过MediaCrawler收集数据）和英文平台（如Twitter、Reddit，通过Xpoz MCP收集数据），生成结构化的情感分析报告。报告内容包括产品提及情况、价格投诉、对比分析以及可操作的洞察结果。适用场景包括：  
(1) 监测竞争对手的市场情绪；  
(2) 跟踪产品发布的市场反响；  
(3) 分析用户在社交媒体上的反馈与痛点；  
(4) 制作市场情报报告。"
---
# 情感雷达（Sentiment Radar）

一个跨平台的社交媒体情感收集与分析工具。

## 支持的平台

| 平台 | 方法 | 是否需要认证 |
|---|---|---|
| 小红书 (XHS) | MediaCrawler（通过CDP浏览器） | 需扫描二维码登录 |
| Twitter | Xpoz MCP (`xpoz.getTwitterPostsByKeywords`) | 需OAuth令牌 |
| Reddit | Xpoz MCP (`xpoz.getRedditPostsByKeywords`) | 需OAuth令牌 |

## 先决条件

### MediaCrawler（用于小红书）
如果尚未安装：
```bash
git clone https://github.com/NanmiCoder/MediaCrawler ~/.openclaw/workspace/skills/media-crawler
cd ~/.openclaw/workspace/skills/media-crawler
uv sync
playwright install chromium
```
配置文件：`config/base_config.py` — 设置 `ENABLE_CDP_MODE = True`，`SAVE_DATA_OPTION = "json"` 

### Xpoz MCP（用于Twitter/Reddit）
需要安装并配置了Xpoz OAuth的mcporter工具。令牌文件位于 `~/.mcporter/xpoz/tokens.json`。

## 工作流程

### 第1步：定义目标
确定要分析的产品/品牌，并搜索相关关键词。示例：
```
Products: Plaud录音笔, 钉钉闪记, 飞书录音豆
Keywords (XHS): Plaud录音笔,钉钉闪记,飞书妙记,AI录音笔评测,录音豆
Keywords (Twitter): Plaud NotePin, DingTalk recorder, Lark voice
```

### 第2步：收集数据

#### 小红书数据收集
使用MediaCrawler和关键词进行搜索。请使用CDP模式（通过用户的Chrome浏览器）以避免被检测到。
爬虫需要扫描二维码进行登录——使用 `exec(background=true)` 在后台运行。

```bash
cd skills/media-crawler
# Update keywords in config/base_config.py, then:
.venv/bin/python main.py --platform xhs --lt qrcode
```

macOS环境下的配置调整：
```bash
export MPLBACKEND=Agg
export PATH="/usr/sbin:$PATH"
```

数据输出文件：`data/xhs/json/search_contents_YYYY-MM-DD.json` 和 `search_comments_YYYY-MM-DD.json`

#### Twitter/Reddit数据收集
直接使用Xpoz MCP工具：
- `xpoz.getTwitterPostsByKeywords` — 返回带有互动数据的帖子
- `xpoz.getRedditPostsByKeywords` — 返回带有评论的帖子

### 第3步：分析数据
对收集到的数据运行分析脚本：
```bash
python3 scripts/analyze.py \
  --data ./data \
  --products '{"Plaud": ["plaud","notepin"], "钉钉": ["钉钉","dingtalk","闪记"]}' \
  --output report.md
```

脚本执行以下操作：
- 关键词分布分析（每个关键词的提及次数、总点赞数/收藏数）
- 评论中产品的提及频率
- 情感分类（正面/负面/中性）
- 按互动量排名的高热度帖子
- 提取关于价格/订阅的投诉信息
- 提取产品比较相关的评论

### 第4步：生成报告
分析结果输出方式：
1. 以JSON格式输出到标准输出（供程序化使用）
2. 以Markdown格式生成报告并保存到指定路径

可以将小红书和Twitter的数据合并成一份综合报告。具体报告结构请参考 `references/report-template.md`。

## 主要分析维度

1. **情感分布** — 正面情感、负面情感与中性情感的比例
2. **产品提及情况** — 哪些产品被讨论得最多
3. **价格相关投诉** — 用户对价格的看法（如订阅疲劳、价值感知）
4. **产品比较评论** — 用户之间的对比意见
5. **用户痛点** — 用户的需求、投诉及未满足的需求
6. **互动指标** — 点赞数、收藏数、分享数等作为 popularity 的衡量标准

## 注意事项：

- 小红书的数据使用中文数字格式（例如“1.1万”）——`analyze.py` 中的 `parse_count()` 函数会处理这种格式。
- MediaCrawler在每次请求之间会暂停2秒以避免被限制访问频率。
- 每页返回约20条相关内容（可通过MediaCrawler配置进行调整）。
- 评论会自动随帖子一起被获取。
- 对于持续监控，可以使用cron任务定期执行脚本，并与之前的报告进行对比分析。