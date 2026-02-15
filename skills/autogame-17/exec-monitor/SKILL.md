# Exec Monitor

**版本：** 1.0.0  
**作者：** OpenClaw Evolver  
**日期：** 2026-02-11  

## 描述  
这是一个轻量级的工具，用于监控和记录 `exec` 工具的使用情况。它是根据 `high_tool_usage:exec` 信号创建的，旨在帮助更好地了解自动化需求及潜在的瓶颈。  

## 使用方法  
```bash
node skills/exec-monitor/index.js "<command>" "<optional_context>"
```  

## 日志记录  
日志文件存储在 `logs/exec_usage.jsonl` 中。