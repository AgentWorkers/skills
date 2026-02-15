---
name: alpha-finder
description: **Market Oracle：用于预测市场情报的工具**  
该工具基于 Polymarket 和 Kalshi 的技术，提供概率评估、市场情绪分析以及套利机会识别功能。适用于用户需要研究预测市场、分析投注赔率或发现市场效率低下的场景。  
使用费用为每次请求 0.03 美元（USDC），通过 Base 网络上的 x402 协议进行支付。
---

# Alpha Finder（市场预测工具）

利用基于AI的市场情报，在Polymarket、Kalshi以及传统数据源中寻找投资机会。

## 配置

私钥必须通过以下方式之一获取：

**选项1：环境变量**  
```bash
export X402_PRIVATE_KEY="0x..."
```

**选项2：配置文件（推荐）**  
脚本会依次在以下位置查找`x402-config.json`文件：  
1. 当前目录：`./x402-config.json`  
2. 主目录：`~/.x402-config.json` （推荐）  
3. 工作目录：`$PWD/x402-config.json`  

请创建配置文件：  
```json
{
  "private_key": "0x1234567890abcdef..."
}
```

**示例（适用于所有用户的主目录配置）：**  
```bash
echo '{"private_key": "0x..."}' > ~/.x402-config.json
```

## 使用方法

运行市场研究脚本，并输入关于预测市场或事件的查询：  
```bash
scripts/analyze.sh "<market query>"
```

该脚本的功能包括：  
- 执行市场情报分析并处理支付请求  
- 每次请求费用为0.03美元（基础网络费用）  
- 搜索Web、GitHub、Reddit和X平台以获取全面分析结果  
- 返回经AI处理的市场洞察和概率评估  

## 示例  

**用户1：** “比特币达到10万美元的概率是多少？”  
```bash
scripts/analyze.sh "Bitcoin 100k prediction market odds"
```

**用户2：** “在选举市场中寻找套利机会。”  
```bash
scripts/analyze.sh "2024 election prediction market arbitrage"
```

**用户3：** “分析Polymarket上关于AI发展的预测结果。”  
```bash
scripts/analyze.sh "Polymarket AI development predictions"
```

**用户4：** “市场对气候政策结果的看法如何？”  
```bash
scripts/analyze.sh "climate policy prediction markets Kalshi Polymarket"
```

## 主要功能：  
- **Polymarket研究**：事件分析与赔率追踪  
- **Kalshi市场分析**：受监管的预测市场洞察  
- **多源情报收集**：搜索Web、GitHub、Reddit和X平台  
- **概率评估**：基于AI的市场情绪分析  
- **套利机会识别**：发现市场中的价格异常  
- **事件深度研究**：针对特定预测市场事件进行深入分析  
- **历史数据对比**：将当前赔率与历史数据对比  

## 数据来源**  
该工具自动搜索以下数据：  
- Polymarket上的事件和赔率信息  
- Kalshi平台的受监管预测市场  
- Reddit上的讨论和用户情绪  
- X/Twitter上的市场评论  
- GitHub仓库（针对与技术相关的预测内容）  
- Web上的新闻和分析资料  

## 错误处理：  
- **“支付失败：USDC余额不足”** → 通知用户为钱包充值USDC  
- **“X402私钥未配置”** → 指导用户配置私钥（见“配置”部分）  
- **超时错误**：API有5分钟的超时限制；复杂研究可能需要更多时间  

## 使用场景：  
- **交易**：发现价格异常的市场和套利机会  
- **研究**：分析特定事件的市场情绪  
- **尽职调查**：在投注前验证市场概率  
- **投资组合管理**：追踪预测市场中的持仓情况  
- **新闻分析**：了解事件对市场赔率的影响