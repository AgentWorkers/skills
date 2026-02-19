# ClawPurse 技能

ClawPurse 是一个本地 Timpi/NTMPI 钱包工具，专为 Neutaro 链上的 AI 代理、自动化脚本以及个人用户设计。

## 概述

ClawPurse 为 AI 代理（包括 OpenClaw）、自动化流程和人类操作员提供加密货币钱包功能，支持在 Neutaro 区块链上自主或手动处理 NTMPI 代币。

## 主要功能

- **查询钱包余额**：查看当前的 NTMPI 持有量
- **发送代币**：将 NTMPI 转移到任何 Neutaro 地址
- **接收代币**：获取接收付款的钱包地址
- **查看交易历史**：列出最近的发送/接收记录
- **验证链状态**：检查与 Neutaro 网络的连接情况
- **质押代币**：将 NTMPI 委托给验证节点以获得奖励（v2.0）
- **管理委托**：查看、重新委托或取消质押代币（v2.0）

## 安装

```bash
# In the ClawPurse directory
npm install && npm run build && npm link
```

安装完成后，`clawpurse` 命令行工具将在全局范围内可用。

## 设置

首次使用前必须初始化钱包：

```bash
clawpurse init --password <secure-password>
```

> **重要提示**：立即备份初始化过程中显示的助记词！

## 环境配置

设置 `CLAWPURSE_PASSWORD`，以避免在每个命令中都输入密码：

```bash
export CLAWPURSE_PASSWORD=<password>
```

## 命令

### 状态检查
```bash
clawpurse status
```
返回链连接状态、链 ID 和当前区块高度。

### 余额查询
```bash
clawpurse balance
```
返回当前的 NTMPI 余额。

### 获取钱包地址
```bash
clawpurse address
```
返回钱包的 Neutaro 地址。

### 发送代币
```bash
clawpurse send <to-address> <amount> [--memo "text"] [--yes]
```
将 NTMPI 发送到指定地址。对于金额超过 100 NTMPI 的交易，可以使用 `--yes` 选项跳过确认步骤。

### 查看交易历史
```bash
clawpurse history [--limit N]
```
显示最近的交易记录。

### 允许列表管理
```bash
clawpurse allowlist list              # View trusted destinations
clawpurse allowlist add <addr>        # Add destination
clawpurse allowlist remove <addr>     # Remove destination
```

### 质押（v2.0）
```bash
clawpurse validators                  # List active validators
clawpurse delegations                 # View current delegations
clawpurse stake <validator> <amount>  # Delegate tokens
clawpurse unstake <validator> <amount> --yes  # Undelegate (22-day unbonding)
clawpurse redelegate <from> <to> <amount>     # Move stake between validators
clawpurse unbonding                   # Show pending unbonding
```

**代理的质押流程：**
```
1. Run: clawpurse validators
2. Select validator with good uptime and reasonable commission
3. Run: clawpurse stake <validator> <amount> --yes
4. Monitor with: clawpurse delegations
5. Rewards auto-deposit to liquid balance on Neutaro
```

## 安全特性

- **单次发送上限**：每次交易最多 1000 NTMPI（可配置）
- **需要确认**：超过 100 NTMPI 的交易需要确认
- **地址验证**：仅接受以 `neutaro1...` 开头的地址
- **目的地允许列表**：可选地仅允许向受信任的地址发送代币
- **加密钱包文件**：使用 AES-256-GCM 加密算法，并通过 scrypt 算法生成密钥

## 代理使用示例

- **操作前检查余额**：```
Before any payment task, run:
clawpurse balance

Parse the output to get available funds.
```
- **进行支付**：```
1. Verify recipient is in allowlist (or use --override-allowlist)
2. Run: clawpurse send <address> <amount> --memo "reason" --yes
3. Capture the tx hash from output
4. Share tx hash with recipient for verification
```
- **接收付款**：```
1. Run: clawpurse address
2. Share the address with the sender
3. After expected payment, run: clawpurse balance
4. Or query chain directly to verify specific tx
```

## 程序化 API

如需高级集成，可以直接导入 ClawPurse 的函数：

```typescript
import {
  loadKeystore,
  getBalance,
  send,
  getChainInfo,
} from 'clawpurse';

// Load wallet
const { wallet, address } = await loadKeystore(process.env.CLAWPURSE_PASSWORD);

// Check balance
const balance = await getBalance(address);
console.log(balance.primary.displayAmount);

// Send tokens
const result = await send(wallet, address, 'neutaro1...', '10.5', {
  memo: 'Service payment',
  skipConfirmation: true,
});
console.log(`Sent! TxHash: ${result.txHash}`);
```

## 安全注意事项

- **切勿在日志或输出中泄露助记词**
- **使用环境变量存储密码**，而非脚本中的命令行参数
- **启用允许列表功能**，以防止向未知地址发送代币
- **通过 `~/.clawpurse/receipts.json` 文件监控交易记录以进行审计**

## 文件结构

| 文件路径 | 用途 |
|------|---------|
| `~/.clawpurse/keystore.enc` | 加密后的钱包文件（权限设置为 0600） |
| `~/.clawpurse/receipts.json` | 交易记录 |
| `~/.clawpurse/allowlist.json` | 可信接收地址列表 |

## 文档资料

- [OPERATOR-GUIDE.md](./docs/OPERATOR-GUIDE.md)：完整的设置和使用指南
- [TRUST-MODEL.md](./docs/TRUST-MODEL.md)：安全性和验证机制
- [ALLOWLIST.md](./docs/ALLOWLIST.md)：目的地允许列表系统

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| “找不到钱包” | 先运行 `clawpurse init` 命令 |
| “状态：DISCONNECTED” | 检查网络连接；可能是 RPC 服务不可用 |
| “金额超出限制” | 调整配置文件中的 `maxSendAmount` 值 |
| “目标地址被屏蔽” | 将地址添加到允许列表中，或使用 `--override-allowlist` 选项 |