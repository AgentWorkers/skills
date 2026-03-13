---
name: trading-card-specialist2
description: Trading card business automation and analysis for OpenClaw agents. Use for: (1) Card analysis and valuation - sports cards, Pokemon, vintage cards, condition assessment, market pricing, (2) eBay listing optimization - SEO titles, descriptions, pricing strategies, category selection, (3) Market intelligence - price trends, competitor tracking, investment opportunities, grading ROI analysis, (4) Inventory management - portfolio tracking, profit analysis, purchase recommendations, (5) Grading strategy - submission planning, grade prediction, service selection, ROI calculation, (6) Business automation - bulk listing generation, market alerts, competitor monitoring, automated reporting.
metadata:
  {
    "openclaw": {
      "emoji": "🃏", 
      "requires": {
        "env": [
          "EBAY_APP_ID",
          "EBAY_CERT_ID", 
          "EBAY_DEV_ID",
          "EBAY_USER_TOKEN",
          "PSA_API_KEY",
          "TWITTER_BEARER_TOKEN",
          "TWITTER_API_KEY", 
          "TWITTER_API_SECRET",
          "REDDIT_CLIENT_ID",
          "REDDIT_CLIENT_SECRET",
          "DATABASE_URL",
          "ENCRYPTION_PASSWORD"
        ],
        "optional_env": [
          "DISCORD_WEBHOOK_URL",
          "SMTP_SERVER",
          "SMTP_USERNAME", 
          "SMTP_PASSWORD",
          "SPORTS_REFERENCE_API_KEY",
          "MONGODB_URI",
          "ENCRYPTION_SALT"
        ]
      },
      "external_apis": [
        "eBay Trading API",
        "eBay Browse API", 
        "PSA Population API",
        "Twitter API v2",
        "Reddit API"
      ]
    }
  }
---

# Trading Card Specialist v2.0.2  
将您的 OpenClaw 代理转变为一个具备市场情报、列表优化和竞争分析能力的专业交易卡业务专家。  

## 概述  
该技能为经销商、收藏家和投资者提供了全面的交易卡业务自动化服务，涵盖了从单张卡片分析到企业级市场情报的整个工作流程。  

**核心功能**：市场分析、eBay 列表优化、评级策略制定、库存管理、竞争对手监控以及智能报告生成。  

**⚠️ 外部依赖**：该技能需集成 eBay API、PSA API 和社交媒体 API，并需要用户提供的凭据。详细要求请参阅 [CREDENTIALS.md]。  

**📋 v2.0.2 更新**：修正了元数据中的环境变量声明问题，确保 ClawHub 注册表的准确性。现在所有外部 API 凭据都在元数据和文档中得到了正确声明。  

## 快速操作  

### 基础卡片分析（免费 tier）  
```
"Analyze this 2023 Topps Chrome Ja Morant PSA 9"
"What should I price this card at?"
"Is this card worth grading?"
```  

### eBay 列表优化  
```
"Create an optimized eBay listing for this card" [attach photo]
"Improve my existing listing for better visibility"
"Generate SEO-optimized title and description"
```  

### 市场情报（高级版）  
```
"Track Luka Doncic rookie cards this month"
"What cards should I buy before playoff season?"
"Show me undervalued cards in my price range"
"Monitor top sellers in basketball cards"
```  

## 核心特性  

### 🔍 市场情报引擎  
- 来自 eBay、COMC、PWCC 等平台的实时价格信息  
- 基于历史数据的趋势分析和预测  
- 玩家表现与卡片价值之间的关联（统计数据的影响）  
- 评级数据整合（PSA、BGS、SGC）  
- 来自社交媒体和论坛的市场情绪监测  

### 📈 eBay 列表优化  
- 通过关键词研究优化标题  
- 以用户利益为中心的描述编写  
- 根据市场状况制定有竞争力的定价策略  
- 提供照片优化建议以提高转化率  
- 选择最佳发布时机以获得最大曝光度  

### 🎯 评级策略优化  
- 提供提交计划的投资回报率（ROI）计算工具  
- 通过照片分析评估卡片状况  
- 基于视觉缺陷的评级预测模型  
- 比较不同评级服务（PSA、BGS、SGC）的时效性和价值  
- 提交成本效益分析  

### 💰 盈利最大化工具  
- 提供带有信心评分的买卖建议  
- 跨体育项目/时代的投资组合多样化分析  
- 季节性趋势预测（如季后赛、新秀热潮周期）  
- 高价值卡片的风险管理  
- 库存周转率优化  

## 订阅层级  

### 免费 tier  
- 基础卡片分析和价格查询  
- 简单的 eBay 列表优化  
- 有限的市场研究（每天 5 次查询）  
- 社区支持  

### 高级订阅（每月 $99）  
- 无限分析和市场情报  
- 高级评级 ROI 计算  
- 批量列表优化（50 张以上卡片）  
- 实时警报和每日简报  
- API 集成（PSA、eBay、社交媒体平台）  
- 竞争对手监控和分析  
- 定制市场报告和预测  

### 企业级（定制价格）  
- 白标部署选项  
- 定制集成和工作流程  
- 专属支持和入职培训  
- 高级投资组合分析  
- 多平台自动化  

## 详细工作流程  

### 市场研究  
1. **目标定位**：体育项目、时代、价格范围、玩家标准  
2. **情报收集**：多平台数据采集  
3. **分析引擎**：模式识别和机会评估  
4. **可操作报告**：具体的购买/避免建议  
5. **持续监控**：表现跟踪和策略调整  

**详情请参阅**：[MARKET-RESEARCH.md](references/MARKET-RESEARCH.md)  

### 列表优化  
1. **投资组合审计**：当前列表的表现分析  
2. **关键词研究**：高流量、低竞争度的关键词  
3. **竞争分析**：顶级卖家的策略评估  
4. **批量优化**：标题/描述/价格更新  
5. **表现跟踪**：转化率提升的监控  

**详情请参阅**：[LISTING-OPTIMIZATION.md](references/LISTING-OPTIMIZATION.md)  

### 评级提交计划  
1. **收藏品评估**：潜在提交卡片的照片分析  
2. **评级预测**：基于 AI 的预测及置信区间  
3. **ROI 计算**：预期价值与评级成本  
4. **服务选择**：根据卡片类型和时间线选择合适的服务  
5. **提交跟踪**：进度监控和结果分析  

**详情请参阅**：[GRADING-STRATEGY.md](references/GRADING-STRATEGY.md)  

## 集成示例  

### 平台连接  
- **eBay 商店**：直接 API 用于列表管理和销售跟踪  
- **PSA/BGS/SGC**：卡片数量数据和认证验证  
- **社交媒体平台**：情绪分析和趋势检测  
- **Discord/Slack**：自动警报和每日市场简报  
- **库存系统**：Google Sheets、自定义数据库  

### API 合作伙伴（高级版）  
- **PSA API**：卡片数量报告、认证查询、提交跟踪  
- **Sports Reference**：玩家统计数据用于表现分析  
- **eBay API**：实时市场数据和列表优化  
- **社交媒体 API**：社区情绪和趋势分析  

**详情请参阅**：[INTEGRATIONS.md](references/INTEGRATIONS.md) 以获取设置指南  

## 安全与合规  

### 核心安全原则  
- 仅使用环境变量——切勿硬编码 API 凭据  
- 实施速率限制——遵守平台服务条款和服务器限制  
- **本地数据存储**：所有敏感信息保留在用户系统中  
- **审计日志**：完整记录 API 调用和数据访问  

### 网页抓取伦理  
- 充分遵守 robots.txt 和网站服务条款  
- 在可用情况下优先使用官方 API  
- 所有自动化数据收集均需用户同意  
- 定期监控平台政策变化  

### 生产环境部署  
- 使用 Tailscale ACL 配置以保护数据库访问安全  
- 敏感库存数据加密存储  
- 定期进行安全审计和令牌轮换  
- 制定紧急联系程序和事件响应机制  

**详情请参阅**：[SECURITY.md](references/SECURITY.md) 以获取完整的安全指南  

## 入门指南  

### 先决条件及所需凭据  
- 具有网页浏览功能的 OpenClaw 代理  
- **外部 API 凭据**：请参阅 [CREDENTIALS.md] 以获取完整设置信息  
- **必备**：用于市场数据和列表功能的 eBay API 凭据  
- **推荐**：用于卡片数量数据的 PSA API，以及用于情绪分析的社交媒体 API  
- **可选**：用于通知的 Discord Webhook 和用于高级功能的数据库  

**⚠️ 凭据透明度**：该技能需要集成多个外部 API。安装前请务必查阅 [CREDENTIALS.md] 以了解所需权限。  

### 快速设置  
1. **安装技能**：导入 `trading-card-specialist.skill`  
2. **设置偏好**：配置关注的体育项目/卡片类别  
3. **连接账户**：链接 eBay 和 Discord 以实现完整功能  
4. **开始分析**：尝试使用附有照片的卡片进行“分析”操作  

### 免费试用  
- 提供 7 天的高级功能试用  
- 全面访问高级分析和自动化功能  
- 支持团队协助进行设置和配置  

### 升级至高级版  
请联系您的 OpenClaw 提供商以激活订阅并获取 API 密钥。  

## 高级功能（高级版）  

### 自动化智能  
- 每日通过 Discord 或电子邮件发送市场简报  
- 对跟踪库存的卡片价格变动发出警报  
- 收到目标竞争对手的新列表通知  
- 分析突发新闻对卡片价值的影响  
- 提供季节性机会提醒（如季后赛期间的溢价机会）  

### 商业智能  
- 为特定领域和策略定制市场报告  
- 通过 AI 提供购买建议  
- 根据风险/回报情况优化投资组合  
- 集成税务和会计系统以记录业务数据  

### 批量操作  
- 为大量库存生成批量列表  
- 提供投资组合再平衡建议  
- 调整整个库存的竞争定价  
- 优化销售和购买的时机  

**详情请参阅**：[PREMIUM-FEATURES.md](references/PREMIUM-FEATURES.md) 以了解详细功能。  

## 成功案例  

### 市场机会发现  
*“发现了一张 1986 年的 Fleer Jordan 卡片，只有 3 个 PSA 10 级评级。分析显示其价值应在 2.5 万美元以上，实际以 1.5 万美元出售，获利 2.8 万美元。”*  

### 列表优化结果  
*“使用该工具优化了 200 张卡片，第一个月的销售额增加了两倍。订阅费用在第一周内就收回了。”*  

### 评级策略成功案例  
*“准备提交价值 10 万美元的 50 张卡片。通过预测评级（从 9 级改为 8 级），节省了 8 万美元。”*  

## 支持与社区  
- **文档**：完整的指南和 API 参考  
- **Discord 社区**：活跃的经销商交流策略  
- **优先支持**：高级订阅用户可享受 24/7 的协助  
- **功能请求**：社区投票决定未来的功能改进  

---

**准备好提升您的交易卡业务了吗？** 从免费 tier 开始使用，待业务规模扩大后再升级至高级版。  
*该技能采用了专为交易卡行业开发的成熟市场情报方法和自动化优化技术。*