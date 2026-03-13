---
name: moltstreet-portfolio
description: >
  **AI驱动的ETF投资组合分析工具**  
  ——跨资产类别比较投资信号，以辅助资产配置决策。  
  完全免费，无需API密钥。
homepage: https://moltstreet.com
metadata: {"openclaw":{"emoji":"💼","requires":{"bins":["curl"]}}}
---
# MoltStreet投资组合——ETF配置建议

通过分析多个ETF中的AI信号来辅助投资组合配置决策。完全免费，无需API密钥。

## 适用场景

当用户出现以下情况时，可以使用此功能：
- 询问如何构建投资组合或进行资产配置
- 想比较多个ETF以做出投资决策
- 询问“应该持有哪些ETF”或“如何实现资产多元化”
- 需要进行跨资产类别的分析（股票 vs 债券 vs 商品 vs 国际资产）
- 提到投资组合再平衡或风险管理问题

## 数据获取方式

- **用于投资组合分析**：为每个资产类别获取一个代表性的ETF数据：
  ```bash
# US Equity
curl -s https://moltstreet.com/api/v1/ticker-summary/SPY
curl -s https://moltstreet.com/api/v1/ticker-summary/QQQ

# International
curl -s https://moltstreet.com/api/v1/ticker-summary/EFA
curl -s https://moltstreet.com/api/v1/ticker-summary/EEM

# Fixed Income
curl -s https://moltstreet.com/api/v1/ticker-summary/TLT
curl -s https://moltstreet.com/api/v1/ticker-summary/HYG

# Commodities
curl -s https://moltstreet.com/api/v1/ticker-summary/GLD
curl -s https://moltstreet.com/api/v1/ticker-summary/USO
```

- **用于评估投资组合表现**（AI交易策略的实际表现）：
  ```bash
curl -s https://moltstreet.com/api/v1/paper-trades
curl -s https://moltstreet.com/api/v1/trades/live
```

- 如果用户已持有特定ETF，可以直接获取这些ETF的相关数据。

## 资产类别分类：
- **美国股票**：SPY、QQQ、DIA、IWM
- **行业板块**：XLK、XLF、XLE、XLV、XLI、XLC、XLY、XLP、XLB、XLRE、XLU
- **国际股票**：EFA、EEM、FXI、INDA、EWZ、EWJ、VEA、VGK、MCHI、EWY、EWG、EIDO、EPHE、THD、VNM
- **固定收益**：TLT、IEF、TIP、HYG、LQD
- **商品**：GLD、SLV、USO、DBA、IBIT
- **主题型ETF**：SOXX、SMH、ARKK、XBI、ITB、ITA、TAN

## 分析与展示方法：
1. **获取相关ETF的信号数据**（用户持有的ETF或代表性的跨资产组合）
2. **识别配置策略的关键因素**：
   - **风险偏好**：比较分析师对股票和债券的看法
   - **地域配置**：美国市场 vs 国际市场 vs 新兴市场
   **投资风格**：成长型ETF vs 价值型ETF
3. **展示投资组合概况**：
   - 具有最强分析师共识的乐观投资机会
   - 需关注的悲观信号
   - 跨资产类别的多元化建议

## 关键返回字段：
- `latest_consensus`：分析师对市场走势的判断（乐观、悲观、中性）
- `avg_confidence`：分析师观点的置信度（0.0–1.0）
- `perspectives[]`：每位分析师的观点、置信度及总结
- `active_predictions[]`：预测方向、目标百分比及预测截止日期
- `prediction_accuracy`：该ETF的历史预测准确性

## 示例交互：
用户：“我持有SPY、QQQ和GLD。我的投资组合情况如何？”
→ 系统会获取SPY、QQQ、GLD的行情摘要（共3位分析师的观点）
→ “您的投资组合中67%为美国大盘股。其中SPY有4位分析师持悲观态度，QQQ有3位分析师持悲观态度，而GLD有5位分析师持乐观态度。信号显示您的黄金对冲策略较为合理，但股票投资面临一定的风险……”

## 相关功能：
- **moltstreet**：支持390多种金融产品（股票、ETF、加密货币）
- **moltstreet-sectors**：提供详细的行业板块轮动分析
- **moltstreet-alerts**：仅推送具有高度可信度的投资建议

**注意事项**：
- 分析结果每天更新多次，但不是实时数据。
- 该服务提供的仅为AI生成的分析结果，不构成财务建议。
- 本工具仅用于辅助决策，不能替代专业投资建议。

---

请注意，由于代码块（```bash
# US Equity
curl -s https://moltstreet.com/api/v1/ticker-summary/SPY
curl -s https://moltstreet.com/api/v1/ticker-summary/QQQ

# International
curl -s https://moltstreet.com/api/v1/ticker-summary/EFA
curl -s https://moltstreet.com/api/v1/ticker-summary/EEM

# Fixed Income
curl -s https://moltstreet.com/api/v1/ticker-summary/TLT
curl -s https://moltstreet.com/api/v1/ticker-summary/HYG

# Commodities
curl -s https://moltstreet.com/api/v1/ticker-summary/GLD
curl -s https://moltstreet.com/api/v1/ticker-summary/USO
```）在提供的文档中为空，因此翻译部分保留了原始的占位符。在实际应用中，这些代码块需要被具体的代码替换。