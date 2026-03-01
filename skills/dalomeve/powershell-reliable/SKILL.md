---
name: powershell-reliable
description: 在 Windows 上可靠地执行 PowerShell 命令。避免使用 `&&` 运算符，处理参数解析问题，从中断中恢复，并确保命令在跨会话环境中的连续性。
---
# 在 Windows PowerShell 中可靠地执行命令

在 Windows PowerShell 中可靠地执行命令，避免常见的陷阱，如 `&&` 链式调用、参数被错误处理以及会话中断等问题。

## 问题描述

Windows PowerShell 与 bash 在许多关键方面存在差异：

| 问题 | Bash | PowerShell | 解决方案 |
|-------|------|------------|----------|
| 命令链式调用 | `cmd1 && cmd2` | `cmd1 -ErrorAction Stop; if ($?) { cmd2 }` | 使用分号并进行错误处理 |
| 参数解析 | `-arg value` | `-Argument value`（不区分大小写） | 使用完整的参数名称 |
| 路径分隔符 | `/` | `\`（或在某些 cmdlet 中使用 `/`） | 使用 `Join-Path` |
| 输出重定向 | `>` `>>` | `>` `>>`（可能存在编码问题） | 使用 `Out-File -Encoding UTF8` |
| 环境变量 | `$VAR` | `$env:VAR` | 使用 `$env:` 前缀 |

## 核心模式

### 1. 安全的命令链式调用

**错误示例**：
```powershell
mkdir test && cd test && echo done
```

**正确示例**：
```powershell
$ErrorActionPreference = 'Stop'
try {
    New-Item -ItemType Directory -Path test -Force
    Set-Location test
    Write-Host 'done'
} catch {
    Write-Error "Failed: $_"
    exit 1
}
```

### 2. 参数安全性

**错误示例**：
```powershell
git commit -m "message"
```

**正确示例**：
```powershell
git commit -Message "message"
# Or use splatting:
$params = @{ Message = "message" }
git commit @params
```

### 3. 路径处理

**错误示例**：
```powershell
$path = "C:/Users/name/file.txt"
```

**正确示例**：
```powershell
$path = Join-Path $env:USERPROFILE "file.txt"
# Or use literal paths:
$path = 'C:\Users\name\file.txt'
```

### 4. 输出编码

**错误示例**：
```powershell
echo "text" > file.txt
```

**正确示例**：
```powershell
"text" | Out-File -FilePath file.txt -Encoding UTF8
```

### 5. 会话连续性

对于长时间运行的命令：
```powershell
# Start background job
$job = Start-Job -ScriptBlock {
    param($arg)
    # Long operation
} -ArgumentList $arg

# Wait with timeout
Wait-Job $job -Timeout 300

# Get results
if ($job.State -eq 'Completed') {
    Receive-Job $job
} else {
    Stop-Job $job
    Write-Warning "Job timed out"
}
```

## 错误恢复

### 重试模式
```powershell
function Invoke-Retry {
    param(
        [scriptblock]$Command,
        [int]$MaxAttempts = 3,
        [int]$DelaySeconds = 2
    )
    
    $attempt = 0
    while ($attempt -lt $MaxAttempts) {
        try {
            $attempt++
            return & $Command
        } catch {
            if ($attempt -eq $MaxAttempts) { throw }
            Start-Sleep -Seconds $DelaySeconds
        }
    }
}

# Usage
Invoke-Retry -Command { Invoke-WebRequest -Uri $url } -MaxAttempts 3
```

### 中断恢复
```powershell
# Checkpoint pattern
$checkpointFile = ".checkpoint.json"

if (Test-Path $checkpointFile) {
    $state = Get-Content $checkpointFile | ConvertFrom-Json
    Write-Host "Resuming from step $($state.step)"
} else {
    $state = @{ step = 0 }
}

switch ($state.step) {
    0 { 
        # Step 1
        $state.step = 1
        $state | ConvertTo-Json | Out-File $checkpointFile
    }
    1 {
        # Step 2
        Remove-Item $checkpointFile
    }
}
```

## 隐私与安全性

- **所有执行操作都是本地进行的**：
  - 不将命令日志发送到外部服务
  - 脚本中不会捕获任何凭据
  - 不会自动上传执行结果
  - 敏感数据通过 `[SecureString]` 进行处理
  - 检点文件仅存储在工作目录中

**敏感数据过滤**：
  - 在写入任何检查点或日志之前：
    - 排除 `Password`、`Token`、`Secret`、`ApiKey`
    - 使用 `[SecureString]` 来存储凭据
    - 绝不显示敏感变量

## 可执行命令的完成标准

一个 PowerShell 命令的执行只有在满足以下条件时才被认为是可靠的：

| 标准 | 验证方法 |
|----------|-------------|
| 无 `&&` 链式调用 | `Select-String '&&' script.ps1` 无输出 |
| 有错误处理 | `Select-String 'try|catch|ErrorAction' script.ps1` 匹配 |
| 路径使用 `Join-Path` | `Select-String 'Join-Path|\\$env:' script.ps1` 匹配 |
| 指定了输出编码 | `Select-String 'Out-File.*Encoding' script.ps1` 匹配 |
| 长时间运行的操作有检查点 | 超过 60 秒的操作有检查点文件 |
| 无硬编码的敏感信息 | `Select-String 'password|token|secret' script.ps1` 无输出 |

## 快速参考

### 常用 cmdlet 的对应关系

| 任务 | Bash | PowerShell |
|------|------|------------|
| 列出文件 | `ls -la` | `Get-ChildItem -Force` |
| 更改目录 | `cd /path` | `Set-Location C:\path` |
| 创建目录 | `mkdir x` | `New-Item -ItemType Directory x` |
| 复制文件 | `cp a b` | `Copy-Item a b` |
| 移动文件 | `mv a b` | `Move-Item a b` |
| 删除文件 | `rm x` | `Remove-Item x` |
| 查看文件内容 | `cat x` | `Get-Content x` |
| 编辑文件 | `vim x` | `notepad x` |
| 查找文本 | `grep x` | `Select-String x` |
| 管道传输 | `\|` | `\|`（相同功能） |
| 重定向输出 | `>` | `>`（使用 `Out-File`） |

### 模板示例
```powershell
$params = @{
    Path = $filePath
    Encoding = 'UTF8'
    Force = $true
}
Set-Content @params
```

## 参考资料

- `references/privacy-checklist.md` - 隐私与安全性检查清单
- Microsoft 文档：[PowerShell 最佳实践](https://docs.microsoft.com/powershell)

---

**可靠执行。优雅恢复。**