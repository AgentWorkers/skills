---
name: linkedin-cli
description: 使用官方的 API v2 将内容发布到 LinkedIn。该 API 需要 OAuth 令牌，因此只有在明确请求或预先安排的情况下才会执行发布操作。
homepage: https://github.com/0xmythril/linkedin-cli
metadata: {"openclaw":{"emoji":"💼","requires":{"bins":["linkedin-cli"],"env":["LINKEDIN_CLIENT_ID","LINKEDIN_CLIENT_SECRET","LINKEDIN_ACCESS_TOKEN"]},"install":[{"id":"npm","kind":"shell","command":"npm install -g github:0xmythril/linkedin-cli#v1.0.0","bins":["linkedin-cli"],"label":"Install linkedin-cli v1.0.0 (npm)"}]}}
---
# linkedin-cli

使用 LinkedIn 的官方 API v2 发布内容到 LinkedIn。该工具受到 LinkedIn 的速率限制，因此**仅当用户明确要求您发布内容时，或通过定时 cron 任务时**才能使用它。切勿未经用户许可就预先编写并发布内容。

## 设置

1. 安装（绑定到特定的发布标签）：
```bash
npm install -g github:0xmythril/linkedin-cli#v1.0.0
```

2. 在 https://www.linkedin.com/developers/apps 创建一个 LinkedIn 应用程序：
   - 启用 **使用 OpenID Connect 登录到 LinkedIn** 和 **在 LinkedIn 上分享** 功能
   - 将 `http://localhost:8585/callback` 添加到 **授权重定向 URL** 中
3. 配置凭据（凭据文件具有受限访问权限）：
```bash
mkdir -p ~/.config/linkedin-cli
touch ~/.config/linkedin-cli/.env
chmod 600 ~/.config/linkedin-cli/.env
cat > ~/.config/linkedin-cli/.env << 'EOF'
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
EOF
```

4. 进行身份验证（会打开浏览器进行 OAuth 验证）：
```bash
linkedin-cli auth
```

5. 验证身份：`linkedin-cli whoami`

## 安全性

- **凭据**：存储在 `~/.config/linkedin-cli/.env` 文件中（运行时由 `dotenv` 读取）。设置 `chmod 600` 以限制访问权限。
- **无安装后脚本**：该包没有安装后脚本——可以通过 `npm pack --dry-run` 进行验证，或查看 `package.json` 文件。
- **无数据传输或网络请求**：除了向 LinkedIn 官方 API (`api.linkedin.com`) 和 OAuth 服务器 (`www.linkedin.com`) 发送请求外，不会进行其他网络操作。
- **固定版本安装**：安装命令会绑定到特定的发布标签。在安装前，请查看源代码仓库：https://github.com/0xmythril/linkedin-cli。
- **依赖项**：仅包含 3 个运行时依赖项：`commander`（用于命令行解析）、`dotenv`（用于加载环境变量）、`open`（用于启动浏览器进行 OAuth 验证）。没有其他间接依赖项。

## 命令

### 验证身份
```bash
linkedin-cli whoami
```

### 进行身份验证
```bash
linkedin-cli auth
```

### 发布文本更新
```bash
linkedin-cli post "Your post text here"
```

### 分享带评论的链接
```bash
linkedin-cli share "https://example.com/article" "Your commentary here"
```

### 删除帖子
```bash
linkedin-cli delete <post-id-urn-or-url>
linkedin-cli delete https://www.linkedin.com/feed/update/urn:li:activity:7654321/
```

## 重要规则

- **除非用户明确要求或通过 cron 任务触发，否则切勿发布内容。**LinkedIn 对 API 的使用有速率限制。
- **发布或分享内容前务必先与用户确认**。请先向用户展示要发布的内容。
- **保持帖子的专业性**——LinkedIn 是一个专业社交平台。
- linkedin-cli 支持原始数字 ID、完整的 URI 以及 LinkedIn 帖子链接。
- 如果收到 401 错误，说明令牌已过期（通常为 60 天）。请让用户运行 `linkedin-cli auth` 重新进行身份验证。
- 该工具仅用于**发布内容**，无法读取动态信息、搜索个人资料或发送消息。