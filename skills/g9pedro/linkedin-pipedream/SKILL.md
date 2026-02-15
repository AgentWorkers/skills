---
name: linkedin-pipedream
description: 通过 Pipedream 的 OAuth 集成，您可以发布内容到 LinkedIn、发表评论、点赞、搜索组织以及管理个人资料。
homepage: https://mcp.pipedream.com
metadata:
  {
    "openclaw":
      {
        "emoji": "💼",
        "requires": { "bins": ["pdauth"], "skills": ["pdauth"] },
        "install": [
          {
            "id": "pdauth-dep",
            "kind": "skill",
            "skill": "pdauth",
            "label": "Install pdauth skill first",
          },
        ],
      },
  }
---

# 通过 Pipedream 进行 LinkedIn 操作——发布内容、发表评论及互动

利用 Pipedream 的 OAuth 基础设施实现完整的 LinkedIn 自动化功能。可以以个人或组织的身份发布内容、在帖子下发表评论、搜索公司等。

## 先决条件

1. **已安装并配置 pdauth CLI** — 请参考 pdauth 技能文档。
2. **通过 OAuth 连接了 LinkedIn 账户**。

## 快速入门

```bash
# 1. Connect LinkedIn (generates OAuth link for user to click)
pdauth connect linkedin --user telegram:5439689035

# 2. After user authorizes, verify connection
pdauth status --user telegram:5439689035

# 3. Post to LinkedIn
pdauth call linkedin.linkedin-create-text-post-user \
  --user telegram:5439689035 \
  --args '{"instruction": "Create a post: Excited to announce our new product launch! 🚀"}'
```

## OAuth 流程

```bash
# Generate OAuth link
pdauth connect linkedin --user USER_ID

# Share with user: "Click to authorize LinkedIn: <link>"
# User clicks → authorizes via LinkedIn → done

# Verify connection
pdauth status --user USER_ID
```

**用户 ID 规范：** 对于 Telegram 用户，使用 `telegram:<user_id>` 的格式。

---

## 可用工具（共 19 个）

### ✅ 通过 MCP（pdauth 调用）实现的功能

| 工具 | 功能 |
|------|---------|
| `linkedin-create-text-post-user` | 以个人账户身份发布内容 |
| `linkedin-create-image-post-user` | 以个人身份发布带图片的内容 |
| `linkedin-create-comment` | 在任何帖子下发表评论 |
| `linkedin-create-like-on-share` | 点赞帖子 |
| `linkedin-search-organization` | 搜索公司 |
| `linkedin-get-current-member-profile` | 获取个人资料 |
| `linkedin-get-member-profile` | 获取任何成员的资料 |
| `linkedin-get-org-member-access` | 检查组织管理员权限 |
| `linkedin-retrieve-comments-shares` | 获取帖子的评论 |
| `linkedin-delete-post` | 删除自己的帖子 |

### ⚠️ 通过 MCP 无法使用的功能（需要绕过）

| 工具 | 问题 | 绕过方法 |
|------|-------|------------|
| `linkedin-create-text-post-organization` | “工具名称过长”的错误 | 使用直接 SDK 调用 |
| `linkedin-create-image-post-organization` | 同样问题 | 使用直接 SDK 调用 |

---

## 工具参考

### 1. 以个人身份发布内容

```bash
pdauth call linkedin.linkedin-create-text-post-user \
  --user telegram:5439689035 \
  --args '{"instruction": "Create a post: Your post content here. Use emojis 🎉 and hashtags #AI #Tech"}'
```

**提示：**
- 发布的内容长度请控制在 3000 字以内。
- 使用表情符号可以提高互动率。
- 适当使用换行符以提高可读性。

### 2. 以个人身份发布带图片的内容

```bash
pdauth call linkedin.linkedin-create-image-post-user \
  --user telegram:5439689035 \
  --args '{"instruction": "Create image post with text: Check out our new office! Image URL: https://example.com/image.jpg"}'
```

### 3. 在帖子下发表评论

```bash
# Comment using post URN
pdauth call linkedin.linkedin-create-comment \
  --user telegram:5439689035 \
  --args '{"instruction": "Comment on urn:li:share:7293123456789012480 with text: Great insights! Thanks for sharing."}'
```

**获取帖子 URI 的方法：**
- 从 LinkedIn URL 中获取：`linkedin.com/posts/username_activity-7293123456789012480` → URI 为 `urn:li:share:7293123456789012480`
- 或者使用 `linkedin-retrieve-comments-shares` 来获取已知帖子的评论。

### 4. 点赞帖子

```bash
pdauth call linkedin.linkedin-create-like-on-share \
  --user telegram:5439689035 \
  --args '{"instruction": "Like the post urn:li:share:7293123456789012480"}'
```

### 5. 搜索公司

```bash
pdauth call linkedin.linkedin-search-organization \
  --user telegram:5439689035 \
  --args '{"instruction": "Search for companies matching: artificial intelligence startups"}'
```

### 6. 获取个人资料

```bash
pdauth call linkedin.linkedin-get-current-member-profile \
  --user telegram:5439689035 \
  --args '{"instruction": "Get my LinkedIn profile"}'
```

返回内容包括：姓名、标题、URI、昵称等。

### 7. 获取成员资料

```bash
pdauth call linkedin.linkedin-get-member-profile \
  --user telegram:5439689035 \
  --args '{"instruction": "Get profile for member URN urn:li:person:30_5n7bx7f"}'
```

### 8. 检查组织管理员权限

```bash
pdauth call linkedin.linkedin-get-org-member-access \
  --user telegram:5439689035 \
  --args '{"instruction": "Check my access level for organization 105382747"}'
```

返回结果包括：`ADMINISTRATOR`、`MEMBER` 或 `NONE`。

### 9. 获取帖子的评论

```bash
pdauth call linkedin.linkedin-retrieve-comments-shares \
  --user telegram:5439689035 \
  --args '{"instruction": "Get comments for post urn:li:share:7293123456789012480"}'
```

### 10. 删除帖子

```bash
pdauth call linkedin.linkedin-delete-post \
  --user telegram:5439689035 \
  --args '{"instruction": "Delete post urn:li:share:7293123456789012480"}'
```

---

## 组织发布内容（需要绕过）

### 错误原因

`linkedin-create-text-post-organization` 通过 MCP 无法使用，原因是：
```
Error: tool name too long
```

这是 Pipedream MCP 的问题，而非 LinkedIn API 的问题。

### 绕过方法：使用直接 SDK 调用

创建一个 Node.js 脚本来以组织身份发布内容：

```javascript
// org-post.mjs
import { PipedreamClient } from '@pipedream/sdk';

const client = new PipedreamClient({
  projectEnvironment: 'development',
  clientId: 'YOUR_CLIENT_ID',      // from ~/.config/pdauth/config.json
  clientSecret: 'YOUR_CLIENT_SECRET',
  projectId: 'YOUR_PROJECT_ID',
});

async function postAsOrg(orgId, text) {
  const result = await client.actions.run({
    id: 'linkedin-create-text-post-organization',
    externalUserId: 'telegram:5439689035',
    configuredProps: {
      linkedin: { authProvisionId: 'apn_4vhLGx4' },  // LinkedIn account ID
      organizationId: orgId,
      text: text,
    },
  });
  console.log('Posted!', result);
}

// Example usage
postAsOrg('105382747', 'Hello from Versatly! 🚀');
```

运行方式：
```bash
node org-post.mjs
```

### 已知的组织 ID

| 组织 | ID | URI |
|--------------|-----|-----|
| Versatly | 105382747 | urn:li:organization:105382747 |

---

## 关键参考值

### Pedro 的 LinkedIn 信息

| 项目 | 值 |
|------|-------|
| 成员 URI | `urn:li:person:30_5n7bx7f` |
| 用户 ID（Pipedream） | `telegram:5439689035` |
| 认证提供者 ID | `apn_4vhLGx4` |
| 组织管理员（Versatly，ID 105382747） |

### URI 格式

| 类型 | 格式 | 示例 |
|------|--------|---------|
| 个人 | `urn:li:person:ID` | `urn:li:person:30_5n7bx7f` |
| 组织 | `urn:li:organization:ID` | `urn:li:organization:105382747` |
| 帖子/分享 | `urn:li:share:ID` | `urn:li:share:7293123456789012480` |
| 评论 | `urn:li:comment:(urn:li:share:ID,ID)` | 复杂的嵌套 URI |

---

## 常见操作模式

### 模式 1：发布内容并验证

```bash
# Post
pdauth call linkedin.linkedin-create-text-post-user \
  --user telegram:5439689035 \
  --args '{"instruction": "Create post: Just shipped a new feature! 🎉"}'

# The response includes the post URN - save it for later
```

### 模式 2：与内容互动

```bash
# Find posts to engage with (manual: get URN from LinkedIn URL)
# Like the post
pdauth call linkedin.linkedin-create-like-on-share \
  --user telegram:5439689035 \
  --args '{"instruction": "Like post urn:li:share:7293123456789012480"}'

# Comment
pdauth call linkedin.linkedin-create-comment \
  --user telegram:5439689035 \
  --args '{"instruction": "Comment on urn:li:share:7293123456789012480: Congrats on the launch!"}'
```

### 模式 3：搜索公司

```bash
# Search for the company
pdauth call linkedin.linkedin-search-organization \
  --user telegram:5439689035 \
  --args '{"instruction": "Search for OpenAI"}'

# Check if you have admin access (for orgs you manage)
pdauth call linkedin.linkedin-get-org-member-access \
  --user telegram:5439689035 \
  --args '{"instruction": "Check access for organization 12345678"}'
```

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| “应用未连接” | 未连接到 LinkedIn OAuth | 运行 `pdauth connect linkedin --user USER_ID` |
| “工具名称过长” | 组织相关工具的 MCP 错误 | 使用直接 SDK 绕过方法 |
| `403 Forbidden` | 没有操作权限 | 检查组织管理员权限 |
| “无效的 URI” | URI 格式错误 | 使用正确的格式：`urn:li:type:id` |
| “速率限制” | API 调用次数过多 | 等待片刻后重试（LinkedIn 每天限制约 100 次调用） |

### 检查连接状态

```bash
# Quick status check
pdauth status --user telegram:5439689035

# JSON output for parsing
pdauth status --user telegram:5439689035 --json
```

### 重新连接

如果 OAuth 连接失效或中断：
```bash
pdauth disconnect linkedin --user telegram:5439689035
pdauth connect linkedin --user telegram:5439689035
# Share new link with user
```

---

## 最佳实践

1. **速率限制：** LinkedIn 对批量操作有严格限制，请合理安排操作时间。
2. **内容质量：** LinkedIn 会惩罚垃圾内容，请撰写有意义的帖子。
3. **组织发布内容：** 在尝试以组织身份发布内容前，务必确认具有管理员权限。
4. **URI 处理：** 在调用 API 之前，务必验证 URI 的格式。
5. **错误恢复：** 如果帖子发布失败，请先检查状态再重试（可能已经成功）。

---

## 示例工作流程：完整的 LinkedIn 营销活动

```bash
# 1. Verify connection
pdauth status --user telegram:5439689035

# 2. Check org admin status
pdauth call linkedin.linkedin-get-org-member-access \
  --user telegram:5439689035 \
  --args '{"instruction": "Check access for organization 105382747"}'

# 3. Post personal announcement
pdauth call linkedin.linkedin-create-text-post-user \
  --user telegram:5439689035 \
  --args '{"instruction": "Create post: Thrilled to share that Versatly just launched our new AI assistant! 🤖 #AI #Startup"}'

# 4. Post as organization (use SDK workaround)
# → Run org-post.mjs script

# 5. Engage with relevant industry posts
pdauth call linkedin.linkedin-create-comment \
  --user telegram:5439689035 \
  --args '{"instruction": "Comment on urn:li:share:XXXXX: Great perspective on AI safety!"}'
```

---

## 文件与配置

| 文件 | 用途 |
|------|---------|
| `~/.config/pdauth/config.json` | Pipedream 的认证信息 |
| `~/.openclaw/workspace/pdauth/` | pdauth CLI 的源代码 |
| `~/.openclaw/workspace/skills/pdauth/SKILL.md` | pdauth 技能参考文档 |

---

## 参考资料

- **pdauth 技能文档** — 用于所有 Pipedream 应用的 OAuth 管理
- [Pipedream MCP](https://mcp.pipedream.com) — 浏览所有可用的集成服务
- [LinkedIn API 文档](https://learn.microsoft.com/en-us/linkedin/marketing/) — 官方 API 参考文档