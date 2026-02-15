---

> 相关技能：[[AGENTS]], [[skills/pai-redteam/Workflows/AdversarialValidation|对抗性验证]], [[skills/pai-redteam/Integration|集成]]

---
名称：RedTeam  
描述：使用32个代理进行对抗性分析。适用于红队分析、攻击策略制定、反驳意见生成及压力测试。详情请参阅 `SkillSearch('redteam')`。

---

## 自定义设置  

**在执行前，请检查用户自定义设置：**  
`~/.claude/skills/CORE/USER/SKILLCUSTOMIZATIONS/RedTeam/`  

如果该目录存在，请加载并应用其中的所有 `REFERENCES.md` 文件、配置文件或资源。这些设置会覆盖默认行为。如果目录不存在，则使用技能的默认设置。  

# RedTeam 技能  

该技能提供军事级别的对抗性分析服务，通过并行部署代理来执行分析。它将论点分解为基本组成部分，从32个专家的角度（工程师、架构师、渗透测试人员、实习生）进行攻击性评估，综合分析结果，并生成有力的反驳意见。  

## 语音通知  

**在执行工作流时，请同时执行以下操作：**  
1. **发送语音通知**：  
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow from the RedTeam skill"}' \
     > /dev/null 2>&1 &
   ```  
2. **输出文本通知**：  
   ```
   Running the **WorkflowName** workflow from the **RedTeam** skill...
   ```  
完整文档请参阅 `~/.claude/skills/CORE/SkillNotifications.md`。  

## 工作流路由  

根据请求将任务路由到相应的工作流。  
**在执行工作流时，请直接输出以下通知：**  
```
Running the **WorkflowName** workflow from the **RedTeam** skill...
```  

| 触发条件 | 对应工作流 |  
|---------|----------|  
| 红队分析（对现有内容进行压力测试） | `Workflows/ParallelAnalysis.md` |  
| 对抗性验证（通过竞争机制生成新内容） | `Workflows/AdversarialValidation.md` |  

---

## 快速参考  

| 工作流 | 功能 | 输出结果 |  
|---------|---------|--------|  
| **ParallelAnalysis** | 对现有内容进行压力测试 | 提供分析结果及反驳意见（各8分） |  
| **AdversarialValidation** | 通过竞争机制生成新内容 | 从多个提案中综合出最佳解决方案 |  

**五阶段分析流程（ParallelAnalysis）：**  
1. **分解**：将论点拆分为24个基本组成部分  
2. **并行分析**：32个代理分别评估各个方面的优缺点  
3. **综合分析**：找出共识性的观点  
4. **形成最强论点**：整理出最有力的论据版本  
5. **生成反驳意见**：提出最有力的反驳意见  

---

## 相关文档：  
- `Philosophy.md`：核心理念、成功标准及代理类型  
- `Integration.md`：技能集成方式、FirstPrinciples的使用方法及输出格式  

---

**示例：**  
- **攻击某个架构提案：**  
   ```
User: "red team this microservices migration plan"
--> Workflows/ParallelAnalysis.md
--> Returns steelman + devastating counter-argument (8 points each)
```  
- **从反对者的角度评估商业决策：**  
   ```
User: "poke holes in my plan to raise prices 20%"
--> Workflows/ParallelAnalysis.md
--> Surfaces the ONE core issue that could collapse the plan
```  
- **对内容进行对抗性验证：**  
   ```
User: "battle of bots - which approach is better for this feature?"
--> Workflows/AdversarialValidation.md
--> Synthesizes best solution from competing ideas
```  

---

**最后更新时间：** 2025-12-20