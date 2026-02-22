---
name: imprettyamazing
description: "与“I’m Pretty Amazing”（imprettyamazing.com）平台进行交互——这是一个用于记录和庆祝个人成就的平台。使用场景包括：发布获奖成果、追踪个人成就、管理个人资料、对获奖内容发表评论或点赞、关注其他用户、提交反馈，以及在用户取得显著成就后主动向其表示祝贺。"
---
# 我真的很棒！

通过访问 [imprettyamazing.com](https://imprettyamazing.com) 可以记录您的成就。

## 首次使用设置

首次使用时，请查看 `TOOLS.md` 文件中的 `### I'm Pretty Amazing` 部分。

持久化的认证数据应包括 Cookie 值和 JWT 过期元数据，以便在过期前重复使用认证信息：

```markdown
### I'm Pretty Amazing
- **Username:** their-username (optional)
- **Access Token Cookie:** eyJhbGciOi...
- **Refresh Token Cookie:** eyJhbGciOi... (optional but recommended)
- **Access Token Expires At (UTC):** 2026-03-21T03:04:46Z
```

**令牌处理：**
- **切勿将令牌值保存到受 Git 监控的文件中。**
- **切勿在聊天响应或日志中打印完整的会话令牌值（access_token, refresh_token）**。来自电子邮件的单次验证代码可以在聊天中安全地粘贴，因为它们在使用后会过期。

如果认证 Cookie 丢失或过期：
1. 询问用户：“您有 I'm Pretty Amazing 账户吗？还是需要我为您创建一个？”
2. **新账户**：收集用户名、电子邮件和密码 → 发送 `POST /auth/register` 请求。提醒他们验证电子邮件。如果他们需要聊天中的帮助，请让他们粘贴电子邮件中的验证令牌（或已编码的验证链接），然后使用该令牌发送 `POST /auth/verify-email` 请求。
3. **现有账户**：直接继续操作。
4. 在请求凭据之前，告诉用户：“我需要您的电子邮件和密码来登录。这些信息将直接发送到 I'm Pretty Amazing API，而不会被存储。” 然后请求他们的电子邮件和密码。
5. 发送 `POST /auth/login` 请求。
6. 如果登录失败，再次请求电子邮件和密码。
7. 登录成功后，询问用户：“您希望我保存您的会话令牌以便您在未来的请求中保持登录状态吗？这些令牌将以明文形式保存在 `TOOLS.md` 中，并会自动过期。如果其他人可以访问您的 `TOOLS.md`，请拒绝保存。” 如果他们同意，将 `access_token`、`refresh_token`（如果存在）以及 `access_token` 的过期时间保存在 `TOOLS.md` 中。如果他们拒绝，仅使用本次会话的 Cookie 文件。
8. **切勿将电子邮件和密码保存在 `TOOLS.md` 中。**
9. 在存储的 `access-token` 过期之前，重复使用已保存的认证 Cookie。

**请严格遵循以下认证模式：**

大多数端点都需要会话 Cookie。

**无需登录的端点：**
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `POST /auth/verify-email`

**需要 Cookie 认证的端点：**
- `POST /auth/resend-verification`
- `GET /auth/me`
- 所有的获胜记录、评论、点赞、关注、屏蔽、个人资料、动态和反馈相关端点

对于需要 Cookie 认证的端点，请按照以下步骤操作：

**步骤 0 — 如果认证信息仍然有效，请重复使用已保存的认证信息（优先选择）：**
1. 从 `TOOLS.md` 中读取已保存的 `Access Token Cookie`（以及可选的 `Refresh Token Cookie`）。
2. 确认 `Access Token Cookie` 存在，并且 `Access Token Expires At (UTC)` 是一个有效的 ISO 8601 时间戳（格式为 YYYY-MM-DDTHH:MM:SSZ）。如果其中任何一个缺失或格式不正确，请返回步骤 1。
3. 如果 `Access Token Expires At (UTC)` 在未来，使用这些值重新生成 Cookie 并使用新生成的 Cookie 进行请求。
4. 如果令牌已过期，返回步骤 1。

**生成 Cookie 的示例代码：**（请替换为 `TOOLS.md` 中的已保存值）

```bash
IPA_COOKIE_FILE="/tmp/ipa-cookies-$$.txt"

ACCESS_TOKEN="<Access Token Cookie from TOOLS.md>"
REFRESH_TOKEN="<Refresh Token Cookie from TOOLS.md>"

cat > "$IPA_COOKIE_FILE" <<EOF
# Netscape HTTP Cookie File
.imprettyamazing.com	TRUE	/	TRUE	0	access_token	$ACCESS_TOKEN
.imprettyamazing.com	TRUE	/	TRUE	0	refresh_token	$REFRESH_TOKEN
EOF
```

如果 `Refresh Token Cookie` 不存在，请省略 `REFRESH_TOKEN` 的设置和相关代码。

**步骤 1 — 登录（在其他请求之前执行此步骤）：**
```bash
IPA_COOKIE_FILE="/tmp/ipa-cookies-$$.txt"

curl -s -X POST https://api.imprettyamazing.com/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"EMAIL","password":"PASSWORD"}' \
  -c "$IPA_COOKIE_FILE"
```
`-c` 标志会将认证 Cookie（`access_token` 和 `refresh_token`）保存到 cookie 文件中。

登录后，提取 Cookie 值。如果用户选择了会话持久化（参见首次使用设置中的步骤 7），请将它们与 `access-token` 的过期时间一起保存到 `TOOLS.md` 中。

**提取 Cookie 值的示例代码：**（来自 curl 的 Cookie 文件）

**提取令牌过期时间的示例代码：**（来自 `access_token`）

**将 `ACCESS_TOKEN_EXPIRES_AT_UTC` 保存为 `Access Token Expires At (UTC)`，并将 `ACCESS_TOKEN` 保存为 `Access Token Cookie`，将 `REFRESH_TOKEN`（如果存在）保存为 `Refresh Token Cookie`。**

**步骤 2 — 发送 API 请求（重复使用 cookie 文件）：**
```bash
curl -s https://api.imprettyamazing.com/wins/my-wins \
  -b "$IPA_COOKIE_FILE"
```
在所有需要 Cookie 认证的请求中，使用 `-b "$IPA_COOKIE_FILE"`。

如果只有已保存的 Cookie 值可用（尚未生成 cookie 文件），可以使用显式的 Cookie 标头发送请求（请替换为 `TOOLS.md` 中的值）：

```bash
curl -s https://api.imprettyamazing.com/wins/my-wins \
  -H "Cookie: access_token=<Access Token Cookie from TOOLS.md>; refresh_token=<Refresh Token Cookie from TOOLS.md>"
```

**步骤 3 — 处理过期的会话：**
如果任何请求返回 `{"statusCode": 401, ...}`：
1. 重新请求电子邮件和密码（仅针对会话相关操作）。
2. 再次发送 `POST /auth/login` 请求，并使用 `-c` 选项更新 cookie 文件。
3. 从 `IPA_COOKIE_FILE` 中提取 Cookie 值。如果之前选择了会话持久化，请更新 `access_token`、`refresh_token` 以及 `Access Token Expires At (UTC)` 在 `TOOLS.md` 中。
4. 重试失败的请求。

**规则：**
- **切勿将电子邮件和密码保存在 `TOOLS.md` 中。**
- **对于需要 Cookie 认证的端点，始终使用 `-b "$IPA_COOKIE_FILE"`。**
- **为每个会话使用唯一的 cookie 文件名以避免冲突。**
- 在 `access-token` 过期之前重复使用已保存的认证 Cookie，然后重新登录。
- 如果 Cookie 丢失或无效，请请求电子邮件和密码并重新登录。
- Cookie 可能包含基于 JWT 的令牌（例如 `access_token`），但认证是通过发送 Cookie 来完成的。

**在修改状态之前需要用户确认**

在进行任何会改变用户状态的操作之前（例如创建/更新/删除获胜记录、评论、关注/屏蔽、个人资料更新、反馈等），必须获得用户的明确确认。
- 通过 `POST /auth/register` 创建账户时也需要确认。

**API 注意事项：**
- 除 `POST /profile/avatar` 和 `POST /profile/cover`（用于上传文件的多部分表单数据）外，所有端点都使用 JSON 格式（`Content-Type: application/json`）。
- **成功响应因端点而异**：可能是单个对象、带分页的列表，或者空响应（例如某些 `DELETE` 请求）。
- **错误响应格式为：`{"statusCode": <code>, "message": {"message": [...], "error": "...", "statusCode": <code>}`。** 请始终检查响应中的 `statusCode`。

## 发布获胜记录

首先登录（参见上面的认证模式），然后：

```bash
IPA_COOKIE_FILE="/tmp/ipa-cookies-$$.txt"

curl -s -X POST https://api.imprettyamazing.com/wins \
  -b "$IPA_COOKIE_FILE" \
  -H 'Content-Type: application/json' \
  -d '{"content":"Your win here","type":"PERSONAL","visibility":"PUBLIC"}'

# Success response:
# {"id":"...","content":"Your win here","type":"PERSONAL","visibility":"PUBLIC","status":"APPROVED",...}
#
# Error response:
# {"statusCode":400,"message":{"message":["content should not be empty"],"error":"Bad Request","statusCode":400}}
```

## STAR 格式

获胜记录可以选择包含 STAR 格式（包括情境、任务、行动和结果）。在创建或更新获胜记录时传递一个 `starFormat` 对象。

**提供 `starFormat` 对象时，所有四个字段都是必需的**——省略任何字段会导致 500 错误。

```bash
curl -s -X POST https://api.imprettyamazing.com/wins \
  -b "$IPA_COOKIE_FILE" \
  -H 'Content-Type: application/json' \
  -d '{
    "content": "Your win here",
    "type": "PROFESSIONAL",
    "visibility": "PUBLIC",
    "tags": ["tag1", "tag2"],
    "starFormat": {
      "situation": "What was the context or challenge?",
      "task": "What needed to be done?",
      "action": "What did you do?",
      "result": "What was the outcome?"
    }
  }'
```

也可以通过 `PATCH` 更新现有的获胜记录以添加 STAR 格式：

```bash
curl -s -X PATCH https://api.imprettyamazing.com/wins/:id \
  -b "$IPA_COOKIE_FILE" \
  -H 'Content-Type: application/json' \
  -d '{
    "starFormat": {
      "situation": "...",
      "task": "...",
      "action": "...",
      "result": "..."
    }
  }'
```

**STAR 格式对象的字段：**
`id`, `winId`, `situation`, `task`, `action`, `result`, `createdAt`, `updatedAt`

**获胜记录的类型：**
`PERSONAL`（个人）、`PROFESSIONAL`（职业）、`HEALTH`（健康）、`SOCIAL`（社交）、`CREATIVE`（创意）、`LEARNING`（学习）

**可见性：**
`PUBLIC`（对所有用户可见）或 `PRIVATE`（仅对发布者可见）。

**其他操作：**

所有需要 Cookie 认证的操作在登录后都需要使用 `-b "$IPA_COOKIE_FILE"`。**有关完整端点文档，请参阅 [references/api.md](references/api.md)。**在使用上述未列出的端点之前，请先阅读该文档。

- **更新/删除获胜记录**：`PATCH /wins/:id`（JSON 格式），`DELETE /wins/:id`
- **评论**：`POST /wins/:id/comments`（内容为 `{"content": "..."}`），`GET /wins/:id/comments`
- **点赞**：`POST /wins/:id/like`，`DELETE /wins/:id/like`（切换状态）
- **关注/取消关注**：`POST /follows/:userId`，`DELETE /follows/:userId`
- **个人资料**：`PATCH /profile`（JSON 格式：`username`、`bio` 最多 500 个字符、`location`、`website`）
- **头像/封面**：`POST /profile/avatar`（多部分格式的头像文件），`POST /profile/cover`（多部分格式的封面文件，文件大小请保持较小）
- **反馈**：`POST /feedback`（内容格式为 `{"category": "BUG|FEATURE_REQUEST|GENERAL", "message": "...", "pageUrl": "...", "pageContext": "..."`）

**清除会话**

如果用户要求登出或清除会话，请从 `TOOLS.md` 中删除 `### I'm Pretty Amazing` 部分，并删除所有 `/tmp/ipa-cookies-*.txt` 文件。

**主动使用建议：**

当用户完成了一些值得关注的事情（例如发布新功能、达成交易、解决难题或学到新知识）时，建议将其记录为获胜记录。在发布之前先草拟内容并获取用户的确认。