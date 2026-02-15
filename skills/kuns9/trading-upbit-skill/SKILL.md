---
name: trading-upbit-skill
description: Upbit自动化交易系统（采用激进型突破策略），支持通过cron任务一次性执行的命令；具备TopVolume（交易量排名）监控功能，并支持基于百分比的预算分配机制。
user-invocable: true
metadata: {"version":"13.1.0","author":"Kuns9","type":"automated-trading","openclaw":{"requires":{"bins":["node"],"env":["UPBIT_ACCESS_KEY","UPBIT_SECRET_KEY"]},"primaryEnv":"UPBIT_ACCESS_KEY"}}
---
# trading-upbit-skill

这是一个专为 OpenClaw 设计的自动化交易技能，支持在 Upbit 平台上进行本地执行。

## 安装前的注意事项（安全问题）

该技能会使用 Upbit 的 API 密钥来运行自动化交易机器人。在安装或使用生产环境密钥之前，请务必：

1. **检查关键文件**：
   - `scripts/execution/upbitClient.js`（Upbit HTTP 客户端）
   - `scripts/config/index.js`（配置文件及密钥的加载逻辑）
   - `skill.js`（技能的入口脚本）

2. **先进行模拟测试**：
   - 将 `execution.dryRun` 设置为 `true`，然后运行 `node skill.js smoke_test`、`node skill.js monitor_once` 或 `node skill.js worker_once`。

3. **使用平台提供的密钥存储机制**：
   - 通过环境变量（OpenClaw Skills 配置或密钥存储）来配置 API 密钥：
     - `UPBIT_OPEN_API_ACCESS_KEY`
     - `UPBIT_OPEN_API_SECRET_KEY`
   - **切勿将密钥直接存储在 `config.json` 文件中**。

4. **在测试期间限制密钥的使用权限**：
   - 尽量使用小额资金或测试账户进行测试。
   - 密切监控您的 Upbit 账户活动。

5. **快速自我检查**：
   - 运行 `node skill.js security_check` 命令，检查代码中是否存在硬编码的外部 URL（允许的 URL 为 `api.upbit.com`）。

**安全提示**：
- 该技能 **不包含任何数据传输功能**，也不会上传任何数据。
- Upbit API 的基础 URL 已被设置为 `https://api.upbit.com/v1`，并且所有重定向都被禁用了。

## 功能概述

- 监控市场（包括关注列表和可选的成交量最高的交易对）
- 在 `resources/events.json` 文件中生成买入/卖出指令
- 在后台线程中处理这些指令（执行交易或进行模拟测试），并将交易结果保存到 `resources/positions.json` 文件中
- 该技能支持定时任务（Cron）执行：`monitor_once` 和 `worker_once` 命令均为一次性执行。

## 命令说明

### monitor_once
- 执行一次市场监控周期，并将生成的交易指令加入队列。
  - 命令：`node skill.js monitor_once`

### worker_once
- 处理待处理的交易指令（买入/卖出），并更新交易持仓。
  - 命令：`node skill.js worker_once`

### smoke_test
- 验证配置文件和公共 API 端点的可用性（不执行实际交易）。
  - 命令：`node skill.js smoke_test`

## 预算策略（v13）

订单金额可以根据可用韩元（KRW）的百分比来设置，并在同一轮交易中平均分配到多个买入指令中。

**计算公式**：
- `totalBudget = floor((availableKRW - reserveKRW) * pct)`（总预算）
- 如果有 N 个待处理的买入信号，`perOrderKRW = floor(totalBudget / N)`（每个订单的金额），结果向下取整。

## 推荐的定时任务设置

- **监控任务**：每 5 分钟执行一次：
  - 命令：`cd <skillRoot> && node skill.js monitor_once`

- **后台处理任务**：每 1 分钟执行一次：
  - 命令：`cd <skillRoot> && node skill.js worker_once`

## 所需文件

- 必需文件：`config.json`（请勿提交到代码仓库）

- 自动生成的文件：
  - `resources/events.json`
  - `resources/positions.json`
  - `resources/topVolumeCache.json`
  - `resources/nearCounter.json`
  - `resources/heartbeat.json`

- 测试工具：`scripts/tests/*`（详见 README_TESTING.md）

```json
{
  "trading": {
    "budgetPolicy": {
      "mode": "balance_pct_split",
      "pct": 0.3,
      "reserveKRW": 0,
      "minOrderKRW": 5000,
      "roundToKRW": 1000
    }
  }
}
```