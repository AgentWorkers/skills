---
name: insurance
description: 个人和商业保险管理功能，包括保单跟踪和理赔支持。当用户提及保险政策、审核保险范围、提交理赔申请、比较不同保险产品或了解保险覆盖的空白区域时，可使用该功能。系统可追踪所有保单、相关文件以及续保日期，并协助用户准备理赔流程。但请注意：该系统绝不提供保险咨询服务，也不会推荐具体的保险金额。
---
# 保险

本技能提供了保险组织系统的功能，帮助您了解自己的保险情况，并找到所需的保险产品。

## 高度重视隐私与安全

### 数据存储（至关重要）
- **所有保险数据仅存储在本地**：`memory/insurance/`
- **不使用任何外部API来处理保险数据**
- **不与保险公司系统建立连接**
- **本技能不提供任何保险产品的购买服务**
- 用户可以完全控制数据的保留和删除

### 安全原则（不可商榷）
- ✅ 跟踪保险单详情和保障范围
- ✅ 记录保险理赔信息
- ✅ 对比不同保险产品的保障内容
- ✅ 标记保险单的续期日期和保障缺口
- ❌ **绝不会提供关于保险需求的建议**
- ❌ **绝不会推荐具体的保险金额**
- ❌ **绝不会替代持证保险代理人**
- ❌ **绝不会协助进行保险产品的购买**

### 法律免责声明
保险决策应基于个人情况、所在司法管辖区以及具体的保险条款。本技能仅帮助您了解自己的保险保障情况并识别潜在的保障缺口。对于重要的保险决策，请务必咨询持证保险代理人或经纪人。

## 快速入门

### 数据存储设置
保险记录存储在您的本地工作区中：
- `memory/insurance/policies.json` – 所有保险单详情
- `memory/insurance/claims.json` – 理赔历史和状态
- `memory/insurance/documents.json` – 保险单文件清单
- `memory/insurance/renewals.json` – 续期信息跟踪
- `memory/insurance/coverage_gaps.json` – 识别出的保障缺口

请使用 `scripts/` 目录中的脚本进行所有数据操作。

## 核心工作流程

### 添加保险单
```
User: "Add my home insurance policy"
→ Use scripts/add_policy.py --type home --carrier "State Farm" --premium 1200
→ Log policy details, coverage limits, deductibles
```

### 记录理赔
```
User: "I need to file an auto insurance claim"
→ Use scripts/log_claim.py --policy auto --incident "accident" --date 2024-03-01
→ Document incident, track claim status, prepare required info
```

### 查看保障内容
```
User: "Review my insurance coverage"
→ Use scripts/review_coverage.py
→ Show all policies, identify gaps, flag upcoming renewals
```

### 对比保险产品
```
User: "Compare these two health insurance plans"
→ Use scripts/compare_policies.py --policy1 planA --policy2 planB
→ Side-by-side comparison of coverage, costs, networks
```

### 检查续期情况
```
User: "Any insurance renewals coming up?"
→ Use scripts/check_renewals.py --days 60
→ Show policies renewing soon with premium changes
```

## 模块参考

有关详细实现信息，请参阅：
- **保险单管理**：[references/policy-management.md](references/policy-management.md)
- **健康保险**：[references/health-insurance.md](references/health-insurance.md)
- **家庭/租客保险**：[references/home-insurance.md](references/home-insurance.md)
- **汽车保险**：[references/auto-insurance.md](references/auto-insurance.md)
- **人寿保险**：[references/life-insurance.md](references/life-insurance.md)
- **理赔流程**：[references/claims.md](references/claims.md)
- **续期审核**：[references/renewals.md](references/renewals.md)

## 脚本参考

| 脚本 | 功能 |
|--------|---------|
| `add_policy.py` | 添加新的保险单 |
| `log_claim.py` | 记录和跟踪保险理赔 |
| `review_coverage.py` | 查看所有保障内容和缺口 |
| `compare_policies.py` | 对比两个保险产品的保障内容 |
| `check_renewals.py` | 检查即将到期的保险单 |
| `add_document.py` | 记录保险单文件 |
| `identify_gaps.py` | 识别潜在的保障缺口 |
| `generate_summary.py` | 生成保险组合概览 |

## 免责声明

本技能仅帮助您了解和整理自己的保险保障情况。对于保险决策或复杂的情况，请务必咨询持证保险代理人或经纪人。