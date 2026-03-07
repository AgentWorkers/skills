---
name: re-master
description: Manage off-plan real estate investments, payment milestones, group buy allocations, and ROI simulations. Use when a user needs to: (1) Track property installments (Dubai 60/40, 70/30 plans), (2) Calculate proportional ownership between investors (Binkl/Dad/Friends), (3) Manage a cash buffer pool for admin payments, (4) Generate unique sharing links for investors, (5) Simulate ROI or payment gap scenarios.
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["python3"]
      }
    }
  }
---

# 房地产管理大师（期房跟踪工具）🏙️

该工具能够实现对期房投资的精准管理和模拟，尤其适用于由管理员管理的现金池进行的团购场景。

## 核心工作流程

### 1. 项目初始化
当用户添加新的房产单元（例如：Rotana、Ohana）时：
1. **定义价格和费用：**通常为4%的首付款加上注册费。
2. **定义付款计划：**例如：10%的首付款 + 每月1%的付款，或每6个月支付10%。
3. **设立缓冲资金：**确定初始的现金池金额（例如：48万阿联酋迪拉姆）。

### 2. 团购分配
根据以下因素计算各投资者的权益：
- **初始首付款贡献：**每位投资者在项目开始时缴纳的金额。
- **每月的付款承诺：**投资者每月需支付的金额。
- **权重时间：**随着付款的进行，各投资者的所有权比例会动态调整。

可以使用 `scripts/equity_calc.py` 进行简单的计算，或使用 `scripts/re_sim.py` 进行多个月的模拟。

### 3. 缓冲资金与里程碑模拟
“管理员现金池”策略：
- 使用现金池来弥补资金缺口或满足早期里程碑的要求。
- 模拟投资者的“公平份额”请求，以确保现金池金额始终高于安全阈值（例如：超过25万阿联酋迪拉姆）。

运行 `python3 scripts/re_sim.py <config.json>` 以生成完整的资金预测报告。

### 4. 分享URL（开发者说明）
`re-master` 工具提供了可供每位投资者查看的数据。要生成URL：
- **本地访问：**如果使用原始的Deal Tracker服务器，可以使用 `dash/<token>` 路由。
- **静态报告：**可以使用模拟结果为参与者生成静态报告。

该工具本身不运行Web服务器，但它提供了实现Web服务器所需的功能逻辑。

## 参考资料
- **迪拜标准：**有关税收、费用和托管的相关信息，请参阅 [references/dubai_standards.md](references/dubai_standards.md)。
- **权益计算公式：**有关团购中使用的“加权贡献”计算逻辑，请参阅 [references/equity_formulas.md](references/equity_formulas.md)。

## 脚本
- `scripts/re_sim.py`：全面的多单元模拟引擎。输入单元/账户配置 → 输出每月的里程碑资金明细。
- `scripts/equity_calc.py`：简单的权益计算工具。

---
*由Binkl创建 👑 — 2026-03-06*