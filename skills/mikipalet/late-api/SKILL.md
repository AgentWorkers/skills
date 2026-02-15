---
name: late-api
description: 官方的 Late API 参考文档，用于在 13 个社交媒体平台上安排发布内容。涵盖了认证、接口端点（endpoints）、Webhook 以及各平台特有的功能。在开发涉及 Late Social Media Scheduling API 的应用程序时，请参考本文档。
---

# Late API参考

使用一个API在13个社交媒体平台上发布内容。

**基础URL：** `https://getlate.dev/api/v1`

**文档：** [getlate.dev/docs](https://getlate.dev/docs)

## 快速入门

```bash
# 1. Create profile
curl -X POST https://getlate.dev/api/v1/profiles \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"name": "My Brand"}'

# 2. Connect account (opens OAuth)
curl "https://getlate.dev/api/v1/connect/twitter?profileId=PROFILE_ID" \
  -H "Authorization: Bearer YOUR_API_KEY"

# 3. Create post
curl -X POST https://getlate.dev/api/v1/posts \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"content": "Hello!", "platforms": [{"platform": "twitter", "accountId": "ACC_ID"}], "publishNow": true}'
```

## 规则文件

如需详细文档，请阅读相应的规则文件：

- [rules/authentication.md](rules/authentication.md) - API密钥格式、使用示例、核心概念
- [rules/posts.md](rules/posts.md) - 创建、安排发布、重试发布、批量上传
- [rules/accounts.md](rules/accounts.md) - 列出账户信息、账户健康检查、粉丝统计
- [rules/connect.md](rules/connect.md) - OAuth流程、Bluesky应用密码、Telegram机器人令牌
- [rules/platforms.md](rules/platforms.md) - 所有13个平台的特定数据
- [rules/webhooks.md](rules/webhooks.md) - 配置Webhook、验证签名、事件处理
- [rules/media.md](rules/media.md) - 预签名上传、支持的格式、平台限制
- [rules/queue.md](rules/queue.md) - 队列管理、时间段配置
- [rules/analytics.md](rules/analytics.md) - YouTube每日观看次数、LinkedIn分析数据
- [rules/tools.md](rules/tools.md) - 媒体下载、标签检查工具、转录功能
- [rules/errors.md](rules/errors.md) - 错误代码、速率限制、发布日志
- [rules/sdks.md](rules/sdks.md) - 直接API使用示例

## 支持的平台

Twitter/X、Instagram、Facebook、LinkedIn、TikTok、YouTube、Pinterest、Reddit、Bluesky、Threads、Google Business、Telegram、Snapchat

---

*[Late](https://getlate.dev) - 专为开发者设计的社交媒体调度API*