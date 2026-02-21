---
name: clawback
description: >
  **功能说明：**  
  该工具能够实时镜像国会的股票交易数据，并通过自动化 broker 执行系统进行交易操作，同时具备风险管理功能。适用于需要根据众议院书记员（House Clerk）和参议院电子文件数据库（eFD）发布的公开信息来跟踪市场动态并自动执行交易的用户。  
  **主要特点：**  
  1. **实时数据同步**：自动从国会相关数据源获取最新的股票交易信息。  
  2. **自动化交易执行**：基于获取的数据，通过预设的策略或算法自动执行交易指令。  
  3. **风险管理**：内置风险控制机制，确保交易行为符合预设的风险管理规则。  
  4. **高度定制性**：用户可以根据自身需求配置交易策略和风险参数。  
  5. **数据可视化**：提供直观的数据可视化界面，便于用户监控交易情况和市场趋势。  
  **适用场景：**  
  - **市场分析师**：用于分析国会决策对股市的影响并据此制定交易策略。  
  - **量化交易系统**：集成到量化交易系统中，实现自动化交易策略的部署。  
  - **合规监控**：确保交易行为符合相关法律法规和监管要求。  
  **使用建议：**  
  - **数据源验证**：在使用前，请确认数据来源的准确性和可靠性。  
  - **策略测试**：在正式交易前，先在模拟环境中测试交易策略的有效性。  
  - **风险监控**：定期审查和调整风险管理设置，确保交易安全。
version: 1.1.0
author: mainfraame
homepage: https://github.com/mainfraame/clawback
user-invocable: true
metadata: {"openclaw": {"emoji": "🦀", "requires": {"bins": ["python3", "pip"]}, "install": {"pip": "{baseDir}"}, "primaryEnv": "BROKER_API_KEY"}}
---
# ClawBack

**自动执行基于国会成员股票交易的策略**

## 代理指令

当用户调用 `/clawback` 时，根据参数执行相应的命令：

### 命令

当用户使用任何参数调用 `/clawback` 时，执行相应的命令：

| 命令 | 功能 |
|---------|--------|
| `/clawback setup` | 运行设置向导：执行 `{baseDir}/bin/clawback.py setup` |
| `/clawback status` | 检查系统状态：执行 `{baseDir}/bin/clawback.py status` |
| `/clawback run` | 启动交易机器人：执行 `{baseDir}/bin/clawback.py run` |
| `/clawback daemon` | 以后台服务模式运行：执行 `{baseDir}/bin/clawback.py daemon` |
| `/clawback test` | 测试通知功能：执行 `{baseDir}/bin/clawback.py test` |
| `/clawback`（无参数） | 显示帮助信息：执行 `{baseDir}/bin/clawback.py --help` |

### 如何执行命令

**选项 1：使用包装脚本（推荐）**
在执行 ClawBack 命令时，请始终：
1. 使用位于 `{baseDir}/bin/clawback.py` 的包装脚本。
2. 将命令作为参数传递（例如：`{baseDir}/bin/clawback.py status`）。
3. 捕获并显示输出结果给用户。

**选项 2：直接使用 Python 执行（如果包装脚本无法使用）**
如果包装脚本失败，您可以直接运行 ClawBack：
1. 进入技能目录：`cd {baseDir}`。
2. 激活虚拟环境：`source venv/bin/activate`。
3. 运行 CLI：`python -m clawback.cli [命令]`。
4. 捕获并显示输出结果。

**重要提示**：请始终检查 `{baseDir}/venv` 是否存在虚拟环境。如果不存在，可能需要先运行设置脚本。

### `/clawback setup` - 交互式设置流程

当用户运行 `/clawback setup` 时，请按照以下步骤操作：

**步骤 1：安装依赖项（如需要）**
检查 `{baseDir}/venv` 是否存在。如果不存在，请运行：
```bash
cd {baseDir} && python3 -m venv venv && source venv/bin/activate && pip install -e .
```

**步骤 2：请求 E*TRADE 凭据**
向用户询问以下信息：
1. **环境**：询问“您是想使用 **沙箱**（测试环境）还是 **生产环境**（真实资金环境）？”
   - 默认值：沙箱环境

2. **消费者密钥**：询问“请输入您的 E*TRADE 消费者密钥（来自 developer.etrade.com）：”
   - 必填项

3. **消费者秘密**：询问“请输入您的 E*TRADE 消费者秘密：”
   - 必填项

4. **账户 ID**：询问“请输入您的 E*TRADE 账户 ID（或留空，将在 OAuth 后获取）：”
   - 可选项 - 可以后获取

**步骤 3：保存配置**
使用提供的信息创建/更新 `~/.clawback/config.json` 文件：
```json
{
  "broker": {
    "adapter": "etrade",
    "environment": "<sandbox or production>",
    "credentials": {
      "apiKey": "<consumer_key>",
      "apiSecret": "<consumer_secret>"
    }
  },
  "trading": {
    "accountId": "<account_id>",
    "initialCapital": 50000,
    "tradeScalePercentage": 0.01,
    "maxPositionPercentage": 0.05,
    "dailyLossLimit": 0.02
  },
  "notifications": {
    "telegram": {
      "enabled": true,
      "useOpenClaw": true
    }
  },
  "congress": {
    "dataSource": "official",
    "pollIntervalHours": 24,
    "minimumTradeSize": 10000
  }
}
```

**步骤 4：确认设置**
告知用户：“配置已保存到 `~/.clawback/config.json`。运行 `/clawback status` 进行验证。”

### 获取 E*TRADE API 凭据

引导用户访问：https://developer.etrade.com
1. 创建开发者账户。
2. 先创建一个沙箱环境下的新应用程序（用于测试）。
3. 复制消费者密钥和消费者秘密。

### 配置文件位置
- 配置文件：`~/.clawback/config.json`
- 技能目录：`{baseDir}`

### 读取保存的配置

要检查用户是否已配置凭据，请读取 `~/.clawback/config.json`：
- 如果文件不存在或凭据为空 → 提示用户重新设置。
- 如果凭据存在 → 可以继续执行 `status` 或 `run` 命令。

CLI 会自动从 `~/.clawback/config.json` 中读取所有配置信息。

### 检查设置状态

在运行 `/clawback status` 或 `/clawback run` 之前，请验证：
1. `{baseDir}/venv` 是否存在（依赖项已安装）。
2. `~/.clawback/config.json` 是否存在，并且其中包含非空的 `broker.credentials.apiKey`。

如果缺少其中任何一个，请建议先运行 `/clawback setup`。

---

ClawBack 会跟踪国会成员（众议院和参议院）披露的股票交易，并在用户的 E*TRADE 经纪账户中执行相应的交易。该工具基于这样一个前提：由于信息优势，国会领导者的交易表现通常优于市场。

## 默认监控的政客

ClawBack 默认会监控以下政客（可配置）：

| 政客 | 所属议院 | 优先级 |
|------------|---------|----------|
| Nancy Pelosi | 众议院 | 1（最高优先级） |
| Dan Crenshaw | 众议院 | 2 |
| Tommy Tuberville | 参议院 | 2 |
| Marjorie Taylor Greene | 众议院 | 3 |

## 交易策略默认值

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------|
| 交易延迟 | 3 天 | 交易前等待披露时间 |
| 持有期限 | 30 天 | 交易头寸的持有时间 |
| 交易规模 | 5% | 每笔交易的最大分配比例 |
| 止损 | 8% | 每笔交易的止损幅度 |
| 投资组合回撤 | 15% | 投资组合的最大损失限度 |
| 披露检查时间 | 美东时间 10:00, 14:00, 18:00 | 每日检查时间 |

## 功能

- **实时跟踪披露信息**：来自官方众议院书记员和参议院的电子文件披露（eFD）。
- **自动执行交易**：通过 E*TRADE API（仅支持该经纪商）。
- **智能交易规模调整**：根据账户规模调整交易规模。
- **动态止损**：锁定利润，限制损失。
- **风险管理**：设置回撤限制，防止连续亏损。
- **Telegram 通知**：接收新交易和止损的提醒。
- **回测引擎**：使用历史数据测试交易策略。

## 性能（回测结果）

| 策略 | 胜率 | 收益率 | 夏普比率 |
|----------|----------|--------|--------|
| 3 天延迟，30 天持有 | 42.9% | +6.2% | 0.39 |
| 9 天延迟，90 天持有 | 57.1% | +4.7% | 0.22 |

根据 NBER 的研究，国会领导者的年均表现优于标准普尔 500 指数 47%。

## 通过 ClawHub 安装

```bash
# Install from ClawHub registry
clawhub install clawback

# Or install from local directory
clawhub install ./clawback
```

## 故障排除

### 常见问题

1. **技能无法执行**：如果在 OpenClaw 中 `/clawback` 无法工作：
   - 检查技能文件是否位于正确的位置：`{baseDir}/`。
   - 确认包装脚本是否可执行：`chmod +x {baseDir}/bin/clawback.py`。
   - 检查虚拟环境是否存在：`{baseDir}/venv/`。

2. **认证问题**：如果 E*TRADE 认证失败：
   - 运行认证工具：`python {baseDir}/scripts/auth_utility.py --auth`。
   - 运行 `{baseDir}/bin/clawback.py setup` 重新配置。
   - 检查 `~/.clawback/config.json` 中的凭据。
   - 确认 E*TRADE API 密钥有效。

3. **令牌过期**：如果令牌过期（有效期为 30 天）：
   - 运行：`python {baseDir}/scripts/auth_utility.py --refresh`。
   - 或者重新进行认证：`python {baseDir}/scripts/auth_utility.py --auth`。

4. **Python 导入错误**：如果出现 “ModuleNotFoundError”：
   - 确保虚拟环境已激活。
   - 在 `{baseDir}/` 中运行 `pip install -e .`。
   - 检查 Python 路径是否包含 `{baseDir}/src`。

### 调试模式

要调试技能的执行过程，可以添加 `DEBUG=1` 环境变量：
```bash
DEBUG=1 {baseDir}/bin/clawback.py status
```

这将显示有关执行过程的更多详细信息。

### 安装后的设置

通过 ClawHub 安装后，`install.sh` 脚本会自动执行以下操作：
1. **Python 环境设置**：创建虚拟环境。
2. **包安装**：通过 pip 安装 ClawBack。
3. **目录结构**：创建 logs/、data/、config/ 目录。
4. **设置提示**：询问是否要运行设置向导。

如果在安装过程中跳过了设置步骤，请手动运行它：
```bash
cd ~/.openclaw/skills/clawback
./setup.sh          # Interactive setup wizard
# or
clawback setup      # CLI-based setup
```

### 改进的设置功能

- **更好的输入处理**：支持交互式和非交互式模式。
- **输入验证**：验证 E*TRADE API 密钥的格式。
- **超时处理**：如果没有输入，自动使用默认值。
- **错误恢复**：如果 CLI 失败，可以手动进行设置。
- **配置检查**：检测现有配置并提供选项。

## 交互式设置向导

设置向导会引导您完成配置过程：

### 步骤 1：环境选择
- **沙箱**（推荐用于测试）：不进行真实交易，使用 E*TRADE 开发者沙箱环境。
- **生产环境**：使用真实资金进行交易。

### 步骤 2：E*TRADE API 凭据
- **消费者密钥**：从 E*TRADE 开发者门户获取。
- **消费者秘密**：从 E*TRADE 开发者门户获取。

### 步骤 3：认证
- 通过 E*TRADE 自动进行 OAuth 认证。
- 打开浏览器进行授权。
- 返回验证码。

### 步骤 4：账户选择
- 列出所有可用的 E*TRADE 账户。
- 选择要使用的账户。

### 步骤 5：Telegram 设置（可选）
- 通过 Telegram 机器人配置通知。
- 如果可用，使用 OpenClaw 内置的 Telegram 频道。

## 环境变量

设置完成后，凭据将存储在 `.env` 文件中：
```bash
# E*TRADE API (required)
BROKER_API_KEY=your_consumer_key_here
BROKER_API_SECRET=your_consumer_secret_here
BROKER_ACCOUNT_ID=your_account_id_here

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# FMP API (optional)
FMP_API_KEY=your_fmp_api_key_here
```

## 使用方法

```bash
# Use the installed CLI command
clawback run      # Start interactive trading mode
clawback daemon   # Run as background service
clawback status   # Check system status
clawback setup    # Re-run setup wizard
clawback test     # Test Telegram notifications
```

## 自动交易

`clawback daemon` 命令会持续运行：
- 在美东时间 10:00、14:00、18:00（文件通常发布的时刻）进行披露检查。
- 在美东时间上午 9:35（市场开盘后 5 分钟）执行交易。
- 每 90 分钟刷新令牌（保持 E*TRADE 会话活跃）。
- 遵循市场交易时间（美东时间上午 9:30 - 下午 4:00）。

## 数据来源

- **众议院书记员**：https://disclosures-clerk.house.gov（PDF 文件解析）
- **参议院电子文件披露**：https://efdsearch.senate.gov（网页抓取）
- **财务建模数据**：可选的增强型财务数据。

## 支持的经纪商

ClawBack 目前仅支持 E*TRADE。虽然支持其他经纪商的适配器模式，但目前仅实现了 E*TRADE 的支持并进行测试。

| 经纪商 | 适配器 | 状态 |
|--------|---------|--------|
| E*TRADE | `etrade_adapter.py` | 已支持 |

## 风险管理

- **每只股票的最大持仓比例**：5%。
- **止损**：每笔交易 8%，投资组合最大回撤 15%。
- **每日限制**：每日最大损失 3%。
- **PDT 合规性**：每日最多 2 笔交易。

## 认证辅助工具

对于在主 CLI 之外进行手动 E*TRADE 认证的情况：
```bash
# Standalone OAuth authentication script
cd {baseDir}
source venv/bin/activate
python scripts/auth_script.py
```

该工具会生成授权 URL，提示用户输入验证码，并完成认证过程。

## 文件位置

| 文件 | 用途 |
|------|---------|
| `~/.clawback/config.json` | 主配置文件 |
| `~/.clawback/.access_tokens.json` | E*TRADE OAuth 令牌 |
| `~/.clawback/data/trading.db` | SQLite 数据库 |

## 安全性

- 源代码中不包含硬编码的凭据。
- 配置信息基于环境变量。
- E*TRADE 令牌存储采用加密方式。
- `.env` 文件被 Git 忽略（防止泄露）。
- 支持可选的生产环境加密。

## 支持

- **文档**：详细设置信息请参阅 README.md。
- **问题反馈**：https://github.com/mainfraame/clawback/issues。
- **社区**：https://discord.com/invite/clawd

## 免责声明

**交易存在重大损失风险。** 本软件仅用于教学目的。过去的国会交易表现不能保证未来的结果。在实际交易前，请务必使用 E*TRADE 沙箱账户进行测试。