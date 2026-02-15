---
name: dividend-premium-tracker
description: 跟踪 CSI 股息低波动指数的股息溢价（股息收益率减去 10 年期债券收益率）。监控股息收益率和 10 年期债券收益率，并根据这些数据计算股息溢价，以辅助投资决策。
version: 1.0.1
---

# 股息溢价追踪器

该工具用于追踪CSI股息低波动指数（CSI Dividend Low Volatility Index, H30269）的股息溢价（股息收益率减去10年期国债收益率）。

## 说明

该工具主要用于监控CSI股息低波动指数（H30269）的股息溢价，这一指标对中国以股息收益为主的投资决策具有重要意义。股息溢价反映了分红股票的超额回报相对于无风险债券的表现。

## 监控内容：

- **CSI股息低波动指数股息收益率**：来自中国证券指数（China Securities Index）
- **10年期中国国债收益率**：来自财政部（Ministry of Finance）
- **股息溢价** = 股息收益率 - 国债收益率

## 功能特点：

- 📊 自动下载并跟踪股息收益率和国债收益率数据
- 📈 生成包含清晰图表的Excel报告
- 🔔 当国债收益率连续3天上升时发出警报
- 🔔 当股息溢价降至1%以下时发出警报
- 📅 支持历史数据回填（backfill historical data）

## 命令：

### 更新今日数据
```bash
python3 scripts/update_dividend_premium.py --update
```

### 检查监控警报
```bash
python3 scripts/monitor_dividend_premium.py --check
```

### 回填历史数据
```bash
python3 scripts/update_dividend_premium.py --backfill 2026-01-01 2026-01-31
```

## 相关文件
```
dividend-premium-tracker/
├── SKILL.md              # This file
├── scripts/
│   ├── update_dividend_premium.py   # Main update script
│   └── monitor_dividend_premium.py  # Monitoring script
├── references/           # Documentation (optional)
└── assets/              # Output files (optional)
```

## 设置：

### Telegram警报（可选）

设置Telegram机器人Token以接收警报：
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
```

### Cron作业（每日更新）
```bash
crontab -e
# Add line:
0 17 * * * cd /path/to/skill && python3 scripts/update_dividend_premium.py --update
```

## 数据来源：

| 数据类型 | 来源 | URL |
|------|--------|-----|
| 股息收益率 | 中国证券指数 | [H30269指标数据文件](https://oss-ch.csindex.com.cn/static/html/csindex/public/uploads/file/autofile/indicator/H30269indicator.xls) |
| 国债收益率 | 财政部 | [ChinaBond数据网站](https://yield.chinabond.com.cn/cbweb-czb-web/czb/moreInfo?locale=cn_ZH&nameType=1) |

## 需求系统配置：

- Python 3.10及以上版本
- pandas库
- openpyxl库
- xlrd库
- curl工具（用于数据下载）

## 使用说明：

- 股息溢价计算公式：`股息收益率 (%) - 国债收益率 (%)`
- 当股息溢价低于1%时，表示可能存在买入机会
- 当股息溢价为负数时，说明分红股票的性价比高于债券
- 支持从2026年1月14日至今的历史数据

---

**相关指数：**
- CSI股息低波动指数（H30269/000966）
- 10年期中国国债