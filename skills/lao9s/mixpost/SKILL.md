---
name: mixpost
description: Mixpost是一款自托管的社交媒体管理软件，可帮助您在多个平台上安排和管理您的社交媒体内容，包括Facebook、Twitter/X、Instagram、LinkedIn、Pinterest、TikTok、YouTube、Mastodon、Google Business Profile、Threads、Bluesky等。
homepage: https://mixpost.app
metadata: {"openclaw":{"emoji":"🗓️","primaryEnv":"MIXPOST_ACCESS_TOKEN","requires":{"env":["MIXPOST_URL","MIXPOST_ACCESS_TOKEN","MIXPOST_WORKSPACE_UUID"]}}}
---

# Mixpost 功能介绍

Mixpost 是一款自托管的社交媒体管理软件，可帮助您在多个平台上安排和管理社交媒体内容，包括 Facebook、Twitter/X、Instagram、LinkedIn、Pinterest、TikTok、YouTube、Mastodon、Google Business Profile、Threads、Bluesky 等。

## 设置

1. 登录到您的 Mixpost 控制面板。
2. 从用户菜单中点击 **访问令牌**（Access Tokens）。
3. 点击 **创建**（Create）以生成新的访问令牌。
4. 获取您的工作区 UUID：前往 **社交媒体账户**（Social Accounts）页面，点击任意账户的 **三个点菜单**（3 dots menu），然后复制该账户的工作区 UUID。
5. 设置环境变量：
   ```bash
   export MIXPOST_URL="https://your-mixpost-instance.com/mixpost"
   export MIXPOST_ACCESS_TOKEN="your-access-token"
   export MIXPOST_WORKSPACE_UUID="your-workspace-uuid"
   ```

## 测试连接

```bash
curl -X GET "$MIXPOST_URL/api/ping" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

---

## 账户

### 获取所有账户

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/accounts" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### 获取特定账户

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/accounts/:accountUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

---

## 媒体

### 获取所有媒体文件

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media?limit=50" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### 获取特定媒体文件

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media/:mediaUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### 上传媒体文件（使用表单数据）

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json" \
  -F "file=@/path/to/your/file.png"
```

### 更新媒体文件

```bash
curl -X PUT "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media/:mediaUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "alt_text": "Alternative text for accessibility"
  }'
```

### 删除媒体文件

```bash
curl -X DELETE "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "items": ["media-id-1", "media-id-2"]
  }'
```

---

## 标签

### 获取所有标签

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### 获取特定标签

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags/:tagUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### 创建标签

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Marketing",
    "hex_color": "#FF5733"
  }'
```

### 更新标签

```bash
curl -X PUT "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags/:tagUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Updated Tag Name",
    "hex_color": "#00FF00"
  }'
```

### 删除标签

```bash
curl -X DELETE "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags/:tagUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

---

## 帖子

### 获取所有帖子

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts?limit=50&status=scheduled&page=1" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

**查询参数：**
- `limit`（数字，默认值：50）：每页显示的帖子数量
- `status`：`draft`（草稿）、`scheduled`（已安排）、`published`（已发布）、`failed`（失败）、`needs_approval`（需要审核）、`trash`（已删除）
- `keyword`（字符串）：按内容搜索帖子
- `accounts`（数组）：按账户 ID 过滤帖子
- `tags`（数组）：按标签名称过滤帖子
- `page`（数字）：分页的页码

### 获取特定帖子

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### 创建帖子

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "schedule": true,
    "date": "2024-12-25",
    "time": "10:00",
    "timezone": "America/New_York",
    "accounts": [1, 2],
    "tags": [1],
    "versions": [
      {
        "account_id": 0,
        "is_original": true,
        "content": [
          {
            "body": "Hello from Mixpost API!",
            "media": [1, 2],
            "url": "https://example.com"
          }
        ],
        "options": {}
      }
    ]
  }'
```

**帖子选项：**
- `schedule`：设置为 `true` 以安排在特定日期/时间发布
- `schedule_now`：设置为 `true` 立即发布
- `queue`：设置为 `true` 将帖子添加到发布队列
- 如果未设置任何选项，帖子将保存为草稿状态

**平台特定选项：**
```json
{
  "options": {
    "facebook_page": {
      "type": "post" // post, reel, story
    },
    "instagram": {
      "type": "post" // post, reel, story
    },
    "linkedin": {
      "visibility": "PUBLIC" // PUBLIC, CONNECTIONS
    },
    "mastodon": {
      "sensitive": false // boolean
    },
    "pinterest": {
      "link": null, // null | string
      "title": "", // string
      "boards": {
        "account-1": "971672010430333260" // The key `account-*` is the ID of your Pinterest account
      }
    },
    "youtube": {
      "title": null, // null | string
      "status": "public" // public, private, unlisted
    },
    "gbp": { // Google Business Profile
      "type": "post", // post, offer, event
      "button": "NONE", // NONE, BOOK, ORDER, SHOP, LEARN_MORE, SIGN_UP, CALL
      "button_link": "", // Leave empty if button is NONE or CALL
      "offer_has_details": false, // Only applies if type is offer
      "coupon_code": "", // Only applies if type is offer and offer_has_details is true
      "offer_link": "", // Only applies if type is offer and offer_has_details is true
      "terms": "", // Only applies if type is offer and offer_has_details is true
      "event_title": "", // Only applies if type is event or offer
      "start_date": null, // null | string - Only applies if type is event or offer
      "end_date": null, // null | string - Only applies if type is event or offer
      "event_has_time": false, // Only applies if type is event
      "start_time": "09:00", // Only applies if type is event and event_has_time is true
      "end_time": "17:00" // Only applies if type is event and event_has_time is true
    },
    "tiktok": {
      "privacy_level": {
        "account-2": "PUBLIC_TO_EVERYONE" // PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIENDS, SELF_ONLY - The key `account-*` is the ID of your TikTok account
      },
      "allow_comments": {
        "account-2": true // boolean
      },
      "allow_duet": {
        "account-2": false // boolean
      },
      "allow_stitch": {
        "account-2": false // boolean
      },
      "content_disclosure": {
        "account-2": false // boolean
      },
      "brand_organic_toggle": {
        "account-2": false // boolean
      },
      "brand_content_toggle": {
        "account-2": false // boolean
      }
    }
  }
}
```

### 更新帖子

```bash
curl -X PUT "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "content": "Updated post content",
    "schedule_at": "2024-12-25T10:00:00Z",
    "media": ["url1", "url2"],
    "tags": ["tag1", "tag2"],
    "account_ids": ["id1", "id2"]
  }'
```

### 删除帖子

```bash
curl -X DELETE "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "trash": false,
    "delete_mode": "app_only"
  }'
```

**删除方式：**
- `app_only`：仅从应用程序中删除帖子（默认值）
- `app_and_social`：从应用程序和社交媒体平台中同时删除帖子
- `social_only`：仅从社交媒体平台中删除帖子

### 删除多篇帖子

```bash
curl -X DELETE "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "posts": ["post-uuid-1", "post-uuid-2"],
    "trash": false,
    "delete_mode": "app_only"
  }'
```

### 安排帖子发布

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/schedule/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "postNow": false
  }'
```

### 将帖子添加到发布队列

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/add-to-queue/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### 审核帖子

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/approve/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```