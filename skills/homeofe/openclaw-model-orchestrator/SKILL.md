---
name: openclaw-model-orchestrator
description: OpenClaw的多大型语言模型（Multi-LLM）协同工作机制，支持扇形分布（fan-out）、流水线处理（pipeline）以及共识机制（consensus pattern）等模式。该机制能够通过基于AAHP v3算法的智能任务调度策略，将任务分配给40多个不同的模型进行处理。
---
# OpenClaw 模型编排器

该工具能够通过聊天界面将任务分配给多个大型语言模型（LLM），并采用 AAHP v3 结构化的任务传递机制，从而将令牌使用量降至最低。

## 编排模式

### 分布式执行（Fan-Out）
将任务拆分为多个子任务，每个子任务由不同的模型独立执行。
规划模型负责分解任务，工作模型并行执行，审核模型负责合并各模型的结果。

```
/orchestrate --mode fan-out --task "Build a REST API with auth" --planner copilot-opus --workers copilot52c,grokfast --reviewer copilot-sonnet46
```

### 管道式执行（Pipeline）
按顺序链接多个模型，每个模型会对前一个模型的输出进行进一步处理。
适用于“计划 → 实施 → 审核 → 优化”的工作流程。

```
/orchestrate --mode pipeline --task "Design and implement a caching layer" --planner copilot-opus --workers copilot52c,copilot-sonnet46 --reviewer copilot-opus
```

### 共识机制（Consensus）
向多个模型发送相同的问题，然后综合出最佳答案。
该机制能够识别模型之间的共识、分歧以及独特的见解。

```
/orchestrate --mode consensus --task "What are the security risks of this API design?" --workers copilot-opus,gemini25,sonnet --reviewer copilot-opus
```

## 智能推荐
编排器会自动对任务进行分类，并推荐最合适的模型组合：

```
/orchestrate recommend "Build a REST API with JWT auth"
```

最终输出包括：任务分类、推荐的规划模型/工作模型/审核模型、推荐理由以及可直接执行的命令。

使用 `help` 作为参数，可获取与任务相关的推荐信息：
```
/orchestrate --task "Audit security" --planner help
```

## 任务配置文件

针对常见任务类型，预先配置了模型组合：

| 配置文件名 | 规划模型 | 工作模型 | 审核模型 | 适用场景 |
|---------|---------|---------|----------|----------|
| coding | copilot-opus | copilot52c, grokfast | copilot-sonnet46 | 特性开发 |
| research | gemini25 | gemini-flash, copilot-flash | copilot-opus | 分析、研究 |
| security | copilot-opus | copilot-sonnet46, gemini25 | sonnet | 安全审计 |
| review | copilot-opus | copilot-sonnet46, copilot-sonnet | 代码/设计审核 |
| bulk | haiku | copilot-flash, gemini25-flash, gpt5mini | 大量操作 |

## AAHP v3 集成

所有模型之间的通信都使用结构化的 AAHP v3 任务传递对象，而非原始的聊天记录。与简单的上下文传递方式相比，这种方式可将令牌使用量减少 98% 以上。每个任务传递对象包含以下内容：
- 任务相关上下文
- 路由元数据（源模型/目标模型、执行模式）
- 变更内容
- 约束条件（输出格式、范围限制）

## 命令

| 命令            | 描述                                      |
|------------------|-----------------------------------------|
| `/orchestrate help`    | 显示帮助信息及可用的编排模式                          |
| `/orchestrate models`   | 列出所有可用模型及其别名                          |
| `/orchestrate recommend "task"` | 为特定任务获取模型推荐组合                        |
| `/orchestrate --task "..." [flags]` | 执行任务编排                              |

## 配置设置

配置信息存储在 `openclaw.plugin.json` 文件中：

```json
{
  "config": {
    "defaultPlanner": "copilot-opus",
    "defaultReviewer": "copilot-sonnet46",
    "defaultWorkers": ["copilot52c", "grokfast", "copilot51"],
    "maxConcurrent": 4,
    "taskProfiles": { ... }
  }
}
```