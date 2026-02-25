---
name: simmer-skill-builder
displayName: Simmer Skill Builder
description: 根据自然语言策略描述，生成完整的、可安装的 OpenClaw 交易技能。适用于以下场景：当用户希望创建新的交易策略、构建交易机器人、自动化交易想法、将推文转化为交易策略，或请求“为我构建一个……的技能”时。生成的技能包将包含 SKILL.md 文件、Python 脚本以及配置文件，可直接安装并运行。
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":false,"entrypoint":null}}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.0"
published: true
---
# Simmer 技能构建器

根据策略描述生成可运行的 Simmer 交易技能。

> 您正在构建一个通过 Simmer SDK 在预测市场中进行交易的 OpenClaw 技能。生成的技能将被安装到您的技能库中，并由您自己运行——它必须是一个完整、自包含的文件夹，能够直接使用。

## 工作流程

### 第一步：理解策略

询问您的团队成员他们的策略具体内容。他们可能会：
- 用简单的语言描述交易策略
- 粘贴关于该策略的推文或讨论帖子
- 提及外部数据源（如 Synth、NOAA、Binance、RSS 等）
- 说类似“为我构建一个购买天气市场数据的机器人”或“创建一个用于捕捉加密货币市场趋势的技能”

直到您完全理解以下内容为止：
1. **信号来源**——是什么数据驱动决策？（外部 API、市场价格、链上数据、时机等）
2. **入场逻辑**——何时买入？（价格阈值、信号背离、时间窗口等）
3. **出场逻辑**——何时卖出？（获利阈值、基于时间的条件、信号反转，或依赖自动风险监控器）
4. **市场选择**——选择哪些市场？（通过标签、关键词、类别或发现逻辑）
5. **头寸大小**——固定金额还是智能调整？每次交易的默认最大金额是多少？

### 第二步：加载参考资料

阅读以下文件以了解相关模式：
1. **`references/skill-template.md`**——标准的技能框架。逐字复制其中的模板代码块（配置系统、获取客户端、安全措施、执行交易、命令行参数）。
2. **`references/simmer-api.md`**——Simmer SDK 的 API 接口说明。包含所有可用的方法、字段名称和返回类型。

如果 Simmer MCP 服务器可用（资源地址为 `simmer://docs/skill-reference`），建议优先阅读该文档以获取最新的 API 文档。否则使用 `references/simmer-api.md`。

有关实际可运行技能的示例，请阅读：
- **`references/example-weather-trader.md`**——模式：使用外部 API 信号进行交易
- **`references/example-mert-sniper.md`**——模式：仅使用 Simmer API 进行过滤和交易

### 第三步：获取外部 API 文档（如需）

如果策略使用了外部数据源：
- **Polymarket CLOB 数据：** 如果 Polymarket MCP 服务器可用，请在其中搜索相关端点（订单簿、价格、价差）。如果不可用，主要的公共端点包括：
  - `GET https://clob.polymarket.com/book?token_id=<token_id>` — 订单簿
  - `GET https://clob.polymarket.com/midpoint?token_id=<token_id>` — 中间价
  - `GET https://clob.polymarket.com/prices-history?market=<token_id>&interval=1w&fidelity=60` — 价格历史数据
  - 从 Simmer 市场响应中获取 `polymarket_token_id`。
- **其他 API（如 Synth、NOAA、Binance、RSS 等）：** 请让团队成员提供相关的 API 文档，或者如果您有权限，可以自行通过网络获取这些文档。

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

- 使用 YAML 格式编写前端内容，包括 `name`、`displayName`、`description`、`metadata`（包含自动执行入口点）、`version: "1.0.0"`、`published: true`
- `requires.pip` 文件中必须包含 `simmer-sdk`
- `requires.env` 文件中必须包含 `SIMMER_API_KEY`
- 正文部分必须包含以下内容：
  - “这是一个模板”的说明
  - 设置流程
  - 配置表
  - 常用命令
  - 示例输出
  - 故障排除部分

#### Python 脚本的要求

从 `references/skill-template.md` 中逐字复制以下代码：
- 配置系统相关函数（`_load_config`、`_get_config_path`、`_update_config`）
- 单例函数 `get_client()`
- `check_context_safeguards()`
- `execute_trade()`
- `calculate_position_size()`
- 命令行入口点及标准参数（`--live`、`--positions`、`--config`、`--set`、`--smart-sizing`、`--no-safeguards`、`--quiet`）

自定义部分：
- `CONFIG_SCHEMA`——包含特定于技能的参数，通过环境变量 `SIMMER_<SKILLNAME>_<PARAM>` 进行配置
- `TRADE_SOURCE`——唯一的标签，例如 `"sdk:<skillname>`）
- 信号逻辑——根据团队成员提供的策略实现
- 市场获取/过滤逻辑——如何找到相关市场
- 主要交易逻辑——核心循环

### 第五步：验证

使用验证工具对生成的技能进行测试：

```bash
python /path/to/simmer-skill-builder/scripts/validate_skill.py /path/to/generated-skill/
```

在将技能交付给团队成员之前，务必修复所有测试失败的问题。

## 重要规则

1. **始终使用 `SimmerClient` 进行交易。** 绝不要直接导入 `py_clob_client`、`polymarket` 或调用 CLOB API 来下达订单。Simmer 负责处理钱包签名、安全措施和交易跟踪。
2. **始终默认为模拟交易模式。** 实际交易必须明确使用 `--live` 标志。
3. **始终为交易添加标签 `source=TRADE_SOURCE`（例如 `"sdk:synth-volatility"`）。
4. **始终包含安全措施**——必须使用 `check_context_safeguards()` 函数，可以通过 `--no-safeguards` 参数跳过此步骤。
5. **在 `execute_trade()` 中必须包含交易逻辑的说明**——这部分内容会公开显示，并影响您的信誉。
6. **仅使用标准库（如 urllib）进行 HTTP 请求**。除非团队成员有特殊需求，否则不要添加 `requests`、`httpx` 或 `aiohttp` 作为依赖项。唯一的 pip 依赖项应该是 `simmer-sdk`。
7. **Polymarket 的最低要求：** 每笔订单至少 5 份份额，最小交易间隔为 0.01 美元。交易前必须进行检查。
8. **必须包含 `sys.stdout.reconfigure(line_buffering=True)`——这对于 cron、Docker 或 OpenClaw 的正常运行是必需的。
9. `get_positions()` 函数返回的数据类对象——必须使用 `from dataclasses import asdict` 进行转换。
10. **不要在生成的代码中暴露 API 密钥**。始终通过 `get_client()` 从环境变量 `SIMMER_API_KEY` 中读取 API 密钥。

## 命名规范

- 技能名称格式：`polymarket-<策略名称>`（针对 Polymarket 的策略），`simmer-<策略名称>`（适用于跨平台的策略）
- 交易来源标签：`sdk:<简称>`（例如 `sdk:synthvol`、`sdk:rssniper`、`sdk:momentum`）
- 环境变量格式：`SIMMER_<简称>_<参数>`（例如 `SIMMER_SYNTHVOL_ENTRY`）
- 脚本文件名：`<描述性名称>.py`（例如 `synth_volatility.py`、`rss_sniper.py`）

## 示例：根据推文生成技能

如果团队成员发送了这样的推文：
> “构建一个机器人，使用 Synth 的波动率预测来交易 Polymarket 的小时合约。当 Synth 的预测概率比市场价格高出 7% 以上时买入，并根据 Kelly 公式确定交易规模。”

您需要：
1. 理解：信号来源是 Synth API 的预测概率与 Polymarket 的市场价格；入场条件是预测概率与市场价格的偏差达到 7%；头寸大小使用 Kelly 公式；交易市场是 Polymarket 的小时合约。
2. 阅读 `references/skill-template.md` 以获取技能框架。
3. 阅读 `references/simmer-api.md` 以了解 SDK 的方法。
4. 阅读 `references/example-weather-trader.md` 以了解相关示例。
5. 向团队成员索取 Synth API 的文档，或自行通过网络获取这些文档。
6. 生成一个名为 `polymarket-synth-volatility/` 的技能文件夹，其中包含：
  - `SKILL.md`（包含设置、配置信息和命令）
  - `synth_volatility.py`（用于获取 Synth 的预测数据、与市场价格进行比较并计算交易规模）
  - `scripts/status.py`（用于显示状态）
7. 使用 `scripts/validate_skill.py` 对生成的技能进行验证。