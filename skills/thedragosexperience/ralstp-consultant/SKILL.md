---
name: ralstp-consultant
description: 使用 RALSTP（递归代理与地标战略-战术规划，Recursive Agents and Landmarks Strategic-Tactical Planning）来分析问题。该方法基于 Dorian Buksz 的博士论文 RALSTP 开发。该工具能够识别相关代理、计算问题的难度，并提出问题的分解方案。
---

# RALSTP咨询师

本方法基于伦敦国王学院Dorian Buksz于2024年发表的论文《递归代理与战略-战术规划（RALSTP）》（"Recursive Agents and Landmarks Strategic-Tactical Planning (RALSTP)"）。

## 核心概念（摘自论文）

### 1. 代理识别

**定义：** 代理是具有**动态类型**的实体，在目标状态搜索过程中处于活跃状态。

**识别方法：**
- **动态类型**：作为任何动作**效果**中谓词的首个参数出现。
- **静态类型**：从未出现在动作效果中。
- **示例：** 在Driverlog中，`truck`和`driver`是动态类型（它们出现在`drive`动作的效果中），而`location`是静态类型。

### 2. 被动对象

非代理的实体——它们是动作的接受者，但本身不执行任何动作。
- 包裹、货物、数据、文件、RTAM（实时任务管理）中的受害者等。

### 3. 代理依赖关系

**定义：** 代理之间的关系取决于它们为其他代理满足的前提条件。

**类型：**
- **独立代理**：彼此之间没有依赖关系的代理。
- **依赖代理**：需要其他代理满足前提条件的代理。
- **冲突代理**：相互干扰的代理。

### 4. 纠缠

**定义：** 当代理为共享资源（如时间、空间、位置等）而发生竞争时。

**衡量方式：**
- 共享谓词的数量。
- 目标状态中的冲突频率。

### 5. 地标

**定义：** 在任何有效计划中都必须成立的事实（从目标状态回溯到初始状态）。

**类型：**
- **事实地标**：必须成立的前提或命题。
- **动作地标**：必须执行的动作。
- **放宽地标**：仅考虑正面效果的地标（忽略删除操作）。

### 6. 战略与战术

- **战略层面：** 抽象的规划层次。解决“首先需要做什么”的问题，忽略具体细节。
- **战术层面：** 具体的执行层次。解决“如何具体执行”的问题。

### 7. 难度指标

根据论文，难度随着以下因素的增加而增加：
- 目标状态中的代理数量增加。
- 代理之间的纠缠关系（冲突依赖）增加。
- 未包含在目标状态中的非动态对象数量增加。

**Buksz复杂性得分 ≈ 代理数量 × 纠缠因子**

## 使用方法

对于任何复杂问题，只需描述问题，我就可以应用RALSTP方法：

```
RALSTP analyze: I need to migrate 1000 VMs from datacentre A to B with minimal downtime
```

## 输出格式

```
## RALSTP Analysis

### Agents Identified
- [list agents and their types]

### Passive Objects  
- [list objects being acted upon]

### Dependency Graph
- [which agents depend on which]

### Difficulty Assessment
- Agent Count: X
- Entanglement: Low/Medium/High
- Estimated Complexity: [score]

### Strategic Phase
- [high-level plan ignoring details]

### Tactical Phase
- [detailed execution]

### Decomposition Suggestion
- Split by: [agent type / landmark / location]
- Parallelize: [what can run concurrently]
- Risks: [potential conflicts/entanglements]
```

## 适用场景

**适用于：**
- 包含多个参与者的多步骤工作流程。
- 具有依赖关系的迁移/任务。
- 资源争夺问题。
- 复杂的协调问题。

**不适用场景：**
- 简单的问答场景。
- 单任务问题。

## 参考文献

博士论文：《递归代理与战略-战术规划（RALSTP）》——Dorian Buksz，伦敦国王学院，2024年。