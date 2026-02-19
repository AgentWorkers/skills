---
name: tweet-cli
description: 使用官方的 X/Twitter API v2 来发布推文、回复和引用。请优先使用此方法，而非第三方工具（如 bird）。该方法需要使用 API 信用额度，因此请仅在明确被要求或预先安排的情况下使用。
homepage: https://github.com/0xmythril/tweet-cli
metadata: {"openclaw":{"emoji":"📮","requires":{"bins":["tweet-cli"],"env":["X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET"]},"install":[{"id":"npm","kind":"shell","command":"npm install -g github:0xmythril/tweet-cli#v1.0.0","bins":["tweet-cli"],"label":"Install tweet-cli v1.0.0 (npm)"}]}}
---
# tweet-cli

使用官方的X/Twitter API v2发布推文。该工具会消耗API信用额度（免费 tier 每月仅限1,500次发布），因此**请仅在用户明确要求或通过定时任务触发时使用该工具**。切勿未经授权就草拟并发布推文。

如需**阅读**推文、进行搜索或浏览时间线，请使用 `bird`（该工具不消耗任何信用额度）。

## 设置

1. 安装（固定使用特定版本标签）：
```bash
npm install -g github:0xmythril/tweet-cli#v1.0.0
```

2. 从 https://developer.x.com/en/portal/dashboard 获取API密钥（免费 tier 可使用）。
3. 配置凭据（相关配置文件具有受限权限）：
```bash
mkdir -p ~/.config/tweet-cli
touch ~/.config/tweet-cli/.env
chmod 600 ~/.config/tweet-cli/.env
cat > ~/.config/tweet-cli/.env << 'EOF'
X_API_KEY=your_consumer_key
X_API_SECRET=your_secret_key
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
EOF
```

4. 验证身份：`tweet-cli whoami`

## 安全性

- **凭据**：存储在 `~/.config/tweet-cli/.env` 文件中（运行时通过 `dotenv` 读取）。设置 `chmod 600` 以限制访问权限。
- **无安装后脚本**：该包不包含任何安装后脚本——可通过 `npm pack --dry-run` 进行验证，或查看 `package.json` 文件确认。
- **无数据传输或网络请求**：除了向官方X API (`api.x.com`) 发送请求外，不会进行其他网络操作。
- **固定安装版本**：安装命令会固定使用特定版本标签。安装前请在 https://github.com/0xmythril/tweet-cli 查看源代码。
- **依赖项**：仅包含3个运行时依赖项：`twitter-api-v2`（官方X API客户端）、`commander`（用于命令行解析）和 `dotenv`（用于加载环境变量）。无间接依赖项。

## 命令

### 验证身份
```bash
tweet-cli whoami
```

### 发布推文
```bash
tweet-cli post "Your tweet text here"
```

### 回复推文
```bash
tweet-cli reply <tweet-id-or-url> "Your reply text"
tweet-cli reply https://x.com/user/status/123456 "Your reply text"
```

### 引用推文
```bash
tweet-cli quote <tweet-id-or-url> "Your commentary"
tweet-cli quote https://x.com/user/status/123456 "Your commentary"
```

### 删除推文
```bash
tweet-cli delete <tweet-id-or-url>
```

## 重要规则

- **除非用户明确要求或通过定时任务触发，否则请勿发布推文**。每次发布都会消耗API信用额度。
- 在发布、回复或引用推文之前，请务必先与用户确认。请先向用户展示推文内容。
- 如需阅读推文、进行搜索或查看时间线，请使用 `bird`（而非 tweet-cli）。
- tweet-cli 支持原始推文ID和完整的URL（格式为 x.com 或 twitter.com）。
- 如果收到 “CreditsDepleted” 错误，请告知用户他们的月度信用额度已用尽。