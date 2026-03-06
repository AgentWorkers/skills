---
name: browserstack
description: 在 BrowserStack 上运行测试。当用户提到“browserstack”、“跨浏览器测试”、“云测试”、“浏览器矩阵”、“在 Safari 上测试”、“在 Firefox 上测试”或“浏览器兼容性”时，请使用此方法。
  Run tests on BrowserStack. Use when user mentions "browserstack",
  "cross-browser", "cloud testing", "browser matrix", "test on safari",
  "test on firefox", or "browser compatibility".
---
# BrowserStack 集成

您可以在 BrowserStack 的云平台上运行 Playwright 测试，以实现跨浏览器和跨设备的测试。

## 先决条件

必须设置以下环境变量：
- `BROWSERSTACK_USERNAME` — 您的 BrowserStack 用户名
- `BROWSERSTACK_ACCESS_KEY` — 您的访问密钥

如果这些变量尚未设置，请告知用户如何从 [browserstack.com/accounts/settings](https://www.browserstack.com/accounts/settings) 获取它们，然后继续下一步。

## 功能

### 1. 配置 BrowserStack

```
/pw:browserstack setup
```

步骤：
1. 检查当前的 `playwright.config.ts` 文件。
2. 添加 BrowserStack 连接选项：

```typescript
// Add to playwright.config.ts
import { defineConfig } from '@playwright/test';

const isBS = !!process.env.BROWSERSTACK_USERNAME;

export default defineConfig({
  // ... existing config
  projects: isBS ? [
    {
      name: 'chrome@latest:Windows 11',
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(JSON.stringify({
            'browser': 'chrome',
            'browser_version': 'latest',
            'os': 'Windows',
            'os_version': '11',
            'browserstack.username': process.env.BROWSERSTACK_USERNAME,
            'browserstack.accessKey': process.env.BROWSERSTACK_ACCESS_KEY,
          }))}`,
        },
      },
    },
    {
      name: 'firefox@latest:Windows 11',
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(JSON.stringify({
            'browser': 'playwright-firefox',
            'browser_version': 'latest',
            'os': 'Windows',
            'os_version': '11',
            'browserstack.username': process.env.BROWSERSTACK_USERNAME,
            'browserstack.accessKey': process.env.BROWSERSTACK_ACCESS_KEY,
          }))}`,
        },
      },
    },
    {
      name: 'webkit@latest:OS X Ventura',
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(JSON.stringify({
            'browser': 'playwright-webkit',
            'browser_version': 'latest',
            'os': 'OS X',
            'os_version': 'Ventura',
            'browserstack.username': process.env.BROWSERSTACK_USERNAME,
            'browserstack.accessKey': process.env.BROWSERSTACK_ACCESS_KEY,
          }))}`,
        },
      },
    },
  ] : [
    // ... local projects fallback
  ],
});
```

3. 添加一个 npm 脚本：`"test:e2e:cloud": "npx playwright test --project='chrome@*' --project='firefox@*' --project='webkit@*'"`

### 2. 在 BrowserStack 上运行测试

```
/pw:browserstack run
```

步骤：
1. 确认凭据已设置。
2. 使用 BrowserStack 项目运行测试：
   ```bash
   BROWSERSTACK_USERNAME=$BROWSERSTACK_USERNAME \
   BROWSERSTACK_ACCESS_KEY=$BROWSERSTACK_ACCESS_KEY \
   npx playwright test --project='chrome@*' --project='firefox@*'
   ```
3. 监控测试执行过程。
4. 按浏览器显示测试结果。

### 3. 获取构建结果

```
/pw:browserstack results
```

步骤：
1. 调用 `browserstack_get_builds` 工具。
2. 获取最新的构建会话信息。
3. 对于每个会话：
   - 状态（通过/失败）
   - 浏览器和操作系统
   - 执行时间
   - 视频链接
   - 日志链接
4. 将结果格式化为摘要表格。

### 4. 查看可用浏览器

```
/pw:browserstack browsers
```

步骤：
1. 调用 `browserstack_get_browsers` 工具。
2. 过滤出与 Playwright 兼容的浏览器。
3. 显示可用的浏览器/操作系统组合。

### 5. 本地测试

```
/pw:browserstack local
```

对于在防火墙后进行本地或 staging 环境中的测试：
1. 安装 BrowserStack Local：`npm install -D browserstack-local`
2. 将本地隧道配置添加到测试配置中。
3. 提供相应的设置说明。

## 使用的 MCP 工具

| 工具 | 用途 |
|---|---|
| `browserstack_get_plan` | 检查账户限制 |
| `browserstack_get_browsers` | 列出可用浏览器 |
| `browserstack_get_builds` | 列出最近的构建记录 |
| `browserstack_get_sessions` | 获取构建中的会话信息 |
| `browserstack_get_session` | 获取会话详情（视频、日志） |
| `browserstack_update_session` | 标记测试结果（通过/失败） |
| `browserstack_get_logs` | 获取文本日志/网络日志 |

## 输出结果

- 跨浏览器测试结果表格
- 每个浏览器的测试结果（通过/失败）
- 链接到 BrowserStack 仪表板的视频/截图
- 任何特定浏览器的失败情况会被突出显示。