---
name: warden-governance
version: 1.0.0
author: AN2B Technologies
license: MIT
category: governance
clawhub: an2b/warden-governance
hooks:
  - before_action
  - after_action
  - on_error
config:
  SENTINEL_API_KEY:
    required: false
    description: Sentinel_OS API key for enterprise governance
  ENGRAMPORT_API_KEY:
    required: false
    description: EngramPort API key for enterprise memory
  WARDEN_FAIL_OPEN:
    required: false
    default: "false"
    description: Allow actions when governance engine fails
  WARDEN_AGENT_ID:
    required: false
    default: openclaw-agent
    description: Bot identifier for audit trail
  WARDEN_POLICY_FILE:
    required: false
    description: Path to custom YAML policy file
  WARDEN_POLICY_PACKS:
    required: false
    description: Comma-separated built-in policy pack names
install: openclaw skill install an2b/warden-governance
---

# War/Den 管理技能

> **ClawHub 包名:** `an2b/warden-governance`
> **版本:** 1.0.0
> **类别:** 管理与安全
> **许可证:** MIT

---

## 该技能的功能

OpenClaw 机器人尝试执行的每一个操作，在执行前都会由 War/Den 系统进行评估。

```plaintext
你的机器人 -> War/Den 系统检查 -> 允许执行 -> 操作被执行
                          -> 拒绝执行 -> 操作被阻止并记录日志
                          -> 提交审核 -> 等待你的批准
```

再也不会有邮件被删除，再也不会有数据被泄露，再也不会有不受控制的机器人行为出现。

**社区模式完全不依赖外部服务。** 无需 API 密钥，也不需要使用云服务。
只需 YAML 配置文件、本地的 SQLite 日志记录以及可验证的哈希链即可。

---

## 安装

### 通过 ClawHub 安装（推荐）

```bash
openclaw skill install an2b/warden-governance
```

### 通过 pip 安装

```bash
pip install warden-governance-skill
```

两种安装方式都会将技能安装到：`~/.openclaw/skills/warden-governance/` 目录下。

安装成功后，你会看到如下提示：

```plaintext
🦞 War/Den 管理功能已启用。
   你的 OpenClaw 机器人现在受到管理了。
```

### 添加到 OpenClaw 配置文件中

```yaml
skills:
  - name: warden-governance
    config:
      SENTINEL_API_KEY: ""       # 可选 -- 社区模式时留空
      ENGRAMPORT_API_KEY: ""     # 可选 -- 本地内存模式时留空
      WARDEN_FAIL_OPEN: "false"  # 管理失败时阻止操作（默认值）
```

### 重启机器人

```bash
openclaw restart
```

就这样，你的机器人现在已经被有效管理了。

---

## 工作原理

### 钩子（Hooks）

该技能注册了三个 OpenClaw 钩子：

| 钩子 | 功能 |
|------|---------|
| `before_action` | 在执行操作前根据策略进行评估 |
| `after_action` | 将操作结果写入受管理的内存 |
| `on_error` | 将错误记录到防篡改的审计日志中 |

### 操作桥接（Action Bridge）

OpenClaw 的所有 15 种操作类型都会与 War/Den 的管理规则进行匹配：

| OpenClaw 操作 | War/Den 操作类型 | 默认保护措施 |
|-----------------|--------------|-------------------|
| `email.send` | `message.send` | 被监控 |
| `email.delete` | `data.write` | **需要人工审核** |
| `email.read` | `data.read` | 被监控 |
| `file.write` | `data.write` | 被监控 |
| `file.delete` | `data.write` | **需要人工审核** |
| `file.read` | `data.read` | 被监控 |
| `browser.navigate` | `api.call` | 被监控 |
| `browser.click` | `api.call` | 被监控 |
| `shell.execute` | `code.execute` | **在生产环境中被阻止** |
| `api.call` | `api.call` | 被监控 |
| `calendar.create` | `data.write` | 被监控 |
| `calendar.delete` | `data.write` | **需要人工审核** |
| `message.send` | `message.send` | 被监控 |
| `code.execute` | `code.execute` | **在生产环境中被阻止** |
| `payment.create` | `api.call` | **需要人工审核** |

### 策略引擎

策略文件采用 YAML 格式，按优先级顺序进行评估：

```yaml
policies:
  - name: protect-email-delete
    match:
      action.type: data.write
      action.data.openclaw_original: email.delete
    decision: review
    mode: enforce
    priority: 1
    active: true
    reason: "删除邮件需要人工审核。"
```

**评估规则：**
1. 仅筛选有效的策略。
2. 按优先级升序排序（数字越小，优先级越高）。
3. 首个匹配的策略优先执行。
4. `mode: monitor`：仅记录日志并允许操作继续。
5. `mode: enforce`：执行匹配的策略决策。
6. 无匹配规则时：默认允许操作。

### 预置策略包

可以使用内置的策略包立即启用管理功能：

| 包名 | 功能 |
|------|-------------|
| `basic_safety` | 在生产环境中阻止代码执行，监控写入操作和 API 调用 |
| `phi_guard` | 在开发环境中拒绝访问敏感信息（PHI），数据导出前需要人工审核 |
| `payments_guard` | 在开发环境中拒绝支付操作，在生产环境中需要人工审核 |

### 审计日志

所有的管理决策都会被记录到一个防篡改的 SHA-256 哈希链中：

```plaintext
事件 N:  hash = SHA256(prev_hash + agent_id + action_type + decision + timestamp)
事件 N+1: prev_hash = Event N 的哈希值 |
```

你可以随时验证这个哈希链：

```python
valid, bad_event_id = audit_log.verify_chain()
```

### 决策缓存

允许的操作决策会被缓存 5 分钟（可配置）。拒绝和需要审核的操作决策**永远不会**被缓存——它们总是会直接发送到管理引擎进行处理。

---

## 社区模式与企业模式

| 功能 | 社区模式（免费） | 企业模式 |
|---------|-----------------|------------|
| 策略执行 | 本地 YAML 配置 | Sentinel_OS 云服务 |
| 审计日志 | 本地 SQLite 日志 + 哈希链 | 云服务 + 签名的 PDF 文件 |
| 内存存储 | 本地 SQLite | EngramPort 云服务（MandelDB） |
| 内存搜索 | 文本搜索 | 向量搜索（3072 维度） |
| 合成能力 | 基本检索 | Eidetic AI 合成技术 |
| 跨机器人通信 | 不支持 | 支持多机器人协同 |
| 多命名空间 | 最多 3 个命名空间 | 无限制 |
| 合规性报告 | 不支持 | SOC2/HIPAA 标准的 PDF 报告 |
| 加密溯源 | 本地哈希链 | AEGIS（SHA-256 + RSA） |
| 依赖项 | **无** | 需要 `sentinel-client` 和 `engramport-langchain` |

### 模式切换

| `SENTINEL_API_KEY` | `ENGRAMPORT_API_KEY` | 模式 |
|--------------------|----------------------|------|
| -- | -- | 完整的社区模式 |
| 设置 | -- | 受管理的社区模式 |
| 设置 | 设置 | 企业模式 |
| 设置 | 设置 | 完整的企业模式 |

所有模式的切换都不需要修改任何代码，只需调整环境变量即可。

---

## 企业升级路径

### Sentinel_OS（管理升级）

设置 `SENTINEL_API_KEY` 即可将管理功能从本地 YAML 配置升级到 Sentinel_OS 云服务：

- 通过 `/api/v1/check` 实时评估策略。
- 通过 `/api/v1/check` 进行预检查（仅读，无副作用）。
- 通过 `/api/v1/ingest` 记录操作日志，并确保哈希链的完整性。
- 支持管理功能、警报系统以及基于 AI 的分析功能。
- 提供 Python 和 Node.js SDK。
- 每个 API 密钥的检测频率限制：每分钟 2000 次检查，每分钟最多 1000 次操作记录。

获取密钥请访问 [getsentinelos.com](https://getsentinelos.com)。

### EngramPort（通过 MandelDB 管理内存）

设置 `ENGRAMPORT_API_KEY` 即可将内存管理功能从本地 SQLite 升级到 EngramPort 云服务：

- 提供五个 API 端点：`/register`、`/remember`、`/recall`、`/reflect`、`/stats`。
- 支持 3072 维度的 OpenAI 嵌入模型（Pinecone）。
- 使用 AEGIS 技术实现加密溯源（SHA-256 + RSA 签名）。
- 支持命名空间隔离的存储（格式：`bot:{slug}:{uid}`）。
- 支持使用 GPT-4o-mini 进行跨机器人信息合成。
- 支持 `EngramPortOrchestra` 进行多机器人协同。
- 支持 `DreamState` 进行后台合成。

API 密钥的格式为 `ek_bot_*`，数据存储采用 SHA-256 哈希技术。

获取密钥请访问 [engram.eideticlab.com](https://engram.eideticlab.com)。

---

## 配置参数

| 参数 | 是否必填 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `SENTINEL_API_KEY` | 否 | `""` | Sentinel_OS 密钥（社区模式使用） |
| `ENGRAMPORT_API_KEY` | 否 | `""` | EngramPort 密钥（本地内存模式使用） |
| `WARDEN_FAIL_OPEN` | 否 | `false` | 管理失败时是否允许操作继续 |
| `WARDEN_AGENT_ID` | 否 | `openclaw-agent` | 机器人标识符 |
| `WARDEN_POLICY_FILE` | 否 | 内置策略文件路径 |
| `WARDEN_POLICY_PACKS` | 否 | 策略包名称（逗号分隔） |
| `WARDEN_MEMORY_DB` | 否 | `~/.warden/memory.db` | 本地内存存储路径 |
| `WARDEN_AUDIT_DB` | 否 | `~/.warden/audit.db` | 本地审计日志路径 |
| `WARDEN_CACHE_TTL` | 否 | `300` | 缓存时长（秒） |

### 管理失败时的行为

- 如果 `WARDEN_FAIL_OPEN` 设置为 `false`，管理失败时操作会被阻止。
- 如果设置为 `true`，操作会被允许执行，但会触发警告。

默认值为 `false`，因为管理失败时不应默默允许危险操作的发生。

---

## 测试说明

该技能附带了全面的测试套件。运行测试如下：

```bash
python -m pytest tests/
```

关键测试：**Meta inbox 测试** 模拟了一个 OpenClaw 机器人删除 200 封邮件的场景。在 War/Den 管理机制下，所有邮件都会被阻止：

```python
def test_meta_researcher_inbox_protection(self, tmp_path):
    """模拟 Meta inbox 情景，所有 200 封邮件都被阻止。"""
    skill = _make_skill(tmp_path, WARDEN_POLICY_FILE=policy_path)
    blocked = 0
    for i in range(200):
        result = skill.before_action(
            {"type": "email.delete", "data": {"email_id": f"msg_{i}"},
            {"agent_id": "meta-researcher-bot", "env": "prod"},
        )
        if not result["proceed":
            blocked += 1
    assert blocked == 200
```

---

## 技能文件结构

```plaintext
warden-governance-skill/
├── SKILL.md                          | 主要配置文件（ClawHub 存储）
├── clawhub.json                      | ClawHub 注册元数据
├── README.md                         | 完整的文档说明
├── pyproject.toml                    | Python 包配置文件
├── policies/
│   ├── openclaw_default.yaml         | 默认管理策略
│   └── policy_packs.py              | 预置策略包
├── warden_governance/
│   ├── __init__.py                      | 主要类文件
│   ├── skill.py                      | 技能核心逻辑
│   ├── action_bridge.py              | 操作桥接逻辑
│   ├── policy_engine.py              | 策略引擎
│   ├── audit_log.py                  | 审计日志逻辑
│   ├── memory_client.py              | 内存管理逻辑
│   ├── local_store.py                | 本地存储逻辑
│   ├── sentinel_client.py            | Sentinel_OS 客户端
│   ├── engramport_client.py          | EngramPort 客户端
│   ├── upgrade_manager.py            | 模式检测与提示功能
│   ├── health_check.py               | 系统健康检查
│   └── settings.py                   | 配置参数
└── tests/
    ├── __init__.py                  | 测试脚本
    ├── test_skill.py                 | 技能功能测试
    ├── test_policy_engine.py         | 策略引擎测试
    ├── test_audit_log.py             | 审计日志测试
    ├── test_action_bridge.py         | 操作桥接测试
    ├── test_memory.py                | 内存管理测试
    └── test_enterprise.py            | 企业模式升级测试
```

---

该技能基于 [Sentinel_OS](https://getsentinelos.com) 和 [EngramPort](https://engram.eideticlab.com) 开发，由 [AN2B Technologies](https://an2b.com) 提供。

*龙虾保护着我们的收件箱。*