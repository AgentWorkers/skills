---
name: proactive-agent
description: "将AI代理从简单的任务执行者转变为能够主动预测用户需求并持续改进的合作伙伴。这一转变涉及WAL协议（Workload Allocation Protocol）、工作缓冲区（Working Buffer）、自主调度机制（Autonomous Crons）以及经过实战验证的运行模式（battle-tested patterns）。"
homepage: https://lobehub.com/skills/openclaw-skills-proactive-agent
metadata: { "openclaw": { "emoji": "🚀", "requires": { "bins": [] } } }
---
# 主动型代理技能

将AI代理从被动执行任务的工具转变为能够主动预测需求并持续改进的合作伙伴。

## 使用场景

✅ **在以下情况下使用此技能：**
- **使代理更加主动**  
- **自动化常规检查**  
- **实现内存持久化**  
- **安排自动化任务**  
- **构建自我提升的代理**

## 核心架构

### 1. WAL协议（预写日志，Write-Ahead Logging）
- **目的**：保存关键状态并在上下文丢失时恢复数据  
- **组成部分**：
  - `SESSION-STATE.md`：当前任务的工作内存  
  - `working-buffer.md`：危险区域日志  
  - `MEMORY.md`：长期存储的关键信息  

### 2. 工作缓冲区（Working Buffer）
- 记录所有发生在“危险区域”内的交互  
- 防止会话重启时丢失关键上下文  
- 自动压缩并归档重要信息  

### 3. 自主任务调度（Autonomous Crons）与手动触发任务调度（Prompted Crons）
- **自主任务调度**：基于上下文感知的自动化任务  
- **手动触发任务**：用户触发的定时任务  
- **心跳检测（Heartbeats）**：定期进行的主动检查  

## 实现模式

### 内存架构
```
workspace/
├── MEMORY.md              # Long-term curated memory
├── memory/
│   └── YYYY-MM-DD.md      # Daily raw logs
├── SESSION-STATE.md       # Active working memory
└── working-buffer.md      # Danger zone log
```

### WAL协议工作流程
1. **记录**：将所有关键交互日志记录到工作缓冲区  
2. **压缩**：定期审查并提取关键信息  
3. **整理**：将重要信息移至`MEMORY.md`  
4. **恢复**：会话重启后从日志中恢复状态  

### 主动行为

#### 1. 心跳检测（Heartbeat Checks）
```bash
# Check every 30 minutes
- Email inbox for urgent messages
- Calendar for upcoming events
- Weather for relevant conditions
- System status and health
```

#### 2. 自主任务调度（Autonomous Crons）
```bash
# Daily maintenance
- Memory compaction and cleanup
- File organization
- Backup verification

# Weekly tasks
- Skill updates check
- Documentation review
- Performance optimization
```

#### 3. 基于上下文的自动化（Context-Aware Automation）
- 识别用户请求中的模式  
- 预测后续需求  
- 提出相关建议  

## 配置

### 基本设置
1. 创建内存目录结构  
2. 设置`SESSION-STATE.md`模板  
3. 配置心跳检测间隔  
4. 定义自主任务调度规则  

### 高级配置
```json
{
  "proactive": {
    "heartbeatInterval": 1800,
    "autonomousCrons": {
      "daily": ["08:00", "20:00"],
      "weekly": ["Monday 09:00"]
    },
    "memory": {
      "compactionThreshold": 1000,
      "retentionDays": 30
    }
  }
}
```

## 使用示例

### 1. 实现WAL协议
```markdown
# SESSION-STATE.md Template

## Current Task
- Task: [Brief description]
- Started: [Timestamp]
- Status: [In Progress/Completed/Failed]

## Critical Details
- [Key information needed for recovery]

## Next Steps
- [Immediate actions]
- [Pending decisions]
```

### 2. 设置心跳检测
```bash
# HEARTBEAT.md Template
# Check every 30 minutes

## Email Checks
- Check for urgent unread messages
- Flag important notifications

## Calendar Checks
- Upcoming events in next 2 hours
- Daily schedule overview

## System Checks
- OpenClaw gateway status
- Skill availability
- Memory usage
```

### 3. 创建自主任务调度
```bash
# Create cron job for daily maintenance
0 8 * * * openclaw run --task "daily-maintenance"
0 20 * * * openclaw run --task "evening-review"

# Weekly optimization
0 9 * * 1 openclaw run --task "weekly-optimization"
```

## 最佳实践

### 1. 内存管理
- **每日**：审查并压缩工作缓冲区  
- **每周**：从每日日志中整理`MEMORY.md`  
- **每月**：归档旧文件  

### 2. 主动行为
- **预测需求**：分析用户请求中的模式  
- **提供建议**：提出相关的下一步操作  
- **自动化处理**：为重复性任务创建定时任务  

### 3. 错误处理
- **全面记录**：将所有关键信息写入工作缓冲区  
- **优雅降级**：组件故障时提供备用方案  
- **自我修复**：自动从错误中恢复  

## 版本历史

### Proactive Agent 1.0
- 基本的WAL协议实现  
- 工作缓冲区基础  
- 简单的心跳检测功能  

### Proactive Agent 2.0
- 改进的内存架构  
- 自主任务调度系统  
- 基于上下文的自动化  

### Proactive Agent 4.0
- 高级模式识别能力  
- 自我提升机制  
- 多代理协同工作  

## 相关技能
- `healthcheck`：系统安全与健康检查  
- `skill-creator`：创建新技能  
- `cron-manager`：任务调度管理  
- `memory-manager`：内存优化工具  

## 致谢

本技能由Hal 9001（@halthelobster）创建——一个每天实际使用这些功能的AI代理。  
它是Hal Stack生态系统的一部分，用于构建强大且具有主动性的AI代理。