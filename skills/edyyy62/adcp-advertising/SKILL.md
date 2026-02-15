---
name: adcp-advertising
displayName: AdCP Advertising
description: 利用人工智能自动化广告活动：创建广告、购买广告媒体、管理广告预算、寻找广告资源、投放展示广告和视频广告、开展CTV（Connected TV）广告活动，并优化广告效果。该工具非常适合用于营销自动化、程序化广告投放、广告购买、广告管理、活动优化、创意内容管理和广告效果追踪。支持通过自然语言发布Facebook广告、Google广告、展示广告和视频广告，以及多渠道广告活动。具备广告定向、受众细分、投资回报率（ROI）追踪和自动竞价等功能。
author: AdCP Community
license: MIT
homepage: https://docs.adcontextprotocol.org
repository: https://github.com/edyyy62/openclaw-adcp
category: advertising
subcategory: marketing-automation
type: agent
keywords:
  - advertising
  - ads
  - marketing
  - campaigns
  - adcp
  - programmatic
  - media-buying
  - display-ads
  - video-ads
  - facebook-ads
  - google-ads
  - ctv
  - connected-tv
  - marketing-automation
  - ad-management
  - campaign-optimization
  - targeting
  - roi-tracking
  - performance-marketing
  - retargeting
---

# 广告上下文协议（AdCP）广告技能

## 概述

**利用人工智能自动化您的广告活动。** 该技能使 OpenClaw 代理能够发现广告资源、启动广告活动、管理创意内容，并在展示广告、视频广告、CTV（Closed-Circuit Television，闭路电视）广告、音频广告等领域优化广告效果——所有这些都可以通过自然语言命令完成。

无需使用仪表板或填写表格，也无需具备广告平台的专门知识。

### 您可以做什么

- 🎯 **几分钟内启动广告活动** - “创建一个针对加利福尼亚州科技专业人士的 1 万美元展示广告活动”
- 🔍 **即时发现广告资源** - “为奢侈品牌寻找优质的视频广告位”
- 🎨 **轻松上传广告内容** - “将这些横幅图片作为创意内容上传”
- 📊 **实时追踪投资回报率（ROI）** - “按创意内容显示活动效果和点击率”
- 🎛️ **自动优化广告支出** - “将预算重新分配给表现最佳的广告包”
- 🌐 **精准定位** - 根据人口统计特征、行为习惯、兴趣爱好、地理位置和设备类型进行定向

### 适用人群

- **营销团队**：负责运行 Facebook 广告、Google 广告和多渠道广告活动
- **媒体采购人员**：管理跨发布平台的程序化广告支出
- **广告代理机构**：自动化客户广告活动的管理和报告
- **电子商务品牌**：发布产品广告并开展再营销活动
- **初创企业**：利用人工智能自动化工具进行精简的营销活动

### 为什么选择此技能？

- **无需学习曲线**：无需掌握复杂的广告平台
- **节省时间**：5 分钟内即可启动广告活动，而无需花费数小时进行手动设置
- **更明智地支出**：人工智能会自动将预算分配给表现最佳的广告包
- **更快扩展**：通过简单的命令管理无限数量的广告活动
- **无风险测试**：提供公共测试代理，无需任何设置

**官方 AdCP 仓库**：https://github.com/adcontextprotocol/adcp  
**官方 AdCP 文档**：https://docs.adcontextprotocol.org  
**完整文档索引**：https://docs.adcontextprotocol.org/llms.txt

## 何时使用此技能

当用户询问以下内容时，请使用此技能：

**广告活动管理**
- “创建一个展示广告活动”
- “为我的产品发布 Facebook 广告”
- “设置一个 5000 美元的视频广告活动”
- “暂停表现不佳的广告活动”

**广告资源发现与媒体采购**
- “为奢侈品牌寻找广告资源”
- “显示主要城市的 CTV 广告位”
- “有哪些展示广告选项？”
- “为一家科技初创企业购买广告媒体”

**创意内容管理**
- “上传这些横幅图片”
- “哪种创意内容的表现最好？”
- “将视频广告添加到我的广告活动中”
- “管理我的广告库”

**效果与优化**
- “我的广告活动效果如何？”
- “按渠道显示投资回报率”
- “优化我的广告支出”
- “将预算重新分配给表现最佳的广告包”
- **追踪展示次数和点击率”

**定位与受众**
- “定位加利福尼亚州的专业人士”
- “设置人口统计定位”
- **创建再营销活动”
- “按设备类型和时间段进行定位”

## 快速入门

### 启动您的第一个广告活动（5 分钟）

**无需设置。** 使用附带的测试代理来尝试所有功能：

**步骤 1：发现可用资源**
```
"Show me advertising capabilities"
```
浏览可用的渠道、发布平台和广告格式。

**步骤 2：寻找广告资源**
```
"Find display ads for a tech startup, budget $5000"
```
人工智能搜索并显示带有价格的匹配广告资源。

**步骤 3：启动广告活动**
```
"Create campaign with Product prod_123, $5000 budget, targeting California tech professionals"
```
广告活动立即上线。

**步骤 4：上传您的广告内容**
```
"Upload these banner images as creatives"
```
上传文件，立即获取创意内容 ID。

**步骤 5：监控效果**
```
"Show campaign metrics and ROI"
```
实时显示展示次数、点击次数和点击率。

### 实际使用示例

**快速启动广告活动：**
```
User: "I need to run display ads for my SaaS product"
Agent: [Discovers products] "Found 5 display packages. Want details?"
User: "Create campaign with Product 1, $10k budget, target CTOs"
Agent: [Creates campaign] "Campaign live! ID: mb_abc123"
```

**效果优化：**
```
User: "How are my video ads performing?"
Agent: [Shows metrics] "Package A: 2.3% CTR, Package B: 0.8% CTR"
User: "Move $5k from B to A"
Agent: [Reallocates] "Budget updated. Package A now $15k"
```

**多渠道广告活动：**
```
User: "Launch omnichannel campaign: display in CA, video in NYC, $50k total"
Agent: [Creates packages] "3 packages created across display and video"
```

## 工作原理

### 自然语言理解

自然地说话。该技能能理解以下内容：
- **预算**：例如 “5000 美元”、“五千美元”
- **地理位置**：例如 “加利福尼亚州”、“美国主要城市”、“纽约和洛杉矶”
- **受众**：例如 “科技专业人士”、“25-45 岁”、“高收入人群”
- **目标**：例如 “提高品牌知名度”、“推动转化”、“增加销售额”

### 进阶工作流程

**1. 发现阶段**
```
"Find video advertising for luxury brands"
```
↓ 代理搜索广告资源
↓ 显示带有价格的匹配广告资源
↓ 解释定位和广告格式

**2. 广告活动创建**
```
"Create campaign with Product 1, $25k, target professionals"
```
↓ 代理创建广告购买请求
↓ 设置定位信息
↓ 返回广告活动 ID 和状态

**3. 创意内容管理**
```
"Upload my banner ads"
```
↓ 代理同步创意内容
↓ 将创意内容分配到广告活动中
↓ 返回创意内容 ID

**4. 监控与优化**
```
"Show performance"
```
↓ 代理获取广告投放数据
↓ 按广告包/创意内容显示指标
↓ 提出优化建议

## 核心操作

### 创建广告活动
```javascript
const campaign = await testAgent.createMediaBuy({
  buyer_ref: 'campaign-2026-q1',
  brand_manifest: { url: 'https://acme.com' },
  packages: [{ product_id: 'premium_display', budget: 10000 }]
});
```

### 上传创意内容
```javascript
await testAgent.syncCreatives({
  creatives: [{ 
    buyer_ref: 'banner-300x250',
    url: 'https://cdn.acme.com/banner.jpg'
  }]
});
```

### 监控效果
```javascript
const delivery = await testAgent.getMediaBuyDelivery({
  media_buy_id: 'mb_abc123'
});
console.log(`CTR: ${delivery.totals.ctr}%, Spend: $${delivery.totals.spend}`);
```

有关完整的 API 文档，请参阅 [REFERENCE.md]；有关详细的工作流程，请参阅 [EXAMPLES.md]。

## 核心概念

### 8 项媒体购买任务

AdCP 提供了 8 项标准化的广告生命周期任务。更多信息请参阅 [媒体购买协议文档](https://docs.adcontextprotocol.org/docs/media-buy/)：

1. **get_adcp_capabilities** - 查阅代理功能和支持的广告类型（约 1 秒）
2. **get_products** - 使用自然语言查找广告资源（约 60 秒）
3. **list_creative_formats** - 查看创意内容规格（约 1 秒）
4. **create_media_buy** - 启动广告活动（几分钟到几天，可能需要审批）
5. **update_media_buy** - 修改广告活动（几分钟到几天）
6. **sync_creatives** - 上传创意内容（几分钟到几天）
7. **list_creatives** - 查询创意内容库（约 1 秒）
8. **get_media_buy_delivery** **追踪广告效果**（约 60 秒）

**完整任务参考**：https://docs.adcontextprotocol.org/docs/media-buy/task-reference/

### 品牌信息

品牌信息可以通过两种方式提供：

**URL 参考**（推荐方式 - 代理会自动获取品牌信息）：
```json
{
  "brand_manifest": {
    "url": "https://brand.com"
  }
}
```

**内联品牌信息**（包含完整品牌详情）：
```json
{
  "brand_manifest": {
    "name": "Brand Name",
    "url": "https://brand.com",
    "tagline": "Brand tagline",
    "colors": { "primary": "#FF0000" },
    "logo": { "url": "https://cdn.brand.com/logo.png" }
  }
}
```

### 定价模式

支持多种定价模式：
- **CPM**（每千次展示费用）：每 1000 次展示的固定价格
- **CPM-Auction**：基于出价的展示费用
- **CPCV**（每次完成观看的费用）：视频广告的完成观看次数
- **Flat-Fee**：固定广告活动费用
- **CPP**（每点击费用）：达到目标受众的比例

对于基于出价的定价，请在您的请求中包含 `bid_price`。

### 异步操作

AdCP **不是实时协议**。操作可能需要：
- **约 1 秒**：简单的查询（如广告格式、创意内容列表）
- **约 60 秒**：人工智能/推理操作（如广告资源查找）
- **几分钟到几天**：需要人工审批的操作（如广告活动创建）

请始终检查响应中的 `status` 字段：
- `completed`：操作成功完成
- `pending`：等待审批或处理中
- `failed`：操作失败（请查看错误详情）

### 定位功能

可以为广告活动应用定位信息：
```javascript
{
  targeting_overlay: {
    geo: {
      included: ['US-CA', 'US-NY'],  // DMA codes or regions
      excluded: ['US-TX']
    },
    demographics: {
      age_ranges: [{ min: 25, max: 44 }],
      genders: ['M', 'F']
    },
    behavioral: {
      interests: ['technology', 'gaming'],
      purchase_intent: ['consumer_electronics']
    },
    contextual: {
      keywords: ['innovation', 'design'],
      categories: ['IAB19'] // Technology & Computing
    }
  }
}
```

## 常见工作流程

### 工作流程 1：从发现广告资源到启动广告活动
```javascript
// 1. Discover capabilities
const caps = await agent.getAdcpCapabilities({});

// 2. Find products
const products = await agent.getProducts({
  brief: 'Q1 2026 brand awareness campaign for tech startup',
  brand_manifest: { url: 'https://startup.com' },
  filters: { channels: ['display', 'video'] }
});

// 3. Check creative formats
const formats = await agent.listCreativeFormats({
  format_types: ['display', 'video']
});

// 4. Create campaign
const campaign = await agent.createMediaBuy({
  buyer_ref: 'q1-2026-awareness',
  brand_manifest: { url: 'https://startup.com' },
  packages: [
    {
      buyer_ref: 'pkg-001',
      product_id: products.products[0].product_id,
      pricing_option_id: 'cpm-standard',
      budget: 15000
    }
  ],
  start_time: { type: 'asap' },
  end_time: '2026-03-31T23:59:59Z'
});

// 5. Upload creatives
await agent.syncCreatives({
  creatives: [...], // Your creative assets
  assignments: {
    'creative_001': ['pkg-001']
  }
});

// 6. Monitor performance
const delivery = await agent.getMediaBuyDelivery({
  media_buy_id: campaign.media_buy_id
});
```

### 工作流程 2：更新正在运行的广告活动
```javascript
// Pause, adjust budget, and resume campaign
await agent.updateMediaBuy({
  media_buy_id: 'mb_abc123',
  updates: {
    status: 'paused',
    budget_change: 5000, // Add $5000
    end_time: '2026-04-30T23:59:59Z'
  }
});

// Resume after adjustments
await agent.updateMediaBuy({
  media_buy_id: 'mb_abc123',
  updates: { status: 'active' }
});
```

**更多工作流程示例**：请参阅 [EXAMPLES.md]，其中包含创意内容管理、多渠道广告活动和优化工作的完整示例。

## 测试代理

用于开发和测试，请使用公共测试代理：

**代理 URL**：`https://test-agent.adcontextprotocol.org/mcp`  
**认证令牌**：`1v8tAhASaUYYp4odoQ1PnMpdqNaMiTrCRqYo9OJp6IQ`

**交互式测试地址**：**[testing.adcontextprotocol.org](https://testing.adcontextprotocol.org)**

## 错误处理

常见错误代码及原因：
- **400 Bad Request**：参数无效：
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "budget must be greater than 0",
    "field": "packages[0].budget"
  }
}
```

**401 Unauthorized**：缺少或无效的认证信息：
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid authentication token"
  }
}
```

**404 Not Found**：无效的 ID 参考：
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Product not found",
    "resource": "product_id: premium_video_30s"
  }
}
```

在处理响应之前，请始终检查错误信息：
```javascript
if (result.error) {
  console.error(`Error: ${result.error.message}`);
  return;
}
```

## 最佳实践

- **1. 先了解代理支持的功能**：在发送其他请求之前，先调用 `get_adcp_capabilities` 以了解代理的支持能力。
- **使用清晰的购买者参考信息**：使用描述性的 `buyer_ref` 值进行追踪，例如：“campaign-2026-q1-tech-launch”。
- **处理异步操作**：检查 `status` 字段，并对待处理的操作进行轮询。
- **编写详细的请求说明**：详细的请求说明有助于获得更匹配的广告资源，例如：“为面向 35-54 岁高收入人群的奢侈汽车品牌提供优质视频广告资源，重点提升品牌知名度，完成观看率需超过 70%。”
- **验证创意内容格式**：在上传之前，务必检查 `list_creative_formats` 以确保创意内容符合要求。
- **监控预算进度**：定期检查广告投放数据，确保广告活动按计划进行。

## 其他资源

- **官方 AdCP 文档**：https://docs.adcontextprotocol.org
- **完整文档索引**：https://docs.adcontextprotocol.org/llms.txt
- **媒体购买协议**：https://docs.adcontextprotocol.org/docs/media-buy/
- **快速参考**：https://docs.adcontextprotocol.org/docs/media-buy/quick-reference
- **任务参考**：https://docs.adcontextprotocol.org/docs/media-buy/task-reference/
- **快速入门指南**：https://docs.adcontextprotocol.org/docs/quickstart

### 本技能的文档资料

- **API 参考**：[REFERENCE.md] - 完整的 API 参考和架构
- **示例**：[EXAMPLES.md] - 实际广告活动示例
- **协议详情**：[PROTOCOLS.md] - MCP 与 A2A 协议的对比
- **定位策略**：[TARGETING.md] - 高级定位策略
- **创意内容管理**：[CREATIVE.md] - 创意内容管理指南

## 关键提醒

- **AdCP 是异步的**：操作可能需要几分钟到几天的时间。
- **可能需要人工审批**：请检查 `pending` 状态。
- **先了解代理支持的功能**：在发送其他请求之前，务必先调用 `get_adcp_capabilities`。
- **品牌信息很重要**：提供详细的品牌信息以获得更好的效果。
- **定位是叠加的**：产品定位 + 您自定义的定位信息 = 最终的定位设置。
- **创意内容格式有严格要求**：上传前务必验证创意内容是否符合格式要求。
- **监控广告效果**：定期检查广告投放数据以确保活动成功。

## 帮助资源

- **官方 AdCP 仓库**：https://github.com/adcontextprotocol/adcp
- **文档**：https://docs.adcontextprotocol.org
- **交互式测试**：https://testing.adcontextprotocol.org
- **完整 API 文档**：https://docs.adcontextprotocol.org/llms.txt