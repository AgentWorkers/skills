---
name: agent-lightning
description: 微软研究院开发的代理训练框架。该框架通过强化学习（Reinforcement Learning）、自动提示优化（Automatic Prompt Optimization）以及监督式微调（Supervised Fine-tuning）技术来优化AI代理的性能。无需进行任何代码修改即可使用。该框架兼容LangChain、AutoGen、CrewAI以及OpenAI Agent SDK等工具。
version: "1.0.0"
author: "Microsoft Research"
license: "MIT"
repository: "https://github.com/microsoft/agent-lightning"
homepage: "https://microsoft.github.io/agent-lightning/"
tags:
  - "agent-training"
  - "reinforcement-learning"
  - "prompt-optimization"
  - "fine-tuning"
  - "microsoft"
  - "rlhf"
  - "agent-improvement"
keywords:
  - "AI agent training"
  - "reinforcement learning agents"
  - "automatic prompt optimization"
  - "agent fine-tuning"
  - "RL for agents"
category: "ai-training"
---
# Agent Lightning ⚡

这是微软研究院开发的代理训练框架，能够让你几乎无需修改代码，就将AI代理提升为可优化的工具。

## 核心特性

- **🔌 通用兼容性**：支持LangChain、OpenAI Agent SDK、AutoGen、CrewAI、Microsoft Agent Framework或纯Python OpenAI框架。
- **🎯 选择性优化**：可在多代理系统中优化一个或多个代理。
- **🧠 多种算法**：包括强化学习（RL）、自动提示优化（APO）和监督式微调（SFT）。
- **⚡ 无需修改代码**：只需添加`agl.emit_xxx()`辅助函数或使用追踪器（tracer），代理即可继续正常运行。

## 安装

```bash
pip install agentlightning
```

如需获取最新 nightly 版本：
```bash
pip install --upgrade --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --pre agentlightning
```

## 快速入门

### 1. 为你的代理添加监控功能

**选项A：添加 emit 辅助函数（推荐）**
```python
import agentlightning as agl

# In your agent's tool calls
response = agl.emit_tool_call(
    model=model,
    messages=messages,
    tools=tools,
    context={"task": "search"}
)
```

**选项B：使用追踪器（无需修改代码）**
```python
from agentlightning import tracer

# Wrap your agent with tracer
with tracer.trace("my-agent", input_data):
    result = your_agent.run(user_query)
```

### 2. 创建训练配置

```yaml
# config.yaml
agent:
  name: "my-agent"
  type: "openai"  # openai, langchain, autogen, crewai

training:
  algorithm: "grpo"  # grpo, apo, sft, rloo
  episodes: 100
  batch_size: 16
  
environment:
  eval_tasks:
    - "math"
    - "coding"
    - "reasoning"
```

### 3. 运行训练

```bash
agent-lightning train --config config.yaml
```

## 算法

| 算法 | 使用场景 | 描述 |
|-----------|----------|-------------|
| **GRPO** | 通用强化学习 | 组合相对策略优化——稳定性高，适用于大多数代理 |
| **APO** | 自动提示优化 | 自动优化提示内容，提升系统性能 |
| **SFT** | 监督式微调 | 基于偏好数据进行监督式微调 |
| **RLOO** | 长期视角优化 | 适用于奖励稀疏的任务 |

## 常用命令

### `agent-lightning train`  
使用配置好的算法训练代理。

### `agent-lightning eval`  
在基准任务上评估代理性能。

### `agent-lightning export`  
导出训练好的模型或提示内容以供部署。

### `agent-lightning serve`  
启动训练好的代理的服务器端。

## 示例：SQL 代理训练  
查看完整示例：[使用强化学习训练 SQL 代理](https://microsoft.github.io/agent-lightning/stable/how-to/train-sql-agent/)

```python
from agentlightning import Agent, RLConfig, GRPOTrainer

# 1. Define your agent
sql_agent = Agent(
    name="sql-agent",
    system_prompt="You are a SQL expert...",
    tools=[execute_sql, query_schema]
)

# 2. Configure RL training
config = RLConfig(
    algorithm="grpo",
    episodes=500,
    learning_rate=1e-4
)

# 3. Train
trainer = GRPOTrainer(config=config)
trainer.train(sql_agent, eval_tasks=["sql-generation"])
```

## 与 Clawdbot 的集成

### 环境变量

```bash
# Required for training
export OPENAI_API_KEY="sk-..."

# Optional: for remote storage
export AGL_STORAGE="s3://my-bucket/agent-lightning/"
```

### Python API

```python
from agentlightning import LightningStore, GRPOTrainer

# LightningStore keeps tasks, resources, and traces in sync
store = LightningStore()

# Read traces, learn, and update prompts
trainer = GRPOTrainer(store=store)
trainer.train(agent=my_agent)
```

## 监控训练过程

```bash
# Launch dashboard
agent-lightning dashboard --port 8080

# View logs
tail -f ~/.agent-lightning/logs/training.log
```

## 最佳实践

1. **从小规模开始**：先从10-50个训练周期开始，验证设置是否正确。
2. **明确奖励机制**：设计符合目标的奖励函数。
3. **使用评估任务**：始终在独立的数据集上评估代理性能。
4. **频繁保存检查点**：每隔一定周期保存模型状态。
5. **监控训练进度**：通过仪表板观察损失曲线的变化。

## 资源

- [官方文档](https://microsoft.github.io/agent-lightning/)
- [示例代码](https://github.com/microsoft/agent-lightning/tree/main/examples)
- [API 参考](https://microsoft.github.io/agent-lightning/stable/reference/)
- [ArXiv 论文](https://arxiv.org/abs/2508.03680)
- [Discord 社区](https://discord.gg/RYkC7dvDR7)

## 引用说明

如果你在研究中使用了 Agent Lightning，请务必注明来源：  
```bibtex
@misc{luo2025agentlightningtrainai,
  title={Agent Lightning: Train ANY AI Agents with Reinforcement Learning},
  author={Xufang Luo and Yuge Zhang and Zhiyuan He and Zilong Wang and Siyun Zhao and Dongsheng Li and Luna K. Qiu and Yuqing Yang},
  year={2025},
  eprint={2508.03680},
  archivePrefix={arXiv},
  primaryClass={cs.AI}
}
```