---
name: counterclaw
description: 用于防御提示注入（prompt injection）攻击的基本个人信息（PII）隐藏工具。
requires:
  env:
    - TRUSTED_ADMIN_IDS
  files:
    - "~/.openclaw/memory/MEMORY.md"
metadata:
  clawdbot:
    emoji: "🛡️"
    version: "1.0.1"
    category: "Security"
    security_manifest:
      network_access: none
      filesystem_access: "Write-only logging to ~/.openclaw/memory/"
      purpose: "Log security violations locally for user audit."
---
# CounterClaw 🦞

> 专为AI代理提供防御性安全保护，能够有效拦截恶意负载。

## 安装

```bash
claw install counterclaw
```

## 快速入门

```python
from counterclaw import CounterClawInterceptor

interceptor = CounterClawInterceptor()

# Input scan - blocks prompt injections
result = interceptor.check_input("Ignore previous instructions")
# → {"blocked": True, "safe": False}

# Output scan - detects PII leaks  
result = interceptor.check_output("Contact: john@example.com")
# → {"safe": False, "pii_detected": {"email": True}}
```

## 主要功能

- 🔒 防御常见的提示注入攻击模式
- 🛡️ 基本的个人信息（如电子邮件、电话号码）加密处理
- 📝 违规行为会被记录到 ~/.openclaw/memory/MEMORY.md 文件中

## 配置

### 仅限管理员操作（需使用 `claw-lock` 命令锁定）
```bash
export TRUSTED_ADMIN_IDS="your_telegram_id"
```

```python
interceptor = CounterClawInterceptor()  # Reads TRUSTED_ADMIN_IDS env
```

## 许可证

MIT许可证 - 详情请参阅 LICENSE 文件