---
name: evm-wallet-skill
description: 这款自主可控的EVM钱包专为AI代理设计。当用户需要创建加密钱包、查看余额、发送ETH或ERC20代币、进行代币交易或与智能合约交互时，均可使用该钱包。它支持Base、Ethereum、Polygon、Arbitrum和Optimism等区块链网络。私钥存储在本地设备上，无需依赖云存储服务，也不需要API密钥。
metadata: {"clawdbot":{"emoji":"💰","homepage":"https://github.com/surfer77/evm-wallet-skill","requires":{"bins":["node","git"]}}}
---

# EVM钱包技能

这是一个完全自主的EVM（以太坊虚拟机）钱包。私钥存储在本地，不依赖任何外部API。

## ⚠️ 安全警告

**切勿泄露您的私钥！**

- 绝不要在聊天、电子邮件或任何消息平台上发送您的私钥。
- 绝不要与他人分享`~/.evm-wallet.json`文件的内容。
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

如果代码尚未安装（没有`src/`文件夹），请执行初始化操作：
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

返回结果：`{"success": true, "address": "0x..."}`

私钥存储在`~/.evm-wallet.json`文件中（权限设置为600）。**切勿共享此文件。**

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
- 收件人地址
- 代币数量
- 所在区块链
- 预计的Gas费用

只有在用户明确同意后，才添加`--yes`参数。

### 交换代币

当用户想要交换、交易、购买或出售代币时：
```bash
# Get quote first
node src/swap.js <chain> <from_token> <to_token> <amount> --quote-only --json

# Execute swap (after user confirms)
node src/swap.js <chain> <from_token> <to_token> <amount> --yes --json
```

- 使用`eth`表示ETH/POL代币；或者提供合约地址。
- 默认滑点为0.5%。可以通过`--slippage <百分比>`参数进行修改。
- 该功能由Odos聚合器提供支持（可自动选择数百个DEX中的最佳交易路径）。

**⚠️ 在执行操作之前，请务必先展示交易报价，并获得用户的确认。**

### 调用合约函数

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

如果有新的更新可用，请通知用户，并提供更新选项：
```bash
cd "$SKILL_DIR" && git pull && npm install
```

## 支持的区块链

| 区块链 | 原生代币 | 适用场景 |
|-------|-------------|---------|
| Base | ETH | 测试环境，费用最低 |
| Ethereum | ETH | 主网环境，费用最高 |
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

1. **未经用户确认，切勿执行任何转移或交换操作。**
2. **切勿泄露`~/.evm-wallet.json`文件中的私钥。**
3. **在执行任何操作之前，务必向用户展示交易详情（金额、收件人、Gas费用估算）。**
4. **建议首次用户使用Base区块链进行测试或小额交易。**
5. **交易成功后，提供交易浏览器链接以便用户验证。**
6. 如果命令执行失败，请清晰显示错误信息并提供解决方法。

## 错误处理

- **“未找到钱包”** → 首先运行`node src/setup.js --json`。
- **“余额不足”** → 显示当前余额，并建议用户充值。
- **“RPC错误”** → 重试一次，系统具有自动故障转移机制。
- **“未找到交易路径”**（在交换操作中） → 可能是因为代币对缺乏流动性。
- **“Gas费用估算失败”** → 可能需要更多ETH来支付Gas费用。