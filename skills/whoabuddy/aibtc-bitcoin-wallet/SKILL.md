---
name: aibtc-bitcoin-wallet
description: 面向代理的比特币L1钱包——支持查询余额、发送BTC、管理未花费的交易输出（UTXOs）。同时兼容Stacks L2（STX、DeFi）以及Pillar智能钱包（sBTC收益功能）。
license: MIT
metadata:
  author: aibtcdev
  version: 1.14.2
  npm: "@aibtc/mcp-server"
  github: https://github.com/aibtcdev/aibtc-mcp-server
---
# AIBTC比特币钱包

这是一项用于管理比特币L1钱包的技能，支持Pillar智能钱包功能以及Stacks L2去中心化金融（DeFi）服务。

## 安装

通过一条命令即可完成安装：

```bash
npx @aibtc/mcp-server@latest --install
```

**测试网（Testnet）安装命令：**

```bash
npx @aibtc/mcp-server@latest --install --testnet
```

## 快速入门

### 检查余额

查看您的比特币余额：

```
"What's my BTC balance?"
```

使用 `get_btc_balance` 命令，可获取总余额、已确认余额和未确认余额。

### 查看费用

获取当前网络费用估算：

```
"What are the current Bitcoin fees?"
```

使用 `get_btc_fees` 命令，可获取快速（约10分钟）、中等（约30分钟）和慢速（约1小时）的交易费用（单位：sat/vB）。

### 发送比特币

将比特币转账到指定地址：

```
"Send 50000 sats to bc1q..."
"Transfer 0.001 BTC with fast fees to bc1q..."
```

使用 `transfer_btc` 命令，需确保钱包已解锁。

## 钱包设置

在发送交易之前，请先完成以下设置：
1. **创建新钱包**：`wallet_create` — 生成加密的BIP39助记词。
2. **导入现有钱包**：`wallet_import` — 从助记词导入钱包信息。
3. **解锁钱包以进行交易**：`wallet_unlock` — 交易前必须解锁钱包。

钱包数据以加密形式存储在 `~/.aibtc/` 目录下。

## 工具参考

### 读取操作

| 工具          | 描述                                      | 参数                                      |
|----------------|-----------------------------------------|-----------------------------------------|
| `get_btc_balance`    | 获取比特币余额                              | `address` （可选；若省略则需解锁钱包）                   |
| `get_btc_fees`    | 获取费用估算                                |                          |
| `get_btc_utxos`    | 列出未确认的交易输出（UTXOs）                        | `address` （可选；若省略则需解锁钱包），`confirmedOnly`           |

### 写入操作（需要钱包解锁）

| 工具          | 描述                                      | 参数                                      |
|----------------|-----------------------------------------|-----------------------------------------|
| `transfer_btc`    | 发送比特币                                | `recipient`（收款地址），`amount`（金额，单位：satoshis），`feeRate`（费用率）     |

### 钱包管理

| 工具          | 描述                                      |                                      |
|----------------|-----------------------------------------|-----------------------------------------|
| `wallet_create`    | 创建新的加密钱包                              |                                        |
| `wallet_import`    | 从助记词导入钱包信息                            |                                        |
| `wallet_unlock`    | 解锁钱包以进行交易                              |                                        |
| `wallet_lock`    | 锁定钱包（清除内存中的钱包数据）                          |                                        |
| `wallet_list`    | 列出所有可用的钱包                              |                                        |
| `wallet_switch`    | 切换当前使用的钱包                              |                                        |
| `wallet_status`    | 获取钱包/会话状态                              |                                        |

## 单位和地址

**金额**：始终以satoshis为单位（1 BTC = 100,000,000 satoshis）

**地址格式**：
- 主网（Mainnet）：`bc1...`
- 测试网（Testnet）：`tb1...`

**费用率**：`fast`、`medium`、`slow` 或自定义的 sat/vB 数值

## 示例操作流程

### 每日余额检查

```
1. "What's my BTC balance?"
2. "Show my recent UTXOs"
3. "What are current fees?"
```

### 发送支付

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

## 进阶功能

本技能主要针对比特币L1层进行开发。其他扩展功能按层次结构进行分类：

### Stacks L2（第二层）

支持智能合约和去中心化金融（DeFi）的比特币L2服务：
- STX代币转账
- ALEX DEX代币交易
- Zest协议借贷服务
- x402付费API（包括AI、存储、实用工具等）——默认采用“先探测后支付”的安全机制

详情请参阅：[references/stacks-defi.md](references/stacks-defi.md)

### Pillar智能钱包（第三层）

基于sBTC的智能钱包，具备自动化收益管理功能：
- 支持Passkey或代理签名交易
- 可将资金转账至BNS名称（例如：alice.btc）
- 通过Zest协议自动提升收益

详情请参阅：[references/pillar-wallet.md](references/pillar-wallet.md)

### 比特币刻录功能

支持在比特币上刻录和检索数字信息：
- 提供刻录和检索数字内容的流程
- 保护未确认的交易输出（UTXOs）免遭意外支出

详情请参阅：[references/inscription-workflow.md](references/inscription-workflow.md)

### x402付费API

基于Stacks L2的按使用次数计费的API，支持自动微支付：
- 使用 `list_x402_endpoints` 查找可用API端点
- 使用 `probe_x402_endpoint` 在支付前查询费用
- 使用 `execute_x402_endpoint` 执行API请求（默认采用“先探测后支付”的安全机制）
- 使用 `send_inbox_message` 发送收件箱消息（替代 `execute_x02_endpoint`）

执行付费API前务必先进行费用查询。切勿在未检查费用的情况下使用 `execute_x02_endpoint` 且 `autoApprove: true` 参数。

**send_inbox_message**：专门用于处理aibtc.com收件箱消息的工具：
- 参数：`recipientBtcAddress`（收款比特币地址，格式：bc1...），`recipientStxAddress`（收款STX地址），`content`（消息内容，最长500个字符）
- 采用赞助交易模式：发送方仅支付sBTC消息的费用，其余费用由系统承担
- 解决了影响通用 `execute_x02_endpoint` 的sBTC结算超时问题
- 完整遵循x402 v2支付流程（包含余额预检查）

详情请参阅：[references/stacks-defi.md](references/stacks-defi.md)（API端点目录）
以及 [references/x402-inbox.md](references/x402-inbox.md)（收件箱相关流程说明）

### Genesis生命周期管理

管理比特币和Stacks平台上的代理身份与信誉：
- L0阶段：生成本地代理密钥
- L1阶段：使用双链签名机制（btc_sign_message + stacks_sign_message）
- L2阶段：激活X代币领取功能及BTC空投
- L3阶段：通过ERC-8004标准进行链上身份注册
- L4阶段：建立信誉体系（get_reputation、give_feedback）

详情请参阅：[references/genesis-lifecycle.md](references/genesis-lifecycle.md)

## 故障排除

### “钱包未解锁”

在发送交易前，请使用密码运行 `wallet_unlock` 命令解锁钱包。

### “余额不足”

使用 `get_btc_balance` 命令确认余额是否足够支付交易金额及费用。

### “地址无效”

确保地址格式正确：
- 主网地址以 `bc1` 开头
- 测试网地址以 `tb1` 开头

详情请参阅：[references/troubleshooting.md](references/troubleshooting.md)

## 更多信息

- [CLAUDE.md](../CLAUDE.md) — 完整工具文档
- [GitHub](https://github.com/aibtcdev/aibtc-mcp-server) — 源代码仓库
- [npm](https://www.npmjs.com/package/@aibtc/mcp-server) — 包安装信息

---

*本技能遵循 [Agent Skills](https://agentskills.io) 开放规范进行设计。*