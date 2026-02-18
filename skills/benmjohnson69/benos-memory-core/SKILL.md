---
name: benos-memory-core
description: >
  BenOS代理环境的核心运行时/易失性内存模块。  
  用途：用于在运行时存储和检索活动会话状态、开放循环（open loops）、决策结果以及临时笔记。
---
# BenOS 内存核心

**用途：**
- 为 BenOS 代理和子模块提供运行时/易失性内存的接口。
- 通过 `index.js` 命令或直接文件编辑来存储会话信息、未完成的操作（open loops）、决策记录以及备注。

**状态/存储位置：**
- 默认路径：`~/.openclaw/workspace/benos/runtime/state.json`
- 规范：也支持存储在 `benos/runtime/` 目录下的相关运行时和会话文件。

**使用方法：**
- 使用相应的技能命令（skill commands）进行代理控制的读写操作。
- 根据需要直接编辑文件以进行手动修复或数据迁移。

**数据结构（版本 1）：**
- `schemaVersion`：版本号
- `lastHydratedAt`：时间戳（ISO8601 格式）或 `null`
- `lastSessionRef`：会话引用字符串或 `null`
- `activeInitiatives`：当前正在进行的操作列表
- `openLoops`：未完成的操作列表
- `recentDecisions`：最近的决策记录列表
- `notes`：备注信息列表

**扩展性：**
- 可以通过添加新的数据结构版本或升级技能功能来扩展该内存核心的功能。