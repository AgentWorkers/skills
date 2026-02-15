# Instagram个人资料抓取工具

这是一个基于浏览器的Instagram个人资料发现和抓取工具。

```yaml
---
name: instagram-scraper
description: Discover and scrape Instagram profiles from your browser.
emoji: 📸
version: 1.0.3
author: influenza
tags:
  - instagram
  - scraping
  - social-media
  - influencer-discovery
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

## 概述

该工具提供了一个两阶段的Instagram抓取系统：

1. **个人资料发现**  
2. **浏览器抓取**  

## 特点

- 🔍  - 根据地理位置和类别发现Instagram个人资料  
- 🌐  - 全面模拟浏览器环境，确保抓取数据的准确性  
- 🛡️  - 通过浏览器指纹识别、模拟人类行为以及使用隐蔽脚本进行抓取  
- 📊  - 提供个人资料信息、统计数据、图片以及互动数据  
- 💾  - 可以将数据导出为JSON或CSV格式，并包含下载的缩略图  
- 🔄  - 可以恢复中断的抓取会话  
- ⚡  - 自动跳过私密账户、粉丝数量较少的账户以及空个人资料  

#### 获取Google API凭证（可选）

1. 访问[Google Cloud Console](https://console.cloud.google.com/)  
2. 创建一个新的项目或选择现有项目  
3. 启用“自定义搜索API”  
4. 创建API凭证（API密钥）  
5. 访问[Programmable Search Engine](https://programmablesearchengine.google.com/)  
6. 创建一个以`instagram.com`为搜索目标的搜索引擎  
7. 复制搜索引擎ID  

## 使用方法

### 代理工具接口

对于OpenClaw代理的集成，该工具提供JSON格式的输出数据：

```bash
# Discover profiles (returns JSON)
discover --location "Miami" --category "fitness" --output json

# Scrape single profile (returns JSON)
scrape --username influencer123 --output json
```

## 输出数据

### 个人资料数据结构

```json
{
  "username": "example_user",
  "full_name": "Example User",
  "bio": "Fashion blogger | NYC",
  "followers": 125000,
  "following": 1500,
  "posts_count": 450,
  "is_verified": false,
  "is_private": false,
  "influencer_tier": "mid",
  "category": "fashion",
  "location": "New York",
  "profile_pic_local": "thumbnails/example_user/profile_abc123.jpg",
  "content_thumbnails": [
    "thumbnails/example_user/content_1_def456.jpg",
    "thumbnails/example_user/content_2_ghi789.jpg"
  ],
  "post_engagement": [
    {"post_url": "https://instagram.com/p/ABC123/", "likes": 5420, "comments": 89}
  ],
  "scrape_timestamp": "2025-02-09T14:30:00"
}
```

### 影响力等级

| 等级 | 粉丝数量范围    |
|-------|-------------------|
| nano  | < 1,000           |
| micro | 1,000 - 10,000    |
| mid   | 10,000 - 100,000  |
| macro | 100,000 - 100万      |
| mega  | > 100万       |

### 文件输出

- **队列文件**：`data/queue/{location}_{category}_{timestamp}.json`  
- **抓取数据**：`data/output/{username}.json`  
- **缩略图**：`thumbnails/{username}/profile_*.jpg`, `thumbnails/{username}/content_*.jpg`  
- **导出文件**：`data/export_{timestamp}.json`, `data/export_{timestamp}.csv`  

## 配置

编辑`config/scraper_config.json`文件以进行配置：

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
    "min_followers": 1000,
    "download_thumbnails": true,
    "max_thumbnails": 6
  },
  "cities": ["New York", "Los Angeles", "Miami", "Chicago"],
  "categories": ["fashion", "beauty", "fitness", "food", "travel", "tech"]
}
```



## 应用的过滤规则

该工具会自动过滤以下类型的账户：

- ❌ 私密账户  
- ❌ 粉丝数量少于1,000的账户（可配置）  
- ❌ 没有发布内容的账户  
- ❌ 不存在或已被删除的账户  
- ❌ 已经被抓取过的账户（避免重复抓取）  

## 故障排除

### 登录问题

- 确保凭证正确  
- 在提示时处理验证码  
- 如果遇到速率限制，请等待一段时间，脚本会自动重试  

### 未发现个人资料

- 检查Google API密钥和配额  
- 确认搜索引擎ID已正确配置为`instagram.com`  
- 尝试不同的地理位置或类别组合  

### 速率限制

- 减慢抓取速度（增加延迟时间）  
- 使用多个Instagram账户  
- 在非高峰时段运行脚本