---
name: browse
description: 使用 stagehand CLI 创建和部署浏览器自动化功能的完整指南
homepage: https://browserbase.com
metadata: {"moltbot":{"emoji":"🌐","requires":{"bins":["stagehand"],"env":["BROWSERBASE_API_KEY","BROWSERBASE_PROJECT_ID"]},"primaryEnv":"BROWSERBASE_API_KEY"}}
---

# 浏览器自动化与功能技能

本指南详细介绍了如何使用 `stagehand` CLI 创建和部署浏览器自动化功能。

## 使用场景

- 用户希望自动化网站操作  
- 用户需要从网站抓取数据  
- 用户希望创建一个 Browserbase 功能  
- 用户希望将自动化任务设置为定时执行或通过 Webhook 调用  

## 先决条件  

### 设置凭据  

```bash
stagehand fn auth status  # Check if configured
stagehand fn auth login   # If needed - get credentials from https://browserbase.com/settings
```  

## 完整工作流程  

### 第一步：交互式探索网站  

启动本地浏览器会话，了解网站结构：  
```bash
stagehand session create --local
stagehand goto https://example.com
stagehand snapshot                    # Get DOM structure with refs
stagehand screenshot -o page.png      # Visual inspection
```  

手动测试网站上的交互操作：  
```bash
stagehand click @0-5
stagehand fill @0-6 "value"
stagehand eval "document.querySelector('.price').textContent"
stagehand session end  # When done exploring
```  

### 第二步：初始化功能项目  

```bash
stagehand fn init my-automation
cd my-automation
```  

系统会生成以下文件：  
- `package.json`（依赖项）  
- `.env`（凭据，来自 `~/.stagehand/config.json`）  
- `index.ts`（功能模板）  
- `tsconfig.json`（TypeScript 配置文件）  

### 第三步：**立即修复 `package.json` 文件**  

**严重错误**：`stagehand fn init` 生成的 `package.json` 文件不完整，导致部署失败（提示 “No functions were built”）。  

**必须修复的内容**：在继续下一步之前，更新 `package.json` 文件：  
```json
{
  "name": "my-automation",
  "version": "1.0.0",
  "description": "My automation description",
  "main": "index.js",
  "type": "module",
  "packageManager": "pnpm@10.14.0",
  "scripts": {
    "dev": "pnpm bb dev index.ts",
    "publish": "pnpm bb publish index.ts"
  },
  "dependencies": {
    "@browserbasehq/sdk-functions": "^0.0.5",
    "playwright-core": "^1.58.0"
  },
  "devDependencies": {
    "@types/node": "^25.0.10",
    "typescript": "^5.9.3"
  }
}
```  

**主要修改内容：**  
- 添加 `description` 和 `main` 字段  
- 添加 `packageManager` 字段  
- 将依赖版本从 “latest” 更改为固定版本（例如 “^0.0.5”）  
- 添加包含 TypeScript 和类型声明的 `devDependencies` 部分  

之后执行以下操作：  
```bash
pnpm install
```  

### 第四步：编写自动化代码  

编辑 `index.ts` 文件：  
```typescript
import { defineFn } from "@browserbasehq/sdk-functions";
import { chromium } from "playwright-core";

defineFn("my-automation", async (context) => {
  const { session, params } = context;
  console.log("Connecting to browser session:", session.id);

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;

  // Your automation here
  await page.goto("https://example.com");
  await page.waitForLoadState("domcontentloaded");

  // Extract data
  const data = await page.evaluate(() => {
    // Complex extraction logic
    return Array.from(document.querySelectorAll('.item')).map(el => ({
      title: el.querySelector('.title')?.textContent,
      value: el.querySelector('.value')?.textContent,
    }));
  });

  // Return results (must be JSON-serializable)
  return {
    success: true,
    count: data.length,
    data,
    timestamp: new Date().toISOString(),
  };
});
```  

**关键概念：**  
- `context.session`：浏览器会话信息（ID、连接地址）  
- `context.params`：函数调用时传递的参数  
- 返回可序列化为 JSON 的数据  
- 最大执行时间为 15 分钟  

### 第五步：本地测试  

启动开发服务器：  
```bash
pnpm bb dev index.ts
```  

开发服务器的地址为 `http://127.0.0.1:14113`。  
使用 `curl` 命令调用该服务器：  
```bash
curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
  -H "Content-Type: application/json" \
  -d '{"params": {"url": "https://example.com"}}'
```  

开发服务器会在文件更改时自动重新加载。请查看终端输出以获取日志信息。  

### 第六步：部署到 Browserbase  

```bash
pnpm bb publish index.ts
# or: stagehand fn publish index.ts
```  

**预期输出：**  
```
✓ Build completed successfully
Build ID: xxx-xxx-xxx
Function ID: yyy-yyy-yyy  ← Save this!
```  

**如果出现 “No functions were built” 的错误**，说明 `package.json` 文件仍未修复（请参考第三步）。  

### 第七步：进行生产环境测试  

```bash
stagehand fn invoke <function-id> -p '{"param": "value"}'
```  

或者通过 API 调用自动化功能：  
```bash
curl -X POST https://api.browserbase.com/v1/functions/<function-id>/invoke \
  -H "Content-Type: application/json" \
  -H "x-bb-api-key: $BROWSERBASE_API_KEY" \
  -d '{"params": {}}'
```  

## 完整示例：Hacker News 数据抓取示例  

```typescript
import { defineFn } from "@browserbasehq/sdk-functions";
import { chromium } from "playwright-core";

defineFn("hn-scraper", async (context) => {
  const { session } = context;
  console.log("Connecting to browser session:", session.id);

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;

  await page.goto("https://news.ycombinator.com");
  await page.waitForLoadState("domcontentloaded");

  // Extract top 10 stories
  const stories = await page.evaluate(() => {
    const storyRows = Array.from(document.querySelectorAll('.athing')).slice(0, 10);

    return storyRows.map((row) => {
      const titleLine = row.querySelector('.titleline a');
      const subtext = row.nextElementSibling?.querySelector('.subtext');
      const commentsLink = Array.from(subtext?.querySelectorAll('a') || []).pop();

      return {
        rank: row.querySelector('.rank')?.textContent?.replace('.', '') || '',
        title: titleLine?.textContent || '',
        url: titleLine?.getAttribute('href') || '',
        points: subtext?.querySelector('.score')?.textContent?.replace(' points', '') || '0',
        author: subtext?.querySelector('.hnuser')?.textContent || '',
        time: subtext?.querySelector('.age')?.textContent || '',
        comments: commentsLink?.textContent?.replace(/\u00a0comments?/, '').trim() || '0',
        id: row.id,
      };
    });
  });

  return {
    success: true,
    count: stories.length,
    stories,
    timestamp: new Date().toISOString(),
  };
});
```  

## 常见模式  

### 参数化抓取  
```typescript
defineFn("scrape", async (context) => {
  const { session, params } = context;
  const { url, selector } = params;  // Accept params from invocation

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;

  await page.goto(url);
  const data = await page.$$eval(selector, els =>
    els.map(el => el.textContent)
  );

  return { url, data };
});
```  

### 认证  
```typescript
defineFn("auth-action", async (context) => {
  const { session, params } = context;
  const { username, password } = params;

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;

  await page.goto("https://example.com/login");
  await page.fill('input[name="email"]', username);
  await page.fill('input[name="password"]', password);
  await page.click('button[type="submit"]');
  await page.waitForURL("**/dashboard");

  const data = await page.textContent('.user-data');
  return { success: true, data };
});
```  

### 多页面处理  
```typescript
defineFn("multi-page", async (context) => {
  const { session, params } = context;
  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;

  const results = [];
  for (const url of params.urls) {
    await page.goto(url);
    await page.waitForLoadState("domcontentloaded");

    const title = await page.title();
    results.push({ url, title });
  }

  return { results };
});
```  

## 故障排除  

### 🔴 “No functions were built. 请检查您的入口文件和函数导出内容。”  

**这是最常见的错误！**  
**原因**：`stagehand fn init` 生成的 `package.json` 文件不完整。  

**解决方法：**  
1. 更新 `package.json` 文件（参见第三步）。  
2. 添加所有必需的字段：`description`、`main`、`packageManager`。  
3. 将依赖版本从 “latest” 更改为固定版本（例如 “^0.0.5”）。  
4. 添加包含 TypeScript 和类型声明的 `devDependencies` 部分。  
5. 执行 `pnpm install` 命令。  
6. 重新尝试部署。  

**快速检查方法**：将您的 `package.json` 文件与代码库中的 `bitcoin-functions/package.json` 文件进行比较。  

### 本地开发服务器无法启动  

```bash
# Check credentials
stagehand fn auth status

# Re-login if needed
stagehand fn auth login

# Install SDK globally
pnpm add -g @browserbasehq/sdk-functions
```  

### 功能在本地可以运行，但在部署时失败  

**常见原因：**  
1. 缺少 `devDependencies`（TypeScript 无法编译）。  
2. 使用了 “latest” 版本而非固定版本。  
3. `package.json` 中缺少必需字段。  

**解决方法**：按照第三步的说明修复 `package.json` 文件。  

### 无法从页面提取数据  

1. 截取页面截图：`stagehand screenshot -o debug.png`  
2. 获取页面快照：`stagehand snapshot`  
3. 使用 `page.evaluate()` 方法查看 DOM 中的内容。  
4. 确保选择器与实际 HTML 结构匹配。  

### “调用超时”  

- 功能的执行时间最长为 15 分钟。  
- 使用具体的等待时间（而非长时间休眠）。  
- 确认页面是否已成功加载。  

## 最佳实践  

1. **`stagehand fn init` 后立即修复 `package.json` 文件**。  
2. **先进行交互式探索**：使用本地浏览器会话了解网站结构。  
3. **手动测试**：在编写代码前验证每个步骤是否正常工作。  
4. **进行本地测试**：部署前先使用开发服务器。  
5. **返回有意义的数据**：包含时间戳、数据数量、URL 等信息。  
6. **优雅地处理错误**：对高风险操作进行异常处理。  
7. **使用具体的选择器**：优先选择数据属性而非 CSS 类名。  
8. **添加日志记录**：使用 `console.log()` 功能帮助调试部署后的功能。  
9. **验证参数**：在使用参数前进行检查。  
10. **设置合理的超时时间**：避免无限等待。  

## 快速检查清单：  
- [ ] 使用 `stagehand session create --local` 探索网站  
- [ ] 手动测试网站交互  
- [ ] 创建项目：`stagehand fn init <名称>`  
- [ ] **立即修复 `package.json` 文件**（第三步）  
- [ ] 执行 `pnpm install`  
- [ ] 在 `index.ts` 中编写自动化代码  
- [ ] 在本地进行测试：`pnpm bb dev index.ts`  
- [ ] 使用 `curl` 进行验证  
- [ ] 部署功能：`pnpm bb publish index.ts`  
- [ ] 在生产环境中测试功能：`stagehand fn invoke <函数ID>`  
- [ ] 保存函数 ID  

## 需要修改的代码（供维护人员使用）  

**文件：`/src/commands/functions.ts`  
**修改行号：146-158**  
**函数：`initFunction()`**  

将现有的 `packageJson` 对象替换为以下内容：  
```typescript
const packageJson = {
  name,
  version: '1.0.0',
  description: `${name} function`,
  main: 'index.js',
  type: 'module',
  packageManager: 'pnpm@10.14.0',
  scripts: {
    dev: 'pnpm bb dev index.ts',
    publish: 'pnpm bb publish index.ts',
  },
  dependencies: {
    '@browserbasehq/sdk-functions': '^0.0.5',
    'playwright-core': '^1.58.0',
  },
  devDependencies: {
    '@types/node': '^25.0.10',
    'typescript': '^5.9.3',
  },
};
```  

这样就可以解决所有新项目中出现的 “No functions were built” 错误。