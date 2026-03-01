---
name: model-route-guard
description: 诊断并解决模型路由冲突问题。确保主模型使用正确的提供者端点，避免出现重复的覆盖（即多个配置同时生效的情况）。
---
# 模型路由保护（Model Route Guard）

用于解决模型路由和提供者端点之间的冲突问题。

## 问题

模型路由问题可能导致以下情况：
- 使用了错误的提供者端点
- 提供者定义重复
- 代理（agent）的覆盖设置与全局配置冲突
- 系统默认使用错误的模型

## 工作流程

### 1. 路由审计（Route Audit）

```powershell
# Check global config
$cfg = Get-Content "$HOME/.openclaw/openclaw.json" -Raw | ConvertFrom-Json
$globalBase = $cfg.models.providers.bailian.baseUrl
$globalModel = $cfg.agents.defaults.model.primary

# Check agent overrides
$agentCfgPath = "$HOME/.openclaw/agents/main/agent/models.json"
if (Test-Path $agentCfgPath) {
    $agentCfg = Get-Content $agentCfgPath -Raw | ConvertFrom-Json
    $agentBase = $agentCfg.providers.bailian.baseUrl
}

"Global baseUrl = $globalBase"
"Global model   = $globalModel"
"Agent baseUrl  = $agentBase"

# Detect conflicts
if ($globalBase -ne $agentBase) {
    Write-Warning "Provider URL mismatch between global and agent config"
}
```

### 2. 解决冲突（Fix Conflicts）

```powershell
# Correct endpoint (coding.dashscope, not coding-intl)
$correctUrl = "https://coding.dashscope.aliyuncs.com/v1"

# Update global config
$cfg.models.providers.bailian.baseUrl = $correctUrl
$cfg | ConvertTo-Json -Depth 10 | Out-File "$HOME/.openclaw/openclaw.json" -Encoding UTF8

# Remove conflicting agent override
if (Test-Path $agentCfgPath) {
    Remove-Item $agentCfgPath -Force
}

# Restart
openclaw gateway restart
```

### 3. 验证（Verification）

```powershell
# Test model call
openclaw models list

# Check active route
openclaw status
```

## 可执行任务的完成标准（Executable Completion Criteria）

| 标准 | 验证内容 |
|----------|-------------|
| 是否存在单一提供者URL | 配置文件中仅存在一个 `bailian.baseUrl` |
| 端点是否正确 | 端点地址是否为 `coding.dashscope.aliyuncs.com` |
| 是否存在重复的覆盖设置 | `models.json` 文件已被删除或内容已统一 |
| 模型调用是否成功 | `openclaw models list` 命令能否正常执行 |

## 隐私/安全要求（Privacy/Safety）

- 审计输出中不包含API密钥
- 对API密钥的值进行遮盖（仅显示前4个字符）
- 仅记录配置文件内容，不进行外部日志记录

## 自动触发条件（Self-Use Trigger）

在以下情况下触发该流程：
- 模型调用因端点错误而失败
- 配置文件中显示多个提供者定义
- 网关重启后出现模型相关问题
- 系统默认使用错误模型

---

**原则：**  
“一条路由，一个权威的数据来源。”（One route, one source of truth.）