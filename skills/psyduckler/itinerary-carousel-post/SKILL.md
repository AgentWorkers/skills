---
name: itinerary-carousel-post
description: >
  根据 `tabiji.ai` 提供的行程信息，创建并发布一条 Instagram 旋转图（carousel）帖子。具体步骤如下：  
  1. 使用给定的行程 URL，为目的地及主要景点查找适合发布到 Instagram 的照片；  
  2. 为这些照片添加文字说明（overlay）；  
  3. 将处理后的照片组合成旋转图格式，并发布到 Instagram。  
  该功能适用于需要为 `tabiji.ai` 提供的行程或目的地创建 Instagram 帖子（包括旋转图或其他社交媒体内容）的场景。
---
# 创建 Instagram 旋转图帖子

端到端流程：行程 URL → 照片获取 → 文本叠加 → 发布 Instagram 旋转图帖子。

## 参数

- **itinerary_url**（必填）：tabiji.ai 的行程 URL（例如：`https://tabiji.ai/i/thaw-dome/`）
- **destination**（必填）：城市/地区名称（例如：“Kuala Lumpur”）
- **attractions**（必填）：5 个景点的名称及简短描述
- **caption**（可选）：自定义标题。如果省略，系统会自动生成一个包含目的地名称、景点列表、生物信息中的链接以及相关标签的标题。

## 流程（建议使用 3 个串联的子代理）

为提高可靠性，将流程拆分为 3 个子代理。每个子代理将输出结果保存到 `/tmp/ig-carousel/` 目录中。

### 子代理 1：照片获取

使用 `instagram-photo-find` 技能工作流为每个景点获取照片（1 个目的地对应 5 张照片，共计 6 张）。

对于每个景点：
1. 使用 `web_search`：`site:instagram.com/p/ "{subject}" photo`（获取 10 张结果）
2. 下载前 5 张符合条件的照片：`curl -s -L -o /tmp/ig-carousel/raw-{slug}-{n}.jpg "https://www.instagram.com/p/{shortcode}/media/?size=l"`
3. 为每张照片打分（1-10 分），用于判断其是否适合作为该景点的封面照片。
4. 保留每个景点最好的照片 → 将照片保存到 `/tmp/igCarousel/{slug}-best.jpg`

输出：6 张最佳照片及 JSON 格式的结果文件 `/tmp/igCarousel/manifest.json`：
```json
[{"slug": "kuala-lumpur", "subject": "Kuala Lumpur", "score": 7, "path": "/tmp/ig-carousel/kuala-lumpur-best.jpg", "source": "instagram.com/p/XXX/"}]
```

### 子代理 2：文本叠加

读取子代理 1 提供的图片列表，为每张照片添加文本叠加效果。

**第 1 张图片（封面）** — 采用简洁的文本样式：
```bash
python3 skills/instagram-photo-text-overlay/scripts/overlay.py \
  --input /tmp/ig-carousel/{dest-slug}-best.jpg \
  --output /tmp/ig-carousel/slide-1.jpg \
  --title "{N} Day {DESTINATION} Itinerary Highlights" \
  --style clean --watermark "tabiji.ai"
```

**第 2–6 张图片** — 为每个景点添加包含内部提示的文本：
```bash
python3 skills/instagram-photo-text-overlay/scripts/overlay.py \
  --input /tmp/ig-carousel/{slug}-best.jpg \
  --output /tmp/ig-carousel/slide-{N}.jpg \
  --title "{ATTRACTION}" \
  --quote "{Specific insider tip about THIS attraction — must directly reference the place in the title, not a generic travel tip}" \
  --author "tabiji.ai" \
  --style quote --watermark "tabiji.ai"
```

输出：6 张带有文本叠加效果的图片，保存在 `/tmp/igCarousel/slide-{1-6}.jpg` 目录中。

### 子代理 3：发布到 Instagram

1. 将图片公开托管到 Instagram 并复制到 tabiji 仓库（`img/instagram/`），然后通过 Git 推送。使用原始的 GitHub URL（`https://raw.githubusercontent.com/psyduckler/tabiji/main/img/instagram/slide-{N}.jpg`）。推送后等待约 30 秒，让 GitHub 的 CDN 加速图片加载。
2. 为每张图片创建旋转图帖子的容器。
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/${IG_USER}/media" \
  -d "image_url=${PUBLIC_URL}" \
  -d "is_carousel_item=true" \
  -d "access_token=${IG_TOKEN}"
```

3. 将所有图片及标题组合成一个旋转图帖子容器。
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/${IG_USER}/media" \
  --data-urlencode "caption=${CAPTION}" \
  -d "media_type=CAROUSEL" \
  -d "children=${CHILD_IDS}" \
  -d "access_token=${IG_TOKEN}"
```

4. 发布旋转图帖子。
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/${IG_USER}/media_publish" \
  -d "creation_id=${CAROUSEL_ID}" \
  -d "access_token=${IG_TOKEN}"
```

5. 获取永久链接：
   如果 `media_publish` 返回 `POST_ID`，则直接获取该永久链接。
```bash
curl -s "https://graph.facebook.com/v21.0/${POST_ID}?fields=permalink&access_token=${IG_TOKEN}"
```

**如果 `media_publish` 返回错误代码 2207051（请求被限制）：** 尽管 Instagram 返回了错误，但有时仍会处理请求。在确认失败前，请务必检查账户的最新发布内容：
   如果最新发布的照片时间在几分钟内，说明发布成功——此时可以获取永久链接。
```bash
curl -s "https://graph.facebook.com/v21.0/${IG_USER}/media?fields=id,timestamp,permalink&limit=1&access_token=${IG_TOKEN}"
```

6. 清理托管的图片：在确认发布成功后，从 tabiji 仓库中删除这些图片，并执行相应的清理操作。
```bash
cd /path/to/tabiji/repo
git rm img/instagram/slide-*.jpg
git commit -m "cleanup: remove instagram carousel images after publish"
git push
```

7. 同时清理本地临时文件。
```bash
rm -rf /tmp/ig-carousel/
```

输出：Instagram 帖子的完整 URL。

## Instagram API 认证

从 macOS Keychain 中获取以下密钥：
- `instagram-access-token`：Graph API 令牌
- `instagram-account-id`：Instagram 用户 ID（17841449394591017）

## 标题模板
```
🇲🇾 {N} Nights in {Destination} — {Itinerary Subtitle}

{One-line hook about the trip}

📍 Swipe through our top 5 picks:
1. {Attraction 1} — {one-line reason}
2. {Attraction 2} — {one-line reason}
3. {Attraction 3} — {one-line reason}
4. {Attraction 4} — {one-line reason}
5. {Attraction 5} — {one-line reason}

Full free itinerary with tips, prices & Reddit recs 👉 {ITINERARY_URL}

💬 {PROVOCATIVE_QUESTION — e.g. "Is 5 nights enough for {Destination} or do you need more?" or "What's the one thing most tourists get wrong about {Destination}?"}

#{destination_hashtag} #{country} #travelitinerary #foodietravel #southeastasia #asiatravel #travelguide #tabiji
```

## 注意事项：

- 使用原始的 GitHub URL 可以用于上传图片；tabiji.ai 使用的 Cloudflare CDN 可能会引发格式验证错误。
- 在创建图片容器时添加 `sleep 1` 以避开请求限制。
- 如果某个景点的照片评分较低（<5 分），可以尝试使用 Unsplash 或 Flickr 等其他图片来源，或使用更具体的地标名称进行搜索。
- 伊斯兰或文化类博物馆的 Instagram 图片质量可能较低——建议尝试使用博物馆的官方 Instagram 账号进行搜索。