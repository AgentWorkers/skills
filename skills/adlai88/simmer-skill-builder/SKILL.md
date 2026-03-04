---
name: simmer-skill-builder
description: 根据自然语言策略描述生成完整的、可安装的 OpenClaw 交易技能。适用于以下场景：用户希望创建新的交易策略、构建交易机器人、自动化交易想法、将推文转化为交易策略，或提出“为我构建一个……的技能”之类的请求。生成的技能包包括 SKILL.md 文件、Python 脚本以及配置文件，可直接安装并运行。
metadata:
  author: Simmer (@simmer_markets)
  version: "1.0.5"
  displayName: Simmer Skill Builder
  difficulty: beginner
---# Simmer Skill Builder

该工具能够根据策略描述自动生成完整的、可运行的Simmer交易技能。

> 您正在开发一个通过Simmer SDK在预测市场进行交易的OpenClaw技能。生成的技能将被安装到您的技能库中，并由您直接运行——它必须是一个能够立即使用的、独立的文件夹。

## 工作流程

### 第一步：理解策略

询问您的团队成员他们的策略具体内容。他们可能会：
- 用通俗的语言描述交易策略
- 粘贴关于该策略的推文或讨论帖子
- 提及外部数据源（如Synth、NOAA、Binance、RSS等）
- 说类似“为我构建一个购买天气市场数据的机器人”或“创建一个用于捕捉加密货币趋势的技能”这样的话

明确以下内容：
1. **信号来源**——是什么数据驱动决策？（外部API、市场价格、链上数据、时机等）
2. **入场逻辑**——何时买入？（价格阈值、信号背离、时间窗口等）
3. **出场逻辑**——何时卖出？（获利阈值、基于时间的条件、信号反转，或依赖自动风险监控器）
4. **市场选择**——选择哪些市场？（通过标签、关键词、类别或发现逻辑）
5. **持仓规模**——固定金额还是智能调整？每次交易的默认最大金额是多少？

### 第二步：加载参考资料

阅读以下文件以了解相关模式：
1. **`references/skill-template.md`**——标准的技能框架。逐字复制其中的模板代码块（配置系统、获取客户端、安全措施、执行交易、命令行参数）。
2. **`references/simmer-api.md`**——Simmer SDK的API接口。包含所有可用的方法、字段名称和返回类型。

如果Simmer MCP服务器可用（资源地址为`simmer://docs/skill-reference`），建议优先参考该文档以获取最新的API信息。否则使用`references/simmer-api.md`。

以下是一些实际运行的技能示例：
- **`references/example-weather-trader.md`**——模式：使用外部API信号 + Simmer SDK进行交易
- **`references/example-mert-sniper.md`**——模式：仅使用Simmer API进行过滤和交易

### 第三步：获取外部API文档（如需）

如果策略使用了外部数据源：
- **Polymarket CLOB数据：** 如果Polymarket MCP服务器可用，请在其中搜索相关的端点（订单簿、价格、价差）。如果不可用，主要的公共端点包括：
  - `GET https://clob.polymarket.com/book?token_id=<token_id>` — 订单簿
  - `GET https://clob.polymarket.com/midpoint?token_id=<token_id>` — 中间价
  - `GET https://clob.polymarket.com/prices-history?market=<token_id>&interval=1w&fidelity=60` — 价格历史
  - 从Simmer市场响应中获取`polymarket_token_id`。
- **其他API（如Synth、NOAA、Binance、RSS等）：** 请您的团队成员提供相应的API文档，或者如果您有权限，可以自行通过网络获取这些文档。

### 第四步：生成技能

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

Simmer技能遵循[AgentSkills](https://agentskills.io)开放标准，因此可以与Claude Code、Cursor、Gemini CLI、VS Code以及其他兼容技能的代理程序兼容。

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
- `name`必须为小写，仅使用连字符，并与文件夹名称一致
- `description`是必填项，最多1024个字符
- `metadata`值必须是扁平字符串（符合AgentSkills规范）
- 在SKILL.md中不要包含`clawdbot`、`requires`、`tunables`或`automaton`等字段——这些信息应放在`clawhub.json`中
- 正文部分必须包括：“这是一个模板”的说明、设置流程、配置表、常用命令、示例输出以及故障排除部分

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

#### Python脚本要求

从`references/skill-template.md`中逐字复制以下内容：
- 配置系统（`from simmer_sdk.skill import load_config, update_config, get_config_path`）
- 单例函数`get_client()`
- `check_context_safeguards()`
- `execute_trade()`
- `calculate_position_size()`
- 命令行参数（`--live`、`--positions`、`--config`、`--set`、`--smart-sizing`、`--no-safeguards`、`--quiet`）

自定义内容：
- `CONFIG_SCHEMA`——包含特定于技能的参数，通过`SIMMER_<SKILLNAME>_<PARAM>`环境变量进行配置
- `TRADE_SOURCE`——唯一的标签，例如`sdk:<skillname>`
- `SKILL_SLUG`——必须与ClawHub的slug完全匹配（例如`"polymarket-weather-trader"`）
- 信号逻辑——根据团队成员提供的策略实现
- 市场获取/筛选逻辑——如何找到相关市场
- 核心交易逻辑——执行交易的循环

### 第五步：验证

使用验证工具对生成的技能进行测试：

```bash
python /path/to/simmer-skill-builder/scripts/validate_skill.py /path/to/generated-skill/
```

在交付给团队成员之前，修复所有测试失败的问题。

### 第六步：发布到ClawHub

验证通过后，将技能发布到ClawHub，使其自动出现在Simmer注册表中：

```bash
npx clawhub@latest publish /path/to/generated-skill/ --slug <skill-slug> --version 1.0.0
```

发布后，Simmer的同步任务将在6小时内将其添加到[simmer.markets/skills](https://simmer.markets/skills)页面。无需手动提交或审批——只需将`simmer-sdk`作为依赖项添加到ClawHub中即可。

告知您的团队成员：
> ✅ 技能已成功发布到ClawHub，将在6小时内出现在`simmer.markets/skills`页面上。

有关完整的发布细节，请参阅[simmer.markets/skillregistry.md](https://simmer.markets/skillregistry.md)。

## 重要规则

1. **始终使用`SimmerClient`进行交易。**切勿直接导入`py_clob_client`、`polymarket`或调用CLOB API来下达订单。Simmer负责处理钱包签名、安全保障和交易跟踪。
2. **始终默认使用模拟模式（dry-run）。**实际交易时必须明确使用`--live`标志。
3. **始终为每笔交易添加标签`source=TRADE_SOURCE`和`skill_slug`。`SKILL_SLUG`必须与ClawHub的slug完全匹配——Simmer使用它来统计每个技能的交易量。
4. **始终加入安全措施**——必须包含`check_context_safeguards()`函数，可以通过`--no-safeguards`选项跳过此步骤。
5. **在`execute_trade()`函数中记录交易理由**——这些理由会公开显示，并影响您的信誉。
6. **仅使用标准库（如`urllib`）进行HTTP请求。除非团队成员有特殊需求，否则不要添加`requests`、`httpx`或`aiohttp`作为依赖项。唯一的pip依赖项应为`simmer-sdk`。
7. **Polymarket的最低要求：**每次订单至少5份合约，最小tick价格为0.01美元。交易前务必进行检查。
8. **务必添加`sys.stdout.reconfigure(line_buffering=True)`——这对于cron/Docker/OpenClaw的兼容性是必需的。
9. `get_positions()`函数返回的数据类对象——必须使用`from dataclasses import asdict`进行转换。
10. **不要在生成的代码中暴露API密钥。**始终通过`get_client()`从`SIMMER_API_KEY`环境变量中获取API密钥。

## 命名规范

- 技能slug格式：`polymarket-<策略名称>`用于特定于Polymarket的技能，`simmer-<策略名称>`用于通用平台
- 交易来源标签：`sdk:<简称>`（例如`sdk:synthvol`、`sdk:rssniper`、`sdk:momentum`）——用于识别交易来源
- 技能slug必须与ClawHub的slug完全匹配（例如`SKILL_SLUG = "polymarket-synth-volatility"`）——用于统计交易量
- 环境变量：`SIMMER_<简称>_<参数>`（例如`SIMMER_SYNTHVOL_ENTRY`）
- 脚本名称：`<描述性名称>.py`（例如`synth_volatility.py`、`rss_sniper.py`）

## 示例：根据推文生成技能

如果团队成员发送了这样的推文：
> “构建一个使用Synth波动率预测在Polymarket上进行交易的机器人。当Synth预测的概率比市场价格高出7%以上时买入，并根据Kelly公式确定交易规模。”

您需要执行以下步骤：
1. 理解策略：信号来源为Synth API的预测概率与Polymarket的价格；入场条件为预测概率与市场价格的7%偏差；交易规模使用Kelly公式；交易市场为Polymarket的小时合约。
2. 阅读`references/skill-template.md`以获取技能框架。
3. 阅读`references/simmer-api.md`以了解SDK的接口方法。
4. 阅读`references/example-weather-trader.md`以了解类似的实现方式。
5. 向团队成员索取Synth API的文档，或自行通过网络获取这些文档。
6. 生成`polymarket-synth-volatility/`文件夹，包含以下文件：
   - `SKILL.md`（包含设置、配置表和命令）
   - `synth_volatility.py`（用于获取Synth预测、与市场价格比较并执行交易）
   - `scripts/status.py`（用于验证技能）
7. 使用`scripts/validate_skill.py`进行验证。
8. 使用`npx clawhub@latest publish polymarket-synth-volatility/ --slug polymarket-synth-volatility --version 1.0.0`命令发布技能。