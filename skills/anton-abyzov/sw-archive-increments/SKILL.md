---
name: archive-increments
description: 智能增量归档专家：该工具能够分析文件的创建时间、状态及使用频率，从而自动推荐哪些文件应该被归档。适用于工作区中文件数量过多、需要清理已完成的工作内容或整理归档文件夹的场景。该工具遵循“10-10-10”工作区组织原则（即每个文件夹中最多存放10个文件，每个文件最多包含10个子文件夹，每个子文件夹最多存放10个文件）。
---

# 增量归档管理器

该工具擅长通过智能归档机制，保持 `.specweave/increments/` 文件夹的整洁与有序。

## 核心知识

### 归档原则

**10-10-10 规则**：
- **10 个活跃增量**：保留最近 10 个活跃的增量
- **10 天**：将超过 10 天未使用的增量归档
- **10 秒**：归档操作应在 10 秒内完成

### 归档结构

```
.specweave/increments/
├── 0023-0032 (Active)          ← Last 10 increments
├── _archive/                   ← Completed/old increments
│   ├── 0001-0022              ← Historical increments
│   └── 0029                   ← Abandoned experiments
└── _abandoned/                 ← Failed/obsolete increments
```

### 智能检测规则

#### **永不归档**：
- **活跃增量**（状态：活跃）
- **暂停的增量**（状态：暂停）——可能恢复
- **最近的增量**（默认保留最近 10 个）
- **存在未解决的 GitHub/JIRA/ADO 问题的增量**
- **存在未提交更改的增量**

#### **必须归档**：
- **60 天前完成的增量**
- **30 天内无活动的增量**（且状态为“完成”）
- **被新版本取代的增量**
- **实验失败的增量**（经确认后归档）

#### **智能分组**：
- **版本分组**：在 v0.8.0 发布后，归档所有 v0.7.x 版本的增量
- **功能分组**：将相关增量归档在一起
- **基于时间**：按季度/月份进行归档

## 使用模式

### 保持工作区整洁
```bash
# Interactive archiving - prompts for confirmation
/sw:archive-increments

# Keep only last 5 increments
/sw:archive-increments --keep-last 5

# Archive all completed increments
/sw:archive-increments --archive-completed
```

### 准备发布
```bash
# Archive all pre-release increments
/sw:archive-increments --pattern "v0.7"

# Archive by date range
/sw:archive-increments --older-than 30d
```

### 从归档中恢复
```bash
# List archived increments
/sw:archive-increments --list-archived

# Restore specific increment
/sw:archive-increments --restore 0015
```

## 配置

### 默认设置
```json
{
  "archiving": {
    "keepLast": 10,              // Keep last 10 increments
    "autoArchive": false,        // Manual by default
    "archiveAfterDays": 60,      // Archive after 60 days
    "preserveActive": true,      // Never archive active
    "archiveCompleted": false    // Manual control
  }
}
```

### 强制清理
```json
{
  "archiving": {
    "keepLast": 5,               // Minimal workspace
    "autoArchive": true,         // Auto-archive on completion
    "archiveAfterDays": 14,      // Archive after 2 weeks
    "archiveCompleted": true     // Auto-archive completed
  }
}
```

## 归档统计

### 当前状态分析
在处理归档任务时，我会分析以下内容：
- 活跃增量的数量
- 最旧活跃增量的年龄
- 增量文件夹的总大小
- 完成增量的数量
- 外部同步状态

### 建议
根据分析结果，我会给出以下建议：
- **空间不足**（活跃增量超过 20 个）：归档除最后一个之外的所有增量
- **过时**（许多增量超过 30 天）：按时间顺序归档
- **发布后**：归档之前的版本
- **文件过大**（大于 100MB）：归档最大的已完成增量

## 安全特性

### 归档前的检查
1. **元数据验证**：检查增量状态
2. **外部同步**：确认没有未解决的问题
3. **Git 状态**：检查是否存在未提交的更改
4. **依赖关系**：确认增量是否被其他活跃增量引用
5. **用户确认**：显示即将被归档的增量内容

### 归档操作
- **原子性操作**：使用 `fs.move` 并启用覆盖保护
- **保持结构**：保留完整的增量结构
- **更新引用**：修复活文档中的链接
- **可逆性**：便于从归档中恢复数据
- **审计追踪**：记录所有归档操作

## 智能建议

### 何时归档
- **重大版本发布后**：归档所有预发布阶段的增量
- **季度清理**：归档超过 3 个月的增量
- **项目阶段转换前**：归档之前的工作成果
- **磁盘空间不足**：归档最大的已完成增量

### 归档模式
- **按版本**：`--pattern "v0.7"`（所有 v0.7.x 版本的增量）
- **按功能**：`--pattern "auth|login"`（与身份验证相关的增量）
- **按时间**：`--older-than 30d`（按时间顺序）
- **按状态**：`--archive-completed`（所有已完成的增量）

## 集成点

### 状态显示
- 以 “23-32 (10 active, 22 archived)” 的格式显示状态
- 当活跃增量超过 15 个时发出警告
- 在适当情况下建议进行归档

### 增量相关命令
- `/sw:done` 可触发自动归档
- `/sw:status` 显示归档统计信息
- `/sw:next` 会考虑已归档的增量

### 活文档
- 归档操作会保留对活文档的引用
- 归档后更新活文档中的链接
- 归档情况会记录在文档统计中

## 最佳实践
1. **定期清理**：每月或每次发布后进行归档
2. **保留最新数据**：始终保留最近 5-10 个增量
3. **保护活跃增量**：切勿强制归档正在进行的任务
4. **分组归档**：将相关功能模块的增量归档在一起
5. **记录归档原因**：添加归档说明以提供上下文信息

## 快速参考

```bash
# Archive old increments
/sw:archive-increments --older-than 30d

# Keep workspace minimal
/sw:archive-increments --keep-last 5

# Archive after release
/sw:archive-increments --pattern "pre-release"

# Restore for reference
/sw:archive-increments --restore 0015

# Check archive stats
/sw:archive-increments --stats
```