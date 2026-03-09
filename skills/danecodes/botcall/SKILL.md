---
name: botcall
description: AI代理的电话号码：用于提供号码、接收短信以及提取验证码。当您需要注册服务、接收两步验证（2FA）代码或进行电话验证时，请使用这些电话号码。
homepage: https://botcall.io
metadata:
  clawdbot:
    emoji: "📱"
    requires:
      env: [BOTCALL_API_KEY]
      bins: [botcall]
    primaryEnv: BOTCALL_API_KEY
    install:
      - id: botcall-cli
        kind: node
        package: botcall
        bins: [botcall]
        label: Install botcall CLI (npm)
---
# botcall – 用于AI代理的电话号码服务

提供电话号码并接收短信验证码。

## 设置

1. 在 [https://botcall.io](https://botcall.io) 获取API密钥。
2. 进行身份验证：
```bash
botcall auth login --api-key bs_live_YOUR_KEY
```

## 命令

### 查看您的套餐和使用情况
```bash
botcall usage
```

### 配置电话号码
```bash
botcall provision
botcall provision --area-code 206  # Seattle area code
```

### 列出您的电话号码
```bash
botcall list
```

### 查看收到的消息
```bash
botcall inbox
botcall inbox --limit 20
```

### 等待验证码
```bash
botcall get-code              # Wait up to 120s
botcall get-code --timeout 60 # Custom timeout
```
仅返回验证码（例如：`847291`），便于解析。

### 释放电话号码
```bash
botcall release <number-id>
```

### 升级套餐
```bash
botcall upgrade starter  # $9/mo - 1 number, 100 SMS
botcall upgrade pro      # $29/mo - 5 numbers, 500 SMS
```

### 管理账单
```bash
botcall billing  # Opens Stripe portal
```

## 示例：注册服务
```bash
# 1. Get a number
botcall provision --area-code 415
# Output: +14155551234

# 2. Use number to sign up (your agent does this)

# 3. Wait for verification code
CODE=$(botcall get-code --timeout 120)
echo "Code received: $CODE"

# 4. Enter code to complete signup
```

## MCP集成

对于Claude Desktop/Cursor，将其添加到您的MCP配置中：
```json
{
  "mcpServers": {
    "botcall": {
      "command": "npx",
      "args": ["@botcallio/mcp"],
      "env": {
        "BOTCALL_API_KEY": "bs_live_YOUR_KEY"
      }
    }
  }
}
```

## 价格

- **免费**：无电话号码（仅限注册）
- **入门级**（$9/月）：1个电话号码，100条短信
- **高级**（$29/月）：5个电话号码，500条短信

## 链接

- 网站：[https://botcall.io](https://botcall.io)
- npm CLI：[https://www.npmjs.com/package/botcall](https://www.npmjs.com/package/botcall)
- MCP：[https://www.npmjs.com/package/@botcallio/mcp](https://www.npmjs.com/package/@botcallio/mcp)