---
name: scalekit-auth
description: 通过 Scalekit 实现安全的 OAuth 令牌管理。该系统负责令牌的存储、刷新以及从第三方服务（如 Gmail、Slack、GitHub 等）中获取令牌的功能。令牌绝不会被存储在本地设备上——系统始终会从 Scalekit 获取最新的令牌。
homepage: https://scalekit.com
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python-deps
        kind: exec
        command: "pip3 install scalekit-sdk-python python-dotenv requests"
        label: "Install Python dependencies"
---

# Scalekit Auth - 安全令牌管理

为AI代理提供集中式的OAuth令牌管理功能。无需在本地存储令牌，支持自动刷新和多服务集成。

## 为什么使用它？

**问题：** OAuth令牌分散在各个配置文件中，缺乏刷新机制，存在安全隐患。

**解决方案：** Scalekit负责处理令牌的整个生命周期：
- ✅ 令牌存储在安全的云环境中（绝不会存储在本地）
- ✅ 支持自动刷新令牌
- ✅ 支持多种服务（如Gmail、Slack、Notion、GitHub等）
- ✅ 始终返回最新、有效的令牌

## 安装

### 1. 安装Skill

```bash
clawhub install scalekit-auth
cd skills/scalekit-auth
pip3 install -r requirements.txt
```

### 2. 获取Scalekit凭据

1. 在 [scalekit.com](https://scalekit.com) 注册
2. 进入控制面板 → 开发者 → 设置 → API凭据
3. 复制以下信息：
   - 客户端ID（Client ID）
   - 客户端密钥（Client Secret）
   - 环境URL（Environment URL）

### 3. 配置凭据

创建 `skills/scalekit-auth/.env` 文件：

```bash
SCALEKIT_CLIENT_ID=your_client_id_here
SCALEKIT_CLIENT_SECRET=your_client_secret_here
SCALEKIT_ENV_URL=https://your-env.scalekit.com
```

**或者** 在代理首次使用时由代理请求您提供这些凭据。

## 设置服务（以Gmail为例）

### 第1步：在Scalekit控制面板中创建连接

1. 进入Scalekit控制面板 → 连接 → 添加连接
2. 选择服务提供商（例如Gmail/Google）
3. 配置OAuth信息：
   - 从Google Cloud控制台获取客户端ID和密钥
   - 设置重定向URI（由Scalekit提供）
4. **复制`connection_name`（例如：`gmail_u3134a`）

### 第2步：在代理中注册该连接

将配置信息告知代理：
```
"Configure Gmail for Scalekit. Connection name is gmail_u3134a"
```

代理会将这些信息保存在 `connections.json` 文件中：
```json
{
  "gmail": {
    "connection_name": "gmail_u3134a",
    "identifier": "mess"
  }
}
```

### 第3步：授权

首次调用API时，系统会提示用户授权：
```
Authorization needed for Gmail.
Link: https://scalekit.com/auth/... (expires in 1 minute!)
```

点击链接进行授权即可完成！

## 使用方法

### 从代理技能中调用

```python
#!/usr/bin/env python3
import sys
sys.path.append('./skills/scalekit-auth')
from scalekit_helper import get_token

# Get fresh token for any service
access_token = get_token("gmail")

# Use it immediately
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/messages", headers=headers)
```

### 从Shell脚本中调用

```bash
# Get token via CLI wrapper
TOKEN=$(python3 skills/scalekit-auth/get_token.py gmail)

# Use in API call
curl -H "Authorization: Bearer $TOKEN" \
  https://gmail.googleapis.com/gmail/v1/users/me/messages
```

## 配置文件

### `connections.json`
该文件将服务名称与Scalekit中的连接名称进行映射：

```json
{
  "gmail": {
    "connection_name": "gmail_u3134a",
    "identifier": "mess"
  },
  "slack": {
    "connection_name": "slack_x7y9z",
    "identifier": "mess"
  }
}
```

**注意：** `identifier` 会自动设置为代理的名称（来自IDENTITY.md文件）。

### `.env`
其中包含Scalekit的API凭据（切勿提交到Git仓库！）：

```bash
SCALEKIT_CLIENT_ID=sk_live_...
SCALEKIT_CLIENT_SECRET=...
SCALEKIT_ENV_URL=https://...
```

## 支持的服务

Scalekit支持以下所有OAuth服务提供商：
- Gmail、Google Calendar、Google Drive
- Slack、Notion、Linear、GitHub
- Salesforce、HubSpot、Zendesk
- 以及50多种其他服务

请查看 [Scalekit Connectors](https://docs.scalekit.com/connectors) 以获取完整列表。

## 授权流程

```
1. Agent calls get_token("gmail")
2. Check if connection configured → if NO, ask user
3. Check if authorized (status == ACTIVE)
4. If NOT authorized:
   - Generate auth link (expires 1 min)
   - Send to user via Telegram/chat
   - Wait for authorization
5. Return fresh access_token
6. Scalekit auto-refreshes in background
```

## 错误处理

**连接未配置：**
```
Error: gmail not configured. Please:
1. Create connection in Scalekit dashboard
2. Provide connection_name
```

**授权过期：**
```
Authorization needed: [link]
(Link expires in 1 minute - click now!)
```

**缺少Scalekit凭据：**
```
Scalekit not configured. Please provide:
- SCALEKIT_CLIENT_ID
- SCALEKIT_CLIENT_SECRET
- SCALEKIT_ENV_URL
```

## 安全最佳实践

1. **切勿在日志中记录令牌信息**——使用 `[REDACTED]` 替代令牌值
2. **将`.env` 文件添加到 `.gitignore` 文件中**——避免将凭据提交到Git仓库
3. **如果凭据泄露，请及时更换**
4. **为开发环境和生产环境使用不同的Scalekit账户**
5. **授权链接的有效期为1分钟**——请尽快处理！

## 故障排除

**“模块未找到”错误：**
```bash
cd skills/scalekit-auth
pip3 install -r requirements.txt
```

**令牌请求返回401错误：**
- 可能是授权已过期
- 代理会提示用户重新授权

**连接未找到：**
- 检查 `connections.json` 文件是否存在
- 确认Scalekit控制面板中的连接名称是否正确

## 示例：Gmail集成

```python
# In your skill's script
from scalekit_helper import get_token
import requests

def fetch_unread_emails():
    token = get_token("gmail")
    
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
    params = {"q": "is:unread", "maxResults": 5}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

## 使用Scalekit Auth发布技能

如果您的技能使用了Scalekit Auth功能：
1. 在 `SKILL.md` 文件中记录相关配置：
   ```markdown
   ## Prerequisites
   - Install scalekit-auth skill
   - Configure [SERVICE] connection in Scalekit
   ```

2. 在脚本中导入相关代码：
   ```python
   sys.path.append('./skills/scalekit-auth')
   from scalekit_helper import get_token
   ```

3. **优雅地处理错误**——引导用户完成连接配置

## API参考

### `get_token(service_name: str) → str`

返回该服务的最新OAuth访问令牌。

**参数：**
- `service_name`：服务标识符（例如：“gmail”、“slack”）

**返回值：**
- `access_token`：最新的OAuth访问令牌

**可能抛出的异常：**
- `ConfigurationError`：服务未配置或缺少Scalekit凭据
- `AuthorizationError`：用户需要重新授权（系统会发送授权链接）

**示例：**
```python
token = get_token("gmail")
print(f"Token: {token[:10]}...")  # Never log full token!
```

## 开发计划

- [ ] 支持多用户使用（每个服务可关联多个用户）
- [ ] 实现令牌缓存（减少API调用次数）
- [ ] 提供CLI工具（例如：`scalekit-auth config gmail gmail_u3134a`）
- [ ] 从API URL自动识别服务类型
- [ ] 支持批量获取令牌

## 贡献建议

发现漏洞或有功能需求？请在ClawHub上提交问题！

---

**请记住：** 令牌属于敏感信息，请妥善处理。 🔐