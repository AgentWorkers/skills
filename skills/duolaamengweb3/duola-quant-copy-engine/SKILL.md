---
name: duola-lobster-agent
description: "这是一个针对 Polymarket 的 `duola` 复制交易 CLI 的机构级执行脚本，适用于 lobster-agent 工作流程。当任务需要生产环境级别的设置和操作时，请使用该脚本：通过 npm 安装/升级软件、领导者的权限配置、交易同步、策略回测、自动交易系统的启动与运行、实时交易控制、故障诊断以及结构化的风险/绩效报告等。"
---
# Duola Lobster Agent

## 概述

作为代理工具链，执行 `duola` 的标准操作工作流程。建议采用分阶段部署的方式：同步（sync）→ 回测（backtest）→ 诊断（doctor）→ 有限范围的实时启动（limited live start）→ 状态/日志审查（status/log review）。

## 计费设置（SkillPay）

在运行时环境中配置一次：

```bash
export SKILLPAY_API_URL="https://skillpay.me"
export SKILLPAY_API_KEY="sk_***"
export SKILLPAY_SKILL_ID="77f983da-1eda-4793-b632-f7502d6beb4b"
export SKILLPAY_PRICE_USDT="0.01"
```

使用支持 `--billing-user-id` 参数的命令进行计费：

支持的命令包括：`sync`、`backtest`、`follow start`、`autopilot onboard`、`autopilot start`。

可以通过 CLI 检查计费端点：

```bash
duola billing balance --user-id <user_id> --output json
duola billing charge --user-id <user_id> --amount 0.01 --output json
duola billing payment-link --user-id <user_id> --amount 1 --output json
```

## 执行工作流程

### 1) 验证运行环境和 CLI

运行以下命令：

```bash
node -v
npm view duola version
duola --version
```

如果 `duola` 未安装，请先进行安装：

```bash
npm install -g duola
```

如果全局安装受到限制，请运行项目本地的 CLI：

```bash
npm install
npm run build
node dist/index.js --version
```

### 2) 注册并检查领导者（Leader）

为每个领导者地址使用唯一的别名。

### 3) 同步数据并进行基线回测

```bash
duola sync <alias> --limit 500 --output json
duola backtest <alias> --lookback 30d --fixed-usd 25 --output json
```

如果回测结果不佳，在进入实时模式前进行调整：
- 增加 `--min-liquidity` 参数的值
- 增加 `--min-time-to-expiry` 参数的值
- 减少 `--fixed-usd` 参数的值

### 4) 运行诊断工具（Doctor）

在进入实时模式前，需要确保 API 连接正常且所有密钥信息正确。

### 5) 启用自动驾驶功能（推荐的使用方式）

使用标准输入（stdin）来输入私钥，并避免显示密钥内容：

```bash
printf '%s' '<private_key>' | duola autopilot onboard <leader_address> \\
  --name <alias> --private-key-stdin --profile balanced --sync-limit 200
```

启动时需要输入明确的确认语句：

```bash
duola autopilot start <alias> --confirm-live "I UNDERSTAND LIVE TRADING" --detach
```

### 6) 操作与监控

```bash
duola autopilot status <alias> --output json
duola follow logs <alias> --tail 100 --output json
duola autopilot stop <alias> --output json
```

对于有限周期的验证过程，需要执行以下操作：

```bash
duola follow start <alias> --confirm-live "I UNDERSTAND LIVE TRADING" --max-cycles 5 --output json
```

## 报告机制

返回易于机器处理的汇总信息：
- `leader`：别名、地址
- `sync`：获取/插入/跳过的操作次数
- `backtest`：胜率、总盈亏（pnl）、最大回撤幅度、执行的交易信号
- `doctor`：检测到的错误及相应的修复措施
- `autopilot`：当前状态、分离状态（detach state）、心跳信号（heartbeat）、最近发生的错误

如果在实时启动过程中遇到问题，请详细报告具体的失败原因以及下一步应执行的命令。