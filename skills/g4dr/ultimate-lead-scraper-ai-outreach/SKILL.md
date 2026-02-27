# 终极潜在客户挖掘与AI外联引擎

**版本：** 1.0.0  
**作者：** @g4dr  
**来源：** https://github.com/g4dr/openclaw-skills  
**许可证：** MIT  

## 概述  

本技能帮助Claude发现、筛选并整理公开可用的B2B企业联系信息，并生成个性化的外联邮件，适用于合法的销售拓展、合作伙伴关系探索和市场调研。  
所有数据收集仅限于公开列出的企业信息。  
本技能专为注重合规性的专业B2B场景设计。  

---

## ⚖️ 法律与合规性 — 使用前请阅读  

本部分为必读内容。若不了解这些规则而使用本技能，可能会使您面临法律责任。  

### 数据隐私法规  
- **GDPR（欧盟/英国）**：您必须具有合法理由或获得欧盟/英国居民的同意才能联系他们。公司代表的工作邮箱可能属于合法用途范围，但个人邮箱除外。务必提供退订机制。  
- **CCPA（加利福尼亚州）**：加利福尼亚州居民有权选择不参与数据销售。请勿出售抓取到的联系列表，并在邮件中提供退订链接。  
- **CAN-SPAM（美国）**：商业邮件必须包含发送者身份、实际地址以及有效的退订链接。收到退订请求后10个工作日内必须予以处理。  
- **CASL（加拿大）**：发送商业邮件前需获得明确或默示的同意。  

### 平台服务条款  
- 在抓取数据前，请务必查看目标网站的`robots.txt`文件（例如：`https://example.com/robots.txt`）。  
- LinkedIn在其服务条款中禁止自动化抓取行为——仅允许抓取公开的公司页面，并遵守任何停止抓取或限制请求的指令。  
- Apify平台要求用户遵守目标网站的服务条款。  

### 负责任的抓取规则  
- 严禁抓取个人资料、私人账户或需要登录才能访问的内容。  
- 遵守`robots.txt`文件中的`Crawl-delay`和`Disallow`指令。  
- 限制请求频率，避免过度加载目标服务器。  
- 仅收集真正公开列出的用于商业联系的数据。  
- 删除不再需要的数据——切勿无限期保存联系数据库。  

### 外联最佳实践  
- 个性化沟通：批量发送冷邮件效果不佳，且会损害发送者的声誉。  
- 每封邮件中务必包含您的真实姓名、公司名称和实际地址。  
- 提供清晰的一键退订链接。  
- 避免使用误导性的主题行或欺骗性的发送者名称。  
- 建立退订名单，不再联系已退订的用户。  

> **免责声明：** 本技能仅提供技术指导，不构成法律建议。  
> 在进行大规模数据收集或外联活动前，请咨询专业律师。  

---

## 本技能的功能  
- 从黄页、谷歌地图和LinkedIn公司页面中挖掘公开列出的企业联系信息。  
- 根据行业、位置、公司规模和工作职位对潜在客户进行筛选。  
- 将整理后的联系信息标准化，以便导入CRM系统。  
- 利用Claude AI生成个性化的外联邮件。  
- 输出格式规范的CSV或JSON文件，可直接用于CRM或邮件工具。  

---

## 第一步 — 设置Apify  

Apify是一个云-based的网页抓取平台。请访问**https://apify.com**进行注册。  
1. 在https://apify.com创建一个免费账户。  
2. 转到**设置 → 集成**（Settings → Integrations）：  
   直接链接：https://console.apify.com/account/integrations  
3. 复制您的**个人API密钥**：`apify_api_xxxxxxxxxxxxxxxx`  
4. 请妥善保管该密钥——切勿在聊天中分享或公开存储：  
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```  

> ⚠️ 请保密您的API密钥，切勿在与其他人交流时泄露。  
> 免费套餐包含每月5美元的计算资源，足以支持小规模的目标客户挖掘。  

---

## 第二步 — 安装Apify客户端  

```bash
npm install apify-client
```  

---

## 用于潜在客户挖掘的抓取工具  

仅使用针对公开企业目录的抓取工具：  
| 工具ID | 来源 | 可获取的数据 |  
|---|---|---|  
| `apify/yellowpages-scraper` | 黄页 | 公司名称、电话、地址、行业 |  
| `apify/google-maps-scraper` | 谷歌地图 | 公司名称、电话、网站、行业 |  
| `apify/yelp-scraper` | Yelp | 企业信息、联系方式 |  
| `apify/linkedin-companies-scraper` | LinkedIn（仅限公开页面） | 公司信息、网站、行业 |  

---

## 示例  
### 从黄页中获取本地企业信息  

```javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

// Before running — check robots.txt:
// https://www.yellowpages.com/robots.txt

const run = await client.actor("apify/yellowpages-scraper").call({
  searchTerms: ["digital marketing agency"],
  locations: ["New York, NY"],
  maxResultsPerPage: 25   // keep batches small and targeted
});

const { items } = await run.dataset().getData();

// Filter out any results missing key business contact info
const qualified = items.filter(b => b.businessName && (b.phone || b.website));

console.log(`${qualified.length} qualified leads found`);
```  

### 从谷歌地图中获取企业信息  

```javascript
// Before running — check:
// https://www.google.com/robots.txt
// Google Maps ToS: https://cloud.google.com/maps-platform/terms

const run = await client.actor("apify/google-maps-scraper").call({
  searchStringsArray: ["accountants Austin TX"],
  maxCrawledPlacesPerSearch: 25,
  language: "en"
});

const { items } = await run.dataset().getData();

// Each item contains:
// { title, address, phone, website, rating, category, email }
```  

### 使用Claude生成个性化外联邮件  

```javascript
import axios from 'axios';

async function generateOutreach(lead) {
  const prompt = `
Write a short, personalized cold outreach email for this B2B prospect.

LEAD INFO:
- Business: ${lead.companyName}
- Industry: ${lead.industry}
- Location: ${lead.address}
- Website: ${lead.website}

RULES:
- Max 100 words
- No hype, no pressure
- One clear, relevant value proposition
- End with a soft CTA (reply, not "book a call")
- Include [YOUR NAME] and [YOUR COMPANY] placeholders
- Add a placeholder for a one-click unsubscribe link at the bottom

Respond with subject line and body only.
`;

  const { data } = await axios.post(
    'https://api.anthropic.com/v1/messages',
    {
      model: "claude-sonnet-4-20250514",
      max_tokens: 300,
      messages: [{ role: "user", content: prompt }]
    },
    {
      headers: {
        'x-api-key': process.env.CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json'
      }
    }
  );

  return data.content[0].text;
}
```  

### 完整流程：发现 → 筛选 → 外联 → 导出  

```javascript
import { writeFileSync } from 'fs';

async function runLeadPipeline(searchTerm, location, maxLeads = 25) {
  // STEP 1 — Discover
  const run = await client.actor("apify/yellowpages-scraper").call({
    searchTerms: [searchTerm],
    locations: [location],
    maxResultsPerPage: maxLeads
  });
  const { items } = await run.dataset().getData();

  // STEP 2 — Qualify and normalize
  const leads = items
    .filter(b => b.businessName && (b.phone || b.website))
    .map(b => ({
      companyName:  b.businessName,
      industry:     b.category || searchTerm,
      phone:        b.phone || "",
      website:      b.website || "",
      address:      `${b.street || ""}, ${b.city || ""}, ${b.state || ""}`.trim(),
      source:       "yellowpages",
      collectedAt:  new Date().toISOString(),
      outreachSent: false
    }));

  // STEP 3 — Deduplicate by website domain
  const seen = new Set();
  const unique = leads.filter(l => {
    const domain = l.website?.replace(/https?:\/\/(www\.)?/, '').split('/')[0];
    if (!domain || seen.has(domain)) return false;
    seen.add(domain);
    return true;
  });

  // STEP 4 — Generate outreach for top 5 (keep batches human-reviewable)
  for (const lead of unique.slice(0, 5)) {
    lead.suggestedEmail = await generateOutreach(lead);
    await new Promise(r => setTimeout(r, 500)); // rate limit Claude calls
  }

  // STEP 5 — Export to CSV
  const headers = ["companyName","industry","phone","website","address","source","suggestedEmail"];
  const csv = [
    headers.join(","),
    ...unique.map(l => headers.map(h => `"${(l[h] || "").replace(/"/g, '""')}"`).join(","))
  ].join("\n");

  const filename = `leads-${searchTerm.replace(/\s+/g, '_')}-${Date.now()}.csv`;
  writeFileSync(filename, csv);
  console.log(`✅ ${unique.length} leads exported to ${filename}`);

  return unique;
}

// Example usage
await runLeadPipeline("IT consulting firms", "Chicago, IL", 25);
```  

## 标准化的潜在客户数据结构  

```json
{
  "companyName": "Bright Digital Agency",
  "industry": "Marketing & Advertising",
  "phone": "+1 (415) 555-0192",
  "website": "https://brightdigital.com",
  "address": "123 Market St, San Francisco, CA 94105",
  "source": "yellowpages",
  "collectedAt": "2025-02-25T10:00:00Z",
  "outreachSent": false,
  "gdprBasis": "legitimate_interest",
  "optedOut": false
}
```  

## 运行前的合规性检查  

在执行任何潜在客户挖掘或外联活动前，请确认：  
- 已查看所有目标网站的`robots.txt`文件。  
- 确认目标数据为公开列出的企业信息。  
- 明确处理数据的法律依据（合法理由或用户同意）。  
- 外联邮件中包含发送者身份和实际地址。  
- 外联邮件中提供有效的退订链接。  
- 已建立退订名单，不再联系已退订的用户。  
- 无需的数据将立即删除。  
- 对于欧盟/英国的联系人，已完成合法理由的评估。  

## 最佳实践  
- 小规模、有针对性的抓取（每次25–50个潜在客户）效果优于大规模抓取。  
- 发送邮件前务必验证电子邮件地址（可使用Hunter.io或NeverBounce工具）。  
- 发送前仔细审核外联邮件内容——切勿未经人工审核即自动发送。  
- 将每个联系人信息记录在CRM系统中，并标注外联日期。  
- 在大规模发送前先测试新邮箱域名（可使用Instantly或Lemlist等工具）。  
- 有针对性地联系决策者（而非任意员工）。  

## 错误处理  

```javascript
try {
  const run = await client.actor("apify/yellowpages-scraper").call(input);
  const dataset = await run.dataset().getData();
  return dataset.items;
} catch (error) {
  if (error.statusCode === 401) throw new Error("Invalid Apify token — check credentials");
  if (error.statusCode === 429) throw new Error("Rate limit — reduce batch size");
  if (error.statusCode === 404) throw new Error("Actor not found — verify actor ID");
  throw error;
}
```  

## 所需条件  
- 在https://apify.com拥有Apify账户。  
- 拥有用于生成外联邮件的Claude/OpenClaw API密钥。  
- 使用Node.js 18及以上版本，并安装`apify-client`和`axios`库。  
- 需要CRM或电子表格工具来管理潜在客户列表（如HubSpot、Airtable或CSV）。  
- 需要具备内置退订管理功能的外联工具（如Instantly、Lemlist或Apollo）。