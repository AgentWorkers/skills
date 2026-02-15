---
name: dropbox-lite
description: 使用自动更新的 OAuth 令牌，在 Dropbox 中上传、下载和管理文件。
homepage: https://www.dropbox.com/developers
---

# Dropbox

支持在 Dropbox 中上传、下载、列出和搜索文件，同时支持自动刷新访问令牌。

## 所需凭据

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `DROPBOX_APP_KEY` | ✅ 是 | 你的 Dropbox 应用密钥 |
| `DROPBOX_APP_SECRET` | ✅ 是 | 你的 Dropbox 应用秘钥 |
| `DROPBOX_REFRESH_TOKEN` | ✅ 是 | OAuth 刷新令牌（长期有效） |
| `DROPBOX_ACCESS_TOKEN` | 可选 | 短期访问令牌（自动刷新） |

将这些凭据保存在 `~/.config/atlas/dropbox.env` 文件中：
```bash
DROPBOX_APP_KEY=your_app_key
DROPBOX_APP_SECRET=your_app_secret
DROPBOX_REFRESH_TOKEN=xxx...
DROPBOX_ACCESS_TOKEN=sl.u.xxx...
```

## 初始设置（一次性操作）

### 1. 创建 Dropbox 应用

1. 访问 https://www.dropbox.com/developers/apps
2. 点击 “创建应用”
3. 选择 “有限访问权限”（Scoped access）
4. 选择 “全 Dropbox 访问权限”（Full Dropbox）或 “应用文件夹访问权限”（App folder）
5. 为应用命名
6. 记下 **应用密钥**（App key）和 **应用秘钥**（App secret）

### 2. 设置权限

在应用设置中的 “权限”（Permissions）选项下，启用以下权限：
- `files.metadata.read`（读取文件元数据）
- `files.metadata.write`（写入文件元数据）
- `files.content.read`（读取文件内容）
- `files.content.write`（写入文件内容）
- `account_info.read`（读取账户信息）

点击 “提交” 以保存设置。

### 3. 运行 OAuth 流程

生成授权 URL：

```python
import urllib.parse

APP_KEY = "your_app_key"

params = {
    "client_id": APP_KEY,
    "response_type": "code",
    "token_access_type": "offline"  # This gets you a refresh token!
}

auth_url = "https://www.dropbox.com/oauth2/authorize?" + urllib.parse.urlencode(params)
print(auth_url)
```

将生成的 URL 提供给用户。用户需要：
1. 在浏览器中打开该 URL
2. 授权该应用
3. 接收到一个 **授权码**（authorization code）

### 4. 将授权码兑换为访问令牌

```bash
curl -X POST "https://api.dropboxapi.com/oauth2/token" \
  -d "code=AUTHORIZATION_CODE" \
  -d "grant_type=authorization_code" \
  -d "client_id=APP_KEY" \
  -d "client_secret=APP_SECRET"
```

响应中包含以下内容：
- `access_token` — 短期访问令牌（有效期约 4 小时）
- `refresh_token` — 长期有效令牌（除非被明确撤销，否则永远不会过期）

## 使用方法

```bash
# Account info
dropbox.py account

# List folder
dropbox.py ls "/path/to/folder"

# Search files
dropbox.py search "query"

# Download file
dropbox.py download "/path/to/file.pdf"

# Upload file
dropbox.py upload local_file.pdf "/Dropbox/path/remote_file.pdf"
```

## 令牌刷新

脚本会自动处理令牌刷新：
1. 当收到 401 Unauthorized 错误时，使用刷新令牌获取新的访问令牌
2. 将新的访问令牌更新到 `dropbox.env` 文件中
3. 重新尝试原始请求

## 令牌生命周期

| 令牌类型 | 有效期 | 存储方式 |
|-------|----------|---------|
| 访问令牌 | 约 4 小时 | 自动更新 |
| 刷新令牌 | 永不过期* | 请妥善保管，切勿共享 |

*除非明确撤销或应用访问权限被取消，否则刷新令牌永远不会过期。

## 故障排除

- **刷新时出现 401 Unauthorized 错误**：
  - 可能是应用连接中断，请重新运行步骤 3 中的 OAuth 流程。

- **出现 403 Forbidden 错误**：
  - 请检查 Dropbox 控制台中的应用权限设置。

- **路径错误**：
  - Dropbox 的路径以 `/` 开头，并且不区分大小写
  - 即使在 Windows 系统上，也请使用正斜杠（/）作为路径分隔符。

## API 参考

- OAuth 指南：https://developers.dropbox.com/oauth-guide
- API 探索器：https://dropbox.github.io/dropbox-api-v2-explorer/