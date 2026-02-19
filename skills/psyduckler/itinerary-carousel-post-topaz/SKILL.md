---
name: itinerary-carousel-post-topaz
description: 根据 tabiji.ai 提供的行程信息，创建并发布一条 Instagram 旋转图（carousel post），并使用 Topaz Labs 的 AI 图像增强功能进行处理。该流程与 `itineraryCarousel-post` 类似，但在找到图片后、添加文字层之前，会增加一个使用 Topaz Labs 进行图像优化/提升的步骤。适用于需要使用 Topaz Labs 图像增强功能来制作 Instagram 旋转图的情况。
---
# 创建 Instagram 旋转图帖子（使用 Topaz AI 技术增强）

**端到端工作流程：**  
行程 URL → 照片获取 → **Topaz AI 增强** → 文本叠加 → 发布到 Instagram 旋转图。

该流程与 `itinerary-carousel-post` 类似，不同之处在于：在为每个景点选择最佳照片后，会添加一个使用 Topaz AI 进行图像增强的步骤。

## 参数  
- **itinerary_url**（必填）：tabiji.ai 的行程 URL（例如：`https://tabiji.ai/i/thaw-dome/`）  
- **destination**（必填）：城市/地区名称（例如：“Kuala Lumpur”）  
- **attractions**（必填）：5 个景点的名称及简短描述  
- **caption**（可选）：自定义标题。如果省略，系统会自动生成一个包含目的地名称、景点列表、用于个人简介中的点击链接以及相关标签的标题。  

## 推荐的工作流程（包含 3 个子任务）  
为提高可靠性，将流程拆分为 3 个子任务，每个任务将结果保存到 `/tmp/ig-carousel/` 目录中。  

### 子任务 1：照片获取与 Topaz 增强  
针对每个景点使用 `instagram-photo-find` 工作流程（1 个目的地对应 5 个景点，共 6 张照片）：  
1. 使用 `web_search`：`site:instagram.com/p/ "{subject}" photo`（返回 10 张结果）  
2. 下载前 5 张符合条件的照片：`curl -s -L -o /tmp/igCarousel/raw-{slug}-{n}.jpg "https://www.instagram.com/p/{shortcode}/media/?size=l"`  
3. 为每张照片打分（1-10 分），用于判断其是否适合作为该景点的封面照片。  
4. 保留每个景点的最佳照片，并将其保存为 `/tmp/igCarousel/{slug}-best.jpg`。  

**5. 对每张最佳照片进行 Topaz 增强处理：**  
**代码块：**  
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
  --form "image=@/tmp/ig-carousel/${slug}-best.jpg" \
  --output "/tmp/ig-carousel/${slug}-enhanced.jpg"
```  

**注意：**  
如果同步端点超时或返回 `process_id` 而不是图片数据，请使用异步处理方式：  
**代码块：**  
```bash
# Async: submit
RESPONSE=$(curl -s --request POST \
  --url https://api.topazlabs.com/image/v1/enhance/async \
  --header "X-API-Key: ${TOPAZ_API_KEY}" \
  --header 'content-type: multipart/form-data' \
  --form 'model=Low Resolution V2' \
  --form 'output_scale_factor=2' \
  --form 'output_format=jpeg' \
  --form "image=@/tmp/ig-carousel/${slug}-best.jpg")

PROCESS_ID=$(echo "$RESPONSE" | jq -r '.process_id')

# Poll status until Completed
while true; do
  STATUS=$(curl -s --header "X-API-Key: ${TOPAZ_API_KEY}" \
    "https://api.topazlabs.com/image/v1/status/${PROCESS_ID}" | jq -r '.status')
  [ "$STATUS" = "Completed" ] && break
  sleep 3
done

# Download result
curl -s --header "X-API-Key: ${TOPAZ_API_KEY}" \
  "https://api.topazlabs.com/image/v1/download/${PROCESS_ID}" \
  --output "/tmp/ig-carousel/${slug}-enhanced.jpg"
```  

**模型选择：**  
`Low Resolution V2`——专为从 Instagram 获取的图片设计，能够处理 JPEG 压缩导致的图像质量下降问题，适用于我们的使用场景。该模型处理速度快且成本低。  

**参数说明：**  
- `output_scale_factor=2`：将图片分辨率提高一倍（2x 缩放）。对于典型的 Instagram 图片（约 1080px），处理后的图片分辨率约为 2160px，这为后续的文本叠加提供了足够的清晰度。  
- `output_format=jpeg`：确保文件大小符合 Instagram 的 8MB 限制。  

**输出结果：**  
6 张经过增强的图片保存在 `/tmp/igCarousel/{slug}-enhanced.jpg`，同时生成 JSON 格式的图片清单文件 `/tmp/igCarousel/manifest.json`：  
**代码块：**  
```json
[{"slug": "kuala-lumpur", "subject": "Kuala Lumpur", "score": 7, "path": "/tmp/ig-carousel/kuala-lumpur-enhanced.jpg", "original": "/tmp/ig-carousel/kuala-lumpur-best.jpg", "source": "instagram.com/p/XXX/", "topaz_enhanced": true}]
```  

### 子任务 2：文本叠加  
读取子任务 1 生成的图片清单文件，然后为每张增强后的图片添加文本叠加效果：  
- **封面图片（第 1 张幻灯片）**：采用简洁的文字样式。  
- **其他幻灯片（第 2–6 张）**：为每个景点添加包含内部提示的文字内容。  
**代码块：**  
```bash
python3 skills/instagram-photo-text-overlay/scripts/overlay.py \
  --input /tmp/ig-carousel/{dest-slug}-enhanced.jpg \
  --output /tmp/ig-carousel/slide-1.jpg \
  --title "{N} Day {DESTINATION} Itinerary Highlights" \
  --style clean --watermark "tabiji.ai"
```  
**输出结果：**  
6 张带有文本叠加效果的图片保存在 `/tmp/igCarousel/slide-{1-6}.jpg`。  

### 子任务 3：发布到 Instagram  
1. 将处理后的图片上传到 Instagram：将图片文件复制到 tabiji 的仓库（`img/instagram/`），并通过 Git 推送。使用原始的 GitHub URL（`https://raw.githubusercontent.com/psyduckler/tabiji/main/img/instagram/slide-{N}.jpg`）。推送完成后等待约 30 秒，以便 GitHub 的 CDN 服务器完成图片缓存。  
2. 为每张图片创建旋转图容器。  
**代码块：**  
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/${IG_USER}/media" \
  -d "image_url=${PUBLIC_URL}" \
  -d "is_carousel_item=true" \
  -d "access_token=${IG_TOKEN}"
```  
3. 将所有图片及对应的标题组合成一个旋转图容器。  
**代码块：**  
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/${IG_USER}/media" \
  --data-urlencode "caption=${CAPTION}" \
  -d "media_type=CAROUSEL" \
  -d "children=${CHILD_IDS}" \
  -d "access_token=${IG_TOKEN}"
```  
4. 最后发布旋转图。  
**代码块：**  
```bash
curl -s -X POST "https://graph.facebook.com/v21.0/${IG_USER}/media_publish" \
  -d "creation_id=${CAROUSEL_ID}" \
  -d "access_token=${IG_TOKEN}"
```  
5. 获取永久链接：  
   如果 `media_publish` 函数返回 `POST_ID`，则直接获取该永久链接。  
**代码块：**  
```bash
curl -s "https://graph.facebook.com/v21.0/${POST_ID}?fields=permalink&access_token=${IG_TOKEN}"
```  
   **如果 `media_publish` 返回错误代码 2207051（表示请求被限制）：**  
   尽管系统返回错误，Instagram 仍可能成功处理请求。因此发布前请务必检查账户的最新发布记录：  
   **代码块：**  
   **如果最新发布的图片时间在几分钟内，说明发布成功，即可获取永久链接。**  
   **清理已上传的图片：**  
   发布确认后，从 tabiji 仓库中删除这些图片，并清理本地临时文件。  
   **代码块：**  
   **代码块：**  
   **输出结果：**  
   最终的 Instagram 发布链接。  

## Instagram API 认证  
所需凭据来自 macOS 的 Keychain：  
- `instagram-access-token`：Graph API 令牌  
- `instagram-account-id`：Instagram 用户 ID（例如：17841449394591017）  

## Topaz API 认证  
所需凭据来自 macOS 的 Keychain：  
- `topaz-api-key`：Topaz Labs 的 API 密钥  

## 标题模板  
**代码块：**  
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

**使用提示：**  
- 使用原始的 GitHub URL 作为 Instagram 图片的链接；直接使用 tabiji.ai 的 Cloudflare CDN 可能会引发格式验证错误。  
- 在创建图片容器时添加 `sleep 1` 的延迟，以避免触发 Instagram 的请求限制。  
- 如果某个景点的照片评分较低（<5 分），可以尝试使用 Unsplash 或 Flickr 等其他图片资源，或使用更具体的景点名称进行搜索。  
- 伊斯兰或文化类博物馆的 Instagram 图片质量可能较低，建议尝试使用博物馆的官方 Instagram 账号进行搜索。  
- **Topaz 的同步端点可能直接返回图片数据（请检查 Content-Type 头部信息）；如果返回 JSON 格式的 `process_id`，请切换到异步处理方式。**  
- **Topaz 的请求限制：** 如果遇到 HTTP 429 错误，请采用指数级退避策略进行重试。同时，连续处理 6 张图片通常不会引发问题。  
- **保留原始图片：** 图片清单文件中同时保存了增强后的图片和原始图片的路径，以便在 Topaz 处理失败时可以回退使用原始图片。