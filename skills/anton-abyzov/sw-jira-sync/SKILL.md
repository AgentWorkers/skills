---
name: jira-sync
description: 关于如何将 SpecWeave 的增量数据与 JIRA 的史诗（epic）或故事（story）进行同步的指导（数据从 SpecWeave 导入 JIRA，状态从 JIRA 更新到 SpecWeave）。在询问 JIRA 集成设置或同步问题时，请参考本指南。如需实际执行同步操作，请使用 `/sw-jira:sync` 命令。
allowed-tools: Read, Write, Edit, Task, Bash
---

# JIRA同步技能

该技能通过委托给`jira-mapper`代理来协调JIRA的同步操作。

**同步行为**：
- 内容（规格说明、任务）从SpecWeave同步到JIRA。
- 状态（打开/关闭）从JIRA同步到SpecWeave。

**⚠️ 重要提示**：此技能仅提供关于JIRA同步的帮助和指导。实际进行同步操作时，用户应直接使用`/sw-jira:sync`命令。在调用该命令时，此技能不应自动激活。

## 何时激活此技能

✅ **在以下情况下激活**：
- 用户询问：“如何设置JIRA同步？”
- 用户询问：“我需要哪些JIRA凭证？”
- 用户询问：“JIRA同步是如何工作的？”
- 用户需要帮助配置JIRA集成

❌ **在以下情况下不要激活此技能**：
- 用户已经调用了`/sw-jira:sync`命令（该命令会自动处理同步操作）。
- 命令正在运行中（避免重复调用）。
- 任务完成钩子正在执行同步操作（这是自动进行的流程）。

## 负责事项

1. 回答有关JIRA同步配置的问题。
2. 帮助用户验证所需的先决条件（JIRA凭证、数据结构）。
3. 解释同步的方向：内容从SpecWeave同步到JIRA，状态从JIRA同步到SpecWeave。
4. 提供故障排除指导。

---

## ⚠️ 重要提示：需要保密信息（必须检查）

**在尝试JIRA同步之前，请务必检查JIRA凭证。**

### 第1步：检查凭证是否存在

```bash
# Check .env file for both required credentials
if [ -f .env ] && grep -q "JIRA_API_TOKEN" .env && grep -q "JIRA_EMAIL" .env; then
  echo "✅ JIRA credentials found"
else
  # Credentials NOT found - STOP and prompt user
fi
```

### 第2步：如果凭证缺失，请停止并显示以下提示信息

```
🔐 **JIRA API Token and Email Required**

I need your JIRA API token and email to sync with JIRA.

**How to get it**:
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Log in with your Atlassian account
3. Click "Create API token"
4. Give it a label (e.g., "specweave-sync")
5. Click "Create"
6. **Copy the token immediately** (you can't see it again!)

**Where I'll save it**:
- File: `.env` (gitignored, secure)
- Format:
  ```
  JIRA_API_TOKEN=your-jira-api-token-here
  JIRA_EMAIL=your-email@example.com
  JIRA_DOMAIN=your-domain.atlassian.net
  ```

**Security**:
✅ .env is in .gitignore (never committed to git)
✅ Token is random alphanumeric string (variable length)
✅ Stored locally only (not in source code)

Please provide:
1. Your JIRA API token:
2. Your JIRA email:
3. Your JIRA domain (e.g., company.atlassian.net):
```

### 第3步：验证凭证格式

```bash
# Validate email format
if [[ ! "$JIRA_EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
  echo "⚠️  Warning: Email format unexpected"
  echo "Expected: valid email address"
  echo "Got: $JIRA_EMAIL"
fi

# Validate domain format
if [[ ! "$JIRA_DOMAIN" =~ \.atlassian\.net$ ]]; then
  echo "⚠️  Warning: Domain format unexpected"
  echo "Expected: *.atlassian.net"
  echo "Got: $JIRA_DOMAIN"
  echo "Note: Self-hosted JIRA may have different domain format"
fi

# Token validation (just check it's not empty)
if [ -z "$JIRA_API_TOKEN" ]; then
  echo "❌ Error: JIRA API token is empty"
  exit 1
fi
```

### 第4步：安全地保存凭证

```bash
# Save to .env
cat >> .env << EOF
JIRA_API_TOKEN=$JIRA_API_TOKEN
JIRA_EMAIL=$JIRA_EMAIL
JIRA_DOMAIN=$JIRA_DOMAIN
EOF

# Ensure .env is gitignored
if ! grep -q "^\\.env$" .gitignore; then
  echo ".env" >> .gitignore
fi

# Create .env.example for team
cat > .env.example << 'EOF'
# JIRA API Token
# Get from: https://id.atlassian.com/manage-profile/security/api-tokens
JIRA_API_TOKEN=your-jira-api-token
JIRA_EMAIL=your-email@example.com
JIRA_DOMAIN=your-domain.atlassian.net
EOF

echo "✅ Credentials saved to .env (gitignored)"
echo "✅ Created .env.example for team (commit this)"
```

### 第5步：使用凭证进行同步

```bash
# Export for JIRA API calls (read from .env without displaying values)
export JIRA_API_TOKEN=$(grep '^JIRA_API_TOKEN=' .env | cut -d '=' -f2-)
export JIRA_EMAIL=$(grep '^JIRA_EMAIL=' .env | cut -d '=' -f2-)
export JIRA_DOMAIN=$(grep '^JIRA_DOMAIN=' .env | cut -d '=' -f2-)

# Create Basic Auth header (JIRA uses email:token)
AUTH=$(echo -n "$JIRA_EMAIL:$JIRA_API_TOKEN" | base64)

# Use in JIRA API calls
curl -H "Authorization: Basic $AUTH" \
     -H "Content-Type: application/json" \
     https://$JIRA_DOMAIN/rest/api/3/issue/PROJ-123
```

### 第6步：切勿记录敏感信息

```bash
# ❌ WRONG - Logs secret
echo "Using token: $JIRA_API_TOKEN"

# ✅ CORRECT - Masks secret
echo "Using JIRA credentials (token present: ✅, email: $JIRA_EMAIL)"
```

### 第7步：错误处理

```bash
# If API call fails with 401 Unauthorized
if [ $? -eq 401 ]; then
  echo "❌ JIRA credentials invalid"
  echo ""
  echo "Possible causes:"
  echo "1. API token expired or revoked"
  echo "2. Email address incorrect"
  echo "3. Domain incorrect (check: $JIRA_DOMAIN)"
  echo "4. Account lacks permissions (need: project admin or issue create/edit)"
  echo ""
  echo "Please verify credentials:"
  echo "https://id.atlassian.com/manage-profile/security/api-tokens"
fi

# If API call fails with 403 Forbidden
if [ $? -eq 403 ]; then
  echo "❌ JIRA permission denied"
  echo ""
  echo "Your account lacks permissions for this operation."
  echo "Required permissions:"
  echo "- Browse projects"
  echo "- Create issues"
  echo "- Edit issues"
  echo "- Administer projects (for Epic creation)"
  echo ""
  echo "Contact your JIRA administrator."
fi
```

### 第8步：生产环境建议

**在生产环境中，建议使用OAuth 2.0而非API令牌：**

**为什么选择OAuth 2.0？**
- ✅ 更安全（无需长期有效的凭证）
- ✅ 权限控制更精细（通过范围进行限制）
- ✅ 令牌会自动更新
- ✅ JIRA中会有审计记录

**如何设置OAuth 2.0**：
1. 访问：https://developer.atlassian.com/console/myapps/
2. 创建一个新的应用程序。
3. 配置OAuth 2.0凭证。
4. 添加所需的权限范围（读取：jira-work，写入：jira-work）。
5. 使用OAuth授权流程而非API令牌。

**对于自托管的JIRA**：请使用个人访问令牌（Personal Access Tokens，简称PAT）代替API令牌。

---

## 使用方法

**导出**：`/sync-jira export 0001`
**导入**：`/sync-jira import PROJ-123`
**同步**：`/sync-jira sync 0001`

所有的转换逻辑均由`jira-mapper`代理负责处理。