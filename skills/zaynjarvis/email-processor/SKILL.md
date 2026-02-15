---
name: email-processor
description: |
  Automate Gmail inbox processing - categorizes unread emails, marks marketing/newsletters/promotions as read, and surfaces important emails requiring attention.
  
  USE WHEN: User asks to "check my emails", "process unread emails", "clean up my inbox", "mark newsletters as read", or any Gmail automation task.
  
  REQUIRES: gog CLI (brew install steipete/tap/gogcli) + Google Cloud OAuth credentials
---

# 电子邮件处理器

该工具通过自动分类未读邮件并将低优先级的邮件标记为已读，来帮助您更高效地管理Gmail收件箱。

## 功能概述

1. 获取所有未读邮件。
2. 识别营销邮件、新闻通讯、促销信息以及普通邮件。
3. 将低优先级的邮件标记为已读。
4. 突出显示重要邮件（如GitHub通知、安全警报和直接发送的私人邮件）。
5. 生成汇总报告。

## 先决条件

### 1. 安装 gog CLI

```bash
brew install steipete/tap/gogcli
```

验证安装是否成功：
```bash
gog --version
```

### 2. 设置 Google Cloud OAuth 访问权限

1. 访问 [Google Cloud 控制台](https://console.cloud.google.com/)。
2. 创建一个新的项目（或使用现有项目）。
3. 启用 Gmail API：
   - 转到“APIs & Services” > “Library”。
   - 搜索“Gmail API”并启用它。
4. 创建 OAuth 凭据：
   - 转到“APIs & Services” > “Credentials”。
   - 点击“Create Credentials” > “OAuth client ID”。
   - 选择“Desktop app”作为应用类型。
   - 下载 JSON 凭据文件。

### 3. 对 gog 进行身份验证

```bash
# Set credentials
gog auth credentials /path/to/client_secret.json

# Add your Gmail account
gog auth add your@gmail.com --services gmail

# Verify
gog auth list
```

## 使用方法

### 快速使用流程

```bash
bash ~/.openclaw/workspace/skills/email-processor/scripts/process-emails.sh
```

### 手动处理（通过 Codex）

1. **获取未读邮件：**
   ```bash
   gog gmail search 'is:unread' --json --max 100
   ```

2. **将特定邮件标记为已读：**
   ```bash
   gog gmail thread modify <thread-id> --remove UNREAD --force
   ```

3. **批量标记营销邮件：**
   ```bash
   gog gmail search 'is:unread' --json --max 100 | \
     jq -r '.threads[] | select(.labels | contains(["CATEGORY_PROMOTIONS"])) | .id' | \
     while read id; do gog gmail thread modify "$id" --remove UNREAD --force; done
   ```

## 邮件分类

### 自动标记为已读的邮件类别

- `CATEGORY_PROMOTIONS` - 促销邮件
- `[Superhuman]/AI/News` - 新闻通讯
- `[Superhuman]/AI/Marketing` - 营销邮件
- `[Superhuman]/AI/Pitch` - 冷 Outreach（主动推广）邮件
- `[Superhuman]/AI/AutoArchived` - 自动分类为低优先级的邮件

### 保留的重要邮件类别

- GitHub 通知（拉取请求、问题、安全警报）
- 直接发送的私人邮件
- 金融/交易相关邮件
- 安全警报
- 日历邀请

## 验证功能是否正常

检查设置是否正确：
```bash
# Test gog connectivity
gog gmail search 'is:unread' --max 5

# Check account
gog auth list

# Test modify (dry run - just list what would be marked)
gog gmail search 'is:unread' --json --max 10 | \
  jq -r '.threads[] | select(.labels | contains(["CATEGORY_PROMOTIONS"])) | {id: .id, subject: .subject}'
```

## 常见问题及解决方法

| 问题 | 解决方案 |
|-------|----------|
| `gog: 命令未找到` | 运行 `brew install steipete/tap/gogcli` |
| 需要身份验证 | 运行 `gog auth credentials` 和 `gog auth add` |
| 令牌过期 | 运行 `gog auth refresh your@gmail.com` |
| Gmail API 未启用 | 在 [Google Cloud 控制台](https://console.cloud.google.com/apis/library/gmail.googleapis.com) 中启用该 API |
| 请求速率限制错误 | 增加请求间隔或减少批量处理的数量 |

## 邮件标签说明

Gmail 会自动应用以下标签：

- `CATEGORY_PERSONAL` - 个人邮件
- `CATEGORY_SOCIAL` - 社交媒体通知
- `CATEGORY_PROMOTIONS` - 促销邮件
- `CATEGORY_UPDATES` - 更新/通知邮件
- `CATEGORY_FORUMS` - 论坛消息
- `IMPORTANT` - 被标记为重要的邮件
- `UNREAD` - 未读状态

（如果使用 Superhuman AI 服务，还会应用以下标签：）

- `[Superhuman]/AI/News` - 新闻通讯
- `[Superhuman]/AI/Marketing` - 营销邮件
- `[Superhuman]/AI/Pitch` - 主动推广邮件
- `[Superhuman]/AI/AutoArchived` - 自动归档的邮件