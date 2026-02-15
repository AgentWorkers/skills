---
name: social-signals
description: 分析加密货币领域的社交信号：KOL（关键意见领袖）的提及、市场情绪、热门代币以及相关新闻
homepage: https://github.com/your-repo/trading
user-invocable: true
metadata: {"moltbot":{"emoji":"📡","requires":{"env":["UNIFAI_AGENT_API_KEY","GOOGLE_API_KEY"]},"primaryEnv":"UNIFAI_AGENT_API_KEY"}}
---

# 社交信号

分析来自Twitter/X、新闻来源以及KOL（关键意见领袖）讨论的加密货币社交信号。

## 数据来源

- **Elfa**：来自X/Twitter上的Web3 KOLs的热门代币
- **TokenAnalysis**：包含社交指标的代币综合分析工具
- **SerpAPI**：用于搜索加密货币相关新闻的Google News接口
- **Twitter**：直接搜索推文和用户时间线

## 命令

### 获取热门代币
```bash
python3 {baseDir}/scripts/signals.py trending
```
获取当前在加密货币KOL中热门的代币。

### 代币情绪分析
```bash
python3 {baseDir}/scripts/signals.py sentiment "<token>"
```
获取特定代币（例如BTC、ETH、SOL）的社交情绪分析结果。

### 搜索新闻
```bash
python3 {baseDir}/scripts/signals.py news "<query>"
```
搜索与某个主题相关的最新加密货币新闻。

### 事件摘要
```bash
python3 {baseDir}/scripts/signals.py events "<keyword>"
```
根据关键词从社交提及中获取事件摘要。

### 全面分析
```bash
python3 {baseDir}/scripts/signals.py analyze "<token>"
```
结合价格、社交和新闻信号进行综合分析。

## 输出格式

结果包括：
- 代币符号及当前指标
- 情绪得分（-1至1）和标签（看涨/看跌/中性）
- 被提及次数和社交互动量
- 主要讨论话题
- 最新新闻标题

## 需要的参数

- `UNIFAI_AGENT_API_KEY`：用于社交信号工具的UnifAI SDK密钥
- `GOOGLE_API_KEY`：用于分析的Gemini API密钥

## 使用示例

**用户**：“Solana的社交情绪如何？”
**助手**：我将分析SOL的社交信号。

```bash
python3 {baseDir}/scripts/signals.py sentiment "SOL"
```

**用户**：“KOL们正在讨论哪些代币？”
**助手**：让我看看加密货币KOL们正在关注哪些热门代币。

```bash
python3 {baseDir}/scripts/signals.py trending
```

## 信号类型

| 信号类型 | 来源 | 描述 |
|--------|--------|-------------|
| 情绪分析 | TokenAnalysis | 代币的总体社交情绪得分 |
| 热门代币 | Elfa | KOL推荐的热门代币 |
| 新闻 | SerpAPI | 最新的加密货币新闻文章 |
| 被提及次数 | Twitter | 推文的传播量和互动量 |

## 注意事项

- 社交信号属于滞后指标，请谨慎使用
- KOL的情绪可能会迅速变化
- 新闻情绪可能无法反映市场趋势
- 最佳用法是结合市场数据一起使用