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
    version: "1.1.0"
    category: "Security"
    type: "python-middleware"
    security_manifest:
      network_access: "optional (only when using email integration scripts)"
      filesystem_access: "Write-only logging to ~/.openclaw/memory/"
      purpose: "Log security violations locally for user audit."
---
# CounterClaw 🦞  
> 为AI代理提供防御性安全保护，能够迅速拦截恶意负载。  

## ⚠️ 安全提示  
该软件包有两种运行模式：  
1. **核心扫描器（离线模式）**：`check_input()` 和 `check_output()`——不进行任何网络请求  
2. **电子邮件集成（联网模式）**：`send_protected_email.sh`——需要使用gog CLI来处理Gmail邮件  

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

## 主要功能：  
- 🔒 防御常见的提示注入攻击（prompt injection）  
- 🛡️ 对个人信息（如电子邮件地址、电话号码、信用卡信息）进行基本屏蔽  
- 📝 将违规行为记录到 `~/.openclaw/memory/MEMORY.md` 文件中  
- ⚠️ 如果未配置 `TRUSTED_ADMIN_IDS`，程序启动时会发出警告  

## 配置  
### 必需的环境变量  
```bash
# Set your trusted admin ID(s) - use non-sensitive identifiers only!
export TRUSTED_ADMIN_IDS="your_telegram_id"
```  
**重要提示：** `TRUSTED_ADMIN_IDS` 变量中只能包含非敏感信息：  
- ✅ Telegram用户ID（例如：“123456789”）  
- ✅ Discord用户ID（例如：“987654321”）  
- ❌ 绝对不能包含API密钥、密码或令牌  

可以通过逗号分隔多个管理员ID：  
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

## 安全注意事项：  
- **默认设置**：如果未设置 `TRUSTED_ADMIN_IDS`，管理员功能将被禁用。  
- **日志记录**：所有违规行为都会被记录到 `~/.openclaw/memory/MEMORY.md` 文件中，并对个人信息进行屏蔽处理。  
- **无网络访问**：该中间件仅支持离线运行，不会进行任何外部网络请求。  
- **文件访问权限**：仅允许写入 `~/.openclaw/memory/MEMORY.md` 文件。  

## 创建的文件  
| 路径        | 用途                |  
|-------------|------------------|  
| `~/.openclaw/memory/` | 首次运行时创建的目录          |  
| `~/.openclaw/memory/MEMORY.md` | 包含屏蔽后的违规记录的文件    |  

## 许可证  
MIT许可证——详见 LICENSE 文件  

## 开发与发布  
### 本地测试  
```bash
python3 tests/test_scanner.py
```  

### 代码检查（Linting）  
```bash
pip install ruff
ruff check src/
```  

### 发布到ClawHub  
每当有推送或拉取请求时，CI系统会自动执行以下操作：  
1. **代码检查（Linting）**：对Python代码进行格式检查。  
2. **单元测试（Tests）**：运行单元测试。  

要发布新版本，请按照以下步骤操作：  
```bash
# Version is set in pyproject.toml
git add -A
git commit -m "Release v1.0.9"
git tag v1.0.9
git push origin main --tags
```  
CI系统会自动完成以下操作：  
- 运行代码检查与单元测试；  
- 如果测试通过且版本标签以 `v*` 开头，该版本将自动发布到ClawHub。