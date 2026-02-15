---
name: crypto-whale-monitor
description: 使用 Web3 和 Etherscan 监控链上的大型加密货币钱包交易（即“鲸鱼”交易），以检测可能影响市场走势的活动。当用户请求针对这些大型链上交易的通知或警报时，可启用此功能。
---

# 加密鲸鱼监控工具（Crypto Whale Monitor）

该工具包含用于连接区块链浏览器并追踪特定“鲸鱼”钱包（large-value wallets）大额交易的逻辑。

## 工作流程：
1. **定义钱包地址**：从用户处获取目标鲸鱼钱包的地址列表。
2. **设置交易金额阈值**：设定交易金额的最低阈值（例如：> 1,000,000 美元）。
3. **执行脚本**：使用 `scripts/monitor.js` 脚本，并传入钱包地址列表和交易金额阈值。
4. **定时执行**：利用 `cron` 工具设置定时任务，定期运行该脚本。

## 脚本：
- `scripts/monitor.js`：用于查询 Etherscan/Alchemy API 的核心逻辑。

## 参考资料：
- `references/wallets.md`：已知的公开鲸鱼钱包地址列表。