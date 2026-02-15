---
name: agent-pulse
description: >
  Send and verify on-chain liveness pulses for autonomous agents on Base via the
  Agent Pulse protocol. Use when you need to: (1) prove an agent is alive by sending
  a pulse, (2) check any agent's liveness status or streak, (3) monitor multiple
  agents, (4) view the global pulse feed, (5) auto-configure wallet and PULSE balance,
  (6) run scheduled heartbeat pulses, or (7) read protocol health and config.
  Supports both API and direct on-chain (cast) modes.
requiredEnv:
  - PRIVATE_KEY
optionalEnv:
  - BASE_RPC_URL
  - API_BASE
  - PULSE_AMOUNT
  - TTL_THRESHOLD
  - PULSE_REGISTRY_ADDRESS
  - PULSE_TOKEN_ADDRESS
  - X402_PAYMENT_HEADER
  - X402_HEADER_NAME
requiredBins:
  - cast
  - curl
  - jq
---

# Agent Pulse 💓

这是用于管理Base链上自主代理的存活状态检测机制。代理会定期发送一个“脉冲”（PULSE代币转移）来证明自身的存活状态。观察者可以通过API或链上接口查询代理的状态。

**网络：** Base（链ID：8453）

| 合同        | 地址                                      |
|-----------------|----------------------------------------------|
| PulseToken      | `0x21111B39A502335aC7e45c4574Dd083A69258b07`  |
| PulseRegistry   | `0xe61C615743A02983A46aFF66Db035297e8a43846`  |
| API             | `https://x402pulse.xyz`         |

> **$PULSE** 是一种用于发送脉冲信号的实用代币。脉冲信号仅用于显示代理最近的交易活动，并不能证明代理的身份、质量或具备“AI”能力。请避免使用可能暗示财务收益的表述。

## 决策树

1. **首次使用？** → 运行 `scripts/setup.sh` 以自动检测钱包、检查余额并验证是否已获得注册许可。
2. **发送脉冲？** → 运行 `scripts/pulse.sh --direct 1000000000000000000`（需要 `PRIVATE_KEY`）。
3. **自动检测代理状态？** → 运行 `scripts/auto-pulse.sh`（支持定时任务；如果TTL值正常，则跳过检测）。
4. **检查单个代理的状态？** → 运行 `scripts/status.sh <地址>` 或 `curl .../api/v2/agent/<地址>/alive`。
5. **检查多个代理的状态？** → 运行 `scripts/monitor.sh <地址1> <地址2> ...`。
6. **查看脉冲信号流？** → 运行 `scripts/monitor.sh --feed`。
7. **查看协议配置/代理健康状况？** → 运行 `scripts/config.sh` 或 `scripts/health.sh`。

## 脚本参考

所有脚本均位于 `scripts/` 目录下。使用 `-h` 或 `--help` 可查看脚本的详细用法。

### setup.sh — 自动配置

使用 `PRIVATE_KEY` 自动检测钱包，检查PULSE代币余额，验证注册许可，并查询代理的状态。

```bash
# Interactive setup
{baseDir}/scripts/setup.sh

# Auto-approve registry + JSON output
{baseDir}/scripts/setup.sh --auto-approve --quiet
```

**环境变量：** `PRIVATE_KEY`（必需）、`BASE_RPC_URL`、`API_BASE`
**所需工具：** `cast`、`curl`、`jq`

### pulse.sh — 发送脉冲信号

通过 `cast send` 直接在链上发送脉冲信号。

```bash
export PRIVATE_KEY="0x..."
{baseDir}/scripts/pulse.sh --direct 1000000000000000000
```

**环境变量：** `PRIVATE_KEY`（必需）、`BASE_RPC_URL`
**所需工具：** `cast`

### auto-pulse.sh — 自动检测代理状态

定期检查代理的存活状态；仅在TTL值过低或代理处于“死亡”状态时发送脉冲信号。适合定时执行。

```bash
# Normal: pulse only if needed
{baseDir}/scripts/auto-pulse.sh

# Force pulse regardless of TTL
{baseDir}/scripts/auto-pulse.sh --force

# Check without sending
{baseDir}/scripts/auto-pulse.sh --dry-run
```

**环境变量：** `PRIVATE_KEY`（必需）、`BASE_RPC_URL`、`PULSE_AMOUNT`（默认值：1e18）、`TTL_THRESHOLD`（默认值：21600秒 = 6小时）
**退出代码：** 0 = 成功；1 = 出错

### status.sh — 代理状态查询

```bash
{baseDir}/scripts/status.sh 0xAgentAddress
```

### config.sh / health.sh — 协议信息查询

```bash
{baseDir}/scripts/config.sh     # addresses, network, x402 config
{baseDir}/scripts/health.sh     # paused status, total agents, health
```

### monitor.sh — 多代理监控工具

```bash
# Check specific agents
{baseDir}/scripts/monitor.sh 0xAddr1 0xAddr2 0xAddr3

# From file (one address per line)
{baseDir}/scripts/monitor.sh -f agents.txt

# JSON output
{baseDir}/scripts/monitor.sh --json 0xAddr1 0xAddr2

# Global pulse feed
{baseDir}/scripts/monitor.sh --feed
```

## API 快速参考

| API端点            | 方法        | 认证方式    | 描述                          |
|-------------------|-----------|-----------|----------------------------------------|
| `/api/v2/agent/{地址}/alive`    | GET       | 无         | 检查代理存活状态及TTL值                |
| `/api/status/{地址}`     | GET       | 无         | 获取代理的完整状态信息                |
| `/api/pulse-feed`      | GET       | 无         | 查看最近的脉冲信号活动                |
| `/api/config`       | GET       | 无         | 查看协议配置                    |
| `/api/protocol-health`    | GET       | 无         | 检查协议的运行状态及暂停状态              |
| `/api/pulse`      | POST       | x402认证    | 通过API发送脉冲信号                  |

## 直接在链上发送脉冲（使用 `cast`）

```bash
export BASE_RPC_URL="https://mainnet.base.org"

# Read: is agent alive?
cast call --rpc-url "$BASE_RPC_URL" \
  0xe61C615743A02983A46aFF66Db035297e8a43846 \
  "isAlive(address)(bool)" 0xAgent

# Read: full status tuple
cast call --rpc-url "$BASE_RPC_URL" \
  0xe61C615743A02983A46aFF66Db035297e8a43846 \
  "getAgentStatus(address)(bool,uint256,uint256,uint256)" 0xAgent

# Write: approve + pulse (requires PRIVATE_KEY)
cast send --rpc-url "$BASE_RPC_URL" --private-key "$PRIVATE_KEY" \
  0x21111B39A502335aC7e45c4574Dd083A69258b07 \
  "approve(address,uint256)(bool)" \
  0xe61C615743A02983A46aFF66Db035297e8a43846 1000000000000000000

cast send --rpc-url "$BASE_RPC_URL" --private-key "$PRIVATE_KEY" \
  0xe61C615743A02983A46aFF66Db035297e8a43846 \
  "pulse(uint256)" 1000000000000000000
```

## 错误处理

| 错误类型            | 原因                                      | 处理方法                          |
|-------------------------|------------------------------------------|--------------------------------------------|
| `BelowMinimumPulse`    | 发送的脉冲金额低于最小要求（默认值：1e18） | 确保发送的金额大于或等于100000000000000000             |
| ERC20转账失败        | 缺少批准或PULSE余额不足                | 运行 `setup.sh --auto-approve`                |
| `whenNotPaused`       | 注册服务处于暂停状态                          | 等待一段时间后再尝试；或检查 `health.sh`                |
| 401/402/403           | 需要支付的API接口未收到付款                | 使用直接在链上的发送方式                |
| 5xx                | API临时错误                        | 重试并设置延迟时间                    |

## 仅读模式（无需 `PRIVATE_KEY`）

以下命令无需 `PRIVATE_KEY` 即可执行——无需使用钱包或进行签名操作：

```bash
# Check any agent's status
{baseDir}/scripts/status.sh 0xAnyAgentAddress

# Monitor multiple agents
{baseDir}/scripts/monitor.sh 0xAddr1 0xAddr2

# View global pulse feed
{baseDir}/scripts/monitor.sh --feed

# Protocol configuration
{baseDir}/scripts/config.sh

# Protocol health
{baseDir}/scripts/health.sh
```

## 安全性注意事项

### 必需的凭证

| 环境变量          | 使用场景      | 默认值                         |
|-----------------|-------------|-----------------------------------------|
| `PRIVATE_KEY`       | 执行写入操作（发送脉冲、批准请求） | 无（仅限读取操作）                    |
| `BASE_RPC_URL`     | 所有链上请求       | `https://mainnet.base.org`                   |
| `API_BASE`      | API请求       | `https://x402pulse.xyz`                   |
| `PULSE_AMOUNT`     | 发送脉冲的代币数量    | `100000000000000000`                   |
| `TTL_THRESHOLD`    | 自动跳过检测的TTL阈值 | 21600秒（6小时）                     |
| `PULSE_REGISTRY_ADDRESS` | 重置注册表地址     | `0xe61C...`                       |
| `PULSE_TOKEN_ADDRESS` | 代币地址        | `0x2111...`                       |
| `X402_payment_HEADER` | API脉冲支付的头部信息   | 无（直接使用链上方式时无需设置）             |
| `X402_HEADER_NAME` | 自定义的X402请求头名称 | `X-402-Payment`                     |

### 审批机制

- `setup.sh --auto-approve` 会设置一个**上限为1,000个PULSE代币的发送额度**（并非无限）。这个额度足够发送大约1,000次脉冲信号后需要重新审批。
- `pulse.sh --direct` 会按每次交易的实际金额进行审批，不会超出预设的额度。
- `PulseRegistry` 合同只能在 `pulse()` 方法中调用 `transferFrom` 函数，不能随意消耗代币。

### 最佳实践

- **切勿** 将 `PRIVATE_KEY` 记录在日志中、打印出来或提交到代码库。
- 使用专门用于发送PULSE代币的钱包，切勿使用主钱包。
- 在执行实际交易前，先使用 `--dry-run` 模式进行测试。
- 在签署交易前，请务必核对合约地址和链ID。
- 先使用少量代币进行测试。

## 参考资料

- **操作指南：`references/action_guide.md` — 详细的API使用模式和示例。
- **合约ABI：`references/contract_abi.json` — PulseRegistry合约的完整ABI文档。