---
name: playwright-cli
description: 该工具可自动化浏览器操作，用于网页测试、表单填写、截图以及数据提取。适用于用户需要浏览网站、与网页交互、填写表单、截取屏幕截图、测试Web应用程序或从网页中提取信息的情况。
allowed-tools: Bash(playwright-cli:*)
---

# 使用playwright-cli进行浏览器自动化

## 快速入门

```bash
playwright-cli open https://playwright.dev
playwright-cli click e15
playwright-cli type "page.click"
playwright-cli press Enter
```

## 核心工作流程

1. 导航：`playwright-cli open https://example.com`
2. 根据快照中的引用与页面元素进行交互
3. 在发生重大更改后重新生成快照

## 命令

### 核心命令

```bash
playwright-cli open https://example.com/
playwright-cli close
playwright-cli type "search query"
playwright-cli click e3
playwright-cli dblclick e7
playwright-cli fill e5 "user@example.com"
playwright-cli drag e2 e8
playwright-cli hover e4
playwright-cli select e9 "option-value"
playwright-cli upload ./document.pdf
playwright-cli check e12
playwright-cli uncheck e12
playwright-cli snapshot
playwright-cli snapshot --filename=after-click.yaml
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5
playwright-cli dialog-accept
playwright-cli dialog-accept "confirmation text"
playwright-cli dialog-dismiss
playwright-cli resize 1920 1080
```

### 导航命令

```bash
playwright-cli go-back
playwright-cli go-forward
playwright-cli reload
```

### 键盘操作

```bash
playwright-cli press Enter
playwright-cli press ArrowDown
playwright-cli keydown Shift
playwright-cli keyup Shift
```

### 鼠标操作

```bash
playwright-cli mousemove 150 300
playwright-cli mousedown
playwright-cli mousedown right
playwright-cli mouseup
playwright-cli mouseup right
playwright-cli mousewheel 0 100
```

### 保存当前操作

```bash
playwright-cli screenshot
playwright-cli screenshot e5
playwright-cli screenshot --filename=page.png
playwright-cli pdf --filename=page.pdf
```

### 切换标签页

```bash
playwright-cli tab-list
playwright-cli tab-new
playwright-cli tab-new https://example.com/page
playwright-cli tab-close
playwright-cli tab-close 2
playwright-cli tab-select 0
```

### 数据存储

```bash
playwright-cli state-save
playwright-cli state-save auth.json
playwright-cli state-load auth.json

# Cookies
playwright-cli cookie-list
playwright-cli cookie-list --domain=example.com
playwright-cli cookie-get session_id
playwright-cli cookie-set session_id abc123
playwright-cli cookie-set session_id abc123 --domain=example.com --httpOnly --secure
playwright-cli cookie-delete session_id
playwright-cli cookie-clear

# LocalStorage
playwright-cli localstorage-list
playwright-cli localstorage-get theme
playwright-cli localstorage-set theme dark
playwright-cli localstorage-delete theme
playwright-cli localstorage-clear

# SessionStorage
playwright-cli sessionstorage-list
playwright-cli sessionstorage-get step
playwright-cli sessionstorage-set step 3
playwright-cli sessionstorage-delete step
playwright-cli sessionstorage-clear
```

### 网络操作

```bash
playwright-cli route "**/*.jpg" --status=404
playwright-cli route "https://api.example.com/**" --body='{"mock": true}'
playwright-cli route-list
playwright-cli unroute "**/*.jpg"
playwright-cli unroute
```

### 开发工具

```bash
playwright-cli console
playwright-cli console warning
playwright-cli network
playwright-cli run-code "async page => await page.context().grantPermissions(['geolocation'])"
playwright-cli tracing-start
playwright-cli tracing-stop
playwright-cli video-start
playwright-cli video-stop video.webm
```

### 安装playwright-cli

```bash
playwright-cli install-browser
playwright-cli install-skills
```

### 配置playwright-cli

```bash
# Use specific browser when creating session
playwright-cli open --browser=chrome
playwright-cli open --browser=firefox
playwright-cli open --browser=webkit
playwright-cli open --browser=msedge
# Connect to browser via extension
playwright-cli open --extension

# Configure the session
playwright-cli config --config my-config.json
playwright-cli config --headed --in-memory --browser=firefox
# Configure named session
playwright-cli --session=mysession config my-config.json
# Start with configured session
playwright-cli open --config=my-config.json
```

### 会话管理

```bash
playwright-cli --session=mysession open example.com
playwright-cli --session=mysession click e6
playwright-cli session-list
playwright-cli session-stop mysession
playwright-cli session-restart mysession
playwright-cli session-stop-all
playwright-cli session-delete
playwright-cli session-delete mysession
```

## 示例：表单提交

```bash
playwright-cli open https://example.com/form
playwright-cli snapshot

playwright-cli fill e1 "user@example.com"
playwright-cli fill e2 "password123"
playwright-cli click e3
playwright-cli snapshot
```

## 示例：多标签页操作流程

```bash
playwright-cli open https://example.com
playwright-cli tab-new https://example.com/other
playwright-cli tab-list
playwright-cli tab-select 0
playwright-cli snapshot
```

## 示例：使用开发工具进行调试

```bash
playwright-cli open https://example.com
playwright-cli click e4
playwright-cli fill e7 "test"
playwright-cli console
playwright-cli network
```

## 具体任务

* **请求模拟** [references/request-mocking.md](references/request-mocking.md)
* **运行Playwright脚本** [references/running-code.md]
* **会话管理** [references/session-management.md]
* **数据存储（cookies、localStorage）** [references/storage-state.md]
* **测试生成** [references/test-generation.md]
* **跟踪代码执行过程** [references/tracing.md]
* **视频录制** [references/video-recording.md]