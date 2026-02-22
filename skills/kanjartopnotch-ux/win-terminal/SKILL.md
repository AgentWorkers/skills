---
name: win-terminal
description: 该工具用于控制 Windows 终端，以执行命令、脚本以及管理 Windows 上的进程。它支持 AI 代理执行 git、npm、pip、node 等命令行工具（CLI）的命令。当你需要运行终端命令、管理开发服务器、检查 Git 仓库的状态、安装依赖项或自动化 Windows 命令行工作流程时，可以使用该工具。
---
# Windows Terminal Control

这是一项技能，它使AI代理能够通过PowerShell或Windows Terminal在Windows机器上执行shell命令。非常适合在无需切换上下文的情况下自动化开发工作流程。

## 核心功能

- **运行命令**：可以执行任何命令行工具或脚本（`git`、`npm`、`pip`、`node`、`python`等）。
- **捕获输出**：能够以正确的编码方式读取命令的stdout和stderr。
- **超时保护**：命令会在30秒后自动超时（可配置），以防止程序挂起。
- **工作目录控制**：可以在指定的项目文件夹中执行命令。
- **回退支持**：如果未安装Windows Terminal，该技能会自动切换到PowerShell。

## 使用方法

### 基本命令执行
```powershell
# Check git status
run-command.ps1 -Command "git status" -WorkingDirectory "C:\Users\kanja\projects\my-app"

# Install dependencies
run-command.ps1 -Command "npm install" -WorkingDirectory "C:\Users\kanja\projects\my-app" -TimeoutSeconds 60

# Run a dev server (non-blocking)
run-command.ps1 -Command "npm run dev" -WorkingDirectory "C:\Users\kanja\projects\my-app"
```

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `Command` | 字符串 | 必需 | 要执行的命令 |
| `WorkingDirectory` | 字符串 | 当前目录 | 在该目录中执行命令 |
| `TimeoutSeconds` | 整数 | 30 | 命令的最大等待时间（秒） |
| `NoGui` | 标志 | 假设 | 强制使用PowerShell而不是Windows Terminal |

## 安全性与限制

### 该技能的支持范围
✅ 可以运行标准的CLI工具（如git、npm、pip、python、node等）。
✅ 可以执行PowerShell命令。
✅ 可以读取命令的输出和错误信息。
✅ 可以在任何你有访问权限的目录中操作。
✅ 可以启动后台进程。
✅ 可以处理最大100KB的输出。

### 该技能无法执行的功能
❌ 无法运行交互式命令（如vim、nano、ssh等）。
❌ 无法在未经授权的情况下运行需要管理员权限的命令。
❌ 无法访问工作区之外的其他用户的文件或系统目录。
❌ 无法无限期运行命令（默认超时时间为30秒）。
❌ 无法执行包含危险模式的命令（会进行安全过滤，以防止攻击）。

### 安全防护措施
- **输入安全过滤**：会阻止已知的危险命令模式（防止命令注入攻击）。
- **超时保护**：防止命令挂起。
- **禁止交互模式**：禁止使用交互式工具，以防止程序挂起。
- **仅使用用户权限**：仅以用户的标准Windows权限运行命令。
- **输出限制**：超过100KB的输出会被截断，以防止内存问题。

### 重要说明
- **非沙箱环境**：命令以用户的实际权限运行。该技能会信任用户的输入。
- **GUI命令**：可能引发意外的GUI窗口。
- **网络命令**：如果网络速度较慢，网络命令可能会超时。
- **Windows Terminal与PowerShell的优先级**：如果安装了Windows Terminal，则优先使用Windows Terminal；否则使用PowerShell。

## 先决条件
- Windows 10/11
- PowerShell 5.1或更高版本
- Windows Terminal（可选，但推荐安装）
- PowerShell的执行策略设置为`RemoteSigned`（用于脚本执行）。

## 故障排除

### “命令超时”
增加超时时间：`run-command.ps1 -Command "slow-command" -TimeoutSeconds 120`

### “检测到交互式命令”
使用非交互式的替代方法：
- 用`Get-Content file.txt`代替`vim file.txt`。
- 用`ssh user@host "command"`代替`ssh user@host`。

### “访问被拒绝”
命令可能需要提升权限。OpenClaw会在需要时请求用户授权。

### “找不到Windows Terminal”
该技能会自动切换到PowerShell。建议安装Windows Terminal以获得更好的使用体验。

## 示例
```powershell
# Git workflow
run-command.ps1 -Command "git add ." -WorkingDirectory "C:\projects\my-app"
run-command.ps1 -Command "git commit -m 'Update'" -WorkingDirectory "C:\projects\my-app"

# Python development
run-command.ps1 -Command "pip install -r requirements.txt" -WorkingDirectory "C:\projects\my-app" -TimeoutSeconds 120
run-command.ps1 -Command "python manage.py migrate" -WorkingDirectory "C:\projects\my-app"

# Node.js development
run-command.ps1 -Command "npm run build" -WorkingDirectory "C:\projects\my-app" -TimeoutSeconds 60
run-command.ps1 -Command "npm test" -WorkingDirectory "C:\projects\my-app"

# File operations
run-command.ps1 -Command "Get-ChildItem -Recurse -Filter '*.py' | Select-Object Name" -WorkingDirectory "C:\projects\my-app"
```