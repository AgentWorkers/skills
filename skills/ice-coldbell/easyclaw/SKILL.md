---
name: easyclaw-skill
description: 从一个独立的技能文件夹中运行面向用户的 EasyClaw DEX 操作。当代理需要提交用户订单或在 EasyClaw 中检查钱包/保证金/订单余额时，可以使用此方法，而无需依赖外部项目目录。
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/ice-coldbell/easyclaw/tree/main/easyclaw-skill
    requires:
      env:
        - SOLANA_RPC_URL
        - ANCHOR_PROVIDER_URL
        - KEYPAIR_PATH
        - ANCHOR_WALLET
        - EASYCLAW_API_BASE_URL
        - EASYCLAW_WS_URL
        - EASYCLAW_API_TOKEN
        - ORDER_ENGINE_PROGRAM_ID
        - MARKET_REGISTRY_PROGRAM_ID
        - API_BASE_URL
        - BACKEND_WS_URL
        - WS_URL
        - API_AUTH_TOKEN
        - API_TOKEN
      bins:
        - node
        - npm
      config:
        - ~/.config/solana/id.json
    primaryEnv: KEYPAIR_PATH
---
# EasyClaw 用户技能（User Skill）

仅执行用户相关的工作流程：

- 账户余额查询与订单状态检查
- 订单提交
- 后端查询（包括持仓、订单、成交记录、订单簿、图表等信息）
- 经过身份验证的代理/策略控制功能以及安全保护机制
- 实时WebSocket监控与基于信号的自动订单执行

请勿在此技能中执行管理员/启动/维护相关的工作流程。

## 运行时与凭证要求

- 钱包签名器来源：`KEYPAIR_PATH` 或 `ANCHOR_WALLET`（默认为 `~/.config/solana/id.json`）
- Solana RPC 服务来源：`SOLANA_RPC_URL` 或 `ANCHOR_PROVIDER_URL`（默认为 `http://127.0.0.1:8899`）
- 后端接口地址：`EASYCLAW_API_BASE_URL` 或 `EASYCLAW_WS_URL`（或在 `backend-common.js` 中配置的别名）
- 可选 API 凭证：`EASYCLAW_API_TOKEN`（用于访问受保护的后端功能）
- 本地进程使用：通过 `solana config get` 命令进行初始化配置，并可生成子 Node.js 进程以执行自动交易
- 本地文件操作：
  - 初始化过程会将选定的钱包环境变量保存到 `easyclaw-skill/.env` 文件中
  - 策略配置相关文件会保存到 `easyclaw-skill/state/strategies/` 目录下

## 命令接口

使用 `{baseDir}/scripts/dex-agent.sh` 命令来执行相关操作：

```bash
# toolchain + environment diagnostics
{baseDir}/scripts/dex-agent.sh doctor

# install local skill dependencies
{baseDir}/scripts/dex-agent.sh install

# wallet, USDC, margin, and open orders
{baseDir}/scripts/dex-agent.sh balance
{baseDir}/scripts/dex-agent.sh balance --json

# submit order tx
{baseDir}/scripts/dex-agent.sh order --market-id 1 --side buy --type market --margin 1000000
{baseDir}/scripts/dex-agent.sh order --market-id 2 --side sell --type limit --margin 2000000 --price 3000000000

# backend REST queries
{baseDir}/scripts/dex-agent.sh backend positions --mine --limit 20
{baseDir}/scripts/dex-agent.sh backend position-history --mine --limit 20
{baseDir}/scripts/dex-agent.sh backend chart-candles --market BTCUSDT --timeframe 1m --limit 120
{baseDir}/scripts/dex-agent.sh backend orderbook-heatmap --exchange binance --symbol BTCUSDT --limit 30
{baseDir}/scripts/dex-agent.sh backend portfolio --period 7d
{baseDir}/scripts/dex-agent.sh backend strategy-templates
{baseDir}/scripts/dex-agent.sh backend agent-risk --agent-id agent-001

# realtime WS monitor
{baseDir}/scripts/dex-agent.sh watch --channels "agent.signals,portfolio.updates,market.price.BTCUSDT"

# realtime signal -> auto order execution
{baseDir}/scripts/dex-agent.sh autotrade --market-id 1 --margin 1000000 --min-confidence 0.75

# guided onboarding + strategy capture + autotrade start
{baseDir}/scripts/dex-agent.sh onboard --market-id 1 --margin 1000000
```

## 相关文件

- `scripts/balance.js`：用户账户余额及订单概览功能
- `scripts/order-execute.js`：用户订单提交辅助工具
- `scripts/backend.js`：后端 REST API 查询辅助工具
- `scripts/ws-watch.js`：后端 WebSocket 监听器
- `scripts/realtime-agent.js`：基于信号的自动订单执行逻辑
- `scripts/onboard.js`：交互式初始化流程（包括钱包选择、注册等待、策略配置及自动交易启动）
- `scripts/background-common.js`：后端接口认证辅助功能
- `scripts/common.js`：通用工具（用于处理 PDA 数据、签名操作、交易处理及数据解码）
- `package.json`：项目所需的本地运行时依赖库
- `.env.example`：示例环境配置文件

## 设置步骤

1. 将 `.env.example` 复制到 `.env` 文件中。
2. 设置正确的签名器地址和 RPC 服务地址。
3. 运行 `dex-agent.sh install` 命令进行安装。
4. 先运行 `dex-agent.sh balance` 命令以验证访问权限。
5. 运行 `dex-agent.sh backend doctor` 和 `dex-agent.sh watch --channel system.status` 命令进行后台检查。
6. 使用 `dex-agent.sh onboard --market-id <id> --margin <u64>` 命令进行初始化配置（需指定市场 ID 和保证金值）。

有关环境变量定义及选项详情，请参阅 [references/dex-env.md](references/dex-env.md)。

## 安全注意事项

- 请将 `KEYPAIR_PATH` 及私钥保存在本地。
- 除非另有说明，否则请使用开发网络（devnet）或本地网络（localnet）进行操作。
- 在提交订单前，请确认 `ORDER_engine PROGRAM_ID` 和 `MARKET_REGISTRY PROGRAM_ID` 的正确性。