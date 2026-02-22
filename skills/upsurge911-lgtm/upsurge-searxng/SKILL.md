---
name: upsurge-searxng
description: >
  **适用于代理的私有情报雷达系统（Private Intelligence Radar for Agents）**  
  该系统有效解决了使用 Brave/Google API 时所面临的高成本和隐私泄露问题。它能够在本地聚合数据，实现“零泄露”（Zero-Leak）的目标，从而确保数据的绝对主权（absolute data sovereignty）。
author: Upsurge.ae
version: 1.4.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
---
# ![Upsurge](logo.jpg)  
# Upsurge.ae开发的OpenClaw专用搜索引擎SearXNG  

### 拯回您的数据——零成本、零泄露的企业级搜索解决方案  

**问题：** 常规的AI搜索工具（如Brave/Google）会将您的查询数据转化为竞争对手的产品训练资料。每一次搜索都会产生额外成本，并可能泄露您的商业机密。  

**现状：** 对于企业来说，采用AI工具是一个巨大的障碍——如果您的搜索引擎会因每次搜索而产生费用，那么您就无法建立一个安全的“作战室”（即一个用于收集和分析内部信息的独立环境）。  

**解决方案：** SearXNG是一款高速运行的**私有情报收集工具**，完全运行在您的Docker网络内部。它能让您的团队同时监控70多种搜索引擎的数据，而无需支付API费用，也无需担心数据泄露的风险。  

## ✨ 主要功能  
*   **专为代理优化设计的Markdown格式：** 专为数据采集而设计的Markdown格式，能有效减少数据解析错误，并将数据提取速度提升至原始片段的2倍。  
*   **时间维度过滤功能：** 支持按“天”、“月”和“年”进行筛选，确保团队关注的是实时市场动态而非过时的信息。  
*   **零搜索成本：** 全球范围内的无限次查询，无需支付每月的API费用或使用令牌。  
* **零数据泄露：** 您的战略性查询数据仅存储在本地Docker网络中，第三方广告网络和AI训练系统无法获取这些信息。  
* **汇总结果：** 可同时从Google、Bing、DuckDuckGo和Wikipedia等来源获取信息。  

## 🎯 使用场景  
*   **市场情报收集：** 在不引起竞争对手注意的情况下监控他们的动向。  
* **技术研究：** 通过`it`类别搜索相关文档和GitHub仓库。  
* **实时报告：** 使用“按天”筛选功能为CEO团队生成每日报告。  
* **数据主权保护：** 当公司法规禁止通过公共搜索API共享内部项目名称时，SearXNG是理想的选择。  

## 🛠 先决条件  
*   SearXNG需运行在`http://localhost:8080`（Docker环境）。  
* **主机上已安装Python 3。**  

## 🚀 使用方法  

```bash
# Broad Market Search
python3 search.py "AI adoption trends"

# Real-time News (Last 24 Hours)
python3 search.py "Market news" --time day --category news

# Technical Deep Dive
python3 search.py "OpenClaw API" --category it
```  

---  
*由Upsurge.ae专为CEO团队打造*