---
name: create-hat-collection
description: 通过引导式对话生成新的Ralph帽子系列预设。会提出澄清性问题，根据模式约束进行验证，并输出可用于实际生产的YAML文件。
---

# 创建帽子集合（Create Hat Collection）

## 概述

此功能通过引导式、对话式的流程生成Ralph帽子集合的预设配置。它会询问关于您工作流程的详细信息，验证配置是否符合架构规范，并生成一个可用于实际生产的YAML预设文件。

**输出：** 一个完整的`.yml`预设文件，保存在`presets/`目录中。

## 适用场景

- 从零开始创建新的多代理工作流程  
- 将工作流程的想法转化为结构化的预设配置  
- 需要关于帽子设计模式和事件路由的指导  

**不适用场景：** 修改现有的预设配置（请使用`/creating-hat-collections`功能）

## 工作流程

### 第1阶段：了解工作流程

通过提问来明确以下内容：  
1. **目的：** 该工作流程旨在解决什么问题？  
2. **架构模式：** 哪种架构模式最适合当前需求？  
   - **流水线（Pipeline）：** A→B→C的线性流程（分析→总结）  
   - **批评者-执行者（Critic-Actor）：** 一人提出建议，另一人进行评审（代码审查）  
   - **监督者-工作者（Supervisor-Worker）：** 协调者将任务分配给专家  
   - **科学方法（Scientific）：** 观察→假设→测试→修复（调试）  
3. **角色分配：** 需要哪些不同的代理角色？  
4. **任务交接：** 每个角色应在何时将任务交接给下一个角色？  
5. **完成条件：** 什么信号表示工作流程已完成？  

### 第2阶段：设计事件流程  

将工作流程映射为事件链：  
```
task.start → [Role A] → event.a → [Role B] → event.b → [Role C] → LOOP_COMPLETE
                                                    ↓
                                         event.rejected → [Role A]
```  

**需要验证的约束条件：**  
- 每个触发器（trigger）只能对应一个特定的“帽子”（避免事件路由混乱）  
- `task.start`和`task.resume`是预定义的触发器，禁止用作其他用途  
- 每个“帽子”必须至少发布一个事件  
- 事件链最终必须达到`LOOP_COMPLETE`状态  

### 第3阶段：生成预设文件  

使用以下结构创建YAML文件：  
```yaml
# <Preset Name>
# Pattern: <Architecture Pattern>
# <One-line description>
#
# Usage:
#   ralph run --config presets/<name>.yml --prompt "<example prompt>"

event_loop:
  starting_event: "<first.event>"  # Ralph publishes this

hats:
  hat_key:
    name: "<Emoji> Display Name"
    description: "<Short description of the hat's purpose>"
    triggers: ["event.triggers.this"]
    publishes: ["event.this.publishes", "alternate.event"]
    default_publishes: "event.this.publishes"
    instructions: |
      ## <HAT NAME> MODE

      <Clear role definition - what this hat does>

      ### Process
      1. <Step one>
      2. <Step two>
      3. Publish appropriate event

      ### Event Format
      ```  
      <event topic="event.name">  
      key: value  
      </event>  
      ```

      ### DON'T
      - <Common mistake to avoid>
      - <Another mistake>
```  

## 架构规范参考  

### 必需的顶层字段  

| 字段 | 描述 |  
|-------|-------------|  
| `event_loop.starting_event` | Ralph发布的第一个事件 |  

### 帽子定义字段  

| 字段 | 是否必填 | 描述 |  
|-------|----------|-------------|  
| `name` | 是 | 显示名称，可添加表情符号（例如：“🔍 分析器”） |  
| `description` | 是 | 概述该“帽子”的用途（一句话） |  
| `triggers` | 是 | 该“帽子”响应的事件列表 |  
| `publishes` | 是 | 该“帽子”可以发布的事件列表 |  
| `default_publishes` | 推荐使用 | 如果“帽子”忘记发布事件时使用的默认事件 |  
| `instructions` | 是 | 适用于特定角色的提示信息（多行内容使用`\|`分隔） |  

### 不允许使用的字段  

这些字段不在架构规范中，请勿使用：  
- `emoji`（请将表情符号添加到`name`字段中）  
- `system_prompt`（请使用`instructions`字段）  
- `subscriptions`/`publications`（请使用`triggers`/`publishes`字段）  

## 事件命名规范  

```
<phase>.ready / <phase>.done      # Phase transitions
<thing>.approved / <thing>.rejected  # Review gates
<noun>.found / <noun>.missing     # Discovery events
<action>.request / <action>.complete # Request-response
```  

**示例事件名称：** `analysis.complete`、`review.approved`、`build.blocked`、`spec.rejected`  

## 验证清单  

在最终确定预设配置之前，请检查以下内容：  
- 每个触发器都只能对应一个“帽子”  
- 没有“帽子”使用`task.start`或`task.resume`作为触发器  
- 所有“帽子”都包含`name`、`description`、`triggers`、`publishes`和`instructions`字段  
- 对于具有多个发布选项的“帽子”，必须设置`default_publishes`字段  
- 事件链能够达到`LOOP_COMPLETE`状态  
- 不存在未被处理的孤立事件（仅作为警告）  
- 提示信息中应包含角色职责、处理步骤、事件格式以及注意事项  

## 输出文件位置  

将生成的预设文件保存在：`presets/<name>.yml`  
对于简化的/嵌入式预设文件，保存路径为：`presets/minimal/<name>.yml`  

## 预设文件测试  

生成预设文件后，请使用以下命令进行测试：  
```bash
# Dry run to validate config parsing
cargo run --bin ralph -- run -c presets/<name>.yml -p "test prompt" --dry-run

# Run smoke tests
cargo test -p ralph-core smoke_runner
```  

使用`/evaluate-presets`命令进行全面的验证。  

## 示例对话  

**用户：** 我需要一个专注于安全代码审查的预设配置。  

**助手：** 我将帮助您创建一个专注于安全审查的预设配置。请回答几个问题：  
1. **审查深度：** 是进行快速扫描还是深入分析？  
2. **所需角色：** 我建议设置以下角色：  
   - 安全分析师（发现漏洞）  
   - 代码审查员（检查代码逻辑/风格）  
   - 总结者（编写最终报告）  
   这些角色是否符合您的需求？或者还需要添加/删除某些角色？  
3. **问题处理方式：** 如果发现问题，是直接修复代码还是仅报告问题？  

**用户：** 需要进行深入分析，这些角色设置合适，只需报告问题即可。  

**助手：** 这是我设计的事件流程：  
```
task.start → [Security Analyst] → security.complete
                                        ↓
          → [Code Reviewer] → review.complete
                                        ↓
          → [Summarizer] → LOOP_COMPLETE
```  
（生成符合架构规范的YAML文件，包含三个相关“帽子”）  

## 常见架构模式参考  

### 流水线（Pipeline）  
```
A → B → C → done
```  
适用于：分析工作流程、文档处理  

### 批评者-执行者（Critic-Actor）  
```
Actor → Critic → approved/rejected
                    ↓
         rejected → Actor (retry)
```  
适用于：代码审查、质量控制流程  

### 监督者-工作者（Supervisor-Worker）  
```
Supervisor → worker.task → Worker → work.done → Supervisor
```  
适用于：复杂任务的拆分与协调  

### 科学方法（Scientific Method）  
```
Observe → Hypothesize → Test → confirmed/rejected
                                    ↓
                         rejected → Observe
```  
适用于：调试、问题调查