---
name: tbot-controller
version: 1.0.0
author: PlusGenie
tags: [openclaw, tbot, tradingboat, trading, docker, ibkr]
description: 通过受控的自动化接口来操作 TradingBoat/TBOT（TBOT 运行时栈）：首先执行数据库查询（DB-first queries），并在明确请求的情况下进行生命周期管理（lifecycle control）。
metadata: {"openclaw":{"emoji":"🛥️","requires":{"bins":["uv"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

## 该技能的功能
- 从 TBOT 的 SQLite 数据库中查询警报、订单、错误和交易组合信息（优先使用数据库查询）。
- 启动或停止 TradingBoat/TBOT 服务（通过 Docker Compose 或 systemd 管理）。
- 仅在明确请求时，才会获取容器的运行状态、端口信息以及进行基本检查。
- 仅在明确请求时，才会读取最近的日志记录。

## 安全规则
- 默认操作为 **只读**（查看状态和日志），除非用户明确要求执行控制操作。
- 对于任何会改变系统状态的操作（如启动、停止、重启或发送信号），必须通过标志 `--run-it` 或环境变量 `RUN_IT=1` 来获得明确确认；否则控制器将拒绝执行这些操作。
- 绝不允许输出任何敏感信息（如 webhook 密钥或令牌），请对这些信息进行加密处理。

## 必须停止执行的场景
如果出现以下任何情况，该技能必须立即停止并请求用户进行干预：
- 运行位置未知，且无法通过系统发现机制唯一确定其位置。
- 无法找到 TBOT 数据库路径，或者无法以只读模式打开该数据库。
- 请求中未包含 `--run-it` 或 `RUN_IT=1` 参数，却试图启动、停止或重启服务，或发送信号。
- 请求中包含可能破坏数据库内容的操作（如 `DROP`、`TRUNCATE`、`ALTER`），或尝试执行任意 SQL 语句。

## 先决条件（首次使用用户需了解）
该技能控制的是一个独立的 TBOT 运行时环境。参考实现的运行时框架为：**openclaw-on-tradingboat**（地址：https://github.com/PlusGenie/openclaw-on-tradingboat**。
该技能本身不会下载或安装运行时环境；如果运行时环境缺失，它将尽可能以只读模式访问数据库，但状态、日志查看和控制操作将无法执行，直到运行时环境被安装完毕。

### 安装运行时环境（建议操作）
1) 克隆运行时环境的仓库：
```bash
git clone https://github.com/PlusGenie/openclaw-on-tradingboat.git
cd openclaw-on-tradingboat
```

2) 确保你可以手动启动该运行时环境（不在该技能的范围内执行）。对于基于 Docker Compose 的安装，通常需要执行以下操作：
```bash
docker compose up -d
```

3) 告知该技能运行时环境的路径（建议操作）：
- 将 `TBOT_COMPOSE_DIR` 设置为包含 `docker-compose.yml` 或 `compose.yaml` 文件的文件夹路径。
示例：
```bash
export TBOT_COMPOSE_DIR="$HOME/develop/github/openclaw-on-tradingboat"
```

或者将该路径添加到 `~/.openclaw/.env` 文件中，或在 `openclaw.json` 文件的 `env` 配置块中进行设置。

### 配置运行时环境的敏感信息
- TBOT 通常使用 `.env` 文件来存储 broker 的凭证和 webhook 密钥。
- **切勿** 将这些敏感信息提交到 Git 仓库中。
- 如果你不确定运行时环境是处于 **测试模式** 还是 **生产模式**，在该技能执行任何交易或操作之前，必须先确认运行时环境的模式。

## 安装/脚本权限设置
该技能通过一个 bash 入口点脚本来执行，确保该脚本具有执行权限：
```bash
chmod +x scripts/tbot.sh
```

### Python 依赖项（OpenClaw 内置）
该技能使用 `uv` 工具在隔离环境中运行 Python 脚本，并自动从 `{baseDir}/scripts/requirements.txt` 文件中安装所需的依赖项。
在 macOS 上安装 `uv` 的命令如下：
```bash
brew install uv
```

**注意**：如果你要发布该技能，确保 `scripts/` 目录（包括 `requirements.txt` 文件）位于仓库的根目录下。

## 重要说明：优先使用数据库查询，状态/控制操作仅依赖系统发现机制
- 数据库查询不需要依赖系统发现机制；系统发现机制仅在需要获取状态、日志或执行控制操作时才需要使用。
- OpenClaw **严禁** 硬编码过时的路径（例如 `~/ib-gateway-docker`）。
- 始终优先使用系统发现机制的返回结果（通常指向 `openclaw-on-tradingboat`）。

## 命令说明
### 入口点（必须指定）
OpenClaw 必须通过以下方式调用该技能：
```bash
bash scripts/tbot.sh <mode> <args...>
```

有效的操作模式包括：
- `ctl`：用于控制 TBOT 服务的启动/停止（通过 Docker 或 systemd）。
- `json`：生成 JSON 格式的信号并发送到 TBOT 的 webhook（非交互式操作）。
- `status`：仅用于读取状态信息（包括系统发现结果）。

### 系统发现机制（仅用于状态/控制操作）
当用户请求“打开 TBOT”、“启动 TBOT”或“查看 TBOT 状态”等操作时，OpenClaw 应首先尝试使用系统发现机制：
```bash
bash scripts/tbot.sh status discover
```

**注意**：这个步骤是强制性的，因为运行时环境的路径可能会随时间变化（例如从 `ib-gateway-docker` 更改为 `openclaw-on-tradingboat`）。

**如果系统发现机制成功找到运行时环境，则通过设置环境变量来执行 `ctl` 命令：**
- **Docker 示例**：
```bash
MODE=docker COMPOSE_DIR="<compose_dir>" bash scripts/tbot.sh ctl status
```

**Compose 文件夹的示例结构**：
```text
~/develop/github/openclaw-on-tradingboat> 
```

**Systemd 示例**：
```bash
MODE=systemd SERVICE_NAME="<service_name>" SYSTEMD_USER="<0|1>" bash scripts/tbot.sh ctl status
```

**如果系统发现机制无法找到运行时环境，则需要询问用户一个具体的问题：**
- **Docker Compose**：`哪个文件夹包含了 `docker-compose.yml` 或 `compose.yaml` 文件？（通常这个文件夹就是 TBOT 的运行时环境。）
- **Systemd**：`服务的名称是什么？（以及该服务是否以 `--user` 参数启动？）

**注意事项**：
- 系统发现机制的操作必须保持 **只读** 性质，不允许启动或停止服务。
- 系统发现机制的返回结果将作为确定操作模式的依据。

### 为什么这很重要
如果 OpenClaw 跳过系统发现机制，可能会错误地判断 TBOT 服务处于关闭状态（实际上服务可能仍在运行）。

### 状态查询（仅限请求时执行）
```bash
bash scripts/tbot.sh ctl status
bash scripts/tbot.sh ctl logs --tail 200
```

**注意**：使用 tbot-runtime 时，Docker Compose 通常会启动三个容器：`ib-gateway-on-tradingboat`（gnzsnz/ib-gateway）、`redis-on-tradingboat` 和 `tbot-on-tradingboat`。
**内部操作示例**：
- **Docker**：`docker compose ps`、`docker compose logs --tail=200`
- **Systemd**：`systemctl --user status <service>`、`journalctl --user -u <service> -n 200`

### 控制操作（需要明确确认）
```bash
bash scripts/tbot.sh ctl start --run-it
bash scripts/tbot.sh ctl stop --run-it
bash scripts/tbot.sh ctl restart --run-it
```

**提示**：可以使用 `MODE=docker` 并将 `COMPOSE_DIR` 设置为 TBOT 的运行时环境路径来通过 Docker Compose 控制该服务。
**内部操作示例**：
- **Docker**：`docker compose up -d`、`docker compose down`
- **Systemd**：`systemctl --user start <service>`、`systemctl --user stop <service>`

### JSON 信号生成（非交互式操作）
- `json` 模式是 **设计上非交互式的**；如果可以从用户输入中推断出所需的 webhook 信息或交易意图，OpenClaw **禁止** 再额外询问用户。
- **默认设置**：
  - **Webhook URL**：`http://127.0.0.1:5001/webhook`（可自定义）
  - **Webhook 密钥**：从 TBOT 的 `.env` 文件中读取（可自定义）
  - **orderRef**：如果未提供，则自动生成（格式为 `Close_<TICKER>_<QTY>_<epoch_ms>`）
- **关闭操作**：会自动根据用户输入推断操作类型（例如 `Close`、`Close_all`），无需用户再次确认。

**保证**：
- 生成的 JSON 数据会经过 `alert_webhook_schema.json` 的格式验证。
- 如果输入的数据不符合格式要求，操作会立即失败。
- 该技能不会执行任何网络请求或 broker 相关的操作。
- 该技能的实现与 gateway 容器（如 `gnzsnz/ib-gateway`）无关。

#### JSON 输出格式要求
当用户请求生成 TradingView 格式的 webhook 数据时，OpenClaw 应输出符合以下格式的 JSON 数据：
```json
{
  "timestamp": 1710000000000,
  "ticker": "ES1!",
  "currency": "USD",
  "timeframe": "5",
  "clientId": 1,
  "key": "WebhookReceived:123456",
  "contract": "future",
  "orderRef": "Long#1",
  "direction": "strategy.entrylong",
  "exchange": "CME",
  "lastTradeDateOrContractMonth": "202603",
  "multiplier": "50",
  "metrics": [
    {"name": "entry.limit", "value": 0},
    {"name": "entry.stop", "value": 0},
    {"name": "exit.limit", "value": 0},
    {"name": "exit.stop", "value": 0},
    {"name": "qty", "value": 1},
    {"name": "price", "value": 5032.25}
  ]
}
```

**提示**：在文档中可以使用占位符 `key`；在实际使用时，请替换为你的真实共享密钥（TVWB 密钥）。

### 数据查询（仅限读取）
- **推荐使用该技能并通过数据库查询**：
  - `bash scripts/tbot.sh status db --table orders --format summary --limit 100`
  - `bash scripts/tbot.sh status db --table alerts --format summary --limit 100`
  - `bash scripts/tbot.sh status db --table errors --format summary --limit 100`
  - `bash scripts/tbot.sh status db --table tbot --format summary --limit 100`
  - 使用 `--format json` 可以获取原始 JSON 数据。
- 交易组合信息来自 `TBOTORDERS` 文件（与 UI 中的 `/orders/data` 相同）。

### 仅限读取的辅助操作（优先使用数据库查询）
- 获取交易组合快照：
  - `bash scripts/tbot.sh status portfolio --format summary`
- 查看错误日志（按类别分组）：
  - `bash scripts/tbot.sh status errors --format summary --limit 200`
  - `bash scripts/tbot.sh status errors --group --limit 200`
- 进行健康检查（使用 HTTP 请求）：
  - `bash scripts/tbot.sh status health --base-url http://127.0.0.1:5001`

**示例输出（格式为 `summary`）**：
```
Totals:
- Market value: 284,103.16
- Unrealized PnL: 134,585.15
- Realized PnL: 0.00

TBOT_TIME        | ORD_TIME                | TICKER | TV_Close | ACTION | TYPE | QTY | LIMIT | STOP | ORDERID | ORDERREF  | STATUS    | POS | MRKVAL     | AVGF     | UnrealPnL  | RealPnL
----------------+-------------------------+--------+----------+--------+------+-----+-------+------+---------+-----------+-----------+-----+------------+----------+------------+--------
2026-02-05 20:06 | 2026-02-05 20:06:12.345 | TSLA   | 399.4796 | BUY    | LMT  | 455 | 0     | 0    | 12345   | Ptf_TSLA  | Portfolio | 455 | 181,763.22 | 187.9038 | 96,266.98  | 0
```

**数据库路径设置**：
- `--db-path` 参数用于指定数据库路径（优先使用数据库查询）：
  - `--db-path /path/to/tbot_sqlite3`
  - `TBOT_DB_PATH=/path/to/tbot_sqlite3`
  - 如果未设置数据卷，TBOT 可能在容器内创建数据库 `/home/tbot/tbot_sqlite3`。
- **推荐设置**：将宿主机的 `/runtime/database` 目录挂载到容器内的 `/home/tbot/database`，并设置 `TBOT_DB_OFFICE=/home/tbot/database/tbot_sqlite3`。
- 挂载后的路径示例：`tbot-runtime (example)/runtime/database/tbot_sqlite3`
- 更新 `tbot-runtime (example)/docker-compose.yml` 后，重新启动 TBOT：
  - `MODE=docker COMPOSE_DIR="/path/to/your/tbot-runtime" bash scripts/tbot.sh ctl restart --run-it`
- **容器注意事项**：`tbot` 容器可能不包含 `sqlite3` 命令行工具；建议通过挂载从宿主机读取数据库数据。
- **备用方式（手动操作）**：`sqlite3 <path> "SELECT ..."` 

### 已知的问题及改进计划
- 系统发现机制可能无法识别某些正在运行的 Docker Compose 环境；在这种情况下，建议优先使用数据库查询来获取交易组合信息。
- 计划添加额外的子命令，例如 `errors --tail`（用于查看错误日志）、`health`（用于检查 `/orders/data` 和 `/tbot/data` 文件的状态）。
- 计划添加一个简洁的总结功能，显示总交易量、前三大持仓以及最大亏损持仓。

## 数据信号：TradingView 格式的 webhook JSON 生成
该技能生成的 JSON 数据包含 TBOT/TradingBoat 需要的字段：
- `timestamp`（自纪元以来的毫秒数）
- `ticker`（例如 `AAPL`、`ES1!`）
- `currency`（例如 `USD`）
- `timeframe`（例如 `1`、`5`、`1D`）
- `clientId`（整数，表示 IBKR 客户 ID）
- `key`（TVWB 共享密钥）
- `contract`（例如 `stock`、`forex`、`crypto`、`future`）
- `orderRef`（字符串类型的订单标识符）
- `direction`（例如 `strategy.entrylong`、`strategy.entryshort` 等）
- `exchange`、`lastTradeDateOrContractMonth`、`multiplier`（主要用于期货交易）
- `metrics`（包含 `{name, value}` 的数组）

**示例 JSON 数据**（使用占位符 `key`）：
```json
{
  "timestamp": 1710000000000,
  "ticker": "ES1!",
  "currency": "USD",
  "timeframe": "5",
  "clientId": 1,
  "key": "WebhookReceived:123456",
  "contract": "future",
  "orderRef": "Long#1",
  "direction": "strategy.entrylong",
  "exchange": "CME",
  "lastTradeDateOrContractMonth": "202603",
  "multiplier": "50",
  "metrics": [
    {"name": "entry.limit", "value": 0},
    {"name": "entry.stop", "value": 0},
    {"name": "exit.limit", "value": 0},
    {"name": "exit.stop", "value": 0},
    {"name": "qty", "value": 1},
    {"name": "price", "value": 5032.25}
  ]
}
```