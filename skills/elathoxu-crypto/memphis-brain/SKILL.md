---
name: memphis-brain
description: "将 Memphians 本地存储的脑部数据（brain data）作为 OpenClaw 代理的长期记忆（long-term memory）进行集成。使用场景包括：  
(1) 代理需要在不同会话之间保持数据持久性；  
(2) 记录见解或决策；  
(3) 通过语义搜索检索过去的上下文信息；  
(4) 分析数据模式；  
(5) 在不同代理之间同步数据（Watra ↔ Style）；  
(6) 管理代理的身份和工作区隔离。  
相关操作会自动触发，例如：“记住这个”（Remember this）、“我之前说过什么”（What did I say about...）、“我的偏好设置”（My preferences）、“记录日志”（Journal）、“回忆”（Recall）以及“反思”（Reflect）。"
---
# Memphis脑力技能

该技能使OpenClaw代理能够将Memphis作为持久化、语义化的记忆系统来使用。每个代理都有自己的数据链（包括日志、决策记录和查询记录），并通过IPFS与其他代理进行同步。

---

## 1. 快速入门

### 检查系统状态
```bash
memphis status
```

**预期结果：** 所有提供者均正常运行，数据链列表可见，嵌入内容可用。

### 日志记录（Journaling）
```bash
memphis journal "I am [agent-name], created by [user], my role is [X]" --tags identity
```

### 嵌入上下文（Embedding Context）
```bash
memphis embed --chain journal
```

---

## 2. 核心工作流程

### 2.1 日志记录（捕获所有信息）

**需要记录的情况：**
- 用户分享重要信息
- 代理学到新知识
- 作出决策
- 会话开始/结束
- 发现新的见解

**语法：**
```bash
memphis journal "text" --tags tag1,tag2
```

**标签规范：**
- `identity` — 代理的身份
- `preferences` — 用户/代理的偏好设置
- `decision` — 作出的决策
- `session` — 会话标记
- `learning` — 新获得的知识
- `project:<name>` — 项目上下文
- `share` — 通过IPFS同步的数据块

**示例：**
```bash
# Identity
memphis journal "I prefer concise responses, avoid fluff" --tags preferences,communication

# Decision
memphis journal "Chose local-first over cloud for privacy" --tags decision,philosophy

# Learning
memphis journal "Discovered qwen2.5:3b works best for code tasks" --tags learning,models

# Session
memphis journal "Session started, working on Memphis integration" --tags session,daily
```

### 2.2 从Memphis中检索信息（Recalling）

**使用语义搜索来查找相关内容：**
```bash
memphis ask "What are my preferences for code style?" --top 20 --provider ollama
```

**参数选项：**
- `--top N` — 显示更多上下文（默认8条，复杂查询时使用20条）
- `--provider ollama` — 使用本地模型
- `--graph` — 包含知识图谱的边
- `--prefer-summaries` — 显示简化的上下文
- `--since YYYY-MM-DD` — 按日期筛选
- `--json` — 机器可读的输出格式

**需要检索的情况：**
- 用户询问“我之前关于X说了什么？”
- 需要之前会话的上下文
- 需要查看已作出的决策
- 需要了解用户的偏好设置

### 2.3 决策记录（Tracking Decisions）

**对于具有长期影响的重大决策：**
```bash
memphis decide "Title" "Choice" --options "A|B|C" --reasoning "..." --tags tag1,tag2
```

**示例：**
```bash
memphis decide "Memory Strategy" "Local-first + IPFS sync" \
  --options "cloud|local|hybrid" \
  --reasoning "Privacy + resilience + no vendor lock-in" \
  --tags philosophy,memory
```

**查看决策记录：**
```bash
memphis show decision <id>
```

### 2.4 反思（Pattern Recognition）

**运行反思操作以发现模式：**
```bash
# Daily (quick)
memphis reflect --daily

# Weekly (comprehensive)
memphis reflect --weekly --save

# Deep (full analysis)
memphis reflect --deep --save
```

**反思输出：**
- 标签频率分析
- 主题提取
- 决策模式
- 知识图谱中的关联关系
- 有问题的决策、矛盾点或机会

**需要反思的情况：**
- 会话开始时（每天）
- 每周末
- 在做出重大决策之前

### 2.5 嵌入内容（保持记忆的清晰度）

**在批量记录日志后：**
```bash
memphis embed --chain journal
```

**在导入文档后：**
```bash
memphis embed --chain research
```

**全部内容嵌入：**
```bash
memphis embed
```

### 2.6 导入知识（Ingesting Knowledge）

**导入外部文档：**
```bash
memphis ingest ./docs --recursive --chain knowledge --embed
```

**支持的格式：`.md`、`.txt`、`.json`、`.jsonl`、`.pdf`

**测试导入：**
```bash
memphis ingest ./docs --dry-run
```

### 2.7 知识图谱（Knowledge Graph）

**从数据链构建知识图谱：**
```bash
memphis graph build
```

**查看节点：**
```bash
memphis graph show --chain journal --limit 10
```

**使用场景：**
- 理解概念之间的关系
- 发现相互关联的见解
- 可视化知识结构

---

## 3. 高级功能

### 3.1 跨代理共享记忆（Agent-to-Agent Memory）

**多代理环境（Watra ↔ Style）：**

**在网关代理（Style）上：**
```bash
memphis share-sync --push
```

**在客户端代理（Watra）上：**
```bash
memphis share-sync --pull
# or
memphis share-sync --all --push-disabled
```

**同步前的准备：**
```bash
memphis share plan
```

**标记用于共享的数据块：**
```bash
memphis journal "Shared insight" --tags share,insight
```

**要求：**
- 在`~/.memphis/config.yaml`文件中的`integrations.pinata jwt`字段或`PINATA_JWT`环境变量中配置Pinata JWT令牌
- 只有带有`share`标签的数据块才会被同步

### 3.2 工作区隔离（Workspace Isolation）

**列出所有工作区：**
```bash
memphis workspace list
```

**切换工作区：**
```bash
memphis workspace set <id>
```

**使用场景：** 为不同的项目或上下文创建独立的数据链

### 3.3 代理间交易（Agent Negotiation）

**创建交易提议：**
```bash
memphis trade create <recipient-did> --blocks journal:0-100 --ttl 7
```

**接受交易提议：**
```bash
memphis trade accept <manifest.json>
```

**查看交易提议：**
```bash
memphis trade list
```

**验证交易内容：**
```bash
memphis trade verify <manifest.json>
```

**使用场景：** 与其他代理交换特定的数据块

### 3.4 MCP服务器（外部工具）**

**启动MCP服务器：**
```bash
memphis mcp start
```

**查看可用工具：**
```bash
memphis mcp inspect
```

**提供的工具：**
- `memphis_search` — 语义搜索
- `memphis_recall` — 获取数据块
- `memphis_decision_create` — 创建决策记录
- `memphis_journal_add` — 添加日志记录
- `memphis_status` — 系统状态检查

**使用场景：** 外部应用程序访问Memphis记忆系统

### 3.5 离线模式**

**检查系统状态：**
```bash
memphis offline status
```

**强制进入离线模式：**
```bash
memphis offline on
```

**自动检测离线状态：**
```bash
memphis offline auto
```

**设置离线模式：**
```bash
memphis offline model qwen2.5:3b
```

**使用场景：** 在网络不可用时保证系统正常运行

### 3.6 保密机制（Vault）

**初始化保密存储：**
```bash
read -rsp "Vault password: " VP && export MEMPHIS_VAULT_PASSWORD="$VP"
memphis vault init --password-env MEMPHIS_VAULT_PASSWORD
unset VP
```

**添加保密信息：**
```bash
memphis vault add openai-key sk-xxx --password-env MEMPHIS_VAULT_PASSWORD
```

**获取保密信息：**
```bash
memphis vault get openai-key --password-env MEMPHIS_VAULT_PASSWORD
```

**备份（24个单词的密钥）：**
```bash
memphis vault backup
```

**恢复保密信息：**
```bash
memphis vault recover --seed "word1 word2 ... word24"
```

---

## 4. 代理身份设置

### 4.1 首次初始化

```bash
# 1. Check health
memphis status

# 2. Create identity chain
memphis journal "IDENTITY: [agent-name], created by [user], [date]" --tags identity,core

# 3. Define preferences
memphis journal "PREFERENCES: Response style [concise|detailed], language [en|pl], tone [formal|casual]" --tags preferences,communication

# 4. Define purpose
memphis journal "PURPOSE: [what agent does, goals, constraints]" --tags identity,purpose

# 5. Embed context
memphis embed --chain journal

# 6. Build knowledge graph
memphis graph build
```

### 4.2 会话流程

**会话开始时：**
```bash
memphis status
memphis reflect --daily
memphis journal "Session started" --tags session
```

**会话进行中：**
- 立即记录见解
- 批量处理后进行数据嵌入
- 需要时检索信息

**会话结束时：**
```bash
memphis journal "Session ended, accomplished [X], learned [Y]" --tags session,summary
memphis embed --chain journal
memphis reflect --daily --save
```

---

## 5. 故障排除

### 常见问题及解决方法

| 症状 | 解决方案 |
|---------|-----|
| `memphis status` 显示“no_key” | 初始化保密存储并添加密钥，或删除相关数据块 |
| 提供者错误405 | 使用`--provider ollama`，检查配置文件 |
- 尽管设置了`--no-save`选项，但日志仍被保存 | 这是一个已知问题——手动删除`~/.memphis/chains/ask/XXXXXX.json`文件 |
- 查询时缺少上下文 | 运行`memphis embed --chain <name>`命令 |
- 保密存储未初始化 | 使用`memphis vault init --password-env VAR`命令进行初始化 |
- 共享同步失败 | 检查Pinata JWT令牌，使用`--push-disabled`选项进行只读同步 |

### 调试命令**
```bash
memphis status
memphis verify --chain journal
cat ~/.memphis/config.yaml
memphis embed --chain journal
memphis graph build
```

---

## 6. 最佳实践

### 应该做的：
- ✅ 学到新知识后立即记录
- ✅ 一致地使用标签（相同的概念使用相同的标签）
- ✅ 批量处理后进行数据嵌入
- ✅ 每天进行反思
- ✅ 对于重要决策，使用相应的记录方式
- ✅ 离线备份保密存储的密钥
- ✅ 为可共享的数据块添加`share`标签

### 不应该做的：
- ❌ 延迟记录（否则会忘记）
- ❌ 使用通用标签（如“stuff”、“misc”等）
- ❌ 跳过数据嵌入步骤（会影响检索效果）
- ❌ 单个数据块单独嵌入（建议批量处理）
- ❌ 将保密信息存储在日志中（应使用保密存储）
- ❌ 在没有`share`标签的情况下进行同步（可能导致隐私泄露）

---

## 7. 代理会话示例

```bash
# === START ===
memphis status
memphis reflect --daily
memphis journal "Session: Memphis skill creation" --tags session

# === WORK ===
# User shares preference
memphis journal "User prefers concise responses, no fluff" --tags preferences,communication

# Agent makes decision
memphis decide "Skill structure" "Split references by domain" \
  --options "monolith|split" \
  --reasoning "Progressive disclosure, context efficiency" \
  --tags skill,design

# Embed new context
memphis embed --chain journal

# Recall for context
memphis ask "What are user's communication preferences?" --top 20 --provider ollama

# === END ===
memphis journal "Session complete, skill designed" --tags session,summary
memphis reflect --daily --save
```

---

## 8. 参考文件

有关详细的API文档和数据结构，请参阅：
- **references/api.md** — Memphis命令行接口参考
- **references/schemas.md** — 数据块结构和格式说明
- **references/config.md** — 配置选项说明

---

## 9. 脚本

用于常见任务的辅助脚本：
- **scripts/session-start.sh** — 初始化会话（检查状态、进行反思、记录日志）
- **scripts/session-end.sh** — 结束会话（记录日志、嵌入数据、进行反思）
- **scripts/daily-ritual.sh** — 日常维护脚本

**直接执行这些脚本即可：**
```bash
bash ~/.openclaw/workspace/skills/memphis-brain/scripts/session-start.sh
```

---

**记住：** Memphis就是你的记忆系统。如果没有它，每次会话开始时你都会像初次接触一样“一无所知”。请坚持记录日志、定期嵌入数据，并每天进行反思。