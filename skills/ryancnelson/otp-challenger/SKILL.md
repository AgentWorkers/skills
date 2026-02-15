---
name: otp-challenger
version: 1.0.3
description: 在执行敏感操作之前，启用代理（agents）和技能（skills）来要求用户提供新的双因素认证（TOTP或YubiKey）验证。这可用于审批工作流中的身份验证，包括部署命令、金融操作、数据访问、管理员操作以及变更控制等场景。
metadata: {"openclaw": {"emoji": "🔐", "homepage": "https://github.com/ryancnelson/otp-challenger", "requires": {"bins": ["jq", "python3", "curl", "openssl", "base64"], "anyBins": ["oathtool", "node"]}, "envVars": {"required": [], "conditionallyRequired": [{"name": "OTP_SECRET", "condition": "TOTP mode", "description": "Base32 TOTP secret (16-128 chars)"}, {"name": "YUBIKEY_CLIENT_ID", "condition": "YubiKey mode", "description": "Yubico API client ID"}, {"name": "YUBIKEY_SECRET_KEY", "condition": "YubiKey mode", "description": "Yubico API secret key (base64)"}], "optional": [{"name": "OTP_INTERVAL_HOURS", "default": "24", "description": "Verification validity period"}, {"name": "OTP_MAX_FAILURES", "default": "3", "description": "Failed attempts before rate limiting"}, {"name": "OTP_FAILURE_HOOK", "description": "Script to execute on verification failures (privileged - runs arbitrary commands)"}]}, "privilegedFeatures": ["OTP_FAILURE_HOOK can execute arbitrary shell commands on failure events"], "install": [{"id": "jq", "kind": "brew", "formula": "jq", "bins": ["jq"], "label": "Install jq via Homebrew", "os": ["darwin", "linux"]}, {"id": "python3", "kind": "brew", "formula": "python3", "bins": ["python3"], "label": "Install Python 3 via Homebrew", "os": ["darwin", "linux"]}, {"id": "oathtool", "kind": "brew", "formula": "oath-toolkit", "bins": ["oathtool"], "label": "Install OATH Toolkit via Homebrew", "os": ["darwin", "linux"]}]}}
---

# OTP 身份验证功能

在用户执行敏感操作之前，要求他们通过两步验证（OTP）来验证身份。

## 使用场景

在以下操作前，必须进行 OTP 验证：
- 部署命令（`kubectl apply`、`terraform apply`）
- 财务操作（转账、支付审批）
- 数据访问（个人身份信息（PII）的导出、客户数据操作）
- 管理操作（用户信息修改、权限变更）

## 脚本

### verify.sh

验证用户的 OTP 代码，并记录验证状态。

```bash
./verify.sh <user_id> <code>
```

**参数：**
- `user_id` - 用户标识符（例如：电子邮件、用户名）
- `code` - 6位数的 TOTP 代码或44个字符的 YubiKey OTP 代码

**退出代码：**
- `0` - 验证成功
- `1` - 代码无效或达到验证次数限制
- `2` - 配置错误（缺少密钥、格式不正确）

**验证成功时的输出：**
```
✅ OTP verified for <user_id> (valid for 24 hours)
✅ YubiKey verified for <user_id> (valid for 24 hours)
```

**验证失败时的输出：**
```
❌ Invalid OTP code
❌ Too many attempts. Try again in X minutes.
❌ Invalid code format. Expected 6-digit TOTP or 44-character YubiKey OTP.
```

### check-status.sh

检查用户的 OTP 验证状态是否仍然有效。

```bash
./check-status.sh <user_id>
```

**退出代码：**
- `0` - 用户的 OTP 验证有效（未过期）
- `1` - 用户未通过验证或 OTP 验证已过期

**输出：**
```
✅ Valid for 23 more hours
⚠️ Expired 2 hours ago
❌ Never verified
```

### generate-secret.sh

生成一个新的 TOTP 密钥，并附带 QR 码（需要安装 `qrencode` 工具）。

```bash
./generate-secret.sh <account_name>
```

## 使用方式

```bash
#!/bin/bash
source ../otp/verify.sh

if ! verify_otp "$USER_ID" "$OTP_CODE"; then
  echo "🔒 This action requires OTP verification"
  exit 1
fi

# Proceed with sensitive action
```

## 配置

**TOTP 需要的配置参数：**
- `OTP_SECRET` - Base32 编码的 TOTP 密钥

**YubiKey 需要的配置参数：**
- `YUBIKEY_CLIENT_ID` - Yubico API 客户端 ID
- `YUBIKEY_SECRET_KEY` - Yubico API 密钥（Base64 编码）

**可选参数：**
- `OTP_INTERVAL_HOURS` - OTP 验证的有效期（默认：24小时）
- `OTP_MAX_FAILURES` - 验证失败次数达到限制前的尝试次数（默认：3次）
- `OTP_STATE_FILE` - 验证状态文件的路径（默认：`memory/otp-state.json`）

配置信息可以通过环境变量或 `~/.openclaw/config.yaml` 文件进行设置：

```yaml
security:
  otp:
    secret: "BASE32_SECRET"
  yubikey:
    clientId: "12345"
    secretKey: "base64secret"
```

## 代码类型自动检测

脚本会自动检测代码类型：
- **6位数字** (`123456`) → TOTP 验证
- **44个ModHex字符** (`cccccc...`) → YubiKey 验证

ModHex 字母表：`cbdefghijklnrtuv`

## 验证状态文件

验证状态存储在 `memory/otp-state.json` 文件中。该文件仅包含时间戳，不包含任何密钥信息。

## 人类可读的文档

请参阅 **[README.md](./README.md)**，以获取以下信息：
- 安装说明
- 设置指南（TOTP 和 YubiKey 的使用方法）
- 安全注意事项
- 故障排除方法
- 使用示例