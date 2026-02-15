---
name: agent-wal
description: "**Write-Ahead Log协议**：用于持久化代理状态数据。该协议可防止在对话数据被压缩过程中丢失用户的修改内容、决策信息以及相关上下文。适用场景包括：  
(1) 收到用户修改时：在响应之前先记录该修改；  
(2) 做出重要决策或进行分析时：在继续执行之前先记录下来；  
(3) 数据压缩前：将工作缓冲区中的数据刷新到WAL（Write-Ahead Log）文件中；  
(4) 会话开始时：重放未应用到数据库中的WAL记录以恢复丢失的上下文；  
(5) 任何需要确保数据在压缩过程中不被丢失的情况下。"
---

# Agent WAL（预写日志，Write-Ahead Log）

在响应用户请求之前，将重要的状态信息写入磁盘。这可以防止一种常见的代理故障：在数据压缩过程中丢失已进行的修改和上下文信息。

## 核心规则

**先写入数据，再响应用户请求。** 如果有需要记录的内容，务必先将其写入 WAL 文件中。

## 何时需要使用 WAL

| 触发条件 | 操作类型 | 例子 |
|---------|------------|---------|
| 用户对你进行了纠正 | `correction` | “不，应该使用 Podman 而不是 Docker” |
| 你做出了关键决策 | `decision` | “决定使用 CogVideoX-2B 进行文本转视频处理” |
| 重要的分析或结论 | `analysis` | “WAL/VFM 应该被视为基础设施的核心部分，而不仅仅是技能” |
| 状态发生变化 | `state_change` | “GPU 服务器的 SSH 密钥认证已配置完成” |
| 用户要求“记住这一点” | `correction` | 用户说的任何内容 |

## 命令

所有相关命令均通过 `scripts/wal.py` 文件执行（该文件位于当前技能目录下）：

```bash
# Write before responding
python3 scripts/wal.py append alexchen correction "Use Podman not Docker for all EvoClaw tooling"
python3 scripts/wal.py append alexchen decision "CogVideoX-5B with multi-GPU via accelerate"
python3 scripts/wal.py append alexchen analysis "Signed constraints prevent genome tampering"

# Working buffer (batch writes during conversation, flush before compaction)
python3 scripts/wal.py buffer-add alexchen decision "Some decision"
python3 scripts/wal.py flush-buffer alexchen

# Session start: replay lost context
python3 scripts/wal.py replay alexchen

# After applying a replayed entry
python3 scripts/wal.py mark-applied alexchen <entry_id>

# Maintenance
python3 scripts/wal.py status alexchen
python3 scripts/wal.py prune alexchen --keep 50
```

## 集成点

### 会话开始时
1. 运行 `replay` 命令以获取未应用的修改记录。
2. 将这些记录读取到当前的处理上下文中。
3. 在应用这些修改后，将它们标记为已应用的状态。

### 用户提出纠正时
1. 在响应用户之前，先运行 `append` 命令（操作类型为 `correction`）。
2. 然后根据用户的纠正内容进行相应的处理。

### 数据压缩前的刷新
1. 运行 `flush-buffer` 命令以持久化所有缓冲中的修改记录。
2. 接着像往常一样将数据写入每日存储文件中。

### 对话过程中
对于不太重要的信息，可以使用 `buffer-add` 命令进行批量写入。缓冲区中的数据会在 `flush-buffer` 命令执行时（即在数据压缩之前）或手动触发时被写入 WAL 文件中。

## 存储方式

WAL 文件：`~/clawd/memory/wal/<agent_id>.wal.jsonl`
缓冲文件：`~/clawd/memory/wal/<agent_id>.buffer.jsonl`

所有记录都采用只读写（append-only）的 JSONL 格式保存。每个记录的内容如下：
```json
{"id": "abc123", "timestamp": "ISO8601", "agent_id": "alexchen", "action_type": "correction", "payload": "Use Podman not Docker", "applied": false}
```