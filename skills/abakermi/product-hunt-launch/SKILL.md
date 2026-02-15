---
name: product-hunt-launch
version: 1.0.0
description: 通过 CLI 实时跟踪您的 Product Hunt 活动的发布数据（排名、点赞数、评论数）。
author: abakermi
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      env: ["PH_API_TOKEN"]
---

# Product Hunt 上线啦 🚀

您可以通过终端实时监控产品上线的各项指标。

## 设置

1. 从 [Product Hunt API 控制台](https://www.producthunt.com/v2/oauth/applications) 获取开发者令牌。
2. 将令牌设置为环境变量：`export PH_API_TOKEN="your_token"`

## 命令

### 检查帖子统计信息
```bash
ph-launch stats --slug "your-product-slug"
# Output: Rank #4 | 🔼 450 | 💬 56
```

### 监控产品上线情况（实时仪表盘）
```bash
ph-launch monitor --slug "your-product-slug" --interval 60
```

### 查看当天的排行榜
```bash
ph-launch leaderboard
```