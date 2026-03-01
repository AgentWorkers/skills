---
name: lp-agent
description: 使用 Hummingbot API，在具有高度集中流动性的去中心化交易所（CLMM DEXs）上运行自动化的流动性提供策略。
metadata:
  author: hummingbot
commands:
  start:
    description: Onboarding wizard — check setup status and get started
  deploy-hummingbot-api:
    description: Deploy Hummingbot API trading infrastructure
  setup-gateway:
    description: Start Gateway and configure network RPC endpoints
  add-wallet:
    description: Add or import a Solana wallet for trading
  explore-pools:
    description: Find and explore Meteora DLMM pools
  select-strategy:
    description: Choose between LP Executor or Rebalancer Controller strategy
  run-strategy:
    description: Run, monitor, and manage LP strategies
  analyze-performance:
    description: Export data and visualize LP position performance
---
# lp-agent

此技能可帮助您使用 Hummingbot API 在集中流动性（CLMM）去中心化交易所（DEX）上运行自动化流动性提供策略。

**命令**（以 `/lp-agent <command>` 的形式运行）：

| 命令 | 描述 |
|---------|-------------|
| `start` | 入门向导 — 检查设置状态并开始使用 |
| `deploy-hummingbot-api` | 部署 Hummingbot API 交易基础设施 |
| `setup-gateway` | 启动网关，配置网络 RPC 端点 |
| `add-wallet` | 添加或导入 Solana 钱包 |
| `explore-pools` | 查找和探索 Meteora DLMM 池 |
| `select-strategy` | 选择 LP 执行器或再平衡控制器 |
| `run-strategy` | 运行、监控和管理 LP 策略 |
| `analyze-performance` | 可视化 LP 位置绩效 |

**是新用户吗？** 运行 `/lp-agent start` 以检查您的设置并获得指导。

**典型工作流程：** `start` → `deploy-hummingbot-api` → `setup-gateway` → `add-wallet` → `explore-pools` → `select-strategy` → `run-strategy` → `analyze-performance`