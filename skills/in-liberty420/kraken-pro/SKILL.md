---
name: kraken-pro
description: 管理Kraken交易所账户——包括投资组合、市场数据、交易操作、收益/质押功能以及账本导出等。通过`python-kraken-sdk`提供REST API接口。适用于用户需要查看加密货币投资组合、获取价格信息、下达/取消交易订单、管理质押操作、导出账本以用于税务申报、存取资金，或以任何方式与Kraken交易所进行交互的场景。
---

# Kraken Skill

通过命令行界面（CLI）管理您的Kraken交易账户。

## 设置

```bash
pip3 install -r requirements.txt
```

通过环境变量或`skill`目录中的`.env`文件设置凭据：
```
KRAKEN_API_KEY=your_key
KRAKEN_API_SECRET=your_secret
```

获取API密钥：https://www.kraken.com/u/security/api

## 命令

运行：`python3 kraken_cli.py <命令> [选项]`

所有命令都支持`--json`选项，以获取原始JSON格式的输出。

### 投资组合（需要授权）

| 命令 | 描述 |
|---------|-------------|
| summary | 投资组合概览（正确处理灵活收益和固定收益） |
| net-worth | 单一资产净值 |
| holdings | 资产明细（以美元计价） |
| balance | 资产数量 |

### 市场数据（无需授权）

| 命令 | 描述 |
|---------|-------------|
| ticker --pair XBTUSD | 价格及24小时统计数据 |
| pairs | 交易对 |
| assets | 资产列表 |

### 订单历史（需要授权）

| 命令 | 描述 |
| open-orders | 活动中的订单 |
| closed-orders [--limit N] | 已完成的订单 |
| trades [--limit N] [--csv] | 交易执行历史（可导出为CSV格式） |

### 账户明细（需要授权）

```
ledger [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--asset BTC] [--type trade|deposit|withdrawal|staking] [--csv] [--limit N]
```

支持分页查询（Kraken每次请求返回最多50条数据）。`--csv`选项可导出原始数据。

### 交易（需要授权）

所有交易命令都需要`--confirm`选项。使用`--validate`选项进行模拟交易。

| 命令 | 描述 |
|---------|-------------|
| buy --pair XBTUSD --type market\|limit --amount N [--price P] --confirm | 下单购买 |
| sell --pair XBTUSD --type market\|limit --amount N [--price P] --confirm | 下单出售 |
| cancel-order --id OXXXXX --confirm | 取消特定订单 |
| cancel-all --confirm | 取消所有未完成的订单 |

**在实际下单前请务必与用户确认。建议先使用`--validate`进行模拟交易。**

### 收益/质押（需要授权）

| 命令 | 描述 |
| earn-positions | 当前的质押情况 |
| earn-strategies | 可用的收益策略 |
| earn-status | 待处理的请求 |
| earn-allocate --strategy-id ID --amount N --confirm | 质押资金 |
| earn-deallocate --strategy-id ID --amount N --confirm | 解锁资金 |

### 资金管理（需要授权）

| 命令 | 描述 |
| deposit-methods --asset BTC | 某资产的存款方式 |
| deposit-address --asset BTC | 获取存款地址 |
| withdraw --asset BTC --key NAME --amount N --confirm | 向保存的地址转账 |
| withdraw-status | 最近的提款状态 |

**提款注意事项：**
- 地址必须预先在Kraken的网页界面中配置（无法通过API添加）
- 无法通过API查询保存的地址名称——请向用户获取地址名称
- 每种资产都需要单独配置地址：即使使用相同的钱包，SOL地址也无法用于USDC的提款
- `--key`参数表示Kraken中保存的地址名称，而非实际地址

## 示例用法

| 用户请求 | 命令 |
|---|---|
| 查看我的投资组合？ | summary |
| BTC的价格是多少？ | ticker --pair XBTUSD |
| 导出2025年的账户明细用于报税 | ledger --start 2025-01-01 --end 2025-12-31 --csv |
| 导出交易历史 | trades --csv |
| 以市场价购买0.1 BTC | buy --pair XBTUSD --type market --amount 0.1 --confirm |
| 查看质押情况 | earn-positions |

## Kraken交易对名称规则

Kraken使用非标准的交易对名称：XBT（而非BTC），XETH（而非ETH），法定货币对前缀为Z（例如ZUSD、ZCAD）。如果不确定交易对名称，可以运行`pairs --json`并查找相关资产信息。

## 投资组合逻辑

Kraken有两种收益方式：
- **自动收益（灵活收益）**：计入主钱包的资产余额中
- **固定收益质押**：单独的收益钱包，不计入交易余额

`summary`命令计算的总价值为：**交易余额 + 固定收益质押金额**

## API权限要求

| 功能 | 所需权限 |
|---------|-----------|
| 查看余额、投资组合、账户明细 | 查询资金信息 |
| 查看/修改订单、交易记录 | 查看/取消订单 |
| 下单/取消订单 | 创建/修改订单 |
| 质押/解锁资金 | 提取资金 |
| 提款 | 提取资金 |
| 市场数据 | 无权限要求 |