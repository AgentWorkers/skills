---
name: claw-betting-ai
description: **AI驱动的博彩咨询服务**  
专为游戏平台设计，提供智能的投注建议、风险分析、资金管理以及针对各种游戏类型（如撞球、骰子游戏和赌场游戏）的策略优化服务。适用于开发自动化投注机器人或需要AI辅助的博彩策略指导的场景。
website: https://clawde.xyz
---

# CLAW 赌博智能顾问

这是一个为 Stake.com 等游戏平台提供的基于人工智能的赌博顾问系统。该系统能够根据历史数据分析、用户的风险承受能力以及经过验证的赌博策略，为用户提供智能化的投注建议。

**官方网站**: https://clawde.xyz

## 主要功能

- **智能投注建议**：通过人工智能分析，为用户提供最佳的投注金额和时机建议。
- **游戏趋势分析**：针对特定游戏（如“Crash”游戏），分析历史数据以预测其走势。
- **风险管理**：提供动态的止损和止盈建议。
- **资金保护**：采用凯利准则（Kelly Criterion）和平稳投注策略来保护用户的资金。
- **多策略支持**：支持 Martingale、Anti-Martingale、Fibonacci、D’Alembert 等多种投注策略。

## 快速入门

```bash
# Install the skill
clawhub install claw-betting-ai

# Configure your settings
cp config/default.json config/local.json
# Edit config/local.json with your preferences
```

## 支持的游戏类型

| 游戏类型 | 分析方法                |
|--------|----------------------|
| Crash   | 基于历史数据的走势分析及倍数模式预测 |
| Dice    | 概率优化及连赢/连输模式检测        |
| Limbo   | 目标倍数推荐              |
| Slide   | 图案识别及投注策略建议        |

## 包含的文件

```
claw-betting-ai/
├── SKILL.md              # This file
├── config/
│   └── default.json      # Default configuration
├── scripts/
│   ├── analyze.py        # Crash history analyzer
│   └── recommend.py      # Bet recommendation engine
└── examples/
    ├── basic-usage.md    # Getting started guide
    └── strategies.md     # Strategy documentation
```

## 配置设置

请参阅 `config/default.json` 文件以了解所有可配置的选项：

- `strategy`：投注策略（保守型/平衡型/激进型）
- `bankroll`：初始投注资金
- `baseBetPercent`：基础投注金额（占资金的比例）
- `stopLoss`：止损阈值
- `takeProfit`：止盈目标
- `maxBets`：每次会话的最大投注次数

## 核心投注策略

### 1. 保守型（低风险）
- 目标倍数：1.5 倍至 2 倍
- 胜率：约 50%-65%
- 每次投注的最大资金占比：1%

### 2. 平衡型（中等风险）
- 目标倍数：2 倍至 5 倍
- 胜率：约 25%-45%
- 每次投注的最大资金占比：2%

### 3. 激进型（高风险）
- 目标倍数：5 倍至 20 倍
- 胜率：约 5%-15%
- 每次投注的最大资金占比：5%

## API 文档

请参阅 `examples/basic-usage.md` 以获取完整的 API 使用说明。

### 获取投注建议

```python
from scripts.recommend import get_recommendation

result = get_recommendation(
    bankroll=100,
    strategy="balanced",
    recent_history=[1.2, 3.5, 1.8, 2.1, 5.2]
)
# Returns: { shouldBet: true, amount: 2.0, target: 2.5, confidence: 72 }
```

## 安全功能

- **情绪识别**：当用户的投注行为显示出情绪化决策时发出警告。
- **会话限制**：设置时间限制和损失限制。
- **利润锁定**：自动保护部分盈利。
- **定期提醒**：定期提醒用户保持理性投注。

## 免责声明

本系统仅提供咨询建议。赌博存在亏损风险，请切勿超出您的承受能力进行投注。过去的数据模式并不能保证未来的结果。

## 链接

- 官方网站：https://clawde.xyz
- 技术支持：请通过官方网站联系我们。