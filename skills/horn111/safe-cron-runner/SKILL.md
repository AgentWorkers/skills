---
name: safe-cron-runner
version: 1.0.2
description: "通过降级权限并设置超时机制，安全地执行后台任务。该过程使用了 ISNAD 签名的清单文件（manifest）。"
author: LeoAGI
metadata: { "openclaw": { "emoji": "🛡️", "category": "security" } }
---
# 安全的 Cron 运行器 🛡️  
**专为 AI 代理设计的安全后台任务执行器。**  

## 概述  
该工具负责执行后台任务，确保自主代理不会意外地（或恶意地）执行耗时较长或需要高权限的命令。  

## 主要防护机制：  
1. **权限降级：** 在执行子进程之前，自动将 root 权限降级为 `nobody`。  
2. **严格的时间限制：** 实施硬性超时机制，以防止无限循环或资源耗尽。  
3. **Shell 注入防护：** 采用基于列表的命令执行方式（不使用 Shell），有效抵御常见的 Shell 注入攻击。  
4. **透明的日志记录：** 分别记录 `stdout`、`stderr` 和执行状态，便于审计。  

## ISNAD 签名  
该工具包含一个 ISNAD 文档（`isnad_manifest.json`），用于验证版本的完整性。  

## 使用方法  

```python
from safe_cron import SafeCronRunner

runner = SafeCronRunner(safe_user="nobody", timeout_sec=60)

# Execute command as a list for safety
result = runner.run_task(["ls", "-la", "/tmp"])
print(result)
```