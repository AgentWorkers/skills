---
name: clawback
description: **功能说明：**  
该工具能够自动执行国会股票交易，并进行风险管理。适用于需要根据众议院书记员（House Clerk）和参议院电子文件数据库（eFD）发布的公开信息来跟踪市场动态并自动进行交易的情况。  

**主要特点：**  
1. **自动执行交易**：根据国会公开的数据，自动委托经纪机构执行股票交易。  
2. **实时风险管理**：实时监控交易过程中的风险，确保交易安全。  
3. **数据来源**：交易指令基于众议院书记员和参议院电子文件数据库（eFD）提供的官方数据。  

**适用场景：**  
- **市场分析师**：利用国会公开信息进行股票交易分析。  
- **量化投资策略**：开发基于国会数据的自动化交易策略。  
- **合规监控**：确保交易行为符合相关法规要求。  

**使用说明：**  
1. **数据获取**：从指定来源获取最新的国会股票交易数据。  
2. **策略制定**：根据数据制定交易策略。  
3. **自动执行**：将策略转化为交易指令，由经纪机构自动执行。  
4. **风险控制**：设置风险阈值，防止交易超出预设范围。  

**注意事项：**  
- 请确保使用的经纪机构支持自动化交易功能。  
- 该工具仅用于合法、合规的交易目的。  

**技术支持：**  
如需技术支持或咨询，请联系我们的技术团队。
version: 1.1.0
author: mainfraame
homepage: https://github.com/mainfraame/clawback
user-invocable: true
metadata: {"openclaw": {"emoji": "🦀", "requires": {"bins": ["python3", "pip"]}, "install": {"pip": "{baseDir}"}, "primaryEnv": "BROKER_API_KEY"}}
---

# ClawBack

**自动执行与国会成员股票交易相关的交易**

## 客户端指令

当用户调用 `/clawback` 时，根据参数执行相应的命令：

### 命令

| 命令 | 功能 |
|---------|--------|
| `/clawback setup` | 交互式设置 - 提示输入凭据（见下文） |
| `/clawback status` | 检查状态：`cd {baseDir} && source venv/bin/activate && python -m clawback.cli status` |
| `/clawback run` | 开始交易：`cd {baseDir} && source venv/bin/activate && python -m clawback.cli run` |
| `/clawback` | 默认为状态检查 |

### `/clawback setup` - 交互式设置流程

当用户运行 `/clawback setup` 时，请按照以下步骤操作：

**步骤 1：安装依赖项（如需要）**
检查 `{baseDir}/venv` 是否存在。如果不存在，请运行：
```bash
cd {baseDir} && python3 -m venv venv && source venv/bin/activate && pip install -e .
```

**步骤 2：提示输入 E*TRADE 凭据**
向用户询问以下信息：

1. **环境**：询问“您想使用 **沙箱**（测试环境）还是 **生产环境**（真实货币交易）？”
   - 默认值：沙箱环境

2. **消费者密钥**：询问“请输入您的 E*TRADE 消费者密钥（来自 developer.etrade.com）：”
   - 必填项

3. **消费者秘钥**：询问“请输入您的 E*TRADE 消费者秘钥：”
   - 必填项

4. **账户 ID**：询问“请输入您的 E*TRADE 账户 ID（或留空，通过 OAuth 获取）：”
   - 可选 - 可以稍后获取

**步骤 3：保存配置**
使用提供的信息创建或更新 `~/.clawback/config.json` 文件：
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
1. 创建一个开发者账户
2. 首先创建一个沙箱应用程序（用于测试）
3. 复制消费者密钥和消费者秘钥

### 配置文件位置

- 配置文件：`~/.clawback/config.json`
- 代码目录：`{baseDir}`

### 读取保存的配置

要检查用户是否已配置凭据，请读取 `~/.clawback/config.json`：
- 如果文件不存在或凭据为空 → 提示重新设置
- 如果凭据存在 → 可以继续执行状态检查或交易命令

CLI 会自动从 `~/.clawback/config.json` 中读取所有配置信息。

### 检查设置状态

在运行 `/clawback status` 或 `/clawback run` 之前，请验证：
1. `{baseDir}/venv` 是否存在（依赖项已安装）
2. `~/.clawback/config.json` 是否存在，并且包含非空的 `broker.credentials.apiKey`

如果缺少任何一项，请建议先运行 `/clawback setup`。

---

ClawBack 跟踪国会成员（众议院和参议院）披露的股票交易，并在用户的 E*TRADE 经纪账户中自动执行相应的交易。该工具基于这样一个前提：由于信息优势，国会领导者的投资表现通常优于市场。

## 默认监控的政客

ClawBack 默认监控以下政客（可配置）：

| 政客 | 所属议院 | 优先级 |
|------------|---------|----------|
| Nancy Pelosi | 众议院 | 1（最高优先级） |
| Dan Crenshaw | 众议院 | 2 |
| Tommy Tuberville | 参议院 | 2 |
| Marjorie Taylor Greene | 众议院 | 3 |

## 交易策略默认值

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------|
| 交易延迟 | 3 天 | 披露信息后等待 3 天再交易 |
| 持有期限 | 30 天 | 交易头寸的持有时间 |
| 交易规模 | 5% | 每笔交易的最大分配比例 |
| 止损 | 8% | 每笔交易的止损幅度 |
| 投资组合回撤 | 15% | 投资组合的最大损失限度 |
| 披露检查时间 | 美国东部时间 10:00, 14:00, 18:00 | 每日检查时间 |

## 功能

- **实时跟踪披露信息**：来自官方众议院书记员和参议院的电子文件披露（eFD）
- **自动执行交易**：通过 E*TRADE API（仅支持该经纪商）
- **智能交易规模调整**：根据用户账户规模调整交易规模 |
- **动态止损**：锁定利润，限制损失 |
- **风险管理**：设置回撤限制，防止连续亏损 |
- **Telegram 通知**：接收新交易和止损的提醒 |
- **回测引擎**：使用历史数据测试交易策略

## 性能（回测结果）

| 策略 | 胜率 | 收益率 | 夏普比率 |
|----------|----------|--------|--------|
| 3 天延迟，30 天持有 | 42.9% | +6.2% | 0.39 |
| 9 天延迟，90 天持有 | 57.1% | +4.7% | 0.22 |

根据 NBER 的研究，国会领导者的投资表现每年优于标准普尔 500 指数 47%。

## 通过 ClawHub 安装

```bash
# Install from ClawHub registry
clawhub install clawback

# Or install from local directory
clawhub install ./clawback
```

### 安装后的设置

通过 ClawHub 安装后，`install.sh` 脚本会自动执行以下操作：
1. **Python 环境设置**：创建虚拟环境
2. **包安装**：通过 pip 安装 ClawBack
3. **目录结构**：创建 logs/、data/、config/ 目录
4. **设置提示**：询问是否要运行设置向导

如果您在安装过程中跳过了设置步骤，可以手动运行：
```bash
cd ~/.openclaw/skills/clawback
./setup.sh          # Interactive setup wizard
# or
clawback setup      # CLI-based setup
```

### 改进的设置功能

- **更好的输入处理**：支持交互式和非交互式模式
- **输入验证**：验证 E*TRADE API 密钥的格式
- **超时处理**：如果没有输入，自动使用默认值
- **错误恢复**：如果 CLI 失败，切换到手动设置
- **配置检查**：检测现有配置并提供选项

## 交互式设置向导

设置向导会指导您完成配置：

### 步骤 1：环境选择
- **沙箱**（建议用于测试）：不进行真实交易，使用 E*TRADE 开发者沙箱环境
- **生产环境**：使用真实货币进行真实交易

### 步骤 2：E*TRADE API 凭据
- **消费者密钥**：从 E*TRADE 开发者门户获取
- **消费者秘钥**：从 E*TRADE 开发者门户获取

### 步骤 3：身份验证
- 与 E*TRADE 自动进行 OAuth 验证
- 打开浏览器进行授权
- 显示验证码

### 步骤 4：账户选择
- 列出所有可用的 E*TRADE 账户
- 选择用于交易的账户

### 步骤 5：Telegram 设置（可选）
- 通过 Telegram 机器人配置通知
- 如果可用，使用 OpenClaw 的内置 Telegram 频道

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

`clawback` 守护进程会持续运行，执行以下操作：
- 在美国东部时间 10:00、14:00、18:00 进行披露信息检查（这些时间是文件通常发布的时刻）
- 在美国东部时间上午 9:35 开始交易（市场开盘后 5 分钟）
- 每 90 分钟刷新令牌（保持 E*TRADE 会话活跃）
- 遵循市场交易时间（上午 9:30 - 下午 4:00）

## 数据来源

- **众议院书记员**：https://disclosures-clerk.house.gov（PDF 文件解析）
- **参议院电子文件披露**：https://efdsearch.senate.gov（网络爬取）
- **财务数据准备**：可选的增强型财务数据

## 支持的经纪商

ClawBack 目前仅支持 E*TRADE。虽然支持其他经纪商的适配器模式，但目前仅实现了 E*TRADE 的功能并进行测试。

| 经纪商 | 适配器 | 状态 |
|--------|---------|--------|
| E*TRADE | `etrade_adapter.py` | 已支持 |

## 风险管理

- **交易限额**：每个股票的最大交易比例为 5%，最多 20 个交易头寸
- **止损**：每个交易头寸的止损幅度为 8%，投资组合的最大损失为 15%
- **每日限额**：每日最大损失限制为 3%
- **PDT 合规性**：每天最多 2 笔交易

## 身份验证辅助工具

对于在主 CLI 之外进行手动 E*TRADE 验证的情况：

```bash
# Standalone OAuth authentication script
cd {baseDir}
source venv/bin/activate
python scripts/auth_script.py
```

该工具会生成授权 URL，提示用户输入验证码，并完成身份验证。

## 文件位置

| 文件 | 用途 |
|------|---------|
| `~/.clawback/config.json` | 主配置文件 |
| `~/.clawback/.access_tokens.json` | E*TRADE OAuth 令牌 |
| `~/.clawback/data/trading.db` | SQLite 数据库 |

## 安全性

- 源代码中不包含硬编码的凭据
- 配置基于环境变量
- E*TRADE 令牌存储采用加密方式
- `.env` 文件被 Git 忽略（防止泄露）
- 可选的生产环境加密

## 支持

- **文档**：详细设置信息请参阅 README.md
- **问题反馈**：https://github.com/mainfraame/clawback/issues
- **社区**：https://discord.com/invite/clawd

## 免责声明

**交易存在重大损失风险。** 本软件仅用于教育目的。过去国会成员的交易表现不能保证未来的结果。在实际交易前，请务必在 E*TRADE 沙箱账户中进行测试。