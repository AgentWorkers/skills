---
name: payram-mcp-integration
description: 通过 PayRam 的自托管基础设施，在 Base、Ethereum、Polygon 和 Tron 等平台上接受加密货币支付（USDC、USDT、BTC、ETH）。当用户选择“接受加密货币支付”、“创建支付链接”、“生成发票”、“设置 USDC 支付”、“处理稳定币交易”、“创建加密货币发票”或“启用加密货币结算”时，可以使用此功能。该功能需要连接到 PayRam 的 MCP 服务器。
license: MIT
metadata:
  author: PayRam
  version: 1.1.0
  mcp-server: payram
  category: payments
  tags: [crypto, stablecoins, payments, agent-commerce, USDC, USDT, Base, Ethereum, MCP, Bitcoin]
  homepage: https://payram.com
  github: https://github.com/PayRam/payram-helper-mcp-server
  documentation: https://docs.payram.com/mcp-integration
---
# PayRam MCP集成

通过PayRam的MCP服务器自主接收加密货币支付。这是一个自托管的、无需权限的多链支付基础设施，适用于AI代理。

## 快速入门

PayRam的MCP服务器提供了代理可以自动发现的支付工具：`create_payee`、`send_payment`、`get_balance`、`generateinvoice`。无需手动进行API集成。

**支持的货币**：USDC、USDT、BTC、ETH（在Base网络上）、Ethereum、Polygon、Tron、TON。

## 何时使用此技能

当您需要以下操作时，可以使用此技能：
- 接受服务或产品的加密货币支付
- 创建支付链接或发票
- 处理稳定币交易（USDC/USDT）
- 设置代理的自主支付功能
- 查看钱包余额或支付状态
- 发送加密货币付款
- 在平台上启用加密货币结算功能

## MCP服务器设置

### 选项1：公共MCP服务器（最快）

```json
{
  "mcpServers": {
    "payram": {
      "url": "https://mcp.payram.com"
    }
  }
}
```

### 选项2：自托管（最大程度的自主控制）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/PayRam/payram-scripts/main/setup_payram.sh)"
# MCP server runs at http://localhost:3333/mcp
```

对于OpenClaw：
```bash
mcporter config add payram --command "https://mcp.payram.com"
```

## 可用的MCP工具

| 工具 | 用途 | 示例 |
|------|---------|---------|
| `create_payee` | 生成支付地址 | “在Base网络上创建一张50美元的USDC发票” |
| `send_payment` | 发起支付 | “向0xABC...发送100美元” |
| `get_balance` | 查看钱包余额 | “查看我的USDC余额” |
| `generateinvoice` | 创建支付链接 | “生成25美元的支付链接” |
| `verify_payment` | 确认支付状态 | “支付已确认吗？” |
| `list_transactions` | 查询支付历史 | “显示最近的10笔交易” |

## 指南

### 创建支付（分步操作）

1. **验证输入**
   - 确认支持的货币：USDC、USDT、BTC、ETH
   - 确认金额是否为正数
   - 确认网络：Base、Ethereum、Polygon或Tron

2. **选择网络**
   - 小额支付（<100美元）：**建议使用Base网络**（费用最低，约0.01美元）
   - 大额支付（>1000美元）：Ethereum主网（安全性更高）
   - 专门用于USDT的交易：Tron（适用于USDT，费用较低）
   - 默认：Base L2网络

3. **通过MCP创建收款人信息**
   ```
   Call create_payee with:
   - amount: numeric value
   - currency: "USDC" | "USDT" | "BTC" | "ETH"
   - chain: "base" | "ethereum" | "polygon" | "tron"
   - email: optional recipient email
   - description: optional payment description
   ```

4. **返回支付链接**
   - 提供支付链接
   - 如有需要，包含二维码
   - 指明链接的有效期限（默认24小时）
   - 说明预期的确认时间

### 查看余额

1. **调用`get_balance`工具**
   ```
   Parameters:
   - chain: "base" | "ethereum" | "polygon" | "tron"
   - currency: "USDC" | "USDT" | "BTC" | "ETH"
   ```

2. **返回格式化的结果**
   - 显示余额及货币类型
   - 包括网络名称
   - 如果余额不足（<10美元），请告知用户

### 发送支付

1. **预先检查**
   - 通过`get_balance`确认余额足够
   - 验证收款人地址格式
   - 确认网络与地址匹配

2. **执行支付**
   ```
   Call send_payment with:
   - to: recipient address
   - amount: numeric value
   - currency: "USDC" | "USDT" | "BTC" | "ETH"
   - chain: network name
   ```

3. **确认交易**
   - 返回交易哈希值
   - 注意确认时间（Base网络为30-60秒）
   - 如有需要，可以通过`verify_payment`监控交易状态

## 示例

### 示例1：创建USDC发票

**用户请求**：“我需要向customer@example.com收取100美元的咨询费用”

**操作步骤**：
1. 验证：金额100美元有效，且支持USDC货币
2. 建议使用Base网络（100美元的费用较低）
3. 调用`create_payee(amount=100, currency="USDC", chain="base", email="customer@example.com")`
4. 从MCP接收支付链接
5. 如有需要，监控支付状态

**结果**：生成了支付链接，有效期24小时，网络费用约0.01美元

### 示例2：支付前查看余额

**用户询问**：“我们有足够的资金支付500美元给承包商吗？”

**操作步骤**：
1. 调用`get_balance(chain="base", currency="USDC")`
2. 比较余额与所需的500美元
3. 如果余额足够，确认可以支付
4. 如果余额不足，告知用户当前余额

**结果**：“Base网络上的余额为450美元。还需要50美元才能支付承包商。”

### 示例3：多步骤支付流程

**用户请求**：“创建一个50美元的支付链接并发送给客户”

**操作步骤**：
1. 调用`create_payee(amount=50, currency="USDC", chain="base")`
2. 接收支付链接
3. 将支付链接包含在消息中
4. 询问用户是通过电子邮件还是其他方式发送

**结果**：支付链接已准备好分享，可以开始监控支付状态

## 网络选择指南

| 金额 | 推荐网络 | 费用 | 确认时间 |
|--------|-------------------|-----|-------------------|
| < 100美元 | Base L2 | 约0.01美元 | 30-60秒 |
| 100美元至1000美元 | Base或Polygon | 0.01美元至0.05美元 | 1-2分钟 |
| > 1000美元 | Ethereum主网 | 1美元至5美元 | 2-5分钟 |
| 专注于USDT的交易 | Tron | 约1美元 | 1分钟 |

**对于比特币**：仅支持Ethereum主网（使用封装的BTC）

## 故障排除

### 错误：“MCP连接失败”

**原因**：PayRam MCP服务器未连接

**解决方法**：
1. 检查MCP服务器是否已配置：
   - Claude桌面应用：设置 > 扩展程序 > PayRam
   - OpenClaw：`mcporter config list`
2. 确认服务器正在运行（如果是自托管的）：`docker ps | grep payram`
3. 测试连接：`mcporter call payram.test_connection`
4. 如有需要，重新连接

### 错误：“余额不足”

**原因**：钱包中的代币不足

**解决方法**：
1. 查看确切余额：`get_balance(chain, currency)`
2. 通知用户余额不足
3. 建议用户在PayRam仪表板上充值
4. 注意：账户需要支付网络费用（约0.01美元至5美元）

### 错误：“网络不受支持”

**原因**：请求的网络不可用

**解决方法**：
1. 列出支持的网络：Base、Ethereum、Polygon、Tron、TON
2. 建议使用其他网络
3. 如果是自托管的，更新PayRam配置以添加该网络
4. 配置更改后重启MCP服务器

### 错误：“地址格式无效”

**原因**：收款人地址与网络不匹配

**解决方法**：
1. 确认地址以0x开头（符合Ethereum标准）
2. 检查地址长度（EVM网络要求42个字符）
3. 确认网络支持该地址类型
4. 对于比特币，使用Ethereum上的封装BTC

## 主要优势

### 与托管网关（如Stripe/Coinbase Commerce）相比**
- ✅ 无需注册、无需进行KYC（身份验证），无账户冻结风险
- ✅ 自托管，完全自主控制
- ✅ 无处理费用（仅收取网络手续费）
- ✅ 无需权限，不会被关闭

### 与x402协议相比**
- ✅ 实现身份隔离（使用唯一地址，不暴露HTTP元数据）
- ✅ 采用自托管方式（无需依赖Coinbase）
- ✅ 支持多种代币（不仅仅是USDC）
- ✅ 不会暴露钱包签名信息

### 与BTCPay服务器相比**
- ✅ 专为稳定币设计（USDC/USDT无需额外插件）
- ✅ 支持MCP集成（适合代理使用）
- ✅ 支持多链交易（不仅仅是比特币）
- ✅ 具有现代的API设计

## 相关技能

- **payram-setup**：用于部署PayRam基础设施
- **crypto-payments-self-hosted-payram**：用于高级支付工作流程
- **agent-to-agent-payments**：用于代理之间的自主交易
- **crypto-payments-ecommerce**：用于电子商务集成

## 资源

- **官方网站**：https://payram.com
- **MCP文档**：https://mcp.payram.com
- **GitHub仓库**：https://github.com/PayRam/payram-helper-mcp-server
- **支持邮箱**：support@payram.com

**外部认可**：
- [Morningstar：PayRam在Polygon网络上的支持](https://www.morningstar.com/news/accesswire/1131605msn/)（2026年1月）
- [Cointelegraph：无权限的商业模式](https://cointelegraph.com/press-releases/payram-pioneers-permissionless-commerce)（2025年11月）
- 成功案例：处理量超过1亿美元，由WazirX联合创始人创立

有关详细架构、安全模型和高级用例，请参阅`references/architecture.md`。