---
name: caffeine
description: 防止 macOS 或 Windows 系统的屏幕和电脑进入睡眠状态。适用于用户希望保持屏幕显示、禁用睡眠功能，或需要长时间不间断地运行任务的情况。
---

# Caffeine

该工具通过阻止显示器和系统进入睡眠状态来让你的电脑保持唤醒。

## 快速入门

### macOS

```bash
caffeinate -d
```

### Windows (PowerShell)

```powershell
# Keep display awake until Ctrl+C
while ($true) {
  $wsh = New-Object -ComObject WScript.Shell
  $wsh.SendKeys('{SCROLLLOCK}{SCROLLLOCK}')
  Start-Sleep -Seconds 60
}
```

---

## macOS

使用内置的 `caffeinate` 命令（无需安装）。

### 常用选项

| 命令 | 功能 |
|---------|--------|
| `caffeinate` | 阻止系统进入睡眠状态，直到命令终止 |
| `caffeinate -d` | 阻止显示器进入睡眠状态 |
| `caffeinate -i` | 阻止系统进入空闲状态（非活动状态）的睡眠 |
| `caffeinate -s` | 阻止系统进入睡眠状态（仅适用于使用交流电源的情况） |
| `caffeinate -t 3600` | 阻止系统进入睡眠状态 3600 秒（1 小时） |
| `caffeinate -d -t 1800` | 保持显示器处于唤醒状态 1800 秒（30 分钟） |

### 示例

- 保持显示器处于唤醒状态 2 小时：  
  ```bash
caffeinate -d -t 7200
```

- 在命令运行期间保持电脑唤醒：  
  ```bash
caffeinate -i -- long-running-command
```

- 在后台运行 Caffeine：  
  ```bash
caffeinate -d &
# To stop later:
pkill caffeinate
```

- 检查 Caffeine 是否正在运行：  
  ```bash
pgrep -l caffeinate
```

---

## Windows

### 方法 1：PowerShell（无需安装）

通过模拟活动来阻止系统进入睡眠状态（按 Ctrl+C 可停止 Caffeine 的运行）：  
```powershell
while ($true) {
  $wsh = New-Object -ComObject WScript.Shell
  $wsh.SendKeys('{SCROLLLOCK}{SCROLLLOCK}')
  Start-Sleep -Seconds 60
}
```

### 方法 2：使用 `powercfg` 修改电源设置

- 暂时禁用系统的睡眠功能：  
  ```powershell
# Disable sleep on AC power
powercfg /change standby-timeout-ac 0
powercfg /change monitor-timeout-ac 0

# Re-enable later (e.g., 30 minutes)
powercfg /change standby-timeout-ac 30
powercfg /change monitor-timeout-ac 15
```

### 方法 3：使用“演示模式”（Presentation Mode）  

- 在某些情况下，启用“演示模式”也可以防止系统进入睡眠状态。  
  ```powershell
# Enable presentation mode (disables sleep + notifications)
presentationsettings /start

# Disable when done
presentationsettings /stop
```

### 方法 4：使用 .NET 编写简单脚本  

- 你可以使用 .NET 编写简单脚本来实现相同的功能。  
  ```powershell
# Prevent sleep for duration of script
Add-Type -AssemblyName System.Windows.Forms
while ($true) {
  [System.Windows.Forms.Cursor]::Position = [System.Windows.Forms.Cursor]::Position
  Start-Sleep -Seconds 60
}
```

---

## 注意事项

- **macOS**：`caffeinate` 是内置命令，需要确保相关进程持续运行。  
- **Windows**：使用 PowerShell 方法时，需要模拟用户活动；`powercfg` 命令用于修改系统的电源设置。  
- 按下 **Ctrl+C** 可以立即停止正在运行的 Caffeine 脚本。