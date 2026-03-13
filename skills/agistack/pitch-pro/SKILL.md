---
name: pitch-pro
description: 为创始人及销售人员提供演讲技巧开发与培训服务。适用于涉及投资者推介、销售演示、简短演讲（如“电梯演讲”）、演讲材料制作或说服性沟通的场景。服务内容包括：构建价值主张、针对不同受众定制演讲内容、准备应对潜在异议的策略，以及提升演讲表达能力。所有服务均属于咨询服务，所有决策均需基于专业人员的判断进行。
---
# Pitch

Pitch开发系统：从基础原理到促成交易的全过程。

## 高度重视隐私与安全

### 数据存储（至关重要）
- **所有商业计划书或策略相关资料仅存储在本地**：`memory/pitch/`
- **禁止对外分享任何商业计划书或策略信息**
- **不与演示文稿或电子邮件系统集成**
- 用户可完全控制数据的保留和删除

### 安全原则（不可妥协）
- ✅ 构建有吸引力的价值主张和演讲内容
- ✅ 生成应对常见问题的策略
- ✅ 起草后续沟通方案
- ✅ 提供演讲技巧指导
- ❌ **绝不保证**一定能获得融资或达成销售
- ❌ **绝不替用户做出商业决策**
- ❌ **绝不替代人类在交易中的判断力**
- ❌ **绝不泄露任何机密的商业信息**

## 快速入门

### 数据存储设置
Pitch相关资料存储在您的本地工作区中：
- `memory/pitch/pitches.json` – 保存Pitch的不同版本及其内容
- `memory/pitch/audiences.json` – 保存目标受众信息
- `memory/pitch/objections.json` – 保存常见反对意见及应对策略
- `memory/pitch/meetings.json` – 保存会议记录和讨论结果

请使用`scripts/`目录中的脚本进行所有数据操作。

## 核心工作流程

### 建立基础
```
User: "Help me build my pitch foundation"
→ Use scripts/build_foundation.py --company "MyCo" --problem "X" --solution "Y"
→ Generate core value proposition and key messages
```

### 创建简短 pitches（30秒/60秒/120秒）
```
User: "Create a 60-second pitch for investors"
→ Use scripts/create_elevator_pitch.py --audience investor --length 60
→ Generate concise pitch tailored to audience
```

### 准备应对反对意见
```
User: "What questions will investors ask?"
→ Use scripts/prep_objections.py --audience investor --stage seed
→ Generate likely questions and recommended responses
```

### 起草后续沟通内容
```
User: "Draft follow-up email after the pitch"
→ Use scripts/draft_followup.py --meeting-id "MEET-123" --tone professional
→ Generate personalized follow-up for review
```

### 练习演讲技巧
```
User: "Coach me on my pitch delivery"
→ Use scripts/coach_delivery.py --pitch-id "PITCH-456"
→ Provide feedback on structure, clarity, and persuasion
```

## 模块参考

如需详细实现指南，请参阅：
- **基础构建**：[references/foundation.md](references/foundation.md)
- **简短 pitches**：[references/elevator-pitches.md](references/elevator-pitches.md)
- **反对意见处理**：[references/objections.md](references/objections.md)
- **目标受众分析**：[references/audiences.md](references/audiences.md)
- **后续沟通策略**：[references/follow-up.md](references/follow-up.md)
- **演讲技巧指导**：[references/delivery.md](references/delivery.md)

## 脚本参考

| 脚本 | 用途 |
|--------|---------|
| `build_foundation.py` | 构建Pitch的核心要素 |
| `create_elevator_pitch.py` | 生成30秒/60秒/120秒的简短Pitch |
| `prep_objections.py` | 准备应对可能出现的疑问 |
| `draft_followup.py` | 起草会议后续沟通内容 |
| `coach_delivery.py` | 提供演讲技巧反馈 |
| `save_meeting_notes.py` | 记录会议讨论结果 |
| `generate_deck_outline.py` | 设计Pitch演示文稿的结构 |
| `analyze_pitch.py` | 分析Pitch中的不足之处 |

## 免责声明

本工具仅提供Pitch辅导和准备支持。融资或销售的最终成功取决于多种因素，而不仅仅是Pitch的质量。我们不对任何结果作出任何保证。