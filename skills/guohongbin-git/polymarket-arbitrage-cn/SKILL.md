---
name: polymarket-arbitrage-cn
description: "Polymarket 套利 | Polymarket 套利策略：预测市场中的套利机会，自动发现价格差异并执行套利操作。  
关键词：Polymarket、预测市场（Prediction market）、套利（Arbitrage）。"
metadata:
  openclaw:
    emoji: 📊
    fork-of: "https://clawhub.ai"
---# Polymarket套利

在Polymarket的预测市场中寻找并执行套利机会。

## 快速入门

### 1. 纸上交易（推荐的第一步）

运行一次扫描以查看当前的可套利机会：

```bash
cd skills/polymarket-arbitrage
pip install requests beautifulsoup4
python scripts/monitor.py --once --min-edge 3.0
```

在`polymarket_data/arbs.json`中查看结果

### 2. 持续监控

每5分钟监控一次，并在新出现的机会时发出警报：

```bash
python scripts/monitor.py --interval 300 --min-edge 3.0
```

使用`Ctrl+C`停止监控

### 3. 理解结果

每个检测到的套利机会包含以下信息：
- **净利润率**：扣除2%费用后的利润空间
- **风险评分**：0-100，评分越低越好
- **成交量**：市场流动性
- **操作建议**：应该买入/卖出哪些结果

好的套利机会应满足以下条件：
- 净利润率：3-5%以上
- 风险评分：低于50
- 成交量：超过100万美元
- 套利类型：`math_arb_buy`（更安全）

## 检测到的套利类型

### 数学套利（主要关注）

**类型A：买入所有结果**（概率之和小于100%）
- 最安全的类型
- 如果能够执行，利润有保障
- 例如：48% + 45% = 93% → 扣除费用后净利润约为5%

**类型B：卖出所有结果**（概率之和大于100%）
- 风险较高（需要足够的流动性）
- 需要资金作为抵押
- 在有经验之前避免尝试

详细示例和策略请参阅`references/arbitrage_types.md`。

### 跨市场套利

同一事件在不同市场上的价格不同（尚未实现——需要语义匹配）

### 订单簿套利

需要实时订单簿数据（网站显示的是中间价，而非可执行价格）

## 脚本

### fetch_markets.py

抓取Polymarket网站的活跃市场信息。

```bash
python scripts/fetch_markets.py --output markets.json --min-volume 50000
```

返回包含市场概率、成交量和元数据的JSON格式数据

### detect_arbitrage.py

分析市场以寻找套利机会。

```bash
python scripts/detect_arbitrage.py markets.json --min-edge 3.0 --output arbs.json
```

考虑以下因素：
- 每笔交易的2%费用
- 多个结果的交易费用计算
- 风险评分

### monitor.py

持续监控并触发警报。

```bash
python scripts/monitor.py --interval 300 --min-edge 3.0 [--alert-webhook URL]
```

功能包括：
- 定期获取市场数据
- 检测套利机会
- 仅对新出现的机会发出警报（避免重复通知）
- 将状态保存到`polymarket_data/`目录

## 工作流程阶段

### 第1阶段：纸上交易（1-2周）

**目标：**了解套利机会的频率和质量

1. 每天运行监控脚本2-3次
2. 将发现的机会记录在电子表格中
3. 确认这些机会在后续仍然存在
4. 计算可能的利润

**决策点：**如果每周发现3-5个好的套利机会，进入第2阶段。

### 第2阶段：微测试（50-100加元）

**目标：**熟悉平台操作

1. 注册Polymarket账户
2. 存入50-100加元的USDC
3. 仅进行手动交易（不使用自动化工具）
- 每次交易的最大金额不超过5-10加元
4. 在电子表格中记录每笔交易

**决策点：**如果20笔交易后盈利，进入第3阶段。

### 第3阶段：扩大规模（500加元）

**目标：**增加每次交易的金额

1. 将资金增加到500加元
- 每笔交易的最大金额不超过5%（25加元）
- 仍然进行手动交易
- 实施严格的风险管理

### 第4阶段：自动化（未来计划）

需要以下条件：
- 钱包集成（管理私钥）
- Polymarket API或浏览器自动化工具
- 执行逻辑
- 监控系统

**只有在手动交易持续盈利后，才考虑自动化。**

详细设置说明请参阅`references/getting_started.md`。

## 风险管理

### 重要规则

1. **每次交易的最大持仓比例：**资金总额的5%
2. **最低利润空间：**扣除费用后的净利润至少为3%
3. **每日亏损限额：**资金总额的10%
4. **优先选择买入套利机会：**在有经验之前避免卖出套利机会

### 警示信号

- 利润空间超过10%（可能是过时的数据）
- 成交量低于10万美元（流动性风险）
- 概率最近更新（套利机会可能已经消失）
- 卖出套利（需要更多的资金和流动性）

## 费用结构

Polymarket的收费标准：
- **做市商费用：**0%
- **撮合费用：**2%

**保守估计：**每笔交易2%的费用

**盈亏平衡计算：**
- 2个结果的市场：需要4%的毛利空间
- 3个结果的市场：需要6%的毛利空间
- N个结果的市场：需要N%的毛利空间

**目标：**扣除费用后的净利润为3-5%

## 常见问题

### “利润空间很高，但消失了”

网站上的概率可能是过时的，或者显示的是中间价而非可执行价格。这种情况很正常。真正的套利机会通常会在几秒钟内消失。

### “无法以显示的价格执行交易”

可能是流动性问题。成交量低的市场会导致概率显示不准确。请选择成交量超过100万美元的市场。

### “扣除费用后的利润空间太小”

调整`--min-edge`阈值。可以尝试将阈值设置为4-5%，以获得更保守的筛选标准。

## 文件和数据

所有监控数据存储在`./polymarket_data/`目录下：
- `markets.json`：最新的市场扫描结果
- `arbs.json`：检测到的套利机会
- `alert_state.json`：已通知的套利机会状态（避免重复通知）

## 高级主题

### Telegram集成（未来计划）

将Webhook地址传递给监控脚本，以便接收警报：

```bash
python scripts/monitor.py --alert-webhook "https://api.telegram.org/bot<token>/sendMessage?chat_id=<id>"
```

### 仓位大小调整

对于一个有p₁和p₂两个结果的数学套利，如果p₁ + p₂ < 100%：

**最佳分配方式：**
- 对结果1的投注金额：（100% / p₁） / [(100%/p₁) + (100%/p₂)] 的资金
- 对结果2的投注金额：（100% / p₂） / [(100%/p₁) + (100%/p₂)] 的资金

这样可以确保无论哪个结果获胜，都能获得相同的利润。

**简化规则：**对于利润空间较小的套利，将资金平均分配到两个结果上。

### 执行速度

套利机会消失得很快。如果计划使用自动化工具：
- 使用WebSocket连接（而非轮询）
- 同时下达限价单
- 提前准备好足够的资金
- 监控Polygon平台的交易费用

## 资源

- **Polymarket：** https://polymarket.com
- **文档：** https://docs.polymarket.com
- **API（如可用）：** 查看Polymarket的API文档
- **社区：** Polymarket的Discord频道

## 帮助支持

- 如有关于技能方面的问题，请参阅`references/arbitrage_types.md`以获取策略细节
- 请参阅`references/getting_started.md`以获取设置帮助
- 查看`polymarket_data/`目录下的输出文件
- 确保已安装以下依赖库：`pip install requests beautifulsoup4`