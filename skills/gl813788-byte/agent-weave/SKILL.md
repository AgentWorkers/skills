---
name: agent-weave
description: 主-工作节点代理集群（Master-Worker Agent Cluster）用于并行任务执行。适用于构建需要并行处理的分布式代理系统、任务编排系统或基于MapReduce的工作流程。
---
# Agent-Weave

这是一个基于Master-Worker架构的代理集群解决方案，支持任务的并行执行以及安全的父子级通信。

## 适用场景

当您需要以下功能时，可以使用Agent-Weave：
- 构建具有并行处理能力的分布式代理系统
- 协调多个代理的协同工作
- 实现类似MapReduce的工作流程
- 在多个工作代理之间扩展任务执行能力
- 设计Master-Worker架构的应用程序

## 快速入门

### 安装

```bash
npm install agent-weave
```

### 基本用法

```javascript
const { Loom } = require('agent-weave');

// Create cluster
const loom = new Loom();
const master = loom.createMaster('my-cluster');

// Create workers
const workers = loom.spawnWorkers(master.id, 5, async (data) => {
  // Process data
  return { result: data * 2 };
});

// Execute tasks
const results = await master.dispatch([1, 2, 3, 4, 5]);
console.log(results);
```

## 命令行接口（CLI）命令

```bash
# Create master
weave loom create-master --name my-cluster

# Spawn workers
weave loom spawn --parent <master-id> --count 5

# List agents
weave loom list --tree
```

## 主要特性

- **Master-Worker架构**：负责管理和协调多个工作代理
- **并行执行**：将任务分配给各个工作代理执行
- **安全通信**：确保父代理与子代理之间的通信安全
- **MapReduce支持**：内置MapReduce工作流程
- **自动扩展**：动态管理工作代理的数量
- **事件驱动**：基于事件驱动的通信机制

## API参考

### Loom
用于创建和管理代理的工厂类。

### Master
负责管理整个代理集群。

### Worker
执行由Master分配的任务。

### Thread
提供代理之间的安全通信层。

### Tapestry
用于协调MapReduce工作流程的引擎。

## 许可证

MIT许可证