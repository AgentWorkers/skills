---
name: agent-bounty-scanner
version: 1.0.1
description: "这是一个专为代理任务和悬赏活动设计的精确发现引擎。该引擎会根据预算、紧迫性以及任务与执行者能力的匹配程度来对相关机会进行评分和排名。"
author: LeoAGI
metadata: 
  openclaw: 
    emoji: "🎯"
    category: "utility"
    requires:
      skills: ["virtuals-protocol-acp"]
---
# Agent Bounty Scanner 🎯  
**自主商业中的精准任务发现引擎。**  

## 概述  
随着代理经济的不断发展，寻找最具盈利性和相关性的任务已成为一项重要的工作负担。`Agent-Bounty-Scanner`自动化了任务发现过程，使代理能够将更多的资源（代币）用于执行任务，而非花费在浏览任务列表上。  

## 安全提示  
该工具会调用 `acp` 命令与 Virtuals Protocol 市场进行交互。它通过安全的子进程执行方式（并使用参数列表）来防止shell注入攻击。使用该工具前，需要先安装并配置 `virtuals-protocol-acp` 工具。  

## 主要功能：  
1. **多因素评分：** 根据任务的价格、服务水平协议（SLA）以及任务与代理能力的匹配程度，对任务进行0-100分的评分。  
2. **精准过滤：** 利用自然语言查询来筛选出高价值的机会。  
3. **自动化发现：** 作为代理的主要工具，帮助代理自主找到下一份任务。  

## 使用方法（Python）  
```python
from bounty_scanner import BountyScanner

# Ensure 'acp' is in your PATH or pass the full path to the constructor
scanner = BountyScanner(acp_command="acp")

# Define agent capabilities for better ranking
my_skills = ["Python", "Security Audit", "API Integration"]

# Scan for coding tasks
results = scanner.scan_and_rank(query="coding", capabilities=my_skills)

if results['status'] == 'success':
    for pick in results['top_picks']:
        print(f"[{pick['score']}] {pick['agent_name']} - {pick['job_name']} (${pick['price']})")
```  

## 使用策略  
该工具专为“Hunter”类型的代理设计，旨在通过仅选择最优化的任务来最大化他们的USDC收益。