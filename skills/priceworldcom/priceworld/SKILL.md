---
name: priceworld
description: 关于网络托管、电子邮件营销、域名注册商、储蓄利率以及人工智能工具的定价信息：您可以查询实际价格，根据真实成本（包括续费费用）来比较不同服务提供商，发现隐藏的费用，并查看哪些银行在悄悄降低年化收益率（APY）。当用户询问软件定价、托管费用、域名续费、储蓄账户利率、人工智能订阅服务或预算建议时，这些信息都非常有用。
---
# PriceWorld — 价格洞察工具

提供5个类别的实时、经过验证的价格数据。我们关注您实际支付的价格，而非营销页面上显示的价格。

**官方网站：** https://priceworld.com  
**数据来源：** 通过直接支付测试，每月独立验证一次。

## 支持的类别  
- ✅ **网站托管**（8家提供商）：Hostinger、SiteGround、Bluehost、DreamHost、HostGator、WP Engine、A2 Hosting、InMotion Hosting  
- ✅ **电子邮件营销**（8个工具）：Mailchimp、Kit、Beehiiv、Buttondown、Brevo、ActiveCampaign、MailerLite、Klaviyo  
- ✅ **域名注册商**（5家注册商）：Namecheap、GoDaddy、Porkbun、Cloudflare、Squarespace（Google Domains）  
- ✅ **储蓄产品**（15家美国银行）：SoFi、Bread Savings、Bask Bank、CIT Bank、Popular Direct、Barclays、Wealthfront、Amex HYSA、Discover、TAB Bank、Capital One 360、Marcus、Betterment、Ally、UBF Direct  
- ✅ **人工智能服务**（8个工具）：ChatGPT Plus、Claude Pro、Gemini Advanced、Perplexity Pro、GitHub Copilot、Midjourney、Cursor、v0  

## 命令  

### 查看价格  
查询特定提供商的当前价格：  
```
priceworld:lookup <provider>
```  

**示例：**  
- `priceworld:lookup hostinger` — 查看Hostinger的托管计划及促销价与续费价  
- `priceworld:lookup beehiiv` — 根据订阅用户数量查看Beehiiv的电子邮件营销套餐  
- `priceworld:lookup godaddy` — 查看GoDaddy的域名注册、续费价格及隐藏费用  
- `priceworld:lookup sofi` — 查看SoFi的年化收益率（APY）及忠诚度评分  
- `priceworld:lookup chatgpt` — 查看ChatGPT的订阅价格及使用限制  

**返回内容：** 计划层级、价格信息、续费费用、隐藏费用、评分详情以及最后一次验证日期。  

### 比较提供商  
进行横向比较：  
```
priceworld:compare <provider1> <provider2>
```  

**示例：**  
- `priceworld:compare hostinger siteground` — 比较Hostinger和SiteGround的服务及价格  
- `priceworld:compare mailchimp kit` — 比较Mailchimp和Kit的电子邮件营销工具  
- `priceworld:compare cloudflare godaddy` — 比较Cloudflare和GoDaddy的服务及价格  

**返回内容：** 包含功能及价格对比的表格，并附有实际成本分析。  

### 找到最划算的选项  
查找性价比最高的选项：  
```
priceworld:cheapest <category> [--options]
```  

**示例：**  
- `priceworld:cheapest hosting` — 按三年总成本（TCO）排名  
- `priceworld:cheapest email-marketing --subscribers=5000` — 按每月成本（针对5000名订阅用户）排名  
- `priceworld:cheapest domains` — 按三年内.com域名的总成本排名  
- `priceworld:cheapest savings` — 按忠诚度评分（而非仅今日的年化收益率）排名  
- `priceworld:cheapest ai-costs` — 按每月价格排名  

**返回内容：** 按类别排名出的性价比最高的选项列表。  

### 检查续费价格  
查看促销期结束后提供商的收费标准：  
```
priceworld:renewal-check <provider>
```  

**示例：**  
`priceworld:renewal-check siteground` — 查看Hostinger的续费价格及涨价幅度  

**返回内容：** 促销价格、续费价格、涨价百分比以及三年总成本（TCO）。  

### 地区价格差异  
检查提供商是否因地区而异价：  
```
priceworld:regional <provider>
```  

**示例：**  
`priceworld:regional hostinger` — 查看Hostinger在不同地区的价格  

**返回内容：** 美国、欧盟、英国、印度和巴西地区的价格对比（以美元显示）。  

## 评分系统  
每个提供商都会获得一个基于数据的综合评分（1.0–5.0分）：  
- **4.5–5.0** 极佳性价比  
- **3.5–4.4** 良好性价比  
- **2.5–3.4** 一般  
- **1.5–2.4** 低于平均水平  
- **1.0–1.4** 低性价比  

评分依据公开的标准从可测量数据中得出，无主观评价，也不存在付费排名行为。完整评分方法请访问：https://priceworld.com/methodology/  

## 关键指标  
- **续费涨价百分比**：促销期结束后需支付的额外费用  
- **三年总成本（TCO）**：包括续费费用在内的总拥有成本  
- **忠诚度评分**：银行对联邦利率变化的响应能力（储蓄效果）  
- **利率差距**：银行年化收益率（APY）与联邦基金利率（Fed Rate）的差异  
- **“缩水通胀”现象**：人工智能工具在价格不变的情况下降低使用限制的情况  

## 数据更新频率  
- 所有价格信息均标注有“最后一次验证”日期  
- 托管/电子邮件/域名价格每月重新验证一次  
- 储蓄产品的利率每周与EFFR（有效联邦基金利率）进行对比  
- 人工智能工具的使用限制每周检查一次  
- 数据来源：官方供应商价格页面 + 直接支付测试  

## 价格说明  
- **货币：** 美元（托管服务提供地区价格）  
- **地区：** 默认为美国价格，托管服务支持5个地区  
- **年价：** 以月度等值形式显示  
- **不包括：** 税费/增值税（VAT）、一次性促销折扣  
- **包含：** 必需附加服务、续费费用及WHOIS隐私费用  

## 限制事项  
- 不包含企业级/定制定价方案  
- 储蓄数据仅涵盖美国银行（未来计划扩展至其他国家）  
- 人工智能工具的使用限制经常变动——请始终在供应商官网核实  
- 本工具与列出的任何提供商均无关联  

## 隐私与安全  
- 无需提供个人信息  
- **请勿粘贴API密钥、发票或账户截图**  
- 查询由辅助系统处理，用户数据不会被存储  

## 工具别名  
- Kit = ConvertKit（2024年重新命名）  
- A2 Hosting = hosting.com（正在重新品牌化中）  
- Google Domains = Squarespace Domains（2023年收购）  

---

*PriceWorld——追踪真实价格，而非营销宣传价格。*