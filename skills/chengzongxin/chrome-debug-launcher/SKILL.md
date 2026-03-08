---
name: chrome-debug-launcher
description: 启动两个独立的 Chrome 浏览器实例：一个为普通模式，另一个开启远程调试功能（监听端口 9222）。当用户输入“打开两个浏览器”、“开启调试浏览器”或任何类似的指令时，系统应自动启动一个用于调试的 Chrome 浏览器，同时保持另一个浏览器处于普通模式。
---
# Chrome 调试启动器

该工具用于启动两个独立的 Chrome 实例：一个用于普通使用，另一个则开启远程调试功能（监听 9222 端口）。

## 操作步骤

1. **终止所有正在运行的 Chrome 进程**。
2. **启动普通的 Chrome 实例**（无需添加任何参数）。
3. **等待 2 秒**，然后启动用于调试的 Chrome 实例。

## 平台对应的命令

### Windows（PowerShell）

```powershell
# Step 1: Kill Chrome
taskkill /F /IM chrome.exe /T 2>$null
Start-Sleep -Seconds 2

# Step 2: Normal Chrome
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe"

# Step 3: Debug Chrome (after 2s)
Start-Sleep -Seconds 2
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList '--remote-debugging-port=9222', '--user-data-dir=C:\selenum\ChromeProfile'
```

### macOS（bash）

```bash
# Step 1: Kill Chrome
pkill -f "Google Chrome" 2>/dev/null; sleep 2

# Step 2: Normal Chrome
open -a "Google Chrome"

# Step 3: Debug Chrome (after 2s)
sleep 2
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/selenium/ChromeProfile" &
```

## 运行结果

- **实例 1**：普通的 Chrome 实例，使用默认配置，用于日常使用。
- **实例 2**：开启远程调试功能的 Chrome 实例，监听 9222 端口，用户数据目录为隔离状态。
  - 可通过 Selenium/Playwright 连接到该实例：`http://localhost:9222`