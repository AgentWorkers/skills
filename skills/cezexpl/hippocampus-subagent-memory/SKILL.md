---
name: hippocampus-subagent-memory
description: 在 OpenClaw 中，使用 Hippocampus 通过作用域 ID（scoped IDs）、有界合并回操作（bounded merge-back）以及显式的跨代理导入（explicit cross-agent imports）来隔离和协调子代理（sub-agent）的内存。
---
# Hippocampus 子代理内存管理

当 OpenClaw 创建需要独立内存的子代理时，可以使用此功能，以避免污染父代理的上下文。

## 使用场景

- 创建独立的子代理内存命名空间
- 防止子代理之间的内存泄漏
- 仅向父代理返回有限范围的数据或结果
- 协调子代理与父代理之间的数据导入/导出操作

## 推荐流程

1. 为子代理生成一个具有唯一标识符（`HIPOKAMP_SUBAGENT_ID`）的实例。
2. 确保子代理仅在其自己的内存命名空间内进行数据操作。
3. 在任务执行完成后，向父代理返回一个包含有限范围数据的结果包。
4. 仅允许经过明确授权的数据被导入到父代理中。

## 使用指南

- 默认情况下，子代理的内存应保持隔离状态，不应与父代理的内存混合。
- 尽量使用数据摘要、结果文件或引用，而非完整的数据副本。
- 为子代理的内存添加会话信息和与父代理的关联元数据。
- 父代理应在门户中完成一次初始化设置；子代理应自动继承相应的权限范围，无需单独登录门户。

## 相关组件

- `hippocampus-memory-core`：负责核心内存管理功能
- `hippocampus-openclaw-onboarding`：用于配置子代理的初始设置
- `@hippocampus/openclaw-context-engine`：提供子代理生命周期管理的自动化钩子（如创建/销毁）