---
name: powerskills-system
description: 通过 PowerShell 使用 Windows 系统命令和信息。可以执行 shell 命令、获取系统信息（主机名、操作系统、运行时间）、列出顶级进程以及读取环境变量。当需要运行命令、检查系统状态或查看 Windows 环境时，可以使用这些功能。
license: MIT
metadata:
  author: aloth
  cli: powerskills
  parent: powerskills
---
# PowerSkills — 系统管理

Shell命令、进程管理、系统信息。

## 要求

- 必须安装PowerShell 5.1或更高版本。

## 操作命令

```powershell
.\powerskills.ps1 system <action> [--params]
```

| 操作        | 参数            | 描述                                      |
|------------|-----------------|-------------------------------------------|
| `exec`       | `--command "whoami" [--timeout 30]` | 运行PowerShell命令                        |
| `info`       |                | 显示系统信息：主机名、操作系统、用户、域名、架构、运行时间        |
| `processes`   | `--limit N`        | 显示CPU使用率最高的N个进程（默认值：20）              |
| `env`       | `--name PATH`       | 获取环境变量的值                          |

## 使用示例

```powershell
# Run a command
.\powerskills.ps1 system exec --command "Get-Process | Select -First 5"

# System info
.\powerskills.ps1 system info

# Top 10 CPU consumers
.\powerskills.ps1 system processes --limit 10

# Check an env var
.\powerskills.ps1 system env --name COMPUTERNAME
```

## 输出字段

### info
- `hostname`：主机名
- `user`：当前用户
- `domain`：域名
- `os`：操作系统
- `arch`：系统架构
- `ps_version`：PowerShell版本
- `uptime_hours`：系统运行时间（以小时为单位）

### processes
- `name`：进程名称
- `pid`：进程ID
- `cpu`：CPU使用率
- `mem_mb`：进程内存占用（以MB为单位）

### exec
- `stdout`：命令的输出结果
- `stderr`：命令的错误输出
- `exit_code`：命令的退出状态码