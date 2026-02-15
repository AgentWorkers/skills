---
name: axelrod
description: 基于人工智能的Base-chain交易和链上查询代理，支持通过自然语言进行操作。适用于用户需要买卖/兑换代币、设置自动化交易策略（如DCA、限价单、RSI指标）、查看投资组合余额、查询代币信息与分析结果、检查订单状态、管理止盈/止损订单，或咨询与Base-chain相关的加密货币/DeFi相关问题的场景。请务必运行`axelrod_chat.py`脚本以获取实时数据。
---

# Axelrod

通过AIxVC AI自动化功能，可以使用自然语言执行基础链（Base-chain）交易和链上查询操作。

## 快速入门

### 首次设置

1. 在OpenClaw的`skills.entries.axelrod.env`文件中配置凭证：

```json
{
  "skills": {
    "entries": {
      "axelrod": {
        "enabled": true,
        "env": {
          "AIXVC_ACCESS_KEY": "your_access_key",
          "AIXVC_SECRET_KEY": "your_secret_key"
        }
      }
    }
  }
}
```

2. 安装依赖项：

```bash
pip install -r skills/axelrod/requirements.txt
```

3. 验证设置：

```bash
python skills/axelrod/scripts/axelrod_chat.py --message "check my balance"
```

## 核心用法

### 简单查询

对于能够快速完成的简单请求：

```bash
python skills/axelrod/scripts/axelrod_chat.py --message "check my ETH balance"
python skills/axelrod/scripts/axelrod_chat.py --message "what is ETH price now"
```

### JSON调试模式

用于查看完整的API响应：

```bash
python skills/axelrod/scripts/axelrod_chat.py --message "check my balance" --json
```

## 强制工作流程

1. **检查AK/SK** — 如果缺少`AIXVC_ACCESS_KEY`或`AIXVC_SECRET_KEY`，请让用户进行配置。切勿猜测或伪造凭证。
2. **运行脚本** — 每当需要实时链上数据或执行操作时，务必运行命令行界面（CLI）。不要仅依赖模型内存来响应请求。
3. **返回标准输出（stdout）** — 捕获脚本的标准输出并返回给用户。允许进行简单的格式化，但不要遗漏关键结果（金额、交易哈希值、确认密钥、错误信息）。
4. **处理确认** — 如果响应中包含`confirmKey`，引导用户进行确认或取消操作（详见下面的确认流程）。

## 功能概述

### 交易操作

- **现货买卖/兑换**：在基础链上进行代币交易
- **DCA**：自动化的定投策略（例如：“每天向ETH定投20u”）
- **限价/触发订单**：在目标价格或盈亏率时执行交易
- **RSI策略**：基于RSI指标的条件交易（例如：“如果1小时RSI < 30，则买入100u BTC”）
- **止盈/止损**：通过`QUERY_ALGO`实现自动化风险管理

**参考文档**：[references/api.md](references/api.md)

### 查询操作

- **余额查询**：单个代币或全部资产的投资组合
- **代币信息与分析**：合约详情、小数位数、分析数据
- **价格查询**：实时价格及24小时内的价格变化
- **订单查询**：活跃订单列表及详细信息
- **止盈/止损订单查询**：止盈/止损订单的状态

### 区块链辅助

- 提供关于加密货币/去中心化金融（DeFi）领域的问答及交易指导
- 提供基础链上的交易计划建议

## 确认流程

通常，交易需要经过风险控制确认；小额交易（约≤10美元）可能可以跳过确认步骤。`confirmKey`的有效时间为**10分钟**。

当响应中包含`confirmKey`时，请用户发送以下内容之一：

```text
yes, please execute <confirmKey>
no, please cancel <confirmKey>
```

如果密钥已过期，用户必须重新提交原始请求。

## 当前限制

| 限制 | 详情 |
| ---------- | ------- |
| 链路** | 仅支持基础链（Base） |
| 多笔交易**：每条消息只能发送一笔交易；如有需要，请让用户分次发送 |
| 不支持的功能**：杠杆交易、期货/期权、借贷、跨链交易、NFT、法定货币的充值/提现 |

## 常见操作模式

### 交易前检查

```bash
# Check balance
python skills/axelrod/scripts/axelrod_chat.py --message "check my ETH balance"

# Check price
python skills/axelrod/scripts/axelrod_chat.py --message "what is ETH price now"

# Then trade
python skills/axelrod/scripts/axelrod_chat.py --message "buy 50u of ETH"
```

### 自动化策略

```bash
# DCA strategy
python skills/axelrod/scripts/axelrod_chat.py --message "DCA 20u into ETH every day"

# RSI conditional strategy
python skills/axelrod/scripts/axelrod_chat.py --message "if 1h RSI < 30, buy 100u BTC"

# Limit order
python skills/axelrod/scripts/axelrod_chat.py --message "buy ETH when price drops to 2500"
```

### 投资组合审核

```bash
# Full portfolio
python skills/axelrod/scripts/axelrod_chat.py --message "check my balance"

# Token analysis
python skills/axelrod/scripts/axelrod_chat.py --message "analyze AXR token for me"

# Order status
python skills/axelrod/scripts/axelrod_chat.py --message "show my recent orders"
```

## 错误处理

### 错误代码

| 代码 | 含义 | 解决方案 |
| ---- | ------- | ---------- |
| `0` | 成功 | — |
| `2` | 缺少AK/SK | 请让用户配置`AIXVC_ACCESS_KEY`和`AIXVC_SECRET_KEY` |
| `3` | HTTP请求失败或响应格式不正确（非JSON） | 检查网络连接，确认端点是否可访问 |
| `4` | API业务错误（代码不在成功范围内） | 阅读错误信息，并指导用户解决问题 |

### 常见问题

| 问题 | 解决方案 |
| ----- | ---------- |
| “请先登录” | AK/SK配置错误 — 重新配置凭证 |
| 认证错误 | 确认AK/SK正确且未过期 |
| 资金不足 | 减少交易金额或补充资金 |
| 代币未找到 | 检查代币符号或合约地址 |
| confirmKey过期 | 重新提交原始交易请求 |
| 一条消息中包含多笔交易 | 将交易拆分为多个请求发送 |

## 按类别划分的示例命令

### 交易

- `"买入50u AXR"`
- `"卖出我50%的ETH"`
- `"将10 SOL兑换成ETH"`

### 自动化策略

- `"每天向ETH定投20u"`
- `"如果1小时RSI < 30，则买入100u BTC"`
- `"当ETH价格降至2500时买入ETH"`

### 投资组合与查询

- `"查看我的余额"`
- `"显示AXR代币信息"`
- `"当前ETH的价格是多少？」`
- `"显示我的最近交易记录"`
- `"显示我的止盈/止损订单"`

### 区块链辅助

- `"帮我分析AXR代币"`
- `"帮我制定基础链交易计划"`

## 最佳实践

### 安全性

1. 绝不要分享你的AK/SK凭证
2. 从小额测试开始
3. 在进行大额交易前核实代币地址
4. 在执行交易前仔细检查确认信息

### 交易注意事项

1. 交易前检查余额
2. 明确指定交易金额（例如“50u”、“50%”、“0.1 ETH”）
3. 从小额交易开始，验证后再逐步增加交易量
4. 使用限价订单以获得更好的入场价格
5. 设置止盈/止损来管理风险

## API参考

有关完整的API合约、SigV4签名协议、请求/响应格式以及响应字段的详细信息，请参考：

**参考文档**：[references/api.md](references/api.md)

## 实现说明

- 该脚本使用AK/SK和SigV4签名方式与AIxVC进行通信。
- 当前API端点：`https://api.aixvc.io/gw/openapi/v2/public/twa/agent/chat`（`chain-id=base`）。
- 如果文档说明与脚本实际行为不一致，请以脚本实现为准。

## 文件结构

- **SKILL.md** — 代理（agent）的使用说明（本文件）。代理通过阅读此文件来了解如何使用该功能。
- **README.md** — 面向用户的设置和使用指南。
- **scripts/axelrod_chat.py** — 命令行客户端。使用`python skills/axelrod/scripts/axelrod_chat.py --message "<instruction>"`来调用该脚本。
- **references/api.md** — 完整的API合约和签名相关参考资料。
- **requirements.txt** — 所需的Python依赖库（`requests`）。

## 故障排除

### 脚本无法运行

```bash
# Ensure Python 3 is available
python --version

# Install dependencies
pip install -r skills/axelrod/requirements.txt

# Test connectivity
curl -I https://api.aixvc.io
```

### API错误

请参考上述错误代码和常见问题。如果问题仍然存在：

1. 查看标准错误输出（stderr）中的错误信息
2. 使用`--json`模式查看完整的API响应
3. 验证AK/SK配置
4. 先尝试执行一个简单的查询（例如“查看我的余额”）

---

**💡 专业提示**：最常见的原因是AK/SK凭证缺失或配置错误。遇到问题时，请务必先核实凭证信息。

**⚠️ 安全提示**：请妥善保管你的AK/SK凭证。切勿将凭证提交到版本控制系统中。只进行你能承受损失的交易。

**🚀 快速上手建议**：首先查看你的余额以确认设置是否正确，然后尝试进行小额交易（例如“买入1u ETH”），熟悉整个操作流程。