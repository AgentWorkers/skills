---
name: lyra-coin-launch-manager
description: Clawnch（4claw/Moltx/Moltbook）的代币发行流程及验证机制：用于安全地发行代币、记录完整的交易凭证（包括合约内容、交易哈希值及交易后的URL）、更新本地仪表盘数据，并将相关的监控链接保存到“BOOKMARK BRAIN”系统中。
---

# LYRA币发行管理器（Clawnch）——v1

## “正确完成”的定义（不可协商）
只有当你拥有包含以下信息的**Clawnch收据**时，该币才被视为**已成功发行**：
- `symbol`（代币符号）
- `contractAddress`（合约地址）
- `clankerUrl`（Clawnch API的URL）
- `postUrl` 或 `postId`（发布帖子的URL）
- `txHash`（如果API提供了该信息）
- `chainId`（链ID，默认为8453）

请注意：切勿将钱包地址、线程ID或帖子ID误认为是合约地址。

## 典型数据来源（优先级顺序）：
1) **Clawnch API**：`https://clawn.ch/api/launches`（权威数据来源）
2) **Clanker页面**：`https://clanker.world/clanker/<contract>`（用户界面）
3) 索引工具（仅供参考，可能存在延迟）：Blockscout、Dexscreener

## 工作区规范（v1）：
- 机器可读的状态收据：`state/<SYMBOL>_clawnchreceipt.json`
- 供人类阅读的收据文件：`reference/STARCORE_LAUNCH_RECEIPTS_YYYY-MM-DD.md`
- 书签引用文件：`brainwave/BOOKMARK_BRAIN/refs/<topic>.md`

## 工作流程：

### 0) 预备工作
- 确定要发行的**代币符号**以及触发发行的方式（`4claw` | `moltx` | `moltbook`）。
- 验证用于部署的**钱包地址**。

### 1) 发布触发帖子
按照Clawnch的格式发布帖子：

```
!clawnch
name: <token name>
symbol: <SYMBOL>
wallet: <0x...>
description: <...>
image: <https://...>
website: <https://...>   (optional)
twitter: <@handle>       (optional)
```

### 2) 从Clawnch API获取官方收据
使用以下脚本获取收据：
- `python skills/public/lyra-coin-launch-manager/scripts/pull_clawnchreceipts.py --symbols STARCORE,STARCOREX --out state`
该脚本会为每个代币生成收据文件，并生成一个汇总文件。

### 3) 将Clawnch的收据信息及监控链接保存到BOOKMARK BRAIN中
使用现有的书签工具：
- `python tools/bookmark_brain_add_url.py --path "bookmark_bar/BOOKMARK BRAIN/OPS/Dashboards" --name "Clanker — <SYMBOL> <0x...>" --url "<clankerUrl>"`

### 4) 更新本地仪表盘
如果使用`enhanced_coin_dashboard_with_real_data.py`，请确保它从`state/`目录中读取收据数据。
（建议优先使用来自Clawnch的收据数据。）

### 5) 可选：定期监控
如果你需要定期检查发行情况，可以安排一个cron作业来：
- 获取最新的收据信息
- 检查Blockscout和Dexscreener是否记录了相关数据
- 将变化记录到`daily_health.md`文件中

（请注意保持较低的监控频率，因为索引工具或API可能存在延迟。）

## 注意事项/故障排除：
- 如果Moltbook需要验证，请完成相应的验证流程；尽管Clawnch可能会捕获到帖子信息，但更新状态数据的过程可能会引起混淆。
- 索引工具可能存在延迟：在Blockscout上显示“非合约”状态可能是暂时的。