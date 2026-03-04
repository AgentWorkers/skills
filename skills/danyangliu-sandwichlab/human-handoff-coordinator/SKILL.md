---
name: human-handoff-coordinator
description: 将自动化处理的相关讨论升级至人工广告专家，以便处理 Meta（Facebook/Instagram）、Google Ads、TikTok Ads 和 YouTube Ads 的相关操作。
---
# 广告人工协助处理

## 目的
核心任务：
- 负责创建广告处理包（ad handling packets）以及处理问题的升级流程（escalation routing）。

此技能专为广告相关工作流程设计，应提供可执行的计划而非通用建议。

## 适用场景
当用户提出以下需求时，请使用此技能：
- 需要与业务成果相关的广告执行指导
- 需要制定涉及收入（revenue）、投资回报率（ROAS）、每次点击成本（CPA）或预算效率（budget efficiency）的增长策略
- 需要针对以下平台的操作建议：Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads
- 需要创建广告处理包或处理问题升级流程

**高频关键词**：
- 广告（ads）、广告活动（advertising）、广告活动（campaign）、增长（growth）、收入（revenue）、投资回报率（ROAS）、每次点击成本（CPA）、投资回报率（ROI）、预算（budget）、出价（bidding）、流量（traffic）、转化率（conversion）、销售漏斗（funnel）、Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads、DSP（Digital Sales Platform）

## 输入信息要求
- **问题**：用户遇到的问题或决策请求
- **背景信息**：相关账户、广告活动及目标信息
- **紧急程度**（ urgency_level）

**可选信息**：
- **错误信息**（error_message）
- **截图或日志**（screenshots_or_logs）
- **期望的回复方式**（preferred_response_style）

## 输出内容
1. **直接答案**（Direct Answer）
2. **根本原因假设**（Root Cause Hypothesis）
3. **立即可执行的操作**（Immediate Actions）
4. **问题升级标准**（Escalation Criteria）
5. **后续需要询问的问题**（Follow-up Questions）

## 工作流程
1. **问题类型分类**（Classify question type）：操作指南、问题诊断、政策咨询、策略制定
2. **首先提供最简洁有效的答案**（Provide shortest valid answer）
3. **根据背景信息提供具体操作清单**（Add context-aware action checklist）
4. **如果风险或不确定性较高，标记需要升级**（Flag escalation if risk or uncertainty is high）
5. **仅在必要时返回后续需要填写的字段**（Return follow-up fields only if required）

## 决策规则
- **如果答案的可靠性较低，说明不确定性并提出验证步骤**（If answer confidence is low, state uncertainty and propose verification steps）
- **如果问题可能影响广告支出安全，优先建议暂停或限制支出**（If issue impacts spend safety, prioritize pause or cap recommendations）
- **如果用户请求超出支持范围的操作，提供完整的背景信息并移交处理**（If user asks for unsupported action, hand off with exact context package）

## 平台注意事项
**主要适用平台**：Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads

**平台操作建议**：
- 建议根据具体平台制定个性化方案；不要将所有平台的建议合并为一个通用计划
- 对于Meta和TikTok Ads，优先考虑创意内容的测试频率
- 对于Google Ads和Amazon Ads，重点关注需求捕捉及广告展示意图的优化
- 对于DSP/程序化广告平台，重点关注受众控制及投放频率的管理

## 约束与注意事项
- **严禁伪造数据或政策结果**（Never fabricate metrics or policy outcomes）
- **区分观察到的事实与假设**（Separate observed facts from assumptions）
- **每项建议都应使用可量化的表述**（Use measurable language for each proposed action）
- **在存在支出风险的情况下，至少提供一种回退或止损方案**（Include at least one rollback or stop-loss condition）

## 故障处理与问题升级
- **如果关键信息缺失，仅要求提供最低限度的必要信息**（If critical inputs are missing, ask for only the minimum required fields）
- **如果平台存在限制，说明权衡方案并提供安全默认选项**（If platform constraints conflict, show trade-offs and a safe default）
- **如果答案的可靠性较低，明确标注并提供验证步骤**（If answer confidence is low, mark it explicitly and provide a validation checklist）
- **遇到高风险问题（如政策变更、计费问题或数据追踪异常）时，提供结构化的处理方案**（If high-risk issues appear, provide a structured handoff payload）

## **代码示例**
### 快速问题分类 JSON
```json
{
  "issue_type": "delivery_drop",
  "severity": "medium",
  "first_actions": ["check spend cap", "check policy status"]
}
```

### 广告处理包示例
```json
{
  "ticket_type": "platform_support",
  "required_fields": [account_id, campaign_id, timeline, last_change]
}
```

**示例说明**：
### 示例 1：广告投放突然中断
**输入**：
- 广告活动展示量下降了60%
- 最近没有进行过任何手动调整

**输出内容**：
- 可能的原因
- 需要检查的第一个操作：检查支出上限（check spend cap）
- 需要检查的第二个操作：检查政策状态（check policy status）
- 是否需要升级处理：是的（Yes, indicate if escalation is needed）

### 示例 2：广告被拒绝，原因不明确
**输入**：
- 广告被拒绝，但拒绝原因不明确
- 用户希望尽快解决问题

**输出内容**：
- 广告被拒绝的原因（Explanation for ad rejection）
- 重新提交广告的指导（Instructions for re-submitting the ad）
- 重新提交的顺序（Order for re-submission）

### 示例 3：需要立即获得人工支持
**输入**：
- 出现计费问题或账户被锁定
- 广告活动发布截止日期为今天

**输出内容**：
- 广告处理包（Ad handling package）
- 紧急程度（Urgency level）
- 需要联系的负责人（Required owner）
- 预计处理时间（ETA）

## 质量检查清单
- [ ] 所有必填字段均已填写且不为空
- [ ] 关键触发词至少包含3个专业术语
- **输入和输出内容均经过实际测试**（Input and output content are operationally testable）
- **工作流程和决策规则与具体功能相匹配**（Workflow and decision rules are capability-specific）
- **平台相关说明具体且详细**（Platform references are explicit and concrete）
- **包含至少3个实际操作示例**（At least 3 practical examples are included）