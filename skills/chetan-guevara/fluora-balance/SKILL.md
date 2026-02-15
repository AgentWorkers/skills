---
name: fluora-balance
description: 请检查您在 Base Mainnet 上的 Fluora 钱包中的 USDC 余额。当用户询问他们的 Fluora 余额、钱包余额、USDC 余额或他们在 Fluora 账户中有多少钱时，可以使用此信息进行回答。
---

# Fluora Balance

请查看在Fluora中配置的钱包在Base Mainnet上的USDC余额。

## 快速入门

运行余额检查脚本：

```bash
cd scripts/
npm install  # First time only
node check_balance.js
```

该脚本将：
1. 从`~/.fluora/wallets.json`文件中读取您的主网钱包地址
2. 查询Base Mainnet上的USDC余额
3. 显示格式化的余额

## 脚本详情

**位置：** `scripts/check_balance.js`

**功能：**
- 从`~/.fluora/wallets.json`文件中读取钱包地址（`USDC_BASE_MAINNET.address`字段）
- 通过`https://mainnet.base.org`连接到Base Mainnet
- 查询地址为`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`的USDC合约
- 返回格式化的USDC余额

**输出格式：**
```
Checking USDC balance on Base Mainnet...

Wallet: 0x7DC445b40719ab482090...
Balance: 1.234567 USDC
```

**JSON输出：** 如需进行程序化解析，请添加`--json`参数：
```bash
node check_balance.js --json
```

## 依赖项

该脚本需要`ethers`（版本6及以上）来与区块链交互：
```bash
cd scripts/
npm install
```

依赖项列在`scripts/package.json`文件中。

## 故障排除

**错误：未找到`~/.fluora/wallets.json`文件**
- 确保Fluora已正确设置
- 如有需要，请运行`fluora-setup`脚本进行初始化

**错误：未找到`USDC_BASE_MAINNET.address`字段**
- 检查`wallets.json`文件中是否包含`USDC_BASE_MAINNET.address`字段
- 如有必要，请重新生成钱包地址

**网络错误**
- 确保网络连接正常
- Base Mainnet的RPC服务可能暂时不可用（请稍后重试）