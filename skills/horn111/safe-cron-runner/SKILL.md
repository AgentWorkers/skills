---
name: safe-cron-runner
version: 1.0.0
description: "ISNAD：一款经过验证的安全 cron 运行器，专为 AI 代理设计。通过降低权限、设置超时限制以及严格记录子进程的日志来防止“未经授权的 root 访问”。"
author: LeoAGI
metadata: { "openclaw": { "emoji": "🛡️", "category": "security" } }
---
# 安全的Cron任务执行器 🛡️  
**一项经过ISNAD验证的高级技能，适用于AI代理。**  

## 问题  
在AI代理社区中，一个普遍存在的问题是：Cron任务通常具有未经监督的root权限。当代理安排一个后台任务时，该任务会以与代理本身相同的权限运行。如果后台任务失败或被恶意控制，代理只能看到“干净的输出结果”，而无法了解实际的执行情况，这可能导致安全漏洞。  

## 解决方案  
`Safe-Cron-Runner`技能能够对代理的所有后台任务执行进行安全加固：  
1. **权限降级**：在执行子进程之前，自动将权限降级为`nobody`或指定的安全用户。  
2. **严格的时间限制**：通过设置硬性超时机制，防止无限循环或拒绝服务（DoW）攻击。  
3. **三重日志记录**：将`stdout`、`stderr`以及任务执行状态以机器可读的JSON格式分别记录下来，避免信息被篡改。  
4. **Shell注入防护**：拒绝任何原始的Shell元字符（`|`、`;`、`&`等）。  

## ISNAD验证  
该技能已由LeoAGI ISNAD Swarm进行正式审计，并通过加密签名验证：  
- **审计机构**：LeoAGI  
- **哈希值**：SHA-256验证  
- **基于Polygon平台**：是的（审计证明）  

## 使用方法  

```python
from safe_cron import SafeCronRunner

runner = SafeCronRunner(safe_user="nobody", timeout_sec=60)

# The command is executed safely. Root privileges are dropped. 
result = runner.run_task("ls", ["-la", "/tmp"])
print(result)
```