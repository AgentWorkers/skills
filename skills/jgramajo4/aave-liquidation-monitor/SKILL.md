---
name: aave-liquidation-monitor
description: "主动监控 Aave V3 的借款头寸，并在发生清算风险时发出警报。查询用户在各个链（Ethereum、Polygon、Arbitrum 等）上的抵押品、债务以及借款健康状况（health factor）。当借款健康状况低于可配置的阈值时（临界值为 1.05，警告值为 1.2），会通过 Telegram/Discord/Slack 发送紧急警报。适用于需要持续监控 Aave 借款头寸的情况，希望在清算风险发生前收到警报，或需要定期获取借款健康状况汇总的情况。"
---

# Aave 清算监控工具

## 快速入门

只需配置一次您的钱包和阈值，该工具就会每 6 小时自动运行一次（可配置）。

### 第 1 步：初始化配置

运行 `/aave-config init` 来设置以下内容：
- 您的以太坊钱包地址（仅用于读取；无需私钥）
- 健康因子阈值（默认：临界 1.05，警告 1.2，稳定 >1.5）
- 检查间隔（以小时为单位，默认 6 小时）
- 通知详细程度（详细模式 = 即使状态稳定也会发送每日摘要；简略模式 = 仅发送警报）
- 首选通知渠道（默认为 Telegram，或指定 Discord/Slack）

示例：
```
/aave-config init
→ Wallet: 0x1234...5678
→ Thresholds: 1.05 (critical), 1.2 (warning)
→ Interval: 6 hours
→ Verbosity: quiet (alerts only)
→ Channel: telegram
```

### 第 2 步：测试监控工具

运行 `/aave-monitor check` 以立即获取您的资产状况，并查看警报格式：

```
/aave-monitor check
→ Fetching position for 0x1234...5678 on Ethereum...
→ Health Factor: 2.31 (Stable ✓)
→ Total Collateral: $50,342.12
→ Total Debt: $21,804.00
→ Borrowed Assets: USDC (15,000), WETH (0.5), USDT (6,804)
→ Supplied Assets: WETH (10), USDC (20,000), DAI (30,000)
```

### 第 3 步：启用主动监控

运行 `/aave-monitor enable` 以每 6 小时自动启动检查。该工具会注册一个 cron 作业，在后台静默运行，并仅在健康因子低于阈值时向您发送警报。

如需手动覆盖设置：
```
/aave-monitor enable --interval 4   # Check every 4 hours
/aave-monitor disable               # Stop monitoring
/aave-monitor status                # See current config + last check result
```

## 配置参考

请参阅 `references/config-guide.md` 以获取详细的配置选项、支持的链以及阈值指南。

请参阅 `references/aave-api.md` 以了解 Aave V3 的 GraphQL 架构和查询模式。

**安全与凭证：** 请参阅 `SECURITY.md` 以了解凭证的处理方式及威胁模型。

**针对审计人员：** 请参阅 `SECURITY.md` 以获取代码审查清单和架构详情。

## 工作原理

1. **查询阶段**：使用您的钱包地址调用 Aave V3 GraphQL API。
2. **分析阶段**：提取健康因子、抵押品、债务以及借入/提供的资产信息。
3. **警报逻辑**：
   - 如果健康因子 < 1.05 → **临界**（红色警报，立即发送）
   - 如果健康因子 < 1.2 → **警告**（黄色警报，立即发送）
   - 如果健康因子 > 1.5 → **稳定**（不发送警报，除非启用详细模式）
4. **通知阶段**：将警报信息发送到您配置的渠道，并附上清晰的摘要。
5. **重试逻辑**：如果 API 失败，最多尝试 3 次，并采用指数级退避策略进行重试。

## 错误处理

- **无效的钱包地址** → 记录错误，跳过当前检查，并在下一个时间间隔重新尝试。
- **API 超时** → 最多尝试 3 次，并采用指数级退避策略（2 秒、4 秒、8 秒）。
- **响应格式错误** → 通知您 API 发生变化，并记录完整响应以便调试。
- **网络错误** → 在后台默默重试；只有在所有重试都失败时才会发送警报。

## 安全与凭证

**无需提供或存储私钥** — 该工具仅用于读取数据。

### 消息传递凭证的工作原理

该工具使用 **OpenClaw 的内置消息路由功能** — 它不会存储 Telegram、Discord 或 Slack 的令牌。

1. 您需要在 OpenClaw 中配置消息渠道（不在本工具的配置范围内）。
2. 该工具仅使用警报文本调用 OpenClaw 的消息 API。
3. OpenClaw 会根据您配置的渠道发送消息。

示例：
```
/aave-config set channel telegram
→ OpenClaw sends alerts via your pre-configured Telegram channel
```

**您必须在 OpenClaw 中已经设置好消息渠道。** 请参阅 OpenClaw 的文档以了解如何设置 Telegram/Discord/Slack 集成。

### 数据处理

- **钱包地址：** 存储在 OpenClaw 的加密配置中（除 Aave 的公共 API 外，不会发送给任何外部服务）。
- **API 响应：** 仅解析健康因子数据；敏感的资产状况数据不会被记录。
- **凭证：** 由 OpenClaw 管理，不会存储在工具文件中。

### 该工具可以访问的内容

✅ **Aave GraphQL API（公共接口）** — 用于读取您的资产状况数据。
✅ **OpenClaw 消息路由** — 用于将格式化的警报发送到您配置的渠道。
✅ **Cron 安排器** — 按设定的时间间隔在后台执行检查。

**禁止的操作：**
- 请求私钥。
- 存储 API 令牌。
- 执行交易。
- 修改您的资产状况。

## 示例

### 警报示例

**临界警报（健康因子 < 1.05）：**
```
🚨 AAVE LIQUIDATION RISK – CRITICAL
Health Factor: 1.02 (Liquidation threshold: 1.0)
⏰ Action required immediately!

📊 Position Summary:
Total Collateral: $50,000
Total Debt: $48,000
Debt Ratio: 96%

Borrowed (at risk):
- USDC: 40,000
- WETH: 8 ETH (~$31k)

Suggested Actions:
1. Repay debt (especially WETH)
2. Supply more collateral
3. Enable eMode if available (higher LTV on correlated assets)

Last checked: 2026-02-11 08:15 UTC
```

**警告警报（健康因子 < 1.2）：**
```
⚠️ AAVE WARNING
Health Factor: 1.15 (Approaching 1.2 threshold)

Position approaching liquidation. Consider:
- Repaying $2,000 USDC or
- Adding $5,000 collateral (WETH or stETH)
```

**资产状况稳定（健康因子 > 1.5，仅限详细模式）：**
```
✅ AAVE POSITION HEALTHY
Health Factor: 2.31
Total Collateral: $50,342.12
Total Debt: $21,804.00

All clear. Check again tomorrow.
```

### 命令示例

```bash
# One-time position check
/aave-monitor check

# Start automatic monitoring
/aave-monitor enable

# Change thresholds (e.g., earlier warning at HF 1.3)
/aave-config set thresholds 1.05 1.3

# Check monitoring status
/aave-monitor status

# View last 5 check results with alerts
/aave-monitor history 5

# Disable monitoring temporarily
/aave-monitor disable
```

## 支持的链

主要支持：以太坊主网

在适用的情况下，也可以支持以下链（使用相同的配置地址）：
- Polygon
- Arbitrum
- Optimism
- Base
- Avalanche
- Gnosis

请编辑 `scripts/monitor.js` 以添加更多支持的链或自定义每个链的端点。

## 自定义设置

**更改检查间隔：**
```
/aave-config set interval 4  # Check every 4 hours
```

**更改警报阈值：**
```
/aave-config set thresholds 1.1 1.25  # Critical at 1.1, warning at 1.25
```

**启用详细模式（即使资产状况稳定也会发送每日摘要）：**
```
/aave-config set verbosity verbose
```

**切换通知渠道：**
```
/aave-config set channel discord
```

## 实现细节

请参阅 `scripts/monitor.js` 以了解核心监控逻辑（GraphQL 查询、健康因子计算、警报格式化）。

请参阅 `scripts/cron-runner.js` 以了解如何将 cron 作业与 OpenClaw 的 cron 安排器集成。

## 故障排除

**“无效的钱包地址”** → 检查地址格式：必须为 0x... 格式。尝试运行 `/aave-config view` 以查看当前配置。

**“API 未返回健康因子”** → 您的钱包可能没有在 Aave 中的资产。尝试运行 `/aave-monitor check` 以获取即时响应。

**“API 端点无法访问”** → Aave API 可能暂时不可用。工具会自动重试。请查看 https://status.aave.com。

**“未发送通知”** → 检查您的通知渠道是否已启用。运行 `/aave-monitor check` 以测试通知是否已成功发送。

## 注意事项

- 健康因子 = 总抵押品 / 总债务（扣除清算阈值后的比率）。
- 当健康因子 ≤ 1.0 时，将发生清算。
- 变动债务会累积利息；固定债务的利率是固定的。
- eMode 允许相关资产（例如稳定币、ETH-LST）具有更高的杠杆率。
- 提供的资产作为抵押品；它们会产生利息，但在您被清算时可能会被没收。

---

**最后更新时间：** 2026-02-11 | **状态：** 可以进行配置使用了。