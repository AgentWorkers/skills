---
name: superclaw
description: 完整的软件开发工作流程：从设计开始，经过计划阶段，最终执行，并设置相应的检查点（checkpoints）。
---
# Superclaw ⚔️  
**OpenClaw代理的规范软件开发工作流程**  
基于Jesse Vincent的[obra/superpowers](https://github.com/obra/superpowers)项目改编。  

---

## 该技能包的作用  
Superclaw可以防止代理直接开始编写代码，而是强制执行一个分为三个阶段的工作流程：  
1. **🧠 头脑风暴**（`brainstorming/SKILL.md`）——先设计再编码  
2. **📋 制定计划**（`writing-plans/SKILL.md`）——实施前先制定计划  
3. **⚙️ 执行计划**（`executing-plans/SKILL.md`）——分批执行并设置检查点  

这三个阶段在软件开发过程中会自动串联执行。  

---

## 工作原理  

### 第一阶段：头脑风暴（先设计再编码）  
**触发条件**：创建新功能、构建组件或添加新功能时  

**流程**：  
1. 查看上下文信息（`MEMORY.md`、`USER.md`及每日日志）  
2. 提出相关问题（如需求、限制条件及权衡因素）  
3. 提出2-3种解决方案并分析优缺点  
4. 展示设计方案  
5. 得到批准  
6. 将设计文档保存到`workspace/docs/plans/YYYY-MM-DD-<topic>-design.md`  
7. **自动触发`writing-plans`技能**  

**重要规则**：设计未获批准前，严禁编写代码。  

---

### 第二阶段：制定计划（实施前先制定计划）  
**触发条件**：设计方案获得批准后  

**流程**：  
1. 询问开发方法（例如是否采用TDD或直接编码）  
2. 确定代码提交的频率  
3. 将工作分解为每段2-5分钟的可执行任务  
4. 将实施计划保存到`workspace/docs/plans/YYYY-MM-DD-<topic>-plan.md`  
5. **自动触发`executing-plans`技能**  

**特点**：这些问题仅用于引导开发过程，不具强制性，尊重用户的偏好和时间限制。  

---

### 第三阶段：执行计划（分批执行并设置检查点）  
**触发条件**：实施计划准备好后  

**流程**：  
1. 从文档中加载实施计划  
2. 将任务分成每组3-5个  
3. 分批执行任务（使用`sessions_spawn`确保任务隔离）  
4. 审查执行结果  
5. 设置检查点（例如：“第N批任务已完成，是否继续？”）  
6. 更新`memory/YYYY-MM-DD.md`以记录进度  
7. 重复此过程直至任务全部完成  

**重要规则**：每批任务最多执行5个；检查点必须严格执行，不可跳过。  

---

## 为什么使用Superclaw？  
**不使用Superclaw时**：  
- 代理会立即开始编码（缺乏设计和计划）  
- 错误可能在多个任务中累积  
- 无法暂停或恢复执行  
- 开发过程中的思路容易丢失  

**使用Superclaw后**：  
- 强制执行“设计→计划→执行”的流程  
- 可及早发现错误（分批执行有助于防止错误扩散）  
- 进度得到实时跟踪  
- 项目具有可恢复性、可审查性和可审计性  

---

## 安装  
```bash
npx clawhub@latest install superclaw
```  
当检测到相关任务时，相关技能会自动加载。  

---

## 针对OpenClaw的定制优化：  
1. **集成`MEMORY.md`、`USER.md`及每日日志**  
2. 开发方法的选择更加灵活（例如询问是否使用TDD，而非强制使用）  
3. 每个任务都会创建新的子代理以隔离执行环境  
4. 代码保存路径统一为`workspace/docs/plans/`  

---

## 测试  
所有技能均经过RED-GREEN-REFACTOR方法论的严格测试：  
| 技能 | 未使用该技能 | 使用该技能 |
|-------|---------------------|-------------------|
| 头脑风暴 | 12秒内完成编码 | 先提出问题并获取批准 |
| 制定计划 | 73秒内完成编码 | 先确定开发方法并制定计划 |
| 执行计划 | 40秒内完成10个任务 | 分成4批执行并设置检查点 |

**集成测试结果**：所有三个技能能够自动串联执行，且通过CLI正常使用。  

---

## 示例工作流程  
**用户需求**：构建一个Markdown笔记管理CLI工具  

**流程**：  
1. **使用**`brainstorming`技能**：  
   - 提出问题（存储格式、搜索功能、标签功能等）  
   - 提出3种实现方案（平面文件、SQLite或JSON）  
   - 展示设计方案并获得批准  
   - 保存设计文档：`workspace/docs/plans/2026-02-25-notes-cli-design.md`  
   - **触发`writing-plans`技能**  

2. **使用**`writing-plans`技能**：  
   - 选择开发方法（TDD或直接编码）  
   - 确定代码提交频率  
   - 制定实施计划（24个任务，每个任务耗时2-5分钟）  
   - 保存计划文档：`workspace/docs/plans/2026-02-25-notes-cli-plan.md`  
   - **触发`executing-plans`技能**  

3. **使用**`executing-plans`技能**：  
   - 第一批任务（1-5个）：项目设置  
   - 第二批任务（6-10个）：创建笔记功能  
   - 第三批任务（11-15个）：列出笔记功能  
   - 重复此过程直至任务全部完成  

**最终结果**：一个功能完备、文档齐全、经过测试且进度可追踪的Markdown笔记管理CLI工具。  

---

## 各技能文件详情：  
- `brainstorming/SKILL.md`：279行代码，包含完整流程及合理性分析  
- `writing-plans/SKILL.md`：10KB，包含开发方法相关问题和任务模板  
- `executing-plans/SKILL.md`：9KB，包含分批执行逻辑及任务隔离机制  

每个技能均可独立使用，也可作为整个工作流程的一部分。  

---

## 致谢  
本技能包基于Jesse Vincent的[obra/superpowers](https://github.com/obra/superpowers)项目进行改编，针对OpenClaw的个性化辅助系统进行了优化，包括集成`MEMORY.md`和`USER.md`、提供灵活的开发方法选择、采用`sessions_spawn`进行任务隔离，以及统一代码保存路径等特性。  

---

## 许可证  
遵循MIT许可证（与obra/superpowers相同）。  

---

## 相关资源：  
- **GitHub仓库**：https://github.com/brothaakhee/superclaw（即将上线）  
- **原始框架**：https://github.com/obra/superpowers  
- **OpenClaw官方文档**：https://docs.openclaw.ai