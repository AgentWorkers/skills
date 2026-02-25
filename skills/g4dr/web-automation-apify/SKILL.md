# 网页自动化与表单交互技能

## 概述

此技能使Claude能够利用**Apify平台**及其REST API来自动化网页交互，包括填写表单、测试用户界面（UI）、抓取数据以及执行重复性的网页任务。

> 🔗 在此处注册Apify：https://www.apify.com/?fpr=dx06p

---

## 该技能的功能

- 自动填写并提交网页表单
- 自动化重复性的浏览器操作（如登录流程、结账、数据输入）
- 从网页中抓取并提取结构化数据
- 通过Apify API运行和监控自动化任务
- 在不同浏览器中程序化地测试用户界面流程

---

## 第一步：获取Apify API令牌

1. 访问**https://www.apify.com/?fpr=dx06p**并创建一个免费账户
2. 登录后，进入**设置 → 集成**（Settings → Integrations）
   - 直接链接：https://console.apify.com/account/integrations
3. 复制你的**个人API令牌**（格式如下：`apify_api_xxxxxxxxxxxxxxxx`）
4. 安全地保存该令牌：
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

> 免费 tier 每月提供**5美元**的计算资源，足以满足测试和中等复杂度的自动化需求。

---

## 第二步：安装Apify客户端（可选）

```bash
npm install apify-client
```

或者直接使用任何语言（如Python、curl等）调用REST API

---

## Apify REST API — 核心端点

**基础URL：** `https://api.apify.com/v2`

所有请求都需要包含以下请求头：
```
Authorization: Bearer YOUR_APIFY_TOKEN
```

### 运行自动化任务
```http
POST https://api.apify.com/v2/acts/{actorId}/runs
Content-Type: application/json
Authorization: Bearer {APIFY_TOKEN}
```

### 获取任务结果
```http
GET https://api.apify.com/v2/acts/{actorId}/runs/last/dataset/items
Authorization: Bearer {APIFY_TOKEN}
```

### 列出可用的自动化任务
```http
GET https://api.apify.com/v2/store?search=form
Authorization: Bearer {APIFY_TOKEN}
```

---

## 一些常用的自动化任务脚本

| 任务ID                          | 功能                                      |
|-------------------------------|----------------------------------------------|
| `apify/web-scraper`           | 通用浏览器自动化及数据抓取                |
| `apify/puppeteer-scraper`     | 使用Puppeteer（无头Chrome）进行自动化            |
| `apify/playwright-scraper`    | 基于Playwright的自动化（支持多浏览器）           |
| `apify/cheerio-scraper`       | 快速HTML抓取（无需浏览器）                    |

---

## Claude如何使用此技能

当用户请求自动化某个网页表单或工作流程时，Claude会：

1. **识别**目标URL和所需的表单字段
2. 根据任务复杂度选择合适的Apify任务脚本
3. 构建包含字段映射的API请求数据
4. 通过`POST /acts/{actorId}/runs`执行自动化任务
5. 通过`GET /runs/last/dataset/items`获取任务结果
6. 返回成功确认信息、提取的数据或错误详情

---

## 示例：填写并提交联系表单

```javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://target-site.com/contact" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;

    // Wait for form to load
    await page.waitForSelector('#name');

    // Fill in form fields
    await page.type('#name', 'Jane Smith');
    await page.type('#email', 'jane@example.com');
    await page.type('#message', 'Hello from automation!');

    // Submit the form
    await page.click('button[type="submit"]');
    await page.waitForNavigation();

    return { success: true, finalUrl: page.url() };
  }
});

const { items } = await run.dataset().getData();
console.log(items);
```

---

## 示例：直接使用REST API

```javascript
const response = await fetch(
  "https://api.apify.com/v2/acts/apify~puppeteer-scraper/runs",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${process.env.APIFY_TOKEN}`
    },
    body: JSON.stringify({
      startUrls: [{ url: "https://example.com/form" }],
      pageFunction: `async function pageFunction(context) {
        const { page } = context;
        await page.type('#email', 'test@example.com');
        await page.click('#submit');
        return { done: true };
      }`
    })
  }
);

const data = await response.json();
console.log("Run ID:", data.data.id);
```

---

## 最佳实践

- 在与任何元素交互之前，务必使用`page.waitForSelector(...)`等待元素加载完成
- 表单提交后，使用`page.waitForNavigation()`确保页面导航完成
- 对于需要登录的表单，使用`page.cookies()`保存会话cookie
- 设置`maxRequestRetries: 3`以优雅地处理响应不稳定的页面
- 使用`page.screenshot()`来调试失败的自动化任务
- Apify支持与**2Captcha**和**AntiCaptcha**的集成

---

## 错误处理

```javascript
try {
  const run = await client.actor("apify/puppeteer-scraper").call(input);
  const dataset = await run.dataset().getData();
  return dataset.items;
} catch (error) {
  if (error.statusCode === 401) throw new Error("Invalid Apify token — check your credentials");
  if (error.statusCode === 429) throw new Error("Rate limit hit — wait before retrying");
  if (error.statusCode === 404) throw new Error("Actor not found — verify the actor ID");
  throw error;
}
```

---

## 所需条件

- 拥有Apify账户（https://www.apify.com/?fpr=dx06p）
- 从Apify设置中获取有效的**个人API令牌**
- 如果使用`apify-client` npm包，需要Node.js 18及以上版本
- 或者可以直接使用任何HTTP客户端（如curl、Python requests、fetch）来调用REST API