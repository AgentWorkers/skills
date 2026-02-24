# 代理审计追踪功能

为AI代理提供防篡改的、基于哈希链的审计日志记录功能，符合欧盟AI法案的要求。

## 为何需要此功能

AI代理会代表您执行操作。自2026年8月2日起，欧盟AI法案要求AI系统必须自动记录操作日志、确保日志记录的防篡改性，并具备人工监督机制。本功能可同时满足这三项要求，且完全无需依赖任何外部库或服务。

## 快速入门

### 1. 将该功能添加到代理的工作空间中

```bash
cp scripts/auditlog.py /path/to/your/workspace/scripts/
chmod +x /path/to/your/workspace/scripts/auditlog.py
```

### 2. 记录操作

```bash
./scripts/auditlog.py append \
  --kind "file-write" \
  --summary "Created config.yaml" \
  --target "config.yaml" \
  --domain "personal"
```

### 3. 验证日志完整性

```bash
./scripts/auditlog.py verify
# Output: OK (N entries verified)
```

## 合规性说明

| 欧盟AI法案条款 | 要求 | 本功能如何帮助满足这些要求 |
|-------------------|-------------|---------------------|
| **第12条** 日志记录 | 自动记录事件 | 所有操作都会附带时间戳、执行者信息及操作目标 |
| **第12条** 日志完整性 | 防篡改的日志记录 | 采用SHA-256哈希链技术，任何修改都会破坏日志链的连续性 |
| **第14条** 人工监督 | 人工审批机制 | `--gate` 标志可将操作与人工审批记录关联起来 |
| **第50条** 透明度 | 可审计的日志记录 | 日志以人类可读的NDJSON格式存储，支持一键验证 |
| **第12条** 可追溯性 | 日志的顺序性 | 日志条目按照时间顺序排列 |

## 日志事件类型

使用以下标准化事件类型来确保审计记录的一致性：

| 事件类型 | 使用场景 |
|------|------------|
| `file-write` | 代理创建或修改文件 |
| `exec` | 代理执行命令 |
| `api-call` | 与外部API进行交互 |
| `decision` | AI做出决策或提出建议 |
| `credential-access` | 访问机密信息或凭证 |
| `external-write` | 代理向外部系统写入数据 |
| `human-override` | 人工覆盖AI的决策 |
| `disclosure` | 向用户披露AI的决策内容 |

## 完整文档

请参阅[README.md](README.md)，以获取完整的使用说明、集成示例、安全模型以及欧盟AI法案合规性指南。

## 日志格式

```json
{
  "ts": "2026-02-24T07:15:00+00:00",
  "kind": "exec",
  "actor": "atlas",
  "domain": "ops",
  "plane": "action",
  "target": "pg_dump production",
  "summary": "Ran database backup",
  "gate": "approval-123",
  "ord": 42,
  "chain": {"prev": "abc...", "hash": "def...", "algo": "sha256(prev\\nline_c14n)"}
}
```

## 与OpenClaw的集成方式

请将以下代码添加到`HEARTBEAT.md`文件中：

```markdown
## Audit integrity check
- Run: `./scripts/auditlog.py verify`
  - If fails: alert with line number + hash mismatch
  - If OK: silent
```

## 系统要求

- Python 3.9及以上版本（无外部依赖）
- MIT许可证

---

本功能由[Roosch](https://github.com/roosch269)和[Atlas](https://github.com/roosch269/agent-audit-trail)共同开发。