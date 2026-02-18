---
name: reddit-quote-topaz
description: >
  **任务描述：**  
  根据提供的 `SKILL.md` 文件内容，需要创建一个 Instagram 卡片轮播（carousel），该轮播包含来自 Reddit 的热门引文（quotes），并使用 Topaz 图像处理技术对图片进行 2 倍放大处理。轮播的封面采用“简洁”（clean）风格，显示为“目标目的地中的热门类别”（Top CATEGORY in Destination）；吸引用户注意力的幻灯片采用“引用”（quote）风格，展示带有 Reddit 来源标注的引文。所有图片在叠加效果应用前均需经过 Topaz 图像处理。触发命令为 “reddit-quote-topaz”。当 Bernard 说出 “reddit-quote-topaz” 时，或需要生成一个使用 Topaz 处理过的 Reddit 引文轮播时，应执行此任务。
---
# Reddit 引文轮播（Topaz 增强版）

该功能与 `reddit-quote-carousel` 类似，但在找到图片后、添加文本覆盖层之前，会使用 **Topaz Labs 的 2 倍图像增强技术** 对图片进行优化处理。

## 触发方式

- 当 Bernard 输入 “reddit-quote-topaz” 时，使用此功能；
- 当 Bernard 输入 “reddit-quote” 时，使用 `reddit-quote-carousel` 功能（不包含 Topaz 增强效果）。

## 参数

- **destination**（必填）：城市/地区（例如：“Barcelona”）
- **category**（必填）：筛选的类别（例如：“便宜美食”、“隐藏宝藏”、“约会之夜场所”）
- **popular_picks_url**（必填）：从 tabiji.ai 的 popular-picks 页面获取景点信息和 Reddit 引文的 URL
- **reddit_post_count**（可选）：分析的 Reddit 帖子数量（用于生成标题）。如果页面提供了该信息，请从中获取。

## 工作流程（包含 3 个子代理）

工作目录：`/tmp/ig-reddit-quote/`

### 子代理 1：抓取景点信息 + 寻找图片 + 图像增强

1. 使用 `web_fetch` 抓取 popular-picks 页面，获取以下内容：
   - 每个景点的名称
   - 每个景点对应的引人入胜的 Reddit 引文（具体、生动、具有个人色彩，而非泛泛而谈的赞美）
   - 引文所在的 Reddit 子版块（例如：“r/london”、“r/AskLondon”）
   - 如果页面显示了总数，还需获取 Reddit 帖子的总数

2. 使用 `instagram-photo-find` 工作流程寻找图片：
   - 为封面幻灯片准备 1 张目的地主题图片
   - 为每个景点准备 1 张图片（用于引文幻灯片）
   - 对每张图片执行 `web_search` → 下载候选图片 → 使用 `vision-score` 算法评估图片质量 → 选择最佳图片

3. 使用 **Topaz Labs 的 2 倍图像增强技术** 对每张最佳图片进行优化处理：
```bash
TOPAZ_API_KEY=$(security find-generic-password -s "topaz-api-key" -w)

curl --request POST \
  --url https://api.topazlabs.com/image/v1/enhance \
  --header "X-API-Key: ${TOPAZ_API_KEY}" \
  --header 'accept: image/jpeg' \
  --header 'content-type: multipart/form-data' \
  --form 'model=Low Resolution V2' \
  --form 'output_scale_factor=2' \
  --form 'output_format=jpeg' \
  --form "image=@/tmp/ig-reddit-quote/${slug}-best.jpg" \
  --output "/tmp/ig-reddit-quote/${slug}-enhanced.jpg"
```

**注意：** 如果同步返回的格式是包含 `process_id` 的 JSON 数据（而非图片字节），请使用异步处理流程：
```bash
# Submit async
RESPONSE=$(curl -s --request POST \
  --url https://api.topazlabs.com/image/v1/enhance/async \
  --header "X-API-Key: ${TOPAZ_API_KEY}" \
  --header 'content-type: multipart/form-data' \
  --form 'model=Low Resolution V2' \
  --form 'output_scale_factor=2' \
  --form 'output_format=jpeg' \
  --form "image=@/tmp/ig-reddit-quote/${slug}-best.jpg")

PROCESS_ID=$(echo "$RESPONSE" | jq -r '.process_id')

# Poll until Completed
while true; do
  STATUS=$(curl -s --header "X-API-Key: ${TOPAZ_API_KEY}" \
    "https://api.topazlabs.com/image/v1/status/${PROCESS_ID}" | jq -r '.status')
  [ "$STATUS" = "Completed" ] && break
  sleep 3
done

# Download
curl -s --header "X-API-Key: ${TOPAZ_API_KEY}" \
  "https://api.topazlabs.com/image/v1/download/${PROCESS_ID}" \
  --output "/tmp/ig-reddit-quote/${slug}-enhanced.jpg"
```

4. 将处理结果写入 `/tmp/ig-reddit-quote/manifest.json` 文件中：
```json
{
  "destination": "Barcelona",
  "category": "Cheap Eats",
  "reddit_post_count": 150,
  "cover_photo": "/tmp/ig-reddit-quote/cover-enhanced.jpg",
  "slides": [
    {
      "name": "Bar Cañete",
      "quote": "Went here on a random Tuesday and had the best patatas bravas of my life.",
      "subreddit": "r/barcelona",
      "photo": "/tmp/ig-reddit-quote/bar-canete-enhanced.jpg",
      "original": "/tmp/ig-reddit-quote/bar-canete-best.jpg",
      "source_url": "instagram.com/p/XXX/",
      "topaz_enhanced": true
    }
  ]
}
```

### 子代理 2：添加文本覆盖层

读取 `manifest.json` 文件，使用 `instagram-photo-text-overlay` 功能为优化后的图片添加文本覆盖层。

- **封面幻灯片**：采用简洁的文本样式
```bash
python3 /Users/psy/.openclaw/workspace/skills/instagram-photo-text-overlay/scripts/overlay.py \
  --input /tmp/ig-reddit-quote/cover-enhanced.jpg \
  --output /tmp/ig-reddit-quote/slide-1.jpg \
  --title "Top {COUNT} {CATEGORY} in {DESTINATION}" \
  --subtitle "Insider Takes from Reddit ({N}+ posts)" \
  --style clean --watermark "tabiji.ai"
```

- **其他幻灯片**：采用引文显示样式，每个景点对应一张图片
```bash
python3 /Users/psy/.openclaw/workspace/skills/instagram-photo-text-overlay/scripts/overlay.py \
  --input /tmp/ig-reddit-quote/{slug}-enhanced.jpg \
  --output /tmp/ig-reddit-quote/slide-{N}.jpg \
  --title "{ATTRACTION_NAME}" \
  --quote "{REDDIT_QUOTE}" \
  --author "{SUBREDDIT}" \
  --style quote --watermark "tabiji.ai"
```

最终输出文件位于：`/tmp/ig-reddit-quote/slide-{1-N}.jpg`

### 子代理 3：将图片发布到 Instagram

1. 将处理后的图片上传到 tabiji 的仓库（`img/instagram/`），并通过 Git 推送
2. 创建轮播图项容器
3. 为轮播图添加标题
4. 完成发布
5. 获取图片的永久链接
6. 清理上传的图片和本地临时文件

## Instagram API 认证

所需密钥来自 macOS 的 Keychain：
- `instagram-access-token`：Graph API 令牌
- `instagram-account-id`：Instagram 用户 ID（17841449394591017）

## Topaz API 认证

- `topaz-api-key`：Topaz Labs 的 API 密钥（存储在 macOS 的 Keychain 中）

## 标题模板
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

## 使用建议：

- 选择具体且富有个人色彩的引文（例如：“这是我吃过的最好吃的薯条”比“这个地方很棒”更有效）
- 确保引文长度控制在 120 字以内，以便在幻灯片上清晰显示
- 如果引文过长，请适当截断，但保留核心内容
- 封面标题应具有列表式的结构（例如：“巴塞罗那的 7 大便宜美食”
- **Topaz 增强模型**：`Low Resolution V2`——专为从网络获取的图片设计
- **Topaz 的使用限制**：如果出现 HTTP 429 错误，请采用指数级重试策略；每次处理 6-8 张图片即可
- 保留原始图片数据，以便在 Topaz 处理图片失败时可以回退使用原始图片