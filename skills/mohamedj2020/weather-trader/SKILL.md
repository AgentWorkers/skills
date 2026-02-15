---
name: weather-enhanced
displayName: Weather Trading (Enhanced)
description: 利用NOAA的天气预报数据，在Polymarket平台上进行天气相关市场的交易。该系统采用动态置信度建模和高质量数据过滤机制，为用户提供更安全、更可靠的交易环境。适用于希望在使用温度数据相关市场时获得高级保护措施的用户。
metadata: {"clawdbot":{"emoji":"🌡️","requires":{"env":["SIMMER_API_KEY"]},"cron":"0 */6 * * *","autostart":false}}
authors:
  - Enhanced by Claude
attribution: "Based on Simmer weather skill, enhanced with dynamic confidence and quality scoring"
version: "2.0.0"
---
# 天气交易（增强版）

## 关键功能：自动交易技能

启用此技能后，将使用真实资金进行实际交易。

**重要信息：**
- **默认状态**：`autostart:false` —— 不会自动运行
- **自动行为**：手动启用后，每6小时运行一次
- **财务风险**：每日可能交易30-60美元（使用质量过滤器时，每日最高100美元）
- **无需逐笔交易审核**：交易会自动执行，无需人工批准

## 安装与安全

### 凭据

**必需的凭据：**
- `SIMMER_API_KEY` —— 来自simmer.markets/dashboard的交易API密钥

**可选（非敏感配置）：**
- 6个`SIMMER_WEATHER_*`环境变量，用于设置交易参数（详见配置文件）

**无需其他凭据**（无需钱包密钥、RPC端点或云服务凭据）。

**可选依赖项：** 如果安装`tradejournal`，它将记录交易详情。默认不安装。安装前请检查源代码。

### 安装方法

- 手动安装（无自动脚本）
- 将文件放入`~/.openclaw/skills/weather-enhanced/`目录
- 创建包含API密钥的`.env`文件
- 系统不会自动写入任何数据

### 依赖项

```
python-dotenv>=1.0.0  # Optional
```

**依赖项列表：**
- 使用内置的`urllib`库（不依赖`requests`库）
- 无`web3`、Telegram机器人或其他未使用的依赖项
- **可选依赖项：** `tradejournal`（用于记录交易日志，但在`requirements.txt`中注释掉了）

### 网络端点

此技能连接到3个端点：

1. **api.weather.gov**（NOAA）
   - **用途**：获取天气预报
   - **发送的数据**：纬度/经度（公共坐标）
   - **接收的数据**：天气预报（公共数据）
   - **认证方式**：无需认证
   - **代码位置**：`weather_trader_enhanced.py`文件第250-280行

2. **nominatim.openstreetmap.org**（地理编码）
   - **用途**：将城市名称转换为坐标
   - **发送的数据**：城市名称字符串（例如：“Chicago”）
   - **接收的数据**：纬度/经度坐标
   - **认证方式**：无需认证
   - **代码位置**：`weather_trader_enhanced.py`文件第200-230行

3. **api.simmer.markets**（交易）
   - **用途**：执行交易、查询投资组合
   - **发送的数据**：`SIMMER_API_KEY`（bearer token）和交易订单
   - **接收的数据**：交易确认信息、持仓情况和余额
   - **认证方式**：使用bearer token
   - **代码位置**：`weather_trader_enhanced.py`文件第300-350行

**注意：** 如果安装了`tradejournal`依赖项，可能会增加额外的端点。

### 安全保障

- 代码中不存在其他网络连接
- API密钥不会被记录到磁盘或控制台
- API密钥仅发送到`api.simmer.markets`
- 无数据泄露或跟踪功能
- 所有网络请求都在源代码中可见（可以使用`grep`验证）

### API密钥权限

您的`SIMMER_API_KEY`应具有以下权限：
- 读取投资组合信息（必需）
- 读取持仓情况（必需）
- 执行交易（必需）
- 无取款权限
- 无修改账户权限

**创建最小权限的API密钥：**
1. 访问simmer.markets/dashboard → SDK选项卡
2. 创建新的API密钥
3. 如果可用，选择“仅用于交易”
4. 绝不要授予取款权限
5. 将密钥存储在`.env`文件中（Git会忽略该文件）
6. 测试完成后定期更换密钥

### 配置存储

- `.env`文件：包含`SIMMER_API_KEY`（不会提交到代码仓库）
- `config.json`：仅包含交易参数（非敏感信息）
- 无持久化日志
- 所有数据均为临时数据（仅显示在控制台）

**注意：** `.env`文件中的旧变量`WALLET_PRIVATE_KEY`和`POLYGON_RPC_URL`已弃用（因为不再使用`web3`库）。

## 安全特性

- **默认设置**：自动交易功能禁用，必须手动启用
- **质量过滤器**：排除流动性较低的市场
- **持仓限额**：每笔交易最多5美元
- **交易次数限制**：每6小时最多5笔交易
- **入场阈值**：仅买入被低估的市场
- **出场阈值**：价格达到盈利时自动卖出

## 启用前的步骤

**请务必完成以下步骤：**

### 1. 查看源代码**

```bash
# Inspect main trading logic
cat weather_trader_enhanced.py | less

# Verify network endpoints (should only find 3)
grep -n "urlopen\|Request\|http" weather_trader_enhanced.py

# Check API key usage (should only send to simmer.markets)
grep -n "api_key\|SIMMER_API_KEY" weather_trader_enhanced.py

# Check optional tradejournal usage
grep -n "tradejournal\|log_trade" weather_trader_enhanced.py
```

### 2. 了解平台行为

**OpenClaw元数据控制：**
- `autostart:false`：启动时不会运行该技能（安全默认设置）
- `cron:"0 */6 * * *"`：仅在自动交易功能启用时执行
- 通过编辑第5行来启用该功能：将`autostart:false`更改为`autostart:true`
- 请参考OpenClaw的官方文档确认设置方法：https://docs.openclaw.ai/
- 手动编辑文件可防止意外激活
- **替代方案**：可以直接手动运行该技能，无需启用自动交易功能

**启用后**：每6小时运行一次（凌晨12点、上午6点、中午12点、下午6点）

**禁用后**：完全不运行

### 3. 验证API密钥权限

检查您的SIMMER API密钥：
- 是否可以读取投资组合信息？（必需）
- 是否可以执行交易？（必需）
- 是否可以取款？（不应有此权限）
- 是否可以修改账户信息？（不应有此权限）

如果您的密钥具有取款权限，请创建一个新的、仅用于交易的密钥。

### 4. 测试实际交易

```bash
# Check balance first
python scripts/status.py

# Execute live trades (start with small balance)
python weather_trader_enhanced.py --live --smart-sizing
```

- 在simmer.markets/dashboard上密切监控交易情况
- 确认交易是否正确执行
- 等待交易结果（1-3天）
- 分析交易结果

### 5. 启用自动交易（可选）

**仅在手动测试成功后启用**

OpenClaw通过`SKILL.md`文件中的`autostart`字段来控制技能的启用状态：
- 请参考OpenClaw的官方文档或平台用户界面进行确认
- 手动编辑文件可防止意外激活

**操作步骤：**
1. 修改`SKILL.md`文件第5行（元数据相关部分）
2. 将`"autostart":false`更改为`"autostart":true`
3. 保存文件
4. 重启OpenClaw：`openclaw restart`
5. 查看日志以确认是否按计划运行

**手动运行方式（备用方案）：**
```bash
python weather_trader_enhanced.py --live --smart-sizing
```
这种方式可完全控制交易时机。

## 快速入门

```bash
# Check balance
python scripts/status.py

# Execute live trades
python weather_trader_enhanced.py --live --smart-sizing

# Optional: Dry run for testing
python weather_trader_enhanced.py --dry-run
```

## 所需条件**

- 从simmer.markets/dashboard的SDK选项卡获取`SIMMER_API_KEY`
- Simmer钱包中需有USDC余额

## 配置

**通过环境变量或`config.json`进行配置：**

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `SIMMER_WEATHER_ENTRY` | 0.15 | 低于此价格时买入 |
| `SIMMER_WEATHER_EXIT` | 0.45 | 高于此价格时卖出 |
| `SIMMER_WEATHER_MAX_POSITION` | 5.00 | 每笔交易的最高金额（美元） |
| `SIMMER_WEATHER_MAX_TRADES` | 5 | 每次运行的最大交易次数 |
| `SIMMER_WEATHER_LOCATIONS` | "ALL" | 目标城市 |
| `SIMMER_WEATHER_MIN_QUALITY` | 0.6 | 市场质量最低要求 |

## 功能特点**

- **动态信心值**：根据预报时间调整交易策略（60-90%）
- **市场质量评分**：过滤流动性较低的市场
- **智能地理编码**：支持美国任何城市
- **增强型解析**：更准确的温度数据识别
- **重试机制**：在API故障时自动恢复

## 命令

```bash
# Live trading
python weather_trader_enhanced.py --live --smart-sizing

# Check positions
python weather_trader_enhanced.py --positions

# View config
python weather_trader_enhanced.py --config

# Set config
python weather_trader_enhanced.py --set entry_threshold=0.20

# Optional: Dry run for testing
python weather_trader_enhanced.py --dry-run
```

## 工作原理**

1. 从NOAA获取目标位置的天气预报
2. 通过Simmer API发现可交易的市场
3. 根据动态信心值计算交易时机（根据预报时间调整）
4. 根据市场质量（流动性、成交量、响应时间）筛选市场
5. 当价格低于入场阈值时执行交易
6. 当价格高于出场阈值时自动平仓

**动态信心值的计算规则：**
- 当前日期：90%
- 1天后：88%
- 2天后：85%
- 3天后：80%
- 7天后及以后：60%

**市场质量评分标准：**
- 流动性（40%）
- 成交量（30%）
- 响应时间（20%）
- 价格极端情况（10%）

**仅对评分≥60%的市场执行交易。**

## 故障排除**

- **“SIMMER_API_KEY未设置”**：请设置环境变量或将其添加到`.env`文件中
- **“未找到可交易的市场”**：如果Polymarket上没有活跃市场，这是正常现象
- **“持仓金额过小”**：增加`max_position_usd`的值，或使用`--smart-sizing`参数
- **“市场质量评分过低”**：说明市场流动性或成交量较低

## 安全检查清单

**安装前请确认：**

### 代码审查**
- 已检查`weather_trader_enhanced.py`源代码
- 已验证3个网络端点的连接情况（NOAA、Nominatim、Simmer）
- 确认API密钥仅发送到`api.simmer.markets`
- 代码中无可疑代码或混淆处理

### 依赖项检查**
- 确认`requirements.txt`中仅列出`python-dotenv>=1.0.0`作为依赖项
- 无未使用的依赖项（已移除`web3`、`telegram`、`requests`）
- 使用内置的`urllib`库进行HTTP请求
- 如果安装`tradejournal`，请先检查源代码

### 配置检查**
- 确认`SKILL.md`文件第5行中的`autostart:false`设置
- 通过OpenClaw的官方文档或用户界面确认启用方法
- 知道如何禁用该技能
- 确认持仓限额（每笔交易最多5美元）

### API密钥设置**
- 创建了最小权限的SIMMER API密钥
- 密钥没有取款权限
- 密钥存储在`.env`文件中（仅用于本地使用，不会提交到代码仓库）
- 确认密钥具有读取投资组合和执行交易的权限

### 测试**
- 成功运行`python scripts/status.py`脚本
- 使用`--live`参数使用小额余额进行手动交易
- 在simmer.markets/dashboard上监控交易情况
- 确认自动交易功能正常运行
- 可选：先使用`--dry-run`进行测试

### 风险说明**
- 了解自动交易的风险
- 知道每日最大交易金额（30-60美元，最高100美元）
- 交易无需逐笔审核
- 知道如何停止自动交易（在OpenClaw中禁用该技能或修改`SKILL.md`文件）
- 开始使用时建议使用小额余额（50-100美元）

### 平台行为**
- 确认OpenClaw会尊重`autostart:false`设置
- 确认该技能仅在手动启用后才会运行
- 知道自动交易的执行时间（启用后每6小时运行一次）
- 知道如何查看OpenClaw的日志

**如果任何选项未勾选，请勿启用此技能。**

## 紧急停止**

**立即停止该技能的方法：**

```bash
# Option 1: Disable in OpenClaw UI

# Option 2: Edit SKILL.md
# Change line 5: "autostart":false
# Then: openclaw restart

# Option 3: Stop OpenClaw entirely
openclaw stop

# Close positions manually on simmer.markets/dashboard
```

## 技术支持**

源代码位于`weather_trader_enhanced.py`文件中
所有网络请求的详细信息都记录在该文件中
无隐藏功能或混淆处理

**请自行承担风险。此技能会使用真实资金进行实际交易。**
**使用前请充分了解预测市场和交易风险。**