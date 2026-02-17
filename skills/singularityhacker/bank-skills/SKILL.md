---
name: bank-skill
version: 0.1.4
description: 通过 Wise API 实现的传统银行业务，结合 Base 上的链上代币交换功能
homepage: https://github.com/singularityhacker/bank-skills
metadata: {"openclaw":{"emoji":"🏦","requires":{"bins":["python"],"env":["WISE_API_TOKEN"]},"primaryEnv":"WISE_API_TOKEN","optionalEnv":["WISE_PROFILE_ID","CLAWBANK_WALLET_PASSWORD","BASE_RPC_URL"]}}
---
# Bank Skill

## 目的

该技能为AI代理提供了**传统银行服务**（通过Wise API）和**链上代币操作**（通过Base网络上的Uniswap）。代理可以通过该技能查询余额、转账、获取账户信息、创建以太坊钱包、交换代币等。

## 先决条件

**对于银行服务（Wise API）：**
- 必须设置`WISE_API_TOKEN`环境变量。
- 可选：`WISE_PROFILE_ID`（默认使用第一个可用的账户配置）。

**对于代币操作（Base网络）：**
- 可选：`CLAWBANK_WALLET_PASSWORD`（钱包密钥库密码，默认为“clawbank-default”）。
- 可选：`BASE_RPC_URL`（Base网络的RPC端点，默认为https://mainnet.base.org）。

## 操作

### 银行服务（Wise API）

#### 1. 查询余额

**目的：**查询配置账户的Wise多币种余额。

**输入：**
- `action`: `"balance"`（必需）

**输出：**
- 包含`currency`、`amount`和`reservedAmount`的JSON数组。

**使用示例：**
```bash
echo '{"action": "balance"}' | ./run.sh
echo '{"action": "balance", "currency": "USD"}' | ./run.sh
```

**示例输出：**
```json
{
  "success": true,
  "balances": [
    {"currency": "USD", "amount": 1250.00, "reservedAmount": 0.00},
    {"currency": "EUR", "amount": 500.75, "reservedAmount": 10.00}
  ]
}
```

#### 2. 获取收款信息

**目的：**获取账户号码、路由号码、IBAN等相关信息，以便他人向您汇款。

**输入：**
- `action`: `"receive-details"`（必需）
- `currency`: 货币代码（可选，省略时返回所有信息）

**输出：**
- 包含账户持有人姓名、账户号码、路由号码（非USD货币时返回IBAN/SWIFT）和银行名称的JSON对象。

**使用示例：**
```bash
echo '{"action": "receive-details"}' | ./run.sh
echo '{"action": "receive-details", "currency": "USD"}' | ./run.sh
```

#### 3. 转账

**目的：**从您的Wise账户向指定账户转账。

**输入：**
- `action`: `"send"`（必需）
- `sourceCurrency`: 源货币代码（必需）
- `targetCurrency`: 目标货币代码（必需）
- `amount`: 转账金额（必需）
- `recipientName`: 收款人全名（必需）
- `recipientAccount`: 收款人账户号码或IBAN（必需）

**USD ACH转账的额外字段：**
- `recipientRoutingNumber`: 9位ABA路由号码（必需）
- `recipientCountry`: 两位字母的国家代码（必需）
- `recipientAddress`: 街道地址（必需）
- `recipientCity`: 城市名称（必需）
- `recipientState`: 州代码（必需）
- `recipientPostCode`: 邮政编码（必需）
- `recipientAccountType`: `"CHECKING"`或`"SAVINGS"`（可选，默认为`"CHECKING"`）

**输出：**
- 包含转账ID、状态和确认信息的JSON对象。

**USD ACH转账示例：**
```bash
echo '{
  "action": "send",
  "sourceCurrency": "USD",
  "targetCurrency": "USD",
  "amount": 100.00,
  "recipientName": "John Smith",
  "recipientAccount": "123456789",
  "recipientRoutingNumber": "111000025",
  "recipientCountry": "US",
  "recipientAddress": "123 Main St",
  "recipientCity": "New York",
  "recipientState": "NY",
  "recipientPostCode": "10001",
  "recipientAccountType": "CHECKING"
}' | ./run.sh
```

**EUR IBAN转账示例（简化版）：**
```bash
echo '{
  "action": "send",
  "sourceCurrency": "USD",
  "targetCurrency": "EUR",
  "amount": 100.00,
  "recipientName": "Jane Doe",
  "recipientAccount": "DE89370400440532013000"
}' | ./run.sh
```

**示例输出：**
```json
{
  "success": true,
  "transfer": {
    "id": 12345678,
    "status": "processing",
    "sourceAmount": 100.00,
    "sourceCurrency": "USD",
    "targetAmount": 93.50,
    "targetCurrency": "EUR"
  }
}
```

### 代币操作（Base网络）

#### 4. 创建钱包

**目的：**为在Base网络上进行代币操作生成一个新的以太坊钱包。

**输入：**
- `action`: `"create-wallet"`（必需）

**输出：**
- 钱包地址（密钥库保存在`~/.clawbank/wallet.json`中）。

**使用示例：**
```bash
echo '{"action": "create-wallet"}' | ./run.sh
```

#### 5. 获取钱包信息

**目的：**获取当前钱包地址和Base网络上的ETH余额。

**输入：**
- `action`: `"get-wallet"`（必需）

**输出：**
- 钱包地址和ETH余额。

**使用示例：**
```bash
echo '{"action": "get-wallet"}' | ./run.sh
```

#### 6. 设置目标代币地址

**目的：**设置用于交换的目标代币地址。

**输入：**
- `action`: `"set-target-token"`（必需）
- `tokenAddress`: Base网络上的ERC-20合约地址（必需）

**使用示例：**
```bash
echo '{"action": "set-target-token", "tokenAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"}' | ./run.sh
```

#### 7. 查看交换配置

**目的：**查看当前的目标代币和交换历史记录。

**输入：**
- `action`: `"get-sweep-config"`（必需）

**使用示例：**
```bash
echo '{"action": "get-sweep-config"}' | ./run.sh
```

#### 8. 查看代币余额

**目的：**查询钱包中的ERC-20代币余额。

**输入：**
- `action`: `"get-token-balance"`（必需）
- `tokenAddress`: ERC-20合约地址（必需）

**使用示例：**
```bash
echo '{"action": "get-token-balance", "tokenAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"}' | ./run.sh
```

#### 9. 购买代币

**目的：**通过Uniswap在Base网络上将ETH兑换为任意代币（支持V3+V4版本）。

**输入：**
- `action`: `"buy-token"`（必需）
- `amountEth`: 要兑换的ETH数量（必需）

**输出：**
- 交易哈希、输入金额、输出金额和交易状态。

**支持的代币：**任何在Base网络上具有WETH流动性的ERC-20代币（如USDC、DAI、WBTC、ClawBank等）。

#### 10. 发送代币

**目的：**从钱包发送ERC-20代币或ETH。

**输入：**
- `action`: `"send-token"`（必需）
- `tokenAddress`: ERC-20合约地址；或输入“ETH”表示发送ETH
- `toAddress`: 收件人钱包地址（必需）
- `amount`: 要发送的代币数量

**使用示例：**
```bash
echo '{"action": "send-token", "tokenAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "toAddress": "0x...", "amount": 5.0}' | ./run.sh
```

#### 11. 导出私钥**

**目的：**导出钱包的私钥以备恢复或导入。

**输入：**
- `action`: `"export-private-key"`（必需）

**输出：**
- 私钥（十六进制字符串）和钱包地址。

**使用示例：**
```bash
echo '{"action": "export-private-key"}' | ./run.sh
```

## 失败情况

**银行服务：**
- **缺少`WISE_API_TOKEN`：**返回`{"success": false, "error": "WISE_API_TOKEN环境变量未设置"`. 请设置正确的API密钥后重试。
- **API密钥无效：**返回`{"success": false, "error": "认证失败——请检查您的WISE_API_TOKEN"`。
- **资金不足：**返回`{"success": false, "error": "USD余额不足"`。请先查询余额后再尝试。
- **收款人信息无效：**返回`{"success": false, "error": "收款人账户信息无效"`。

**代币操作：**
- **钱包不存在：**返回`{"success": false, "error": "钱包未创建。请先使用`create-wallet`命令创建钱包"`。
- **ETH余额不足：**返回`{"success": false, "error": "余额不足。需要X ETH作为交易手续费"`。
- **未设置目标代币：**返回`{"success": false, "error": "未设置目标代币。请先使用`set-target-token`命令设置目标代币"`。
- **找不到流动性池：**返回`{"success": false, "error": "未找到[代币]的流动性池"`。
- **未知操作：**返回`{"success": false, "error": "未知操作：<操作名称>"`。请参考操作说明。`

## 使用场景

**银行服务：**查询余额、进行国际转账、分享账户信息以接收汇款。

**代币操作：**创建钱包、在Base网络上交换代币、发送代币、查看余额。

**禁止使用的情况：**
- 不要将Wise用于加密货币的出入金操作（Wise限制此类操作）。
- 不要用于持有大量资金的账户（仅限研发用途）。
- 代币操作需要Base网络访问权限以及ETH作为交易手续费。

## 技术细节**

- **代币交换实现：**采用混合V3+V4路由机制（优先尝试V3版本，对于需要特定功能的代币则使用V4版本）。
- 支持在Base网络上具有WETH流动性的任何代币。
- 自动检测交易手续费等级（0.05%、0.3%、1%）。
- 交易手续费约为250k gas（V3版本）或450k gas（V4版本）。

**安全性：**
- 钱包密钥库使用密码加密。
- 私钥不会被记录或公开。
- 所有交易均在本地签名完成。
- 代币操作不依赖外部API（直接与区块链交互）。