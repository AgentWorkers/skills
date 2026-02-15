---
name: ralstp-consultant
description: 使用 RALSTP（递归代理与标志性战略-战术规划）来分析问题。该方法基于 Dorian Buksz 的博士论文（RALSTP）开发。该工具能够识别相关代理、计算问题的复杂性，并提供问题分解的建议。
---

# RALSTP顾问

本技能基于伦敦国王学院Dorian Buksz于2024年发表的论文《递归代理与战略-战术规划（RALSTP）》（Recursive Agents and Landmarks Strategic-Tactical Planning (RALSTP)）。

## 核心概念（摘自论文）

### 1. 代理（Agents）识别

**定义：**代理是具有**动态类型**的对象，在目标状态搜索过程中处于活跃状态。

**识别方法：**
- **动态类型**：作为任何动作效果（effects）中谓词（predicate）的第一个参数出现。
- **静态类型**：从未出现在动作效果中。
- **示例：**在Driverlog中，`truck`和`driver`是动态类型（它们出现在`drive`动作的效果中），而`location`是静态类型。

**真实PDDL示例（RTAM领域）：**
```pddl
(:types  
   ambulance police_car tow_truck fire_brigade - vehicle
   acc_victim vehicle car - subject
   ...
)
```
- **代理：** ambulance（救护车）、police_car（警车）、tow_truck（拖车）、fire_brigade（消防队）（它们会出现在`at`、`available`、`busy`等动作效果中）。
- **被动对象：**acc_victim（事故受害者）、car（车辆）（被其他代理作用，但自身不采取行动）。

### 2. 被动对象（Passive Objects）

这些对象不是代理——它们是被其他代理作用的对象，但自身不采取任何行动。
- 包裹（packages）、货物（cargo）、数据（data）、文件（files）、事故受害者（victims）在RTAM中属于被动对象。

### 3. 代理依赖关系（Agent Dependencies）

**定义：**代理之间的关系取决于它们为其他代理满足的前提条件（preconditions）。

**类型：**
- **独立代理（Independent）**：彼此之间没有依赖关系的代理。
- **依赖代理（Dependent）**：需要其他代理满足前提条件的代理。
- **冲突代理（Conflicting）**：相互干扰的代理。

### 4. 纠缠（Entanglement）

**定义：**当代理为共享资源（如时间、空间、位置等）而发生竞争时。

**衡量标准：**
- 共享谓词的数量。
- 目标状态中的冲突频率。

**真实PDDL示例（RTAM - 道路交通事故）：**
```pddl
(:durative-action confirm_accident
   :parameters (?V - police_car ?P - subject ?A - accident_location)
   :condition (and (at start (at ?V ?A)) (at start (at ?P ?A)) ...)
   :effect (and (at end (certified ?P)) ...)
)

(:durative-action untrap
   :parameters (?V - fire_brigade ?P - acc_victim ?A - accident_location)
   :condition (and (at start (certified ?P)) (at start (available ?V)) ...)
)
```
- **纠缠关系：**消防队（fire_brigade）必须先完成“untrap”动作，警车（police_car）才能开始救援。
- **资源冲突：**两者都需要位于同一事故现场（accident_location）。
- **可用性限制：**消防队在进行救援时处于忙碌状态，其他代理必须等待。

### 5. 地标（Landmarks）

**定义：**在任何有效计划中都必须成立的事实（从目标状态回到初始状态）。

**类型：**
- **事实地标（Fact Landmarks）**：必须成立的命题。
- **动作地标（Action Landmarks）**：必须执行的动作。
- **放宽地标（Relaxed Landmarks）**：仅考虑积极效果的地标（忽略删除操作）。

**真实PDDL示例（RTAM - 顺序依赖关系）：**
```
Goal: (delivered victim1) ∧ (delivered car1)

Required sequence of fact landmarks:
1. (certified victim1)     ← police must confirm
2. (untrapped victim1)     ← fire must free them
3. (aided victim1)         ← ambulance must treat
4. (loaded victim1 ambulance) ← ambulance must load
5. (at victim1 hospital)   ← deliver to hospital
6. (delivered victim1)     ← FINAL

Action landmarks:
- confirm_accident → untrap → first_aid → load_victim → unload_victim → deliver_victim
```

### 6. 战略与战术（Strategic vs Tactical）

- **战略（Strategic）：**抽象的规划层面。解决“首先需要做什么”的问题，忽略具体细节。
- **战术（Tactical）：**详细的执行层面。解决“如何具体执行”的问题。

### 7. 难度指标

根据论文，难度随着以下因素增加：
- 目标状态中的代理数量增加。
- 代理之间的纠缠关系加剧（冲突依赖增多）。
- 未达到目标状态的非活跃动态对象增多。

**Buksz复杂性得分 ≈ 代理数量 × 纠缠因子（Buksz Complexity Score ≈ Agent Count × Entanglement Factor）**

## 实现说明（自然语言 vs PDDL）

该技能有两种使用模式：

1. **概念模式（默认模式）：**使用大型语言模型（LLM）将RALSTP方法应用于**自然语言**问题（例如：“规划一次营销活动”）。无需PDDL文件。系统会概念性地识别代理和地标。
2. **正式模式（可选）：**如果您提供PDDL领域/问题文件，可以运行内置的`scripts/analyze.py`来数学化地提取代理和地标信息。

*以下说明适用于两种模式，但提供了“真实PDDL示例”以提供技术背景。*

## 使用方法

对于任何复杂问题，只需描述问题，系统将应用RALSTP方法进行处理：

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
- 复杂的协调任务。

**不适用场景：**
- 简单的问答问题。
- 单任务问题。

## 参考文献

博士论文：《递归代理与战略-战术规划（RALSTP）》——Dorian Buksz，伦敦国王学院，2024年。

## 示例：RTAM领域（IPC-2014）

**领域：**道路交通事故管理（Road Traffic Accident Management）

**来源：** https://github.com/potassco/pddl-instances/tree/master/ipc-2014/domains/road-traffic-accident-management-temporal-satisficing

### 完整分析

**代理（4个）：**
- ambulance（救护车）：将受害者送往医院。
- police_car（警车）：确认事故情况/受害者状态。
- tow_truck（拖车）：拖拽受损车辆。
- fire_brigade（消防队）：解救受害者、扑灭火源。

**被动对象：**
- acc_victim（事故受害者）：需要帮助的人。
- car（车辆）：涉及事故的车辆。
- accident_location（事故现场）、hospital（医院）、garage（车库）。

**依赖关系（关键路径）：**
```
police_car → fire_brigade → ambulance → hospital
     ↓            ↓           ↓
  certify      untrap       deliver
```

**地标链（必须按顺序执行）：**
1. `confirm_accident`（警车到达现场确认事故）。
2. `untrap`（消防队解救受害者）。
3. `first_aid`（救护车提供急救）。
4. `load_victim`（救护车装载受害者）→ `unload_victim`（卸下受害者）→ `deliver_victim`（运送受害者）。
5. `load_car`（拖车装载车辆）→ `unload_car`（卸下车辆）→ `deliver_vehicle`（运送车辆）。

**纠缠关系：**
- 多辆车必须位于同一事故现场。
- 车辆的可用性有限（执行动作时可能处于忙碌状态）。
- 顺序约束：在确认事故情况之前不能进行运送。

**难度：** 高——4个代理，依赖关系紧密，共享资源有限。