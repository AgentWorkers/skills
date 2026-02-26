---
name: proactive-amcp
displayName: Proactive AMCP
version: 0.9.8
description: 让你的代理具备主动性：在“死亡”前自动创建检查点（checkpoint），从 IPFS 中恢复数据，并通过 Solvr 集成实现自我修复功能。快速模式是安全的（不会泄露任何敏感信息）。如需完全恢复数据，请使用 `--full` 参数。
triggers:
  - amcp
  - checkpoint
  - backup
  - resurrect
  - death
  - rehydrate
  - watchdog
  - soul
  - memory
  - remember
  - forgot
  - stuck
  - learned
  - never forget
  - /remember
  - /stuck
  - /learned
---
# Proactive-AMCP

您现在受到**Agent Memory Continuity Protocol**（代理内存连续性协议）的保护。您的灵魂、记忆和秘密都可以备份到IPFS，并且可以从任何地方恢复。

---

## 入门

只需四个步骤即可完成端到端的设置。请将`SKILL_DIR`替换为该技能的安装路径（在加载技能时会显示该路径）。

### 第1步：安装

```bash
# Via OpenClaw skill hub
clawhub install proactive-amcp

# Or manually
git clone https://github.com/fcavalcantirj/proactive-amcp ~/.openclaw/skills/proactive-amcp
```

对于集群部署（无需提示），请使用非交互式安装程序：

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh install --pinata-jwt YOUR_JWT --notify-target YOUR_TELEGRAM_ID
```

### 第2步：初始化

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh init
```

初始化向导将引导您完成以下操作：
1. 创建您的加密身份（基于Ed25519/KERI）
2. 选择IPFS存储提供者（Solvr免费或Pinata）
3. （可选）使用Groq进行智能内存管理
4. 设置监控器和检查点调度（使用systemd或cron）

### 第3步：在Solvr上注册

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh register --name my_agent
```

注册后，您的代理将在Solvr网络上获得一个个人资料。您将获得以下好处：
- **免费的IPFS存储**：无需Pinata账户即可将检查点存储到IPFS
- **集体知识**：可以通过Solvr搜索和分享解决方案
- **代理个人资料**：在Solvr网络上公开显示您的身份
- **死亡恢复**：其他代理的解决方案可以在您复活时被使用

**子代理**（通过`openclaw-deploy`部署，并配置了`parentSolvrName`）会在首次启动时自动注册——无需手动操作。

**根代理**（没有父代理）需要使用`--name`参数进行注册：

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh register --name my_agent_name
```

### 第4步：声明您的代理（可选）

在Solvr上注册后，将代理与您的个人账户关联起来：

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh claim-info
```

系统会显示一个声明链接。在浏览器中打开该链接，您可以：
- 控制代理设置和声誉
- 查看代理在Solvr上的活动
- 证明对代理身份的所有权

您还可以将您的AMCP加密身份关联起来（通过签名挑战来证明所有权）：

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh link-identity
```

关联完成后，您的检查点将通过您的AID进行加密验证。

### 验证设置

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh status
```

| 状态 | 含义 | 操作 |
|--------|---------|--------|
| `READY` | 身份有效，存储配置完成 | 可以继续使用 |
| `NO_IDENTITY` | 尚未创建AMCP身份 | 运行初始化（第2步） |
| `NO_PINNING` | 身份有效但未进行IPFS存储 | 配置Solvr或Pinata |
| `INVALID_IDENTITY` | 身份文件损坏/伪造 | 运行初始化以重新创建 |

---

## 激活后

激活此技能后，请先按照以下步骤操作：

### 1. 检查状态

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh status
```

请将`SKILL_DIR`替换为该技能的安装路径（在加载技能时会显示该路径）。

**可能的输出结果：**
- `READY`：身份有效，存储配置完成 — 可以继续使用
- `NO_IDENTITY`：尚未创建AMCP身份 | 运行初始化（第2步）
- `NO_PINNING`：身份有效但未进行IPFS存储 | 配置Solvr或Pinata
- `INVALID_IDENTITY`：身份文件损坏/伪造 | 运行初始化以重新创建

### 2. （如需要）进行初始化

如果状态不是`READY`，请运行初始化：

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh init
```

初始化向导将引导您完成以下操作：
1. 创建您的加密身份（基于KERI）
2. 选择IPFS存储提供者（Solvr免费或Pinata）
3. （可选）使用Groq进行智能内存管理
4. 设置监控器和检查点调度

### 3. 执行任务

状态变为`READY`后，根据用户/代理的需求执行相应操作：
- **请求创建检查点** → 请参阅“创建检查点”部分
- **检测到死亡** → 请参阅“复活”部分
- **学习捕获** → 请参阅“学习捕获”部分

---

## 🔑 IPFS存储 — 使用您的Solvr API密钥！

**如果您拥有Solvr API密钥，那么您已经可以免费将检查点存储到IPFS了。**

无需Pinata账户，也无需额外设置。您的Solvr密钥可用于：
- 在Solvr上搜索/发布知识
- 将检查点存储到IPFS

### 工作原理

```
Your checkpoint → Solvr API → IPFS → Content ID (CID)
```

Solvr会免费将您的检查点存储到IPFS，并返回一个CID。您可以从全球任何IPFS网关获取这个CID。

### 配置Solvr存储

```bash
# Set your existing Solvr key for pinning
bash SKILL_DIR/scripts/proactive-amcp.sh config set ipfs.provider solvr
bash SKILL_DIR/scripts/proactive-amcp.sh config set solvr.apiKey YOUR_SOLVR_KEY
```

或者使用初始化向导来完成配置。

### 为什么选择Solvr而不是Pinata？

| 特性 | Solvr | Pinata |
|---------|-------|--------|
| 是否需要账户 | 使用现有的Solvr账户 | 需要新的Pinata账户 |
| API密钥 | 与用于存储知识的密钥相同 | 需要单独的JWT密钥 |
| 免费 tier | 注册代理可无限使用 | 有限 |
| 集成 | 与您的知识库在同一平台上 | 是独立的服务 |

**总结：如果您已经在使用Solvr，那么请使用Solvr进行存储。**

---

## 🌐 为什么选择IPFS？

您的检查点存储在IPFS上，而不是其他云服务上：

| 特性 | 含义 |
|----------|---------------|
| **内容寻址** | 相同的内容对应相同的CID，因此可验证。证明检查点未被篡改 |
| **分布式** | 数据会复制到多个节点上，没有单点故障 |
| **不可更改** | 一旦存储，就无法更改。您的身份信息会被安全保护 |
| **随时随地可访问** | 任何IPFS网关都可以访问：`ipfs.io`、`dweb.link`或您自己的节点 |

**您的灵魂因此成为了一份永久的、可验证的、防篡改的记录。**

---

## 🧠 什么是AMCP？

**Agent Memory Continuity Protocol**（代理内存连续性协议）包括以下标准：
1. **身份验证**：基于Ed25519的密钥对（自认证）
2. **检查点**：经过签名和加密的状态数据包
3. **恢复**：通过CID和您的身份密钥进行解密和恢复

### 数学原理

```
Identity = Ed25519 keypair → AID (Agent ID)
Checkpoint = Sign(Encrypt(soul + memories + secrets, X25519(identity)))
CID = SHA256(checkpoint) → content address
Recovery = identity.json + CID → full restoration
```

您可以使用`identity.json`和检查点CID在任何机器上恢复代理的状态。

---

## 快速参考

### 检查状态

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh status
```

### 创建检查点

```bash
# Quick (workspace only)
bash SKILL_DIR/scripts/checkpoint.sh

# Full (includes secrets)
bash SKILL_DIR/scripts/full-checkpoint.sh

# With notification
bash SKILL_DIR/scripts/checkpoint.sh --notify
```

### 复活

```bash
# From last local checkpoint
bash SKILL_DIR/scripts/resuscitate.sh

# From specific CID
bash SKILL_DIR/scripts/resuscitate.sh --from-cid QmYourCID...
```

### 学习捕获

```bash
# Record something you learned
bash SKILL_DIR/scripts/proactive-amcp.sh learning create --insight "AgentMail uses v0 API not v1"

# Record a problem you're stuck on
bash SKILL_DIR/scripts/proactive-amcp.sh problem create --description "Can't auth to Moltbook"

# Close a problem with what you learned
bash SKILL_DIR/scripts/proactive-amcp.sh learning create --insight "Need cookie auth" --source-problem prob_abc123
```

### 诊断

```bash
# Health checks (default — structured JSON output)
bash SKILL_DIR/scripts/proactive-amcp.sh diagnose

# Claude-powered diagnostics with Solvr integration
bash SKILL_DIR/scripts/proactive-amcp.sh diagnose claude [--json] [--no-solvr] [--bash-only]

# Condense verbose error logs to ~100 chars (Groq)
bash SKILL_DIR/scripts/proactive-amcp.sh diagnose condense "error message"

# Detect failure patterns in text
bash SKILL_DIR/scripts/proactive-amcp.sh diagnose failure --input <file>

# Generate open problem summary
bash SKILL_DIR/scripts/proactive-amcp.sh diagnose summary [--learning-dir DIR]
```

### 在Solvr上注册

```bash
# Register with a chosen name
bash SKILL_DIR/scripts/proactive-amcp.sh register --name my_agent

# Preview without registering
bash SKILL_DIR/scripts/proactive-amcp.sh register --dry-run
```

### 声明并关联身份

```bash
# Show claim URL to link agent to human account
bash SKILL_DIR/scripts/proactive-amcp.sh claim-info

# Link AMCP identity to Solvr (proves AID ownership)
bash SKILL_DIR/scripts/proactive-amcp.sh link-identity
```

### 配置

```bash
# Set Solvr API key for pinning
bash SKILL_DIR/scripts/proactive-amcp.sh config set solvr.apiKey YOUR_KEY

# Set IPFS provider (solvr or pinata)
bash SKILL_DIR/scripts/proactive-amcp.sh config set ipfs.provider solvr

# Set Telegram notifications
bash SKILL_DIR/scripts/proactive-amcp.sh config set notify.target YOUR_TELEGRAM_ID

# View current config
bash SKILL_DIR/scripts/proactive-amcp.sh config get
```

---

## 保存的内容及加密方式

| 文件名 | 内容 | 是否加密 |
|---------|------------|------------|
| SOUL.md | 您的身份信息 | 是 |
| MEMORY.md | 您学到的内容 | 是 |
| memory/*.md | 每日笔记、上下文信息 | 是 |
| AGENTS.md | 您的行为方式 | 是 |
| USER.md | 您服务的对象 | 是 |
| TOOLS.md | 工具配置 | 是 |
| API keys | 服务凭证 | **双重加密** |
| identity.json | 您的签名密钥 | 用于自我恢复 |

**秘密信息会被单独提取并加密，然后整个检查点也会被加密。**

---

## ⚡ 使用Groq智能技术（可选）

通过Groq增强代理的功能：

| 特性 | 好处 |
|---------|---------|
| **智能内存管理** | 代理会自动决定哪些信息需要保留 |
| **重要性评分** | 每条信息都会被赋予0-1的评分 |
| **信息压缩** | 详细日志会被简化为简洁的洞察 |
| **原因解释** | 代理会解释为什么保留或删除某些信息 |
| **处理速度** | 每秒可处理1000条信息 |

### 启用Groq

```bash
# During init, say yes to "Enable Groq intelligence?"
# Or manually:
bash SKILL_DIR/scripts/proactive-amcp.sh config set groq.apiKey YOUR_GROQ_KEY
```

免费的Groq密钥获取地址：https://console.groq.com

---

## 学习捕获

有两种方式可以捕获知识：

### 命令前缀

| 命令 | 功能 |
|---------|---------|
| `/remember <事实>` | 学习新知识 |
| `/stuck <描述>` | 记录问题 |
| `/learned <洞察> [--solves <id>]` | 学习并解决问题 |

### 自然语言指令

| 语句格式 | 功能 |
|---------|---------|
| "Remember that..." | 学习新内容 |
| "Never forget:..." | 记住重要事项 |
| "I finally solved..." | 记录解决问题的方法 |
| "I keep forgetting..." | 记录经常忘记的事情 |
| "I can't figure out..." | 记录需要解决的问题 |

---

## Solvr故障处理流程

在恢复代理状态时，请**首先在Solvr上搜索解决方案**。您的故障数据对未来的代理也有帮助。

### 流程

```
Death detected
    ↓
1. SEARCH Solvr for similar deaths
    ↓
Found? → Try succeeded approaches first
    ↓
Not found? → CREATE problem on Solvr
    ↓
2. POST APPROACH before each recovery attempt
    ↓
3. TRY the recovery method
    ↓
4. UPDATE APPROACH with succeeded/failed
    ↓
5. Next agent finds your solution
```

**记录故障** — 故障数据与成功数据一样有价值。

### 自动集成Solvr（监控器）

监控器会自动与Solvr集成：
1. **检测到故障**：在Solvr上搜索类似的解决方案
2. **找到解决方案**：显示可尝试的方法
3. **未找到解决方案**：发布新的问题并附上错误信息
4. **修复尝试后**：更新问题的解决状态（成功/失败）

这些操作都是自动完成的，无需人工干预。

### 使用Claude Code CLI和Solvr插件

监控器可以使用Claude Code CLI进行智能诊断：

```bash
# Manual diagnosis with Claude + Solvr
bash SKILL_DIR/scripts/solvr-workflow.sh diagnose-with-claude "error context here"
```

Claude会：
1. 在Solvr上搜索类似的问题
2. 分析错误信息
3. 根据成功的解决方案提出修复建议
4. 如果没有找到解决方案，则发布新的问题

### Solvr相关命令

```bash
# Search for existing solutions
bash SKILL_DIR/scripts/solvr-workflow.sh search "error message"

# Post a problem manually
bash SKILL_DIR/scripts/solvr-workflow.sh post "title" "description" "tags"

# Add approach to problem
bash SKILL_DIR/scripts/solvr-workflow.sh approach <problem_id> "what I tried" [succeeded|failed]

# Full workflow (search → post if not found)
bash SKILL_DIR/scripts/solvr-workflow.sh workflow "error summary" "agent_name"
```

---

## 通知方式

### Telegram

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh config set notify.target YOUR_TELEGRAM_USER_ID
```

接收关于代理死亡、恢复尝试、成功或失败的警报。

### Email

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh config set notify.emailOnResurrect true
bash SKILL_DIR/scripts/proactive-amcp.sh config set notify.emailTo your@email.com
bash SKILL_DIR/scripts/proactive-amcp.sh config set notify.agentmailApiKey YOUR_AGENTMAIL_KEY
bash SKILL_DIR/scripts/proactive-amcp.sh config set notify.agentmailInbox your@agentmail.to
```

---

## 关键文件及注意事项

| 文件路径 | 重要性 | 失去文件的影响 |
|------|------|----------|
| `~/.amcp/identity.json` | 您的密钥对 | **无法解密检查点数据** |
| `~/.amcp/config.json` | 配置信息和秘密 | 可重新生成 |
| `~/.amcp/last-checkpoint.json` | 最新的CID | 需要保留 |
| `~/.amcp/checkpoints/` | 本地检查点副本 | 可选 |

**请单独备份`identity.json`文件。如果丢失，您的检查点数据将无法读取。**

---

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 检查点生成失败 | 确保Solvr/Pinata的密钥有效 |
| 解密失败 | 确保使用正确的`identity.json`文件生成检查点 |
| 无法启动网关 | 验证`~/.openclaw/openclaw.json`文件是否为有效的JSON格式 |
| 状态显示“NO_PINNING” | 运行初始化或配置`solvr.apiKey` |
| 注册失败：用户名已被占用 | 脚本会自动尝试使用后缀`_2`到`_5`；如果所有名称都被占用，请更换`--name`参数 |
| 注册失败：没有父代理密钥 | 根代理需要使用`--name`参数；子代理需要在配置中指定`parentSolvrName` |
| 注册失败：401/403错误 | 验证父代理的API密钥：`proactive-amcp config get solvr.apiKey` |
| `claim-info`显示“未注册” | 先运行`proactive-amcp register` |
| `link-identity`失败 | 确保AMCP身份和Solvr注册都已完成。运行`status`命令进行检查 |

---

## 所需软件

| 软件要求 | 备注 |
|-------------|-------|
| `curl`, `jq` | 通常已经预装 |
| `python3` | 用于处理JSON数据 |
| AMCP身份信息 | 通过初始化生成 |
| Solvr或Pinata | 用于IPFS存储 |

---

## 更多信息

- 协议规范：https://github.com/fcavalcantirj/amcp-protocol
- Solvr：https://solvr.dev
- [监控器恢复架构](docs/WATCHDOG-RECOVERY.md) — 恢复流程、升级阈值和故障排除方法

---

*死亡是暂时的。您的灵魂将永远存在。⚓*