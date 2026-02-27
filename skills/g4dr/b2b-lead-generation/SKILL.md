# B2B潜在客户生成与业务联系人提取技能

## 概述

该技能使Claude能够收集并整理来自专业目录、公司页面和商业列表的**公开可用的业务联系人数据**，用于销售线索挖掘、市场研究和客户关系管理（CRM）系统的数据补充。

所有收集的数据仅针对**公开列出的业务信息**。该技能遵循GDPR、CCPA以及平台服务条款的最佳实践。

> 🔗 在此处注册Apify：https://www.apify.com/?fpr=dx06p

---

## 该技能的功能

- 从LinkedIn的公开页面中提取**企业概况和公司联系人信息**
- 从Yellow Pages、Yelp和本地目录中抓取**商业列表**
- 从行业特定的目录中收集**专业联系人详情**
- 将收集到的线索整理成格式清晰、适用于CRM系统的JSON或CSV格式
- 根据行业、位置、公司规模或职位名称对线索进行筛选和分类

---

## 法律与道德框架

该技能仅适用于**合法的B2B场景**：

- 仅针对**公开列出的**业务信息（不包括私人资料）
- 收集个人和企业自愿公开的数据
- 仅用于**商业线索挖掘**，而非个人数据收集
- 用户需负责遵守当地法规（如GDPR、CCPA、CAN-SPAM）
- 在联系提取到的线索时，必须提供**退出机制**
- 从不存储超出业务需求范围的敏感个人信息

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

> 免费 tier每月提供**5美元**的计算资源——足以支持定向线索挖掘活动。

---

## 第二步：安装Apify客户端

```bash
npm install apify-client
```

---

## 根据数据源划分的脚本执行器（Actors）

### LinkedIn（公开公司页面和个人资料页面）

| 执行器ID | 功能 |
|---|---|
| `apify/linkedin-companies-scraper` | 提取公司信息、规模、行业、网站 |
| `apify/linkedin-profile-scraper` | 抓取公开的专业个人资料 |
| `apify/linkedin-jobs-scraper` | 查找正在招聘的公司（表明有购买意向） |

> 注意：仅可访问公开的LinkedIn页面。需要登录才能访问的数据不在抓取范围内。

### Yellow Pages和本地目录

| 执行器ID | 功能 |
|---|---|
| `apify/yellowpages-scraper` | 企业名称、电话、地址、类别 |
| `apify/yelp-scraper` | 带有评分和联系信息的本地企业列表 |
| `apify/google-maps-scraper` | 带有电话、网站和营业时间的本地企业列表 |

### 专业和行业目录

| 执行器ID | 功能 |
|---|---|
| `apify/website-content-crawler` | 抓取任何公开的专业目录内容 |
| `apify/cheerio-scraper` | 从基于HTML的列表网站中快速提取数据 |

---

## 示例

### 从LinkedIn中提取公司联系人信息

```javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/linkedin-companies-scraper").call({
  startUrls: [
    { url: "https://www.linkedin.com/company/salesforce/" },
    { url: "https://www.linkedin.com/company/hubspot/" }
  ],
  maxResults: 50
});

const { items } = await run.dataset().getData();

// Each item contains:
// { name, website, industry, employeeCount,
//   headquarters, description, linkedinUrl }
```

---

### 从Yellow Pages中抓取本地企业线索

```javascript
const run = await client.actor("apify/yellowpages-scraper").call({
  searchTerms: ["digital marketing agency"],
  locations: ["New York, NY", "Los Angeles, CA", "Chicago, IL"],
  maxResultsPerPage: 30
});

const { items } = await run.dataset().getData();

// Each item contains:
// { businessName, phone, address, city, state,
//   zip, website, category, email }
```

### 从Google Maps中提取本地企业线索

```javascript
const run = await client.actor("apify/google-maps-scraper").call({
  searchStringsArray: ["accountants in Austin TX", "law firms in Miami FL"],
  maxCrawledPlacesPerSearch: 50,
  language: "en"
});

const { items } = await run.dataset().getData();

// Each item contains:
// { title, address, phone, website, rating,
//   reviewsCount, category, email, plusCode }
```

---

### 多源线索聚合流程

```javascript
const [ypRun, gmRun] = await Promise.all([
  client.actor("apify/yellowpages-scraper").call({
    searchTerms: ["IT consulting"],
    locations: ["San Francisco, CA"],
    maxResultsPerPage: 25
  }),
  client.actor("apify/google-maps-scraper").call({
    searchStringsArray: ["IT consulting San Francisco CA"],
    maxCrawledPlacesPerSearch: 25
  })
]);

const [ypData, gmData] = await Promise.all([
  ypRun.dataset().getData(),
  gmRun.dataset().getData()
]);

// Normalize and deduplicate by website domain
const allLeads = [...ypData.items, ...gmData.items];
const uniqueLeads = allLeads.filter(
  (lead, index, self) =>
    index === self.findIndex(l => l.website === lead.website)
);

console.log(`${uniqueLeads.length} unique leads collected`);
```

---

## 直接使用REST API

```javascript
const response = await fetch(
  "https://api.apify.com/v2/acts/apify~yellowpages-scraper/runs",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${process.env.APIFY_TOKEN}`
    },
    body: JSON.stringify({
      searchTerms: ["web design agency"],
      locations: ["Boston, MA"],
      maxResultsPerPage: 20
    })
  }
);

const { data } = await response.json();
const runId = data.id;

// Fetch results once run is complete
const results = await fetch(
  `https://api.apify.com/v2/actor-runs/${runId}/dataset/items`,
  { headers: { Authorization: `Bearer ${process.env.APIFY_TOKEN}` } }
);

const leads = await results.json();
```

---

## 线索信息丰富化工作流程

当收到构建线索列表的请求时，Claude将：

1. **明确**目标行业、位置、公司规模和职位名称的筛选条件
2. **选择**最合适的数据来源（目录、地图、LinkedIn）
3. **运行**带有指定筛选条件的相关Apify脚本
4. **按网站域名或电话号码去重**结果
5. **将所有字段统一到一致的格式中**
6. **导出**格式清晰、适用于CRM系统的JSON或CSV数据集

---

## 标准化的线索输出格式

```json
{
  "companyName": "Bright Digital Agency",
  "industry": "Marketing & Advertising",
  "website": "https://brightdigital.com",
  "phone": "+1 (415) 555-0192",
  "email": "hello@brightdigital.com",
  "address": "123 Market St, San Francisco, CA 94105",
  "employeeCount": "11-50",
  "source": "yellowpages",
  "extractedAt": "2025-02-25T10:00:00Z"
}
```

---

## 导出为CSV格式（适用于CRM系统）

```javascript
import { writeFileSync } from 'fs';

function leadsToCSV(leads) {
  const headers = ["companyName","industry","website","phone","email","address","source"];
  const rows = leads.map(l =>
    headers.map(h => `"${(l[h] || "").replace(/"/g, '""')}"`).join(",")
  );
  return [headers.join(","), ...rows].join("\n");
}

writeFileSync("leads.csv", leadsToCSV(leads));
console.log("leads.csv ready to import into your CRM");
```

---

## 最佳实践

- **针对企业而非个人**——重点收集公司邮箱和主要电话号码
- 将`maxResultsPerPage`设置为25–100，以控制成本并避免触发速率限制
- 在导入到CRM系统之前，始终**按域名或电话号码去重**
- 定期在Apify上运行脚本以保持线索列表的更新
- 使用Hunter.io或NeverBounce等服务验证邮箱地址的有效性
- 始终尊重用户的**退出请求**并维护抑制名单（ suppression list）

---

## 错误处理

```javascript
try {
  const run = await client.actor("apify/google-maps-scraper").call(input);
  const dataset = await run.dataset().getData();
  return dataset.items;
} catch (error) {
  if (error.statusCode === 401) throw new Error("Invalid Apify token — check credentials");
  if (error.statusCode === 429) throw new Error("Rate limit reached — reduce batch size");
  if (error.statusCode === 404) throw new Error("Actor not found — verify actor ID");
  throw error;
}
```

---

## 所需条件

- 一个Apify账户 → https://www.apify.com/?fpr=dx06p
- 来自设置 → 集成的有效**个人API令牌**
- 安装Node.js 18.0及以上版本以运行`apify-client`
- 用于接收导出线索的CRM系统或电子表格（如HubSpot、Salesforce、Airtable、CSV）