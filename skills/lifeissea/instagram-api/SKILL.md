---
name: Instagram API
description: 使用官方的 Meta Graph API 将内容发布到 Instagram（动态、故事、Reels、轮播图以及私信）。需要借助 Imgur 来托管媒体文件。
version: 1.1.1
author: raon
requires_env:
  - INSTAGRAM_ACCESS_TOKEN
  - INSTAGRAM_BUSINESS_ACCOUNT_ID
  - IMGUR_CLIENT_ID
---
# instagram-api

本技能使用Meta Graph API直接在Instagram和Threads上发布内容。媒体托管通过Imgur API完成（用于生成图片/视频的公开链接）。

---

## 获取Imgur客户端ID

由于Instagram Graph API仅支持使用公开链接上传媒体文件，因此需要获取Imgur的客户端ID：

1. 访问 [https://api.imgur.com/oauth2/addclient](https://api.imgur.com/oauth2/addclient)
2. 输入 **应用程序名称**（例如：`raon-instagram`）
3. 选择 **授权类型** 为 “Anonymous usage without user authorization”（无需用户授权的匿名使用）
4. 设置 **授权回调URL** 为 `https://localhost`（由于是匿名使用，只需填写正确的格式即可）
5. 输入电子邮件后提交申请，然后查看并记录 **客户端ID**
6. 设置环境变量：
   ```bash
   export IMGUR_CLIENT_ID="your_client_id_here"
   ```

---

## 设置环境变量

```bash
# ~/.openclaw/.env 또는 ~/.zshrc에 추가
export INSTAGRAM_ACCESS_TOKEN="your_token_here"
export INSTAGRAM_BUSINESS_ACCOUNT_ID="your_account_id_here"

# Threads (선택)
export THREADS_ACCESS_TOKEN="your_threads_token_here"
export THREADS_USER_ID="your_threads_user_id_here"

# Imgur (이미지 호스팅용 — 피드/릴스 업로드 시 필요)
export IMGUR_CLIENT_ID="your_imgur_client_id_here"
```

---

## 获取Meta Graph API令牌

1. 访问 [Meta for Developers](https://developers.facebook.com/)
2. 创建新的应用程序，并选择 **Business** 类型
3. 添加 Instagram Graph API 产品
4. 申请以下权限：
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
5. 在 [Graph API Explorer](https://developers.facebook.com/tools/explorer/) 中获取 **访问令牌**（Access Token）
   - 请确保获取的是长期有效的令牌（有效期为60天）
6. 查看并记录 **企业账户ID**（Business Account ID）：
   ```bash
   curl "https://graph.facebook.com/v21.0/me/accounts?access_token=YOUR_TOKEN"
   ```

> 💡 **Imgur客户端ID**：请从 [https://api.imgur.com/oauth2/addclient](https://api.imgur.com/oauth2/addclient) 获取（选择 “Anonymous usage”）

---

## 脚本使用方法

### 发布动态（Feed Posts）
```bash
bash scripts/post-feed.sh <이미지경로> <캡션파일>

# 예시
bash scripts/post-feed.sh ./photo.jpg ./caption.txt
```

### 发布故事（Stories）
```bash
bash scripts/post-story.sh <이미지경로>

# 예시
bash scripts/post-story.sh ./story.jpg
```

### 发布直播（Lives）
```bash
bash scripts/post-reels.sh <영상경로> <캡션파일>

# 예시
bash scripts/post-reels.sh ./reel.mp4 ./caption.txt
```

### 发布轮播图（Carousel Posts）
```bash
bash scripts/post-carousel.sh <캡션파일> <이미지1> <이미지2> [이미지3...]

# 예시
bash scripts/post-carousel.sh ./caption.txt ./img1.jpg ./img2.jpg ./img3.jpg
```

### 发布Threads帖子
```bash
bash scripts/post-threads.sh <캡션파일> [이미지URL]

# 예시 (텍스트만)
bash scripts/post-threads.sh ./caption.txt

# 예시 (이미지 포함)
bash scripts/post-threads.sh ./caption.txt "https://example.com/image.jpg"
```

---

## 文件结构

```
instagram-api/
├── SKILL.md                    # 이 파일
└── scripts/
    ├── post-feed.sh            # 피드 포스팅
    ├── post-story.sh           # 스토리 포스팅
    ├── post-reels.sh           # 릴스 포스팅
    ├── post-carousel.sh        # 캐러셀 포스팅
    └── post-threads.sh         # Threads 포스팅
```

---

## 注意事项：

- Instagram仅支持使用公开链接上传媒体文件（无法直接上传本地文件）
- 该技能通过Imgur生成临时公开链接
- 发布直播视频可能需要几分钟时间完成
- 如果API调用失败，请查看 `~/logs/sns/` 目录中的日志文件