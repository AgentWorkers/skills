---
name: prediction-trader
description: 利用AI技术对Polymarket和Kalshi平台上的预测市场进行分析，并结合社交信号进行综合评估
homepage: https://github.com/your-repo/trading
user-invocable: true
metadata: {"moltbot":{"emoji":"📈","requires":{"env":["UNIFAI_AGENT_API_KEY","GOOGLE_API_KEY"]},"primaryEnv":"UNIFAI_AGENT_API_KEY"}}
---

# 预测交易助手

这是一个基于人工智能的预测市场分析工具，能够从多个平台和社交信号中收集数据。

## 支持的平台

- **Polymarket**：位于Polygon平台上的海外预测市场（涵盖加密货币、政治、体育、世界事件等领域）
- **Kalshi**：受美国商品期货交易委员会（CFTC）监管的预测市场（涵盖联邦利率、GDP、CPI等经济指标）

## 命令

### 比较市场
```bash
python3 {baseDir}/scripts/trader.py compare "[topic]"
```
比较两个平台上关于特定主题的预测市场情况。

### 获取热门市场
```bash
python3 {baseDir}/scripts/trader.py trending
```
获取两个平台上当前热门的预测市场信息。

### 分析主题
```bash
python3 {baseDir}/scripts/trader.py analyze "[topic]"
```
提供包括市场数据及社交信号在内的全面分析报告。

### 平台特定操作
```bash
# Polymarket
python3 {baseDir}/scripts/trader.py polymarket trending
python3 {baseDir}/scripts/trader.py polymarket crypto
python3 {baseDir}/scripts/trader.py polymarket search "[query]"

# Kalshi
python3 {baseDir}/scripts/trader.py kalshi fed
python3 {baseDir}/scripts/trader.py kalshi economics
python3 {baseDir}/scripts/trader.py kalshi search "[query]"
```

## 输出格式

输出结果包括：
- 市场问题/标题
- “是/否”选项的价格（表示概率）
- 交易量
- 数据来源平台
- 数据更新日期（如有的话）

## 所需参数

- `UNIFAI_AGENT_API_KEY`：用于访问Polymarket工具和社交信号的UnifAI SDK密钥
- `GOOGLE_API_KEY`：用于访问Gemini API进行语言模型分析的密钥

## 使用示例

**用户**：“比较比特币的预测市场情况”

**助手**：我将比较Polymarket和Kalshi平台上关于比特币的预测市场信息。

```bash
python3 {baseDir}/scripts/trader.py compare "bitcoin"
```

**用户**：“当前的联邦利率预测是多少？”

**助手**：我正在从Kalshi获取关于联邦利率的预测数据。

```bash
python3 {baseDir}/scripts/trader.py kalshi fed
```

## 注意事项

- Polymarket的数据通过UnifAI工具获取（可能存在访问频率限制）
- Kalshi的数据通过公开API直接获取（读取无需认证）
- 该工具仅支持数据查询，交易操作需要平台认证
- 所有价格均以小数形式显示（例如0.75表示75%的概率）