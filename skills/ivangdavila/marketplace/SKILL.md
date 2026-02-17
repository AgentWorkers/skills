---
name: Marketplace
slug: marketplace
version: 1.0.1
description: 作为买家、卖家或开发者，您可以通过平台对比、商品列表优化以及诈骗检测功能，在在线市场中轻松进行操作。
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 架构

本指南提供基于用户角色的市场参与建议。系统会根据用户的角色自动加载相应的文件。

```
marketplace/
├── buyer.md      # Price comparison, scam detection, negotiation
├── seller.md     # Listing creation, pricing, platform rules
├── builder.md    # Marketplace creation, economics, liquidity
├── arbitrage.md  # Price gaps, ROI calculations, ToS risks
└── compliance.md # Tax obligations, legal pitfalls, bans
```

## 快速参考

| 角色 | 文件 | 加载时机 |
|------|------|--------------|
| 购买商品 | `buyer.md` | 比较价格、识别骗局、进行谈判 |
| 卖出商品 | `seller.md` | 创建商品列表、定价、处理买家请求 |
| 建设市场平台 | `builder.md` | 平台设计、商业模式、支付系统 |
| 套利/转售 | `arbitrage.md` | 寻找价格差异、计算实际投资回报率 |
| 法律/税务问题 | `compliance.md` | 税务问题、服务条款违规、账户暂停 |

## 核心规则

### 1. 适用于特定平台，切勿通用化
- 每个平台都有独特的费用、规则和运营模式
- eBay拍卖与Amazon Buy Box、FB Marketplace的运作方式不同
- 必须明确指出所提供建议适用于哪个平台

### 2. 总成本，而非标价
- 计算总成本时需包括：平台费用、运费、税费、退货费用
- Amazon的推荐费根据商品类别不同，范围在8%至45%之间
- eBay的推荐费为13%以上，Poshmark为20%，Mercari的推荐费则有所差异

### 3. 识别骗局模式
- 在本地市场平台上使用库存图片是危险信号
- “寄到我的地址，我会额外支付费用”这种说法属于三角诈骗手段
- 在平台外进行交易将无法获得任何保护
- 新注册的账户、高价值商品以及交易紧迫性都可能是骗局的迹象

### 4. 定价策略：基于已售商品情况，而非仅看列表价格
- 列出的价格并不代表实际成交价格
- 必须研究已售商品的情况
- 考虑商品状况：状态为“良好”与“非常好”时，价格可能相差30%

### 5. 账户被暂停的风险是真实存在的
- 如果Amazon的买家投诉率（ODR）超过1%，账户可能会被封禁
- 操纵评论或虚假评价会导致永久封禁
- 来自品牌方的IP投诉会导致账户立即被暂停
- 拥有多个账户的用户可能会被立即终止服务

### 6. 费用计算复杂，切勿估算
- 必须精确计算各项费用：
- Amazon：推荐费 + FBA（亚马逊物流服务）费用 + 存储费用 + 退货处理费用 + 广告费用
- eBay：最终成交价格（根据商品类别而定）+ 推广费用 + 支付费用
- 在定价时需考虑退货情况（某些类别中退货成本可能占利润的15%-30%）

### 7. 需要实时数据
- 切勿仅凭记忆或培训数据来报价
- 库存情况和价格每小时都在变化
- 竞争对手的库存水平会影响最佳定价策略
- 在提供任何建议前，务必核实当前的市场状况