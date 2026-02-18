---
name: reddit-quote-carousel
description: >
  根据要求，以下是将 SKILL.md 文件中的内容翻译成中文（简体中文）的结果：
  **创建一个基于 Reddit 引用的热门景点列表的 Instagram 轮播图：**
  - **封面幻灯片**：采用“简洁”风格，标题为“目的地中的热门景点（Top Attractions in Destination）”。
  - **每个景点幻灯片**：采用“引用”（quote）风格，并展示一条真实的 Reddit 引用。
  - **触发条件**：当 Bernard 说出“reddit-quote”或请求创建一个包含 Reddit 引用的轮播图时，系统应执行相应的操作。
  请注意，由于原文件中包含具体的代码示例、命令和 URL（如 `___CODE_BLOCK_0___`），这些内容在翻译过程中保持不变。
---
# Reddit 引用轮播图

Instagram 轮播图：包含封面图片以及来自 Reddit 引用的内容，这些引用来自 `tabiji.ai` 的热门推荐列表。

## 触发条件

当输入 “reddit-quote” 时，使用此技能。

## 参数

- **destination**（必填）：城市/地区（例如：“巴塞罗那”）
- **category**（必填）：推荐内容的类别（例如：“便宜美食”、“隐藏的宝藏”、“约会夜店”）
- **popular_picks_url**（必填）：从 `tabiji.ai` 的热门推荐页面获取景点信息和 Reddit 引用的 URL
- **reddit_post_count**（可选）：分析的 Reddit 帖子数量（用于生成标题，例如：“150+ 帖子”）。如果可用，请从热门推荐页面获取该数据。

## 工作流程（包含 3 个子代理）

工作目录：`/tmp/ig-reddit-quote/`

### 子代理 1：抓取推荐内容并查找图片

1. 使用 `web_fetch` 获取热门推荐页面，获取以下信息：
   - 每个景点的名称
   - 每个景点的精彩 Reddit 引用（要求引用具体、生动且具有个人色彩，而非泛泛而谈的赞美）
   - 引用对应的 Reddit 子版块（例如：“r/london”、“r/AskLondon”）
   - 如果页面显示的话，获取总的 Reddit 帖子数量

2. 使用 `instagram-photo-find` 工作流程查找图片：
   - 为封面图片选择 1 张代表目的地的图片
   - 为每个景点选择 1 张图片（用于引用展示）
   - 对于每张图片，执行 `web_search` → 下载候选图片 → 使用 `vision-score` 算法筛选出最佳图片

3. 将结果写入 `/tmp/ig-reddit-quote/manifest.json` 文件：
```json
{
  "destination": "Barcelona",
  "category": "Cheap Eats",
  "reddit_post_count": 150,
  "cover_photo": "/tmp/ig-reddit-quote/cover-best.jpg",
  "slides": [
    {
      "name": "Bar Cañete",
      "quote": "Went here on a random Tuesday and had the best patatas bravas of my life. The old guy next to me ordered for me and everything was incredible.",
      "subreddit": "r/barcelona",
      "photo": "/tmp/ig-reddit-quote/bar-canete-best.jpg",
      "source_url": "instagram.com/p/XXX/"
    }
  ]
}
```

### 子代理 2：添加文字叠加层

读取 `manifest.json` 文件，并使用 `instagram-photo-text-overlay` 技能为图片添加文字叠加层。

**封面图片（第 1 张）**：采用简洁的文字样式：
```bash
python3 /Users/psy/.openclaw/workspace/skills/instagram-photo-text-overlay/scripts/overlay.py \
  --input /tmp/ig-reddit-quote/cover-best.jpg \
  --output /tmp/ig-reddit-quote/slide-1.jpg \
  --title "Top {COUNT} {CATEGORY} in {DESTINATION}" \
  --subtitle "Insider Takes from Reddit ({N}+ posts)" \
  --style clean --watermark "tabiji.ai"
```

其中：
- `{COUNT}`：景点数量
- `{CATEGORY}`：推荐类别
- `{DESTINATION}`：目的地名称
- `{N}`：`manifest.json` 中记录的 Reddit 帖子数量

**后续图片（第 2 张至第 N 张）**：采用引用展示的样式，每个景点对应一张图片：
```bash
python3 /Users/psy/.openclaw/workspace/skills/instagram-photo-text-overlay/scripts/overlay.py \
  --input /tmp/ig-reddit-quote/{slug}-best.jpg \
  --output /tmp/ig-reddit-quote/slide-{N}.jpg \
  --title "{ATTRACTION_NAME}" \
  --quote "{REDDIT_QUOTE}" \
  --author "{SUBREDDIT}" \
  --style quote --watermark "tabiji.ai"
```

最终输出文件路径：`/tmp/ig-reddit-quote/slide-{1-N}.jpg`

### 子代理 3：将图片发布到 Instagram

使用与 `create-instagram-carousel-post` 相同的流程：
1. 将图片存储在 `tabiji repo` 的 `img/instagram/` 目录中
2. 创建轮播图容器
3. 为轮播图添加标题
4. 发布轮播图
5. 清理存储的图片和临时文件

## 标题模板：
```
{flag_emoji} Top {COUNT} {CATEGORY} in {DESTINATION}

Real recommendations from {N}+ Reddit posts 🧵

📍 Swipe for the spots + what Redditors actually said:
1. {Attraction 1}
2. {Attraction 2}
...

Full list with maps, prices & more Reddit recs 👉 {POPULAR_PICKS_URL}

💬 {PROVOCATIVE_QUESTION — e.g. "What's the most overrated restaurant you've been to abroad?" or "Would you trust a stranger's Reddit rec over a Michelin star?"}

#{destination} #{category_tag} #redditfinds #traveltips #foodietravel #localfavorites #tabiji
```

## 提示：

- 选择具体且生动的引用：“这是我吃过的最好吃的薯条”比“这个地方很棒”更有吸引力
- 引用长度应控制在 120 个字符以内，以便在图片上显示得清晰
- 如果引用太长，可以适当截短，但保留核心内容
- 封面标题应采用列表式的格式，例如：“巴塞罗那的 7 大便宜美食”