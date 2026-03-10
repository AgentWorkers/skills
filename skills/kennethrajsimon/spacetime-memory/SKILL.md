---
name: spacetime-memory
description: 高性能的 SpacetimeDB 内存集成方案，专为 OpenClaw 设计。该方案将传统的静态文件存储方式替换为基于 WebAssembly 的高效内存管理系统，该系统运行在本地 SpacetimeDB 实例上，能够提供极快的数据访问速度。
acceptLicenseTerms: true
metadata:
  {
    "openclaw": {
      "emoji": "🧠"
    }
  }
---
# SpacetimeDB内存集成

本技能为OpenClaw提供了一个基于WebAssembly的低延迟内存系统，该系统通过[SpacetimeDB](https://spacetimedb.com/)实现。该系统可直接连接到本地运行的SpacetimeDB实例，用于存储和检索内存数据。

## 可用工具
- **stdb_store**：用于存储内存数据字符串以及可选的标签。
- **stdb_search**：用于查询本地内存数据。

## 架构
内存后端是一个编译为WebAssembly的SpacetimeDB模块，运行在`127.0.0.1:3001`端口（本地部署）。OpenClaw通过生成的SpacetimeDB TypeScript SDK使用WebSocket与数据库进行直接通信。

当您需要快速存储和检索结构化的长期内存数据时，请使用这些工具。