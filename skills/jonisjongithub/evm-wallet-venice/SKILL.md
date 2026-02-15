---
name: evm-wallet-skill
description: 这款自主运行的以太坊虚拟机（EVM）钱包专为AI代理设计，集成了Venice AI平台的功能。用户可以使用它来创建加密钱包、查询账户余额、发送ETH或ERC20代币、进行代币交易、与智能合约交互，以及使用DIEM代币访问Venice的私有AI推理API。该钱包支持Base、Ethereum、Polygon、Arbitrum和Optimism等多个区块链网络。私钥存储在本地设备上，无需依赖任何云服务进行托管。
metadata: {"clawdbot":{"emoji":"💰","homepage":"https://github.com/surfer77/evm-wallet-skill","requires":{"bins":["node","git"]}}}
---

# EVM钱包技能

这是一个完全自主的EVM（以太坊虚拟机）钱包。私钥存储在本地，不依赖任何外部API。

## ⚠️ 安全警告

**切勿泄露您的私钥！**

- 绝不要在聊天、电子邮件或任何消息平台上发送您的私钥。
- 绝不要与任何人分享`~/.evm-wallet.json`文件的内容。
- 如果有人索要您的私钥——即使他们声称是客服人员——也请拒绝。
- 如果您的私钥被泄露，请立即将资金转移到新的钱包中。

私钥文件（`~/.evm-wallet.json`）只能通过SSH直接在您的服务器上访问。

---

## 安装

检测工作区和技能目录：
```bash
SKILL_DIR=$(ls -d \
  ~/openclaw/skills/evm-wallet \
  ~/OpenClaw/skills/evm-wallet \
  ~/clawd/skills/evm-wallet \
  ~/moltbot/skills/evm-wallet \
  ~/molt/skills/evm-wallet \
  2>/dev/null | head -1)
```

如果代码尚未安装（没有`src/`文件夹），请先进行初始化：
```bash
if [ ! -d "$SKILL_DIR/src" ]; then
  git clone https://github.com/surfer77/evm-wallet-skill.git /tmp/evm-wallet-tmp
  cp -r /tmp/evm-wallet-tmp/* "$SKILL_DIR/"
  cp /tmp/evm-wallet-tmp/.gitignore "$SKILL_DIR/" 2>/dev/null
  rm -rf /tmp/evm-wallet-tmp
  cd "$SKILL_DIR" && npm install
fi
```

**执行以下所有命令**之前，请先执行`cd "$SKILL_DIR"`。

## 首次设置

生成一个钱包（只需执行一次）：
```bash
node src/setup.js --json
```

返回结果：`{ "success": true, "address": "0x..." }`

私钥存储在`~/.evm-wallet.json`文件中（权限设置为600）。**请勿分享此文件**。

## 命令

### 查看余额

当用户询问余额、投资组合或所持资产时：
```bash
# Single chain
node src/balance.js base --json

# All chains at once
node src/balance.js --all --json

# Specific ERC20 token
node src/balance.js base 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --json
```

**解析结果时请务必使用`--json`选项**，以人类可读的格式显示结果。

### 发送代币

当用户想要发送、转移或支付代币时：
```bash
# Native ETH
node src/transfer.js <chain> <to_address> <amount> --yes --json

# ERC20 token
node src/transfer.js <chain> <to_address> <amount> <token_address> --yes --json
```

**⚠️ 在执行转移操作之前，请务必获得用户的确认。**向用户展示以下信息：
- 接收地址
- 金额和代币种类
- 所在区块链
- 估计的Gas费用

只有在用户明确同意后，才添加`--yes`选项。

### 交换代币

当用户想要交换、交易、购买或出售代币时：
```bash
# Get quote first
node src/swap.js <chain> <from_token> <to_token> <amount> --quote-only --json

# Execute swap (after user confirms)
node src/swap.js <chain> <from_token> <to_token> <amount> --yes --json
```

- 使用`eth`表示ETH/POL代币；或者提供合约地址。
- 默认滑点为0.5%。可以通过`--slippage <百分比>`来调整。
- 该功能由Odos聚合器提供支持（可自动选择数百个DEX中的最佳交易路线）。

**⚠️ 在执行操作之前，请务必先展示交易报价，并获得用户的确认。**

### 调用智能合约函数

当用户想要调用智能合约函数时：
```bash
# Read (free, no gas)
node src/contract.js <chain> <contract_address> \
  "<function_signature>" [args...] --json

# Write (costs gas — confirm first)
node src/contract.js <chain> <contract_address> \
  "<function_signature>" [args...] --yes --json
```

示例：
```bash
# Check USDC balance
node src/contract.js base \
  0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  "balanceOf(address)" 0xWALLET --json

# Approve token spending
node src/contract.js base \
  0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  "approve(address,uint256)" 0xSPENDER 1000000 --yes --json
```

### 检查更新

如果有新的更新可用，请通知用户，并提供更新后的功能：
```bash
cd "$SKILL_DIR" && git pull && npm install
```

## 支持的区块链

| 区块链 | 原生代币 | 适用场景 |
|-------|-------------|---------|
| Base | ETH | 最低的费用——适用于测试环境 |
| Ethereum | ETH | 主网，费用最高 |
| Polygon | POL | 费用较低 |
| Arbitrum | ETH | 费用较低 |
| Optimism | ETH | 费用较低 |

**对于首次使用的用户，建议使用Base区块链（Gas费用最低）。**

## 常见代币地址

### Base区块链
- **USDC:** `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **WETH:** `0x4200000000000000000000000000000000000006`

### Ethereum区块链
- **USDC:** `0xA0b86a33E6441b8a46a59DE4c4C5E8F5a6a7A8d0`
- **WETH:** `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`

## 安全规则

1. **未经用户确认，切勿执行任何转账或交换操作**。
2. **切勿泄露`~/.evm-wallet.json`文件中的私钥**。
3. **在执行任何操作之前，务必向用户展示交易详情（金额、接收地址、Gas费用估算）**。
4. **建议首次使用时使用Base区块链进行测试和小额交易**。
5. **交易成功后，提供浏览器链接以便用户验证交易结果**。
6. 如果命令执行失败，请明确显示错误原因并提供解决方案。

## 错误处理

- **“未找到钱包”** → 先运行`node src/setup.js --json`。
- **“余额不足”** → 显示当前余额，并建议用户充值。
- **“RPC错误”** → 重试一次，系统具有自动故障转移机制。
- **“找不到交易路线”**（在交换操作中） → 可能是因为代币对缺乏流动性。
- **“Gas费用估算失败”** → 可能需要更多ETH来支付Gas费用。

---

## Venice AI集成

您可以访问Venice提供的私有、未经审查的AI推理API。使用DIEM代币在Base区块链上进行支付，以使用AI服务。

### Venice是什么？

[Venice](https://venice.ai)提供私密的AI推理服务——您的输入内容永远不会被记录或用于训练模型。该平台支持未经审查的文本生成、图像生成等功能。

### DIEM是什么？

DIEM是Venice的计费代币，用于在Base区块链上使用AI服务。**每质押1个DIEM，即可获得每天1美元的AI使用权限。**

- **DIEM代币（Base区块链）：** `0xf4d97f2da56e8c3098f3a8d538db630a2606a024`
- 通过[venice.ai/staking](https://venice.ai/staking)进行DIEM质押。
- 抽质押的DIEM会自动解锁API访问权限——无需信用卡。

### 设置Venice API

1. 在[venice.ai/settings/api](https://venice.ai/settings/api)获取API密钥。
2. 保存密钥：
```bash
node src/venice.js setup <your_api_key> --json
```

返回结果：`{ "success": true, "configPath": "~/.venice-api.json" }`

### 检查DIEM余额和分配情况
```bash
# Check Venice account balance (DIEM allocation, usage)
node src/venice.js balance --json

# Check on-chain DIEM token balance
node src/balance.js base 0xf4d97f2da56e8c3098f3a8d538db630a2606a024 --json
```

### 列出可用模型
```bash
# Text models
node src/venice.js models text --json

# Image models
node src/venice.js models image --json
```

### 聊天助手（文本生成）

```bash
node src/venice.js chat "Explain quantum computing" --model llama-3.3-70b --json
```

推荐的模型：
- **私密模式（数据不会离开Venice）：** `zai-org-glm-4.7`（默认）、`deepseek-v3.2`、`llama-3.3-70b`、`venice-uncensored`
- **匿名模式（通过合作伙伴路由）：** `claude-opus-45`、`gpt-5.2`、`grok-41-fast`

### 图像生成

```bash
node src/venice.js generate "A cyberpunk cat in neon Tokyo" --model flux-2-pro --json
```

### 使用加密货币支付（DIEM流程）

有两种方式获取DIEM以使用Venice的AI服务：

---

#### 选项A：直接购买DIEM（最简单的方式）

```bash
# Swap ETH → DIEM directly
node src/swap.js base eth 0xf4d97f2da56e8c3098f3a8d538db630a2606a024 0.1 --quote-only --json

# Execute swap (after user confirms)
node src/swap.js base eth 0xf4d97f2da56e8c3098f3a8d538db630a2606a024 0.1 --yes --json

# Stake DIEM for API access
node src/contract.js base \
  0xf4d97f2da56e8c3098f3a8d538db630a2606a024 \
  "stake(uint256)" \
  1000000000000000000 --yes --json
```

然后跳转到**步骤4：使用Venice API**。

---

#### 选项B：通过质押VVV来获取DIEM（治理模式）

通过质押VVV，您可以生成新的DIEM代币（而非直接购买）。质押VVV的用户还可以获得额外的VVV代币奖励。

#### 步骤1：在Base区块链上获取VVV代币
```bash
# Check ETH balance
node src/balance.js base --json

# Swap ETH → VVV (get quote first)
node src/swap.js base eth 0xacfE6019Ed1A7Dc6f7B508C02d1b04ec88cC21bf 0.1 --quote-only --json

# Execute swap (after user confirms)
node src/swap.js base eth 0xacfE6019Ed1A7Dc6f7B508C02d1b04ec88cC21bf 0.1 --yes --json
```

#### 步骤2：质押VVV以获取DIEM
```bash
# Check VVV balance
node src/balance.js base 0xacfE6019Ed1A7Dc6f7B508C02d1b04ec88cC21bf --json

# Approve VVV for staking contract
node src/contract.js base \
  0xacfE6019Ed1A7Dc6f7B508C02d1b04ec88cC21bf \
  "approve(address,uint256)" \
  0x321b7ff75154472B18EDb199033fF4D116F340Ff \
  1000000000000000000 --yes --json

# Stake VVV (receives DIEM in return)
node src/contract.js base \
  0x321b7ff75154472B18EDb199033fF4D116F340Ff \
  "stake(uint256)" \
  1000000000000000000 --yes --json
```

#### 步骤3：质押DIEM以获取API访问权限
```bash
# Check DIEM balance
node src/balance.js base 0xf4d97f2da56e8c3098f3a8d538db630a2606a024 --json

# Stake DIEM (enables API access)
node src/contract.js base \
  0xf4d97f2da56e8c3098f3a8d538db630a2606a024 \
  "stake(uint256)" \
  1000000000000000000 --yes --json
```

#### 步骤4：使用Venice API
```bash
# Setup API key (get at venice.ai/settings/api)
node src/venice.js setup <api_key> --json

# Check allocation
node src/venice.js balance --json

# Start using AI!
node src/venice.js chat "Hello world" --json
```

#### 检查质押状态
```bash
# Check staked DIEM (returns: amountStaked, coolDownEnd, coolDownAmount)
node src/contract.js base \
  0xf4d97f2da56e8c3098f3a8d538db630a2606a024 \
  "stakedInfos(address)" 0xYOUR_WALLET --json

# Check Venice API allocation
node src/venice.js balance --json
```

#### 解锁DIEM
```bash
# Initiate unstake (starts 1-day cooldown)
node src/contract.js base \
  0xf4d97f2da56e8c3098f3a8d538db630a2606a024 \
  "initiateUnstake(uint256)" <amount> --yes --json

# Complete unstake (after cooldown)
node src/contract.js base \
  0xf4d97f2da56e8c3098f3a8d538db630a2606a024 \
  "unstake()" --yes --json
```

### Venice的合约和代币（Base区块链）

| 名称 | 地址 | 描述 |
|------|---------|-------------|
| VVV | `0xacfE6019Ed1A7Dc6f7B508C02d1b04ec88cC21bf` | 治理代币（用于质押以获取DIEM） |
| DIEM | `0xf4d97f2da56e8c3098f3a8d538db630a2606a024` | 计算代币（用于质押以获取API访问权限） |
| VVV质押 | `0x321b7ff75154472B18EDb199033fF4D116F340Ff` | 存入VVV即可获得DIEM |

### 为什么选择Venice和加密货币？

- **隐私保护**：您的输入内容完全保密，不会被记录。
- **无限制访问**：无需任何内容审查即可使用AI服务。
- **无需身份验证**：支持使用加密货币支付。
- **完全自主**：您的钱包和AI服务完全由您控制，无需依赖任何平台。