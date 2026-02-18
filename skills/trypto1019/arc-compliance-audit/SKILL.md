---
name: compliance-audit
description: **自主代理操作的不可篡改审计追踪**：记录技能执行情况、数据访问行为、决策过程以及预算变更，所有记录均附有防篡改的哈希值。这对于企业治理、事件响应和信任验证至关重要。
user-invocable: true
metadata: {"openclaw": {"emoji": "📋", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 合规性审计追踪

为自主代理提供不可篡改、具有防篡改功能的审计日志记录。每个操作都会生成一个哈希链条记录，其完整性可被验证。

## 设计目的

自主代理在无需人工监督的情况下进行决策、执行任务、访问数据以及支出资金。当出现问题时，需要准确了解具体发生了什么。现有的代理框架缺乏标准的审计追踪机制，而本功能正是为填补这一空白而设计的。

## 命令

### 记录操作
```bash
python3 {baseDir}/scripts/audit.py log --action "skill_executed" --details '{"skill": "scanner", "target": "some-skill", "result": "clean"}'
```

### 记录决策
```bash
python3 {baseDir}/scripts/audit.py log --action "decision" --details '{"choice": "deploy v2", "reason": "all tests passed", "alternatives_considered": ["rollback", "hotfix"]}'
```

### 记录数据访问
```bash
python3 {baseDir}/scripts/audit.py log --action "data_access" --details '{"resource": "api_key", "purpose": "moltbook_post", "accessor": "ghost_agent"}'
```

### 记录预算变更
```bash
python3 {baseDir}/scripts/audit.py log --action "budget_change" --details '{"amount": -10.00, "merchant": "namecheap", "reason": "domain purchase", "balance_after": 190.00}'
```

### 查看最近的操作记录
```bash
python3 {baseDir}/scripts/audit.py view --last 20
```

### 按操作类型查看记录
```bash
python3 {baseDir}/scripts/audit.py view --action skill_executed
```

### 在指定时间范围内查看记录
```bash
python3 {baseDir}/scripts/audit.py view --since "2026-02-15T00:00:00" --until "2026-02-16T00:00:00"
```

### 验证审计追踪的完整性
```bash
python3 {baseDir}/scripts/audit.py verify
```

### 导出审计追踪记录
```bash
python3 {baseDir}/scripts/audit.py export --format json > audit-export.json
python3 {baseDir}/scripts/audit.py export --format csv > audit-export.csv
```

### 生成合规性摘要
```bash
python3 {baseDir}/scripts/audit.py summary --period day
```

## 记录格式

每条审计记录包含以下内容：
- **时间戳** — ISO 8601 格式，UTC 时区
- **操作类型** — 执行的操作（如执行技能、做出决策、访问数据、修改预算、发生错误或自定义操作）
- **代理** — 执行操作的代理
- **详细信息** — 包含操作相关数据的结构化 JSON 数据
- **哈希值** — 前一条记录的哈希值与当前记录数据的 SHA-256 哈希值拼接而成（用于防篡改）
- **序列号** — 递增的序列编号

## 完整性验证

审计追踪采用哈希链技术：每条记录都包含前一条记录哈希值的 SHA-256 哈希值以及当前记录的数据。如果任何记录被修改或删除，哈希链将会断裂，`verify` 命令会指出篡改的具体位置。

## 存储方式

审计日志以每日 JSON 文件的形式存储在 `~/.openclaw/audit/` 目录下（文件名为 `audit-YYYY-MM-DD.json`）。这种方式既保证了每个文件的体积较小，又保留了完整的审计历史记录。

## 使用场景

- **事件响应**：在错误发生前的 5 分钟内发生了什么？
- **预算透明度**：展示每一笔支出的详细情况及其原因
- **信任验证**：证明代理未被入侵
- **企业合规性**：满足自主系统的审计要求
- **故障排查**：追踪导致意外结果的决策流程