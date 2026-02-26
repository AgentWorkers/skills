---
name: repliz
description: Repliz 社交媒体管理 API 集成：在使用 Repliz 管理社交媒体账户、日程安排和评论时可以使用该功能。需要 `REPLIZ_ACCESS_KEY` 和 `REPLIZ_SECRET_KEY` 环境变量。
homepage: https://repliz.com
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":["curl"],"env":["REPLIZ_ACCESS_KEY","REPLIZ_SECRET_KEY"]},"primaryEnv":"REPLIZ_ACCESS_KEY"}}
---
# Repliz API 技能

## 先决条件与设置

在使用此技能之前，您必须完成以下设置步骤：

### 1. 注册/登录 Repliz
- **注册**：访问 https://repliz.com/register 创建新账户
- **登录**：访问 https://repliz.com/login 登录您的现有账户

### 2. 连接社交媒体账户
登录后，连接您的社交媒体账户：
- 进入您的 Repliz 仪表板
- 添加并连接诸如 **Instagram**、**Threads**、**TikTok**、**Facebook**、**LinkedIn** 或 **YouTube** 等账户
- 确保账户显示为“已连接”状态后再继续下一步

### 3. 获取 API 凭据
要获取用于基本身份验证的访问密钥（Access Key）和秘密密钥（Secret Key）：
1. 访问 https://repliz.com/user/setting/api
2. 生成或复制您的 **访问密钥** 和 **秘密密钥**
3. 安全存储这些凭据——它们用于发布、删除和管理您的社交媒体内容

### 4. 配置环境变量
此技能需要设置以下环境变量：

```json
{
  "title": "",
  "description": "您的帖子内容",
  "type": "text",
  "medias": [],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e"
}
```

```json
{
  "title": "",
  "description": "标题",
  "type": "图片",
  "medias": [{"type": "图片", "缩略图": "图片链接", "链接": "图片链接", "alt": "描述"}],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e"
}
```

```json
{
  "title": "你好，这是来自 Repliz 的消息",
  "description": "你好，这是来自 Repliz 的消息",
  "type": "视频",
  "medias": [
    {
      "type": "视频",
      "缩略图": "视频缩略图链接",
      "链接": "视频链接"
    }
  ],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e"
}
```

```json
{
  "title": "你好，这是来自 Repliz 的消息",
  "description": "你好，这是来自 Repliz 的消息",
  "type": "相册",
  "medias": [
    {
      "type": "图片",
      "缩略图": "缩略图链接-1",
      "链接": "图片链接-1",
      "alt": "图片描述-1"
    },
    {
      "type": "图片",
      "缩略图": "缩略图链接-2",
      "链接": "图片链接-2",
      "alt": "图片描述-2"
    },
    {
      "type": "图片",
      "缩略图": "缩略图链接-99",
      "链接": "图片链接-99",
      "alt": "图片描述-99"
    }
  ],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e"
}
```

```json
{
  "title": "",
  "description": "您的帖子内容",
  "type": "故事",
  "medias": [
    {
      "type": "图片或视频" // 您可以选择
      "缩略图": "缩略图链接",
      "链接": "媒体链接"
    }
  ],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e"
}
```

```json
{
  "title": "你好，这是来自 Repliz 的消息",
  "description": "你好，这是来自 Repliz 的消息",
  "type": "视频",
  "medias": [
    {
      "type": "视频",
      "缩略图": "视频缩略图链接",
      "链接": "视频链接"
    }
  ],
  "additionalInfo": {
    "合作者": [
      "usernameCollab1",
      "usernameCollab2",
      "usernameCollab3"
    ]
  },
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e"
}
```

```json
{
  "title": "第一篇帖子",
  "description": "",
  "medias": [],
  "scheduleAt": "2026-02-14T10:35:09.658Z",
  "accountId": "680affa5ce12f2f72916f67e",
  "回复": [
    {"title": "", "描述": "第二篇帖子的回复", "type": "文本", "medias": []},
    {"title": "", "描述": "第三篇帖子的回复", "type": "文本", "medias": []}
  ]
}
```

```json
{
  "text": "您的回复"
}
```

## 错误处理
- `401`：无效的授权头
- `404`：未找到
- `500`：内部服务器错误

## 注意事项
- 发布内容时使用的 `accountId` 来自账户列表中的 `_id` 字段
- `scheduleAt` 使用 ISO 8601 格式表示时间（例如：`2026-02-14T10:35:09.658Z`）
- 队列状态可以是：待处理（pending）、已解决（resolved）或被忽略（ignored）