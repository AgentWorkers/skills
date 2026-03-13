# AaronDB Edge 技能

这是一个专为自主代理（sovereign agents）设计的高性能、分布式 Datalog 引擎。

## 前言

```yaml
name: aarondb-edge
description: Distributed Datalog engine for sovereign agents. Enables persistent fact management and reasoning.
version: 1.1.0
author: criticalinsight
repository: https://github.com/criticalinsight/aarondb-edge
npm: https://www.npmjs.com/package/@criticalinsight/aarondb-edge
requirements:
  - "@criticalinsight/aarondb-edge"
```

## 描述

该技能使 AI 代理能够使用本地或分布式 Datalog 引擎来存储、检索和推理数据。它遵循“数据库即价值（Database as a Value）”的理念，支持不可变的状态管理以及基于时间线的调试功能。

## 安装

要使用此技能，请确保您的代理运行时环境中已安装了核心包：

```bash
npm install @criticalinsight/aarondb-edge
```

## 使用方法

### 1. 初始化

```javascript
import { AaronDB } from '@criticalinsight/aarondb-edge';

// Initialize a new database instance
const db = new AaronDB();
```

### 2. 数据操作

数据以“datoms”（实体、属性、值）的形式进行存储。

```javascript
await db.transact([
  { e: "agent/philosophy", a: "type", v: "RichHickey" },
  { e: "agent/philosophy", a: "principle", v: "Simplicity" }
]);
```

### 3. 查询

使用 Datalog 语法进行查询，并支持变量绑定。

```javascript
const results = db.query({
  where: [
    ["?e", "type", "RichHickey"],
    ["?e", "principle", "?p"]
  ]
});
```

## 架构模式

- **数据库即价值（Database as a Value）**：始终将数据库状态视为不可变的值。避免在 `transact` 流程之外手动修改状态。
- **共享发现层（Shared Discovery Layer）**：在 Cloudflare Worker 模式下，数据可以通过共享的 D1/KV 后端在各个代理之间同步。在库模式（library mode）下，数据状态优先保存在本地，但也可以导出/导入为统一的数据日志，以实现跨代理协作。