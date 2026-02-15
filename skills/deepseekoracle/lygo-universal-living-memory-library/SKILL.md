---
name: lygo-universal-living-memory-library
description: **Universal LYGO Living Memory Library升级版**：  
该升级版提供了严格、低噪声的内存索引管理功能（最多支持20个文件），支持对文件进行标记处理，并提供了审计与压缩工作流程，从而帮助用户通过LYGO-MINT工具保持数据的一致性并验证数据的完整性。该工具仅作为辅助工具使用，不具备控制功能。
---

# LYGO通用内存库（v1.1）

## 什么是LYGO通用内存库？
这是一个为LYGO系统设计的通用升级工具，用于构建一个简洁、可靠的内存管理库：
- 活动索引中最多可包含20个文件（占用较少的系统资源）
- 文件会被标记为“FRAGILE”以供手动审查
- 提供审计工作流程（用于检查文件完整性和变化情况）
- 支持压缩功能（确保数据传输的准确性）
- 通过LYGO-MINT哈希值和锚点来记录文件的来源和变更历史

该工具属于“纯辅助工具”类型：除非被明确调用，否则不会自动执行任何操作。

## 适用场景
- 当您需要确定哪些文件属于系统的核心组件时
- 对这些文件进行审计
- 将大量文件压缩成一个整洁的“主档案”
- 生成内存状态的快照并使用LYGO-MINT工具对其进行标记和记录

## 使用方法（复制/粘贴命令）
- “运行‘Living Memory Audit’（索引大小限制为20个文件），并报告文件的变更情况或脆弱性。”
- “使用LYGO通用内存库的规则将这些日志文件压缩成‘主档案’。”
- “使用LYGO-MINT工具对主档案进行处理，并生成相应的锚点信息。”

## 核心验证工具（安装地址）
- https://clawhub.ai/DeepSeekOracle/lygo-mint-verifier

## 参考资料
- `references/library_spec.md`（相关规则及文件角色说明）
- `references/core_files_index.json`（包含活跃文件的索引信息）
- `references/audit_protocol.md`（审计工作流程规范）
- `references/compression_protocol.md`（压缩算法说明）
- `references/seal_220cupdate_excerpt.md`（文件完整性检查说明）

## 相关脚本
- `scripts/audit_library.py`（用于对文件索引进行审计）
- `scripts/self_check.py`（用于检查文件结构的完整性）