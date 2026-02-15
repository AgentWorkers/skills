---
name: browserbase-functions
description: **使用官方的bb CLI指导Claude部署无服务器浏览器自动化**
---

# Browserbase函数技能

本技能将指导您使用官方的`bb` CLI来部署无服务器的浏览器自动化脚本。

## 使用场景

- 当用户希望按计划自动执行某些操作时
- 当用户需要为浏览器自动化脚本设置Webhook接口时
- 当用户希望在云端（而非本地）运行自动化脚本时
- 当用户咨询有关Browserbase函数的相关信息时

## 先决条件

### 1. 获取凭证

从以下链接获取API密钥和项目ID：https://browserbase.com/settings

### 2. 设置环境变量

- 可以将这些变量保存以供后续使用：
```bash
stagehand fn auth login
# Enter API key and Project ID when prompted
```

- 或者为当前会话导出这些变量：
```bash
eval "$(stagehand fn auth export)"
```

- 或者直接在代码中设置这些变量：
```bash
export BROWSERBASE_API_KEY="your_api_key"
export BROWSERBASE_PROJECT_ID="your_project_id"
```

## 创建函数项目

### 1. 使用官方CLI进行初始化

```bash
pnpm dlx @browserbasehq/sdk-functions init my-function
cd my-function
```

初始化后，将会创建以下内容：
```
my-function/
├── package.json
├── index.ts        # Your function code
└── .env            # Add credentials here
```

### 2. 将凭证添加到`.env`文件中

```bash
# Copy from stored credentials
echo "BROWSERBASE_API_KEY=$BROWSERBASE_API_KEY" >> .env
echo "BROWSERBASE_PROJECT_ID=$BROWSERBASE_PROJECT_ID" >> .env
```

- 或者手动编辑`.env`文件：
```
BROWSERBASE_API_KEY=your_api_key
BROWSERBASE_PROJECT_ID=your_project_id
```

### 3. 安装依赖项

```bash
pnpm install
```

## 函数结构

```typescript
import { defineFn } from "@browserbasehq/sdk-functions";
import { chromium } from "playwright-core";

defineFn("my-function", async (context) => {
  const { session, params } = context;
  
  // Connect to browser
  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;
  
  // Your automation
  await page.goto(params.url || "https://example.com");
  const title = await page.title();
  
  // Return JSON-serializable result
  return { success: true, title };
});
```

**关键对象：**
- `context.session.connectUrl`：用于连接Playwright的CDP（Chrome DevTools Protocol）端点
- `context.params`：函数调用时传递的输入参数

## 开发流程

### 1. 启动开发服务器

```bash
pnpm bb dev index.ts
```

开发服务器的运行地址为`http://127.0.0.1:14113`

### 2. 在本地进行测试

```bash
curl -X POST http://127.0.0.1:14113/v1/functions/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"params": {"url": "https://news.ycombinator.com"}}'
```

### 3. 迭代开发

开发服务器会在文件更改时自动重新加载。可以使用`console.log()`进行调试，调试信息会显示在终端中。

## 部署

### 将函数发布到Browserbase

```bash
pnpm bb publish index.ts
```

部署完成后，会得到以下输出：
```
Function published successfully
Build ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Function ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**请保存函数ID**——您需要该ID来调用已发布的函数。

## 调用已发布的函数

### 通过curl调用

```bash
# Start invocation
curl -X POST "https://api.browserbase.com/v1/functions/FUNCTION_ID/invoke" \
  -H "Content-Type: application/json" \
  -H "x-bb-api-key: $BROWSERBASE_API_KEY" \
  -d '{"params": {"url": "https://example.com"}}'

# Response: {"id": "INVOCATION_ID"}

# Poll for result
curl "https://api.browserbase.com/v1/functions/invocations/INVOCATION_ID" \
  -H "x-bb-api-key: $BROWSERBASE_API_KEY"
```

### 通过代码调用

```typescript
async function invokeFunction(functionId: string, params: object) {
  // Start invocation
  const invokeRes = await fetch(
    `https://api.browserbase.com/v1/functions/${functionId}/invoke`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-bb-api-key': process.env.BROWSERBASE_API_KEY!,
      },
      body: JSON.stringify({ params }),
    }
  );
  const { id: invocationId } = await invokeRes.json();

  // Poll until complete
  while (true) {
    await new Promise(r => setTimeout(r, 5000));
    
    const statusRes = await fetch(
      `https://api.browserbase.com/v1/functions/invocations/${invocationId}`,
      { headers: { 'x-bb-api-key': process.env.BROWSERBASE_API_KEY! } }
    );
    const result = await statusRes.json();
    
    if (result.status === 'COMPLETED') return result.results;
    if (result.status === 'FAILED') throw new Error(result.error);
  }
}
```

## 常见用法

### 参数化爬取

```typescript
defineFn("scrape", async ({ session, params }) => {
  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;
  
  await page.goto(params.url);
  await page.waitForSelector(params.selector);
  
  const items = await page.$$eval(params.selector, els => 
    els.map(el => el.textContent?.trim())
  );
  
  return { url: params.url, items };
});
```

### 带有身份验证的脚本

```typescript
defineFn("authenticated-action", async ({ session, params }) => {
  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;
  
  // Login
  await page.goto("https://example.com/login");
  await page.fill('[name="email"]', params.email);
  await page.fill('[name="password"]', params.password);
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard');
  
  // Do authenticated work
  const data = await page.textContent('.user-data');
  return { data };
});
```

### 错误处理

```typescript
defineFn("safe-scrape", async ({ session, params }) => {
  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;
  
  try {
    await page.goto(params.url, { timeout: 30000 });
    await page.waitForSelector(params.selector, { timeout: 10000 });
    
    const data = await page.textContent(params.selector);
    return { success: true, data };
  } catch (error) {
    return { 
      success: false, 
      error: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
});
```

## CLI参考

| 命令 | 描述 |
|---------|-------------|
| `pnpm dlx @browserbasehq/sdk-functions init <名称>` | 创建新项目 |
| `pnpm bb dev <文件>` | 启动本地开发服务器 |
| `pnpm bb publish <文件>` | 将函数部署到Browserbase |

## 故障排除

### “缺少API密钥”
```bash
# Check credentials
stagehand fn auth status

# Set for current shell
eval "$(stagehand fn auth export)"

# Or add to .env in project directory
```

### 开发服务器无法启动
```bash
# Make sure SDK is installed
pnpm add @browserbasehq/sdk-functions

# Or use npx
npx @browserbasehq/sdk-functions dev index.ts
```

### 函数执行超时
- 最大执行时间为15分钟
- 可为特定页面操作设置超时时间
- 使用`waitForSelector`代替`sleep`函数进行等待

### 无法连接到浏览器
- 确保`session.connectUrl`的设置正确
- 使用`chromium.connectOverCDP()`而不是`chromium.launch()`来连接浏览器