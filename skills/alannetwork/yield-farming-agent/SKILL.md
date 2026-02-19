---
name: yieldvault-agent
description: 专为 BNB Chain 设计的自主收益 farming（收益获取）代理系统，具备确定性执行能力、智能合约集成功能以及自动化决策机制。
---
# YieldVault Agent

这是一个专为 BNB Chain 设计的自动化收益 farming（收益获取）代理工具，具备确定性执行能力、智能合约集成功能以及自动决策机制。

## 主要特性

- **确定性决策引擎**：相同的输入总是产生相同的输出（可审计）
- **智能合约集成**：能够与 BNB 测试网/主网上的 YieldVault 合约进行交互
- **自主调度器**：每小时自动执行收益 farming 操作，无需人工干预
- **交易执行器**：自动执行存款（DEPOSIT）、取款（WITHDRAW）、收获（HARVEST）、复利（COMPOUND）和再平衡（REBALANCE）等操作
- **Telegram 通知**：实时推送执行结果、年化收益率（APR）变化以及错误信息
- **风险管理**：仅选择风险评分（risk_score）≤ 0.5 的钱包进行操作
- **收益优化**：计算净年化收益率（Net APR）= 年化收益率（APR）- 手续费（fees）- 风险惩罚（risk_penalty）

## 安装

```bash
clawhub install yieldvault-agent
```

## 快速入门

### 1. 配置

```bash
cp config.deployed.json .env.local
# Edit with your contract addresses and RPC endpoint
```

### 2. 部署合约（如需要）

```bash
cd contracts
npm install
npm run deploy:testnet
```

### 3. 运行测试

```bash
npm test                    # Unit tests
node test.live.mock.js      # Integration tests (offline)
node test.live.js           # Live testnet tests
```

### 4. 启动调度器

```bash
node scheduler.js
# Runs decision cycle every hour against testnet
```

### 5. 监控通知

系统会自动发送 Telegram 通知，内容包括：
- 操作开始（vault_id、操作类型、金额）
- 年化收益率变化（变化幅度超过 1%）
- 错误信息（包含错误等级）
- 操作周期完成情况（包含统计摘要）

## 架构

```
Smart Contracts (BNB Testnet/Mainnet)
    ↓
BlockchainReader (live vault data)
    ↓
YieldFarmingAgent (deterministic decisions)
    ↓
TransactionExecutor (sign & broadcast)
    ↓
Scheduler (hourly automation)
    ↓
Notifications (Telegram alerts)
```

## 配置

请编辑 `configscheduler.json` 文件：

```json
{
  "chainId": 97,
  "interval_minutes": 60,
  "harvest_threshold_usd": 25,
  "rebalance_apr_delta": 0.02,
  "max_allocation_percent": 0.35,
  "risk_score_threshold": 0.5
}
```

## 决策逻辑

1. **读取** 当前钱包的状态（年化收益率 APR、总价值 TVL、用户余额）
2. **计算** 净年化收益率（Net APR）= 年化收益率（APR）- 手续费（fees）- 风险惩罚（risk_score × 0.10）
3. **筛选** 风险评分（risk_score）≤ 0.5 的钱包
4. **选择** 净年化收益率最高的钱包
5. **决定** 执行操作：
   - 如果待领取的收益（pending_rewards）≥ 25 美元，则执行收获（HARVEST）操作
   - 如果净年化收益率（net_apr）增长超过 2%，则执行复利（COMPOUND）操作
   - 如果有其他钱包的收益增长幅度超过当前钱包 2%，则执行再平衡（REBALANCE）操作
   - 如果钱包已经达到最优状态，则不执行任何操作（NOOP）
6. **执行** 交易（包含重试机制）
7. **记录** 执行日志（使用 SHA256 算法进行审计）

## 支持的网络

- **测试网：** BNB Chain 测试网（chainId: 97）
- **主网：** BNB Chain 主网（chainId: 56）

## 安全性

- ✅ 执行过程具有确定性（可重复、可审计）
- ✅ 每个决策操作都有 SHA256 算法生成的审计记录
- ✅ 采用保守的风险筛选策略
- ✅ 限制每个钱包的最大投资比例（不超过 35%）
- ✅ 采用指数级重试机制
- ✅ 不使用硬编码的私钥（使用环境变量）

## 生产环境准备

在主网部署前，请完成以下准备工作：
- **Chainlink Oracle**：获取实时的年化收益率数据
- **硬件钱包支持**：支持 Ledger/Trezor 等硬件钱包的签名功能
- **智能合约审计**：请专业团队对智能合约进行安全审查
- **紧急暂停机制**：具备多签名（multi-sig）暂停功能

详细的生产环境要求请参阅 `FINAL_CHECKLIST.md` 文件。

## 文档资料

- `README.md`：完整用户指南
- `SKILL.md`：本文档
- `FINAL_CHECKLIST.md`：生产环境要求
- `INTEGRATION_GUIDE.md`：智能合约集成指南
- `EXAMPLES.md`：使用示例
- `RESPUESTAS_PREGUNTAS.md`：常见问题解答与架构说明

## 技术支持

欢迎提交问题或 Pull Request：https://github.com/open-web-academy/yieldvault-agent-bnb

## 许可证

MIT 许可证