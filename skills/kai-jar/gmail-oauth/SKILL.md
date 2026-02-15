---
name: gmail-oauth
description: 通过 `gog CLI` 和手动 OAuth 流程来设置 Gmail API 访问权限。此方法适用于设置 Gmail 集成、续期过期的 OAuth 令牌，或在无头服务器上解决 Gmail 认证问题。
---

# Gmail OAuth 设置

使用 `gog` CLI 实现的无头（headless）方式访问 Gmail API 的 OAuth 流程。

## 先决条件

- 已安装 `gog` CLI（通过 `brew install steipete/tap/gogcli` 安装）
- 拥有包含 OAuth 凭据的 Google Cloud 项目（桌面应用类型）
- 项目中已启用 Gmail API

## 快速设置

### 1. 创建 Google Cloud 项目及凭证

1. 访问 https://console.cloud.google.com
2. 创建一个新的项目（或选择现有项目）
3. **启用 Gmail API**：点击 “APIs & Services” → “Library”，搜索 “Gmail API” 并启用它
4. **配置 OAuth 同意页面**：点击 “APIs & Services” → “OAuth consent screen”：
   - 选择 “External” 用户类型
   - 填写应用名称和用户支持邮箱
   - 添加权限范围：`gmail.modify`（根据需要添加其他权限）
   - **重要**：点击 “PUBLISH APP” 以获取永久性访问令牌（详见故障排除部分）
5. **创建凭证**：点击 “APIs & Services” → “Credentials” → “Create Credentials” → “OAuth client ID”：
   - 应用类型：**Desktop app**
   - 下载 JSON 凭证文件

### 2. 配置 `gog`

```bash
gog auth credentials /path/to/client_secret.json
gog auth keyring file  # Use file-based keyring for headless
export GOG_KEYRING_PASSWORD="your-password"  # Add to .bashrc
```

### 3. 运行授权流程

交互式运行 `scripts/gmail-auth.sh` 脚本，或：

```bash
# Generate URL
scripts/gmail-auth.sh --url

# User opens URL, approves, copies code from localhost redirect
# Exchange code (do this quickly - codes expire in minutes!)
scripts/gmail-auth.sh --exchange CODE EMAIL
```

### 4. 验证授权结果

```bash
gog gmail search 'is:unread' --max 5 --account you@gmail.com
```

## 故障排除

### “访问被阻止：[应用] 未完成 Google 验证流程”

**原因**：应用处于 “测试” 模式，且使用的 Gmail 账户不是测试用户。

**解决方案**（选择一种）：
1. **发布应用**（推荐）：
   - 进入 Google Cloud 控制台 → “APIs & Services” → “OAuth consent screen”
   - 点击 “PUBLISH APP” 并确认
   - 个人使用无需经过 Google 审核
   - 令牌将变为永久性访问令牌

2. **添加测试用户**：
   - 在 OAuth 同意页面中选择 “Test users” → 添加需要授权的 Gmail 账户
   - 注意：这些令牌仍然会在 7 天后过期

### “Google 未验证此应用” 的警告

**对于个人应用来说这是正常的。** 点击：
1. 选择 “Advanced”（左下角）
2. 点击 “Go to [应用名称]”（虽然提示不安全，但可以继续操作）

由于你是应用的所有者，因此可以安全地继续使用。

### 令牌在 7 天后过期

**原因**：应用仍处于 “测试” 模式。

**解决方法**：发布应用（参见上述步骤）。发布后的应用将获得永久性访问令牌。

### 出现 “invalid_request” 或 “invalid_grant” 错误

**原因**：
- 授权代码已过期（有效期通常只有几分钟）
- 代码已被使用
- 重定向 URI 不匹配

**解决方法**：生成新的授权 URL 并尽快完成授权流程。获取代码后立即使用它。

### 出现 “redirect_uri_mismatch” 错误

**原因**：令牌交换过程中使用的重定向 URI 与授权 URL 中指定的 URI 不匹配。

**解决方法**：此脚本使用的是 `http://localhost` 作为重定向 URI。请确保授权 URL 和令牌交换过程中使用的重定向 URI 一致。

### 批准权限后页面卡住（在移动设备上）

**原因**：移动设备上的浏览器无法连接到本地主机（localhost）。

**解决方法**：
- 使用桌面浏览器
- 或者在页面卡住时点击地址栏（URL 中包含授权代码）
- URL 的格式应为：`http://localhost/?code=4/0ABC...`

### 同时勾选多个权限选项导致页面卡住

**原因**：请求的 OAuth 权限范围过多。

**解决方法**：仅请求必要的权限范围。通常 `gmail.modify` 即可满足大部分需求，且只会显示一个权限选项。

### 在 Google Cloud 控制台中找不到项目

**原因**：登录了错误的 Google 账户。

**解决方法**：
- 点击右上角的个人资料图标
- 切换账户
- 检查每个账户对应的项目列表

### 新项目中出现 “invalid_request” 错误（与 oob 重定向相关）

**原因**：对于 2022 年之后创建的 OAuth 客户端，Google 已弃用了 `urn:ietf:wg:oauth:2.0:oob` 协议。

**解决方法**：使用 `http://localhost` 作为重定向 URI（此脚本的默认设置）。授权成功后，浏览器会自动跳转到 `http://localhost` 并在 URL 中显示授权代码。

## 权限范围参考

| 权限范围 | 访问权限 |
|-------|--------|
| `gmail.modify` | 读取、发送、删除邮件、管理标签（推荐） |
| `gmail.readonly` | 仅限读取 |
| `gmail.send` | 仅限发送邮件 |
| `gmailCompose` | 创建邮件草稿并发送 |

## 相关文件

- `scripts/gmail-auth.sh` — 交互式授权辅助脚本

## 提示

- **发布你的应用**：避免受到测试用户的使用限制和 7 天令牌有效期的限制
- **尽快交换授权代码**：代码的有效期很短
- **使用桌面浏览器**：移动浏览器可能无法正确处理本地主机（localhost）的请求
- **只需一个权限范围**：`gmail.modify` 通常足以满足大部分使用需求