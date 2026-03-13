---
name: simmer-skill-builder
description: 根据自然语言策略描述，生成完整的、可安装的 OpenClaw 交易技能。适用于以下场景：当用户希望创建新的交易策略、构建交易机器人、自动化交易想法、将推文转化为交易策略，或请求“为我构建一个……的技能”时。生成的技能包包含完整的文件结构（SKILL.md 文件、Python 脚本以及配置文件），可直接安装并运行。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.1.0"
  displayName: Simmer Skill Builder
  difficulty: beginner
---# Simmer Skill Builder

该工具可以根据策略描述生成完整的、可运行的Simmer交易技能。

> 您正在构建一个通过Simmer SDK在预测市场中进行交易的OpenClaw技能。生成的技能将被安装到您的技能库中，并由您直接运行——它必须是一个能够立即使用的、完整的、自包含的文件夹。

## 工作流程

### 第1步：理解策略

询问您的团队成员他们的策略具体内容。他们可能会：
- 用简单的语言描述交易策略
- 粘贴关于该策略的推文或讨论帖子
- 提及外部数据源（如Synth、NOAA、Binance、RSS等）
- 说类似“为我构建一个购买天气市场数据的机器人”或“创建一个用于捕捉加密货币市场趋势的技能”这样的话

明确以下内容：
1. **信号来源**——是什么数据驱动决策？（外部API、市场价格、链上数据、时机等）
2. **入场逻辑**——何时买入？（价格阈值、信号背离、时间窗口等）
3. **出场逻辑**——何时卖出？（获利阈值、基于时间的条件、信号反转，或依赖自动风险监控器）
4. **市场选择**——选择哪些市场？（通过标签、关键词、类别或发现逻辑）
5. **头寸大小**——固定金额还是智能调整？每次交易的默认最大金额是多少？

### 第2步：加载参考资料

阅读以下文件以了解相关模板：
1. **`references/skill-template.md`**——标准的技能框架。逐字复制其中的模板代码块（配置系统、获取客户端、安全措施、执行交易、命令行参数等）。
2. **`references/simmer-api.md`**——Simmer SDK的API接口。包含所有可用的方法、字段名称和返回类型。

如果Simmer MCP服务器可用（资源地址为`simmer://docs/skill-reference`），建议优先参考该文档以获取最新的API文档。否则使用`references/simmer-api.md`。

以下是一些实际运行的技能示例：
- **`references/example-weather-trader.md`**——模式：使用外部API信号 + Simmer SDK进行交易
- **`references/example-mert-sniper.md`**——模式：仅使用Simmer API进行过滤和交易

### 第3步：获取外部API文档（如需）

如果策略使用了外部数据源：
- **Polymarket CLOB数据：** 如果Polymarket MCP服务器可用，请在其中搜索相关的端点（订单簿、价格、价差等信息）。如果不可用，主要的公共端点包括：
  - `GET https://clob.polymarket.com/book?token_id=<token_id>` — 订单簿
  - `GET https://clob.polymarket.com/midpoint?token_id=<token_id>` — 中间价
  - `GET https://clob.polymarket.com/prices-history?market=<token_id>&interval=1w&fidelity=60` — 价格历史数据
  - 从Simmer市场响应中获取`polymarket_token_id`。
- **其他API（如Synth、NOAA、Binance、RSS等）：** 请让团队成员提供相关的API文档，或者如果您有权限，可以自行从网上获取这些文档。

### 第4步：生成技能

在磁盘上创建一个完整的文件夹：

```
<skill-slug>/
├── SKILL.md          # AgentSkills-compliant metadata + documentation
├── clawhub.json      # ClawHub + automaton config
├── <script>.py       # Main trading script
└── scripts/
    └── status.py     # Portfolio viewer (copy from references)
```

#### SKILL.md 前言（遵循AgentSkills格式）

Simmer技能遵循[AgentSkills](https://agentskills.io)开放标准，因此可以与Claude Code、Cursor、Gemini CLI、VS Code以及其他兼容技能的代理程序配合使用。

```yaml
---
name: <skill-slug>
description: <What it does + when to trigger. Max 1024 chars.>
metadata:
  author: "<author>"
  version: "1.0.0"
  displayName: "<Human Readable Name>"
  difficulty: "intermediate"
---
```

规则：
- `name`必须使用小写字母，并且只能包含连字符，要与文件夹名相匹配
- `description`是必填项，最多1024个字符
- `metadata`的值必须是扁平字符串（符合AgentSkills规范）
- 在SKILL.md中不要包含`clawdbot`、`requires`、`tunables`或`automaton`等字段——这些信息应放在`clawhub.json`中
- 正文部分必须包含以下内容：“这是一个模板”的说明、设置流程、配置表、常用命令、示例输出以及故障排除部分

#### clawhub.json（ClawHub + Automaton配置）

```json
{
  "emoji": "<emoji>",
  "requires": {
    "env": ["SIMMER_API_KEY"],
    "pip": ["simmer-sdk"]
  },
  "cron": null,
  "autostart": false,
  "automaton": {
    "managed": true,
    "entrypoint": "<script>.py"
  }
}
```

- `requires.pip`中必须包含`simmer-sdk`——这是使技能自动出现在Simmer注册表中的关键依赖项
- `requires.env`必须包含`SIMMER_API_KEY`
- `automaton.entrypoint`必须指向主要的Python脚本
- **`tunables`——在这里声明所有可配置的环境变量，以便自动调整和在仪表板上显示这些变量。这些变量是配置范围和默认值的来源——`clawhub_sync`会自动将这些信息同步到技能注册表中。

示例可配置变量：
```json
{
  "tunables": [
    {"env": "MY_SKILL_THRESHOLD", "type": "number", "default": 0.15, "range": [0.01, 1.0], "step": 0.01, "label": "Entry threshold"},
    {"env": "MY_SKILL_LOCATIONS", "type": "string", "default": "NYC", "label": "Target cities (comma-separated)"},
    {"env": "MY_SKILL_ENABLED", "type": "boolean", "default": true, "label": "Feature toggle"}
  ]
}
```

支持的类型：`number`（带有`range`和`step`）、`string`、`boolean`。请确保默认值与Python脚本中的`CONFIG_SCHEMA`保持一致。

#### Python脚本要求

从`references/skill-template.md`中逐字复制以下内容：
- 配置系统（`from simmer_sdk.skill import load_config, update_config, get_config_path`）
- 单例函数`get_client()`
- `check_context_safeguards()`
- `execute_trade()`
- `calculate_position_size()`
- 命令行参数入口点（`--live`、`--positions`、`--config`、`--set`、`--smart-sizing`、`--no-safeguards`、`--quiet`）

自定义设置：
- `CONFIG_SCHEMA`——包含`SIMMER_<SKILLNAME>_<PARAM>`环境变量的技能特定参数
- `TRADE_SOURCE`——唯一的标签，例如`sdk:<skillname>`）
- `SKILL_SLUG`——必须与ClawHub的slug完全匹配（例如`"polymarket-weather-trader"`）
- 信号逻辑——根据团队成员提供的策略实现
- 市场获取/过滤逻辑——用于查找相关市场
- 主要策略函数——交易的核心循环

### 第5步：验证

使用验证工具对生成的技能进行测试：

```bash
python /path/to/simmer-skill-builder/scripts/validate_skill.py /path/to/generated-skill/
```

在交付给团队成员之前，务必修复所有测试失败的问题。

### 第6步：发布到ClawHub

验证通过后，将技能发布到ClawHub，以便它自动出现在Simmer注册表中：

```bash
npx clawhub@latest publish /path/to/generated-skill/ --slug <skill-slug> --version 1.0.0
```

发布后，Simmer的同步任务将在6小时内将其添加到[simmer.markets/skills](https://simmer.markets/skills)列表中。无需手动提交或审批——只需将`simmer-sdk`作为依赖项添加到发布过程中即可。

告知团队成员：
> ✅ 技能已成功发布到ClawHub，将在6小时内出现在`simmer.markets/skills`中。

有关完整的发布细节，请参阅[simmer.markets/skillregistry.md](https://simmer.markets/skillregistry.md)。

## 重要规则

1. **始终使用`SimmerClient`进行交易。** 切勿直接导入`py_clob_client`、`polymarket`或调用CLOB API来下达订单。Simmer负责处理钱包签名、安全检查和交易跟踪。
2. **始终启用模拟模式。** 实际交易时必须明确使用`--live`标志。
3. **始终为每笔交易添加标签`source=TRADE_SOURCE`和`skill Slug=SKILL_SLUG`。`SKILL Slug`必须与ClawHub的slug完全匹配——Simmer会使用它来统计每个技能的交易量。
4. **始终包含安全措施**——必须使用`check_context_safeguards()`函数，可以通过`--no-safeguards`选项跳过此步骤。
5. **在`execute_trade()`函数中记录交易理由**——这些理由会公开显示，并影响您的信誉。
6. **仅使用标准库（如`urllib`）进行HTTP请求。除非团队成员有特殊需求，否则不要添加`requests`、`httpx`或`aiohttp`作为依赖项。唯一的pip依赖项应该是`simmer-sdk`。
7. **Polymarket的最低要求：** 每笔订单至少5份份额，最小交易间隔为0.01美元。交易前请务必进行检查。
8. **务必添加`sys.stdout.reconfigure(line_buffering=True)`——这对于Cron任务、Docker和OpenClaw的运行是必需的。
9. `get_positions()`函数返回的数据类对象——使用时请使用`from dataclasses import asdict`进行转换。
10. **切勿在生成的代码中暴露API密钥。** 始终通过`get_client()`从`SIMMER_API_KEY`环境变量中获取API密钥。

## 命名规范

- 技能slug格式：`polymarket-<策略名称>`用于特定于Polymarket的技能，`simmer-<策略名称>`用于通用平台
- 交易来源标签：`sdk:<简称>`（例如`sdk:synthvol`、`sdk:rssniper`、`sdk:momentum`）——用于重新购买或冲突检测
- 技能slug必须与ClawHub的slug完全匹配（例如`SKILL_SLUG = "polymarket-synth-volatility"`）——用于统计交易量
- 环境变量：`SIMMER_<简称>_<参数>`（例如`SIMMER_SYNTHVOL_ENTRY`）
- 脚本名称：`<描述性名称>.py`（例如`synth_volatility.py`、`rss_sniper.py`）

## 示例：根据推文生成技能

如果团队成员发送了这样的推文：
> “构建一个使用Synth波动率预测来交易Polymarket加密货币每小时合约的机器人。当Synth预测概率比市场价格高出7%以上时买入，并根据Kelly公式确定交易量。”

您需要执行以下步骤：
1. 理解策略：信号来源是Synth API的预测概率与Polymarket的价格；入场条件是预测概率与市场价格的7%偏差；交易策略是使用Kelly公式；交易市场是加密货币每小时合约。
2. 阅读`references/skill-template.md`以获取技能的框架结构。
3. 阅读`references/simmer-api.md`以了解SDK的API方法。
4. 阅读`references/example-weather-trader.md`以获取类似的实现示例。
5. 向团队成员索取Synth API的文档，或者自行从网上获取。
6. 生成`polymarket-synth-volatility/`文件夹，其中包含：
   - `SKILL.md`（包含设置、配置表和命令）
   - `synth_volatility.py`（用于获取Synth预测结果、与市场价格比较并计算交易量）
   - `scripts/status.py`（用于存储状态信息）
7. 使用`scripts/validate_skill.py`进行验证。
8. 使用`npx clawhub@latest publish polymarket-synth-volatility/ --slug polymarket-synth-volatility --version 1.0.0`命令发布技能。