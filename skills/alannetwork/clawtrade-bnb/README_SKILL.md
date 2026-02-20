# ClawTrade-BNB — OpenClaw 技能  

**一个具备可解释性、多智能体用户界面以及一键激活功能的自主去中心化金融（DeFi）交易代理。**  

> 安装它。配置它。激活它。然后观看它的交易过程。  

---

## 功能介绍  
**ClawTrade-BNB** 是一个专为 BNB 链开发的、可投入实际使用的自主收益 farming（收益 farming）与资产再平衡代理工具：  
- ✅ 每 60 秒执行一次智能交易策略  
- ✅ 生成真实的链上交易记录（可在 BscScan 上验证）  
- ✅ 显示每个决策的依据（通过“可解释性”面板展示）  
- ✅ 实时监控所有智能体的运行状态（多智能体用户界面）  
- ✅ 具备自动学习和优化能力（基于强化学习机制）  
- 支持三种风险策略配置（保守型/平衡型/激进型）  
- 可以切换至“仅建议”模式（不执行交易，仅生成交易提案）  

---

## 快速入门（3 个步骤）  
### 1. 安装与配置  
```bash
# Install dependencies
npm install

# Copy config
cp .env.example .env

# Edit .env with your testnet private key
nano .env
# (Add PRIVATE_KEY=your_key)
```  

### 2. 启动代理并查看仪表盘  
```bash
npm run start
```  
**操作结果：**  
```
✅ Agent API: http://localhost:3001
✅ Dashboard: http://localhost:5173
✅ Network: testnet
```  

### 3. 打开浏览器  
```
http://localhost:5173
```  
接下来：  
1. 点击“激活代理”  
2. 选择风险策略（保守型/平衡型/激进型）  
3. 查看实时交易记录  
4. 点击交易操作的“原因”部分查看决策依据  
5. 点击交易哈希值，查看 BscScan 的交易验证结果  

---

## 配置文件（.env）  
```bash
# ⚠️ SECURITY: Use testnet keys only. Never commit real keys.

PRIVATE_KEY=6d816d...          # Your wallet private key (testnet)
RPC_URL=https://bsc-testnet... # BNB Testnet RPC (default provided)
NETWORK=testnet                # testnet or mainnet
OPERATOR_MODE=auto_execute     # auto_execute or suggest_only
RISK_PROFILE=balanced          # conservative, balanced, aggressive
AGENT_PORT=3001                # Agent API port
UI_PORT=5173                   # Dashboard port
DEMO_MODE=true                 # Use env wallet (no wallet connect needed)
```  

### 风险策略配置  
| 策略类型 | 最小投资额 | 年化收益率波动率 | 每笔交易的最大Gas费用 | 是否集中投资 | 适用场景 |  
|---------|-----------|-----------|-----------|-------------|----------|  
| **保守型** 🛡️ | $30 | 3.0% | 1.5x | 否 | 安全、稳定 |  
| **平衡型** ⚖️ | $25 | 2.0% | 2.0x | 是（适度风险） | 推荐使用 |  
| **激进型** 🚀 | $15 | 1.0% | 1.2x | 是（高风险） | 高收益 |  

---

## 常用命令  
```bash
# Start everything
npm run start

# Start only agent (no UI)
npm run agent start

# Start only dashboard
npm run dev:dashboard

# Show status
npm run status

# Tail logs
npm run logs [--limit 20] [--filter HARVEST]

# Switch network
npm run network testnet|mainnet

# Show metrics
npm run metrics [--json]

# Show demo checklist
npm run demo

# CLI help
npm run help
```  

---

## 仪表盘用户界面  
### 主页（/）  
- 产品概述（15 秒展示）  
- 主要功能  
- 应用程序快速链接  

### 操作员面板（/app）  
**左侧侧边栏：**  
- 连接钱包、选择策略类型、激活代理  
- 实时交易记录（最近 20 笔交易）  
- 分析数据（性能指标）  
- 设置（网络配置、运行模式、风险策略）  

**主要内容：**  
- 代理运行状态信息（策略、风险水平、执行情况、学习进度）  
- 实时交易记录及决策依据  
- 状态指示灯（🟢：活跃状态；🔴：出现错误）  

### “可解释性”功能  
点击任何交易操作的“原因”部分，即可查看该操作的决策依据：  
```json
{
  "decision": {
    "profile": "balanced",
    "mode": "auto_execute",
    "confidence": 0.95,
    "rules_triggered": [
      "pending_yield_above_threshold",
      "acceptable_gas_ratio"
    ],
    "metrics_snapshot": {
      "yield_usd": 50.00,
      "gas_usd": 5.50,
      "aprs": { "vault1": 8.5, "vault2": 6.2 },
      "delta_pct": 2.3
    },
    "agent_trace": [
      { "agent": "CompoundYield", "message": "Pending yield $50 exceeds threshold", "ts": "18:00:00" },
      { "agent": "GasOptimizer", "message": "Gas cost acceptable (2.1x threshold)", "ts": "18:00:02" }
    ]
  }
}
```  

---

## API 接口  
该技能提供了用于用户界面和集成的 HTTP API：  
```bash
# Health check
curl http://localhost:3001/api/health

# Current status
curl http://localhost:3001/api/status

# Performance metrics
curl http://localhost:3001/api/metrics

# Recent actions (limit=20)
curl http://localhost:3001/api/actions?limit=20

# Action detail with explainability
curl http://localhost:3001/api/actions/cycle-42

# Activate operator
curl -X POST http://localhost:3001/api/operator/activate \
  -H "Content-Type: application/json" \
  -d '{"profile":"balanced"}'

# Pause agent (safe)
curl -X POST http://localhost:3001/api/operator/pause

# Switch mode
curl -X POST http://localhost:3001/api/operator/mode \
  -H "Content-Type: application/json" \
  -d '{"mode":"suggest_only"}'
```  

---

## 演示流程（60 秒）  
**0:00** — 打开 http://localhost:5173（仪表盘首页）  
**0:10** — 点击“打开应用程序”  
**0:15** — 用户界面加载完成（显示操作员信息及代理运行状态）  
**0:20** — 选择风险策略（平衡型）  
**0:25** — 点击“激活代理”  
**0:30** — 第一个交易周期开始执行，交易记录显示在界面中  
**0:40** — 点击交易操作的“原因”部分，查看决策依据  
**0:45** — 点击交易哈希值，查看 BscScan 的交易验证结果  
**0:55** — 查看代理团队的实时运行状态  

---

## 架构概述  
```
Skill Root
├── skill.json           (OpenClaw manifest)
├── package.json         (dependencies + scripts)
├── .env.example         (configuration template)
├── README_SKILL.md      (this file)
│
├── src/
│  ├── cli.js           (command interface)
│  ├── risk-profiles.js (strategy parameters)
│  ├── defi-strategy-engine.js (core execution)
│  ├── reinforced-learning.js (auto-optimization)
│  ├── performance-analytics.js (metrics)
│  └── network-switcher.js (testnet ↔ mainnet)
│
├── server.js           (API + log reader)
├── api/                (REST endpoints)
│  └── logs.js
│
├── dashboard/          (React frontend)
│  └── src/
│     ├── App.tsx       (main UI)
│     └── components/
│        ├── Operator.tsx
│        ├── AgentTeam.tsx
│        ├── ActivityFeed.tsx
│        └── Explainability.tsx
│
├── execution-log.jsonl (append-only action log)
└── performance-metrics.json (cumulative metrics)
```  

---

## 常见问题与解决方法  
### “RPC 连接失败”  
- 检查 `.env` 文件中的 `RPC_URL` 设置  
- 备用链接：https://bsc-testnet.publicnode.com  

### “私钥无效”  
- 确保私钥为十六进制格式（如 `0x...`）或原始二进制格式  
- 请在演示环境中仅使用测试网钱包，切勿使用主网私钥  

### 端口已被占用  
- 更改 `.env` 文件中的 `AGENT_PORT` 或 `UI_PORT` 值  
- 或者手动终止相关进程：`lsof -ti:3001 | xargs kill -9`  

### 无日志输出  
- 等待第一个交易周期完成（约 60 秒）  
- 检查钱包余额（测试网钱包中需持有至少 0.01 BNB）  
- 运行 `npm run logs` 查看日志信息  

### 仪表盘为空或 API 返回 404 错误  
- 确保服务器已启动：`npm run start`  
- 检查控制台是否有错误信息  
- 尝试访问 `localhost:3001/api/health`  

---

## 安全注意事项  
⚠️ **严禁：**  
- 不要将 `.env` 文件或真实私钥上传至 Git 仓库  
- 在演示环境中切勿使用主网私钥  
- 不要在日志或截图中泄露私钥信息  

✅ **推荐做法：**  
- 开发阶段使用测试网钱包  
- 主网环境使用硬件钱包  
- 如有疑问，可切换至“仅建议”模式  

---

## 面向黑客马拉松的特色功能  
**ClawTrade-BNB** 搭载了以下三项在黑客马拉松中获奖的功能：  
### 1️⃣ 一键激活功能  
- 用户通过用户界面按钮即可激活代理  
- 代理自动执行三种交易策略  
- 无需手动进行交易操作  

### 2️⃣ 可解释性功能  
- 点击任何交易操作的“原因”部分，可查看决策依据及置信度  
- 查看代理的完整操作流程（谁执行了什么、何时执行的）  
- 获取决策时的各项指标数据  

### 3️⃣ 多智能体可视化界面  
- 实时监控所有智能体的运行状态  
- 显示策略、风险水平、执行情况、学习进度等信息  
- 提供实时交易记录及结果的颜色编码显示  

---

## 更多资源  
- [SKILL.md](./SKILL.md) — 完整的功能说明文档  
- [REPLICATION_GUIDE.md](./REPLICATION_GUIDE.md) — 他人使用的安装指南  
- [GitHub](https://github.com/open-web-academy/clawtrade-bnb) — 源代码仓库  

---

## 技术支持  
**遇到问题？**  
1. 查阅上述故障排除方法  
2. 运行 `npm run logs` 查看最近的交易记录  
3. 检查 RPC 连接状态及钱包余额  
4. 使用 `npm run logs` 的输出信息在 GitHub 上提交问题  

**想要贡献代码？**  
- 克隆项目仓库  
- 创建新的功能分支  
- 提交包含测试代码的 Pull Request  

---

**版本信息：** 1.1.0  
**许可证：** MIT  
**适用范围：** 已准备好在黑客马拉松及其他场景中使用  

---