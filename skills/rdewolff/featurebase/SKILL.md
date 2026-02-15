---
name: featurebase
description: Featurebase API 用于处理客户反馈、功能请求、变更日志和支持相关事务。该 API 可用于管理用户反馈、跟踪功能投票结果、响应支持请求，以及发布变更日志更新。
---

# 特性管理平台（Featurebase）

这是一个用于处理特性请求、支持请求以及变更日志的客户反馈平台。

## 设置

从 Featurebase 获取您的 API 密钥：
1. 进入“设置”（Settings） → “API”（API）。
2. 复制您的 API 密钥。

将密钥保存到 `~/.clawdbot/clawdbot.json` 文件中：
```json
{
  "skills": {
    "entries": {
      "featurebase": {
        "apiKey": "YOUR_API_KEY",
        "orgSubdomain": "whisperit"
      }
    }
  }
}
```

或者通过环境变量设置：`FEATUREBASE_API_KEY=xxx` 和 `FEATUREBASE_ORG=whisperit`。

## 快速参考

### 发布内容（特性请求与反馈）
```bash
{baseDir}/scripts/featurebase.sh posts list                     # List all posts
{baseDir}/scripts/featurebase.sh posts list --status open       # Filter by status
{baseDir}/scripts/featurebase.sh posts list --board feedback    # Filter by board
{baseDir}/scripts/featurebase.sh posts show <id>                # Get post details
{baseDir}/scripts/featurebase.sh posts create --title "Title" --content "Description" --board feedback
{baseDir}/scripts/featurebase.sh posts update <id> --status "in-progress"
{baseDir}/scripts/featurebase.sh posts comment <id> --content "Reply text"
```

### 支持/帮助台
```bash
{baseDir}/scripts/featurebase.sh support list                   # List support tickets
{baseDir}/scripts/featurebase.sh support list --status open     # Open tickets only
{baseDir}/scripts/featurebase.sh support show <id>              # Ticket details
{baseDir}/scripts/featurebase.sh support reply <id> --content "Response"
{baseDir}/scripts/featurebase.sh support close <id>             # Close ticket
```

### 变更日志
```bash
{baseDir}/scripts/featurebase.sh changelog list                 # List entries
{baseDir}/scripts/featurebase.sh changelog create --title "v2.0" --content "Release notes..."
{baseDir}/scripts/featurebase.sh changelog publish <id>         # Publish draft
```

### 用户信息
```bash
{baseDir}/scripts/featurebase.sh users list                     # List users
{baseDir}/scripts/featurebase.sh users search "email@example.com"
{baseDir}/scripts/featurebase.sh users show <id>                # User details + activity
```

### 特性管理板（Feature Management Boards）
```bash
{baseDir}/scripts/featurebase.sh boards list                    # List all boards
```

## 发布内容的状态
- `open` - 新发布/可供投票
- `under-review` - 正在审核中
- `planned` - 已计划开发
- `in-progress` - 正在开发中
- `complete` - 已完成
- `closed` - 不再支持/已关闭

## 常见工作流程

### 回复热门特性请求
```bash
# Find top-voted open requests
{baseDir}/scripts/featurebase.sh posts list --status open --sort votes

# Add a status update
{baseDir}/scripts/featurebase.sh posts update <id> --status planned
{baseDir}/scripts/featurebase.sh posts comment <id> --content "We're planning this for Q1!"
```

### 处理支持请求队列
```bash
# List open tickets
{baseDir}/scripts/featurebase.sh support list --status open

# Reply to a ticket
{baseDir}/scripts/featurebase.sh support reply <id> --content "Thanks for reaching out..."

# Close resolved tickets
{baseDir}/scripts/featurebase.sh support close <id>
```

## 注意事项

- API 基础地址：`https://do.featurebase.app/v2`
- 认证方式：通过 `Authorization` 头部传递令牌（Bearer token）
- 组织子域名：您的 Featurebase 子域名（例如：`whisperit.featurebase.app`）
- 速率限制：请参考 Featurebase 的官方文档了解当前的限制规定
- 在修改或关闭工单之前，请务必确认相关信息。