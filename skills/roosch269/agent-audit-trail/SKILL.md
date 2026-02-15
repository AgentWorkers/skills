# 代理审计追踪功能

为AI代理提供防篡改的、基于哈希链的审计日志记录功能。

## 为什么需要这个功能？

代理会代表您执行操作。您需要知道它们具体做了什么、何时执行的，以及事后能够证明没有任何内容被篡改。

该功能提供以下特性：
- **只允许追加的NDJSON日志**——便于人类阅读和通过grep工具搜索
- **哈希链机制**——每条日志记录都包含前一条日志的SHA-256哈希值和当前日志的哈希值，从而能够检测到篡改行为
- **单调顺序**——与门控操作相关的事件会按照时间顺序进行记录
- **完整性验证**——通过一个命令即可验证整个日志链的完整性

## 快速入门

### 1. 将脚本添加到代理的工作空间中

将`scripts/auditlog.py`文件复制到代理工作空间的`scripts/`目录中。

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

### 3. 验证日志链的完整性

```bash
./scripts/auditlog.py verify
# Output: OK (or error with line number if tampered)
```

## 使用方法

### 添加日志记录

```bash
./scripts/auditlog.py append \
  --kind <event-type> \
  --summary <description> \
  [--domain <domain>] \
  [--target <identifier>] \
  [--gate <gate-reference>] \
  [--provenance '{"source": "...", "channel": "..."}'] \
  [--details '{"key": "value"}']
```

**必需参数：**
- `--kind`：事件类型（例如：`file-write`、`exec`、`api-call`、`credential-access`）
- `--summary`：便于人类阅读的描述性文本

**可选参数：**
- `--domain`：逻辑域（默认值：`unknown`）
- `--target`：操作的目标对象（文件路径、URL或命令）
- `--gate`：需要审批的操作的引用（仅适用于需要审批的操作）
- `--provenance`：包含来源信息的JSON对象
- `--details`：包含额外结构化数据的JSON对象

### 验证日志链的完整性

```bash
./scripts/auditlog.py verify [--log path/to/audit.ndjson]
```

如果验证通过，程序会返回退出码0并显示“OK”；否则会显示出出错的行号及哈希值不匹配的详细信息。

## 日志格式

每条日志记录都是一个JSON对象：

```json
{
  "ts": "2026-02-05T07:15:00+00:00",
  "kind": "file-write",
  "actor": "atlas",
  "domain": "personal",
  "plane": "action",
  "target": "config.yaml",
  "summary": "Created config.yaml",
  "ord": 42,
  "chain": {
    "prev": "abc123...",
    "hash": "def456...",
    "algo": "sha256(prev\nline_c14n)"
  }
}
```

### 日志字段说明

| 字段          | 描述                                      |
|---------------|-----------------------------------------|
| `ts`           | 带有时区偏移的ISO-8601时间戳                         |
| `kind`          | 事件类型                                      |
| `actor`         | 执行操作的用户或代理名称                             |
| `domain`         | 用于分类的逻辑域                             |
| `plane`          | 日志处理的执行环境（通常为“action”）                     |
| `target`         | 操作的目标对象                               |
| `summary`        | 人类可读的描述性文本                             |
| `gate`          | 需要审批的操作的引用                             |
| `provenance`      | 包含来源信息的JSON对象                         |
| `ord`          | 用于保证日志顺序的标识符                         |
| `chain`          | 基于哈希值的日志链数据                             |

## 与OpenClaw的集成

### 心跳检测（Heartbeat验证）

在`HEARTBEAT.md`文件中添加相应的代码：

```markdown
## Audit integrity check
- Run: `./scripts/auditlog.py verify`
  - If fails: alert with line number + hash mismatch
  - If OK: silent
```

### 需要审批的操作

对于需要人工审批的操作，请在日志中包含审批的引用：

```bash
./scripts/auditlog.py append \
  --kind "external-write" \
  --summary "Posted to Twitter" \
  --gate "approval-2026-02-05-001" \
  --target "https://x.com/status/123" \
  --provenance '{"channel": "telegram", "message_id": "456"}'
```

## 安全模型

1. **只允许追加日志**：该脚本仅用于添加新日志，从不修改现有日志记录。
2. **哈希链机制**：每条日志的哈希值依赖于所有之前的日志记录。
3. **篡改检测**：任何修改都会破坏日志链的完整性。
4. **文件锁定**：使用`fcntl.LOCK_EX`实现安全的并发访问控制。

### 该功能的局限性

- 无法防止root/admin权限的攻击者篡改所有日志。
- 如果代理被入侵，攻击者仍可能在日志中伪造记录。
- 日志可能被删除（建议使用异地备份机制）。

该功能主要用于提供审计证据，而非防止篡改行为。它只能检测到篡改行为，但不能完全阻止篡改。

## 配置设置

默认日志路径：`audit/atlas-actions.ndjson`

您可以使用`--log`参数自定义日志路径：

```bash
./scripts/auditlog.py --log path/to/my-audit.ndjson append --kind test --summary "Test entry"
```

## 系统要求

- Python 3.9及以上版本（用于`zoneinfo`模块）
- 无需依赖任何外部库

## 设计理念

“信任，但要进行验证。”——通过这个功能，我们可以确保代理的行为可以被审计。

代理应当对其操作负责，而这个功能使得这种责任机制可以被追踪和验证。

## 许可证

采用MIT许可证——可自由使用；如果您对该功能进行了改进，请贡献代码。

## 贡献方式

如有问题或想要提交Pull Request，请访问：https://github.com/roosch/agent-audit-trail