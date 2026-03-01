---
name: powershell-safe-chain
description: 安全地链式执行 PowerShell 命令（即连续执行多个 PowerShell 命令），无需使用 `&&` 运算符。通过使用 `try/catch` 语句、`ErrorAction` 属性以及正确的命令执行顺序，可以确保在 Windows 环境中命令能够可靠地运行。
---
# PowerShell 安全命令链

在 Windows PowerShell 中可靠地执行命令链操作，避免使用 `&&` 这种反模式（即避免错误导致后续命令继续执行）。

## 问题

PowerShell 与 bash 有以下不同：
- `&&` 不能用于命令链操作
- 参数解析不区分大小写，但要求严格匹配
- 默认情况下，错误会继续执行后续命令（没有快速失败机制）
- 路径分隔符因操作系统而异（`\` 与 `/`）

## 工作流程

### 1. 安全命令链模式

**错误做法：**
```powershell
mkdir test && cd test && echo done
```

**正确做法：**
```powershell
$ErrorActionPreference = 'Stop'
try {
    New-Item -ItemType Directory -Path test -Force
    Set-Location test
    Write-Host 'done'
} catch {
    Write-Error "Failed at step: $_"
    exit 1
}
```

### 2. 条件命令链

```powershell
# If-then pattern
if (Test-Path $file) {
    Remove-Item $file
    Write-Host "Deleted"
} else {
    Write-Warning "File not found"
}

# Pipeline with error handling
Get-Process | Where-Object CPU -GT 100 | Stop-Process -WhatIf
```

### 3. 复杂命令的分组执行

```powershell
$params = @{
    Path = $filePath
    Encoding = 'UTF8'
    Force = $true
}
Set-Content @params
```

## 可执行脚本的验证标准

| 标准 | 验证方法 |
|--------|-------------|
| 脚本中不使用 `&&` | `Select-String '&&' *.ps1` 会返回空结果 |
| 设置了 `ErrorAction` | `Select-String 'ErrorAction' *.ps1` 会匹配相关脚本 |
| 包含 `try/catch` 语句 | `Select-String 'try|catch' *.ps1` 会匹配相关脚本 |
| 路径使用 `Join-Path` | `Select-String 'Join-Path' *.ps1` 会匹配相关脚本 |

## 隐私/安全注意事项

- 不要硬编码凭证信息
- 使用 `[SecureString]` 类型来存储密码
- 通过 `$env:VAR` 访问环境变量

## 自我使用场景

适用于以下情况：
- 编写 PowerShell 脚本
- 链接多个命令
- 执行文件操作

---

**安全地执行命令链操作。确保错误能够被及时处理。**