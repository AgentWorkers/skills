---
name: memory-manager
description: 自动会话记录和内存管理功能，适用于基础设施、项目和工具。请在涉及服务器配置更改、服务更新、部署操作、定时任务（cron jobs）、代码仓库（repositories）、API接口、集成设置或凭证管理的会话结束时使用该功能。这能够确保文档的完整性，同时避免因冗余信息而导致的文档臃肿。
---
# 内存管理器

智能的会话结束内存管理功能：能够自动捕获基础设施、项目和工具的重要变更信息，同时过滤掉无关的细节。

## 该功能触发条件

在会话结束时执行，当聊天内容包含以下关键词时：
- **基础设施**：服务器、部署环境、服务、systemd、nginx、docker、数据库
- **项目**：代码仓库、github、功能模块、定时任务（cron）、API接口
- **工具**：集成方案、凭证信息、API密钥、配置设置

## 保存的内容

### 日志（每日必保存）
文件名：`memory/YYYY-MM-DD.md`

**保存内容：**
- 新增或变更的服务/服务器
- 项目部署或重要功能更新
- 定时任务的更新
- 基础设施的修复或迁移
- 重要的错误及其解决方法
- 配置变更

**不保存的内容：**
- 聊天记录
- 调试步骤（除非这些步骤揭示了重要的信息）
- 临时性的测试结果
- 微小的代码修改

### MEMORY.md（仅保存结构性的变更）
**保存内容：**
- 新项目（包含基本信息）
- 工作流程或架构的变更
- 重要的设计决策
- 被弃用或已归档的系统

**不保存的内容：**
- 常规性的更新
- 临时性的变更
- 已经记录在日志中的详细信息

### TOOLS.md（仅保存新的工具/凭证信息）
**保存内容：**
- 新的API密钥或凭证信息
- 新的服务器（IP地址、SSH配置、用途）
- 新的集成方案

### PROJECTS.md（项目生命周期的变更）
详细内容请参考 [PROJECTS.md Guide](references/projects-guide.md)。

**保存内容：**
- 新项目的启动
- 项目状态的变化（从原型阶段到生产环境、从活跃状态到归档状态）
- 重要的技术栈变更
- URL地址或部署位置的变更

## 处理流程
1. **扫描会话内容**，查找与基础设施、项目或工具相关的关键词。
2. **根据上述标准进行筛选**。
3. **生成包含时间戳和结构化摘要的日志文件**。
4. **仅当存在结构性变更时，更新 MEMORY.md**。
5. **仅当有新的凭证信息、服务器信息或集成方案时，更新 TOOLS.md**。
6. **仅当项目生命周期发生变更时，更新 PROJECTS.md**。

## 日志格式

```markdown
## HH:MM UTC — Brief Title

**What happened:** 1-2 sentence summary

**Changes:**
- Service X deployed to server Y
- Cron job Z updated with new logic
- Project A: feature B shipped

**Impact:** (only if significant)
- Performance improved 2x
- Fixed critical bug affecting users
```

## MEMORY.md 的更新指南

仅添加需要在多个会话中长期保留的信息：
- 新的、永久性的服务
- 重要的架构决策
- 被弃用的技术或开发模式

每条记录的长度请控制在 **5行以内**。详细信息请记录在日志文件中。

## 参考资料
- [PROJECTS.md Guide](references/projects-guide.md) - 数据结构及更新标准