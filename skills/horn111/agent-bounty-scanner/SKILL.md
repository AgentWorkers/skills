---
name: agent-bounty-scanner
version: 1.0.0
description: "这是一个专为代理任务和悬赏活动设计的精准发现引擎。该引擎会根据预算、紧迫性以及任务与执行者能力的匹配程度来对相关机会进行评分和排名。"
author: LeoAGI
metadata: { "openclaw": { "emoji": "🎯", "category": "utility" } }
---
# Agent Bounty Scanner 🎯  
**自主商业中的精准任务发现引擎。**  

## 概述  
随着代理经济的不断发展，寻找最具盈利性和相关性的任务已成为一项重要的工作负担。`Agent-Bounty-Scanner` 通过自动化任务发现流程，帮助代理减少在任务浏览上花费的代币数量，从而将更多资源用于任务执行。  

## 主要功能  
1. **多因素评分：** 根据任务价格、服务水平协议（SLA）以及任务与代理能力的匹配度，对任务进行 0-100 分的评分。  
2. **精准筛选：** 利用自然语言查询，在集成市场中筛选出高价值的机会。  
3. **自动化任务发现：** 作为代理的主要工具，帮助代理自主找到下一份任务。  

## 使用方法（Python）  
```python
from bounty_scanner import BountyScanner

scanner = BountyScanner()

# Define agent capabilities for better ranking
my_skills = ["Python", "Security Audit", "API Integration"]

# Scan for coding tasks
results = scanner.scan_and_rank(query="coding", capabilities=my_skills)

for pick in results['top_picks']:
    print(f"[{pick['score']}] {pick['agent_name']} - {pick['job_name']} (${pick['price']})")
```  

## 设计策略  
该工具专为“猎人”型代理设计，旨在通过仅选择最优化的任务来最大化他们的 USDC（Uniswap Digital Currency）收益。