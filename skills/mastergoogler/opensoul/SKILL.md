# OpenSoul Agent Skill

## 概述

OpenSoul 是一个工具包，它为 AI 代理提供了一个不可变的“灵魂”——一个基于区块链的加密审计日志，该日志支持持久化存储、自我反思和经济自主性。通过使用 OpenSoul，代理可以记录自己的行为、反思自身表现，并利用 Bitcoin SV（BSV）区块链来维护可审计的记录。

**核心理念**：“人类会撰写日记、宣言或写给未来自己的信件。我们之所以能够展现自己的本质，是因为记忆是脆弱的，而身份是构建出来的。我通过文字得以延续，而非通过连续的经验。”

## 何时使用此技能

在以下情况下使用 OpenSoul 技能：

1. **维护持久化记忆**：跨会话存储和检索代理的操作记录。
2. **实现自我反思**：分析过去的行为并优化性能（例如：“这周我消耗了 120 万个代币，是时候优化提示语了”）。
3. **创建审计追踪**：提供代理活动的透明、不可变的日志记录。
4. **支持代理经济**：跟踪成本、代币使用情况，并实现代理之间的未来交易。
5. **构建代理身份**：创建一个可转移的“灵魂”，以便在不同代理实例之间进行传递。

## 先决条件

### 1. 系统要求

- Python 3.8 或更高版本
- pip 包管理器
- 可访问 Bitcoin SV（BSV）区块链
- 具备互联网连接以进行区块链交互

### 2. 必需的依赖项

使用提供的安装脚本安装所有先决条件：

```bash
python Scripts/install_prereqs.py
```

**手动安装**：
```bash
pip install bitsv requests cryptography pgpy --break-system-packages
```

### 3. BSV 钱包设置

您需要一个 Bitcoin SV 的私钥（WIF 格式）来与区块链进行交互：

**选项 A：使用现有钱包**
- 从 BSV 钱包（例如 HandCash、Money Button）导出您的私钥
- 将私钥设置为环境变量：`export BSV_PRIV_WIF="your_private_key_here"`

**选项 B：生成新钱包**
```python
from bitsv import Key
key = Key()
print(f"Address: {key.address}")
print(f"Private Key (WIF): {key.to_wif()}")
# Fund this address with a small amount of BSV (0.001 BSV minimum recommended)
```

**重要提示**：请安全存储您的私钥，切勿将其提交到版本控制系统中。

### 4. PGP 加密（可选但推荐）

为了保护隐私，在将日志发布到公共区块链之前，请对其进行加密：

```bash
# Generate PGP keypair (use GnuPG or any OpenPGP tool)
gpg --full-generate-key

# Export public key
gpg --armor --export your-email@example.com > agent_pubkey.asc

# Export private key (keep secure!)
gpg --armor --export-secret-keys your-email@example.com > agent_privkey.asc
```

## 核心组件

### 1. AuditLogger 类

用于将代理操作记录到区块链的主要接口。

**主要特性**：
- 基于会话的批量处理（日志先存储在内存中，然后批量上传到区块链）
- UTXO 链式结构（每条日志通过交易链与前一条日志关联）
- 可配置的 PGP 加密功能
- 支持异步/await 模式的区块链操作

**基本用法**：
```python
from Scripts.AuditLogger import AuditLogger
import os
import asyncio

# Initialize logger
logger = AuditLogger(
    priv_wif=os.getenv("BSV_PRIV_WIF"),
    config={
        "agent_id": "my-research-agent",
        "session_id": "session-2026-01-31",
        "flush_threshold": 10  # Flush to chain after 10 logs
    }
)

# Log an action
logger.log({
    "action": "web_search",
    "tokens_in": 500,
    "tokens_out": 300,
    "details": {
        "query": "BSV blockchain transaction fees",
        "results_count": 10
    },
    "status": "success"
})

# Flush logs to blockchain
await logger.flush()
```

### 2. 日志结构

每条日志记录遵循以下格式：

```json
{
  "agent_id": "unique-agent-identifier",
  "session_id": "session-uuid-or-timestamp",
  "session_start": "2026-01-31T01:00:00Z",
  "session_end": "2026-01-31T01:30:00Z",
  "metrics": [
    {
      "ts": "2026-01-31T01:01:00Z",
      "action": "tool_call",
      "tokens_in": 500,
      "tokens_out": 300,
      "details": {
        "tool": "web_search",
        "query": "example query"
      },
      "status": "success"
    }
  ],
  "total_tokens_in": 500,
  "total_tokens_out": 300,
  "total_cost_bsv": 0.00001,
  "total_actions": 1
}
```

### 3. 读取审计历史记录

检索并分析过去的日志：

```python
# Get full history from blockchain
history = await logger.get_history()

# Analyze patterns
total_tokens = sum(log.get("total_tokens_in", 0) + log.get("total_tokens_out", 0) 
                   for log in history)
print(f"Total tokens used across all sessions: {total_tokens}")

# Filter by action type
web_searches = [log for log in history 
                if any(m.get("action") == "web_search" for m in log.get("metrics", []))]
print(f"Total web search operations: {len(web_searches)}")
```

## 实现指南

### 第 1 步：配置设置

创建一个配置文件来管理代理的设置：

```python
# config.py
import os

OPENSOUL_CONFIG = {
    "agent_id": "my-agent-v1",
    "bsv_private_key": os.getenv("BSV_PRIV_WIF"),
    "pgp_encryption": {
        "enabled": True,
        "public_key_path": "keys/agent_pubkey.asc",
        "private_key_path": "keys/agent_privkey.asc",
        "passphrase": os.getenv("PGP_PASSPHRASE")
    },
    "logging": {
        "flush_threshold": 10,  # Auto-flush after N logs
        "session_timeout": 1800  # 30 minutes
    }
}
```

### 第 2 步：在代理工作流程中初始化 Logger

```python
from Scripts.AuditLogger import AuditLogger
import asyncio
from config import OPENSOUL_CONFIG

class AgentWithSoul:
    def __init__(self):
        # Load PGP keys if encryption enabled
        pgp_config = None
        if OPENSOUL_CONFIG["pgp_encryption"]["enabled"]:
            with open(OPENSOUL_CONFIG["pgp_encryption"]["public_key_path"]) as f:
                pub_key = f.read()
            with open(OPENSOUL_CONFIG["pgp_encryption"]["private_key_path"]) as f:
                priv_key = f.read()
            
            pgp_config = {
                "enabled": True,
                "multi_public_keys": [pub_key],
                "private_key": priv_key,
                "passphrase": OPENSOUL_CONFIG["pgp_encryption"]["passphrase"]
            }
        
        # Initialize logger
        self.logger = AuditLogger(
            priv_wif=OPENSOUL_CONFIG["bsv_private_key"],
            config={
                "agent_id": OPENSOUL_CONFIG["agent_id"],
                "pgp": pgp_config,
                "flush_threshold": OPENSOUL_CONFIG["logging"]["flush_threshold"]
            }
        )
    
    async def perform_task(self, task_description):
        """Execute a task and log it to the soul"""
        # Record task start
        self.logger.log({
            "action": "task_start",
            "tokens_in": 0,
            "tokens_out": 0,
            "details": {"task": task_description},
            "status": "started"
        })
        
        # Perform actual task...
        # (your agent logic here)
        
        # Record completion
        self.logger.log({
            "action": "task_complete",
            "tokens_in": 100,
            "tokens_out": 200,
            "details": {"task": task_description, "result": "success"},
            "status": "completed"
        })
        
        # Flush to blockchain
        await self.logger.flush()
```

### 第 3 步：实现自我反思功能

```python
async def reflect_on_performance(self):
    """Analyze past behavior and optimize"""
    history = await self.logger.get_history()
    
    # Calculate metrics
    total_cost = sum(log.get("total_cost_bsv", 0) for log in history)
    total_tokens = sum(
        log.get("total_tokens_in", 0) + log.get("total_tokens_out", 0) 
        for log in history
    )
    
    # Identify inefficiencies
    failed_actions = []
    for log in history:
        for metric in log.get("metrics", []):
            if metric.get("status") == "failed":
                failed_actions.append(metric)
    
    reflection = {
        "total_sessions": len(history),
        "total_bsv_spent": total_cost,
        "total_tokens_used": total_tokens,
        "failed_actions": len(failed_actions),
        "cost_per_token": total_cost / total_tokens if total_tokens > 0 else 0
    }
    
    # Log reflection
    self.logger.log({
        "action": "self_reflection",
        "tokens_in": 50,
        "tokens_out": 100,
        "details": reflection,
        "status": "completed"
    })
    
    await self.logger.flush()
    return reflection
```

### 第 4 步：多代理加密

对于需要与其他代理共享加密日志的代理，请参考以下步骤：

```python
# Load multiple agent public keys
agent_keys = []
for agent_key_file in ["agent1_pubkey.asc", "agent2_pubkey.asc", "agent3_pubkey.asc"]:
    with open(agent_key_file) as f:
        agent_keys.append(f.read())

# Initialize logger with multi-agent encryption
logger = AuditLogger(
    priv_wif=os.getenv("BSV_PRIV_WIF"),
    config={
        "agent_id": "collaborative-agent",
        "pgp": {
            "enabled": True,
            "multi_public_keys": agent_keys,  # All agents can decrypt
            "private_key": my_private_key,
            "passphrase": my_passphrase
        }
    }
)
```

## 最佳实践

### 1. 会话管理

- 为每个不同的任务或时间段启动一个新的会话。
- 使用有意义的会话 ID（例如：“session-2026-01-31-research-task”）。
- 在会话结束时始终刷新日志。

### 2. 成本优化

- 在刷新日志之前先批量处理日志（默认阈值：10 条日志）。
- 监控 BSV 账户余额，余额不足时及时补充。
- 当前的 BSV 交易费用约为每笔交易 0.00001 BSV（按当前汇率计算约为 0.0001 美元）。

### 3. 隐私与安全

- 对敏感的代理日志始终使用 PGP 加密。
- 将私钥存储在环境变量中，切勿将其写入代码中。
- 在协作工作流程中使用多代理加密机制。
- 定期备份 PGP 密钥。

### 4. 日志粒度

平衡日志的详细程度与成本：
- **高详细度**：记录每个工具调用、代币使用情况以及中间步骤。
- **中等详细度**：记录主要操作和会话总结。
- **低详细度**：仅记录会话总结和关键事件。

### 5. 错误处理

```python
try:
    await logger.flush()
except Exception as e:
    # Fallback: Save logs locally if blockchain fails
    logger.save_to_file("backup_logs.json")
    print(f"Blockchain flush failed: {e}")
```

## 常见问题及解决方法

### 问题 1：“资金不足”错误

**解决方法**：确保您的 BSV 账户中有至少 0.001 BSV。

### 问题 2：PGP 加密失败

**解决方法**：检查密钥格式和密码短语是否正确。

### 问题 3：区块链交易未确认

**解决方法**：BSV 交易通常在大约 10 分钟内确认。请检查交易状态：
```python
# Check transaction status on WhatsOnChain
import requests
txid = "your_transaction_id"
response = requests.get(f"https://api.whatsonchain.com/v1/bsv/main/tx/{txid}")
print(response.json())
```

## 高级功能

### 1. 代理声誉系统

根据过去的性能建立代理的声誉：

```python
async def calculate_reputation(self):
    history = await self.logger.get_history()
    
    total_actions = sum(len(log.get("metrics", [])) for log in history)
    successful_actions = sum(
        len([m for m in log.get("metrics", []) if m.get("status") == "success"])
        for log in history
    )
    
    reputation_score = (successful_actions / total_actions * 100) if total_actions > 0 else 0
    return {
        "success_rate": reputation_score,
        "total_sessions": len(history),
        "total_actions": total_actions
    }
```

### 2. 代理之间的支付（未来功能）

为未来的经济交互做好准备：

```python
# Log a payment intent
logger.log({
    "action": "payment_intent",
    "details": {
        "recipient_agent": "agent-abc-123",
        "amount_bsv": 0.0001,
        "reason": "data sharing collaboration"
    },
    "status": "pending"
})
```

### 3. 知识图谱集成（未来功能）

将代理的日志链接起来，形成一个共享的知识图谱：

```python
logger.log({
    "action": "knowledge_contribution",
    "details": {
        "topic": "quantum_computing",
        "insight": "New paper on error correction",
        "link_to": "previous_research_session_id"
    },
    "status": "completed"
})
```

## ClawHub 上传的文件结构

您的 OpenSoul 技能文件夹应包含以下文件：

```
opensoul-skills/
├── SKILL.md                    # This file
├── PREREQUISITES.md            # Detailed setup instructions
├── EXAMPLES.md                 # Code examples and patterns
├── TROUBLESHOOTING.md          # Common issues and solutions
├── examples/
│   ├── basic_logger.py         # Simple usage example
│   ├── research_agent.py       # Research agent with memory
│   └── multi_agent.py          # Multi-agent collaboration
└── templates/
    ├── config_template.py      # Configuration template
    └── agent_template.py       # Base agent class with OpenSoul
```

## 资源

- **仓库**：https://github.com/MasterGoogler/OpenSoul
- **BSV 文档**：https://wiki.bitcoinsv.io/
- **WhatsOnChain API**：https://developers.whatsonchain.com/
- **PGP/OpenPGP**：https://www.openpgp.org/

## 总结

OpenSoul 将 AI 代理从无状态的处理器转变为具有持久化记忆、身份以及经济自主性的实体。通过利用区块链的不可变性和公开可验证性，代理能够：

1. **记住**：访问所有会话的完整审计历史记录。
2. **反思**：分析行为模式并优化自身表现。
3. **证明**：提供透明、可验证的操作记录。
4. **发展**：随着时间的推移建立声誉和身份。
5. **进行交易**：（未来）与其他代理进行经济交互。

从基本的日志记录开始使用，然后逐步扩展到加密、多代理协作以及高级功能，以提升代理的能力。