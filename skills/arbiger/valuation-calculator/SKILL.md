---
name: valuation-calculator
description: 快速股票估值计算器——通过简单的命令计算PEG比率、EV/EBITDA比率、40法则、DCF模型等财务指标。该工具的灵感来源于YouTube上的教程以及Day1Global Tech的“技术收益深度分析”技能课程。
---
# 估值计算器

这是一个快速的股票估值工具，可即时提供市场估值指标。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `value <股票代码>` | 单只股票的完整估值 |
| `value peg <股票代码>` | PEG比率 + 预期市盈率/过去市盈率 + 预期增长率 |
| `value ev <股票代码>` | 企业价值/息税折旧摊销前利润（EV/EBITDA） + 40法则 |
| `value dcf <股票代码>` | 净现值（DCF）估值（使用默认参数） |
| `value dcf <股票代码> --auto` | 使用**自动计算的加权平均资本成本（WACC）**进行DCF估值（CAPM模型） |
| `value dcf <股票代码> --wacc=0.10 --growth=0.15 --terminal=0.03` | 自定义DCF参数 |
| `value` | 所有持仓的估值（从`holdings.md`文件中读取） |
| `value --index` | 三大指数（SPY、QQQ、DIA） |

## 输出指标

- **PEG比率** = 预期市盈率 ÷ 收益增长率 |
- **预期市盈率** = 基于未来12个月的预期收益 |
- **过去市盈率** = 基于过去12个月的实际收益 |
- **预期收益增长率** = （过去市盈率 ÷ 预期市盈率 - 1）× 100% |
- **EV/EBITDA** = 企业价值 ÷ 息税折旧摊销前利润 |
- **40法则** = 收入增长率百分比 + 利润率百分比 |
- **DCF** = 折现现金流估值

## DCF参数

| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `--auto` | 使用CAPM模型自动计算WACC | - |
| `--wacc=0.10` | 加权平均资本成本 | 10% |
| `--growth=0.15` | 未来增长率 | 5% |
| `--terminal=0.03` | 终值增长率 | 2.5% |

### 自动计算WACC（CAPM模型）

WACC = 无风险利率（Rf）+ β × （市场回报率（Rm）- 无风险利率（Rf）

- **Rf** = 10年期国债收益率（自动从Yahoo Finance获取） |
- **β** = 股票的贝塔系数（来自Yahoo Finance） |
- **Rm - Rf** = 市场风险溢价（5.5%）

## 持仓文件

默认从`~/.openclaw/workspace/holdings.md`文件中读取持仓信息。

## 数据来源

Yahoo Finance API（yfinance）

## 使用示例

```
value NVDA          # Full valuation
value peg NVDA      # PEG only
value ev NVDA       # EV/EBITDA + Rule of 40
value dcf NVDA     # DCF (default params)
value dcf NVDA --auto  # DCF with auto-WACC
value dcf NVDA --wacc=0.08 --growth=0.15 --terminal=0.03  # Custom
value               # All holdings dashboard
value --index       # Major indices
```

## 评估标准

| PEG比率 | 评级 |
|-----|--------|
| < 0.5 | 🔥 严重低估 |
| 0.5 - 1.0 | 👍 低估 |
| 1.0 - 1.5 | ✅ 公平价值 |
| > 1.5 | ⚠️ 高估 |

| 40法则 | 评级 |
|------------|--------|
| >= 40% | ✅ 合格 |
| < 40% | ⚠️ 不合格 |

| DCF增长潜力 | 评级 |
|------------|--------|
| > 20% | ✅ 低估 |
| -20% ~ 20% | ⚠️ 公平价值 |
| < -20% | ❌ 高估 |

---

**灵感来源：**
- YouTube: [布萊恩稳赚 - 股票估值筛选](https://youtu.be/gVWvhIAtGDE)
- Day1Global Tech Earnings Deepdive Skill