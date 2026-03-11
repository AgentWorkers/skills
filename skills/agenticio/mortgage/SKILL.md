---
name: mortgage
description: >
  **抵押贷款流程指南：包含负担能力计算与应用进度跟踪**  
  适用于用户咨询购房相关问题时（如抵押贷款利率、负担能力、首付款、抵押贷款申请或贷款机构比较）。本指南提供负担能力计算方法，解释不同类型的抵押贷款，协助用户准备申请材料，并跟踪贷款审批的各个关键节点。但请注意：本指南绝不提供抵押贷款方面的专业建议，也不推荐具体的贷款机构。
---
# 抵押贷款

这是一个抵押贷款导航系统，帮助用户从规划贷款到完成整个流程。

## 高度的隐私与安全保障

### 数据存储（至关重要）
- **所有抵押贷款数据仅存储在本地**：`memory/mortgage/`
- **不使用任何外部API来处理抵押贷款数据**
- **不与贷款机构系统连接**
- **不提供利率锁定服务，也不接收贷款申请**
- 用户可以完全控制数据的保留和删除

### 安全原则（不可妥协）
- ✅ 计算用户的贷款承受能力
- ✅ 解释不同类型的抵押贷款及其条款
- ✅ 准备贷款申请所需的文件清单
- ✅ 跟踪贷款申请的各个阶段
- ❌ **绝不提供抵押贷款建议或产品推荐**
- ❌ **绝不推荐特定的贷款机构**
- ❌ **绝不保证贷款申请一定会获得批准或提供具体的利率**
- ❌ **绝不替代持牌的抵押贷款经纪人**

### 法律免责声明
抵押贷款的决策涉及重大的财务承诺，需要根据个人情况、信用记录和市场状况来做出。本工具仅提供教育性和辅助性的服务。请始终与持牌的抵押贷款经纪人或财务顾问合作。

## 快速入门

### 数据存储设置
抵押贷款数据存储在您的本地工作空间中：
- `memory/mortgage/affordability.json` - 贷款承受能力计算结果
- `memory/mortgage/scenarios.json` - 不同贷款方案对比
- `memory/mortgage/documents.json` - 贷款申请所需文件
- `memory/mortgage/applications.json` - 贷款申请跟踪信息
- `memory/mortgage/lenders.json` - 贷款机构对比信息

请使用 `scripts/` 目录下的脚本来执行所有数据操作。

## 核心工作流程

### 计算贷款承受能力
```
User: "How much house can I afford on $100k salary?"
→ Use scripts/calculate_affordability.py --income 100000 --debts 500
→ Estimate affordable price range and monthly payment
```

### 比较不同类型的抵押贷款
```
User: "Should I get a fixed or ARM mortgage?"
→ Use scripts/compare_types.py --scenario "first-time buyer"
→ Explain options with pros/cons for situation
```

### 准备贷款申请文件
```
User: "What documents do I need for mortgage application?"
→ Use scripts/prep_documents.py --type "conventional" --employment "w2"
→ Generate complete document checklist
```

### 跟踪贷款申请进度
```
User: "Track my mortgage application"
→ Use scripts/track_application.py --application-id "APP-123"
→ Show current stage and next steps
```

### 比较不同贷款机构的报价
```
User: "Compare these two lender offers"
→ Use scripts/compare_lenders.py --lender1 "Bank A" --lender2 "Credit Union B"
→ Side-by-side comparison of rates, fees, terms
```

## 模块参考

如需详细实现指南，请参阅：
- **贷款承受能力计算**：[references/affordability.md](references/affordability.md)
- **抵押贷款类型**：[references/mortgage-types.md](references/mortgage-types.md)
- **文件准备**：[references/documents.md](references/documents.md)
- **贷款机构比较**：[references/lender-comparison.md](references/lender-comparison.md)
- **贷款申请跟踪**：[references/application-tracking.md](references/application-tracking.md)
- **贷款流程完成**：[references/closing.md](references/closing.md)

## 脚本参考

| 脚本          | 功能                |
|-----------------|----------------------|
| `calculate_affordability.py` | 计算购房的贷款承受能力       |
| `compare_types.py` | 比较不同类型的抵押贷款       |
| `prep_documents.py` | 生成贷款申请文件清单         |
| `track_application.py` | 跟踪贷款申请的状态           |
| `compare_lenders.py` | 比较不同贷款机构的报价         |
| `calculate_payment.py` | 计算每月还款金额           |
| `estimate_closing_costs.py` | 估算贷款手续费用           |
| `set_reminder.py` | 设置利率锁定的提醒           |

## 免责声明

本工具仅提供教育性和辅助性的服务。抵押贷款的决策应基于个人情况、信用记录和市场状况。请务必咨询持牌的抵押贷款经纪人或财务顾问。