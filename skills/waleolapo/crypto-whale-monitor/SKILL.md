---
name: crypto-whale-monitor
description: 通过 Web3 RPC 在链上监控大型加密货币钱包（即“大户”）的余额，以检测可能引发市场波动的活动。可以从 `references/wallets.md` 文件中读取钱包地址，或者接受用户提供的自定义钱包地址。
---
# 加密鲸鱼监控工具（Crypto Whale Monitor）

该工具包含用于连接区块链浏览器并追踪特定“鲸鱼”钱包（即持有大量加密货币的账户）的逻辑。

## 工作流程：
1. **定义钱包地址**：将已知的鲸鱼钱包地址添加到 `references/wallets.md` 文件中。
2. **执行监控**：运行 `npm start`（或 `./scripts/monitor.js`）以开始扫描这些钱包的余额。
3. **分析结果**：查看输出信息，寻找“WHALE DETECTED”（即检测到鲸鱼钱包）的警告信息。
4. **定时监控**：设置定时任务（cron job），定期运行 `npm start` 以自动执行监控。

## 脚本：
- `scripts/monitor.js`：通过公共 RPC 接口检查钱包余额的核心脚本。默认从 `references/wallets.md` 文件中读取钱包地址列表。

## 参考文件：
- `references/wallets.md`：包含所有已知、公开的鲸鱼钱包地址的列表。