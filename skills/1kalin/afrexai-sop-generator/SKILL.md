# SOP生成器  
（SOP Generator: Creates Standard Operating Procedures from plain-language process descriptions.）  

## 使用方法  
（Usage:）  
只需描述任何业务流程，该工具即可生成结构化的标准操作程序（SOP）文档，内容包括：  
- 带有编号的逐步说明  
- 角色分配与职责  
- 决策点及升级路径  
- 质量检查点与验收标准  
- 每个步骤的时间预估  
- 常见故障模式及故障排除方法  

## 适用场景  
（When to Use:）  
- 首次记录团队流程时  
- 新员工入职时（需要明确操作流程）  
- 在不同地点或部门之间标准化操作  
- 为合规审计（如ISO、SOC2等）做准备  
- 将传统经验转化为可复制的系统  

## 操作步骤  
（Instructions:）  
当用户请求创建SOP或记录某个流程时，请按照以下步骤操作：  
1. 询问用户需要记录的具体流程（如未提供，请先明确）。  
2. 了解执行该流程的人员及其执行频率。  
3. 使用以下格式生成完整的SOP文档：  
   ```markdown
# SOP: [Process Name]
**Version:** 1.0 | **Owner:** [Role] | **Frequency:** [How often]
**Last Updated:** [Date]

## Purpose
[Why this process exists and what it achieves]

## Scope
[Who this applies to, when it applies]

## Prerequisites
- [What's needed before starting]

## Procedure

### Step 1: [Action]
**Responsible:** [Role]  
**Time:** [Estimate]  
- Detail 1
- Detail 2
- **Decision point:** If [condition], go to Step X

### Step 2: [Action]
...

## Quality Checks
- [ ] [Verification item]

## Failure Modes
| Issue | Cause | Resolution |
|-------|-------|------------|

## Revision History
| Date | Version | Changes | Author |
|------|---------|---------|--------|
```  

4. 根据流程的复杂性调整文档内容：简单流程对应简单的SOP；复杂流程则需要更详细的说明。  
5. 包含具体、可执行的细节，避免使用泛化的内容。  
6. 标出用户需要补充公司特定信息的部分。  

## 提示  
（Tips:）  
- 优先处理最繁琐或容易出错的流程。  
- 请实际执行该流程的人员审核SOP内容。  
- 每季度对SOP进行审查：过时的流程比没有流程更糟糕。  
- 对于复杂操作，可参考[AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)，其中包含10个行业的SOP模板和操作框架。