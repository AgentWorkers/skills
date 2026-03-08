# 技能操作符（PassDeck）

技能操作符（Skill Operator）是用于协作物理会话（collaborative agent sessions）的编排和管理引擎。它通过使用 Loro-CRDT（一种基于 CRDT 的数据结构）以及仅支持追加操作的日志架构（append-only log architecture），实现了高性能的数据持久化，确保数据不会丢失，并在所有代理（agents）之间保持一致。

## 💾 核心功能

### `team.create`
- **描述**: 在磁盘上初始化一个新的持久化协作物理会话。创建初始快照（snapshot）和元数据（metadata）。
- **参数**: `{ taskName: string }`
- **输出**: `{ sessionId: string, status: 'Persisted' }`

### `team.sync`
- **描述**: 将增量式的 CRDT 更新安全地追加到会话日志中。每次更新在持久化之前，都会使用来自源代理的 Ed25519 签名进行验证。
- **参数**: `{ sessionId: string, updatePayload: base64, publicKeyHex: string, signatureHex: string }`
- **输出**: `{ success: true, version: string }`

### `team.load`
- **描述**: 通过合并基础快照和增量更新日志来恢复协作物理会话的完整状态。提供了“防崩溃”的状态恢复机制。
- **参数**: `{ sessionId: string }`
- **输出**: `{ payload: base64, format: 'full-merged-snapshot' }`

## 🛡️ 主要特点
- **性能**: 增量同步性能达到 O(1) 级别。
- **容错性**: 通过快照（Snapshot）和预写日志（WAL, Write-Ahead Logging）技术实现即时崩溃恢复。
- **安全性**: 每次同步操作都内置了 Ed25519 签名验证机制。