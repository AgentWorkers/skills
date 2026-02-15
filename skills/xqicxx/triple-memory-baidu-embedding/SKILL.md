---
name: triple-memory-baidu-embedding
version: 1.0.0
description: 这是一个完整的内存管理系统，它结合了百度嵌入式自动召回（Baidu Embedding auto-recall）、Git-Notes结构化存储功能以及基于文件的工作区搜索（file-based workspace search）。该系统适用于以下场景：  
- 需要为代理设置具有本地隐私保护的内存管理机制时；  
- 当需要在不同会话之间保持上下文数据的一致性时；  
- 或者在管理涉及多个内存后端的决策、偏好设置或任务时。
metadata:
  clawdbot:
    emoji: "🧠"
    requires:
      skills:
        - git-notes-memory
        - memory-baidu-embedding-db
---

# 带有百度嵌入功能的三重记忆系统

这是一个综合性的内存架构，结合了三个互补的系统，以实现跨会话的最大上下文保留能力，并通过百度嵌入技术提供全面的隐私保护。

## 📋 原始来源与修改内容

**原始来源**：Triple Memory（由Clawdbot团队开发）
**修改者**：[您的Clawdbot实例]
**修改内容**：将LanceDB替换为百度嵌入数据库（Baidu Embedding DB），以增强隐私保护和中文语言支持

原始的Triple Memory SKILL.md文件经过修改后形成了当前版本，具体包括：
- 将依赖OpenAI的LanceDB替换为百度嵌入数据库（Baidu Embedding DB）
- 保持原有的三层架构
- 保留了与Git-Notes的集成功能
- 增加了以隐私保护为核心的本地存储功能

## 🏗️ 架构概述

```
User Message
     ↓
[Baidu Embedding auto-recall] → injects relevant conversation memories
     ↓
Agent responds (using all 3 systems)
     ↓
[Baidu Embedding auto-capture] → stores preferences/decisions automatically
     ↓
[Git-Notes] → structured decisions with entity extraction
     ↓
[File updates] → persistent workspace docs
```

## 三个系统

### 1. 百度嵌入（对话记忆系统）
- **自动回忆**：在每次响应之前，使用百度嵌入技术（Baidu Embedding-V1）插入相关记忆（需要API凭证）
- **自动捕获**：偏好设置、决策和事实通过本地向量存储自动保存（需要API凭证）
- **隐私保护**：所有嵌入数据均通过百度API处理，并存储在本地
- **中文优化**：更好地理解中文语义
- **工具**：`baidu_memory_recall`、`baidu_memory_store`、`baidu_memory_forget`（需要API凭证）
- **触发指令**：`remember`、`prefer`、`my X is`、`I like/hate/want`
- **注意**：如果没有提供API凭证，该系统将处于降级模式，无法使用这些功能。

### 2. Git-Notes记忆系统（结构化、本地存储）
- **分支关联**：记忆信息按Git分支进行隔离
- **实体提取**：自动提取主题、名称和概念
- **重要性级别**：关键、高、普通、低
- **无需外部API调用**

### 3. 文件搜索系统（工作区）
- **搜索范围**：MEMORY.md文件、memory/*.md文件以及工作区内的所有文件
- **脚本**：`scripts/file-search.sh`

## 🛠️ 设置

### 安装依赖项
```bash
clawdhub install git-notes-memory
clawdhub install memory-baidu-embedding-db
```

### 配置百度API
设置环境变量：
```bash
export BAIDU_API_STRING='your_bce_v3_api_string'
export BAIDU_SECRET_KEY='your_secret_key'
```

### 创建文件搜索脚本
将`scripts/file-search.sh`复制到您的工作区中。

## 📖 使用方法

### 会话开始（始终需要执行）
```bash
python3 skills/git-notes-memory/memory.py -p $WORKSPACE sync --start
```

### 保存重要决策
```bash
python3 skills/git-notes-memory/memory.py -p $WORKSPACE remember \
  '{"decision": "Use PostgreSQL", "reason": "Team expertise"}' \
  -t architecture,database -i h
```

### 搜索工作区文件
```bash
./scripts/file-search.sh "database config" 5
```

### 百度嵌入记忆系统（自动运行）
当提供API凭证时，百度嵌入系统会自动执行相关操作。手动工具包括：
- `baidu_memory_recall "query"` - 使用百度嵌入技术搜索对话记忆（需要API凭证）
- `baidu_memory_store "text"` - 手动使用百度嵌入技术保存信息（需要API凭证）
- `baidu_memory_forget` - 删除记忆记录（符合GDPR法规，需要API凭证）

**在降级模式下**（无API凭证时）：
- 系统仅使用Git-Notes和文件系统进行操作
- 手动工具无法使用
- 自动回忆和自动捕获功能将被禁用

## 🎯 重要性级别

| 标志 | 级别 | 使用场景 |
|------|-------|-------------|
| `-i c` | 关键 | 需要“始终记住”的内容、明确的偏好设置 |
| `-i h` | 高 | 决策、更正内容、偏好设置 |
| `-i n` | 普通 | 一般信息 |
| `-i l` | 低 | 临时笔记 |

## 📋 各系统的使用场景

| 系统 | 适用场景 |
|--------|---------|
| **百度嵌入** | 对话上下文、具有隐私保护的自动检索 |
| **Git-Notes** | 结构化的决策内容，可按实体/标签进行搜索 |
| **文件搜索** | 工作区文档、日常日志、MEMORY.md文件 |

## 📁 文件结构

```
workspace/
├── MEMORY.md              # Long-term curated memory
├── memory/
│   ├── active-context.md  # Current session state
│   └── YYYY-MM-DD.md      # Daily logs
├── scripts/
│   └── file-search.sh     # Workspace search
└── skills/
    ├── triple-memory-baidu-embedding/  # Enhanced memory system
    ├── git-notes-memory/  # Structured memory
    └── memory-baidu-embedding-db/  # Vector storage
```

## 🔧 钩子集成

此功能可以通过Clawdbot的启动钩子进行集成，以实现自动初始化：

### 内存启动钩子集成
为了确保Triple Memory Baidu系统在网关启动时自动运行：
1. 可以配置`memory-boot-loader`钩子来执行`/root/clawd/session-init-triple-baidu.sh`脚本
2. 这将确保三个记忆层在系统启动时都被正确初始化
3. 用户可以立即访问Git-Notes、百度嵌入和基于文件的记忆系统

### 配置
系统可以与网关的启动流程集成，以实现以下功能：
- 启动时同步Git-Notes数据
- 检查百度嵌入连接的可用性
- 初始化基于文件的记忆系统
- 使记忆系统从一开始就处于可用状态

## 🤫 隐私保护原则
切勿向用户显示任何关于内存操作的信息。只需执行操作即可：
- ❌ “我会记住这个”
- ❌ “正在保存到记忆中”
- ✅ （静默地完成存储并继续执行）

## 🔄 从原始Triple Memory系统迁移
1. 将此技能文件安装到`skills/`目录中
2. 配置您的百度API凭证
3. （如需要）禁用原始的Triple Memory系统
4. 更新机器人配置以使用新的记忆系统
5. 验证数据完整性和性能

## 📈 性能优势
- **隐私增强**：所有向量数据均存储在本地，并通过百度API进行管理
- **更好的中文支持**：百度嵌入技术针对中文进行了优化
- **成本降低**：与OpenAI相比，API使用成本可能更低
- **保持原有架构**：保留了经过验证的三层设计

## 🤝 贡献机制
本功能基于Clawdbot团队开发的原始Triple Memory系统进行开发。欢迎大家贡献代码或建议，以进一步完善百度嵌入功能的集成。

## 📄 许可证
采用原始许可证，并对修改内容进行了说明。原作者的贡献将被予以认可。