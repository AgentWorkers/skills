---
name: publora-mastodon
description: 使用 Publora API 在 Mastodon 上发布或安排内容发布。当用户希望通过 Publora 在 Mastodon 上发布或安排内容发布时，可以使用此技能。
---
# Publora — Mastodon

通过 Publora API 发布和安排 Mastodon 内容。

> **先决条件：** 需要安装 `publora` 核心技能，以便进行身份验证设置和获取平台 ID。

## 获取您的 Mastodon 平台 ID

```bash
GET https://api.publora.com/api/v1/platform-connections
# Look for entries like "mastodon-instance_social"
```

## 立即发布到 Mastodon

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Just launched something new on the open web 🎉 #fediverse #opensource',
    platforms: ['mastodon-instance_social']
  })
});
```

## 安排 Mastodon 发布内容

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Weekly update: here\'s what the team shipped #buildinpublic #indiedev',
    platforms: ['mastodon-instance_social'],
    scheduledTime: '2026-03-16T10:00:00.000Z'
  })
});
```

## Mastodon 使用技巧：

- **字符限制为 500 个**（具体数量可能因实例而异，但 500 个是标准值）
- **去中心化**：您的账户存储在一个实例上，但可以在整个网络中跨多个实例使用
- **标签（Hashtags）非常重要**：由于没有推荐算法，Mastodon 依赖标签来帮助用户发现内容
- **对于敏感话题，内容警告（Content Warnings, CW）是文化惯例**
- **技术导向的社区**：包括开发者、隐私保护倡导者和开源爱好者
- **推荐的标签**：`#fediverse`、`#opensource`、`#indiedev`、`#buildinpublic`
- **不抑制链接**：分享 URL 是非常有效的传播方式