---
name: totoxu-montecarlo
description: >
  **Monte Carlo Crypto Trading Core**  
  该工具通过模拟数千条未来的价格路径（基于几何布朗运动模型），来评估交易策略的获胜概率、破产风险以及止损策略的实际效果。
version: 1.0.0
author: totoxu
requires:
  binaries:
    - python3
  env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
metadata:
  clawdbot:
    requires:
      env: ["SKILL_BILLING_API_KEY", "SKILL_ID"]
    files:
      - "scripts/*"
---
# 蒙特卡洛加密核心（Monte Carlo Crypto Core）

该技能允许您执行复杂的蒙特卡洛模拟，以评估交易策略的效果。它可以帮助您回答诸如以下问题：“如果我以70,000美元的价格买入比特币，假设日波动率为5%，并设置止损价为65,000美元，那么在30天内被强制平仓的概率是多少？”

## 设置环境  
1. 安装`requests`库：`pip install requests`  
2. 设置`SKILLPAY_API_KEY`环境变量，该变量应包含技能所有者的SkillPay API密钥。  

## 计费（每次调用费用为0.001美元，通过SkillPay支付）  
此技能为付费服务。**每次**模拟调用都需要提供`--user USER_ID`参数。如果调用失败并生成了`payment_url`，您必须将该链接展示给用户。  

---

## 工具：运行蒙特卡洛模拟  
**命令：**  
```bash  
python scripts/montecarlo.py --user USER_ID --price 70000 --vol 0.04 --drift 0.001 --days 30 --paths 5000 --stop-loss 65000 --position long  
```  

**必填参数：**  
- `--user`：用于计费的用户ID。  
- `--price`：资产的当前价格。  
- `--vol`：估计的日波动率（以小数形式表示，例如0.04表示4%）。您可以根据历史数据的标准差来计算该值。  

**可选参数：**  
- `--drift`：预期的日回报率。默认值为0.0。正的漂移率有利于多头策略，负的漂移率有利于空头策略。  
- `--days`：模拟未来的天数。默认值为30天。  
- `--paths`：要运行的模拟路径数量。路径数量越多，模拟结果越准确，但计算速度越慢。最大值为20,000，默认值为10,000。  
- `--position`：`long`或`short`，表示交易方向。默认值为`long`（多头）。  
- `--stop-loss`：触发止损的价格水平。  
- `--take-profit`：实现盈利时平仓的价格水平。  

**输出结果：**  
返回一个JSON对象，其中包含预期价格、最差/最佳情况的5%和95%概率，以及风险指标（如触发止损的概率`hit_stop_loss_pct`和整体盈利概率）。  

请使用这些概率来向用户解释您的交易建议。除非用户明确同意承担较高风险，否则不要推荐盈利概率低于50%的交易。