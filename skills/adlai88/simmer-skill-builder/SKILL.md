---
name: simmer-skill-builder
displayName: Simmer Skill Builder
description: 根据自然语言策略描述生成完整的、可安装的 OpenClaw 交易技能。适用于以下场景：当用户希望创建新的交易策略、构建交易机器人、自动化交易想法、将推文转化为交易策略，或请求“为我生成一个……的技能”时。生成的技能文件包括 SKILL.md 文件、Python 脚本以及配置文件，可直接安装并运行。
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"env":["SIMMER_API_KEY"],"pip":["simmer-sdk"]},"cron":null,"autostart":false,"automaton":{"managed":false,"entrypoint":null}}}
authors:
  - Simmer (@simmer_markets)
version: "1.0.5"
difficulty: beginner
published: true
---
# Simmer Skill Builder

本工具可根据策略描述自动生成完整的、可运行的交易技能。

> 您正在开发一个通过 Simmer SDK 在预测市场中进行交易的 OpenClaw 技能。生成的技能将被安装到您的技能库中，并由您直接运行——它必须是一个可以立即使用的、独立完整的文件夹。

## 工作流程

### 第一步：理解策略

询问您的团队成员他们的策略具体内容。他们可能会：
- 用通俗的语言描述交易策略
- 粘贴关于该策略的推文或讨论帖子
- 提及外部数据源（如 Synth、NOAA、Binance、RSS 等）
- 说类似“为我构建一个用于交易天气市场的数据机器人”或“创建一个用于追踪加密货币动量的技能”

请明确以下内容：
1. **信号来源**：是什么数据驱动决策？（外部 API、市场价格、链上数据、时机等）
2. **入场逻辑**：何时买入？（价格阈值、信号背离、时间窗口等）
3. **出场逻辑**：何时卖出？（获利阈值、基于时间的条件、信号反转，或依赖自动风险监控器）
4. **市场选择**：选择哪些市场？（通过标签、关键词、类别或发现逻辑）
5. **头寸大小**：固定金额还是智能调整？每次交易的默认最大金额是多少？

### 第二步：加载参考资料

阅读以下文件以了解相关模板：
1. **`references/skill-template.md`**：标准的技能框架。请逐字复制其中的模板代码块（配置系统、获取客户端、安全措施、执行交易、命令行参数等）。
2. **`references/simmer-api.md`**：Simmer SDK 的 API 接口文档。包含所有可用的方法、字段名称和返回类型。

如果 Simmer MCP 服务器可用（资源地址为 `simmer://docs/skill-reference`），建议优先参考该文档以获取最新的 API 文档；否则使用 `references/simmer-api.md`。

以下是一些实际运行的技能示例：
- **`references/example-weather-trader.md`**：模式：使用外部 API 信号 + Simmer SDK 进行交易
- **`references/example-mert-sniper.md`**：模式：仅使用 Simmer API 进行过滤和交易

### 第三步：获取外部 API 文档（如需）

如果策略使用了外部数据源：
- **Polymarket CLOB 数据**：如果 Polymarket MCP 服务器可用，请在其中搜索相关端点（订单簿、价格、价差等信息）。如果不可用，主要的公共端点包括：
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

- 使用 YAML 格式编写文件头，包含 `name`、`displayName`、`description`、`metadata`（包括自动执行入口点）、`version: "1.0.0"`、`published: true` 等字段
- `requires.pip` 文件中必须包含 `simmer-sdk`
- `requires.env` 文件中必须包含 `SIMMER_API_KEY`
- 文件正文中必须包含以下内容：
  - “这是一个模板”的说明
  - 设置流程
  - 配置信息表
  - 常用命令
  - 示例输出
  - 故障排除指南

#### Python 脚本的要求

请逐字复制 `references/skill-template.md` 中的以下代码：
- 配置系统相关代码：`from simmer_sdk.skill import load_config, update_config, get_config_path`
- 单例函数 `get_client()`
- `check_context_safeguards()`
- `execute_trade()`
- `calculate_position_size()`
- 命令行入口点及参数：`--live`、`--positions`、`--config`、`--set`、`--smart-sizing`、`--no-safeguards`、`--quiet`

自定义部分：
- `CONFIG_SCHEMA`：包含特定于技能的参数，通过环境变量 `SIMMER_<SKILLNAME>_<PARAM>` 进行配置
- `TRADE_SOURCE`：一个唯一的标签，例如 `"sdk:<skillname>`（用于标识数据来源）
- `SKILL_SLUG`：必须与 ClawHub 的名称完全匹配（例如 `"polymarket-weather-trader"`）
- 信号逻辑：根据团队成员提供的策略实现
- 市场获取/筛选逻辑：用于查找相关市场
- 主要交易逻辑：核心交易循环

### 第五步：验证生成的技能

使用验证工具对生成的技能进行测试：

```bash
python /path/to/simmer-skill-builder/scripts/validate_skill.py /path/to/generated-skill/
```

在将技能交付给团队成员之前，务必修复所有测试失败的问题。

### 第六步：发布到 ClawHub

验证通过后，将技能发布到 ClawHub，以便它自动显示在 Simmer 注册表中：

```bash
npx clawhub@latest publish /path/to/generated-skill/ --slug <skill-slug> --version 1.0.0
```

发布后，Simmer 的同步任务会在 6 小时内将其添加到 [simmer.markets/skills](https://simmer.markets/skills) 页面。无需手动提交或审批——只需将 `simmer-sdk` 作为依赖项即可完成发布。

告知团队成员：
> ✅ 技能已发布到 ClawHub，将在 6 小时内显示在 [simmer.markets/skills](https://simmer.markets/skills) 页面上。

有关完整的发布详情，请参阅 [simmer.markets/skillregistry.md](https://simmer.markets/skillregistry.md)。

## 重要规则

1. **始终使用 `SimmerClient` 进行交易**。切勿直接导入 `py_clob_client`、`polymarket` 或调用 CLOB API 来下达交易指令。Simmer 负责处理钱包签名、安全措施和交易跟踪。
2. **始终默认使用模拟交易模式**。实际交易时必须明确使用 `--live` 标志。
3. **始终为每笔交易添加标签 `source=TRADE_SOURCE` 和 `skill Slug`。`SKILL Slug` 必须与 ClawHub 的名称完全匹配——Simmer 会使用该标签来统计每个技能的交易量。
4. **始终添加安全措施**：必须使用 `check_context_safeguards()` 函数；可以通过 `--no-safeguards` 参数跳过此步骤。
5. **在 `execute-trade()` 函数中记录交易理由**——这些理由会公开显示，并影响您的信誉。
6. **仅使用标准库（如 urllib）进行 HTTP 请求**。除非团队成员有特殊需求，否则不要添加 `requests`、`httpx` 或 `aiohttp` 作为依赖项。唯一的 pip 依赖项应为 `simmer-sdk`。
7. **Polymarket 的最低要求**：每次交易至少 5 份合约，最小价格波动为 0.01 美元。交易前务必进行检查。
8. **务必添加 `sys.stdout.reconfigure(line_buffering=True)`——这对于 cron/Docker/OpenClaw 的正常运行是必需的。
9. `get_positions()` 函数返回的数据类对象必须使用 `from dataclasses import asdict` 进行转换。
10. **切勿在生成的代码中暴露 API 密钥**。始终通过 `get_client()` 从环境变量 `SIMMER_API_KEY` 中获取 API 密钥。

## 命名规范

- 技能名称格式：
  - 对于 Polymarket 特定的技能：`polymarket-<strategy>`
  - 通用平台的技能：`simmer-<strategy>`
- 交易来源标签：`sdk:<shortname>`（例如 `sdk:synthvol`、`sdk:rssniper`、`sdk:momentum`）——用于识别数据来源
- 技能名称必须与 ClawHub 的名称完全匹配（例如 `SKILL_SLUG = "polymarket-synth-volatility"`）
- 环境变量格式：`SIMMER_<SHORTNAME>_<PARAM>`（例如 `SIMMER_SYNTHVOL_ENTRY`）
- 脚本文件名：`<描述性名称>.py`（例如 `synth_volatility.py`、`rss_sniper.py`）

## 示例：根据推文生成技能

假设团队成员发送了这样的推文：
> “构建一个使用 Synth 波动率预测来交易 Polymarket 加密货币每小时合约的机器人。当 Synth 的预测概率比市场价格高出 7% 以上时买入，并根据 Kelly 公式确定交易规模。”

您需要执行以下步骤：
1. 理解策略：信号来源为 Synth API 的预测概率与 Polymarket 的市场价格；入场条件为预测概率与市场价格的 7% 差异；交易规模使用 Kelly 公式；交易市场为 Polymarket 的每小时合约。
2. 阅读 `references/skill-template.md` 以获取技能框架。
3. 阅读 `references/simmer-api.md` 以了解 SDK 的接口方法。
4. 阅读 `references/example-weather-trader.md` 以获取类似的实现示例。
5. 向团队成员索取 Synth API 的文档，或直接从网上获取。
6. 生成名为 `polymarket-synth-volatility/` 的技能文件，包含：
  - `SKILL.md`（包含设置信息、配置表和命令）
  - `synth_volatility.py`（用于获取 Synth 的预测数据、与市场价格进行比较并计算交易规模）
  - `scripts/status.py`（用于监控技能状态）
6. 使用 `scripts/validate_skill.py` 对技能进行验证。
7. 使用命令 `npx clawhub@latest publish polymarket-synth-volatility/ --slug polymarket-synth-volatility --version 1.0.0` 发布技能。