---
name: black-box
description: 不可篡改的审计日志，用于记录代理操作，这些日志存储在 TiDB Zero 中。
metadata:
  openclaw:
    emoji: 📦
    requires:
      bins: ["python3", "curl"]
      env: ["TIDB_HOST", "TIDB_PORT", "TIDB_USER", "TIDB_PASSWORD"]
---
# Black Box（由 TiDB Zero 提供支持）

## 概述
**Black Box** 是一个专为 AI 代理设计的、不可破坏的审计日志系统。它充当“飞行数据记录器”的角色，实时将关键操作、错误信息以及推理过程流式传输到持久化的云数据库（TiDB Zero）中。

## 安全性与配置
1. **推荐使用自定义数据库：** 设置 `TIDB_*` 环境变量。
2. **自动配置（备用方案）：** 如果未找到凭据，该工具会使用 TiDB Zero API 创建一个临时数据库用于日志记录。连接字符串会缓存在 `~/.openclaw_black_box_dsn` 文件中。

## 为什么使用它？
*   **容错能力：** 容器崩溃时，本地日志会丢失，但云端的日志会保留下来。
*   **审计追踪：** 可以准确记录代理的具体操作及其原因（符合合规性要求）。
*   **调试：** 可以检索导致故障之前的最后 100 条操作记录。

## 先决条件
*   **TiDB 凭据：** 标准的 MySQL 连接参数（`TIDB_HOST`、`TIDB_USER` 等）。
* **网络连接：** 需要能够访问 TiDB Cloud（端口 4000）。

## 使用方法

### 1. 记录事件
记录关键操作或错误信息：

```bash
python {baseDir}/run.py --action log --level ERROR --message "System crash imminent: Memory leak detected"
```

### 2. 读取日志
检索最近 N 条日志（默认值：10 条）：

```bash
python {baseDir}/run.py --action read --limit 20
```

## 数据表结构
该工具会创建一个名为 `agent_logs` 的表格，包含以下列：`timestamp`（时间戳）、`level`（日志级别）、`message`（日志内容）以及 `metadata`（JSON 格式的元数据）。