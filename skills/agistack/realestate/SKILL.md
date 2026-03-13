---
name: realestate
description: >
  **房地产交易支持服务**  
  包括 affordability analysis（经济能力分析）、property evaluation（房产评估）以及 offer strategy（购房策略制定）。  
  适用于用户咨询购房、卖房、寻找房源、抵押贷款、房屋检查或租赁协议等相关事宜。  
  服务内容包括：  
  - 计算用户的实际购房能力；  
  - 系统性地评估房产价值；  
  - 制定购房策略；  
  - 审核相关合同；  
  - 跟踪交易进程中的关键节点。  
  **重要说明：**  
  本服务不提供任何投资建议。
---
# 房地产

房地产导航系统：智能购房，智能售房。

## 关键的隐私与安全问题

### 数据存储（至关重要）
- **所有房地产数据仅存储在本地**：`memory/realestate/`
- **不使用MLS（Multiple Listing Service）**或任何房源列表服务
- **不与抵押贷款机构建立连接**
- **本工具不用于提交任何文件**  
- 用户可完全控制数据的保留和删除

### 安全保障措施
- ✅ 计算包括所有费用在内的实际购房能力  
- ✅ 系统化地评估房产  
- ✅ 制定基于数据的报价策略  
- ✅ 审查租赁协议  
- ❌ **绝不提供投资建议**  
- ❌ **绝不保证房产价值**  
- ❌ **绝不替代持牌房地产经纪人**  
- ❌ **绝不替代房地产律师**

### 重要提示
房地产交易在法律上非常复杂且风险较高。本工具仅提供教育性支持。请始终根据所在地区的法规，与持牌房地产经纪人、抵押贷款专业人士及律师合作。

### 数据结构
房地产数据存储在本地：
- `memory/realestate/affordability.json` – 购房能力计算  
- `memory/realestate/properties.json` – 房产评估  
- `memory/realestate/offers.json` – 报价策略及历史记录  
- `memory/realestate/inspections.json` – 检查结果  
- `memory/realestate/contracts.json` – 合同审查笔记  
- `memory/realestate/transactions.json` – 交易跟踪记录

## 核心工作流程

### 计算购房能力  
```
User: "What can I actually afford?"
→ Use scripts/calculate_affordability.py --income 120000 --debts 800 --downpayment 60000
→ Calculate true monthly cost including taxes, insurance, maintenance
```

### 评估房产  
```
User: "Evaluate this house at 123 Main St"
→ Use scripts/evaluate_property.py --address "123 Main St" --price 650000
→ Generate systematic evaluation checklist
```

### 制定报价策略  
```
User: "Help me make an offer on the house I saw"
→ Use scripts/build_offer.py --property "PROP-123" --comps "COMP-1,COMP-2"
→ Analyze comparables, determine offer range, plan contingencies
```

### 准备房产检查  
```
User: "What should I look for during inspection?"
→ Use scripts/prep_inspection.py --property-type "single-family" --year 1985
→ Generate inspection checklist by property type and age
```

### 审查租赁协议  
```
User: "Review this lease agreement"
→ Use scripts/review_lease.py --file "lease.pdf"
→ Identify unusual clauses, flag potential issues
```

## 模块参考
- **购房能力分析**：请参阅 [references/affordability.md](references/affordability.md)  
- **房产评估**：请参阅 [references/evaluation.md](references/evaluation.md)  
- **报价策略**：请参阅 [references/offers.md](references/offers.md)  
- **检查指南**：请参阅 [references/inspection.md](references/inspection.md)  
- **销售策略**：请参阅 [references/selling.md](references/selling.md)  
- **租赁协议审查**：请参阅 [references/leases.md](references/leases.md)  
- **交易结算流程**：请参阅 [references/closing.md](references/closing.md)

## 脚本参考
| 脚本 | 用途 |
|--------|---------|
| `calculate_affordability.py` | 计算实际购房能力 |
| `evaluate_property.py` | 系统化评估房产 |
| `build_offer.py` | 制定报价策略 |
| `prep_inspection.py` | 准备房产检查 |
| `review_lease.py` | 审查租赁协议 |
| `track_transaction.py` | 跟踪交易进度 |
| `compare_properties.py` | 比较多套房产 |
| `analyze_market.py` | 分析当地市场数据 |