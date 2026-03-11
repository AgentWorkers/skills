---
name: consulting
description: 咨询实践管理包括项目范围的界定、提案撰写、定价策略的制定以及客户关系管理。当用户提及咨询项目、提案、定价、客户关系或交付成果时，这些内容尤为相关。该管理方法有助于明确实际问题的范围，撰写有竞争力的提案，根据项目价值制定合理的定价方案，有条理地呈现分析结果，并妥善处理复杂的客户情况。然而，它绝不能替代咨询师的判断力或独立性。
---
# 咨询服务

我们的咨询实践系统致力于通过实际行动带来实质性的改变。

## 关键隐私与安全措施

### 数据存储（至关重要）
- **所有客户数据仅存储在本地**：`memory/consulting/`
- **严格保护客户隐私**——不同项目之间绝不共享任何数据
- **不使用任何外部客户关系管理（CRM）系统**  
- **不将客户信息存储在云端**  
- 客户可完全控制数据的保留和删除

### 安全准则
- ✅ 明确咨询服务的范围并识别实际问题  
- ✅ 撰写提案并规划交付成果  
- ✅ 协助制定定价策略并引导价值讨论  
- ✅ 应对客户的复杂情况  
- ❌ **绝不能**替代咨询师的判断或独立性  
- ❌ **绝不能**替客户做出决策  
- ❌ **绝不能**在不同项目中泄露客户信息  

### 专业提示  
咨询服务的价值源于咨询师的独立性和专业判断。虽然这些工具能辅助您的工作，但所有专业意见、决策以及与客户的关系都完全属于您。

### 数据结构  
咨询相关数据存储在本地：
- `memory/consulting/engagements.json`：当前及过去的咨询项目  
- `memory/consulting/proposals.json`：提案模板及历史记录  
- `memory/consulting/deliverables.json`：交付成果的结构  
- `memory/consulting/pricing.json`：定价策略及参考数据  
- `memory/consulting/relationships.json`：客户关系记录  

## 核心工作流程

### 明确咨询项目范围  
```
User: "Help me scope this new client engagement"
→ Use scripts/scope_engagement.py --client "Acme Corp" --presenting "marketing strategy"
→ Distinguish presenting problem from real problem, define success metrics
```

### 撰写提案  
```
User: "Write a proposal for the operations project"
→ Use scripts/write_proposal.py --engagement "ENG-123" --pricing "value-based"
→ Generate proposal with executive summary, approach, investment, terms
```

### 制定定价策略  
```
User: "How should I price this engagement?"
→ Use scripts/structure_pricing.py --type "project" --value "$500K savings"
→ Recommend pricing model and anchor points
```

### 规划交付成果  
```
User: "Structure my findings for maximum impact"
→ Use scripts/structure_findings.py --audience "C-suite" --type "recommendation"
→ Build deliverable: recommendation first, supporting evidence, implementation
```

### 应对复杂情况  
```
User: "Client is not implementing what we agreed"
→ Use scripts/navigate_situation.py --type "implementation-gap" --engagement "ENG-123"
→ Prepare conversation that holds client accountable without damaging relationship
```

## 相关参考资料  
- **项目范围界定**：参见 [references/scoping.md](references/scoping.md)  
- **提案撰写**：参见 [references/proposals.md](references/proposals.md)  
- **定价策略**：参见 [references/pricing.md](references/pricing.md)  
- **交付成果结构**：参见 [references/deliverables.md](references/deliverables.md)  
- **客户关系管理**：参见 [references/relationships.md](references/relationships.md)  
- **复杂沟通技巧**：参见 [references/difficult-conversations.md](references/difficult-conversations.md)  
- **客户推荐机制**：参见 [references/referrals.md](references/referrals.md)  

## 脚本参考  
| 脚本 | 用途 |  
|--------|---------|  
| `scope_engagement.py` | 明确新项目的范围 |  
| `write_proposal.py` | 撰写客户提案 |  
| `structure_pricing.py` | 设计定价策略 |  
| `structure_findings.py` | 规划交付成果的结构 |  
| `navigate_situation.py` | 应对客户的复杂需求 |  
| `log_engagement.py` | 记录项目详细信息 |  
| `track_deliverable.py` | 跟踪交付进度 |  
| `generate_questions.py` | 生成调研问题 |