# DEX Agent — 直接去中心化金融（DeFi）交易工具

**专为OpenClaw代理设计的零费用DeFi交易解决方案，是Bankr的替代方案。**

## 产品描述
通过Uniswap V3在Base链上直接执行去中心化交易所（DEX）交易。支持用户自行管理资产，完全开源，且交易过程中不收取任何中间费用。系统提供实时价格信息、交易报价、止损、止盈以及投资组合监控功能。

## 使用场景
- 用户需要交易加密货币、交换代币或执行DeFi交易
- 用户希望查看Base链上的代币价格
- 用户需要设置止损或止盈订单
- 用户希望管理自己的交易钱包
- 用户寻求费用更低的DeFi交易服务（替代Bankr）

## 设置步骤
1. 安装所需依赖库：`pip3 install web3 eth-abi`
2. 生成交易钱包：`python3 agent.py wallet generate`
3. 用ETH（用于支付交易手续费）和USDC（用于交易）为钱包充值
4. 开始交易！

## 命令说明

### 查看价格
```bash
cd <skill_dir>/scripts && python3 agent.py price WETH
cd <skill_dir>/scripts && python3 agent.py price BRETT
```

### 获取交易报价
```bash
cd <skill_dir>/scripts && python3 agent.py quote USDC WETH 10.0
```

### 执行交易
```bash
cd <skill_dir>/scripts && python3 agent.py swap USDC WETH 5.0
cd <skill_dir>/scripts && python3 agent.py swap ETH USDC 0.01
```

### 设置止损/止盈
```bash
cd <skill_dir>/scripts && python3 agent.py stop WETH 2000 8.0 0.005
cd <skill_dir>/scripts && python3 agent.py tp WETH 2000 5.0 0.005
cd <skill_dir>/scripts && python3 agent.py monitor
```

### 查看投资组合
```bash
cd <skill_dir>/scripts && python3 agent.py balances
cd <skill_dir>/scripts && python3 agent.py wallet
```

## 支持的链
- Base（链ID：8453）

## 支持的DEX
- Uniswap V3

## 相比Bankr的主要优势
- **零交易手续费**（仅收取Gas费用）
- **免费提供止损/止盈功能**（无需订阅服务）
- **用户自行管理私钥**（完全控制资产）
- **交易执行速度更快**（约3秒，相比Bankr的约20秒）
- **开源且可定制**

## 安全提示
- 私钥存储在本地，不会被传输到任何外部服务器
- 建议始终启用滑点保护功能（默认设置为1%）
- 开始使用时建议使用少量资金进行测试
- 本文档仅提供技术指导，不构成任何财务建议