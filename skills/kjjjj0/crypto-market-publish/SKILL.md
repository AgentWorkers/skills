---
name: crypto-market
description: 全面的加密货币市场监控和经济数据分析工具。适用于追踪加密货币价格、市场情绪、经济数据发布，以及分析经济指标对加密货币市场的影响。支持价格警报、经济日历管理、实际价值更新和自动化报告功能。安装完成后，您可以在您的加密货币工作区（安装指南文件中指定的默认路径）直接运行该工具。
---
# 加密货币市场监控器

这是一个完整的加密货币市场监控系统，具备价格跟踪、经济数据发布和影响分析功能。

## 安装

快速安装：
```bash
clawhub install crypto-market
```

如需手动安装，请参阅 [INSTALL.md](INSTALL.md)。

## 快速入门

### 价格监控
实时监控13种主要加密货币（BTC、ETH、XRP、BNB、SOL、ADA、AVAX、DOGE、TRX、LINK、SUI、WLFI、XAUT）的价格，提供价格波动警报（±5%）、市场情绪分析以及EMA技术指标。

**从您的加密货币工作区开始：**
```bash
cd scripts
python3 crypto_monitor_telegram.py
```

### 经济数据报告
查看即将发布的经济数据（7天预测），包括数据的重要性和倒计时。

**从您的加密货币工作区开始：**
```bash
cd economic
python3 daily_economic_report_v2.py
```

## 经济数据分析

### 更新实际数据
当经济数据发布时，系统会自动更新实际数据以触发买入/卖出分析。

**从您的加密货币工作区开始：**
```bash
cd economic
python3 update_economic_data.py update "数据名称" "实际值" --datetime "发布时间"
```

**示例：**
```bash
# CPI data (lower is bullish)
python3 update_economic_data.py update "CPI 消费者价格指数" "2.1%" --datetime "2026-03-13 21:30"

# NFP data (higher is bullish)
python3 update_economic_data.py update "非农就业数据" "+280K" --datetime "2026-03-14 21:30"

# GDP data (higher is bullish)
python3 update_economic_data.py update "GDP 季度报告" "1.8%" --datetime "2026-03-20 21:30"

# Unemployment rate (lower is bullish)
python3 update_economic_data.py update "失业率" "4.0%" --datetime "2026-03-14 21:30"
```

### 快速分析（不保存数据）
无需将分析结果保存到数据库即可进行分析。

**示例：**
```bash
python3 update_economic_data.py analyze "CPI" "2.1%" "2.3%" "2.4%"
```

### 查看更新后的数据
查看所有带有实际数据的经济信息。

```bash
python3 update_economic_data.py list
```

## 买入/卖出分析

### 买入信号指标（数值越高表示越乐观） 🟢
- 非农就业数据（NFP）
- 国内生产总值（GDP）
- 零售销售
- ADP就业数据
- 制造业采购经理指数（PMI）
- 服务业采购经理指数（PMI）

**规则：** 实际数据 > 预期数据（+2%） = 买入信号

### 卖出信号指标（数值越低表示越悲观） 🟢
- 消费者价格指数（CPI）
- 生产者价格指数（PPI）
- 失业率
- 美联储利率（FOMC）

**规则：** 实际数据 < 预期数据（-2%） = 卖出信号（压力缓解）

## 定期报告

### 每日经济报告
- **时间：** 每日08:00
- **内容：** 7天经济数据预测
- **格式：** 显示重要事件及其预期值和剩余时间

### 全面监控
- **时间：** 每30分钟一次
- **内容：** 加密货币价格 + 经济数据提醒
- **功能：** 波动警报、市场情绪、EMA指标

## 默认工作区结构

```
crypto/                    # Your crypto workspace
├── economic/            # Economic data scripts
├── scripts/             # Monitoring scripts
├── data/                # Data storage (actual_data.json)
└── logs/                # Log files
```

## 数据类型

### 重要指标
- 非农就业数据（NFP） - 每月第一个周五，21:30
- 消费者价格指数（CPI） - 每月中间，21:30
- 美联储利率（FOMC） - 每季度，02:00
- 国内生产总值（GDP） - 每季度末，21:30
- 失业率 - 每月第一个周五，21:30

### 中等重要性指标
- ADP就业数据 - 每月第一个周三，21:15
- 零售销售 - 每月中间，21:30
- 制造业采购经理指数（PMI） - 每月第一天，22:00
- 服务业采购经理指数（PMI） - 每月第一天，22:00
- 生产者价格指数（PPI） - 每月中间，21:30

**有关各指标的详细信息，请参阅 [data-types.md](references/data-types.md)。**

## 脚本

**核心模块（位于 economic/ 目录下）：**
- `economic_calendar.py` - 经济日历管理
- `economic_analyzer.py` - 买入/卖出分析引擎
- `update_economic_data.py` - 实际数据管理

**监控相关脚本（位于 scripts/ 目录下）：**
- `crypto_monitor_telegram.py` - 价格监控 + 经济数据通知

**参考资料：**
- [quick-reference.md](references/quick-reference.md) - 命令参考手册
- [data-types.md](references/data-types.md) - 经济指标详情
- [usage-examples.md](references/usage-examples.md) - 实际使用场景

## 自定义

### 更改工作区设置
请编辑脚本中的路径或创建配置文件。详情请参阅 [INSTALL.md](INSTALL.md)。

### 修改警报阈值
编辑 `scripts/crypto_monitor_telegram.py` 文件中的相关设置：
```python
ALERT_THRESHOLD = 5.0  # Change to your preferred threshold
```

### 添加/删除支持的加密货币
请编辑 `scripts/crypto_monitor_telegram.py` 文件中的 `TOKENS` 字典。

## 重要说明

1. **时区：** 所有时间均采用亚洲/上海（北京时间）
2. **数据存储：** 实际数据保存在 `data/actual_data.json` 文件中
3. **影响分析：** 根据实际数据与预期数据的偏差自动判断市场走势
4. **警报阈值：** 价格波动达到±5%时触发警报

**有关详细的安装、自定义和使用说明，请参阅 [INSTALL.md](INSTALL.md) 和 [usage-examples.md](references/usage-examples.md)。**