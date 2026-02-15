---
name: facebook
description: 通过 Graph API 管理 Facebook 页面、帖子及相关数据（如用户互动情况）。可以发布内容、查看评论，并分析用户的参与度（即用户与帖子的互动程度）。
metadata: {"clawdbot":{"emoji":"👤","requires":{"env":["FACEBOOK_ACCESS_TOKEN","FACEBOOK_PAGE_ID"]}}}
---

# Facebook

这是一个社交媒体平台（提供“Pages API”服务）。

## 环境配置

```bash
export FACEBOOK_ACCESS_TOKEN="xxxxxxxxxx"  # Page Access Token
export FACEBOOK_PAGE_ID="xxxxxxxxxx"
```

## 获取页面信息

```bash
curl "https://graph.facebook.com/v18.0/$FACEBOOK_PAGE_ID?fields=name,followers_count,fan_count" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

## 获取页面帖子

```bash
curl "https://graph.facebook.com/v18.0/$FACEBOOK_PAGE_ID/posts?fields=message,created_time,shares,likes.summary(true)" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

## 创建新帖子

```bash
curl -X POST "https://graph.facebook.com/v18.0/$FACEBOOK_PAGE_ID/feed" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN" \
  -d "message=Hello from automation!"
```

## 发布带图片的帖子

```bash
curl -X POST "https://graph.facebook.com/v18.0/$FACEBOOK_PAGE_ID/photos" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN" \
  -F "url=https://example.com/image.jpg" \
  -F "caption=Check this out!"
```

## 获取帖子评论

```bash
curl "https://graph.facebook.com/v18.0/{post_id}/comments" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

## 获取页面分析数据（Page Insights）

```bash
curl "https://graph.facebook.com/v18.0/$FACEBOOK_PAGE_ID/insights?metric=page_impressions,page_engaged_users&period=day" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN"
```

## 回复评论

```bash
curl -X POST "https://graph.facebook.com/v18.0/{comment_id}/comments" \
  -H "Authorization: Bearer $FACEBOOK_ACCESS_TOKEN" \
  -d "message=Thanks for your comment!"
```

## 链接：
- 商业账户：https://business.facebook.com
- 文档：https://developers.facebook.com/docs/graph-api