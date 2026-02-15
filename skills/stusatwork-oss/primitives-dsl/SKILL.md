---
name: primitives-dsl
description: "通用游戏架构DSL（Domain-Specific Language），包含六种基本组件：LOOP（循环）、TILEGRID（网格结构）、CONTROLBLOCK（控制模块）、POOL（资源池）、EVENT（事件处理）、DISPATCHER（调度器）。适用场景包括：  
1. 设计可移植的游戏/模拟循环；  
2. 在不同架构之间进行转换（如68K、Cell、CUDA、ECS）；  
3. 向AI代理解释游戏引擎的结构；  
4. 将复杂的逻辑重构为明确的状态管理和流程控制。  
使用该DSL后，会生成以下输出：  
- 基本组件映射（Primitive Map）；  
- 数据流图（Dataflow Sketch）；  
- 具体实现示例（Worked Example）；  
- 可移植性说明（Portability Notes）。"
---

# primitives-dsl — 通用游戏架构模式

## 该技能的作用

提供了一个简洁、可移植的DSL（Domain-Specific Language），包含**六个通用原语**，这些原语广泛应用于68K时代的循环结构、Cell/PPU+SPU协同处理、CUDA/GPU内核以及现代的ECS（Elastic Compute System）引擎中。

**原语包括：**  
- **LOOP**（循环）  
- **TILEGRID**（平铺网格）  
- **CONTROLBLOCK**（控制块）  
- **POOL**（资源池）  
- **EVENT**（事件）  
- **DISPATCHER**（调度器）  

使用该技能可以：  
- 设计能够在不同平台上顺畅运行的游戏/模拟循环结构；  
- 在不同的架构之间进行代码转换（68K ↔ Cell ↔ CUDA ↔ ECS）；  
- 以清晰的方式向AI代理解释引擎结构；  
- 每次使用相同的原语词汇来生成可复用的“示例代码”。  

## 适用场景  

- 在开始新的子系统开发时，需要一个可移植的思维模型；  
- 将混乱的代码重构为明确的状态和流程；  
- 将旧代码映射到现代的架构模式中；  
- 设计适用于受限设备、边缘设备或“未来可扩展的软件”的循环结构。  

## 不适用场景  

- 不要发明新的原语（保持词汇的稳定性）；  
- 不要争论各种引擎技术（如Unity、Unreal或自定义引擎）；  
- 不要跳过具体的实现细节——每次使用该技能时，都必须生成图表、表格或伪代码。  

## DSL的定义  

**LOOP**  
一个具有明确阶段的重复更新循环，支持时间切片和顺序控制。  

**TILEGRID**  
一种具有稳定邻接关系的空间索引结构（适用于2D/3D网格、导航瓷砖、区域单元等）。  

**CONTROLBLOCK**  
一个紧凑且权威的状态记录，用于协调行为并强制执行约束条件（包含标志位、计数器、句柄、计时器等）。  

**POOL**  
一个用于管理频繁创建的对象（如实体、子弹、粒子等）的受限资源分配器；在关键路径中禁止使用无限制的`new`操作。  

**EVENT**  
一种结构化的消息，用于表示“某件事情发生了”，具有最小的数据负载和明确的路由元数据。  

**DISPATCHER**  
负责将任务和事件路由到相应的处理程序（CPU线程、SPU、GPU内核或ECS系统），同时也是调度策略的实现场所。  

## 输出要求  

调用该技能后，必须生成以下内容：  
1. **原语映射表**：说明系统中的各个部分与哪些原语相对应；  
2. **数据流图**：以文本图表或表格的形式描述状态/事件的流动过程；  
3. **一个可复用的示例代码**；  
4. **可移植性说明**：说明该技能如何应用于68K、Cell、CUDA或ECS架构。  

## 调用方式（可复制粘贴的提示）  

```
"Apply primitives-dsl to design a loop for ___ . Provide a Primitive Map + Dataflow + Portability."

"Translate this architecture into LOOP/TILEGRID/CONTROLBLOCK/POOL/EVENT/DISPATCHER."

"Given these constraints (___), propose a primitives-dsl design and a worked example."
```  

## 规范与风格要求：  
- 原语名称必须全部大写；  
- 对于数据映射，优先使用表格形式而非段落描述；  
- 使用简洁的伪代码（避免完整的实现细节）；  
- 必须明确标注`CONTROLBLOCK`中的各个字段名称；  
- 必须指定`POOL`的资源分配范围（即使只是猜测值）；  
- `EVENT`必须包含路由键或通道信息；  
- `DISPATCHER`必须明确指定调度策略（如FIFO、优先级、固定步长等）。  

## 参考资料：  
- **快速参考**：[`assets/quick_card.md`](assets/quick_card.md)  
- **架构映射**：[`references/architecture_mapping.md`](references/architecture_mapping.md)  
- **示例代码**：  
  - [`references/example_shooter.md`](references/example_shooter.md) — 经典射击游戏循环示例  
  - [`references/example_mall.tick.md`](references/example_mall_tick.md) — GLITCHDEXMALL区域模拟示例  
  - [`references/example_npc_step.md`](references/example_npc_step.md) — NPC状态机示例  

## 外部资源：  
- [Anthropic Skills Repository](https://github.com/anthropics/skills) — 技能开发相关资源  
- [Alien Bash II](https://github.com/) — 68K源代码库（Glenn Cumming开发）  
- NVIDIA CUDA编程指南 — 现代GPU原语相关内容  
- Cell Broadband Engine编程手册 — SPE（Cell Broadband Engine）的工作分配机制