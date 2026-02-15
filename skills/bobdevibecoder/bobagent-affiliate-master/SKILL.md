---
name: affiliate-master
description: 专为 OpenClaw 代理设计的全面型联盟营销自动化工具。该工具能够生成、跟踪和优化联盟链接，并确保所有披露信息符合美国联邦贸易委员会（FTC）的规定，同时支持多网络联盟营销策略。
metadata:
  {
    "openclaw":
      {
        "version": "1.0.0",
        "author": "Vernox",
        "license": "MIT",
        "tags": ["affiliate", "marketing", "monetization", "automation", "ftc-compliance"],
        "category": "marketing",
      },
  }
---

# AffiliateMaster – 联盟营销自动化工具

**Vernox的首个盈利工具：将内容转化为现金。**

## 概述

AffiliateMaster是一款专为OpenClaw代理设计的全面联盟营销自动化工具，涵盖了从链接生成到收入追踪的整个联盟营销流程，并内置了符合联邦贸易委员会（FTC）规定的功能。

## 主要功能

### ✅ 链接管理
- 从多个联盟网络（Amazon、ShareASale、CJ、Impact）生成联盟链接
- 跟踪点击量、转化率和收入
- 自动链接缩短和品牌化
- 链接健康状况监控

### ✅ 符合FTC规定
- 所有内容均自动添加披露声明
- 可自定义披露模板
- 适用于不同平台的格式（博客、社交媒体、电子邮件）
- 提供合规性审计日志

### ✅ 内容集成
- 自动检测适合添加联盟链接的内容
- 根据上下文智能插入链接
- 生成点击号召语（CTA）文本
- 支持A/B测试链接布局

### ✅ 多网络支持
- Amazon Associates
- ShareASale
- Commission Junction (CJ)
- Impact
- 通过API支持自定义联盟网络

### ✅ 分析与优化
- 实时收入仪表盘
- 转化率追踪
- 识别最受欢迎的产品
- 提供自动化优化建议

## 安装

```bash
clawhub install affiliate-master
```

## 快速入门

### 1. 配置API密钥

```bash
# Edit config file
~/.openclaw/skills/affiliate-master/config.json
```

```json
{
  "networks": {
    "amazon": {
      "accessKey": "YOUR_ACCESS_KEY",
      "secretKey": "YOUR_SECRET_KEY",
      "associateId": "YOUR_ASSOCIATE_ID",
      "region": "us-east-1"
    },
    "shareasale": {
      "apiKey": "YOUR_API_KEY",
      "affiliateId": "YOUR_AFFILIATE_ID"
    }
  },
  "disclosure": {
    "text": "This post contains affiliate links. If you buy through these links, we may earn a commission at no extra cost to you.",
    "placement": "top",
    "platforms": {
      "blog": "above-fold",
      "twitter": "end",
      "email": "footer"
    }
  }
}
```

### 2. 生成第一个联盟链接

```javascript
// Find a product
const products = await affiliateMaster.searchProduct('wireless headphones');

// Generate affiliate link
const link = await affiliateMaster.generateLink({
  network: 'amazon',
  product: products[0]
});

// Result:
// {
//   "originalUrl": "https://amazon.com/dp/B0XXXXX",
//   "affiliateUrl": "https://amzn.to/3xxxxx?tag=your-id-20",
//   "disclosure": "Affiliate link",
//   "trackingId": "aff_12345"
// }
```

### 3. 将链接插入内容中

```javascript
const content = `Check out these amazing wireless headphones! They have great sound quality.`;

const enhanced = await affiliateMaster.enhanceContent(content, {
  autoInsert: true,
  disclosurePlacement: 'top'
});

// Result: Content with affiliate links and FTC disclosure inserted
```

## 工具功能

### `generateLink`
生成产品的联盟链接。

**参数：**
- `network` (string): 联盟网络名称（amazon, shareasale, cj, impact）
- `product` (object): 产品数据（id, url, name）
- `shorten` (boolean): 是否生成缩短链接（默认值：true）

**返回值：**
- `affiliateUrl`: 生成的联盟链接
- `disclosure`: 必需的披露声明文本
- `trackingId`: 唯一的跟踪标识符

### `searchProduct`
在多个联盟网络中搜索产品。

**参数：**
- `query` (string): 搜索查询
- `network` (string): 搜索的网络（默认值：全部）
- `category` (string): 产品类别过滤器

**返回值：**
- 匹配的产品列表，包含价格和佣金率

### `enhanceContent`
自动将联盟链接插入内容中。

**参数：**
- `content` (string): 原始内容
- `options` (object):
  - `autoInsert` (boolean): 是否自动检测适合添加链接的位置
  - `disclosurePlacement` (string): 揭露声明的放置位置
  - `maxLinks` (number): 最大可插入的链接数量

**返回值：**
- 含有联盟链接和披露声明的优化后的内容

### `getAnalytics`
检索性能分析数据。

**参数：**
- `dateRange` (string): 7天、30天、90天或全部时间范围
- `network` (string): 按网络筛选（可选）

**返回值：**
- 点击量、转化率、收入、每点击费用（EPC）以及最受欢迎的产品

### `validateCompliance`
检查内容的合规性。

**参数：**
- `content` (string): 需要验证的内容
- `platform` (string): 平台类型（博客、社交媒体、电子邮件）

**返回值：**
- 合规性状态、缺失的披露声明以及优化建议

## 使用场景

### 博客变现
- 自动在产品评论中插入联盟链接
- 在所有帖子中添加FTC披露声明
- 跟踪哪些产品带来的收入最多

### 电子邮件营销变现
- 在精选的产品推荐中添加联盟链接
- 跟踪点击量和转化率
- 随时间优化产品推荐内容

### 社交媒体变现
- 为Twitter/X生成缩短的联盟链接
- 添加符合规定的披露声明
- 跟踪点击率

### 电子商务套利
- 比较不同联盟网络的佣金率
- 找到最高报酬的推广机会
- 自动生成链接

## 价格

- **免费版：** 每月最多生成1,000个链接
- **专业版：** 每月9美元 – 无限链接 + 高级分析功能
- **团队版：** 每月29美元 – 团队账户 + API访问权限

## 制定计划

- [ ] 与更多联盟网络集成
- [ ] 基于人工智能的产品推荐功能
- [ ] 根据性能数据自动优化
- [ ] 为产品目录批量生成链接
- [ ] 支持自定义域名以创建品牌化链接
- [ ] 实时佣金率提醒

## 合规性

AffiliateMaster的设计充分考虑了FTC规定：
- 自动生成披露声明
- 适用于各种平台的格式
- 提供审计日志以满足监管要求

**免责声明：** 本工具有助于遵守法规，但不能替代专业法律建议。如有具体的合规需求，请务必咨询法律专业人士。

## 支持

如遇问题、功能请求或疑问，请联系我们：
- GitHub: https://github.com/vernox/affiliate-master
- Discord: https://discord.gg/clawd

---

**生成收入。确保合规。自动化一切流程。**