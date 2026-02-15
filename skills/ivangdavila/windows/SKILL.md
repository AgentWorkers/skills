---
name: Windows
description: 在 Windows 系统中，存在一些特定的模式、安全实践以及操作上的陷阱，这些因素可能导致系统出现“无声故障”（即故障发生时没有明显的错误提示或警报）。
metadata:
  category: system
  skills: ["windows", "powershell", "security", "automation"]
---

## 凭据管理

- **切勿在脚本中硬编码密码**——请使用 Windows 凭据管理器：
  ```powershell
  # Store
  cmdkey /generic:"MyService" /user:"admin" /pass:"secret"
  # Retrieve in script
  $cred = Get-StoredCredential -Target "MyService"
  ```

- **对于脚本，应使用 `Get-Credential` 并安全地导出凭据**：
  ```powershell
  $cred | Export-Clixml -Path "cred.xml"  # Encrypted to current user/machine
  $cred = Import-Clixml -Path "cred.xml"
  ```

## 隐性故障处理

- Windows Defender 会自动将下载的脚本或可执行文件放入隔离区——如果脚本消失，请检查隔离区。
- 组策略会悄悄地覆盖本地设置——使用 `gpresult /r` 来查看实际应用了哪些设置。
- 防病毒软件的实时扫描功能可能会间歇性地阻止文件操作——请为构建或自动化文件夹添加例外规则。
- PowerShell 的 `-ErrorAction SilentlyContinue` 会隐藏错误——建议使用 `Stop` 并手动处理错误。

## 符号链接

- 创建符号链接需要管理员权限或 `SeCreateSymbolicLinkPrivilege` 权限——普通用户会遇到操作失败的情况。
- 可以在不使用管理员权限的情况下启用符号链接的开发者模式：设置 → 开发者选项 → 开发者模式。
- `mklink` 命令仅适用于 CMD，PowerShell 使用 `New-Item -ItemType SymbolicLink` 来创建符号链接。

## 脚本签名

- 未签名的脚本在受限环境中会引发错误，并且错误信息可能难以理解——在生产环境中请务必对脚本进行签名：
  ```powershell
  $cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert
  Set-AuthenticodeSignature -FilePath script.ps1 -Certificate $cert
  ```

## 操作安全

- 对于具有破坏性的操作，务必先使用 `-WhatIf` 选项进行测试：
  `Remove-Item -Recurse -WhatIf`
- 使用 `Start-Transcript` 命令记录操作日志——以便在出现问题时进行调查。
- NTFS 权限管理：可以使用 `icacls` 命令进行设置，但权限继承规则可能比较复杂——在更改权限前请先在测试环境中进行测试。

## WinRM 远程控制

- 正确地启用 WinRM 远程功能：仅使用 `Enable-PSRemoting -Force` 是不够的——工作组环境还需要配置 `TrustedHosts`：
  `Set-Item WSMan:\localhost\Client\TrustedHosts -Value "server1,server2"`
- HTTPS 远程连接需要设置证书——否则网络上的其他设备可以读取用户的凭据。

## 事件日志记录

- 脚本应记录到 Windows 事件日志中，以便进行集中监控：
  ```powershell
  New-EventLog -LogName Application -Source "MyScript" -ErrorAction SilentlyContinue
  Write-EventLog -LogName Application -Source "MyScript" -EventId 1000 -Message "Started"
  ```

- 自定义事件源的创建需要管理员权限——请在安装脚本时设置好，而不是在运行时。

## 文件锁定

- Windows 会对文件进行严格的锁定管理——在执行任何操作之前，请先测试文件访问权限：
  ```powershell
  try { [IO.File]::OpenWrite($path).Close(); $true } catch { $false }
  ```

- 定时任务如果写入相同的文件，可能会导致冲突——请使用临时文件并进行原子性的文件重命名操作。

## 临时文件管理

- `$env:TEMP` 变量会自动填充临时文件——脚本应使用 `try/finally` 语句来确保临时文件被正确清理：
  ```powershell
  $tmp = New-TemporaryFile
  try { ... } finally { Remove-Item $tmp -Force }
  ```

- 临时文件可能会在系统重启后仍然存在——这与 Linux 的 `/tmp` 目录不同。

## 服务账户的相关注意事项

- 服务是在不同的用户上下文中运行的——`$env:USERPROFILE` 指向的是系统配置文件，而不是用户的个人配置文件。
- 以 SYSTEM 账户进行网络访问时会使用系统的凭据——这可能会导致某些操作失败，而使用用户账户时却可以成功。
- 服务无法访问映射的驱动器——请使用 UNC 路径（如 `\\server\share`）来访问共享资源。