---
name: aibtc-bitcoin-wallet
description: 适用于代理的比特币L1钱包：支持查询余额、发送BTC、管理未花费的交易输出（UTXOs）。同时兼容Stacks L2（STX、DeFi）以及Pillar智能钱包（sBTC收益功能）。
license: MIT
metadata:
  author: aibtcdev
  version: 1.14.2
  npm: "@aibtc/mcp-server"
  github: https://github.com/aibtcdev/aibtc-mcp-server
---

# AIBTC比特币钱包

这是一项用于管理比特币L1钱包的技能，该钱包支持Pillar智能钱包功能以及Stacks L2去中心化金融（DeFi）服务。

## 安装

通过一条命令即可完成安装：

```bash
npx @aibtc/mcp-server@latest --install
```

**测试网版本：**

```bash
npx @aibtc/mcp-server@latest --install --testnet
```

## 快速入门

### 检查余额

查询您的比特币余额：

```
"What's my BTC balance?"
```

使用`get_btc_balance`命令，可获取总余额、已确认余额和未确认余额。

### 查询费用

获取当前网络费用估算：

```
"What are the current Bitcoin fees?"
```

使用`get_btc_fees`命令，可获取快速（约10分钟）、中等（约30分钟）和慢速（约1小时）的交易费用（单位：sat/vB）。

### 发送比特币

将比特币转账到指定地址：

```
"Send 50000 sats to bc1q..."
"Transfer 0.001 BTC with fast fees to bc1q..."
```

使用`transfer_btc`命令，需要确保钱包已解锁。

## 钱包设置

在发送交易之前，请先设置钱包：
1. **创建新钱包**：`wallet_create`——生成加密的BIP39助记词。
2. **导入现有钱包**：`wallet_import`——通过助记词导入钱包信息。
3. **解锁钱包以进行交易**：`walletunlock`——交易前必须解锁钱包。

钱包数据以加密形式存储在`~/.aibtc/`目录下。

## 工具参考

### 读取操作

| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `get_btc_balance` | 查询比特币余额 | `address`（可选；若省略则需解锁钱包） |
| `get_btc_fees` | 获取费用估算 | 无参数 |
| `get_btc_utxos` | 列出未确认的交易输出（UTXOs） | `address`（可选；若省略则需解锁钱包），`confirmedOnly`（可选） |

### 写入操作（需要解锁钱包）

| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `transfer_btc` | 发送比特币 | `recipient`（收款地址），`amount`（金额，单位：satoshis），`feeRate`（费用率） |

### 钱包管理

| 工具 | 描述 | ----------------------|
| `wallet_create` | 创建新的加密钱包 |
| `wallet_import` | 从助记词导入钱包信息 |
| `wallet_unlock` | 解锁钱包以进行交易 |
| `wallet_lock` | 锁定钱包（清除内存中的钱包数据） |
| `wallet_list` | 列出所有可用钱包 |
| `wallet_switch` | 切换活跃钱包 |
| `wallet_status` | 获取钱包/会话状态 |

## 单位和地址

- **金额**：始终以satoshis为单位（1 BTC = 100,000,000 satoshis）。
- **地址**：
  - 主网：`bc1...`（原生SegWit格式）
  - 测试网：`tb1...`
- **费用率**：`fast`、`medium`、`slow`或自定义的sat/vB数值。

## 示例流程

### 每日余额检查

```
1. "What's my BTC balance?"
2. "Show my recent UTXOs"
3. "What are current fees?"
```

### 发送付款

```
1. "Unlock my wallet" (provide password)
2. "Send 100000 sats to bc1qxyz... with medium fees"
3. "Lock my wallet"
```

### 多钱包管理

```
1. "List my wallets"
2. "Switch to trading wallet"
3. "Unlock it"
4. "Check balance"
```

## 分层架构

本技能主要针对比特币L1层进行开发。其他扩展功能按层次结构进行分类：

### Stacks L2（第二层）

支持智能合约和去中心化金融（DeFi）的比特币L2服务：
- STX代币转账
- ALEX DEX代币交易
- Zest协议借贷服务
- 提供x402 API接口（包括AI、存储、实用工具等）

详情请参阅：[references/stacks-defi.md](references/stacks-defi.md)

### Pillar智能钱包（第三层）

基于sBTC的智能钱包，具备收益自动化功能：
- 支持Passkey或代理签名交易
- 可将比特币发送到BNS地址（例如：alice.btc）
- 通过Zest协议自动提升收益

详情请参阅：[references/pillar-wallet.md](references/pillar-wallet.md)

### 比特币刻录

在比特币上刻录并检索数字资产：
- 提交并显示刻录内容及元数据
- 保护未确认的交易输出（UTXOs）免遭意外支出

详情请参阅：[references/inscription-workflow.md](references/inscription-workflow.md)

### Genesis生命周期

比特币及Stacks平台上的代理身份与信誉管理：
- L0阶段：生成本地代理密钥
- L1阶段：使用双链签名机制（btc_sign_message + stacks_sign_message）
- L2阶段：激活X代币发放功能
- 保持活跃状态需每5分钟进行一次身份验证

详情请参阅：[references/genesis-lifecycle.md](references/genesis-lifecycle.md)

## 常见问题解决方法

### “钱包未解锁”

在发送交易前，请使用密码运行`wallet_unlock`命令解锁钱包。

### “余额不足”

请使用`get_btc_balance`命令检查余额，确保有足够的比特币用于支付交易金额及费用。

### “地址无效”

请确认地址格式正确：
- 主网地址以`bc1`开头
- 测试网地址以`tb1`开头

详情请参阅：[references/troubleshooting.md](references/troubleshooting.md)

## 更多信息

- [CLAUDE.md](../CLAUDE.md) - 完整的工具文档
- [GitHub](https://github.com/aibtcdev/aibtc-mcp-server) - 源代码仓库
- [npm](https://www.npmjs.com/package/@aibtc/mcp-server) - 包安装信息

---

*本技能遵循[Agent Skills](https://agentskills.io)开放规范进行开发。*