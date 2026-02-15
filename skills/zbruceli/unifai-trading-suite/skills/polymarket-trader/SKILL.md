---
name: polymarket-trader
description: 查询 Polymarket 预测市场的相关内容——包括热门事件、加密货币、政治、体育等方面的信息，以及支持搜索功能。
homepage: https://polymarket.com
user-invocable: true
metadata: {"moltbot":{"emoji":"🔮","requires":{"env":["UNIFAI_AGENT_API_KEY","GOOGLE_API_KEY"]},"primaryEnv":"UNIFAI_AGENT_API_KEY"}}
---

# Polymarket Trader

用于查询Polymarket——Polygon区块链上领先的去中心化预测市场。

## 关于Polymarket

Polymarket是一个去中心化的预测市场平台，用户可以在此平台上对现实世界事件的结局进行预测和交易。该平台基于Polygon区块链运行，交易结算使用USDC.e作为货币。

## 命令

### 热门事件
```bash
python3 {baseDir}/scripts/polymarket.py trending
```
获取当前热门的预测事件。

### 加密货币市场
```bash
python3 {baseDir}/scripts/polymarket.py crypto
```
获取与加密货币相关的预测市场。

### 政治市场
```bash
python3 {baseDir}/scripts/polymarket.py politics
```
获取政治相关的预测市场。

### 搜索市场
```bash
python3 {baseDir}/scripts/polymarket.py search "<query>"
```
按关键词搜索市场。

### 分类市场
```bash
python3 {baseDir}/scripts/polymarket.py category <name>
```
按类别获取市场（热门、新市场、政治、加密货币、科技、文化、体育、世界、经济）。

## 输出格式

结果包括：
- 事件/市场名称
- 是/否的价格（概率）
- 交易量
- 流动性
- 结束日期

## 分类

| 分类 | 描述 |
|----------|-------------|
| 热门 | 最受欢迎的市场 |
| 新市场 | 最近创建的市场 |
| 政治 | 政治事件和选举 |
| 加密货币 | 加密货币预测 |
| 科技 | 科技行业事件 |
| 文化 | 娱乐和文化 |
| 体育 | 体育赛事结果 |
| 世界 | 全球事件 |
| 经济 | 经济指标 |

## 使用示例

**用户**：“Polymarket上有什么热门事件？”
**助手**：我将从Polymarket获取热门事件的信息。

```bash
python3 {baseDir}/scripts/polymarket.py trending
```

**用户**：“搜索与比特币相关的市场”
**助手**：我正在Polymarket中搜索与比特币相关的市场。

```bash
python3 {baseDir}/scripts/polymarket.py search "bitcoin"
```

## 所需权限

- `UNIFAI_AGENT_API_KEY` - 用于Polymarket工具的UnifAI SDK密钥
- `GOOGLE_API_KEY` - 用于LLM处理的Gemini API密钥

## API信息

- **数据来源**：UnifAI Polymarket工具（工具包ID：127）
- **可用功能**：search、getEventsByCategory、getPrices、 getOrderBooks
- **速率限制**：遵循UnifAI API的速率限制

## 注意事项

- 该工具仅支持读取数据（交易需要钱包认证）
- 价格以小数形式显示（0.75表示75%的概率）
- 市场在Polygon区块链上结算
- 交易使用USDC.e作为货币
- 该工具不适用于受限制的地区