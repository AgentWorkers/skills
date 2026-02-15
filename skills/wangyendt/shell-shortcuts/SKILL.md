---
name: shell-shortcuts
description: 在新机器上配置跨平台的终端快捷命令，包括 `proxy_on`/`proxy_off`（环境变量 + Git 全局代理设置）、`goto`（用于跳转到指定路径的快捷方式）、`gpu`（用于查看 NVIDIA SMI 状态的命令），以及可选的 Conda 自动激活功能。这些命令适用于设置 Windows PowerShell 的自动运行脚本（AutoRun），或添加到 macOS/Linux 系统的 shell 配置文件（rc 文件）中。
---
# Shell 快捷键（proxy_on、proxy_off、goto、gpu、conda 自动启动）

目标：通过一组简单的命令，使新安装的机器在 Windows、macOS 和 Ubuntu 上表现出一致的行为：

- `proxy_on` / `proxy_off`：切换终端代理（环境变量 + Git 全局代理）
- `goto`：创建持久性的路径快捷键（例如 `goto work`）
- `gpu`：显示 NVIDIA GPU 的状态（使用 `nvidia-smi` 工具；仅适用于 Windows 和 Ubuntu）
- 可选：在新打开的 Shell 窗口中自动激活 Conda 环境

需要注意的是，这些设置具有一定的主观性：

- 在 Windows 上，建议使用 PowerShell 来实现完整的 `goto` 功能。
- 为了确保命令的可重复执行性（idempotence），请将所有相关函数/脚本放在有明确标记的代码块中。

## 默认设置（根据需要修改）

- HTTP/HTTPS 代理：`http://127.0.0.1:7890`
- SOCKS5 代理：`socks5://127.0.0.1:7890`
- NO_PROXY：`localhost,127.0.0.1,.qualcomm.com,*.amazonaws.com`

## Windows：PowerShell（推荐）

编辑您的 PowerShell 配置文件（`$PROFILE`）：

添加（或替换）以下代码块。`goto` 的路径信息存储在文件 `$HOME\.goto_paths.json` 中。

```powershell
# >>> shell-shortcuts >>>

function proxy_off {
  param([switch]$Quiet)
  Remove-Item Env:http_proxy,Env:https_proxy,Env:all_proxy,Env:no_proxy -ErrorAction SilentlyContinue
  Remove-Item Env:HTTP_PROXY,Env:HTTPS_PROXY,Env:ALL_PROXY,Env:NO_PROXY -ErrorAction SilentlyContinue

  if (Get-Command git -ErrorAction SilentlyContinue) {
    git config --global --unset http.proxy 2>$null | Out-Null
    git config --global --unset https.proxy 2>$null | Out-Null
  }

  if (-not $Quiet) { Write-Host "Proxy is OFF" }
}

function proxy_on {
  param(
    [string]$HttpProxyUrl = "http://127.0.0.1:7890",
    [string]$SocksProxyUrl = "socks5://127.0.0.1:7890",
    [string]$NoProxyList = "localhost,127.0.0.1,.qualcomm.com,*.amazonaws.com"
  )

  proxy_off -Quiet

  $env:http_proxy  = $HttpProxyUrl
  $env:https_proxy = $HttpProxyUrl
  $env:HTTP_PROXY  = $HttpProxyUrl
  $env:HTTPS_PROXY = $HttpProxyUrl

  $env:all_proxy = $SocksProxyUrl
  $env:ALL_PROXY = $SocksProxyUrl

  $env:no_proxy = $NoProxyList
  $env:NO_PROXY = $NoProxyList

  if (Get-Command git -ErrorAction SilentlyContinue) {
    git config --global http.proxy  $HttpProxyUrl  | Out-Null
    git config --global https.proxy $HttpProxyUrl  | Out-Null
  }

  Write-Host "Proxy is ON"
  Write-Host "  HTTP/HTTPS: $HttpProxyUrl"
  Write-Host "  SOCKS5:     $SocksProxyUrl"
  Write-Host "  NO_PROXY:   $NoProxyList"
}

function _goto_db_path {
  Join-Path $HOME ".goto_paths.json"
}

function _goto_load {
  $db = _goto_db_path
  if (-not (Test-Path -LiteralPath $db)) { return @{} }
  try {
    $raw = Get-Content -Raw -Encoding UTF8 -LiteralPath $db
    if (-not $raw.Trim()) { return @{} }
    $obj = $raw | ConvertFrom-Json
    $ht = @{}
    foreach ($p in $obj.PSObject.Properties) { $ht[$p.Name] = [string]$p.Value }
    return $ht
  } catch {
    throw "Failed to parse goto DB: $db. Fix JSON or delete it."
  }
}

function _goto_save([hashtable]$ht) {
  $db = _goto_db_path
  $dir = Split-Path -Parent $db
  if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
  ($ht | ConvertTo-Json -Depth 5) | Set-Content -Encoding UTF8 -LiteralPath $db
}

function goto {
  param(
    [Parameter(Position = 0)][string]$Cmd,
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$Rest
  )

  $ht = _goto_load

  switch ($Cmd) {
    { $_ -in @($null, "", "ls", "list") } {
      if ($ht.Count -eq 0) { Write-Host "No shortcuts. Use: goto add <key> <path>"; return }
      Write-Host "Available shortcuts:"
      foreach ($k in ($ht.Keys | Sort-Object)) {
        "{0,-12} -> {1}" -f $k, $ht[$k] | Write-Host
      }
      return
    }
    "add" {
      if ($Rest.Count -lt 2) { throw "Usage: goto add <shortcut> <path>" }
      $key = $Rest[0]
      $path = ($Rest | Select-Object -Skip 1) -join " "
      if ($path -like "~*") { $path = $path -replace "^~", $HOME }
      $resolved = Resolve-Path -LiteralPath $path -ErrorAction Stop
      $ht[$key] = $resolved.Path
      _goto_save $ht
      Write-Host "Added: $key -> $($ht[$key])"
      return
    }
    { $_ -in @("rm","remove","del") } {
      if ($Rest.Count -ne 1) { throw "Usage: goto remove <shortcut>" }
      $key = $Rest[0]
      $ht.Remove($key) | Out-Null
      _goto_save $ht
      Write-Host "Removed: $key"
      return
    }
    "clear" {
      _goto_save @{}
      Write-Host "All shortcuts cleared."
      return
    }
    default {
      if (-not $Cmd) { return }
      if (-not $ht.ContainsKey($Cmd)) {
        Write-Host "Unknown shortcut: $Cmd"
        Write-Host "Tip: goto list"
        return 1
      }
      Set-Location -LiteralPath $ht[$Cmd]
      return
    }
  }
}

function gpu {
  $cmd = Get-Command nvidia-smi -ErrorAction SilentlyContinue
  if (-not $cmd) {
    Write-Host "nvidia-smi not found (need NVIDIA driver/tools)."
    return 1
  }
  & $cmd.Path
}

# Optional: Conda auto-activate (edit these)
# $CondaRoot = "D:\\ProgramData\\miniconda3"
# $CondaEnv  = "wayne3.10"
# if (Test-Path -LiteralPath (Join-Path $CondaRoot "Scripts\\conda.exe")) {
#   $hook = (& (Join-Path $CondaRoot "Scripts\\conda.exe") "shell.powershell" "hook") 2>$null | Out-String
#   if ($hook) { Invoke-Expression $hook }
#   conda activate $CondaEnv
# }

# <<< shell-shortcuts <<<
```

**使用方法：**

```powershell
proxy_on
proxy_off
goto list
goto add work D:\work
goto work
gpu
```

## Windows：CMD（可选）

CMD 中预定义了 `goto` 关键字。实际使用的命令是 `jump`，您可以通过 `doskey` 将 `goto` 别名为 `jump` 以在交互式会话中使用。

**推荐布局：**

- 将脚本放在 `C:\Users\<YourUsername>\bin\` 目录下。
- 将该目录添加到系统的 PATH 环境变量中（或在 CMD 的启动脚本中完成此操作）。

创建 `C:\Users\<YourUsername>\cmd_startup.cmd` 文件：

```bat
@echo off
set "PATH=%USERPROFILE%\bin;%PATH%"

REM Optional: conda auto-activate (edit these)
REM call "D:\ProgramData\miniconda3\condabin\conda.bat" activate wayne3.10

REM Interactive alias only (scripts/cmd /c should call jump directly)
doskey goto=jump $*
```

**启用自动运行（当前用户）：**

```bat
reg add "HKCU\Software\Microsoft\Command Processor" /v AutoRun /t REG_SZ /d "%USERPROFILE%\cmd_startup.cmd" /f
```

将这些 `.cmd` 文件放在 `%USERPROFILE%\bin` 目录下：

- `proxy_on.cmd` / `proxy_off.cmd`：设置/取消设置代理环境变量以及 Git 全局代理。
- `gpu.cmd`：运行 `nvidia-smi` 命令以显示 GPU 状态。
- `jump.cmd`：从 `%USERPROFILE%\.goto_paths` 文件中读取路径信息并创建持久性的快捷键（格式：`key|C:\abs\path`）。

如需详细的模板，请参阅 `shell-shortcuts/references/windows-cmd.md`。

## macOS / Ubuntu（bash/zsh）

将以下函数添加到 `~/.zshrc` 或 `~/.bashrc` 文件中：

- `proxy_on` / `proxy_off`
- `goto`（路径信息存储在 `~/.goto_paths` 文件中）
- Ubuntu：`gpu`（需要安装 `nvidia-smi` 工具）

相关模板位于 `shell-shortcuts/references/unix.md` 文件中（请复制并调整代理设置）。