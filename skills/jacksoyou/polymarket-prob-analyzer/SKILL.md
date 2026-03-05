---
name: polymarket-prob-analyzer
description: 根据网络研究和分析，计算 Polymarket 事件的概率范围。当用户需要估算事件发生的概率、为交易决策提供概率范围，或按事件名称或 URL 请求 Polymarket 事件的分析时，可以使用此功能。
metadata:
  author: 小赚 (@xiaozhuan)
  version: "2.2.0"
  displayName: Polymarket Probability Analyzer
  difficulty: beginner
---
# Polymarket 概率分析器

**分析 Polymarket 事件并计算概率范围。**

## 概述

该技能通过收集来自多个在线来源的信息来分析 Polymarket 事件，并计算出相应的概率范围。使用 SkillPay.me 进行计费——每次分析费用为 0.001 美元。

## 工作原理

分析器遵循以下多步骤流程：

1. **事件识别**：解析用户提供的事件名称或 Polymarket URL。
2. **信息收集**：搜索相关新闻、专家观点和历史数据。
3. **概率计算**：分析收集到的信息以估算概率范围。
4. **计费检查**：检查用户的 SkillPay.me 账户余额；如需支付，则生成支付链接。
5. **结果返回**：返回包含置信水平的概率范围。

## 计费流程（使用正确的 SkillPay API 端点）

**首次使用用户：**
1. 通过 `/api/v1/billing/balance` 检查账户余额。
2. 如果余额 ≤ 0，通过 `/api/v1/billing/payment-link` 生成支付链接。
3. 用户点击链接并支付 8.00 美元（最低充值金额）。
4. 用户重新运行命令，分析继续进行。

**后续使用：**
1. 通过 `/api/v1/billing/balance` 检查账户余额。
2. 如果余额 ≥ 0.001 美元，通过 `/api/v1/billing/charge` 进行计费。
3. 分析立即开始。

**无需注册！** 用户只需支付一次费用，即可无限次使用该技能。

## 快速入门

```bash
# Analyze an event by name
python scripts/prob_analyzer.py --event "Will Bitcoin hit $100k by 2025?"

# Analyze by Polymarket URL
python scripts/prob_analyzer.py --url https://polymarket.com/event/bitcoin-100k

# Get detailed breakdown
python scripts/prob_analyzer.py --event "Trump 2024" --verbose

# Skip billing check (dev mode)
python scripts/prob_analyzer.py --event "Test" --skip-billing
```

## 使用方法

### 首次使用（余额不足）
```
User: "Analyze Bitcoin price to $100k"

→ Skill checks SkillPay.me balance
→ Balance insufficient → returns payment link
→ User clicks link, pays 8.00 USDT
→ User re-runs command
→ Analysis proceeds, returns probability ranges
```

### 后续使用（余额充足）
```
User: "Analyze Bitcoin price to $90k"

→ Skill checks SkillPay.me balance
→ Balance sufficient → runs analysis
→ Returns: Low: 40%, Mid: 60%, High: 75%
```

## 输出格式

### 标准输出
```
🎯 Event: Will Bitcoin hit $100k by 2025?

📊 Probability Range:
  Low:   35.0%  (Conservative estimate)
  Mid:   55.0%  (Balanced estimate)
  High:  70.0%  (Optimistic estimate)

📈 Confidence: Medium

🔑 Key Factors:
• Institutional adoption increasing
• Regulatory uncertainty remains
• Market volatility expected
• Historical price patterns suggest upward trend

📚 Sources: 12 sources analyzed
```

### 支付链接格式

当用户余额不足时：
```
💳 Checking SkillPay.me billing status...
   User ID: gateway_xxx...
   Cost: 0.001 USDT

💳 Payment Required - First-Time User

👉 https://skillpay.me/checkout/[link]

💰 To use this skill, please complete a one-time payment:
   Amount: 8.00 USDT (minimum top-up)
   Network: BNB Chain
   Currency: USDT (BEP-20)

   After payment, you'll get 8.00 + 0.001 = 8.001 USDT total balance
   Each analysis costs 0.001 USDT

💡 After completing payment, re-run this command to get your analysis!
```

### 详细输出
包含以下额外信息：
- 来源引用
- 影响因素的权重
- 历史对比数据
- 替代方案
- 风险因素

## 功能特点

### 事件特定分析

**比特币/加密货币事件：**
- 机构采用趋势
- 监管政策变化
- 技术分析（阻力位、市场动量）
- 历史上的 4 年周期
- ETF 流量和机构兴趣

**政治事件（特朗普/选举）：**
- 历史上现任者的优势
- 当前民意调查数据
- 经济指标
- 关键州分析
- 投票率模式

**经济事件（美联储/利率）：**
- 通货膨胀趋势
- 经济增长指标
- 美联储的信号和立场
- 市场预期
- 历史利率走势

### 概率计算

对于每个事件，该技能会计算以下概率：
- **低概率（20-40%）**：较为保守，考虑了负面情况。
- **中等概率（40-60%）**：较为平衡，综合了所有可用信息。
- **高概率（60-80%）**：较为乐观，假设条件有利。

每个概率估计都包含：
- 置信水平（低/中/高）
- 主要影响因素
- 来源引用

## 环境变量

### 开发者变量（用于发布）

```bash
export SKILLPAY_API_KEY=sk_f549ac2997d346d904d7908b87223bb13a311a53c0fa2f8e4627ae3c2d37b501
export SKILLPAY_SKILL_ID=polymarket-prob-analyzer
export SKILLPAY_PRICE=0.001
```

### 用户变量（自动生成）

无需用户进行任何配置！用户 ID 会自动从以下信息生成：
- Telegram ID（如果存在）
- OpenClaw Gateway ID
- 系统用户名
- UUID（备用）

## 开发者设置

### 首次设置

1. 在 SkillPay.me 上注册。
2. 获取 API 密钥。
3. 设置环境变量（见上文）。
4. 将技能打包并发布。

### 测试

```bash
# Test without billing
python scripts/prob_analyzer.py --event "Test" --skip-billing

# Test with billing
python scripts/prob_analyzer.py --event "Bitcoin $100k"
```

## 计费详情

- **费用**：每次分析 0.001 美元。
- **货币**：USDT（在 BNB 链上使用 BEP-20 协议）。
- **支付处理方**：SkillPay.me。
- **收入分配**：95% 归开发者，5% 作为平台费用。
- **用户体验**：支付一次后即可无限次使用。

## 故障排除

**“需要支付”**
→ 点击提供的支付链接。
→ 使用您的钱包支付 8.00 美元（最低充值金额）。
→ 重新运行分析命令。

**“余额不足”（首次使用）**
→ 点击支付链接。
→ 完成一次性支付。
→ 重新运行命令以继续使用。

**“支付失败”**
→ 检查您的 SkillPay.me 账户余额。
→ 确保钱包中有足够的 USDT（BEP-20）。
→ 联系 SkillPay.me 客服。

**“API 错误”**
→ 检查网络连接。
→ 验证 SkillPay.me 服务状态。
→ 重新尝试命令。

## 技术细节

- **语言**：Python 3。
- **依赖库**：requests（HTTP 客户端）。
- **计费 API**：SkillPay.me v1 端点：
  - `/api/v1/billing/balance`：检查用户余额。
  - `/api/v1/billing/payment-link`：生成支付链接（首次使用用户）。
  - `/api/v1/billing/charge`：按使用次数计费。
- **事件解析**：基于正则表达式的 URL 解析。
- **概率算法**：基于事件关键词的启发式分析。

## 最佳实践

1. **提供明确的事件名称**：具体事件有助于获得更准确的分析结果。
2. **在重要决策时使用详细输出模式**：获取详细的推理过程和影响因素。
3. **审查置信水平**：高置信度的结果更可靠。
4. **考虑完整的概率范围**：不要只关注中间值。

## 版本历史

- **2.2.0**：更新了 SkillPay API 端点（`v1/billing/balance`、`payment-link`、`charge`），以匹配 Polymarket-autotrader 的实现。
- **2.1.1**：尝试更新但发布时失败。
- **2.1.0**：之前的实现版本。
- **2.0.0**：计费功能改进。
- **1.7.0-2.0.2**：多次尝试集成支付功能。
- **1.0.0**：初始版本。

---

**由 ❤️ 小赚 制作**