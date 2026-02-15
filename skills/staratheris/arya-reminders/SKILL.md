---
name: arya-reminders
description: 自然语言提醒器（波哥大）：创建安全的定时任务，并将提醒内容记录到 Markdown 文档中（可选也可记录到 Sheets 表格中）。
metadata:
  openclaw:
    emoji: "⏰"
    requires:
      bins: ["bash", "python3"]
---

# Arya Reminders  
专为Jaider设计的OpenClaw自然语言提醒工具  

## 功能介绍  
- 能够以西班牙语（及常见格式）解析相对和绝对的日期/时间；  
- 默认使用时区“America/Bogota”；  
- 支持创建一次性（one-shot）的提醒任务（类似于定时任务）；  
- 所有提醒信息都会被记录在`memory/reminders.md`文件中；  
- （未来可选功能）支持将提醒信息同步到Google Sheets。  

## 使用方法（对话式指令）  
示例：  
- “提醒我明天下午3点支付电费”  
- “45分钟后提醒我检查烤箱的状态”  
- “今天下午5:30提醒我给妈妈打电话”  
- “周五上午9点提醒我完成手工作业”  

## 命令操作（手动执行）  
### 创建一次性提醒  
```bash
bash skills/arya-reminders/create-reminder.sh "Mensaje" "Cuándo"
```  

### 查看提醒记录  
```bash
cat memory/reminders.md
```  

## 注意事项：  
- 该工具无需依赖外部API；  
- 使用Gateway自带的`cron`工具来执行提醒任务（请勿硬编码外部链接或ID）。