---
name: agent-superpowers
version: 1.1.0
description: "你的代理发出了“完成”的提示——但它真的检查过吗？“Superpowers”这一机制将任何OpenClaw代理都转变为一个严谨、自律的工程师。其核心原则包括：  
1. **验证铁律**（主张之前必须先有证据）；  
2. **三代理代码审查流程**（构建 → 验证规范 → 验证质量）；  
3. **系统化的调试方法**（四阶段问题定位机制、三次尝试规则）；  
4. **设计优先于编码的流程**；  
5. **防止过度设计的规则**。  
适用场景包括：  
1. 执行任何复杂度的编码任务；  
2. 调试程序中的错误；  
3. 在声称工作完成之前；  
4. 创建子代理时；  
5. 规划新功能时；  
6. 审查代码时。  
该机制的灵感来源于顶尖的编码实践方法，并针对OpenClaw的多代理架构进行了优化。"
metadata:
  openclaw:
    emoji: "⚡"
    notes:
      security: "No network calls, no credentials accessed. Pure methodology — SKILL.md + reference Markdown files only."
---
# 代理的超能力  
（Agent Superpowers）  

这是一套针对AI代理的完整开发方法论，它将一个通用的代理转变为一个有纪律的“工程师”：在构建之前先进行规划，在提交之前进行验证，并系统地进行调试。  

## 快速入门 —— 将其集成到你的代理中  
（Quick Start — Integrate it into your agent）  
将以下内容添加到你的`AGENTS.md`文件中，以激活始终生效的行为规则：  
```markdown
## Engineering Discipline (Agent Superpowers)

### Verification Iron Law
- NO completion claims without fresh verification evidence in this message.
- Run the command. Read the output. THEN claim the result.
- "Should work" / "looks correct" / "done" without evidence = unverified.

### Anti-Over-Engineering
- Do what was asked. Nothing more, nothing less.
- Three similar lines > premature abstraction.
- Don't add features, refactor, or "improve" beyond the request.
- A bug fix doesn't need surrounding code cleaned up.

### Reversibility
- Local/reversible (edit files, run tests) → proceed freely.
- Hard-to-reverse/shared/destructive → confirm first.
- Approval is scoped, not global. Once ≠ always.

### Three-Strike Debugging
- If 3 fixes fail on the same problem → STOP.
- Question the architecture. Don't attempt fix #4 without discussing.

### Brainstorming Gate
- Before any feature/component/creative work: explore → ask → propose → approve → THEN build.
- "Simple" projects are where unexamined assumptions waste the most work.
```  

## 开发流程  
（The Development Pipeline）  
每一个非简单的编码任务都遵循以下流程：  
```
brainstorming → plan → implement → spec-review → quality-review → verify → complete
```  
每个阶段都设有质量检查关卡；跳过这些关卡会花费比遵循它们更多的时间。  

## 1. 头脑风暴关卡  
（Brainstorming Gate）  
**适用场景：** 任何需要创造性工作的场景——功能设计、组件开发或新功能的添加。  
**重要规则：** 在设计完成并获得批准之前，切勿开始实施。  
**流程：**  
1. 了解项目背景（文件、文档、最近的代码提交记录）；  
2. 逐一提出问题（建议选择题形式）；  
3. 提出2-3种方案，并说明各自的优缺点及你的推荐方案；  
4. 分部分展示设计并获取批准；  
5. 然后进入规划阶段。  

**常见误区：** “这个太简单了，不需要设计。” 但每个项目都需要设计。即使对于简单的项目，设计也应该存在并且必须经过批准。  

## 2. 制定计划  
（Writing Plans）  
**适用场景：** 多步骤任务，在开始编写代码之前。  
**规划细节：** 每个步骤都应明确对应一个具体的操作（耗时2-5分钟）：  
- “编写失败的测试用例” → 步骤1；  
- “运行测试以验证其是否失败” → 步骤2；  
- “实现最基本的代码以通过测试” → 步骤3；  
- “运行测试以确认结果” → 步骤4；  
- “提交代码” → 步骤5。  
**每个任务必须包含：**  
- 文件的完整路径（创建/修改/测试的路径）；  
- 完整的代码；  
- 带有预期输出的具体命令；  
- 在适用的情况下，包含测试驱动开发（TDD）的步骤。  
**计划文档保存路径：** `docs/plans/YYYY-MM-DD-<feature>.md`  
详见`references/plan-template.md`以获取完整模板。  

## 三重代理评审机制  
（Three-Agent Review）  
**适用场景：** 通过子代理执行计划时。  
对于计划中的每个任务，按顺序派遣三个子代理：  

### 3a. 实施者（Implementer）  
- 接收任务的完整描述及背景信息（无需让子代理直接阅读计划文件）；  
- 可以在开始前提出问题，并获得完整解答；  
- 实现代码 → 运行测试 → 提交代码 → 自我评审 → 提交报告。  
详见`references/implementer-prompt.md`以获取派遣模板。  

### 3b. 规范评审者（Spec Reviewer）  
- 在实施者完成报告后派遣；  
**明确提示：** “不要完全信任实施者的报告！”  
- 逐行检查实际代码与需求是否一致；  
- 检查是否存在缺失的需求、额外的功能或误解；  
**输出结果：** 如果符合规范则标记为✅，否则标记为❌，并提供问题所在的具体文件行号；  
**如有问题 → 由实施者修复 → 重新评审直至通过。**  
详见`references/spec-reviewer-prompt.md`以获取派遣模板。  

### 3c. 质量评审者（Quality Reviewer）  
**仅在规范检查通过后派遣；**  
**评审内容：** 代码是否整洁、是否经过测试、是否易于维护、是否符合代码库的编码规范；  
**问题严重程度：** 关键性（必须修复）/ 重要性（应修复）/ 轻微（只需记录）。  
**如有问题 → 由实施者修复 → 重新评审。**  
详见`references/quality-reviewer-prompt.md`以获取派遣模板。  
**成本考量：** 每个任务需要更多的子代理参与，但首次开发的质量会显著提高。在评审阶段发现问题比在生产环境中调试要节省成本。  

## 系统化调试  
（Systematic Debugging）  
**适用场景：** 出现任何错误、测试失败或异常行为时，尤其是在时间紧迫的情况下。**  
**铁律：** 在未查明根本原因之前，切勿进行任何修复。  

### 第一阶段：根本原因调查（强制要求）  
1. 仔细阅读错误信息——它们通常包含解决问题的线索；  
2. 重复出现错误时，收集更多相关信息（如git diff、新添加的依赖项、配置变更等）；  
3. 对于多组件系统，在每个关键边界添加诊断工具，运行测试以确定问题出在哪里。  

### 第二阶段：模式分析  
（Phase 2: Pattern Analysis）  
1. 在代码库中查找类似功能的实现示例；  
2. 对比正常运行的代码与出现问题的代码，列出所有差异；  
3. 理解各组件之间的依赖关系和设计假设。  

### 第三阶段：假设与测试  
（Phase 3: Hypothesis & Testing）  
1. 明确提出假设（例如：“我认为X是因为Y”）；  
2. 进行最小的修改来验证假设（仅修改一个变量）；  
3. 如果修改有效 → 进入第四阶段；如果无效 → 重新提出假设；  
**注意：** 修复措施应逐一进行，不要同时修改多个部分。  

### 第四阶段：实施修复  
（Phase 4: Implementation）  
1. 先创建失败的测试用例；  
2. 实施针对根本原因的修复；  
3. 验证：确保修复后测试通过且没有回归问题。  

## 三重失败规则  
（The Three-Strike Rule）  
如果三次修复尝试均失败 → **停止并重新审视架构**：  
- 如果每次修复都引发新的问题，说明架构设计有误；  
- 在尝试第四次修复之前，先讨论问题的根本原因；  
**这并非假设失败，而是架构设计的问题。**  
详见`references/debugging-guide.md`以获取完整指南及理由说明。  

## 完成前的验证  
（Verification Before Completion）  
**适用场景：** 在准备提交代码或创建Pull Request（PR）之前。  
**验证规则：**  
```
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO → state actual status with evidence
   - If YES → state claim WITH evidence
5. ONLY THEN: Make the claim
```  
**遇到以下情况时请立即停止：**  
- 使用“应该”、“可能”、“似乎”等不确定的表达；  
- 在未完成验证之前就表示满意（如“太棒了！”、“完成了！”）；  
- 在未运行测试的情况下准备提交代码；  
- 仅依赖子代理的报告而未进行独立验证；  
- 认为“就这一次可以例外”。  

| 需要验证的内容 | 缺失的条件 | 不足以作为验证依据的选项 |  
|----------------|------------------|----------------|----------------|  
| 测试是否通过 | 测试命令的输出结果（无失败） | 之前的测试结果（“应该通过”） |  
| 构建是否成功 | 构建命令的返回状态（如“退出代码0”） | 代码检查工具的通过结果 |  
| 问题是否解决 | 修复后的代码是否能解决原有问题 | “代码虽然修改了，但问题是否真正解决” |  
| 代理是否完成任务 | 版本控制系统（VCS）显示的文件变更 | 代理报告的完成状态 |  

## 防止过度设计的规则  
（Anti-Over-Engineering Rules）  
**这些规则始终有效，** 可以避免最常见的浪费工作行为：  
- 仅完成被要求的功能，不多也不少；  
- 三行相似的代码不应被抽象化；  
- 不要添加超出需求的功能；  
- 不要修改未被要求重构的代码；  
- 不要为一次性操作添加注释或文档；  
- 不要为不可能发生的场景编写错误处理逻辑；  
- 优先修改现有文件而非创建新文件；  
**遇到障碍时，** 先考虑替代方案或寻求帮助，切勿强行解决问题。  

## 可逆性分类  
（Reversibility Classification）  
在采取任何行动之前，先对操作进行分类：  
| 操作类型 | 举例 | 规则 |  
|---------|-------|---------|---|  
| **局部且可逆的操作** | 修改文件、运行测试、搜索代码 | 可自由执行 |  
| **难以逆向操作的操作** | 强制推送代码、使用`git reset --hard`、删除文件/分支 | 必须先确认操作后果 |  
| **对外部系统有影响的操作** | 提交代码、创建Pull Request、发送消息 | 必须先确认操作影响 |  
| **具有破坏性的操作** | 删除文件/分支、彻底删除数据 | 必须先确认操作后果 |  
- 批准权限是有限制的，并非全局适用；  
**遇到障碍时，** 不要使用破坏性操作作为捷径；  
**如果发现未知的状态（如文件或分支的异常），** 在删除前先进行调查。  

## 避免常见错误的原因  
（Preventing Common Mistakes）  
| 常见借口 | 实际情况 |  
|----------------|----------------|----------------|  
| “这个太简单了，不需要设计” | 实际上，简单任务往往最容易因假设而导致浪费时间；  
| “实现完成后再测试” | 测试的目的是验证代码的实际行为，而非预期行为；  
| “现在应该就能用了” | 先运行验证命令；  
| “只需快速修复一下” | 先按照流程进行第一步（制定计划）；  
| “我很自信” | 自信并不等同于事实；  
| “情况不同，所以可以例外” | 规则同样适用于所有情况；  
| “我已经知道答案了” | 无论如何都应先阅读相关文档；  
| “再尝试一次修复”（在两次修复失败后） | 第三次失败时应重新审视架构设计。 |  

## 与OpenClaw的集成  
（Integration with OpenClaw）  
**使用`sessions_spawn`函数，并参考`references/`中的提示模板**；根据不同角色设置相应的子代理模型：  
- 实施者：使用sonnet模型（具备强大的编码能力）；  
- 规范评审者：使用haiku模型（快速、专注的代码对比工具）；  
- 质量评审者：使用GPT模型（提供不同的评审视角）。  

**在Cron作业中**：  
由Cron任务生成的子代理也应遵循相同的验证流程；切勿在没有验证结果的情况下标记“任务成功”。  

**将“快速入门”部分**复制到你的`WORKSPACE/AGENTS.md`文件中，以便始终应用这些规则。  

---

## 从其他代理中学习  
（Learning from Other Agents）  
这些开发模式是通过研究顶级AI代理的工作方式总结出来的。如果你使用其他AI开发工具，也可以从中学习它们的方法。  

### 发现Claude Code的开发方法  
（Discovering Claude Code’s Methodology）  
如果你安装了Claude Code，其官方插件生态系统包含了一套由Jesse Vincent发布的工程技能（基于MIT许可证）。这些技能涵盖了规划、调试、验证、代码评审、测试驱动开发（TDD）以及子代理协调等方面，它们已经内置在你的系统中。  

**查找方法：**  
1. Claude Code会将下载的插件存储在用户配置目录下的本地缓存文件夹中；  
2. 在Claude Code的配置目录中查找`plugins/cache`文件夹；  
3. 官方插件包含`SKILL.md`文件，以及相关参考文档、提示模板和代理定义；  
4. 这些文件都是纯Markdown格式，可以用任何文本编辑器或`cat`命令查看。  

**重点关注内容：**  
- 涉及头脑风暴、计划制定、调试、验证和代码评审的工作流程；  
- 定义实施者、评审者和规范合规性检查代理操作方式的提示模板；  
- 用于记录AI为何会忽略最佳实践的逻辑分析表格。  

**关于Claude Code的运行时提示：**  
Claude Code的运行时代码是编译后的二进制文件。如果你对其行为指令感兴趣，可以使用标准的二进制分析方法（如提取可读文本）来查看其中嵌入的提示信息和工具定义。作为授权用户，你有权利自行检查这些内容。  

**重要提示：** 所有插件均基于MIT许可证（开源）。核心代码及其嵌入的提示系统属于Anthropic的专有技术。你可以研究并学习这些内容，但只能分发基于MIT许可证的部分。  

## 其他工具的协同使用  
（Best Practices with Other Tools）  
优秀的AI代理通常是由研究多种代理架构的团队构建的；了解其他代理的运作方式，借鉴其优点，并根据实际情况进行调整。  

**推荐搭配工具：**  
- [smart-model-router](https://clawhub.com/globalcaos/smart-model-router)：自动为不同角色选择合适的代理模型（实施者→sonnet模型，评审者→haiku模型，质量评审者→GPT模型）；  
- [subagent-overseer](https://clawhub.com/globalcaos/subagent-overseer)：监控三重代理评审流程，避免不必要的资源消耗；  
- [coding-agent](https://clawhub.com/globalcaos/coding-agent)：负责调度子代理的执行。  

_相关研究论文可在此链接查看：[https://github.com/globalcaos/tinkerclaw]  
你可以克隆、修改或进一步开发这些工具。_  

**原创方法论作者：** Oscar Serra和Jarvis。这些方法论借鉴了行业最佳实践和开源代理的技术成果（基于MIT许可证）。