---
name: cyber-ir-playbook
description: 根据事件日志生成事件响应时间线及报告包。这些资料可用于记录从事件检测到恢复的全过程、跟踪各个处理阶段，并为相关利益方提供详细的事件总结。
---
# 网络事件响应手册（Cyber IR Playbook）

## 概述  
将事件信息转换为标准化的响应时间线及基于阶段的报告格式。

## 工作流程  
1. 收集带有时间戳的事件信息。  
2. 将事件分类为检测（Detection）、遏制（Containment）、清除（Eradication）、恢复（Recovery）或事件后期处理（Post-incident）等阶段。  
3. 构建有序的时间线，并总结当前阶段的完成情况。  
4. 生成适用于内部员工和高管的报告文件。  

## 使用配套资源  
- 运行 `scripts/ir_timeline_report.py` 以生成规范的时间线报告。  
- 阅读 `references/ir-phase-guide.md` 以获取阶段划分的指导信息。  

## 注意事项  
- 重点关注防御性的事件处理及事件后的经验总结。  
- 严禁提供任何用于攻击性的利用方法或指令。