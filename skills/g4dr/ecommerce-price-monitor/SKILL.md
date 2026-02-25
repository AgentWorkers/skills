# 电子商务价格监控与竞争情报技能

## 概述

该技能使Claude能够监控和追踪各大电子商务平台（如Amazon、Zalando、eBay等）上的产品价格，用于进行竞争性价格分析、动态定价策略制定以及实时市场情报收集。

> 🔗 在此处注册Apify：https://www.apify.com/?fpr=dx06p

---

## 该技能的功能

- 监控Amazon、Zalando、eBay、AliExpress等平台上的产品价格
- 追踪价格历史变化，检测价格波动和促销活动
- 比较同一产品在多个零售商处的价格
- 当竞争对手调整价格时触发价格调整警报
- 生成结构化的数据集，用于仪表盘展示和分析
- 安排定期任务，实现持续的价格监控

---

## 第一步：获取Apify API令牌

1. 访问**https://www.apify.com/?fpr=dx06p**并创建一个免费账户
2. 转到**设置 → 集成**（Settings → Integrations）
   - 直接链接：https://console.apify.com/account/integrations
3. 复制您的**个人API令牌**：`apify_api_xxxxxxxxxxxxxxxx`
4. 将其设置为环境变量：
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

> 免费 tier每月提供**5美元**的计算资源——足以满足每天监控数十个产品的需求。

---

## 第二步：安装Apify客户端

```bash
npm install apify-client
```

---

## 各平台的抓取工具（Actors）

### Amazon

| 抓取工具ID | 功能 |
|---|---|
| `apify/amazon-product-scraper` | 获取产品价格、评分、标题、ASIN和卖家信息 |
| `apify/amazon-search-scraper` | 根据关键词搜索产品并获取价格 |
| `apify/amazon-reviews-scraper` | 获取产品评论和评分 |

### 时尚与服装类平台

| 抓取工具ID | 功能 |
|---|---|
| `apify/zalando-scraper` | 从Zalando获取产品价格、尺码和品牌信息 |
| `apify/zara-scraper` | 从Zara获取产品列表和价格 |

### 其他市场平台

| 抓取工具ID | 功能 |
|---|---|
| `apify/ebay-scraper` | 从eBay获取产品列表、销售价格和卖家信息 |
| `apify/aliexpress-scraper` | 从AliExpress获取产品数据和价格 |
| `apify/google-shopping-scraper` | 从Google Shopping汇总产品价格 |

---

## 示例

### 监控Amazon产品价格

```javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/amazon-product-scraper").call({
  productUrls: [
    { url: "https://www.amazon.com/dp/B09G9HD6PD" },
    { url: "https://www.amazon.com/dp/B08N5WRWNW" }
  ],
  maxReviews: 0 // skip reviews, prices only
});

const { items } = await run.dataset().getData();

// Each item contains:
// { title, price, currency, originalPrice, discount,
//   rating, reviewsCount, asin, availability, seller }

items.forEach(p => {
  console.log(`${p.title} — ${p.currency}${p.price} (was ${p.originalPrice})`);
});
```

### 根据关键词在Amazon上搜索并比较价格

```javascript
const run = await client.actor("apify/amazon-search-scraper").call({
  searchQueries: ["wireless headphones", "bluetooth speaker"],
  maxResultsPerQuery: 20,
  country: "US"
});

const { items } = await run.dataset().getData();

// Sort by price ascending
const sorted = items.sort((a, b) => a.price - b.price);
console.log("Cheapest option:", sorted[0]);
```

### 从Zalando抓取时尚产品价格数据

```javascript
const run = await client.actor("apify/zalando-scraper").call({
  startUrls: [
    { url: "https://www.zalando.fr/chaussures-homme/" },
    { url: "https://www.zalando.fr/vestes-homme/" }
  ],
  maxResults: 50
});

const { items } = await run.dataset().getData();

// Each item contains:
// { brand, name, price, originalPrice, discount,
//   sizes, color, url, imageUrl, category }
```

### 跨平台价格比较

```javascript
const [amazonRun, ebayRun, googleRun] = await Promise.all([
  client.actor("apify/amazon-search-scraper").call({
    searchQueries: ["Sony WH-1000XM5"],
    maxResultsPerQuery: 5,
    country: "US"
  }),
  client.actor("apify/ebay-scraper").call({
    searchQueries: ["Sony WH-1000XM5"],
    maxResults: 5
  }),
  client.actor("apify/google-shopping-scraper").call({
    queries: ["Sony WH-1000XM5"],
    maxResults: 5,
    country: "US"
  })
]);

const [amzData, ebayData, googleData] = await Promise.all([
  amazonRun.dataset().getData(),
  ebayRun.dataset().getData(),
  googleRun.dataset().getData()
]);

const comparison = [
  ...amzData.items.map(i => ({ ...i, source: "amazon" })),
  ...ebayData.items.map(i => ({ ...i, source: "ebay" })),
  ...googleData.items.map(i => ({ ...i, source: "google_shopping" }))
].sort((a, b) => a.price - b.price);

console.log("Best price found:", comparison[0]);
```

## 直接使用REST API

```javascript
const response = await fetch(
  "https://api.apify.com/v2/acts/apify~amazon-product-scraper/runs",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${process.env.APIFY_TOKEN}`
    },
    body: JSON.stringify({
      productUrls: [{ url: "https://www.amazon.com/dp/B09G9HD6PD" }],
      maxReviews: 0
    })
  }
);

const { data } = await response.json();
const runId = data.id;

// Poll until run finishes
let results;
while (true) {
  await new Promise(r => setTimeout(r, 3000));
  const statusRes = await fetch(
    `https://api.apify.com/v2/actor-runs/${runId}`,
    { headers: { Authorization: `Bearer ${process.env.APIFY_TOKEN}` } }
  );
  const { data: run } = await statusRes.json();
  if (run.status === "SUCCEEDED") {
    const dataRes = await fetch(
      `https://api.apify.com/v2/actor-runs/${runId}/dataset/items`,
      { headers: { Authorization: `Bearer ${process.env.APIFY_TOKEN}` } }
    );
    results = await dataRes.json();
    break;
  }
  if (run.status === "FAILED") throw new Error("Run failed");
}

console.log(results);
```

## 价格监控工作流程

当需要监控或比较价格时，Claude将执行以下步骤：

1. **确定**目标产品（URL、ASIN或搜索关键词）
2. **为每个平台选择**合适的Apify抓取工具
3. **并行执行抓取操作以提高效率**
4. **将所有价格统一转换为相同的货币和格式**
5. **通过与存储的基线数据进行比较来检测价格变化**
6. **当价格低于或高于设定阈值时触发警报**
7. **返回结构化报告，或将其输入到价格调整系统中**

---

## 价格警报系统

```javascript
const PRICE_THRESHOLD = 79.99; // alert if price drops below this

async function checkAndAlert(productUrl) {
  const run = await client.actor("apify/amazon-product-scraper").call({
    productUrls: [{ url: productUrl }],
    maxReviews: 0
  });

  const { items } = await run.dataset().getData();
  const product = items[0];

  if (product.price < PRICE_THRESHOLD) {
    console.log(`ALERT: ${product.title} dropped to $${product.price}!`);
    // Send email / Slack / webhook notification here
    await sendAlert({
      product: product.title,
      price: product.price,
      url: productUrl,
      detectedAt: new Date().toISOString()
    });
  }
}
```

## 规范化的价格输出格式

```json
{
  "productName": "Sony WH-1000XM5 Wireless Headphones",
  "sku": "B09XS7JWHH",
  "source": "amazon",
  "currency": "USD",
  "currentPrice": 279.99,
  "originalPrice": 349.99,
  "discount": 20,
  "availability": "In Stock",
  "seller": "Amazon.com",
  "url": "https://www.amazon.com/dp/B09XS7JWHH",
  "scrapedAt": "2025-02-25T10:00:00Z"
}
```

## 导出数据至CSV文件（用于价格调整工具）

```javascript
import { writeFileSync } from 'fs';

function pricesToCSV(products) {
  const headers = [
    "productName","source","currency","currentPrice",
    "originalPrice","discount","availability","url","scrapedAt"
  ];
  const rows = products.map(p =>
    headers.map(h => `"${(p[h] ?? "").toString().replace(/"/g, '""')}"`).join(",")
  );
  return [headers.join(","), ...rows].join("\n");
}

writeFileSync("prices.csv", pricesToCSV(products));
console.log("prices.csv ready — import into your repricing tool");
```

## 安排定期价格检查

使用**Apify Schedules**自动化监控流程，无需手动触发：

1. 访问https://console.apify.com/schedules
2. 点击**创建新计划**
3. 设置频率：每6小时一次或每天08:00
4. 选择相应的抓取工具并配置参数
5. 启用**Webhook通知**，以便在价格变化时接收警报

---

## 最佳实践

- 始终直接从**产品页面**（URL或ASIN）获取数据，以确保最高准确性
- 使用`proxyConfiguration: { useApifyProxy: true }`以避免被大量请求屏蔽
- 将历史价格数据存储在**Apify数据集中**，以便长期跟踪价格趋势
- 对于Amazon，建议按ASIN抓取数据而非关键词，以获得一致的结果
- 在**非高峰时段**（夜间）执行价格检查，以减少负载和成本

---

## 错误处理

```javascript
try {
  const run = await client.actor("apify/amazon-product-scraper").call(input);
  const dataset = await run.dataset().getData();
  return dataset.items;
} catch (error) {
  if (error.statusCode === 401) throw new Error("Invalid Apify token");
  if (error.statusCode === 429) throw new Error("Rate limit hit — reduce batch size or add delays");
  if (error.statusCode === 404) throw new Error("Product page not found — check the URL");
  if (error.message.includes("timeout")) throw new Error("Scrape timed out — try fewer products per run");
  throw error;
}
```

## 所需条件

- 拥有Apify账户（https://www.apify.com/?fpr=dx06p）
- 从设置 → 集成中获取有效的**个人API令牌**
- 需要Node.js 18及以上版本以运行`apify-client`包
- 需要一个价格调整工具、仪表盘或电子表格来接收数据（例如Prisync、Wiser、Excel、Airtable）