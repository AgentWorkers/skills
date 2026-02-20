---
name: clawtrade-bnb
version: 1.1.0
description: 基于 BNB 链路的自主 DeFi 交易代理，具备多策略引擎、网络切换功能以及强化学习技术。
keywords: trading, defi, autonomous-agent, multi-strategy, reinforced-learning, bnb-chain
---
# CawTrade BNB - 自动化去中心化金融（DeFi）交易代理 v1.1.0

这是一个专为 BNB 链路的测试网（Testnet）和主网（Mainnet）设计的自动化交易代理。它具备三种智能交易策略、实时性能分析功能、链上事件记录机制以及自我优化的强化学习能力。

## 核心特性

### 🤖 三种自动化交易策略
1. **复合收益（Compound Yield）**：自动将获得的奖励重新投资以实现指数级增长。
2. **再平衡（Rebalance）**：自动将资金从低年利率（APR）的账户转移到高年利率的账户。
3. **动态收割（Dynamic Harvest）**：根据gas成本优化进行智能收割。

### 🌐 网络切换
- 可即时在测试网和主网之间切换（无需重启）。
- 每个网络都有独立的配置设置（gas费用、阈值、RPC调用等）。
- 每个链路的合约地址都进行了映射。
- 网络偏好设置可持久保存。

### 📊 实时分析
- 实际年利率（基于历史收益计算）。
- 每个账户的性能详细报告。
- 交易策略效果评分。
- 成功率跟踪（目标：>90%）。
- 失败模式检测。

### 🧠 强化学习（Reinforced Learning）
- 从过去的失败中自动学习。
- 动态优化交易策略参数。
- 根据成功率调整阈值。
- 为每种策略生成置信度评分。
- 随时间自我提升。

### ⛓️ 链上事件记录
- 所有操作都会附带交易哈希（TX hash）进行记录。
- 提供可审计的区块链交易记录。
- 提供 BNB 测试网扫描工具链接。
- 完整的执行历史记录。

### 🎮 控制面板 CLI
- 提供交互式的命令行界面。
- 支持网络管理命令。
- 显示性能指标。
- 跟踪学习进度。
- 实时优化策略。

## 安装与配置

### 1. 安装 CawTrade
```bash
clawhub install clawtrade-bnb
cd ~/.openclaw/workspace/skills/clawtrade-bnb
npm install
```

### 2. 配置环境
```bash
# Copy example config
cp config.deployed.json config.live.json

# Edit with your settings
nano config.live.json
# Set RPC endpoint, contract addresses, wallet
```

### 3. 设置私钥（确保安全）
```bash
# Option A: Environment variable (recommended)
export PRIVATE_KEY="your_testnet_private_key"

# Option B: .env file (git-ignored)
echo "PRIVATE_KEY=your_key" >> .env

# NOTE: Never commit private keys!
```

### 4. 验证配置
```bash
# Test connection and contracts
node agent-cli.js network status

# Check wallet balance
npm run verify
```

## 快速启动 - 三个命令
```bash
# Terminal 1: Run strategy engine (60-second cycles)
node strategy-scheduler.js

# Terminal 2: Real-time dashboard
npm run dev:dashboard
# → Open http://localhost:5173

# Terminal 3: Control panel
node agent-cli.js

# Example commands:
node agent-cli.js network testnet        # Switch network
node agent-cli.js perf summary           # See performance
node agent-cli.js learn now              # Optimize strategies
```

## 架构概述
```
DeFi Strategy Engine
├─ Compound Yield Strategy
│  └─ Harvest when pending > $25 → Re-deposit
├─ Rebalance Strategy
│  └─ Move 20% from low-APR to high-APR vault
└─ Dynamic Harvest Strategy
   └─ Harvest only if pending > 2x gas cost

         ↓ (runs every 60 seconds)

Strategy Scheduler
├─ Read vault APRs & pending rewards
├─ Execute all 3 strategies
└─ Log actions + TX hashes

         ↓ (logs to blockchain)

On-Chain Logger
├─ execution-log.jsonl (append-only)
├─ performance-metrics.json (cumulative)
└─ learning-state.json (optimization history)

         ↓ (analyzes continuously)

Reinforced Learning System
├─ Tracks success rates per strategy
├─ Detects failure patterns
├─ Auto-adjusts thresholds
└─ Generates improvement reports

         ↓ (displays real-time)

Dashboard + Control Panel
├─ React dashboard (http://localhost:5173)
├─ Agent CLI (network, perf, learn commands)
└─ Performance API (/api/logs, /api/health)
```

## 配置文件

- **config.deployed.json**：包含合约地址和ABI（Application Binary Interface）。
```json
{
  "chainId": 97,
  "network": "BNB Testnet",
  "contracts": [
    {
      "vaultId": "vault_eth_staking_001",
      "address": "0x588eD88A145144F1E368D624EeFC336577a4276b",
      "strategy": "Ethereum 2.0 Staking",
      "risk_score": 0.3
    }
  ]
}
```

- **config scheduler.json**：设置策略阈值。
```json
{
  "scheduler": {
    "execution_interval_seconds": 60,
    "enabled": true
  },
  "agent": {
    "harvest_threshold_usd": 25,
    "rebalance_apr_delta": 2.0,
    "max_allocation_percent": 0.35,
    "min_confidence": 0.6
  }
}
```

## 交易策略逻辑

每 60 秒执行一次以下操作：

1. **复合收益（Compound Yield）**：
   - 检查每个账户的待收获奖励。
   - 如果待收获奖励 ≥ $25，则进行收割并重新投资。
   - 将操作记录到交易日志中（附带交易哈希）。

2. **再平衡（Rebalance）**：
   - 比较所有账户的年利率。
   - 如果最高年利率与最低年利率之间的差异 ≥ 2%，则进行资金再平衡。
   - 将 20% 的资金从表现较差的账户转移到表现较好的账户。
   - 将操作记录到交易日志中（附带交易哈希）。

3. **动态收割（Dynamic Harvest）**：
   - 估算每次收割所需的 gas 成本。
   - 仅当待收获奖励大于 gas 成本的 2 倍时才进行收割。
   - 优化每次操作的最大盈利能力。
   - 将操作记录到交易日志中（附带交易哈希）。

**示例输出：**
```
Cycle #42 @ 2026-02-18T18:00:00Z
✓ vault_eth_staking_001: COMPOUND ($45.50 harvested)
✓ vault_high_risk_001: REBALANCE (2.1% APR delta)
✓ vault_link_oracle_001: HARVEST ($12.30 pending)
✅ Total Rewards: $57.80 | Compounded: $45.50
```

## 命令行接口（CLI）命令

### 网络管理
```bash
node agent-cli.js network status      # Current network config
node agent-cli.js network testnet     # Switch to testnet
node agent-cli.js network mainnet     # Switch to mainnet (⚠️ production)
```

### 性能监控
```bash
node agent-cli.js perf summary        # Quick stats
node agent-cli.js perf report         # Detailed analysis
node agent-cli.js perf vaults         # Per-vault breakdown
node agent-cli.js perf strategies     # Strategy effectiveness
```

### 强化学习
```bash
node agent-cli.js learn now           # Analyze & optimize
node agent-cli.js learn report        # View improvements
node agent-cli.js learn reset         # Reset learning state
```

## 支持的网络

| 网络 | 链路 ID | 使用场景 | 最低收割金额 | Gas 成本倍数 |
|---------|----------|----------|-------------|----------------|
| BNB 测试网 | 97 | 开发环境 | $25 | 1.2倍 |
| BNB 主网 | 56 | 生产环境 | $100 | 1.5倍 |

## 网络切换

无需重启即可即时切换网络：
```bash
# Current config
node agent-cli.js network status
# → BNB Testnet

# Switch to production
node agent-cli.js network mainnet
# → Updated RPC, contract addresses, and thresholds

# All settings updated automatically
```

## 安全性与可靠性

### 链上审计
- 所有操作都会附带交易哈希进行记录。
- 通过 BNB 测试网/主网扫描工具进行区块链验证。
- 使用只读执行日志文件（execution-log.jsonl）。
- 提供完整的审计追踪记录以确保合规性。

### 风险管理
- 决策逻辑具有确定性（可复现、可审计）。
- 成功率监控（目标：>90%）。
- 为每种策略设置置信度阈值。
- 具有优雅的错误处理和恢复机制。
- 通过学习机制自动优化参数。

### 私钥安全
- 私钥从不硬编码，仅通过环境变量存储。
- .env 文件被 Git 忽略（防止泄露）。
- 开发阶段使用测试网，准备就绪后使用主网。
- 生产环境建议使用硬件钱包。

## 文件结构
```
clawtrade-bnb/
├── defi-strategy-engine.js          # 3 strategies (compound, rebalance, harvest)
├── on-chain-logger.js                # Event logging with TX hashes
├── strategy-scheduler.js              # Main loop (60s cycles)
├── network-switcher.js                # Testnet ↔ mainnet toggle
├── performance-analytics.js           # Real APR & metrics
├── reinforced-learning.js             # Self-improving parameters
├── agent-cli.js                       # Control panel
├── dashboard/                         # React frontend (real-time)
├── contracts/                         # Vault smart contracts
├── config.deployed.json               # Contract addresses & ABIs
├── config.scheduler.json              # Strategy thresholds
├── execution-log.jsonl                # Action history (generated)
├── performance-metrics.json           # Metrics (generated)
├── learning-state.json                # Learning progress (generated)
├── README.md                          # User guide
├── README_STRATEGY.md                 # Strategy details
├── README_ADVANCED.md                 # Network switching & learning
├── SKILL.md                           # This file
└── package.json                       # Dependencies
```

## 与其他组件的集成

CawTrade 是一个独立的、功能完备的交易代理。它还可以与其他组件集成，例如：

- **Telegram 通知**：向 OpenClaw 用户发送警报。
- **电子邮件报告**：每日性能总结。
- **数据库日志**：将指标存储在持久化数据库中。
- **Webhook 集成**：触发外部服务。

## 文档资料

| 文件 | 用途 |
|------|---------|
| `README.md` | 完整的用户指南 |
| `README_STRategy.md` | 交易策略详情及示例 |
| `README_ADVANCED.md` | 网络切换与强化学习机制 |
| `SKILL.md` | 安装与架构指南 |

## 你将获得什么

- **适用于生产环境的代码**（经过测试、有文档支持且具备错误处理功能）。
- **三种盈利策略**（自动优化、自我学习）。
- **实时性能仪表盘**（基于 React 的实时更新）。
- **CLI 控制面板**（通过终端进行管理）。
- **链上日志记录**（可审计、透明度高）。
- **即时网络切换功能**（可在几秒内完成测试网到主网的切换）。
- **自我优化能力**（能从失败中自动学习）。
- **完整的文档资料**（包括使用指南、示例和常见问题解答）。

## 复制本交易代理的步骤

其他人可以按照以下步骤进行复制：

1. **安装**：```bash
   clawhub install clawtrade-bnb
   npm install
   ```
2. **配置**：```bash
   # Edit config files with your contracts & RPC
   nano config.deployed.json
   ```
3. 部署合约（如需使用新的账户）：```bash
   cd contracts && npm run deploy:testnet
   ```
4. 运行：```bash
   node strategy-scheduler.js      # Main engine
   npm run dev:dashboard           # Dashboard
   node agent-cli.js               # Control panel
   ```
5. 监控：
   - 仪表盘：http://localhost:5173
   - 日志文件：execution-log.jsonl
   - 分析报告：node-agent-cli.js

**总设置时间：约 15 分钟**

## 支持与社区资源

- GitHub 问题反馈：https://github.com/open-web-academy/clawtrade-bnb-bnb
- ClawHub：https://clawhub.com（搜索：clawtrade-bnb）
- Discord：https://discord.com/invite/clawd

## 版本历史

- **v1.1.0**（2026-02-18）：添加网络切换功能、性能分析机制和强化学习功能。
- **v1.0.0**（2026-02-17）：初始版本，包含三种交易策略和链上记录功能。

## 许可证

MIT 许可证 - 可自由使用、修改和分发。