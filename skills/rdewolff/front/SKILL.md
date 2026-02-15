---
name: front
description: Front.app API 用于管理对话、消息、评论以及团队协作功能。
homepage: https://front.com
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["curl"],"env":["FRONT_API_TOKEN"]},"primaryEnv":"FRONT_API_TOKEN"}}
---

# Front

使用 Front 的 API 来管理对话、发送/接收消息以及与团队成员进行协作。

## 设置

从 Front 的“设置”（Settings）→“开发者”（Developers）→“API 令牌”（API Tokens）中获取 API 令牌。将其保存在 `~/.clawdbot/clawdbot.json` 文件中：
```json
{
  "skills": {
    "entries": {
      "front": {
        "apiKey": "YOUR_FRONT_API_TOKEN"
      }
    }
  }
}
```

或者通过环境变量设置：`FRONT_API_TOKEN=your_token`

## 快速参考

### 列出收件箱中的消息
```bash
{baseDir}/scripts/front.sh inboxes
```

### 列出所有对话
```bash
{baseDir}/scripts/front.sh conversations [inbox_id]      # Active conversations (unassigned + assigned)
{baseDir}/scripts/front.sh conversations --all           # Include archived
{baseDir}/scripts/front.sh conversations --archived      # Archived only
{baseDir}/scripts/front.sh conversations --unassigned    # Unassigned only
{baseDir}/scripts/front.sh conversations --assigned      # Assigned only
{baseDir}/scripts/front.sh conversations --limit 200     # Increase result limit (default: 100)
```

### 获取对话详情
```bash
{baseDir}/scripts/front.sh conversation <conversation_id>
```

### 查看对话中的消息
```bash
{baseDir}/scripts/front.sh messages <conversation_id>
```

### 搜索对话
```bash
{baseDir}/scripts/front.sh search "query text"
{baseDir}/scripts/front.sh search "from:client@example.com"
{baseDir}/scripts/front.sh search "tag:urgent"
```

### 阅读评论（团队笔记）
```bash
{baseDir}/scripts/front.sh comments <conversation_id>
```

### 添加评论（团队笔记）
```bash
{baseDir}/scripts/front.sh add-comment <conversation_id> "Your team note here"
```

### 回复对话
```bash
{baseDir}/scripts/front.sh reply <conversation_id> "Your reply message"
# With --draft flag to save as draft instead of sending:
{baseDir}/scripts/front.sh reply <conversation_id> "Draft message" --draft
```

### 列出团队成员
```bash
{baseDir}/scripts/front.sh teammates
```

### 分配对话任务
```bash
{baseDir}/scripts/front.sh assign <conversation_id> <teammate_id>
```

### 为对话添加标签
```bash
{baseDir}/scripts/front.sh tag <conversation_id> <tag_id>
```

### 列出所有标签
```bash
{baseDir}/scripts/front.sh tags
```

### 获取联系信息
```bash
{baseDir}/scripts/front.sh contact <contact_id_or_handle>
```

### 查看草稿
```bash
{baseDir}/scripts/front.sh drafts [inbox_id]    # Search conversations for drafts
```
注意：Front API 没有专门用于查看草稿的端点。此命令会检查当前活跃的对话中是否有未发送的草稿回复。

## 常见工作流程

**每日收件箱审核：**
```bash
# List unassigned open conversations
{baseDir}/scripts/front.sh conversations --unassigned --status open
```

**查找与客户的对话：**
```bash
{baseDir}/scripts/front.sh search "from:customer@company.com"
```

**添加团队背景信息：**
```bash
{baseDir}/scripts/front.sh add-comment cnv_abc123 "Customer is VIP - handle with care"
```

## 注意事项

- **API 基础地址**：会自动检测（根据公司设置，例如 `https://company.api.frontapp.com`）
- **认证方式**：在请求头中传递 Bearer 令牌
- **请求速率限制**：每分钟 120 次请求
- **对话 ID** 以 `cnv_` 开头
- **收件箱 ID** 以 `inb_` 开头
- 在发送回复前请务必确认信息

## API 限制

- **无全局搜索功能**：`/conversations/search` 端点可能会根据 API 计划的不同返回 404 错误
- **无全局草稿功能**：草稿信息是按对话单独存储的，无法全局访问
- **对话与收件箱的区别**：默认显示未归档/未删除的对话（即未关闭、未分配或已分配的对话）