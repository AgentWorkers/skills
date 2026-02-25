```yaml
---
name: facebook-scraper
description: 从浏览器中发现并抓取Facebook页面和公共群组的信息。
emoji: 📘
version: 1.0.0
author: influenza
tags:
  - facebook
  - scraping
  - social-media
  - page-discovery
  - group-discovery
  - business-pages
metadata:
  clawdbot:
    requires:
      bins:
        - python3
        - chromium

    config:
      stateDirs:
        - data/output
        - data/queue
        - thumbnails
      outputFormats:
        - json
        - csv
---
```

```bash
# 发现Facebook页面（返回JSON格式的数据）
discover --location "Miami" --category "restaurant" --type page --output json

# 发现Facebook群组（返回JSON格式的数据）
discover --location "New York" --category "fitness" --type group --output json

# 抓取单个页面的信息（返回JSON格式的数据）
scrape --page-name examplebusiness --output json

# 抓取单个群组的信息（返回JSON格式的数据）
scrape --page-name examplegroup --type group --output json
```

```json
{
  "page_name": "example_business",
  "display_name": "Example Business",
  "entity_type": "page",
  "category": "Restaurant",
  "subcategory": "Italian Restaurant",
  "about": "一家成立于1985年的家族经营的意大利餐厅",
  "followers": 45000,
  "page_likes": 42000,
  "location": "Miami, FL",
  "address": "123 Main St, Miami, FL 33101",
  "phone": "+1-555-0123",
  "email": "info@example.com",
  "website": "https://example.com",
  "hours": "周一至周六 11:00 AM - 10:00 PM",
  "is_verified": false,
  "page_tier": "mid",
  "profile_pic_local": "thumbnails/example_business/profile_abc123.jpg",
  "cover_photo_local": "thumbnails/example_business/cover_def456.jpg",
  "recent_posts": [
    {"post_url": "https://facebook.com/example_business/posts/123", "reactions": 320, "comments": 45, "shares": 12}
  ],
  "scrape_timestamp": "2026-02-20T14:30:00"
}
```

```json
{
  "page_name": "example_group",
  "display_name": "Miami Fitness Community",
  "entity_type": "group",
  "about": "一个为迈阿密健身爱好者设立的社区",
  "members": 15000,
  "privacy": "Public",
  "posts_per_day": 25,
  "location": "Miami",
  "page_tier": "mid",
  "profile_pic_local": "thumbnails/example_group/profile_abc123.jpg",
  "cover_photo_local": "thumbnails/example_group/cover_def456.jpg",
  "scrape_timestamp": "2026-02-20T14:30:00"
}
```

```json
{
  "google_search": {
    "enabled": true,
    "api_key": "",
    "search_engine_id": "",
    "queries_per_location": 3
  },
  "scraper": {
    "headless": false,
    "min_likes": 1000,
    "download_thumbnails": true,
    "max_thumbnails": 6
  },
  "cities": ["New York", "Los Angeles", "Miami", "Chicago"],
  "categories": ["restaurant", "retail", "fitness", "real-estate", "healthcare", "beauty"]
}
```