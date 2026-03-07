---
name: trading-agents
description: 基于 AgentScope 的多智能体股票诊断系统。用于股票分析、生成投资报告，或构建多智能体协作的 AI 金融分析工作流。
---

# Trading Agents股票投资分析系统

基于 AgentScope 框架的多智能体协作股票诊断系统。

## 系统架构

### 智能体团队

1. **分析师团队** (ReActAgent)
   - MarketAnalyst: 技术面分析
   - FundamentalsAnalyst: 基本面分析
   - NewsAnalyst: 舆情面分析

2. **研究员团队** (AgentBase)
   - BullishResearcher: 看多研究员
   - BearishResearcher: 看空研究员
   - ResearchFacilitator: 研究主持人

3. **交易与风控团队**
   - Trader: 交易员
   - AggressiveRisk: 激进型风控
   - NeutralRisk: 中性型风控
   - ConservativeRisk: 保守型风控
   - RiskFacilitator: 风控协调人

4. **基金经理**
   - Manager: 最终决策

### 工作流程

```
阶段1: 数据采集（分析师团队）
  ↓
阶段2: 研究员辩论
  ↓
阶段3: 交易员决策
  ↓
阶段4: 风险管理讨论
  ↓
阶段5: 基金经理最终决策
```

## 快速开始

### 使用方法

**方式一: 作为 OpenClaw 技能使用**

将本目录复制到 OpenClaw 项目的 skills 目录：
```bash
cp -r trading-agents /path/to/openclaw/skills/
```

**方式二: 作为 Python 包安装**

```bash
# 安装整个技能包
pip install /path/to/trading-agents/

# 或进入 scripts 目录安装核心代码
pip install /path/to/trading-agents/scripts/
```

### 基本用法

**OpenClaw 中使用:**
```python
# OpenClaw 会自动加载技能
from trading_agents import StockAdvisorSystem

# 或使用完整路径
from trading_agents.scripts import StockAdvisorSystem
```

**独立使用:**
```python
from trading_agents import StockAdvisorSystem

# 创建系统实例
advisor = StockAdvisorSystem()

# 诊断股票
result = advisor.diagnose("600519.SH", base_report_dir="report")

# 保存完整报告
advisor.save_report(result)

print(f"报告目录: {result['report_dir']}")
print(f"最终决策: {result['final_decision']}")
```

### 使用特定模型

```python
from trading_agents.config import config

# 切换模型
config.model_name = "qwen-max-2025-01-25"  # 或其他支持的模型

# 支持的模型:
# - kimi-k2.5
# - qwen-max-2025-01-25
# - qwen3.5-plus
# - glm-5
# - MiniMax/MiniMax-M2.5
```

## 配置说明

### 环境变量

```bash
# Tushare API Token
TUSHARE_TOKEN=your_token_here

# 阿里云百炼 API Key
ALIYUN_BAILIAN_API_KEY=your_key_here
```

### 配置参数

```python
from trading_agents.config import config

# 辩论轮数
config.debate_rounds = 2

# 风控讨论轮数
config.risk_discussion_rounds = 2

# 权重配置
config.tech_weight = 0.25    # 技术面权重
config.fund_weight = 0.35    # 基本面权重
config.news_weight = 0.20    # 舆情面权重
config.research_weight = 0.20 # 研究员共识权重
```

## 输出报告

系统生成以下报告文件:

- `MarketAnalyst_技术面分析.md`
- `FundamentalsAnalyst_基本面分析.md`
- `NewsAnalyst_舆情面分析.md`
- `研究员辩论报告.md`
- `交易员决策报告.md`
- `风险管理讨论报告.md`
- `最终决策报告.md`
- `complete_diagnosis_report.json` (完整JSON数据)
- `{股票名}_{代码}_{时间}_{决策}.pdf` (合并PDF报告)

## 核心组件

### 分析师智能体

```python
from trading_agents.agents import (
    MarketAnalystAgent,
    FundamentalsAnalystAgent,
    NewsAnalystAgent
)

# 技术面分析
market_analyst = MarketAnalystAgent()
report = market_analyst.analyze("600519.SH")

# 基本面分析
fund_analyst = FundamentalsAnalystAgent()
report = fund_analyst.analyze("600519.SH")

# 舆情分析
news_analyst = NewsAnalystAgent()
report = news_analyst.analyze("600519.SH", "贵州茅台")
```

### 数据工具

```python
from trading_agents.tools import TushareTools, AKShareTools

# Tushare 数据
tushare = TushareTools(token)
data = tushare.get_stock_daily("600519.SH", days=60)
indicators = tushare.get_technical_indicators("600519.SH")

# AKShare 数据
akshare = AKShareTools()
news = akshare.get_stock_news("600519.SH", days=7)
sentiment = akshare.get_market_sentiment()
```

### AgentScope 工具包

```python
from trading_agents.tools import (
    create_market_analyst_toolkit,
    create_fundamentals_analyst_toolkit,
    create_news_analyst_toolkit,
    create_stock_toolkit
)

# 创建工具包
toolkit = create_stock_toolkit()
```

## 批量诊断

```python
from trading_agents.batch_diagnose import batch_diagnose

stocks = ["600519.SH", "000858.SZ", "002594.SZ"]
results = batch_diagnose(stocks, output_dir="report/batch")
```

## 依赖安装

```bash
pip install agentscope>=0.0.5
pip install tushare>=1.2.89
pip install akshare>=1.12.0
pip install pandas>=2.0.0
pip install fpdf2>=2.8.0
pip install python-dotenv
```

## 项目结构

### Skill 目录结构 (OpenClaw 兼容)

```
trading-agents/              # 技能根目录
├── SKILL.md                 # Skill 说明文档 (必需)
├── __init__.py              # Python 包标识 (OpenClaw 需要)
├── setup.py                 # 安装配置
└── scripts/                 # 完整源代码
    ├── __init__.py
    ├── stock_advisor.py  # 主系统入口
    ├── config.py            # 系统配置
    ├── batch_diagnose.py    # 批量诊断
    ├── streamlit_app.py     # Web 界面
    ├── requirements.txt     # 依赖清单
    ├── agents/
    │   ├── __init__.py
    │   ├── analysts.py      # 分析师团队 (ReActAgent)
    │   ├── researchers.py   # 研究员团队 (AgentBase)
    │   ├── trader.py        # 交易员
    │   ├── risk_managers.py # 风险管理团队
    │   └── manager.py       # 基金经理
    └── tools/
        ├── __init__.py
        ├── tushare_tools.py # Tushare 数据接口
        ├── akshare_tools.py # AKShare 数据接口
        └── toolkit.py       # AgentScope 工具注册
```

### 移植到其他项目

只需复制整个 `trading-agents` 目录：

```bash
# 从源项目复制到目标项目
cp -r /source/project/.qoder/skills/trading-agents \
      /target/project/.qoder/skills/

# 或在目标项目中克隆后复制
mkdir -p /target/project/.qoder/skills/
cp -r trading-agents /target/project/.qoder/skills/
```

## 注意事项

1. **API Token**: 需要配置 TUSHARE_TOKEN 和 ALIYUN_BAILIAN_API_KEY
2. **中文字体**: PDF生成需要系统中文字体支持
3. **网络连接**: 需要访问阿里云百炼 API
4. **数据限制**: Tushare 免费版有数据调用限制
