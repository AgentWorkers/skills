# 存储记忆 📦

**状态：** ✅ 正在运行 | **模块：** 存储模块 | **所属部分：** 代理大脑（Agent Brain）

记忆的编码、检索、整合与遗忘过程。这是大脑的存储系统。

## 功能概述

- **编码（Encode）**：将经历转化为可存储的记忆。
- **检索（Retrieve）**：查找相关的过往知识。
- **整合（Consolidate）**：强化重要记忆，压缩旧记忆。
- **遗忘（Decay）**：删除过时、价值较低的数据。

## 记忆类型

### 情景记忆（Episodic Memory）
包含具体事件及其背景信息的记忆：
```
"2026-02-17: Meeting with Anthony about TIM2 funding"
```

### 事实记忆（Factual Memory）
关于知识与事实的记忆：
```
"VitaDAO is a longevity-focused DAO"
```

### 程序性记忆（Procedural Memory）
关于操作步骤的记忆：
```
"How to run crypto check → perplexity → extract → memory"
```

### 偏好记忆（Preference Memory）
用户的个人选择或偏好：
```
"Prefers concise responses over detailed"
```

## 操作流程

### 存储（Store）
```json
{
  "type": "episodic|factual|procedural|preference",
  "content": "...",
  "context": {...},
  "importance": 0.9,
  "tags": ["topic", "people"],
  "timestamp": "2026-02-17T01:30:00Z"
}
```

### 检索（Retrieve）
- 通过相似性（语义搜索）
- 按时间顺序（情景记忆）
- 通过标签（索引查找）
- 按重要性排序（强化记忆）

### 整合（Consolidate）
- 合并相似的记忆
- 提取记忆中的模式
- 加强频繁被访问的记忆

### 遗忘（Decay）
- 自动删除过时的记忆

## 使用场景

```
"Remember that X"
"Learn: how to do X"
"I prefer X over Y"
"What do you know about X?"
"Forget about X"
```

## 集成机制

作为代理大脑的一部分，该模块与以下模块协同工作：
- **Gauge**：判断何时需要检索记忆。
- **Signal**：检测记忆之间的冲突。
- **Ritual**：存储常用的记忆快捷方式。

## 参数设置

- **遗忘率（Decay Rate）**：每月0.95
- **遗忘阈值（Threshold）**：0.1（低于此阈值的记忆将被删除）
- **整合频率（Consolidation Frequency）**：每日
- **最大情景记忆数量（Max Episodic Memory）**：1000条（超出此数量的记忆将被压缩）