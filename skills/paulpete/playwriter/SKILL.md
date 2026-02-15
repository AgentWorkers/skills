---
name: playwriter
description: 通过 Playwright 和 Chrome 的持久化会话以及完整的 Playwright Page API 实现浏览器自动化操作。
hats: [developer, qa_tester]
---

# Playwright

## 概述

使用 Playwright 可以在本地 Chrome 会话中运行 Playwright Page 脚本。该工具会保留用户的登录信息、Cookie 以及浏览器扩展程序，非常适合用于 Web 仪表板测试和需要身份验证的流程。

## 使用场景

- 验证 Ralph Web 仪表板的用户界面
- 在不重新登录的情况下导航到已认证的页面
- 测试需要浏览器扩展程序或保存状态的流程
- 捕获可访问性快照以辅助元素定位

## 先决条件

- 安装 CLI：
  ```bash
  npm i -g playwriter
  ```
- 安装 Playwright Chrome 扩展程序（请参考 Playwright 仓库中的安装说明）
- 确保 Chrome 浏览器正在运行，并且已启用该扩展程序

## 核心工作流程

1. 创建一个会话：
   ```bash
   playwriter session new
   ```
2. 列出所有会话并复制会话 ID：
   ```bash
   playwriter session list
   ```
3. 在该会话中执行 Playwright 代码：
   ```bash
   playwriter -s <session_id> -e "await page.goto('https://example.com')"
   ```

## 执行环境

在 `-e` 命令的作用域内，可以使用以下变量：
- `page`（Playwright Page 对象）
- `context`（BrowserContext 对象）
- `state`（在同一会话中多次调用时保持不变的持久化对象）
- `require`（用于加载辅助模块）

示例：会话数据的持久化：
```bash
playwriter -s <session_id> -e "state.lastUrl = page.url()"
playwriter -s <session_id> -e "console.log(state.lastUrl)"
```

## 常见用法模式

### 导航 + 点击操作
```bash
playwriter -s <session_id> -e "await page.goto('http://localhost:3000'); await page.getByRole('button', { name: 'Run' }).click();"
```

### 填写表单
```bash
playwriter -s <session_id> -e "await page.getByLabel('Email').fill('qa@example.com'); await page.getByLabel('Password').fill('secret'); await page.getByRole('button', { name: 'Sign in' }).click();"
```

### 获取可访问性快照（带标签）
```bash
playwriter -s <session_id> -e "const { screenshotWithAccessibilityLabels } = require('playwriter'); await screenshotWithAccessibilityLabels(page, { path: '/tmp/a11y.png' });"
```

### 拦截网络请求
```bash
playwriter -s <session_id> -e "await page.route('**/api/**', async route => { const res = await route.fetch(); const body = await res.json(); await route.fulfill({ json: { ...body, injected: true } }); });"
```

### 读取页面内容
```bash
playwriter -s <session_id> -e "const text = await page.locator('main').innerText(); console.log(text);"
```

## 提示

- 建议使用 `getByRole` 和 `getByLabel` 来获取稳定的元素选择器。
- 利用可访问性快照来识别可靠的元素角色和标签。
- 保持会话的整洁性：如果会话状态变得混乱，请重置或关闭会话。
- 对于多步骤流程，可以将中间数据存储在 `state` 对象中。