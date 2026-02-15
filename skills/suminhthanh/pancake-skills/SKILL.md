---
name: pancake-skills
description: 与Pancake Platform API进行交互，以管理页面（pages）、对话（conversations）、消息（messages）、客户（customers）、统计数据（statistics）、标签（tags）、帖子（posts）和用户（users）。使用该API可完成以下操作：  
1. 管理页面并生成访问令牌（access token）；  
2. 处理对话和消息；  
3. 管理客户信息；  
4. 查看统计数据和分析结果；  
5. 管理标签和帖子；  
6. 管理用户/员工；  
7. 上传媒体内容；  
8. 操作聊天插件（chat plugin）。
---

# pancake-skills

## 目标

本技能提供了与Pancake Platform API交互的能力——这是一个多渠道销售管理平台。它支持以下所有操作：

- **页面（Pages）**：列出页面、生成页面访问令牌
- **对话（Conversations）**：管理对话、添加标签、分配工作人员、标记为已读/未读
- **消息（Messages）**：获取消息历史记录、发送消息（收件箱、回复评论、私信）
- **客户（Customers）**：管理客户、添加/修改/删除备注
- **统计信息（Statistics）**：统计广告效果、用户互动情况、页面数据、标签使用情况、用户信息
- **标签（Tags）**：列出页面的标签
- **帖子（Posts）**：列出帖子内容
- **用户（Users）**：管理工作人员、配置轮询机制
- **上传（Upload）**：上传媒体内容
- **聊天插件（Chat Plugin）**：通过聊天插件发送消息

## 环境设置（必填）

**用户API**（端点 `/api/v1/pages`）：
- `USER_ACCESS_TOKEN`：个人访问令牌，可从**账户 → 个人设置**中获取。有效期为90天。

**页面API**（端点 `/api/public_api/v1` 和 `/api/public_api/v2`）：
- `PAGE_ACCESS_TOKEN`：页面访问令牌，可从**设置 → 工具**中获取。除非被删除或更新，否则永久有效。

**可选设置**：
- `PANCAKE_BASE_URL`：默认值为 `https://pages.fm`
- `CONFIRM_WRITE`：设置为 `YES` 以允许写入操作（POST/PUT/DELETE）

## 快速调用方式

推荐使用脚本：`scripts/pancake.sh`

### 示例（GET请求）

```bash
# Liệt kê pages (User API)
export USER_ACCESS_TOKEN="***"
bash scripts/pancake.sh pages-list

# Liệt kê conversations của page (Page API)
export PAGE_ACCESS_TOKEN="***"
bash scripts/pancake.sh conversations-list 123456789

# Lọc conversations theo tags và type
bash scripts/pancake.sh conversations-list 123456789 "?tags=1,2&type=INBOX"

# Lấy tin nhắn trong conversation
bash scripts/pancake.sh messages-list 123456789 conv_abc123

# Liệt kê tags
bash scripts/pancake.sh tags-list 123456789

# Liệt kê staff
bash scripts/pancake.sh users-list 123456789

# Thống kê page (SINCE/UNTIL là Unix timestamp)
bash scripts/pancake.sh stats-page 123456789 1704067200 1706745600
```

### 示例（POST请求）

```bash
export PAGE_ACCESS_TOKEN="***"
export CONFIRM_WRITE=YES

# Gửi tin nhắn inbox
echo '{"action":"reply_inbox","message":"Xin chào!"}' | \
  bash scripts/pancake.sh messages-send 123456789 conv_abc123

# Gửi tin nhắn với attachment (dùng content_ids từ upload API)
echo '{"action":"reply_inbox","content_ids":["xxx"]}' | \
  bash scripts/pancake.sh messages-send 123456789 conv_abc123

# Reply comment
echo '{"action":"reply_comment","message_id":"comment123","message":"Cảm ơn bạn!"}' | \
  bash scripts/pancake.sh messages-send 123456789 conv_abc123

# Private reply từ comment
echo '{"action":"private_replies","post_id":"post123","message_id":"comment123","message":"Inbox nhé!"}' | \
  bash scripts/pancake.sh messages-send 123456789 conv_abc123

# Thêm tag vào conversation
echo '{"action":"add","tag_id":"123"}' | \
  bash scripts/pancake.sh conversations-tag 123456789 conv_abc123

# Gỡ tag khỏi conversation
echo '{"action":"remove","tag_id":"123"}' | \
  bash scripts/pancake.sh conversations-tag 123456789 conv_abc123

# Assign staff vào conversation
echo '{"assignee_ids":["user-uuid-1","user-uuid-2"]}' | \
  bash scripts/pancake.sh conversations-assign 123456789 conv_abc123

# Đánh dấu conversation đã đọc
bash scripts/pancake.sh conversations-read 123456789 conv_abc123

# Cập nhật thông tin khách hàng
echo '{"changes":{"name":"Nguyễn Văn A","gender":"male","birthday":"1990-01-15"}}' | \
  bash scripts/pancake.sh customers-update 123456789 customer_uuid

# Thêm ghi chú cho khách hàng
echo '{"message":"Khách hàng VIP, ưu tiên hỗ trợ"}' | \
  bash scripts/pancake.sh customers-add-note 123456789 customer_uuid

# Upload file
bash scripts/pancake.sh upload 123456789 /path/to/image.jpg

# Cập nhật round robin users
echo '{"inbox":["user-uuid-1"],"comment":["user-uuid-2"]}' | \
  bash scripts/pancake.sh users-round-robin 123456789
```

## 安全限制

- 在未设置 `CONFIRM_WRITE`=YES` 时，禁止写入数据
- 在执行写入操作前，必须先执行一次 GET 请求以确认数据的ID和格式
- 禁止将访问令牌保存到仓库中
- **重要提示**：在发送消息时，`message` 和 `content_ids` 是**互斥的**——不能同时发送这两个参数

## 本技能涉及的端点

### 用户API (`https://pages.fm/api/v1`)
- `GET /pages`：列出所有页面
- `POST /pages/{page_id}/generate_page_access_token`：生成页面访问令牌

### 页面API v2 (`https://pages.fm/api/public_api/v2`)
- `GET /pages/{page_id}/conversations`：列出所有对话记录

### 页面API v1 (`https://pages.fm/api/public_api/v1`)

**对话（Conversations）**：
- `POST /pages/{page_id}/conversations/{conversation_id}/tags`：添加/删除标签
- `POST /pages/{page_id}/conversations/{conversation_id}/assign`：分配工作人员
- `POST /pages/{page_id}/conversations/{conversation_id}/read`：标记为已读
- `POST /pages/{page_id}/conversations/{conversation_id}/unread`：标记为未读

**消息（Messages）**：
- `GET /pages/{page_id}/conversations/{conversation_id}/messages`：获取消息内容
- `POST /pages/{page_id}/conversations/{conversation_id}/messages`：发送消息

**客户（Customers）**：
- `GET /pages/{page_id}/page_customers`：列出所有客户
- `PUT /pages/{page_id}/page_customers/{page_customer_id}`：更新客户信息
- `POST /pages/{page_id}/page_customers/{page_customer_id}/notes`：添加备注
- `PUT /pages/{page_id}/page_customers/{page_customer_id}/notes`：修改备注
- `DELETE /pages/{page_id}/page_customers/{page_customer_id}/notes`：删除备注

**统计信息（Statistics）**：
- `GET /pages/{page_id}/statistics/pages_campaigns`：获取广告活动统计
- `GET /pages/{page_id}/statistics/ads`：获取广告统计
- `GET /pages/{page_id}/statistics/customer_engagements`：获取用户互动统计
- `GET /pages/{page_id}/statistics/pages`：获取页面统计
- `GET /pages/{page_id}/statistics/tags`：获取标签使用统计
- `GET /pages/{page_id}/statistics/users`：获取用户统计

**其他操作**：
- `GET /pages/{page_id}/tags`：列出页面标签
- `GET /pages/{page_id}/posts`：列出所有帖子
- `GET /pages/{page_id}/users`：列出所有用户
- `POST /pages/{page_id}/round_robin_users`：更新轮询配置
- `GET /pages/{page_id}/sip_call_logs`：获取通话记录
- `GET /pages/{page_id}/export_data`：导出数据
- `POST /pages/{page_id}/upload_contents`：上传媒体文件

### 聊天插件（Chat Plugin） (`https://pages.fm/api/v1`)
- `POST /pke_chat_plugin/messages`：通过聊天插件发送消息
- `GET /pke_chat_plugin/messages`：获取聊天插件中的消息记录

## 参考资料

- OpenAPI 规范：`references/openapi-pancake.yaml`
- 详细参数和响应格式请参阅OpenAPI文档。