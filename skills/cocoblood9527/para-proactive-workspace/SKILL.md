---
name: para-proactive-workspace
description: "这是一个适用于生产环境的工作空间模板，它结合了Tiago Forte提出的PARA方法（包括项目、区域、资源和档案管理）以及Proactive Agent架构，用于文件组织、文件夹结构优化、提升工作效率、知识管理以及实现AI代理的记忆持久化功能。该模板专为OpenClaw平台设计，包含19个以上的模板和3份可视化指南。"
version: 1.0.0
author: Cocoblood9527
homepage: https://github.com/Cocoblood9527/para-proactive-workspace
---
# PARA + 主动代理工作空间 🦞📁

这是一个可用于生产环境的工作空间模板，它结合了两个强大的系统：

1. **PARA 方法**（Tiago Forte）——用于整理您的内容
2. **主动代理架构**（Hal Labs）——用于实现人工智能辅助的记忆管理和任务连续性

## 您将获得什么

### PARA 结构
- `1-projects/`：带有截止日期的活跃项目
- `2-areas/`：正在进行中的责任事项
- `3-resources/`：参考资料
- `4-archives/`：已完成的项目
- `+inbox/`：临时收件箱（每周处理一次）
- `+temp/`：临时存储空间

### 主动代理记忆系统
- `memory/`：每日日志和工作缓冲区
- `.learnings/`：错误日志和学习记录
- `SESSION-STATE.md`：当前工作状态
- `AGENTS.md`：操作规则
- `SOUL.md`：代理身份信息
- `USER.md`：您的个人资料
- `HEARTBEAT.md`：定期检查清单

## 安装

```bash
# Create workspace directory
mkdir -p ~/workspace
cd ~/workspace

# Copy template files
cp -r ~/.openclaw/skills/para-proactive-workspace/assets/templates/* .

# Or manually create structure following the guide below
```

## 目录结构

```
workspace/
│
├── 📁 1-projects/          # Active projects
│   └── project-name/
│       ├── README.md
│       ├── notes.md
│       ├── docs/
│       └── assets/
│
├── 📁 2-areas/             # Ongoing responsibilities
│   ├── health/
│   ├── finance/
│   └── learning/
│
├── 📁 3-resources/         # Reference materials
│   ├── articles/
│   ├── books/
│   └── templates/
│
├── 📁 4-archives/          # Completed items
│   └── 2024-projects/
│
├── 📁 +inbox/              # Temporary inbox
├── 📁 +temp/               # Scratch space
│
├── 📁 .agents/             # Agent configuration
├── 📁 .learnings/          # Learning logs
│   ├── ERRORS.md
│   ├── LEARNINGS.md
│   └── FEATURE_REQUESTS.md
│
├── 📁 memory/              # Daily logs
│   └── working-buffer.md
│
├── 📄 AGENTS.md            # Operating rules
├── 📄 HEARTBEAT.md         # Periodic checklist
├── 📄 MEMORY.md            # Long-term memory
├── 📄 ONBOARDING.md        # First-run setup
├── 📄 README.md            # Workspace overview
├── 📄 SESSION-STATE.md     # Active task state
├── 📄 SOUL.md              # Agent identity
├── 📄 TOOLS.md             # Tool configurations
├── 📄 USER.md              # Your profile
└── 📄 .gitignore           # Git ignore rules
```

## PARA 方法说明

### 项目（1-projects/）
**定义：** 与目标相关的一系列任务，具有明确的截止日期。

**示例：**
- 完成网站重新设计（截止日期：3月1日）
- 规划去日本的旅行（出发日期：4月15日）
- 推出产品新功能（第二季度目标）

**何时移至“档案”文件夹：** 项目完成后或被取消时。

### 责任事项（2-areas/）
**定义：** 需要长期维护的特定活动领域。

**示例：**
- 健康与健身
- 个人财务
- 职业发展
- 人际关系
- 家庭维护

**何时移至“档案”文件夹：** 当这些事项不再与您的日常生活相关时。

### 参考资料（3-resources/）
**定义：** 您持续感兴趣的主题或领域。

**示例：**
- 园艺技巧
- Python 编程
- 旅行目的地
- 食谱
- 书籍笔记

**何时移至“档案”文件夹：** 当您对这些内容不再感兴趣时。

### 档案（4-archives/）
**定义：** 来自其他三个类别的不再活跃的文件。

**用途：** 将其移出视线范围，但仍然可以随时查阅。

## 主动代理架构说明

### 核心文件

| 文件 | 用途 | 更新时机 |
|------|---------|----------------|
| `SOUL.md` | 代理的身份、原则和边界 | 当代理的身份或规则发生变化时 |
| `USER.md` | 您的个人资料、目标和偏好 | 随着您分享更多信息时更新 |
| `AGENTS.md` | 操作规则和工作流程 | 当工作模式逐渐明确时更新 |
| `TOOLS.md` | 工具配置和使用说明 | 当您学习新工具时更新 |
| `SESSION-STATE.md` | 当前任务和上下文信息 | 持续更新（WAL 协议） |
| `HEARTBEAT.md` | 定期检查清单 | 定期查看 |
| `MEMORY.md` | 策略性长期记忆记录 | 定期整理和更新 |

### 记忆系统

**三层记忆结构：**
1. **SESSION-STATE.md**：当前工作状态
2. `memory/YYYY-MM-DD.md`：每日原始日志
3. `MEMORY.md`：经过整理的长期记忆记录

**WAL 协议（预写日志）：**
- 任何更正内容 → 立即记录
- 任何决策 → 立即记录
- 任何名称/偏好设置 → 立即记录
- 具体数值 → 立即记录

**工作缓冲区：**
- 当上下文使用率达到 60% 时激活
- 记录所有交互内容
- 在数据压缩后仍能保留原始信息

## 使用流程

### 日常工作流程
1. **收集文件** → 将文件放入 `+inbox/`
2. **分类处理** → 将文件放入相应的 PARA 文件夹中
3. **开始工作** → 创建或更新项目
4. **记录日志** → 代理将操作内容写入 `memory/`

### 每周回顾
1. 清空 `+inbox/` 和 `+temp/`
2. 检查 `2-areas/` 中的责任事项，确保它们仍需维护
3. 将已完成的项目归档
4. 查看 `.learnings/` 中的错误记录和学习心得

### 每月回顾
1. 清理 `4-archives/` 中的文件
2. 评估 `3-resources/` 中的资料是否仍然相关
3. 使用 `MEMORY.md` 中的总结内容更新知识库

## 集成方式

### PARA 与主动代理的集成

| PARA | 主动代理 | 集成方式 |
|------|-----------------|-------------|
| 项目笔记 | `1-projects/X/notes.md` | 代理可以读取和写入 |
| 决策记录 | `SESSION-STATE.md` | 通过 WAL 协议自动记录 |
| 日常工作内容 | `memory/YYYY-MM-DD.md` | 自动记录 |
| 学习记录 | `.learnings/LEARNINGS.md` | 用于记录错误和学习成果 |
| 完成项目 | `4-archives/` | 将项目归档 |

## 最佳实践

### 对于您（人类用户）：
- 每周处理一次 `+inbox/` 中的文件（保持收件箱整洁）
- 每天清理 `+temp/` 文件夹
- 使用统一的命名规范
- 每月检查各责任事项的进展

### 对于您的代理：
- 启动时阅读 `SOUL.md` 和 `USER.md`
- 使用 WAL 协议记录重要信息
- 将错误记录到 `.learnings/ERRORS.md` 中
- 定期查看 `HEARTBEAT.md` 中的定期检查清单

## 致谢

- **PARA 方法**：Tiago Forte（“构建第二大脑”项目）
- **主动代理**：Hal Labs (@halthelobster）
- **集成技术**：OpenClaw 社区

## 许可证

MIT 许可证——自由使用、修改和分享。

---

*整理您的内容，赋能您的代理，构建您的“第二大脑”。* 🧠🦞