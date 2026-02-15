---
name: dvsa-tc-audit-readiness-operator-licence-uk
description: 生成DVSA/交通委员会要求的“展示给我”（“show me”）审计准备检查清单和证据索引。适用于准备审计或运营商许可证审查时使用。
---

# DVSA与交通委员会审计准备（英国）

## 目的  
生成用于展示审计准备情况的材料：当天的检查清单、证据索引以及与运营商执照要求及审计期望相对应的差距清单。  

## 使用场景  
- “为我准备DVSA审计所需的材料，并提供当天的检查清单。”  
- “为[客户]创建审计响应包，并列出存在的差距。”  
- “编制运营商执照合规性的证据索引。”  
- “今天我们应该准备好哪些材料来展示给审计员？”  

## 不适用场景  
- 仅涉及一般性合规性咨询，无需任何具体文件的场景。  
- 与运营/客户服务相关的请求（如路线规划、定价、绩效评估等），而非合规性相关的请求。  

## 输入内容  
- **必填项**：  
  - 审计背景（DVSA审计、交通委员会调查或客户审计的准备工作）及具体日期  
  - 审计范围：涉及的仓库/运营中心/车队，以及时间范围（例如过去28天/90天）  
- **可选项**：  
  - 企业内部的操作流程/政策文件（请粘贴文本）及文件保留规则  
  - 之前的审计发现及处理措施  
- **示例**：  
  - “今天DVSA将前往X仓库进行审计；需要当天的检查清单和证据索引。”  

## 输出文件  
- `dvsa-visit-today-checklist.md`  
- `audit-evidence-index.md`（适用于Excel的表格格式）  
- `gaps-register.md`  

## 成功标准  
- 所列内容均为实际可核查的项目  
- 提供明确的文件查找路径  
- 突出显示与运营商执照要求相关的关键事项（避免超出政策范围的法律解释）  

## 工作流程  
1. 确认审计类型和范围。  
   - 如果信息缺失，请**立即询问用户**相关细节。  
2. 使用`assets/dvsa-visit-today-checklist-template.md`生成当天的检查清单。  
3. 使用`assets/audit-evidence-index-template.md`编制证据索引（包括文件内容、存储位置、负责人及更新时间）。  
4. 识别潜在的差距：  
   - 将未知内容标记为“差距——需确认来源及负责人”。  
   - 通过`assets/gaps-register-template.md`生成差距清单。  
5. 关于运营商执照的要求：  
   - 添加一个简短的部分，引用`references/operator-licence-sensitivity-placeholders.md`中的内容，并将其与企业内部政策对应起来。  
6. 如果用户需要对现有文件进行修改，请**事先征得同意**。  

## 输出格式  
```text
# dvsa-visit-today-checklist.md
Audit type:
Scope:
Date:

## Immediate readiness (today)
- …

## Documents to pull (and where)
- …

## People/process readiness (“show me”)
- …

## Known risks / sensitivities
- …
```  

## 安全性与特殊情况处理  
- 不要自行设定文件保留期限或法律义务；如有需要，请询问企业的内部政策文件。  
- 如果收到“这些内容是否合法？”的疑问，请立即要求提供相关的具体记录和所需的输出文件。  

## 示例  
- 输入：**“今天DVSA将进行审计”**  
- 输出：当天所需的检查清单、证据索引及差距清单，以便迅速采取行动。