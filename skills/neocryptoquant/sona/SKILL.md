---
name: sona
description: **自主运行的Solana钱包代理**：由AI进行逻辑判断，使用Rust语言处理交易签名。支持转账、交换、质押操作，同时提供聊天功能，并能在预设的支出限额范围内切换不同的使用模式。
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - SONA_TOKEN
      bins: []
      config: []
    primaryEnv: SONA_TOKEN
    homepage: https://www.sonawallet.xyz
    repository: https://github.com/Ubuntu-Technologies/sona
    emoji: "\U0001F4B0"
    os:
      - darwin
      - linux
      - win32
---
# SONA — 代理钱包技能

**类别**: 区块链 / 人工智能钱包  
**网络**: Solana（Devnet）  
**安装**: `clawhub install sona`  
**版本**: 1.0.1  

---

## 什么是SONA？  

SONA是一个自主的Solana钱包代理。它会监控您的链上钱包，根据您的YAML策略规则进行操作，并执行交易和转账——所有操作都受到四项“宪法法则”的约束，这些法则任何人工智能都无法违背。  

```
Observe → Reason → Decide → Execute
```  

所有操作都受到宪法法则的约束：每次操作的最大花费为5000万lamports（由Rust语言强制执行），并且每笔交易都会附带一个链上的备忘录（Memo）记录。  

---

## 插件工具（10个）  

| 工具 | 参数 | 描述 |  
|------|------------|-------------|  
| `get_wallet_status` | — | SOL余额、地址、模式、周期统计信息 |  
| `get_sol_price` | — | 通过Pyth Hermes预言机获取实时的SOL/USD汇率 |  
| `get_agent_status` | — | 模式、当前运行状态、已执行的周期数、上一个周期的结束时间 |  
| `set_mode` | `mode`, `acknowledgment?` | 在标准模式、辅助模式或“上帝模式”之间切换（需要授权） |  
| `get_policy` | — | 当前的YAML策略规则及消费限额 |  
| `transfer_sol` | `to`, `amount_sol` | 转移SOL——所有操作都遵循宪法法则（需要授权） |  
| `get_pending_actions` | — | 辅助模式下的待批准操作队列（需要授权） |  
| `approve_action` | `cycle_id` | 批准队列中的操作以供执行（需要授权） |  
| `chat` | `message` | 向SONA AI发送自然语言指令（需要授权） |  
| `get_activity` | `limit?` | 最近的代理活动摘要 |  

---

## 设置流程  

### 1. 启动SONA  

```bash
git clone <repo>
cd <repo>
bun install
bun run sona init   # set passphrase, create wallet
bun run sona start  # agent starts on port 3000
```  

### 2. 获取会话令牌  

```bash
curl -s -c cookies.txt -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_user","password":"your_pass"}' | jq -r '.token'
```  

### 3. 设置环境变量  

```bash
export SONA_API_URL=http://localhost:3000
export SONA_TOKEN=<token-from-step-2>
```  

### 4. 安装该技能  

```bash
clawhub install sona
```  

---

## 宪法法则  

所有操作都受到四项不可更改的法则的约束。任何工具调用都无法绕过这些法则：  

| 法则 | 名称 | 执行方式 |  
|-----|------|-------------|  
| I | 所有者至高无上 | 您的YAML策略优先于所有人工智能的判断 |  
| II | 消费限制 | 每次操作的最大花费为5000万lamports（由Rust语言强制执行） |  
| III | 完全透明 | 每笔交易都会附带链上的备忘录记录 |  
| IV | 安全停机机制 | 如果模拟失败，代理将停止运行，资金将保持原状 |  

---

## 代理操作流程示例  

```
Agent: "Check SONA's wallet balance"
→ calls get_wallet_status
→ returns: 4.82 SOL, god mode, 142 cycles run

Agent: "Transfer 0.1 SOL to vault"
→ calls transfer_sol { to: "vault", amount_sol: 0.1 }
→ SONA reasons, simulates, executes within Law II limit
→ returns: tx confirmed, Memo logged on-chain

Agent: "What is the current SOL price?"
→ calls get_sol_price
→ returns: $142.30 USD (Pyth Hermes)
```  

---

## 必需的环境变量  

| 变量 | 是否必需 | 默认值 | 描述 |  
|----------|----------|---------|-------------|  
| `SONA_API_URL` | 否 | `http://localhost:3000` | SONA控制台的基本URL |  
| `SONA_TOKEN` | 是 | — | JWT会话令牌（所有更改状态的操作均需使用） |  

仅用于读取数据的工具（`get_wallet_status`, `get_sol_price`, `get_agent_status`, `get_policy`, `get_activity`）无需令牌即可使用。所有更改状态的工具都需要`SONA_TOKEN`。