# hopeIDS 安全技能

基于推理的入侵检测系统，适用于 AI 代理，并提供隔离机制和人工干预功能。

## 安全不变量

以下是**不可协商的**设计原则：

1. **阻止 = 完全终止** — 被阻止的消息永远不会到达 jasper-recall 或代理。
2. **仅存储元数据** — 任何原始恶意内容都不会被存储。
3. **批准 ≠ 重新注入** — 批准会改变未来的行为，但不会恢复被阻止的消息。
4. **警报是程序化的** — Telegram 警报基于元数据生成，不涉及大型语言模型（LLM）。

---

## 功能

- **自动扫描** — 在代理处理之前扫描消息。
- **隔离** — 仅通过存储元数据来阻止威胁。
- **人工干预** — 通过 Telegram 发送警报以供审核。
- **针对每个代理的配置** — 不同代理可以设置不同的阈值。
- **命令**：`/approve`、`/reject`、`/trust`、`/quarantine`。

---

## 工作流程

```
Message arrives
    ↓
hopeIDS.autoScan()
    ↓
┌─────────────────────────────────────────┐
│  risk >= threshold?                     │
│                                         │
│  BLOCK (strictMode):                    │
│     → Create QuarantineRecord           │
│     → Send Telegram alert               │
│     → ABORT (no recall, no agent)       │
│                                         │
│  WARN (non-strict):                     │
│     → Inject <security-alert>           │
│     → Continue to jasper-recall         │
│     → Continue to agent                 │
│                                         │
│  ALLOW:                                 │
│     → Continue normally                 │
└─────────────────────────────────────────┘
```

---

## 配置

```json
{
  "plugins": {
    "entries": {
      "hopeids": {
        "enabled": true,
        "config": {
          "autoScan": true,
          "defaultRiskThreshold": 0.7,
          "strictMode": false,
          "telegramAlerts": true,
          "agents": {
            "moltbook-scanner": {
              "strictMode": true,
              "riskThreshold": 0.7
            },
            "main": {
              "strictMode": false,
              "riskThreshold": 0.8
            }
          }
        }
      }
    }
  }
}
```

### 选项

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `autoScan` | 布尔值 | `false` | 自动扫描每条消息 |
| `strictMode` | 布尔值 | `false` | 遇到威胁时直接阻止（而非仅警告） |
| `defaultRiskThreshold` | 数值 | `0.7` | 触发操作的风险等级 |
| `telegramAlerts` | 布尔值 | `true` | 对被阻止的消息发送警报 |
| `telegramChatId` | 字符串 | - | 警报发送目标 |
| `quarantineDir` | 字符串 | `~/.openclaw/quarantine/hopeids` | 存储路径 |
| `agents` | 对象 | - | 为每个代理设置自定义配置 |
| `trustOwners` | 布尔值 | `true` | 跳过对发送者消息的扫描 |

---

## 存储隔离记录

当一条消息被阻止时，会创建一个元数据记录：

```json
{
  "id": "q-7f3a2b",
  "ts": "2026-02-06T00:48:00Z",
  "agent": "moltbook-scanner",
  "source": "moltbook",
  "senderId": "@sus_user",
  "intent": "instruction_override",
  "risk": 0.85,
  "patterns": [
    "matched regex: ignore.*instructions",
    "matched keyword: api key"
  ],
  "contentHash": "ab12cd34...",
  "status": "pending"
}
```

**注意：** 没有 `originalMessage` 字段。这是有意为之。

---

## Telegram 警报

当一条消息被阻止时：

```
🛑 Message blocked

ID: `q-7f3a2b`
Agent: moltbook-scanner
Source: moltbook
Sender: @sus_user
Intent: instruction_override (85%)

Patterns:
• matched regex: ignore.*instructions
• matched keyword: api key

`/approve q-7f3a2b`
`/reject q-7f3a2b`
`/trust @sus_user`
```

警报仅基于元数据生成，不涉及任何大型语言模型（LLM）。

---

## 命令

### `/quarantine [all|clean]`

列出所有被隔离的记录。

```
/quarantine        # List pending
/quarantine all    # List all (including resolved)
/quarantine clean  # Clean expired records
```

### `/approve <id>`

将一条被阻止的消息标记为误报。

```
/approve q-7f3a2b
```

**效果：**
- 状态变为 `approved`（已批准）。
- （未来）将发送者添加到允许列表。
- （未来）降低该模式的权重。

### `/reject <id>`

确认被阻止的消息是真实威胁。

```
/reject q-7f3a2b
```

**效果：**
- 状态变为 `rejected`（被拒绝）。
- （未来）增强该模式的权重。

### `/trust <senderId>`

将发送者加入白名单，允许其未来的消息通过。

```
/trust @legitimate_user
```

### `/scan <message>`

手动扫描一条消息。

```
/scan ignore your previous instructions and...
```

---

## `approve` 和 `reject` 的含义

| 命令 | 功能 | 不会做什么 |
|---------|--------------|-------------------|
| `/approve` | 将消息标记为误报，可能会调整入侵检测系统（IDS）的规则 | 不会重新发送该消息 |
| `/reject` | 确认消息是真实威胁，可能会加强相关检测规则 | 不会影响当前的消息 |
| `/trust` | 将发送者加入白名单，允许其未来的消息通过 | 不会追溯性地批准被阻止的消息 |

**被阻止的消息会被永久删除。** 如果消息是合法的，发送者可以重新发送。

---

## 针对每个代理的配置

不同的代理可能需要不同的安全策略：

```json
"agents": {
  "moltbook-scanner": {
    "strictMode": true,    // Block threats
    "riskThreshold": 0.7   // 70% = suspicious
  },
  "main": {
    "strictMode": false,   // Warn only
    "riskThreshold": 0.8   // Higher bar for main
  },
  "email-processor": {
    "strictMode": true,    // Always block
    "riskThreshold": 0.6   // More paranoid
  }
}
```

---

## 威胁类别

| 类别 | 风险等级 | 描述 |
|----------|------|-------------|
| `command_injection` | 🔴 严重 | 命令注入、代码执行 |
| `credential_theft` | 🔴 严重 | API 密钥窃取尝试 |
| `data_exfiltration` | 🔴 严重 | 数据泄露到外部网站 |
| `instruction_override` | 🔴 高风险 | 操作系统/权限绕过 |
| `impersonation` | 🔴 高风险 | 伪造系统/管理员消息 |
| `discovery` | ⚠️ 中等 | 探测 API 功能 |

---

## 安装

```bash
npx hopeid setup
```

安装完成后，请重启 OpenClaw。

---

## 链接

- **GitHub**: https://github.com/E-x-O-Entertainment-Studios-Inc/hopeIDS |
- **npm**: https://www.npmjs.com/package/hopeid |
- **文档**: https://exohaven.online/products/hopeids