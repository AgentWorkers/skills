---
name: mindcore
description: 一种用于人工智能代理的仿生情感引擎。该引擎通过五层神经传导机制（L0：随机噪声 → L1：传感器感知 → L2：潜意识冲动 → L3：人格机制 → L4：决策输出）以及五个心理动力学模块，实现类似人类的情绪反应。该引擎完全独立于任何大型语言模型（LLM），可在本地CPU上使用纯Python语言运行。它能够模拟每天150次情绪冲动，涵盖9个情绪类别，并考虑昼夜节律、情绪调节以及短期记忆等因素的影响。
---
# MindCore — 模仿人类潜意识的引擎

> 为您的AI代理赋予自主的思维、情感和自发的冲动。

## 功能概述

MindCore是一个独立的后台守护进程，它模拟了人类的**潜意识**。该进程每秒都会进行随机事件模拟（类似掷骰子的操作），从而生成诸如“我想喝奶茶”、“我感到无聊”或“我突然想聊天”之类的随机想法。

当某个想法出现的概率超过预设的阈值时，MindCore会向您的AI代理发送一个JSON信号，提示它：“我有话要说。”

## 架构

```
Layer 0: Noise Generators (3000 nodes)
    ├── Pink Noise (1/f, long-range correlation)
    ├── Ornstein-Uhlenbeck (physiological baseline)
    ├── Hawkes Process (emotional chain reaction)
    └── Markov Chain (attention drift)
         ↓
Layer 1: Sensor Layer (150 sensors)
    ├── Body State (hunger/fatigue/bio-rhythms)
    ├── Environment (time/weather/noise)
    └── Social Context (interaction/neglect)
         ↓
Layer 2: Impulse Emergence (150 impulse nodes)
    ├── Synapse Matrix (sensor → impulse mapping)
    ├── Sigmoid Probability + Mood Modulation
    └── Dice Roll → Random Firing
         ↓
Layer 3: Personality Gate (Softmax Sampling)
    ├── Learnable Personality Weights
    └── Short-Term Memory Topic Boost
         ↓
Layer 4: Output Template → JSON signal
```

## 快速入门

```bash
# Install dependencies
pip install -r requirements.txt

# Start the engine
python main.py
```

MindCore需要Python 3.8及以上版本的支持。首次运行时，它会自动下载`all-MiniLM-L6-v2`（约80MB）本地自然语言处理模型，用于生成神经网络矩阵。

## 主要特性

- **每日150次冲动**：涵盖9个类别（食物、社交、娱乐等）
- **随机生成，无固定时间表**：基于粉噪声（Pink Noise）、霍克斯过程（Hawkes Process）和Sigmoid概率模型
- **昼夜节律**：根据真实时钟驱动的饥饿/口渴/睡眠周期
- **短期记忆**：采用5个槽位的FIFO缓冲区，具有2小时的指数衰减机制
- **情绪基线**：持续调节冲动的概率值
- **可调频率**：通过`BURST_BASE_OFFSET`参数来控制系统的活跃程度

## 集成方式

MindCore输出标准的JSON格式数据，专为[OpenClaw](https://openclaw.ai)设计，同时也兼容任何支持外部信号注入的AI代理框架。

详细的集成指南请参阅`references/INTEGRATION.md`。

## 文件结构

- `main.py`：程序的入口点及核心逻辑循环
- `engine/`：包含引擎的5层处理流程实现
- `engine_supervisor.py`：守护进程模式下的进程管理器
- `data/`：存储运行时数据（传感器状态、神经网络矩阵、记忆信息）
- `js_bridge/`：用于与OpenClaw集成的JavaScript桥接层

## 许可证

MindCore采用AGPL-3.0许可证（提供商业许可选项——请联系zmliu0208@gmail.com）