---
name: Kaspa Wallet
description: 发送和接收 KAS 加密货币；查询余额；进行支付；生成钱包。
---

# Kaspa 钱包 CLI

这是一个专为 Kaspa 区块链网络设计的独立命令行钱包工具。

## 安装

```bash
python3 install.py
```

**系统要求：** 需要安装 Python 3.8 及以上版本，并确保已安装 `pip`。支持 macOS、Linux 和 Windows 系统。

**安装过程中可能遇到的问题及解决方法：**
- 如果 `pip` 安装失败，可以尝试手动执行 `pip install kaspa`；或者设置 `KASPA_PYTHON=python3.12` 后运行 `python3 install.py`。
- 如果系统中没有 `venv` 环境，可以在 Ubuntu/Debian 系统上使用 `sudo apt install python3-venv` 来安装。
- 如果需要重新安装钱包，请执行 `rm -rf .venv && python3 install.py`。

## 环境变量

**必填环境变量：**
```bash
export KASPA_PRIVATE_KEY="64-character-hex-string"
# OR
export KASPA_MNEMONIC="your twelve or twenty four word seed phrase"
```

**可选环境变量：**
```bash
export KASPA_NETWORK="mainnet"              # mainnet (default), testnet-10
export KASPA_RPC_URL="wss://..."            # Custom RPC endpoint
export KASPA_RPC_CONNECT_TIMEOUT_MS="30000" # Connection timeout (default: 15000)
```

## 命令说明

所有命令的输出结果均为 JSON 格式。退出代码：
- 0 表示成功；
- 1 表示失败。

### 检查余额

```bash
./kaswallet.sh balance                    # Your wallet balance
./kaswallet.sh balance kaspa:qrc8y...     # Any address balance
```

**输出示例：**
```json
{"address": "kaspa:q...", "balance": "1.5", "sompi": "150000000", "network": "mainnet"}
```

### 发送 KAS

```bash
./kaswallet.sh send <address> <amount>           # Send specific amount
./kaswallet.sh send <address> max                # Send entire balance
./kaswallet.sh send <address> <amount> priority  # Priority fee tier
```

**成功输出示例：**
```json
{"status": "sent", "txid": "abc123...", "from": "kaspa:q...", "to": "kaspa:q...", "amount": "0.5", "fee": "0.0002"}
```

**失败输出示例：**
```json
{"error": "Storage mass exceeds maximum", "errorCode": "STORAGE_MASS_EXCEEDED", "hint": "...", "action": "consolidate_utxos"}
```

### 查看网络信息

```bash
./kaswallet.sh info
```

**输出示例：**
```json
{"network": "mainnet", "url": "wss://...", "blocks": 12345678, "synced": true, "version": "1.0.0"}
```

### 费用估算

```bash
./kaswallet.sh fees
```

**输出示例：**
```json
{"network": "mainnet", "low": {"feerate": 1.0, "estimatedSeconds": 60}, "economic": {...}, "priority": {...}}
```

### 生成新钱包

```bash
./kaswallet.sh generate-mnemonic
```

**输出示例：**
```json
{"mnemonic": "word1 word2 word3 ... word24"}
```

### 获取支付 URI

```bash
./kaswallet.sh uri                          # Your address
./kaswallet.sh uri kaspa:q... 1.5 "payment" # With amount and message
```

## 错误处理

所有错误都会以 JSON 格式返回详细信息：
| 错误代码 | 错误原因 | 解决方案 |
|-----------|---------|------------|
| `STORAGE_MASS_EXCEEDED` | 当前未花费的交易输出（UTXO）数量不足 | 先向自己发送 `max` 数量的 KAS 以合并这些交易输出 |
| `NO_UTXOS` | 无可花费的交易输出 | 等待交易确认或向钱包充值 |
| `INSUFFICIENT_FUNDS` | 账户余额过低 | 检查余额并增加充值金额 |
| `RPC_TIMEOUT` | 网络延迟 | 重试或增加请求超时时间 |
| `NO_CREDENTIALS` | 未设置钱包密钥 | 请设置 `KASPA_PRIVATE_KEY` 或 `KASPA_MNEMONIC` |
| `SDK_NOT_INSTALLED` | 未安装 Kaspa SDK | 请运行 `python3 install.py` 安装 SDK |

## 常见操作流程

### 合并未花费的交易输出（解决 `STORAGE_MASS_EXCEEDED` 错误）

当发送交易失败并收到 `STORAGE_MASS_EXCEEDED` 错误时，可以执行以下操作：
```bash
# 1. Get your address
./kaswallet.sh balance
# Returns: {"address": "kaspa:qYOUR_ADDRESS...", ...}

# 2. Send max to yourself (consolidates UTXOs)
./kaswallet.sh send kaspa:qYOUR_ADDRESS... max

# 3. Now send the original amount (will work)
./kaswallet.sh send kaspa:qRECIPIENT... 0.5
```

### 查看交易状态

交易发送成功后，可以使用交易 ID (`txid`) 在以下地址的区块浏览器中验证交易状态：
- 主网：`https://explorer.kaspa.org/txs/{txid}`
- 测试网：`https://explorer-tn10.kaspa.org/txs/{txid}`

### 切换网络

```bash
# Testnet
export KASPA_NETWORK="testnet-10"
./kaswallet.sh info

# Back to mainnet
export KASPA_NETWORK="mainnet"
./kaswallet.sh info
```

## 单位说明

- **KAS**：人类可读的单位，例如 1.5 KAS。
- **sompi**：最小单位，1 KAS = 100,000,000 sompi。

所有命令的输入参数均支持 KAS 单位；输出结果中也会同时显示 KAS 和 sompi 的数值（如适用）。

## 安全注意事项

- 私钥和助记词仅通过环境变量传递，切勿记录或公开这些信息。
- 该钱包不会将任何凭据存储在磁盘上。
- 每次执行命令时都会建立新的 RPC 连接。

## 代理程序使用示例

```bash
# Check if wallet is configured and has funds
./kaswallet.sh balance
# Parse: if balance > 0, wallet is ready

# Send payment with error handling
./kaswallet.sh send kaspa:recipient... 1.0
# If errorCode == "STORAGE_MASS_EXCEEDED":
#   Run: ./kaswallet.sh send YOUR_ADDRESS max
#   Then retry original send

# Verify network connectivity
./kaswallet.sh info
# Check: synced == true before sending
```