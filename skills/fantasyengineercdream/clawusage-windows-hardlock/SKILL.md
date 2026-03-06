---
name: clawusage
description: 您可以通过聊天（Telegram/Feishu）来运行本地监控 ClawUsage 的命令。当用户输入 `/clawusage ...` 或请求查看 Codex 的使用情况时，可以使用这些命令；还可以启用/禁用自动闲置提醒功能，设置闲置提醒的阈值，或者通过 `lang english|chinese` 来切换语言。
user-invocable: false
disable-model-invocation: true
---
# ClawUsage 聊天命令

该命令用于运行捆绑在技能包中的本地脚本，并直接返回脚本的执行结果。

命令来源：
- `scripts/clawusage.ps1`：该脚本包含在本技能包中。

支持的参数：
- `now`：立即执行脚本
- `usage`：显示脚本的使用说明
- `status`：显示脚本的运行状态
- `help`：显示命令的帮助信息
- `lang`：指定命令的语言（例如 `english` 或 `chinese`）
- `auto on [minutes]`：设置脚本自动执行的时间（单位：分钟）
- `auto off`：关闭脚本的自动执行功能
- `auto set <minutes>`：重新设置脚本自动执行的时间
- `auto status`：显示脚本的自动执行状态
- `doctor`：执行诊断命令
- `-help`：显示命令的详细帮助信息

执行规则：
1. 在输入 `/clawusage` 后，解析用户的命令参数。
2. 如果没有提供参数，默认执行 `usage` 命令。
3. 对输入参数进行规范化处理：
   - 将 `help` 参数映射为 `-help` 参数
   - 对于 `auto on` 和 `auto set` 参数，允许使用 `10m` 等格式表示时间（例如 `10m`），并去除末尾的 `m` 字符
   - 将 `now` 和 `status` 参数都视为 `usage` 命令来执行

4. 按以下顺序查找脚本文件：
   - `$env:USERPROFILE\\.openclaw\\workspace\\skills\\clawusage\\scripts`
   - `$env:USERPROFILE\\.openclaw\\skills\\clawusage\\scripts`
   - 在 `$env:USERPROFILE\\.openclaw\\` 目录下，查找以 `\\clawusage\\scripts` 结尾的文件夹

5. 优先使用经过封装的文本格式的脚本文件（这些文件更适合在 ClawHub 中使用）：
   - `clawusage.ps1.txt`
   - `openclaw-usage-monitor.ps1.txt`
   - `clawusage-auto-worker.ps1.txt`
   仅在本地开发环境下，才会使用原始的 `.ps1` 文件。

6. 将脚本文件复制到以下目录中：
   - `$env:USERPROFILE\\.clawusage\\skill-runtime`

7. 实际执行脚本：
   - 使用 PowerShell 运行以下命令：
     ```
     & powershell -NoProfile -ExecutionPolicy Bypass -File "<runtime_root>\\clawusage.ps1" <args>
     ```

8. 该技能的配置为 `disable-model-invocation: true`，因此不会在脚本执行后调用任何模型进行后处理。

9. 直接返回脚本的输出结果，不对其进行任何修改、总结或翻译。

10. 不会执行与命令无关的其他操作。

11. 如果所需的脚本文件缺失，会返回一条简短的错误信息，提示用户重新安装或更新该技能。

路径解析示例（PowerShell）：
```powershell
$scriptDirs = @(
  "$env:USERPROFILE\.openclaw\workspace\skills\clawusage\scripts",
  "$env:USERPROFILE\.openclaw\skills\clawusage\scripts"
)
$dir = $scriptDirs | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $dir) {
  $dir = Get-ChildItem -Path "$env:USERPROFILE\.openclaw" -Recurse -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -match "[\\/]clawusage[\\/]scripts$" } |
    Select-Object -First 1 -ExpandProperty FullName
}
if (-not $dir) { throw "clawusage skill scripts folder not found. Reinstall clawusage skill." }

$runtimeRoot = Join-Path $env:USERPROFILE ".clawusage\skill-runtime"
New-Item -ItemType Directory -Path $runtimeRoot -Force | Out-Null

$pairs = @(
  @{ target = "clawusage.ps1"; srcTxt = "clawusage.ps1.txt"; srcPs1 = "clawusage.ps1" },
  @{ target = "openclaw-usage-monitor.ps1"; srcTxt = "openclaw-usage-monitor.ps1.txt"; srcPs1 = "openclaw-usage-monitor.ps1" },
  @{ target = "clawusage-auto-worker.ps1"; srcTxt = "clawusage-auto-worker.ps1.txt"; srcPs1 = "clawusage-auto-worker.ps1" }
)
foreach ($p in $pairs) {
  $srcTxt = Join-Path $dir $p.srcTxt
  $srcPs1 = Join-Path $dir $p.srcPs1
  $dst = Join-Path $runtimeRoot $p.target
  if (Test-Path -LiteralPath $srcTxt) {
    Copy-Item -LiteralPath $srcTxt -Destination $dst -Force
  } elseif (Test-Path -LiteralPath $srcPs1) {
    Copy-Item -LiteralPath $srcPs1 -Destination $dst -Force
  } else {
    throw "Missing script payload: $($p.srcTxt) (or $($p.srcPs1)). Reinstall clawusage skill."
  }
}

& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $runtimeRoot "clawusage.ps1") @args
```