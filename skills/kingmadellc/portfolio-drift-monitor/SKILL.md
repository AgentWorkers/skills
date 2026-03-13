---
name: Portfolio Drift Monitor
description: "实时Kalshi投资组合漂移警报功能：监控投资组合的持仓情况，并在持仓变动超出您设定的阈值时发出警报。该功能通过快照对比来检测变化，同时限制检查频率以避免频繁的系统负担；此外还提供方向性指示（通过表情符号表示）。系统每小时自动检查一次，以便及时捕捉早晨和晚间简报之间的持仓波动。该功能是OpenClaw预测市场交易栈（OpenClaw Prediction Market Trading Stack）的一部分，属于风险管理模块，与Kalshi指挥中心（Kalshi Command Center）及市场晨报（Market Morning Brief）协同使用。"
---
# 投资组合漂移监控器

实时监控您在 Kalshi 平台上的投资组合持仓情况，并在持仓发生显著变动时发送可配置的警报。非常适合活跃的交易者，用于追踪风险敞口、损益波动以及持仓集中度。

## 概述

投资组合漂移监控器会持续跟踪您的 Kalshi 持仓情况，并在任何持仓超出您设定的阈值百分比时发出警报。其功能包括：

- **比较持仓快照**：当前持仓与上次记录的快照进行对比
- **检测漂移**：标记出变动幅度达到或超过阈值（默认为 5%）的持仓
- **限制 API 调用频率**：防止过度使用 API（可配置，默认间隔为 60 分钟）
- **警报格式化**：使用表情符号（📈/📉）、方向箭头和价格变化来显示警报信息
- **持久化数据存储**：将快照保存在本地文件 `~/.openclaw/state/portfolio_snapshot.json` 中

## 适用场景

- 如果您在夜间持有 Kalshi 持仓，并希望在持仓发生剧烈变动时收到警报
- 需要在每日晨会和晚会之间每小时检查一次持仓情况
- 管理多个持仓并希望尽早发现集中风险
- 希望有一个轻量级的风险监控工具，能够自动运行而无需人工干预

## 先决条件

- **kalshi_python SDK**：通过 `pip install kalshi-python` 安装
- **Kalshi API 凭据**：环境变量 `KALSHI_KEY_ID` 和 `KALSHI_KEY_PATH`
- **API 密钥文件**：位于 `KALSHI_KEY_PATH` 指定的路径（通常为 `~/.kalshi/key.pem`）

## 配置

请设置以下环境变量或修改默认值：

| 变量          | 默认值         | 作用                |
|----------------|-----------------|-------------------|
| `KALSHI_KEY_ID`     | （必填）       | 您的 Kalshi API 密钥 ID（来自 dev.kalshi.com） |
| `KALSHI_KEY_PATH`     | （必填）       | Kalshi 私钥文件路径（ES256 PEM 格式）     |
| `PORTFOLIO_DRIFT_THRESHOLD` | `5.0`         | 触发警报的百分比变化（例如 5%）     |
| `PORTFOLIO_DRIFT_INTERVAL` | `60`         | 检查间隔（用于限制 API 调用频率）     |

## 使用方法

您可以使用以下命令来触发监控：

- `check portfolio drift`          | 检查投资组合漂移情况          |
- `portfolio alert`            | 发送投资组合警报            |
- `position monitor`           | 监控持仓情况            |
- `drift check`            | 检查漂移情况            |

## 工作原理

### 第一步：获取当前投资组合信息

该工具会调用 Kalshi 的 API 来获取您当前的所有持仓信息：

```bash
python scripts/portfolio_drift.py
```

此步骤会从环境变量中读取 `KALSHI_KEY_ID` 和 `KALSHI_KEY_PATH`，进行身份验证后获取所有持仓数据。

### 第二步：加载之前的快照

首次运行时，会创建一个基准快照；后续运行时，会将当前持仓与上次保存的快照进行比较。

### 第三步：检测漂移

对于每个持仓，计算以下指标的百分比变化：
- **持仓数量**
- **未实现损益（USD 价值）**
- **价格**（平均买入价与当前价格）

如果任何指标的变化幅度达到或超过阈值，就会标记该持仓。

### 第四步：格式化并输出警报

输出包含以下内容的警报信息：
- 方向性表情符号（📈/📉）
- 持仓代码及方向（买入/卖出）
- 百分比变化（带符号显示，例如 “+12.5%”）
- 自上次检查以来的时间

### 第五步：更新快照

将当前的投资组合信息保存为新的基准数据，以供下一次检查使用。

## 输出格式

以下是一个持仓发生漂移的示例输出：

```
📈 YES/TRUMP.25DEC → +12.5% (↑$1,250 P&L, ↑350 shares)
   Last check: 47 minutes ago

📉 NO/ELEX.HOUSEGOV → -8.3% (↓$425 unrealized P&L)
   Last check: 42 minutes ago

No significant drift: KALSHI.USD, CRYPTO.BTC
```

### 错误处理

- **首次运行**：创建基准快照，不发送警报
- **API 请求失败**：记录错误信息，不更新快照
- **达到调用频率限制**：如果未达到指定间隔，则跳过检查
- **无持仓**：输出 “投资组合为空”

## 命令示例

- `check portfolio now`          | 立即检查投资组合漂移情况        |
- `check with custom threshold`       | 使用自定义阈值进行检查        |
- `check and see full state file`     | 查看完整的状态文件          |

## 阈值调整

| 配置方案 | 阈值           | 检查间隔           | 适用场景            |
|---------|-----------------|-----------------|-------------------|
| **严格**    | 3%            | 30 分钟           | 活跃日内交易，持仓较多         |
| **标准**    | 5%            | 60 分钟           | 默认设置，平衡信号与噪声比例     |
| **宽松**    | 10%            | 120 分钟           | 长期持仓，减少警报次数       |
| **敏感型**    | 2%            | 15 分钟           | 基于新闻的交易策略         |

## 与 OpenClaw 生态系统的集成

该工具是预测市场交易栈中的风险管理组件，可定时每小时检查一次持仓情况，以便在晨会和晚会之间及时发现持仓波动。

**调度示例**：
```yaml
skills:
  portfolio-drift-monitor:
    enabled: true
    schedule: "0 * * * *"  # Every hour
    timeout_seconds: 30
```

| 连接的技能        | 连接方式                |
|----------------|----------------------|
| **市场晨会**       | 通过晨会/晚会获取最新持仓信息       |
| **Kalshi 命令中心**     | 通过命令中心监控持仓情况         |
| **Kalshalyst**       | 通过反向分析跟踪持仓风险         |

**安装完整工具栈**：
```bash
clawhub install kalshalyst kalshi-command-center polymarket-command-center prediction-market-arbiter xpulse portfolio-drift-monitor market-morning-brief personality-engine
```

## 性能与成本

- **运行时间**：每次检查少于 5 秒
- **API 调用次数**：1 次（读取投资组合信息）
- **成本**：0 美元（Kalshi 提供免费服务）
- **状态文件大小**：约 2KB（`portfolio_snapshot.json`）

## 扩展性

每天 24 次检查（每小时一次）相当于 24 次 API 调用，完全在免费服务范围内。

## 调试

请查看日志和状态文件：
```bash
# View current snapshot
cat ~/.openclaw/state/portfolio_snapshot.json | python -m json.tool

# Run manually with debug output
python -u scripts/portfolio_drift.py 2>&1 | head -50

# Verify credentials
echo $KALSHI_KEY_ID
ls -la $KALSHI_KEY_PATH
```

## 代理漏洞修复流程

**重要提示**：当您（作为代理）在运行过程中发现并修复了脚本中的漏洞，必须使用文件编辑工具将修复代码直接写入磁盘中的源文件。仅通过聊天展示修复内容是不够的——因为下一次自动运行时会重新开始新的会话，之前的修复内容将不会被应用。

发现漏洞后的操作步骤：
1. 修改磁盘上的实际 `.py` 文件（例如 `~/skills/portfolio-drift-monitor/scripts/portfolio_drift.py`）
2. 同时更新 `~/.openclaw/skills/portfolio-drift-monitor/scripts/portfolio_drift.py` 中的副本
3. 在确认两个文件都已更新后，再告知用户修复完成
4. 如果修复内容较为复杂，请在 `~/skills/` 目录下提交 Git 提交

**注意**：如果您仅在聊天中展示了修复方案，切勿直接声明 “问题已修复”。

## 已知限制

- **仅支持 Kalshi 平台**：目前仅支持监控 Kalshi 平台上的持仓。Polymarket 平台上的持仓需要单独跟踪。
- **基于价格的漂移计算**：漂移幅度是根据市场中间价计算的，而非成交量或未平仓合约数量。
- **警报传输方式**：警报信息直接输出到标准输出（stdout），需要通过 OpenClaw 代理或其他脚本（如 iMessage、Slack 等）来传递。

## 额外资源

- 完整的配置指南请参考 [drift-config.md](references/drift-config.md)
- API 详细信息请参阅 [kalshi_python SDK 文档](https://docs.kalshi.com)

---

## 反馈与问题

- 发现漏洞？有功能需求？想分享使用效果吗？
- **GitHub 问题报告**：[github.com/kingmadellc/openclaw-prediction-stack/issues](https://github.com/kingmadellc/openclaw-prediction-stack/issues)
- **X/Twitter**：[@KingMadeLLC](https://x.com/KingMadeLLC)

本工具属于 **OpenClaw 预测市场工具栈** 的一部分，是 ClawHub 平台上首个预测市场相关的功能模块。