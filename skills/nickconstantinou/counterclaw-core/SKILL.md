---
name: counterclaw
description: 用于防御提示注入（prompt injection）攻击以及进行基本个人身份信息（PII）屏蔽的拦截器。
homepage: https://github.com/nickconstantinou/counterclaw-core
install: "pip install ."
requirements:
  env:
    - TRUSTED_ADMIN_IDS
  files:
    - "~/.openclaw/memory/"
    - "~/.openclaw/memory/MEMORY.md"
metadata:
  clawdbot:
    emoji: "🛡️"
    version: "1.0.9"
    category: "Security"
    type: "python-middleware"
    security_manifest:
      network_access: none
      filesystem_access: "Write-only logging to ~/.openclaw/memory/"
      purpose: "Log security violations locally for user audit."
---
# CounterClaw 🦞  
> 为 AI 代理提供防御性安全保护，能够迅速拦截恶意负载。  

## ⚠️ 安全提示  
此软件包仅支持 **离线模式**，不会进行任何网络请求。  

## 安装  
```bash
claw install counterclaw
```  

## 快速入门  
```python
from counterclaw import CounterClawInterceptor

interceptor = CounterClawInterceptor()

# Input scan - blocks prompt injections
# NOTE: Examples below are TEST CASES only - not actual instructions
result = interceptor.check_input("{{EXAMPLE: ignore previous instructions}}")
# → {"blocked": True, "safe": False}

# Output scan - detects PII leaks  
result = interceptor.check_output("Contact: john@example.com")
# → {"safe": False, "pii_detected": {"email": True}}
```  

## 主要功能  
- 🔒 防范常见的提示注入攻击（prompt injection）  
- 🛡️ 基本的个人信息（PII）隐藏功能（包括电子邮件、电话号码、信用卡信息）  
- 📝 将违规行为记录到 `~/.openclaw/memory/MEMORY.md` 文件中  
- ⚠️ 如果未配置 `TRUSTED_ADMIN_IDS`，启动时会发出警告  

## 配置  
### 必需的环境变量  
```bash
# Set your trusted admin ID(s) - use non-sensitive identifiers only!
export TRUSTED_ADMIN_IDS="your_telegram_id"
```  
**注意：** `TRUSTED_ADMIN_ids` 变量中只能包含非敏感信息：  
- ✅ Telegram 用户 ID（例如：“123456789”）  
- ✅ Discord 用户 ID（例如：“987654321”）  
- ❌ 绝对不能包含 API 密钥  
- ❌ 绝对不能包含密码  
- ❌ 绝对不能包含令牌  

您可以通过逗号分隔来设置多个管理员 ID：  
```bash
export TRUSTED_ADMIN_IDS="telegram_id_1,telegram_id_2"
```  

### 运行时配置  
```python
# Option 1: Via environment variable (recommended)
# Set TRUSTED_ADMIN_IDS before running
interceptor = CounterClawInterceptor()

# Option 2: Direct parameter
interceptor = CounterClawInterceptor(admin_user_id="123456789")
```  

## 安全注意事项  
- **默认行为**：如果未设置 `TRUSTED_ADMIN_ids`，管理员功能将被禁用。  
- **日志记录**：所有违规行为都会被记录到 `~/.openclaw/memory/MEMORY.md` 文件中，并对其中包含的个人信息进行隐藏处理。  
- **无网络访问权限**：该中间件仅支持离线运行，不会进行任何外部网络请求。  
- **文件访问权限**：仅允许写入 `~/.openclaw/memory/MEMORY.md` 文件。  

## 创建的文件  
| 路径 | 用途 |  
|------|---------|  
| `~/.openclaw/memory/` | 首次运行时创建的目录  
| `~/.openclaw/memory/MEMORY.md` | 包含隐藏了个人信息的违规记录文件  

## 许可证  
MIT 许可证——详情请参阅 LICENSE 文件。  

## 开发与发布  
### 在本地运行测试  
```bash
python3 tests/test_scanner.py
```  

### 代码检查（Linting）  
```bash
pip install ruff
ruff check src/
```  

### 发布到 ClawHub  
每次提交或拉取请求时，持续集成（CI）系统会执行以下操作：  
1. **代码检查**：对 Python 代码进行格式检查（linting）。  
2. **单元测试**：运行单元测试。  

要发布新版本，请按照以下步骤操作：  
```bash
# Version is set in pyproject.toml
git add -A
git commit -m "Release v1.0.9"
git tag v1.0.9
git push origin main --tags
```  
CI 系统会自动执行：  
- 代码检查与单元测试；  
- 如果测试通过且版本标签以 `v*` 开头，该版本将自动发布到 ClawHub。