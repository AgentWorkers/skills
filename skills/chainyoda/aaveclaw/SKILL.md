---
name: aaveclaw
description: Aave V3借贷协议在Base Sepolia测试网上运行。用户可以存入WETH作为抵押品，借入USDC，偿还贷款，提取抵押品，查看自身的借贷健康状况，并通过测试网提供的工具（fountain） mint测试代币。该协议适用于希望使用Aave借贷服务、检查自身借贷状况或获取测试网代币的用户。
---

# aaveclaw - 在 Base Sepolia 上使用 Aave V3 协议进行借贷

该工具用于在 Base Sepolia 测试网络上与 Aave V3 借贷协议进行交互，通过 `~/.x402-config.json` 配置文件中的钱包管理整个借贷流程。

## 设置

首次使用时，请运行 `setup.sh` 命令以安装所需的依赖项（ethers v6）：

```
bash scripts/setup.sh
```

## 命令

### 检查健康因子

查看当前的借贷状况。该命令可随时执行，仅用于读取信息。

```
bash scripts/health.sh [address]
```

如果未提供地址，系统将使用配置好的钱包地址。

### 铸造测试代币（ faucet）

从 Aave 的代币发放器（faucet）获取测试网络中的 WETH 或 USDC。如果钱包中没有任何代币，请先执行此命令。

```
bash scripts/faucet.sh weth 1       # Mint 1 WETH
bash scripts/faucet.sh usdc 1000    # Mint 1000 USDC
```

### 存入抵押品

将 WETH 存入 Aave 作为抵押品。如有需要，系统会自动将原生 ETH 转换为 WETH。

```
bash scripts/deposit.sh 0.5         # Deposit 0.5 WETH
```

### 借入 USDC

使用存入的抵押品借入 USDC，利率为浮动利率。

```
bash scripts/borrow.sh 100          # Borrow 100 USDC
```

### 偿还债务

偿还借入的 USDC。使用 `max` 参数可一次性还清全部债务。

```
bash scripts/repay.sh 50            # Repay 50 USDC
bash scripts/repay.sh max           # Repay all debt
```

### 提取抵押品

提取存入的 WETH 抵押品。如果未欠债务，可以使用 `max` 参数提取全部抵押品。

```
bash scripts/withdraw.sh 0.5        # Withdraw 0.5 WETH
bash scripts/withdraw.sh max        # Withdraw all
```

## 使用指南

- **在进行任何操作之前，请务必先运行 `health.sh` 命令以查看当前借贷状况。**
- **在执行存入、借款、偿还或提取操作之前，请先询问用户所需的具体金额。**
- **任何状态变更操作后，系统会自动显示当前的健康因子。**
- **当健康因子降至 1.5 以下时，系统会发出警告——这意味着您的借贷资产存在被清算的风险。**
- **建议新用户先通过代币发放器获取测试代币，再开始借贷操作。**
- **典型操作流程：** 通过代币发放器获取代币 → 存入抵押品 → 借入资金 → 偿还债务 → 提取抵押品。

## 网络信息

- **网络**: Base Sepolia（链 ID：84532）
- **浏览器**: https://sepolia.basescan.org
- **远程过程调用 (RPC)**: https://sepolia.base.org
- **代币**: WETH（18 位小数），USDC（6 位小数）

## 错误处理

- **如果缺少私钥**：系统会提示用户使用 `{"private_key": "0x..."}` 创建 `~/.x402-config.json` 文件。
- **如果余额不足**：系统会显示实际余额及所需补充的金额。
- **如果借款后健康因子过低**：Aave 会自动撤销相关交易。
- **如果代币发放器出现故障**：可能是由于铸造限制或暂时不可用所致。