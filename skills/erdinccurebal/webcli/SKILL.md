---
name: webcli
description: 使用 `webcli` 无头浏览器浏览网页、阅读页面内容、点击按钮、填写表单以及截取屏幕截图。当用户需要访问网站、从网页中收集信息或与 Web 应用程序交互时，可以使用该工具。
allowed-tools: Bash(webcli *)
---
# webcli — 无头浏览器命令行工具

您可以通过 `webcli` 命令来使用无头浏览器。该工具可用于浏览网页、读取内容、与页面元素交互以及截取屏幕截图。

## 先决条件

```bash
npm install -g @erdinccurebal/webcli
npx playwright install chromium
```

官网：https://erdinccurebal.github.io/webcli/
仓库地址：https://github.com/erdinccurebal/webcli

## 命令参考

### 导航
```bash
webcli go <url>                    # Navigate to URL (auto-starts daemon)
webcli go <url> -w networkidle     # Wait for network to settle
webcli go <url> -t mytab           # Open in named tab
webcli back                        # Go back in history
webcli forward                     # Go forward
webcli reload                      # Reload current page
```

### 读取页面内容
```bash
webcli source                      # Get full visible text of the page
webcli links                       # List all links (text + href)
webcli forms                       # List all forms with their inputs
webcli html <selector>             # Get innerHTML of element
webcli attr <selector> <attribute> # Get element attribute value
```

### 与页面元素交互
```bash
webcli click "<visible text>"      # Click element by visible text
webcli clicksel "<css selector>"   # Click element by CSS selector
webcli fill "<selector>" "<value>" # Fill an input field (preferred for forms)
webcli type "<text>"               # Type with keyboard (for focused element)
webcli select "<selector>" "<val>" # Select dropdown option
webcli press Enter                 # Press keyboard key (Enter, Tab, Escape...)
webcli focus "<selector>"          # Focus an element
```

### 等待
```bash
webcli wait "<selector>"           # Wait for CSS selector to be visible
webcli waitfor "<text>"            # Wait for text to appear on page
webcli sleep 2000                  # Sleep for N milliseconds
```

### 截取屏幕截图
```bash
webcli screenshot                  # Take screenshot (returns path)
webcli screenshot -o page.png      # Save to specific file
```

### 浏览器设置
```bash
webcli viewport 1920 1080          # Change viewport size
webcli useragent "<string>"        # Change user agent
```

### 标签页与后台进程管理
```bash
webcli tabs                        # List open tabs
webcli quit                        # Close current tab
webcli quit -t mytab               # Close specific tab
webcli status                      # Show daemon info (PID, uptime, tabs)
webcli stop                        # Stop daemon and close browser
```

### 全局选项
所有命令均支持以下选项：
- `-t, --tab <名称>` — 指定目标标签页（默认值："default"）
- `--json` — 以结构化 JSON 格式输出结果
- `--timeout <毫秒>` — 命令超时时间（默认值：30000 毫秒）

## 最佳实践

### 通用工作流程
1. 使用 `webcli go <网址>` 进行页面导航
2. 使用 `webcli source` 读取页面内容
3. 通过 `webcli click`、`webcli fill` 或 `webcli press` 与页面元素交互
4. 再次使用 `webcli source` 查看交互后的页面内容
5. 如需查看视觉结果，可以使用 `webcli screenshot`

### 表单填写
- 对于输入字段，始终使用 `webcli fill` — 该命令能正确处理 React/Vue 控制的输入元素
- 对于按钮，可以使用 `webcli click` 或 `webcli clicksel`
- 使用 `webcli press Enter` 提交表单
- 提交表单后，先执行 `webcli sleep 1000`，然后再使用 `webcli source` 检查结果

### 多标签页浏览
```bash
webcli go https://site-a.com -t research
webcli go https://site-b.com -t reference
webcli source -t research          # Read from specific tab
webcli source -t reference
```

### 错误处理
- 如果命令超时，尝试执行 `webcli sleep 2000` 后重新尝试
- 如果找不到某个元素，使用 `webcli source` 查看页面内容
- 如果后台进程出现卡顿，先使用 `webcli stop`，然后再尝试该命令
- 在与动态加载的内容交互之前，使用 `webcli wait "<选择器>"` 等待元素加载完成

## 重要提示
- 在尝试与页面交互之前，务必使用 `webcli source` 读取页面内容，以确保了解页面的具体结构
- 对于表单输入，建议使用 `webcli fill` 而不是 `webcli type`
- 在可能的情况下，优先使用 `webcli click`（通过文本选择）而非 `webcli clicksel`（通过元素选择器）——这样更加可靠
- 在快速连续操作之间使用 `webcli sleep`，以便页面有足够时间更新
- 后台进程会在命令执行之间保持运行状态——除非页面内容发生变化，否则无需重新导航