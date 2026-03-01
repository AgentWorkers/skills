---
name: gateway-token-doctor
description: 诊断并修复导致 401 错误的网关令牌不匹配问题。确保配置文件、服务接口以及命令行界面（CLI）中的令牌信息保持一致。
---
# Gateway Token Doctor

用于诊断并修复由于令牌不匹配导致的 401 错误。

## 问题

Gateway 令牌不一致会导致以下问题：
- 401 “未经授权” 错误
- 命令行界面（CLI）/用户界面（UI）认证失败
- 服务启动失败
- 认证功能逐渐失效

## 工作流程

### 1. 令牌审计

```powershell
# Check all token surfaces
$cfg = Get-Content "$HOME/.openclaw/openclaw.json" -Raw | ConvertFrom-Json
$auth = $cfg.gateway.auth.token
$remote = $cfg.gateway.remote.token
$service = $env:OPENCLAW_GATEWAY_TOKEN

"auth.token   = $auth"
"remote.token = $remote"
"service.token = $service"

if ($auth -and $remote -and $auth -ne $remote) {
    Write-Warning "Token mismatch: auth != remote"
}
```

### 2. 令牌对齐修复

```powershell
# Generate or use existing token
$token = $auth

# Update config
$cfg.gateway.auth.token = $token
$cfg.gateway.remote.token = $token
$cfg | ConvertTo-Json -Depth 10 | Out-File "$HOME/.openclaw/openclaw.json" -Encoding UTF8

# Update service startup script
$servicePath = "$HOME/.openclaw/gateway.cmd"
$content = Get-Content $servicePath -Raw
$content = $content -replace 'OPENCLAW_GATEWAY_TOKEN=.*', "OPENCLAW_GATEWAY_TOKEN=$token"
$content | Out-File $servicePath -Encoding UTF8

# Restart
openclaw gateway restart
```

### 3. 验证

```powershell
# Test gateway access
openclaw gateway status

# Test CLI auth
openclaw whoami
```

## 可执行操作完成标准

| 标准 | 验证内容 |
|----------|-------------|
| 所有令牌对齐 | `auth`、`remote` 和 `service` 的值一致 |
| Gateway 返回响应 | `openclaw gateway status` 命令执行成功 |
| CLI 认证正常工作 | `openclaw whoami` 命令能返回用户信息 |
| 日志中无 401 错误 | `Select-String "401"` 命令在日志中未找到相关记录 |

## 隐私/安全注意事项

- 绝不记录实际的令牌值
- 在输出结果中仅显示令牌的前 4 个字符
- 令牌仅存储在配置文件中

## 使用场景

- 当出现 401 错误时
- 在配置更改后重启 Gateway 时
- 当 CLI 显示认证不匹配时
- 当服务无法启动时

---

**对齐令牌，恢复访问权限。**