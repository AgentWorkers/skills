---
name: memory-hygiene
description: 审计、清理并优化 Clawdbot 的向量内存（LanceDB）。当内存因大量无用数据而膨胀，或者由于不必要的自动召回操作导致令牌使用量过高时，可以使用此方法；同时，也可以用于设置内存维护的自动化流程。
homepage: https://github.com/xdylanbaker/memory-hygiene
---

# 内存管理

保持向量内存的简洁性，防止因垃圾内存而造成资源浪费。

## 快速命令

**审计：** 检查内存中的内容  
```
memory_recall query="*" limit=50
```

**清除：** 清空所有向量内存  
```bash
rm -rf ~/.clawdbot/memory/lancedb/
```  
然后重启网关：`clawdbot gateway restart`  

**重新填充数据：** 清除内存后，从 `MEMORY.md` 文件中读取关键信息并重新存储  
```
memory_store text="<fact>" category="preference|fact|decision" importance=0.9
```

## 配置：禁用自动捕获功能  

自动捕获功能（`autoCapture: true`）是产生垃圾数据的主要来源。请禁用该功能：  
```json
{
  "plugins": {
    "entries": {
      "memory-lancedb": {
        "config": {
          "autoCapture": false,
          "autoRecall": true
        }
      }
    }
  }
}
```  
使用 `gateway action=config.patch` 来应用更改。  

## 应该存储的内容（有意为之）  

✅ 应该存储的内容：  
- 用户偏好设置（工具、工作流程、沟通方式）  
- 关键决策（项目选择、架构设计）  
- 重要信息（账户信息、凭证位置、联系人）  
- 经验教训  

❌ 绝对不要存储的内容：  
- 心跳状态（如 “HEARTBEAT_OK”、“无新消息”）  
- 短暂性信息（当前时间、临时状态）  
- 原始消息日志（已保存在文件中）  
- OAuth URL 或令牌  

## 每月维护任务  

设置每月一次的清除和重新填充数据任务：  
```
cron action=add job={
  "name": "memory-maintenance",
  "schedule": "0 4 1 * *",
  "text": "Monthly memory maintenance: 1) Wipe ~/.clawdbot/memory/lancedb/ 2) Parse MEMORY.md 3) Store key facts to fresh LanceDB 4) Report completion"
}
```  

## 存储指南  

使用 `memory_store` 时，请遵循以下原则：  
- 保持文本简洁（少于 100 个单词）  
- 为重要信息设置合适的分类等级（0.7–1.0）  
- 每条内存记录只记录一个概念或信息点