---
name: browserbase-create
description: **使用 stagehand CLI 指导 Claude 创建新的浏览器自动化脚本**

本指南将指导您使用 stagehand CLI 命令行工具来创建新的浏览器自动化脚本。以下是详细的步骤：

1. **安装 stagehand CLI：**
   首先，确保您已经在系统中安装了 stagehand CLI。如果您还没有安装，请访问 [stagehand 官网](https://stagehand.io/) 下载并安装适合您操作系统的版本。

2. **创建项目：**
   使用以下命令创建一个新的项目：
   ```
   stagehand new my_project
   ```
   将 `my_project` 替换为您想要命名的项目名称。

3. **进入项目目录：**
   使用以下命令进入项目目录：
   ```
   cd my_project
   ```

4. **编写脚本：**
   在项目目录中，您可以使用 `stagehand script` 命令来编写新的脚本。例如，要创建一个简单的脚本来打开 Google Chrome 浏览器并访问某个网页，您可以执行以下命令：
   ```
   stagehand script open_chrome https://www.google.com
   ```
   这将创建一个名为 `open_chrome` 的脚本文件，其中包含打开 Google Chrome 浏览器并导航到指定网址的代码。

5. **运行脚本：**
   使用以下命令运行脚本：
   ```
   stagehand run open_chrome
   ```
   脚本将按照您编写的代码执行相应的操作。

6. **调试脚本：**
   如果您在运行脚本时遇到问题，可以使用 `stagehand debug` 命令来调试脚本。例如，要单步执行脚本中的某一行代码，您可以执行以下命令：
   ```
   stagehand debug open_chrome step 5
   ```
   （将 `5` 替换为您想要调试的代码行号。）

7. **保存和退出：**
   完成脚本编写或调试后，您可以使用 `stagehand save` 命令保存脚本。要退出 stagehand CLI，只需输入 `stagehand exit` 即可。

通过以上步骤，您就可以使用 stagehand CLI 来创建和运行浏览器自动化脚本了。如果您需要更多关于 stagehand CLI 的帮助或示例，请查看 [stagehand 官方文档](https://stagehand.io/docs/)。
---

# 创建自动化技能

本技能将指导用户使用 `stagehand` 命令行工具（CLI）来创建新的浏览器自动化脚本。

## 使用场景

当以下情况发生时，可以使用本技能：
- 用户希望自动化某个网站任务
- 用户需要从网站中抓取数据
- 用户希望创建一个 Browserbase 功能
- 从零开始开发一个新的自动化脚本

## 工作流程

### 1. 明确目标

提出以下问题以了解需求：
- 需要自动化哪个网站/URL？
- 最终目标是什么（提取数据、提交表单、监控页面变化等）？
- 是否需要身份验证？
- 该自动化脚本应该按计划运行还是按需执行？

### 2. 交互式探索网站

启动一个本地浏览器会话以了解网站结构：
```bash
stagehand session create --local
stagehand goto https://example.com
```

使用快照功能来分析网站的 DOM 结构：
```bash
stagehand snapshot
```

截取屏幕截图以查看页面的视觉布局：
```bash
stagehand screenshot -o exploration.png
```

### 3. 确定关键元素

对于自动化的每个步骤，需要确定：
- 用于交互式元素的选取器（selectors）
- 所需的等待条件（wait conditions）
- 需要提取的数据

利用可访问性树（accessibility tree）来理解元素之间的关系：
```
[@0-5] button: "Submit"
[@0-6] textbox: "Email"
[@0-7] textbox: "Password"
```

### 4. 手动测试交互过程

在编写代码之前，先验证每个步骤是否能够正常工作：
```bash
stagehand fill @0-6 "test@example.com"
stagehand fill @0-7 "password123"
stagehand click @0-5
stagehand wait networkidle
stagehand snapshot
```

### 5. （如需）启用网络请求捕获功能

对于基于 API 的自动化脚本或调试过程，可以启用网络请求捕获功能：
```bash
stagehand network on
# perform actions
stagehand network list
stagehand network show 0
```

### 6. 创建自动化脚本

在理解整个流程后，创建一个完整的自动化脚本项目：
```bash
stagehand fn init my-automation
cd my-automation
```

该项目包含以下内容：
- `package.json`（包含项目依赖项）
- `.env` 文件（包含凭据信息，这些信息通常来自 `~/.stagehand/config.json`）
- `tsconfig.json`（类型配置文件）
- `index.ts` 模板文件

使用 `index.ts` 文件编写自动化逻辑：
```typescript
import { defineFn } from "@browserbasehq/sdk-functions";
import { chromium } from "playwright-core";

defineFn("my-automation", async (context) => {
  const { session } = context;
  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;

  // Your automation steps here
  await page.goto("https://example.com");
  await page.fill('input[name="email"]', context.params.email);
  await page.click('button[type="submit"]');
  
  // Extract and return data
  const result = await page.textContent('.result');
  return { success: true, result };
});
```

### 7. 本地测试

启动本地开发服务器：
```bash
pnpm bb dev index.ts
# or: stagehand fn dev index.ts
```

然后通过 `curl` 命令在本地执行自动化脚本：
```bash
curl -X POST http://127.0.0.1:14113/v1/functions/my-automation/invoke \
  -H "Content-Type: application/json" \
  -d '{"params": {"email": "test@example.com"}}'
```

### 8. 部署到 Browserbase

当准备好上线时，将自动化脚本部署到 Browserbase 平台：
```bash
pnpm bb publish index.ts
# or: stagehand fn publish index.ts
```

### 9. 进行生产环境测试

在部署后的环境中执行自动化脚本：
```bash
stagehand fn invoke <function-id> -p '{"email": "test@example.com"}'
```

## 最佳实践

### 选取器（Selectors）：
- 尽量使用数据属性（`data-testid`）而非 CSS 类名
- 将文本内容作为备选选择方式（例如 `text=Submit`）
- 避免使用不稳定的选取器（如 `nth-child`）

### 等待机制（Waiting）：
- 点击操作后务必等待页面导航或网络请求完成
- 对于动态生成的元素，使用 `waitForSelector` 等待条件
- 设置合理的超时时间

### 错误处理（Error Handling）：
- 将高风险操作放在 `try/catch` 块中处理
- 返回结构化的错误信息
- 记录中间步骤以便于调试

### 数据提取（Data Extraction）：
- 使用 `page.evaluate()` 方法进行复杂的数据提取
- 在返回数据之前对其进行验证
- 能够优雅地处理缺失的元素

## 示例：电子商务价格监控脚本
```typescript
defineFn("price-monitor", async (context) => {
  const { session, params } = context;
  const browser = await chromium.connectOverCDP(session.connectUrl);
  const page = browser.contexts()[0]!.pages()[0]!;

  await page.goto(params.productUrl);
  await page.waitForSelector('.price');

  const price = await page.evaluate(() => {
    const el = document.querySelector('.price');
    return el?.textContent?.replace(/[^0-9.]/g, '');
  });

  return {
    url: params.productUrl,
    price: parseFloat(price || '0'),
    timestamp: new Date().toISOString(),
  };
});
```