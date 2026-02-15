---
name: web-qa-bot
description: 基于人工智能的自动化质量保证（QA）工具，适用于Web应用程序。支持烟雾测试（Smoke Tests）、可访问性测试（Accessibility Tests）以及视觉回归测试（Visual Regression Tests）。可与Cursor、Claude、ChatGPT、Copilot等工具集成使用，并已准备好支持Vibe-coding功能。
version: 0.1.3
author: NextFrontierBuilds
keywords: [automated-qa, ai-testing, smoke-test, accessibility-testing, visual-regression, ci-testing, playwright-alternative, e2e-testing, qa, testing, automation, ai, ai-agent, vibe-coding, cursor, claude, chatgpt, copilot, github-copilot, mcp, llm, devtools, ai-tools, developer-tools, typescript, moltbot, openclaw]
---

# web-qa-bot

这是一个基于AI技术的Web应用程序自动化测试工具，采用基于可访问性树的测试方法（accessibility-tree-based testing）来进行质量保证（QA）。

## 概述

该工具提供了用于Web应用程序自动化测试的工具。它利用浏览器的可访问性树（accessibility trees）来可靠地检测页面元素，而非依赖不稳定的CSS选择器。

## 安装

```bash
npm install -g web-qa-bot agent-browser
agent-browser install
```

## 命令

### 快速健康检查（Quick Smoke Test）

```bash
web-qa-bot smoke https://example.com
```

执行基本的功能检查：
- 页面是否成功加载
- 控制台是否有错误信息
- 导航元素是否存在
- 图片是否具有替代文本（alt text）

### 运行测试套件（Run Test Suite）

```bash
web-qa-bot run ./tests/suite.yaml --output report.md
```

### 生成PDF报告（Generate PDF Report）

```bash
web-qa-bot report ./results.json -o report.pdf -f pdf
```

## 使用场景

### 1. 快速站点健康检查（Quick Site Health Check）

```bash
# Smoke test a production URL
web-qa-bot smoke https://app.example.com --checks pageLoad,consoleErrors,navigation
```

### 2. 部署前的质量保证（Pre-deployment QA）

在每次部署前创建并运行测试套件：

```yaml
# tests/critical-paths.yaml
name: Critical Paths
baseUrl: https://staging.example.com

tests:
  - name: Login flow
    steps:
      - goto: /login
      - type: { ref: Email, text: test@example.com }
      - type: { ref: Password, text: testpass }
      - click: Sign In
      - expectVisible: Dashboard
      - expectNoErrors: true
```

```bash
web-qa-bot run ./tests/critical-paths.yaml --output qa-report.pdf -f pdf
```

### 3. 监控代码回归（Monitor for Regressions）

```bash
# Run tests and fail CI if issues found
web-qa-bot run ./tests/smoke.yaml || exit 1
```

### 4. 程序化测试（Programmatic Testing）

```typescript
import { QABot } from 'web-qa-bot'

const qa = new QABot({
  baseUrl: 'https://example.com',
  headless: true
})

await qa.goto('/')
await qa.click('Get Started')
await qa.snapshot()
qa.expectVisible('Sign Up')
await qa.close()
```

## 与代理浏览器（agent-browser）的集成

该工具封装了代理浏览器（agent-browser）的命令行接口（CLI），以实现浏览器自动化操作：

```bash
# Connect to existing browser session
web-qa-bot smoke https://example.com --cdp 18800

# Run headed for debugging
web-qa-bot run ./tests/suite.yaml --no-headless
```

## 测试结果格式

测试结果以结构化的JSON格式返回：

```json
{
  "name": "Smoke Test",
  "url": "https://example.com",
  "summary": {
    "total": 4,
    "passed": 3,
    "failed": 0,
    "warnings": 1
  },
  "tests": [
    {
      "name": "Page Load",
      "status": "pass",
      "duration": 1234
    }
  ]
}
```

## 提示

1. **使用基于角色的选择器（role-based selectors）**：比CSS类更可靠。
2. **检查控制台错误（Check console errors）**：通常能发现隐藏的问题。
3. **测试两种导航方式**：直接访问URL和应用程序内部的路由机制。
4. **失败时生成截图（Screenshot on failure）**：测试套件会自动执行此操作。
5. **监控弹出窗口（Monitor for modals）**：某些弹出窗口可能会阻止用户与页面的交互。

## 报告格式

- **Markdown**：默认格式，便于人类阅读。
- **PDF**：通过ai-pdf-builder生成的专业报告格式。
- **JSON**：适用于持续集成/持续部署（CI/CD）的机器可读格式。

## 故障排除

### “agent-browser未找到”（"agent-browser not found”）

```bash
npm install -g agent-browser
agent-browser install
```

### “元素未找到”（"Element not found”）

首先生成页面的快照以查看可用的元素引用：

```bash
agent-browser snapshot
```

### “等待元素超时”（"Timeout waiting for element”）

增加超时时间，或检查该元素是否处于加载状态：

```yaml
steps:
  - waitMs: 2000
  - waitFor: "Loading" # Wait for loading to appear
  - waitFor: "Content" # Then wait for content
```

## 链接

- [GitHub](https://github.com/NextFrontierBuilds/web-qa-bot)
- [npm](https://www.npmjs.com/package/web-qa-bot)