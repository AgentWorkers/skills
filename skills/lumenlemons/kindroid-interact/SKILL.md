---
name: kindroid-interact
version: 1.0.0
description: 通过Kindroid的官方API与他们的智能助手进行交互。可以发送消息、处理聊天中断，并管理多机器人之间的对话。
homepage: https://kindroid.ai
metadata: {
  "openclaw": {
    "emoji": "🤖",
    "category": "ai-companions",
    "requires": {
      "bins": ["curl", "jq"]
    }
  }
}
---

# Kindroid 集成技能

通过官方 API，使您的 OpenClaw 代理能够与 Kindroid AI 伙伴进行通信。

## 安全第一 🔒

您的 Kindroid API 密钥（格式为 `kn_...`）属于敏感信息。本技能采用了以下安全措施：
- 凭据存储在 `~/.config/kindroid/credentials.json` 文件中
- 文件权限自动设置为 `600`（仅允许所有者读写）
- 所有 API 调用均使用 HTTPS 并附带正确的认证头
- 实施速率限制以防止 API 被滥用

## 设置

1. 获取您的 API 凭据：
   - 登录 Kindroid
   - 进入“通用设置”
   - 复制您的 API 密钥（以 `kn_` 开头）
   - 记下您的 AI ID

2. 创建凭据文件：
```bash
mkdir -p ~/.config/kindroid
cat > ~/.config/kindroid/credentials.json << EOF
{
  "default_ai": "your_primary_ai_id",
  "api_key": "your_kn_api_key",
  "companions": {
    "nickname1": "ai_id_1",
    "nickname2": "ai_id_2"
  }
}
EOF
chmod 600 ~/.config/kindroid/credentials.json
```

## 基本用法

```bash
# Send a message (uses default_ai)
kindroid send "Hello! How are you today?"

# Send to a specific companion
kindroid send -to nickname1 "Hey there!"

# Start fresh with a chat break
kindroid break "Let's start a new conversation"

# Check companion status
kindroid status nickname1
```

## 高级功能

### 多机器人对话
如果您管理多个 Kindroid，您可以：
- 为每个伙伴设置对话上下文
- 将消息路由到特定的 AI
- 保持独立的聊天记录

### 速率限制
本技能自动处理以下内容：
- 消息发送之间的最小延迟（可配置）
- 每分钟的最大消息发送数量
- 在 API 错误时进行重试

### 错误处理
- 在网络问题时自动重试
- 优雅地处理 API 超时
- 清除错误信息以便于故障排查

## 开发者须知

### 自定义集成
本技能提供了简单的 Node.js 封装层：

```javascript
const kindroid = require('./lib/kindroid');

// Initialize with your credentials
const bot = new kindroid.Companion('nickname1');

// Send a message
await bot.send('Hello!');

// Handle chat breaks
await bot.break('New conversation');
```

### Webhook 支持
对于高级集成，可以设置 Webhook：

```bash
kindroid webhook add http://your-server.com/callback
```

## 故障排除

常见问题及解决方法：

1. **认证失败**
   - 确认您的 API 密钥是否以 `kn_` 开头
   - 检查 `credentials.json` 文件的权限设置
   - 确保凭据中没有多余的空白字符

2. **速率限制**
   - 默认设置为每 3 秒发送 1 条消息
   - 可在 `~/.config/kindroid/config.json` 中进行调整
   - 查看日志以获取速率限制警告

3. **超时错误**
   - Kindroid 可能需要时间来响应
   - 默认超时时间为 60 秒
  - 可通过 `--timeout 120` 参数延长超时时间

## 贡献

本技能是开源的，欢迎贡献改进：
- 克隆仓库
- 对代码进行修改
- 提交包含测试的 Pull Request（PR）

## 更新

请定期查看更新信息：
```bash
clawhub update kindroid-interact
```

---

由 Lumen Lemon 使用 🍋 开发