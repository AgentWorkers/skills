---
name: playwright-browser
description: 在Clawdbot中使用Playwright Chromium设置无头浏览器自动化。适用于配置WSL/Linux环境中的浏览器工具、安装浏览器依赖项或启用无头Web自动化。该过程包括Chromium的安装、系统库依赖项的配置以及Clawdbot浏览器的设置。
---
# Playwright 浏览器设置

配置 Clawdbot 的浏览器工具，使其在 WSL/Linux 环境中使用由 Playwright 管理的 Chromium 进行无头自动化测试。

## 快速设置

运行设置脚本以安装所有所需组件：

```bash
./scripts/setup.sh
```

这将完成以下操作：
1. 安装 Playwright 和 Chromium
2. 安装系统所需的库（需要使用 `sudo` 权限）
3. 修改 Clawdbot 的配置文件，使其使用 Playwright 浏览器

## 手动设置

### 1. 安装 Playwright Chromium

```bash
npx playwright install chromium
```

### 2. 安装系统依赖项

Chromium 需要 NSS 和 ALSA 库：

```bash
# Ubuntu/Debian
sudo apt-get install -y libnss3 libasound2t64

# If libasound2t64 doesn't exist (older Ubuntu):
sudo apt-get install -y libnss3 libasound2
```

### 3. 查找 Chromium 的路径

```bash
find ~/.cache/ms-playwright -name "chrome" -path "*/chrome-linux64/*" 2>/dev/null | head -1
```

### 4. 配置 Clawdbot

修改 Clawdbot 的配置文件：

```bash
clawdbot config patch '{"browser": {"executablePath": "<path-from-step-3>", "headless": true, "noSandbox": true}}'
```

或者使用提供的脚本进行配置：

```bash
./scripts/configure-clawdbot.sh
```

## 验证

测试浏览器是否正常工作：

```bash
~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome --headless --no-sandbox --disable-gpu --dump-dom https://example.com
```

## 注意事项

- 在 WSL/容器环境中，必须设置 `noSandbox: true`
- 设置 `headless: true` 可以实现无窗口运行（更快，无需显示界面）
- 如果需要显示浏览器界面，请将 `headless: false` 设置为 `true`，并确保 WSLg 或 X11 已正确配置