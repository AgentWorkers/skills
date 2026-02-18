---
name: creative-ops-copilot
description: Turn messy client briefs into a production-ready plan for motion design/VFX projects: scope, assumptions/exclusions, deliverables matrix, schedule/milestones, review rounds, and estimate/quote. Also generate an invoice draft payload for Chris's local invoicing system (invoicing_system_2025) or export quote/invoice JSON/CSV/Markdown. Use when Chris asks to go from brief/email notes/chat logs into a clear plan + quote/invoice, or to create a repeatable project folder + docs.
---

# Creative Ops Copilot

## 操作步骤

1) 获取输入需求：
- 直接粘贴需求文本，或提供需求文件的路径（以文本、电子邮件或聊天记录的形式）。

2) 生成以下输出文件（必须生成）：
- `docs/creative-ops/plan.md`（适用于客户的文档）
- `docs/creative-ops/estimate.json`（结构化的任务清单）
- `docs/creative-ops/invoice-draft.json`（可用于后续的API导入）

3) 如果Chris有要求，还需执行以下操作：
- 创建一个适合AE/C4D/Octane项目的文件夹结构，并在其中添加`docs/README.md`文件。
- 将发票草稿发送到本地开票API（仅当基础URL已配置且Chris明确指示“发送”时执行）。

## 标准输出文件结构（plan.md）

- 项目概述（一段文字）
- 目标/成功标准
- 交付物（以表格形式列出）
  - 格式、时长、宽高比、版本、音频交付物
- 工作流程假设
  - 包含的内容、不包含的内容、审核轮次
- 未解决的问题（仍需解答的问题）
- 制作计划
  - 各阶段、里程碑、审核时间窗口
- 风险/依赖项
- 估算
  - 任务清单、所需工时、单价、小计、应急费用
- 下一步行动

## 可靠的生成方法

建议先生成结构化数据，再将其渲染为最终文档：

1) 提取关键信息：
- 客户名称
- 项目名称
- 截止日期/时间限制
- 交付物清单
- 限制条件（品牌要求、法律合规性、素材供应、审批流程）

2) 确定制作方式：
- 使用模板还是定制方案
- 选择2D AE、3D C4D还是混合制作方式

3) 根据项目需求进行成本估算：
- 考虑动画/视觉特效的复杂度
- 包括前期准备（需求分析、风格框架设计）、制作过程（动画制作、3D建模）、音频/音乐处理（如适用）、最终渲染及版本控制

## 推荐使用的脚本

使用提供的脚本来生成一致的输出文件：

```powershell
python skills/creative-ops-copilot/scripts/creative_ops_copilot.py --brief "<paste brief>" --out .
```

如果需求文件是以文件形式提供的：

```powershell
python skills/creative-ops-copilot/scripts/creative_ops_copilot.py --brief-file "C:\path\to\brief.txt" --out .
```

如需创建项目文件夹结构：

```powershell
python skills/creative-ops-copilot/scripts/creative_ops_copilot.py --brief "..." --out . --skeleton
```

如需将发票草稿发送到本地开票API（仅当配置完成后执行）：

```powershell
python skills/creative-ops-copilot/scripts/creative_ops_copilot.py --brief "..." --out . --push-invoice
```

## 配置文件

可选的配置文件：
- `skills/creative-ops-copilot/references/config.example.json`

请将其复制到：
- `skills/creative-ops-copilot/references/config.json`

然后编辑文件中的以下内容：
- `invoicingApi.baseUrl`
- `invoicingApi.apiKey`（如需要）
- `rateCard`（默认值）

## 注意事项

- 保持输出文件简洁、清晰，并符合客户的需求。
- 如果有任何信息缺失或不明确，请在“未解决的问题”部分列出，切勿自行猜测。