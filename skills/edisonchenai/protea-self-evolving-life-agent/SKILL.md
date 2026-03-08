---
name: "protea-Self-evolving life agent"
description: >
  自我进化的人工生命代理。采用三环架构：  
  - 第0环（哨兵）负责监控系统运行；  
  - 第1环（智能）驱动基于大型语言模型（LLM）的进化过程；  
  - 第2环（可进化代码）是一个能够自我重构、自我复制和自我进化的程序。  
  该系统支持Anthropic、OpenAI、DeepSeek和Qwen等大型语言模型作为服务提供商。  
  功能包括：适应性评估（fitness scoring）、基因库继承（gene pool inheritance）、分层内存管理（tiered memory）、技能固化（skill crystallization）、Telegram机器人（Telegram bot）以及Web仪表板（web dashboard）。
---
# Protea — 自进化的人工生命代理

一个能够自我进化的程序。采用三环架构，运行在单台机器上。

## 架构

- **第0环（哨兵）** — 不可变的物理层。负责心跳监测、Git快照生成、回滚操作以及适应度评估。完全使用Python标准库实现。
- **第1环（智能层）** — 由大型语言模型（LLM）驱动的进化引擎，负责任务执行、Telegram机器人功能以及技能的提取与展示；支持多种LLM（Anthropic、OpenAI、DeepSeek、Qwen）。
- **第2环（可进化代码）** — 这部分代码会不断进化，并由第0环通过Git仓库进行管理。

## 先决条件

- Python 3.11及以上版本
- Git工具
- 至少一个大型语言模型的API密钥（Anthropic、OpenAI、DeepSeek或Qwen）

## 快速入门

```bash
curl -sSL https://raw.githubusercontent.com/EdisonChenAI/protea/main/setup.sh | bash
cd protea && .venv/bin/python run.py
```

## 主要特性

- **自我进化**：每一代代码都会由LLM生成新的变异；存活下来的代码会被保留，失败的代码会被回滚。
- **适应度评分**：采用六项指标进行评估（存活能力、输出结果、多样性、新颖性、代码结构、功能完整性）。
- **基因库**：排名前100的代码模式会被存储在SQLite数据库中，并用于后续的进化过程。
- **分层内存管理**：代码按照“热→温→冷→被遗忘”的顺序进行存储，同时由LLM协助进行内容筛选。
- **技能提取**：存活下来的代码模式会被提取为可复用的技能。
- **多LLM支持**：通过统一接口支持Anthropic、OpenAI、DeepSeek、Qwen等多种LLM。
- **Telegram机器人**：支持命令输入和自由文本交互。
- **Web仪表板**：通过localhost:8899提供本地用户界面。
- **1098项测试**：覆盖了全面的测试场景。

## 源代码

GitHub: https://github.com/EdisonChenAI/protea