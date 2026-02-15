# 代理内存套件（Agent Memory Kit）

**类型：** 实践工具 / 开发框架  
**依赖项：** 无（仅依赖Markdown格式）  

---

## 说明  
这是一个专为AI代理设计的内存管理系统。通过将内存划分为三个层次——**情景记忆（记录发生了什么）、语义记忆（存储已知信息）和程序记忆（存储操作方法）**——来防止“忘记如何执行某项任务”的问题。  

## 安装  
```bash
# Create memory folder structure
mkdir -p memory/procedures

# Copy templates
cp templates/ARCHITECTURE.md memory/
cp templates/feedback.md memory/
cp templates/procedure-template.md memory/procedures/
```  

## 使用方法  
1. 阅读 `README.md` 以了解系统详细信息。  
2. 将内存加载功能添加到代理的唤醒脚本（`AGENTS.md`）中。  
3. 在记录事件、创建操作步骤或跟踪反馈时使用提供的模板。  

## 文件列表  
| 文件名 | 用途 |  
|------|---------|  
| `README.md` | 完整的使用说明文档 |  
| `templates/ARCHITECTURE.md` | 内存系统概述（可复制到相关目录） |  
| `templates/feedback.md` | 成功/失败事件跟踪模板 |  
| `templates/procedure-template.md` | 操作步骤文档模板 |  
| `templates/daily-template.md` | 日志记录模板 |  
| `templates/compaction-survival.md` | **新功能：** 预压缩数据清理指南 |  
| `templates/context-snapshot-template.md` | **新功能：** 快速上下文保存模板 |  
| `helpers/check-compaction.sh` | **新功能：** 令牌使用量检查工具 |  

## 关键概念  
- **情景记忆（Episodic Memory）**：记录每日发生的事件。  
- **语义记忆（Semantic Memory）**：系统整理后的知识库（存储在 `MEMORY.md` 文件中）。  
- **程序记忆（Procedural Memory）**：存储具体的操作方法。  
- **反馈循环（Feedback Loops）**：通过分析成功与失败的经验来提升代理性能。  

## 使用原则  
**务必记录操作步骤（HOW），而不仅仅是事件本身（WHAT）**。未来的你需要这些具体的操作指南。