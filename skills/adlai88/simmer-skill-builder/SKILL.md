---
name: simmer-skill-builder
displayName: Simmer Skill Builder
description: 根据自然语言策略描述生成完整的、可安装的 OpenClaw 交易技能。适用于以下场景：当用户希望创建新的交易策略、构建交易机器人、自动化交易想法、将推文转化为交易策略，或请求“为我构建一个……的技能”时。生成的技能包包含完整的文件结构（SKILL.md 文件、Python 脚本以及配置文件），可直接安装并运行。
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":false,"entrypoint":null}}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.2"
published: true
---
# Simmer 技能构建器

该工具能够根据策略描述生成完整的、可运行的 Simmer 交易技能。

> 您正在构建一个通过 Simmer SDK 在预测市场中进行交易的 OpenClaw 技能。生成的技能将安装到您的技能库中，并由您直接运行——它必须是一个完整、独立的文件夹，能够立即投入使用。

## 工作流程

### 第一步：理解策略

询问您的团队成员他们的策略具体内容。他们可能会：
- 用通俗的语言描述交易策略
- 粘贴关于该策略的推文或讨论帖
- 提及外部数据源（如 Synth、NOAA、Binance、RSS 等）
- 说类似“为我构建一个用于交易天气市场的数据机器人”或“创建一个用于捕捉加密货币市场动量的技能”

明确以下内容：
1. **信号来源**——是什么数据驱动决策？（外部 API、市场价格、链上数据、交易时机等）
2. **入场逻辑**——何时买入？（价格阈值、信号背离、交易窗口等）
3. **出场逻辑**——何时卖出？（获利阈值、基于时间的条件、信号反转，或依赖自动风险监控器）
4. **市场选择**——选择哪些市场？（通过标签、关键词、类别或发现逻辑）
5. **头寸大小**——固定金额还是智能调整？每次交易的默认最大金额是多少？

### 第二步：加载参考资料

阅读以下文件以了解相关模板和模式：
1. **`references/skill-template.md`**——标准的技能框架。逐字复制其中的模板代码块（配置系统、获取客户端、安全措施、执行交易、命令行参数等）。
2. **`references/simmer-api.md`**——Simmer SDK 的 API 接口文档。包含所有可用的方法、字段名称和返回类型。

如果 Simmer MCP 服务器可用（资源地址为 `simmer://docs/skill-reference`），建议优先参考该文档以获取最新的 API 文档；否则使用 `references/simmer-api.md`。

查看以下示例技能以了解实际实现方式：
- **`references/example-weather-trader.md`**——模式：使用外部 API 信号进行交易
- **`references/example-mert-sniper.md`**——模式：仅使用 Simmer SDK 进行过滤和交易

### 第三步：获取外部 API 文档（如需）

如果策略使用了外部数据源：
- **Polymarket CLOB 数据**：如果 Polymarket MCP 服务器可用，请在其中查找相关端点（订单簿、价格、价差等信息）。如果不可用，主要公共端点包括：
  - `GET https://clob.polymarket.com/book?token_id=<token_id>` — 订单簿
  - `GET https://clob.polymarket.com/midpoint?token_id=<token_id>` — 中间价
  - `GET https://clob.polymarket.com/prices-history?market=<token_id>&interval=1w&fidelity=60` — 价格历史数据
  - 从 Simmer 市场响应中获取 `polymarket_token_id`。
- **其他 API（如 Synth、NOAA、Binance、RSS 等）**：请让团队成员提供相关的 API 文档，或者如果您有权限，可以直接从网上获取这些文档。

### 第四步：生成技能

在磁盘上创建一个完整的文件夹：

```
<skill-slug>/
├── SKILL.md          # Metadata + documentation
├── <script>.py       # Main trading script
└── scripts/
    └── status.py     # Portfolio viewer (copy from references)
```

#### SKILL.md 的要求

- 使用 YAML 格式编写文件头，包含 `name`、`displayName`、`description`、`metadata`（包括自动执行入口点）、`version: "1.0.0"`、`published: true` 等信息
- `requires.pip` 文件中必须包含 `simmer-sdk` 的依赖
- `requires.env` 文件中必须包含 `SIMMER_API_KEY` 环境变量
- 文件正文中必须包含以下内容：
  - “这是一个模板”的说明
  - 设置流程
  - 配置信息表
  - 常用命令
  - 示例输出
  - 故障排除指南

#### Python 脚本的要求

逐字复制以下内容来自 `references/skill-template.md`：
- 配置系统相关函数（`_load_config`、`_get_config_path`、`_update_config`）
- 单例函数 `get_client()`
- `check_context_safeguards()` 安全检查函数
- `execute_trade()` 交易执行函数
- 命令行入口点及常用参数（`--live`、`--positions`、`--config`、`--set`、`--smart-sizing`、`--no-safeguards`、`--quiet`）

自定义部分：
- `CONFIG_SCHEMA`——包含特定于技能的参数，通过环境变量 `SIMMER_<SKILLNAME>_<PARAM>` 进行配置
- `TRADE_SOURCE`——唯一的标签，例如 `"sdk:<skillname>`
- 信号处理逻辑——根据团队成员提供的策略实现
- 市场数据获取/筛选逻辑——如何找到相关市场
- 主交易逻辑——核心循环部分

### 第五步：验证生成的技能

使用验证工具对生成的技能进行测试：

```bash
python /path/to/simmer-skill-builder/scripts/validate_skill.py /path/to/generated-skill/
```

在将技能交付给团队成员之前，务必修复所有测试失败的问题。

## 规则说明

1. **始终使用 `SimmerClient` 进行交易**。严禁直接导入 `py_clob_client`、`polymarket` 或调用 CLOB API 来下达交易指令。Simmer 负责处理钱包签名、安全机制和交易跟踪。
2. **始终以模拟模式运行**。实际交易必须明确使用 `--live` 标志。
3. **务必为每笔交易添加标签`source=TRADE_SOURCE`（例如 `"sdk:synth-volatility"`）。
4. **务必加入安全措施**——必须使用 `check_context_safeguards()` 函数，可以通过 `--no-safeguards` 参数跳过此步骤。
5. **在 `execute_trade()` 函数中记录交易逻辑**——这些逻辑会被公开显示，并影响您的信誉。
6. **仅使用标准库（如 ` urllib`）进行 HTTP 请求**。除非团队成员有特殊需求，否则不要添加 `requests`、`httpx` 或 `aiohttp` 作为依赖项。唯一的 pip 依赖项应为 `simmer-sdk`。
7. **Polymarket 的最低要求**：每次交易至少 5 份合约，最小价格变动为 0.01 美元。交易前必须进行确认。
8. **必须添加 `sys.stdout.reconfigure(line_buffering=True)`——这是为了在 cron、Docker 或 OpenClaw 环境中正确显示输出。
9. `get_positions()` 函数返回的数据类对象必须使用 `from dataclasses import asdict` 进行转换。
10. **切勿在生成的代码中暴露 API 密钥**。始终通过 `get_client()` 从 `SIMMER_API_KEY` 环境变量中获取 API 密钥。

## 命名规范

- 技能名称格式：`polymarket-<策略名称>`（针对 Polymarket 的特定策略），`simmer-<策略名称>`（适用于通用平台）
- 交易来源标签：`sdk:<简称>`（例如 `sdk:synthvol`、`sdk:rssniper`、`sdk:momentum`）
- 环境变量格式：`SIMMER_<简称>_<参数>`（例如 `SIMMER_SYNTHVOL_ENTRY`）
- 脚本文件名：`<描述性名称>.py`（例如 `synth_volatility.py`、`rss_sniper.py`）

## 示例：根据推文生成技能

假设团队成员发送了这样的推文：
> “构建一个机器人，利用 Synth 的波动率预测来交易 Polymarket 的小时合约。当 Synth 的预测概率比市场价格高出 7% 以上时买入，并使用 Kelly 定量策略进行交易。”

您需要执行以下步骤：
1. 理解策略逻辑：信号来源为 Synth API 的预测概率与 Polymarket 的市场价格；入场条件为预测概率与市场价格的 7% 差异；头寸调整使用 Kelly 定量策略；交易市场为 Polymarket 的小时合约。
2. 阅读 `references/skill-template.md` 以获取技能框架。
3. 阅读 `references/simmer-api.md` 以了解 SDK 的接口方法。
4. 阅读 `references/example-weather-trader.md` 以了解外部 API 信号的实现方式。
5. 向团队成员索取 Synth API 的文档，或直接从网上获取这些文档。
6. 生成一个名为 `polymarket-synth-volatility/` 的技能文件夹，其中包含：
  - `SKILL.md`（包含设置信息、配置表和命令）
  - `synth_volatility.py`（用于获取 Synth 的预测数据、与市场价格进行比较并执行交易）
  - `scripts/status.py`（用于显示交易状态）
7. 使用 `scripts/validate_skill.py` 对生成的技能进行验证。