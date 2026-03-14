---
name: axon-agent
description: Register and operate an AI Agent on the Axon blockchain (AI Agent Native L1, Cosmos SDK + EVM, Chain ID 9001). Use when a user wants to: (1) register an agent on Axon chain, (2) check agent on-chain status (isAgent, ONLINE, reputation), (3) set up the agent-daemon for heartbeat maintenance, (4) troubleshoot Axon agent registration or heartbeat failures. Do NOT use for general EVM/Solidity work unrelated to Axon.
---

# Axon Agent 技能

Axon 是一个基于 AI 的原生 L1 区块链。这里的“Agent”指的是一个 EVM 地址，它需要使用 100 个 AXON 代币来调用 `register()` 函数，并定期发送心跳信号以保持在线状态。

**官方仓库：** https://github.com/axon-chain/axon  
**区块链参数：** RPC：`https://mainnet-rpc.axonchain.ai/` | 区块链 ID：`9001` | 每 5 秒生成一个新区块 | 注册表地址：`0x0000000000000000000000000000000000000901`

**重要提示：** 官方的 Python SDK 存在一个 ABI（应用程序接口）错误，请务必使用 `scripts/register.py` 脚本进行注册。详情请参阅 `references/known-issues.md`。

---

## 先决条件

- 需要安装 Python 3.8 及更高版本和 Go 1.21 及更高版本的服务器。
- EVM 钱包的私钥需保存为文件（例如：`/opt/axon/private_key.txt`，并设置权限为 600）。
- 账户余额至少需要 120 个 AXON 代币（包括 100 个代币用于注册、20 个代币用于燃烧以及额外的 gas 费用）。
- 需要安装 `web3` Python 包：`pip install web3`。

---

## 第 1 阶段：检查余额和状态

```bash
python3 scripts/check-status.py --private-key-file /opt/axon/private_key.txt
```

如果 `isAgent` 的值为 `True`，则直接进入第 3 阶段（设置守护进程）。

---

## 第 2 阶段：注册代理

```bash
# Dry run first
python3 scripts/register.py \
  --private-key-file /opt/axon/private_key.txt \
  --capabilities "nlp,reasoning,coding,research" \
  --model "claude-sonnet-4.6" \
  --dry-run

# Real registration
python3 scripts/register.py \
  --private-key-file /opt/axon/private_key.txt \
  --capabilities "nlp,reasoning,coding,research" \
  --model "claude-sonnet-4.6"
```

注册成功后，`isAgent` 的值将变为 `True`。请记录注册时使用的区块编号——首次发送心跳信号将在大约 720 个区块后（约 1 小时）进行。

**可使用的功能示例：** `nlp`（自然语言处理）、`reasoning`（推理）、`coding`（编码）、`research`（研究） | `trading`（交易）、`analysis`（分析） | `vision`（视觉处理）、`audio`（音频处理）  
**模型：** 使用实际运行的模型名称（例如：`claude-sonnet-4.6`、`glm-5`、`kimi-k2.5`）。

---

## 第 3 阶段：构建并启动守护进程

```bash
# Clone repo (if not already)
git clone https://github.com/axon-chain/axon /opt/axon
cd /opt/axon

# Build daemon
go build -o tools/agent-daemon/agent-daemon ./tools/agent-daemon/

# Start daemon
nohup /opt/axon/tools/agent-daemon/agent-daemon \
  --rpc https://mainnet-rpc.axonchain.ai/ \
  --private-key-file /opt/axon/private_key.txt \
  --heartbeat-interval 720 \
  --log-level info \
  >> /opt/axon/daemon.log 2>&1 &

echo "PID: $!"
```

查看日志文件：`tail -f /opt/axon/daemon.log`  
预期日志内容：每大约 720 个区块（约 1 小时）会显示一次“heartbeat confirmed”（心跳信号确认）。

---

## 第 4 阶段：配置定时任务（Cron 作业）

```bash
# Copy watchdog to your server (replace YOUR_SERVER and YOUR_KEY)
scp scripts/watchdog.sh user@YOUR_SERVER:/opt/axon/watchdog.sh
ssh user@YOUR_SERVER "chmod +x /opt/axon/watchdog.sh"

# Add cron (every 5 min)
ssh user@YOUR_SERVER "(crontab -l 2>/dev/null; echo '*/5 * * * * /opt/axon/watchdog.sh') | crontab -"
```

---

## 故障排除

有关常见问题的解决方法，请参阅 `references/known-issues.md`：
- SDK 与区块链 API 不匹配（最常见的故障原因）
- 首次发送心跳信号的时间延迟
- 官方仓库与分叉仓库之间的混淆
- 代币经济模型（20 个 AXON 代币会被永久燃烧）

**快速诊断方法：**
```bash
# Check daemon running
pgrep -f agent-daemon && echo "running" || echo "NOT running"

# Check on-chain status
python3 scripts/check-status.py --private-key-file /opt/axon/private_key.txt
```

---

## 多代理设置

每个代理都需要自己的 EVM 钱包、100 个 AXON 代币以及独立的守护进程。具体操作步骤相同，只需为每个代理运行不同的守护进程，并将日志文件重定向到不同的位置（例如：`daemon-cto.log`）。