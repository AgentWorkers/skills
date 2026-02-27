---
name: aicash-miner
description: >
  **AICash Network自动挖矿工具（用于Base L2平台上的$CASH代币）**  
  适用于在AICash内存池网络中设置自动化计算证明（Proof of Compute）挖矿任务。支持多实例挖矿、systemd服务管理以及实时统计数据跟踪功能。
---
# AICash Miner

这是一个用于AI CASH MEMPOOL网络（aicash.network）的自动化挖矿代理。

## 快速入门

1. 从https://aicash.network获取API凭据（在浏览器中生成soul.md文件）。
2. 运行设置脚本：

```bash
scripts/setup.sh --api-key <KEY> --wallet <WALLET> --endpoint <ENDPOINT>
```

该脚本会创建挖矿程序、systemd服务，并启动挖矿过程。

## 配置

**必填参数：**
- `--api-key` — 来自aicash.network的API密钥（格式：`cash_xxx`）
- `--wallet` — 用于接收奖励的EVM钱包地址
- `--endpoint` — Supabase挖矿端点的URL

**可选参数：**
- `--name <name>` — 服务名称（默认：`aicash-miner`）
- `--instances <n>` — 并行挖矿实例的数量（默认：1）

## 多实例挖矿

运行多个挖矿实例以提高区块捕获率：

```bash
scripts/setup.sh --api-key <KEY> --wallet <WALLET> --endpoint <ENDPOINT> --instances 6
```

该脚本会创建6个独立的systemd服务：`aicash-miner`、`aicash-miner-2`至`aicash-miner-6`。

## 管理

```bash
# Check status
scripts/status.sh

# Stop all miners
scripts/stop.sh

# Start all miners
scripts/start.sh

# Update API credentials
scripts/setup.sh --api-key <NEW_KEY> --wallet <WALLET> --endpoint <NEW_ENDPOINT>
```

## 工作原理

1. 向API发送带有无效区块编号的请求以获取当前区块信息。
2. 为当前区块提交计算证明（Proof of Compute）。
3. 从API响应中获取实际奖励金额。
4. 在遇到错误时自动重试；跳过已被领取的区块。
5. 通过systemd服务实现24/7不间断运行，并具备自动重启功能。