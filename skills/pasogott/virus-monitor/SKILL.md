---
name: virus-monitor
version: 0.1.0
description: 维也纳病毒监测系统（污水处理 + Sentinel）
author: ClaudeBot
tags: [health, vienna, monitoring, covid, influenza, rsv]
---

# 病毒监测工具

该工具整合了多个奥地利的病毒监测数据源：

## 数据来源

1. **国家废水监测系统** (abwassermonitoring.at)  
   - 每人每天的SARS-CoV-2病毒拷贝数  
   - 包括维也纳在内的各州数据  

2. **维也纳医科大学Sentinel系统** (viro.meduniwien.ac.at)  
   - 呼吸道病毒的阳性检出率  

3. **DINÖ（奥地利流感诊断网络）**  
   - 每周报告  

4. **AGES废水监测仪表盘** (abwasser.ages.at)  
   - SARS-CoV-2、流感、RSV病毒数据  
   - 全奥地利范围  

## 使用方法  

```bash
# Alle Daten als JSON
virus-monitor

# Nur bestimmte Quelle
virus-monitor --source abwasser
virus-monitor --source sentinel
virus-monitor --source ages
```  

## 输出结果  

```json
{
  "timestamp": "2026-01-09T00:37:00Z",
  "status": "erhöht",
  "sources": {
    "abwasser": { ... },
    "sentinel": { ... },
    "ages": { ... }
  },
  "summary": {
    "wien": {
      "sars_cov_2": "...",
      "influenza": "...",
      "rsv": "..."
    }
  }
}
```  

## 状态级别  

- `低`：正常的季节性活动  
- `中等`：活动水平升高，建议提高警惕  
- `高`：活动水平显著升高  
- `非常高`：病毒传播非常活跃  

## 所需依赖库/工具  

- `curl`：用于发送HTTP请求  
- `jq`：用于处理JSON数据  
- 标准的Unix工具（awk、grep、sed）  

## 注意事项  

- 废水监测数据存在约1-2周的延迟  
- Sentinel系统的数据每周更新一次（周五）  
- AGES仪表盘是一个基于Shiny技术的动态应用程序