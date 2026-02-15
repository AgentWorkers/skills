---
name: bluesky
version: 1.6.0
description: "完整的Bluesky CLI：发布内容、回复评论、点赞、重新发布、关注用户、屏蔽用户、静音用户、搜索信息、查看主题讨论、查看图片。这些功能都允许你通过终端与Bluesky进行交互。"
homepage: https://bsky.app
metadata:
  openclaw:
    emoji: "🦋"
    requires:
      bins: ["python3"]
    tags: ["social", "bluesky", "at-protocol", "cli"]
---

# Bluesky CLI

这是一个功能齐全的命令行界面（CLI），用于操作Bluesky/AT协议。

## 用户操作指南

**第一步：检查是否已登录**
```bash
bsky whoami
```

- 如果显示用户名（handle），则表示可以开始使用下面的命令；
- 如果显示“未登录”，则需要引导用户完成设置流程。

**常见操作：**
- “发布到Bluesky”：`bsky post "文本"`
- “查看我的时间线”：`bsky timeline`
- “点赞这条帖子”：`bsky like <链接>`
- “关注某人”：`bsky follow @用户名`

## 设置

如果用户尚未登录（`bsky whoami`显示“未登录”），请引导他们完成设置：

### 获取应用密码

告知用户：
> 访问 bsky.app → 点击个人头像 → 设置 → 隐私与安全 → 应用密码 → 添加应用密码。将密码命名为“OpenClaw”，并复制该密码（格式为 `xxxx-xxxx-xxxx-xxxx`）。此密码仅会显示一次！

### 登录

用户获取到应用密码后，运行以下命令：
```bash
bsky login --handle THEIR_HANDLE.bsky.social --password THEIR_APP_PASSWORD
```

示例：
```bash
bsky login --handle alice.bsky.social --password abcd-1234-efgh-5678
```

**安全提示：** 密码仅用于获取会话令牌，使用后立即丢弃，不会存储在磁盘上。会话会自动刷新。

## 快速参考

| 操作 | 命令 |
|--------|---------|
| 查看时间线 | `bsky timeline` 或 `bsky tl` |
| 发布内容 | `bsky post "文本"` |
| 发布带图片的内容 | `bsky post "文本" --image photo.jpg --alt "描述"` |
| 回复帖子 | `bsky reply <链接> "文本"` |
| 引用帖子 | `bsky quote <链接> "文本"` |
| 查看帖子讨论串 | `bsky thread <链接>` |
| 创建新帖子 | `bsky create-thread "帖子1" "帖子2" "帖子3"` 或 `bsky ct` |
- 点赞 | `bsky like <链接>` |
- 重新发布 | `bsky repost <链接>` |
- 关注 | `bsky follow @用户名` |
- 封禁 | `bsky block @用户名` |
- 静音 | `bsky mute @用户名` |
- 搜索 | `bsky search "查询"` |
- 查看通知 | `bsky notifications` 或 `bsky n` |
- 删除帖子 | `bsky delete <链接>` |

## 命令详解

### 时间线操作
```bash
bsky timeline              # 10 posts
bsky timeline -n 20        # 20 posts
bsky timeline --json       # JSON output
```

### 发布内容
```bash
bsky post "Hello world!"                           # Basic post
bsky post "Check this!" --image pic.jpg --alt "A photo"  # With image
bsky post "Test" --dry-run                         # Preview only
```

### 回复与引用帖子
```bash
bsky reply <post-url> "Your reply"
bsky quote <post-url> "Your take on this"
```

### 查看帖子讨论串
```bash
bsky thread <post-url>           # View conversation
bsky thread <url> --depth 10     # More replies
bsky thread <url> --json         # JSON output
```

### 创建新帖子
```bash
bsky create-thread "First post" "Second post" "Third post"   # Create a thread
bsky ct "Post 1" "Post 2" "Post 3"                           # Short alias
bsky create-thread "Hello!" "More thoughts" --dry-run         # Preview only
bsky create-thread "Look!" "Nice" --image pic.jpg --alt "A photo"  # Image on first post
```

### 互动操作
```bash
bsky like <post-url>             # ❤️ Like
bsky unlike <post-url>           # Remove like
bsky repost <post-url>           # 🔁 Repost (aliases: boost, rt)
bsky unrepost <post-url>         # Remove repost
```

### 社交图谱操作
```bash
bsky follow @someone             # Follow user
bsky unfollow @someone           # Unfollow user
bsky profile @someone            # View profile
bsky profile --json              # JSON output
```

### 管理操作
```bash
bsky block @someone              # 🚫 Block user
bsky unblock @someone            # Unblock
bsky mute @someone               # 🔇 Mute user
bsky unmute @someone             # Unmute
```

### 搜索与通知
```bash
bsky search "query"              # Search posts
bsky search "topic" -n 20        # More results
bsky notifications               # Recent notifications
bsky n -n 30                     # More notifications
```

### 删除帖子
```bash
bsky delete <post-url>           # Delete your post
bsky delete <post-id>            # By ID
```

## 结构化输出（JSON格式）

若需以JSON格式获取命令输出，可在命令后添加 `--json`：
```bash
bsky timeline --json
bsky search "topic" --json
bsky notifications --json
bsky profile @someone --json
bsky thread <url> --json
```

## 错误处理

| 错误信息 | 处理方法 |
|-------|-----|
| “会话过期” | 重新运行 `bsky login` |
| “未登录” | 运行 `bsky login --用户名 ... --密码 ...` |
| “帖子长度超过限制（最多300个字符）” | 缩短帖子内容 |
| “图片过大” | 使用大小小于1MB的图片 |

## 注意事项：

- 所有 `<链接>` 参数可以接受 `https://bsky.app/...` 或 `at://` 格式的网址；
- 如果未指定域名，系统会自动在链接后添加 `.bsky.social`；
- 图片帖子需要使用 `--alt` 参数以提高可访问性（Bluesky的要求）；
- 会话令牌会自动刷新，密码不会被存储在系统中。