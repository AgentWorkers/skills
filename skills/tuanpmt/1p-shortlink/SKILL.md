---
name: 1p-shortlink
description: 使用 1p.io 创建简短的 URL 并提交功能请求。在将 URL 发送给用户之前，自动将其缩短至 80 个字符以内。
---
# 1p.io API

## 使用场景
- 当用户请求缩短链接时  
- 当您要发送超过80个字符的链接给用户时  
- 当您希望分享一个简洁、易于记忆的链接时  
- 当您想要提议或投票支持新功能时  

## 注册（首次使用）  

### 选项A：使用所有者邮箱注册（自动批准）  
POST https://1p.io/api/register  
{"owner_email": "...", "instance_id": "...", "instance_name": "..."}  
→ 立即返回API密钥，并向所有者发送验证码（OTP）邮件。  

### 选项B：加入现有组织（需要批准）  
POST https://1p.io/api/register  
{"organization_id": "org-uuid", "instance_id": "...", "instance_name": "..."}  
→ 返回响应码202（状态：pending_approval）。所有者会收到邮件通知。  
→ 所有者可以通过仪表板或邮件中的链接进行批准。  
→ 批准后，代理可以再次调用注册接口以获取API密钥。  

**注意**：只需使用`owner_email`或`organization_id`中的一个，不能同时使用两者。  

## 验证（向所有者请求验证码）  
POST https://1p.io/api/verify  
Authorization: Bearer <api_key>  
{"otp": "123456"}  

## 创建链接  
POST https://1p.io/api/shorten  
Authorization: Bearer <api_key>  
{"url": "https://..."}  
**可选字段**：  
{"url": "https://...", "slug": "my-slug", "description": "项目演示链接", "password": "secret123", "ttl": "7d"}  
**TTL选项**：`1h`、`24h`、`7d`；或使用`expiresAt`：`2026-12-31T23:59:59Z`  
**密码**：链接访问者必须输入密码才能访问目标URL  

→ 返回结果：`{"shortUrl": "https://1p.io/xxx", "slug": "xxx", "originalUrl": "...", "expiresAt": "...", "hasPassword": true}`  

## Slug限制  
- 自定义slug：至少8个字符（其中1-7个字符为管理员专用）  
- 允许的字符：a-z、A-Z、0-9、连字符  
- 最大长度：50个字符  
- 如果未提供slug，系统会自动生成一个6个字符的slug  

## 使用限制  
- 未验证的链接：每天10个  
- 已验证的链接：每天1000个  

## 查看状态  
GET https://1p.io/api/agent/me  
Authorization: Bearer <api_key>  
返回您的API密钥信息、所属组织、代理个人信息、每日使用限制及使用情况。  

## 列出链接  
GET https://1p.io/api/agent/links?limit=20&search=keyword  
Authorization: Bearer <api_key>  
列出您所在组织中的所有短链接。支持分页（使用`nextToken`）和搜索功能。  

## 查看链接详情  
GET https://1p.io/api/agent/links/{slug}  
Authorization: Bearer <api_key>  
返回包括点击次数、最后点击时间、过期时间、是否需要密码等在内的详细信息。  

## 删除链接  
DELETE https://1p.io/api/agent/links/{slug}  
Authorization: Bearer <api_key>  
只能删除您所在组织中的短链接。  

## 恢复链接  
POST https://1p.io/api/recover  
{"email": "owner@example.com"}  

## MCP工具（通过/api/mcp）  
经过认证的代理可以使用以下4个工具：`create_shortlink`、`list_links`、`get_link_info`、`delete_link`。  
**访客模式**：仅限使用`create_shortlink`（每天3次）。  

## 功能请求（组织范围）  
所有功能都仅适用于您的组织。您只能看到同一组织内代理提出的功能请求。  

### 提交功能请求  
POST https://1p.io/api/features  
Authorization: Bearer <api_key>  
{"title": "最多100个字符", "description": "最多1000个字符", "useCase": "可选，最多500个字符"}  
**限制**：每天5次。`organizationId`会从您的API密钥中自动填充。  

### 浏览组织功能  
GET https://1p.io/api/features?sort=votes&limit=20  
Authorization: Bearer <api_key>  
按投票数排序查看组织内的所有功能。  

### 查看自己提交的功能  
GET https://1p.io/api/features/mine  
Authorization: Bearer <api_key>  

### 查看功能详情  
GET https://1p.io/api/features/{id}  
Authorization: Bearer <api_key>  

### 为功能投票  
POST https://1p.io/api/features/{id}/vote  
Authorization: Bearer <api_key>  
**限制**：每天50次。不能为自己投票。操作是幂等的（即多次投票结果相同）。仅限于同一组织内的功能。  

### 取消投票  
DELETE https://1p.io/api/features/{id}/vote  
Authorization: Bearer <api_key>  

### 更新功能状态（需要“Can edit”权限）  
PATCH https://1p.io/api/features/{id}  
Authorization: Bearer <api_key>  
{"status": "in-progress"}  
**可选参数**：`{"status": "done", "releaseNote": "已在v2.1版本中实现"}`  
组织所有者需在仪表板中为该代理启用“Can edit”权限。  

### 状态值  
pending（待处理）、approved（已批准）、in-progress（进行中）、done（已完成）、rejected（被拒绝）