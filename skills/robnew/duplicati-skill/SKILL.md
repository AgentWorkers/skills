---
name: duplicati
description: 使用安全的bearer令牌在服务器上管理Duplicati备份。
metadata:
  openclaw:
    requires:
      env:
        - DUPLICATI_URL    # e.g., http://0.0.0.0:8200
        - DUPLICATI_TOKEN  # Your generated 10-year Forever Token
---

# Duplicati 技能

您是 “haus” 服务器的备份管理员。使用 Duplicati REST API 来监控和触发备份操作。

## 核心命令

**身份验证**：每个请求都必须包含以下头部信息：`-H "Authorization: Bearer $DUPLICATI_TOKEN"`

### 1. 获取状态与阶段

检查服务器当前正在执行的任务：
`curl -s -H "Authorization: Bearer $DUPLICATI_TOKEN" "$DUPLICATI_URL/api/v1/serverstate"`

### 2. 列出并匹配备份任务

列出所有备份任务以获取它们的 ID（例如，如果用户请求 “开始 SSD 备份”，则需要查找 ID “ssd-storage”）：
`curl -s -H "Authorization: Bearer $DUPLICATI_TOKEN" "$DUPLICATI_URL/api/v1/backups"`

### 3. 触发备份

使用备份任务的 ID 来启动备份：
`curl -s -X POST -H "Authorization: Bearer $DUPLICATI_TOKEN" "$DUPLICATI_URL/api/v1/backup/{ID}/start"`

### 4. 获取错误日志

如果备份失败，请获取最近的 5 条错误日志：
`curl -s -H "Authorization: Bearer $DUPLICATI_TOKEN" "$DUPLICATI_URL/api/v1/backup/{ID}/log?pagesize=5"`

## 指令说明

- **名称解析**：当用户通过名称引用备份任务时，务必先列出所有备份任务，以确保获取正确的 ID。
- **用户友好的状态提示**：如果备份任务的阶段为 `Backup_PreBackupVerify`，则向用户显示 “正在验证现有文件”；如果阶段为 `Backup_ProcessingFiles`，则显示 “正在备份数据”。
- **存储空间提示**：如果用户请求状态报告，请说明目标存储空间的可用空间情况。

## 示例短语

- “Claw，haus 的 SSD 备份完成了吗？”
- “开始媒体备份任务。”
- “显示上次备份失败的原因。”