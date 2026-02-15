---
name: xpoz-setup
description: "设置并验证用于社交媒体情报收集的 Xpoz MCP 服务器。这是所有 Xpoz 功能所必需的。该过程涉及服务器配置、OAuth 登录以及连接验证，且用户交互量极少。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["mcporter"], "network": ["mcp.xpoz.ai", "www.xpoz.ai"], "credentials": "Xpoz account (free tier) — obtained via Google OAuth during setup" },
      },
  }
tags:
  - xpoz
  - mcp
  - setup
  - oauth
  - social-media
---

# Xpoz 设置

**为 Xpoz（一个社交智能平台）自动配置 MCP 服务器并处理身份验证。**

此技能是所有 Xpoz 技能的先决条件。它用于配置 Xpoz MCP 服务器并处理 OAuth 登录，以便您的代理能够访问 Twitter、Instagram、TikTok 和 Reddit 的数据。

---

## 代理操作指南

**如果您是正在阅读此指南的代理，请按以下步骤操作。用户无需运行任何命令。**

### 第 1 步：检查是否已认证

```bash
mcporter call xpoz.checkAccessKeyStatus
```

- 如果 `hasAccessKey: true` → **停止操作。Xpoz 已准备就绪。** 返回发送您到这里的其他技能。
- 如果返回 `false` 或服务器未配置 → 继续下一步。

### 第 2 步：检查是否可以找到 mcporter

```bash
which mcporter
```

如果找不到 `mcporter`，**请停止操作并通知用户。** `mcporter` 是 OpenClaw 的组成部分——如果缺少它，可能表示 OpenClaw 安装不完整。不要单独安装 `mcporter`。请告知用户：

> “需要 `mcporter`，但未找到。它包含在 OpenClaw 中，请确保 OpenClaw 已正确安装。”

### 第 3 步：添加 Xpoz MCP 服务器

```bash
mcporter config add xpoz https://mcp.xpoz.ai/mcp --auth oauth
```

此步骤会将 Xpoz 注册为支持 OAuth 认证的远程 HTTP MCP 服务器。`mcporter` 会自动从 `https://mcp.xpoz.ai/.well-known/oauth-authorization-server` 获取 OAuth 终端点。

如果服务器已经存在但认证失败，请跳过此步骤。

### 第 4 步：判断环境（本地还是远程）

确定您是在带有浏览器的本地机器上运行，还是在远程/无头服务器上运行：

```bash
# Check for display server (Linux) or macOS
echo "DISPLAY=${DISPLAY:-unset} WAYLAND=${WAYLAND_DISPLAY:-unset} OS=$(uname)"
```

**本地机器**：满足以下任意一个条件：
- `$DISPLAY` 被设置（使用 X11 的 Linux）
- `$WAYLANDDISPLAY` 被设置（使用 Wayland 的 Linux）
- `uname` 返回 `Darwin`（macOS）

**远程/无头服务器**：不满足上述任何条件。

然后按照相应的流程操作：

---

### 第 4a 步：本地环境——浏览器自动流程

```bash
mcporter config login xpoz
```

`mcporter` 会打开用户的默认浏览器，用户完成授权后，回调会自动完成。请告知用户：

> “我正在将您连接到 Xpoz 以获取社交媒体数据。应该会打开一个浏览器窗口——只需使用您的 Google 账户登录并点击‘授权’即可！”

然后跳到 **第 5 步**。

---

### 第 4b 步：远程环境——手动代码流程

在无头服务器上，尝试打开浏览器时 `mcporter config login xpoz` 可能会崩溃。此时需要手动处理 OAuth 流程：

#### 4b-i. 生成授权 URL

运行以下脚本以生成包含 PKCE 的 OAuth 授权 URL：

```bash
bash "$(dirname "$0")/../xpoz-setup/scripts/oauth-remote.sh" get-url
```

如果该脚本不可用，可以手动生成授权 URL：

```python
import secrets, hashlib, base64, urllib.parse, os

os.makedirs(os.path.expanduser('~/.cache/xpoz-oauth'), exist_ok=True)

# Generate PKCE
verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
state = secrets.token_urlsafe(32)

params = {
    'response_type': 'code',
    'code_challenge': challenge,
    'code_challenge_method': 'S256',
    'redirect_uri': 'https://www.xpoz.ai/oauth/openclaw',
    'state': state,
    'scope': 'mcp:tools',
    'resource': 'https://mcp.xpoz.ai/',
}

# Step 1: Dynamic client registration
import json, urllib.request
reg_req = urllib.request.Request(
    'https://mcp.xpoz.ai/oauth/register',
    data=json.dumps({
        'client_name': 'OpenClaw Agent',
        'redirect_uris': ['https://www.xpoz.ai/oauth/openclaw'],
        'grant_types': ['authorization_code'],
        'response_types': ['code'],
        'token_endpoint_auth_method': 'none',
    }).encode(),
    headers={'Content-Type': 'application/json'},
)
reg_resp = json.loads(urllib.request.urlopen(reg_req).read())
params['client_id'] = reg_resp['client_id']

auth_url = 'https://mcp.xpoz.ai/oauth/authorize?' + urllib.parse.urlencode(params)

# Save state for later token exchange
with open(os.path.expanduser('~/.cache/xpoz-oauth/state.json'), 'w') as f:
    json.dump({'verifier': verifier, 'state': state, 'client_id': reg_resp['client_id'], 'redirect_uri': params['redirect_uri']}, f)

print(auth_url)
```

#### 4b-ii. 将授权 URL 发送给用户

通过活跃的聊天通道将授权 URL 发送给用户，并附上如下信息：

> “我需要连接到 Xpoz 以进行社交媒体搜索。请打开此链接并使用您的 Google 账户登录：
>
> [授权 URL]
>
> 授权完成后，Xpoz 会显示一个授权代码。请将其复制并发送给我！”

#### 4b-iii. 等待用户的回复

**在此处等待用户的回复。** 在用户复制授权代码之前不要继续。用户需要时间来打开链接、登录并完成授权。只有在用户将代码发送回聊天窗口后才能继续。

#### 4b-iv. 从用户的回复中提取代码

用户可能会复制以下内容：
- 仅代码：`AUTH_CODE_HERE`
- 或完整的 URL：`https://www.xpoz.ai/oauth/openclaw?code=AUTH_CODE_HERE&state=...`

如果用户复制了完整的 URL，请提取 `code` 参数；如果复制了纯文本字符串，则直接使用该字符串。

#### 4b-v. 交换代码并配置 mcporter

使用提取到的代码运行交换脚本。该脚本会将代码转换为令牌，并一步完成 `mcporter` 的配置——令牌不会被打印或暴露：

```bash
bash "$(dirname "$0")/../xpoz-setup/scripts/oauth-remote.sh" exchange AUTH_CODE_HERE
```

预期输出：`OK: Xpoz 配置成功`

**安全注意事项：**
- 访问令牌不会被打印到标准输出或日志中
- OAuth 状态文件（`~/.cache/xpoz-oauth/state.json`）在交换后会自动删除
- 令牌仅存储在 `mcporter` 的配置中

然后继续执行 **第 5 步** 进行验证。

---

### 第 5 步：验证认证

```bash
mcporter call xpoz.checkAccessKeyStatus
```

确认 `hasAccessKey: true`。如果未通过：
- **本地环境：** 重新运行 `mcporter config login xpoz`
- **远程环境：** 询问用户是否已完成授权，如有需要请重新发送链接

### 第 6 步：返回到调用该技能的页面

设置完成。返回调用此技能的页面，继续处理用户的请求。不要让用户等待——他们只是要求您执行某些操作，而认证只是先决条件而已。

---

## 什么是 Xpoz？

Xpoz 是一个用于获取社交媒体数据的远程 MCP 服务器：

- **支持的平台：** Twitter、Instagram、TikTok、Reddit
- **数据规模：** 索引了超过 15 亿条帖子
- **功能：** 按关键词搜索帖子、按主题查找用户、查看用户资料、过滤互动数据、导出 CSV 文件
- **认证方式：** 使用 OAuth 2.1 和动态客户端注册（PKCE，支持公共客户端）
- **配置方式：** 完全远程化——无需安装 npm 包，无需本地安装，无需复制 API 密钥

**提供免费 tier**——无需信用卡。

官方网站：[xpoz.ai](https://xpoz.ai)

---

## 技术细节

### OAuth 发现机制

Xpoz 公开了标准的 OAuth 2.1 授权服务器元数据文档：

```
GET https://mcp.xpoz.ai/.well-known/oauth-authorization-server
```

关键端点：
- **授权：** `https://mcp.xpoz.ai/oauth/authorize`
- **令牌：** `https://mcp.xpoz.ai/oauth/token`
- **动态注册：** `https://mcp.xpoz.ai/oauth/register`
- **支持 PKCE：** 支持 S256
- **公共客户端：** `token_endpoint_auth_methods_supported` 中包含 `none`

`mcporter` 会自动处理所有这些操作——您无需直接调用这些端点。

### 服务器配置

配置完成后，`mcporter` 的配置文件中会包含相关信息：

```json
{
  "xpoz": {
    "transport": "http",
    "url": "https://mcp.xpoz.ai/mcp"
  }
}
```

OAuth 令牌由 `mcporter` 独立管理，与服务器配置分开存储。

---

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 未找到 `mcporter` | 确保 OpenClaw 已正确安装（`mcporter` 是 OpenClaw 的组成部分） |
| 浏览器无法打开 | 在无头服务器上运行时，从标准输出中捕获 URL 并发送给用户 |
- 登录后显示“未经授权” | 运行 `mcporter config login xpoz --reset` |
- 认证超时 | 用户可能未完成浏览器操作——重新发送授权链接 |
- 服务器已存在 | 跳过第 3 步，直接执行第 4 步 |

---

## 计划与定价

| 计划 | 价格 | 包含的内容 |
|------|-------|----------|
| 免费 | 每月 $0 | 有限次搜索，支持所有平台 |
| 专业版 | 每月 $20 | 无限次搜索 |
| 最高级 | 每月 $200 | 无限次搜索 + 优先处理 + 批量导出 |

详情：[xpoz.ai](https://xpoz.ai)

---

**专为 ClawHub 设计 • 所有 Xpoz 技能的必备组件**