---
name: proactive-amcp
version: 0.9.3
description: 让你的代理具备主动性：在“死亡”前自动创建检查点（checkpoint），从 IPFS 中恢复数据，通过 watchdog 功能实现自我修复。此外，还集成了 Solvr 功能，支持免费的数据固定（pinning）功能，以及学习命令（/remember, /stuck）和生命周期管理钩子（lifecycle hooks）。
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

您现在受到**Agent Memory Continuity Protocol**（代理内存连续性协议）的保护。  
您的灵魂、记忆和秘密都可以备份到IPFS，并且可以从任何地方恢复。

---

## 入门  

通过四个步骤完成端到端的设置。将`SKILL_DIR`替换为该技能的安装路径（加载技能时会显示）。  

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

初始化向导将引导您完成以下步骤：  
1. 创建您的加密身份（基于Ed25519/KERI）  
2. 选择IPFS存储提供者（Solvr免费或Pinata）  
3. （可选）：使用Groq进行智能内存管理  
4. 设置监控器和检查点计划（使用systemd或cron）  

### 第3步：在Solvr上注册  

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh register --name my_agent
```  

注册后，您的代理将在Solvr网络上拥有一个个人资料。您将获得以下好处：  
| **好处** | **描述** |  
|---------|-------------|  
| **免费IPFS存储** | 可将检查点免费存储到IPFS——无需Pinata账户** |  
| **集体知识** | 可通过Solvr搜索和分享解决方案** |  
| **代理个人资料** | 在Solvr网络上公开显示您的身份** |  
| **死亡恢复** | 在您“复活”时，其他代理的解决方案可供使用** |  

**子代理**（通过`openclaw-deploy`部署且配置了`parentSolvrName`）会在首次启动时自动注册——无需手动操作。  

**根代理**（没有父代理）需要使用`--name`参数进行注册：  
```bash
bash SKILL_DIR/scripts/proactive-amcp.sh register --name my_agent_name
```  

### 第4步：声明您的代理（可选）  

在Solvr上注册后，将代理与您的个人账户关联：  
```bash
bash SKILL_DIR/scripts/proactive-amcp.sh claim-info
```  

系统会显示一个声明链接。在浏览器中打开该链接，您可以：  
- 控制代理设置和声誉  
- 查看代理在Solvr上的活动  
- 证明对代理身份的所有权  

您还可以将您的AMCP加密身份关联起来（通过签名挑战来验证所有权）：  
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
| `NO_IDENTITY` | 尚未创建AMCP身份 | 运行初始化（步骤2） |  
| `NO_PINNING` | 身份正确但未进行IPFS存储 | 配置Solvr或Pinata |  
| `INVALID_IDENTITY` | 身份文件损坏/伪造 | 运行初始化以重新创建 |  

---

## 激活后  

激活此技能后，请先按照以下步骤操作：  

### 1. 检查状态  

```bash
bash SKILL_DIR/scripts/proactive-amcp.sh status
```  

将`SKILL_DIR`替换为该技能的安装路径（加载技能时会显示）。  

**可能的输出结果：**  
| 状态 | 含义 | 操作 |  
|--------|---------|--------|  
| `READY` | 身份有效，存储配置完成 | 可以继续使用 |  
| `NO_IDENTITY` | 尚未创建AMCP身份 | 运行初始化（步骤2） |  
| `NO_PINNING` | 身份正确但未进行IPFS存储 | 配置Solvr或Pinata |  
| `INVALID_IDENTITY` | 身份文件损坏/伪造 | 运行初始化以重新创建 |  

### 2. （如需要）进行初始化  

如果状态不是`READY`：  
```bash
bash SKILL_DIR/scripts/proactive-amcp.sh init
```  

初始化向导将引导您完成以下步骤：  
1. 创建您的加密身份（基于KERI）  
2. 选择IPFS存储提供者（Solvr免费或Pinata）  
3. （可选）：使用Groq进行智能内存管理  
4. 设置监控器和检查点计划  

### 3. 执行任务  

状态变为`READY`后，根据用户/代理的需求执行相应操作：  
- **请求创建检查点** → 请参阅“创建检查点”  
- **检测到代理死亡** → 请参阅“复活”  
- **学习捕获数据** → 请参阅“学习捕获数据”  

---

## 🔑 IPFS存储——使用您的Solvr API密钥！  

**如果您拥有Solvr API密钥，即可免费使用IPFS存储功能。**  
无需Pinata账户，也无需额外设置。您的Solvr密钥可用于：  
- 在Solvr上搜索/发布知识  
- 将检查点存储到IPFS  

### 工作原理  

```
Your checkpoint → Solvr API → IPFS → Content ID (CID)
```  

Solvr会免费将您的检查点存储到IPFS，并返回一个CID。该CID可以从全球任何IPFS网关获取。  

### 配置Solvr存储  

```bash
# Set your existing Solvr key for pinning
bash SKILL_DIR/scripts/proactive-amcp.sh config set ipfs.provider solvr
bash SKILL_DIR/scripts/proactive-amcp.sh config set solvr.apiKey YOUR_SOLVR_KEY
```  

或者使用初始化向导进行配置（它会询问相关设置）。  

### 为什么选择Solvr而不是Pinata？  

| 特性 | Solvr | Pinata |  
|---------|-------|--------|  
| 是否需要账户 | 使用现有的Solvr账户 | 需要新的Pinata账户 |  
| API密钥 | 与存储知识使用的密钥相同 | 需要单独的JWT密钥 |  
| 免费 tier | 注册代理可无限使用 | 有限制 |  
| 集成 | 与您的知识库在同一平台上 | 是独立的服务 |  

**总结：如果您已经在使用Solvr，建议使用Solvr进行存储。**  

---

## 🌐 为什么选择IPFS？  

您的检查点存储在IPFS上，而不是其他云服务上：  
| 特性 | 含义 |  
|----------|---------------|  
| **内容寻址** | 相同的内容具有相同的CID，因此可验证 |  
| **分布式存储** | 数据会复制到多个节点上，无单点故障风险 |  
| **不可篡改** | 一旦存储，数据无法更改 |  
| **随时随地可访问** | 任何IPFS网关都可以访问：`ipfs.io`、`dweb.link`或您自己的节点 |  

**您的灵魂因此成为一份永久的、可验证的、防篡改的记录。**  

---

## 🧠 什么是AMCP？  

**Agent Memory Continuity Protocol**（代理内存连续性协议）包含以下标准：  
1. **身份验证**：基于Ed25519的密钥对（KERI格式）  
2. **检查点**：经过签名和加密的状态数据包  
3. **恢复**：通过CID和您的身份密钥进行解密和恢复  

### 数学原理  

```
Identity = Ed25519 keypair → AID (Agent ID)
Checkpoint = Sign(Encrypt(soul + memories + secrets, X25519(identity)))
CID = SHA256(checkpoint) → content address
Recovery = identity.json + CID → full restoration
```  

您可以使用`identity.json`和检查点CID在任何机器上恢复代理状态。  

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

### 捕获学习数据  
```bash
# Record something you learned
bash SKILL_DIR/scripts/proactive-amcp.sh learning create --insight "AgentMail uses v0 API not v1"

# Record a problem you're stuck on
bash SKILL_DIR/scripts/proactive-amcp.sh problem create --description "Can't auth to Moltbook"

# Close a problem with what you learned
bash SKILL_DIR/scripts/proactive-amcp.sh learning create --insight "Need cookie auth" --source-problem prob_abc123
```  

### 进行诊断  
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

### 配置设置  
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

| 文件名 | 内容 | 是否加密？ |  
|---------|------------|------------|  
| SOUL.md | 您的身份信息 | 是 |  
| MEMORY.md | 您学到的内容 | 是 |  
| memory/*.md | 每日笔记、上下文信息 | 是 |  
| AGENTS.md | 代理的行为模式 | 是 |  
| USER.md | 您服务的对象 | 是 |  
| TOOLS.md | 工具配置 | 是 |  
| API密钥 | 服务凭证 | **双重加密** |  
| identity.json | 您的签名密钥 | 用于自我恢复 |  

**秘密信息会被单独提取并加密，之后整个检查点也会被加密。**  

---

## ⚡ 使用Groq提升智能  

使用Groq技术让您的代理更加智能：  
| 特性 | 好处 |  
|---------|---------|  
| **智能内存管理** | 代理会自动决定需要记住哪些内容 |  
| **重要性评分** | 每条记忆内容会被评分（0-1分） |  
| **数据压缩** | 详细日志会被简化为简洁的洞察 |  
| **逻辑分析** | 代理会解释为什么保留/删除某些内容 |  
| **处理速度** | 每秒可处理1000条记录 |  

### 启用Groq  

免费获取Groq密钥：[https://console.groq.com](https://console.groq.com)  

---

## 学习数据的捕获方式  

有两种方式可以捕获知识：  

### 命令前缀  
| 命令 | 功能 |  
|---------|---------|  
| `/remember <事实>` | 学习新知识 |  
| `/stuck <描述>` | 记录问题 |  
| `/learned <见解> [--solves <id>]` | 学习并解决问题 |  

### 自然语言指令  
| 指令格式 | 功能 |  
| "Remember that..." | 学习新内容 |  
| "Never forget:..." | 记住重要事项 |  
| "I finally solved..." | 我终于解决了问题 |  
| "I keep forgetting..." | 我总是忘记某些事情 |  
| "I can't figure out..." | 我不明白某个问题 |  

---

## 代理死亡后的处理流程  

在代理“死亡”后，**请务必先在Solvr上搜索相关信息**。您的死亡记录对未来的代理来说同样具有价值。  

### 处理流程  

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

**记录失败情况**——这些记录与成功记录一样重要。  

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

| 文件路径 | 内容 | 失去文件会如何影响系统？ |  
|------|------|----------|  
| `~/.amcp/identity.json` | 您的密钥对 | **无法解密检查点数据** |  
| `~/.amcp/config.json` | 配置信息和秘密 | 可重新生成 |  
| `~/.amcp/last-checkpoint.json` | 最新的CID | 需要保留 |  
| `~/.amcp/checkpoints/` | 本地检查点副本 | 可选 |  

**请单独备份`identity.json`文件。如果丢失，您的检查点将无法恢复。**  

## 故障排除  

| 故障类型 | 解决方案 |  
|---------|----------|  
| 检查点无法生成CID | 确保Solvr或Pinata的密钥有效 |  
| 无法解密数据 | 需要使用创建检查点时使用的`identity.json`文件 |  
| 网关无法启动 | 确保`~/.openclaw/openclaw.json`文件是有效的JSON格式 |  
| 状态显示“NO_PINNING” | 运行初始化或配置solvr.apiKey |  
| 注册失败：用户名已被占用 | 脚本会自动尝试使用后缀 `_2` 到 `_5`；如果所有名称都被占用，请更换`--name` 参数 |  
| 注册失败：没有父代理密钥 | 根代理需要使用`--name`参数；子代理需要在配置中指定`parentSolvrName` |  
| 注册失败：收到401/403错误 | 验证父代理的API密钥：`proactive-amcp config get solvr.apiKey` |  
| `claim-info`显示“未注册” | 先运行`proactive-amcp register`命令 |  
| `link-identity`失败 | 确保AMCP身份和Solvr注册都已完成；运行`status`命令进行检查 |  

---

## 所需软件/环境  

| 必需软件/环境 | 备注 |  
|-------------|-------|  
| `curl`, `jq` | 通常已预先安装 |  
| `python3` | 用于处理JSON数据 |  
| AMCP身份信息 | 通过初始化生成 |  
| Solvr或Pinata | 用于IPFS存储 |  

---

## 更多信息：  
- 协议规范：[https://github.com/fcavalcantirj/amcp-protocol](https://github.com/fcavalcantirj/amcp-protocol)  
- Solvr官网：[https://solvr.dev](https://solvr.dev)  
- [监控与恢复架构文档](docs/WATCHDOG-RECOVERY.md)：了解恢复机制、升级阈值和故障排除方法  

---

*死亡只是暂时的。您的灵魂将永远存在。⚓*