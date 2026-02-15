---
name: tachograph-infringement-triage-root-cause-uk
description: 对行车记录仪（tachograph）的使用违规行为进行分类处理，识别常见的违规模式，并生成“下一步需要检查的内容”提示以及每周的审查笔记。适用于每周进行的行车记录仪/违规行为审查（tacho/WTD reviews）。
---

# 计速器违规处理与根本原因分析（英国）

## 目的  
运行每周审查流程，将违规记录转化为清晰的分类提示、根本原因分析以及“下一步应检查的内容”。

## 使用场景  
- 对这些驾驶员进行每周的计速器违规情况及WTD（Work-Task-Decision）合规性审查。  
- 对这些违规行为进行分类处理，并告知下一步应检查的内容。  
- 将该PDF违规报告汇总为具体的行动方案和驾驶员后续需要处理的事项。  

**不适用场景**  
- 仅需要向驾驶员发送一条信息时（请使用“infringement coach”技能）。  
- 需要一般性的规则说明，但不需要相关记录时。  

## 输入内容  
- **必填项**：  
  - 驾驶员名单 + 时间范围  
  - 违规行为摘要（CSV/PDF格式或手动输入的违规记录）  
- **可选项**：  
  - 任何已知的运营背景信息（如行驶路线、延误情况、多站停靠、渡轮/火车运输、人员配置等）  
  - 之前的违规记录历史  

**示例输入**：  
- “驾驶员A–F，上周的违规记录已附上；需要生成每周的报告包。”  

## 输出内容  
- `weekly-tacho-wtd-review.md`（供管理者查看）  
- `triage-actions-by-driver.md`（按驾驶员分类的违规处理建议）  

**成功标准**：  
- 明确列出每种违规类型的“下一步检查内容”。  
- 标记出可能接近调查或纪律处分阈值的违规行为（根据公司政策）。  

## 工作流程  
1. 确认审查的时间范围和驾驶员名单。  
   - 如果信息缺失 → **立即停止并询问用户**。  
2. 将违规记录整理成按驾驶员分类的列表（仅包含事实信息）。  
3. 使用`references/common-infringement-patterns.md`文件进行模式匹配分析。  
4. 对每位驾驶员生成：  
  - 可能的根本原因分析提示（需要询问的问题及应进行的运营检查）。  
  - 根据`assets/what-to-check-next-playbook.md`文件，制定下一步的检查步骤。  
5. 使用`assets/weekly-review-pack-template.md`生成每周报告包。  
6. 如果违规行为的处理需要参考之前的违规记录，**立即停止并询问用户**以获取相关数据。  

## 输出格式  
```text
# triage-actions-by-driver.md
Period:
Sources:

## Driver [X]
Infringements (facts):
- …

What to check next:
- …

Root-cause prompts:
- …

Proposed follow-up:
- Coaching / monitoring / investigation trigger (per policy)
```  

## 安全性与特殊情况处理  
- 如果记录不完整（如某些日期缺失或下载数据有遗漏），应将其标记为风险或数据缺口，而非猜测原因。  
- 避免使用指责性语言，保持分类分析的中立性。  

**示例输出**：  
- 输入：**“对12名驾驶员进行每周审查”**  
- 输出：包含每周报告包以及每位驾驶员的违规处理建议和下一步检查内容。