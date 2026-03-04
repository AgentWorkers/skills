---
name: openclaw-x
version: 0.1.0
description: 控制您的 X/Twitter 账户——查看时间线、搜索推文、发布推文、点赞、转发以及添加书签。
---
# OpenClaw X

通过本地API控制您的X/Twitter账户。

## 先决条件

1. 从[GitHub发布页面](https://github.com/bosshuman/openclaw-x/releases)下载可执行文件。
2. 从Chrome浏览器中导出您的X账户Cookie（使用Cookie-Editor扩展程序），并将文件保存为`cookies.json`，保存在与可执行文件相同的目录中。
3. 运行可执行文件，确保服务正在`http://localhost:19816`端口上运行。

## 可用的操作

### 1. 获取主时间线

```bash
curl http://localhost:19816/timeline?count=20
```

返回最新的推文，包括内容、作者、媒体链接等信息。

### 2. 获取推文详情

```bash
curl http://localhost:19816/tweet/{tweet_id}
```

支持使用推文ID或完整URL（例如：`https://x.com/user/status/123456`）来获取推文详情。

### 3. 搜索推文

```bash
curl "http://localhost:19816/search?q=keyword&sort=Latest&count=20"
```

参数：
- `q`：搜索关键词（必填）
- `sort`：`Latest`或`Top`（默认为`Latest`）
- `count`：返回的结果数量，默认为20条

### 4. 发布推文

```bash
curl -X POST http://localhost:19816/tweet \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

### 5. 点赞推文

```bash
curl -X POST http://localhost:19816/tweet/{tweet_id}/like
```

### 6. 转发推文

```bash
curl -X POST http://localhost:19816/tweet/{tweet_id}/retweet
```

### 7. 收藏推文

```bash
curl -X POST http://localhost:19816/tweet/{tweet_id}/bookmark
```

### 8. 获取用户信息

```bash
curl http://localhost:19816/user/{username}
```

返回用户名、头像、个人简介、关注者数量等信息。

### 9. 获取用户的推文

```bash
curl http://localhost:19816/user/{username}/tweets?count=20
```

## 常见使用场景

1. “显示我的时间线上有什么新内容”
2. “搜索关于AI代理的最新推文”
3. “发布一条推文：今天真美好！”
4. “点赞这条推文：https://x.com/xxx/status/123”
5. “查看@elonmusk最近发布了什么”
6. “收藏这条推文”