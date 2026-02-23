---
name: Memory
slug: memory
version: 1.0.2
homepage: https://clawic.com/skills/memory
description: 这是一种无限容量、高度组织化的存储系统，能够与您的代理内置内存相辅相成，提供无限制的分类存储功能。
changelog: Redesigned as complementary system, user-defined categories, optional sync from built-in memory.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
# 内存 🧠

**拥有无限容量且永不遗忘的超强记忆系统。**

您的智能助手具备基本的内置内存功能。此技能为您添加了无限容量、高度组织化的存储空间，用于存储其他所有信息——这些信息是并行存储的，且互不冲突。

## 工作原理

```
Built-in Agent Memory          This Skill (~/memory/)
┌─────────────────────┐        ┌─────────────────────────────┐
│ MEMORY.md           │        │ Infinite categorized storage │
│ memory/ (daily logs)│   +    │ Any structure you want       │
│ Basic recall        │        │ Perfect organization         │
└─────────────────────┘        └─────────────────────────────┘
         ↓                                  ↓
   Agent basics                    Everything else
   (works automatically)           (scales infinitely)
```

**此功能并非替代内置内存。** 智能助手的内置内存依然会正常使用，此技能只是为其提供了额外的、可无限扩展的存储空间。

## 设置

首次使用时，请阅读 `setup.md` 以配置内存系统。需要考虑的关键问题包括：
1. 用户需要哪些分类？
2. 是否需要将某些数据从内置内存同步到新系统中？
3. 用户希望如何查找所需信息？

## 使用场景

当用户需要超出基本内存容量的长期、有序存储空间时，此功能非常有用——例如：详细的项目记录、庞大的联系人网络、决策过程记录、专业领域知识、收藏的资料等随时间增长的数据结构化内容。

## 架构

所有存储数据都位于 `~/memory/` 文件夹中，该文件夹与智能助手的内置内存是分开的。

```
~/memory/
├── config.md              # System configuration
├── INDEX.md               # What's stored, where to find it
│
├── [user-defined]/        # Categories the user needs
│   ├── INDEX.md           # Category overview
│   └── {items}.md         # Individual entries
│
└── sync/                  # Optional: synced from built-in memory
    └── ...
```

**用户自行定义分类结构。** 常见分类示例包括：
- `projects/`：详细的项目信息
- `people/`：包含完整信息的联系人资料
- `decisions/`：决策背后的思考过程
- `knowledge/`：专业领域的知识库或参考资料
- `collections/`：用户收集的各类资料（书籍、食谱等）

更多分类模板请参阅 `memory-template.md`。

## 快速参考

| 功能 | 对应文件 |
|-------|------|
| 首次设置 | `setup.md` |
| 所有分类模板 | `memory-template.md` |
| 存储组织方式 | `patterns.md` |
| 常见问题及解决方法 | `troubleshooting.md` |

---

## 核心规则

### 1. 与内置内存分离

该存储系统位于 `~/memory/` 文件夹中。请勿修改以下文件：
- 智能助手的工作区根目录下的 `MEMORY.md` 文件
- 智能助手工作区内的 `memory/` 文件夹（如果存在的话）

**此系统是内置内存的补充，而非替代品。** 两者会同时运行。

### 2. 用户自定义分类结构

在设置过程中，根据用户的需求来创建相应的分类文件夹：
- 如果用户表示“我有很多项目”，则创建 `~/memory/projects/` 文件夹
- 如果用户表示“我经常与人交流”，则创建 `~/memory/people/` 文件夹
- 如果用户希望记录决策过程，创建 `~/memory/decisions/` 文件夹
- 如果用户正在学习某个主题，创建 `~/memory/knowledge/[主题]/` 文件夹
- 如果用户有收藏习惯，创建 `~/memory/collections/[收藏内容]/` 文件夹

**系统没有预设的分类结构。** 用户可以根据实际需求自行创建分类。

### 3. 每个分类都有索引文件

每个文件夹都会生成一个 `INDEX.md` 文件，用于列出该文件夹内的所有文件内容：

```markdown
# Projects Index

| Name | Status | Updated | File |
|------|--------|---------|------|
| Alpha | Active | 2026-02 | alpha.md |
| Beta | Paused | 2026-01 | beta.md |

Total: 2 active, 5 archived
```

索引文件通常保持较小的规模（少于 100 条记录）。当文件数量过多时，可将其拆分为子分类。

### 4. 即时写入数据

当用户分享重要信息时，请立即执行以下操作：
1. 将数据写入 `~/memory/` 目录下的相应文件中
2. 更新对应的 `INDEX.md` 文件
3. 然后回复用户

**切勿等待或批量处理，应立即写入数据。**

### 5. 先搜索再查找

查找信息时，请按照以下步骤操作：
1. 先确认信息是否存储在 `~/memory/` 或内置内存中
2. 在 `~/memory/` 目录内使用 `grep` 或语义搜索工具进行查找
3. 通过 `INDEX.md` 文件导航到相应的分类文件夹，再找到具体文件

```bash
# Quick search
grep -r "keyword" ~/memory/

# Navigate
cat ~/memory/INDEX.md           # What categories exist?
cat ~/memory/projects/INDEX.md  # What projects?
cat ~/memory/projects/alpha.md  # Specific project
```

### 6. 选择性地从内置内存同步数据（可选）

如果用户希望将某些数据从内置内存复制到新系统中，请按照以下步骤操作：

```
~/memory/sync/
├── preferences.md    # Synced from built-in
└── decisions.md      # Synced from built-in
```

**同步是单向的：** 数据仅从内置内存复制到新系统，切勿修改内置内存的内容。

### 7. 通过拆分文件来扩展存储空间

当某个分类文件夹的内容过多时（例如包含超过 100 条记录），请执行以下操作：
- 创建子分类文件夹
- 为每个子分类生成新的 `INDEX.md` 文件
- 在根目录下的 `INDEX.md` 文件中添加对子分类的引用

```
~/memory/projects/
├── INDEX.md           # "See active/, archived/"
├── active/
│   ├── INDEX.md       # 30 active projects
│   └── ...
└── archived/
    ├── INDEX.md       # 200 archived projects
    └── ...
```

---

## 适合存储的内容（与内置内存的区别）

| 适合存储在 `~/memory/` 的内容 | 适合存储在内置内存中的内容 |
|------------------------|------------------|
| 详细的项目记录 | 当前项目的状态信息 |
| 完整的联系人资料 | 快速查阅的关键联系人信息 |
- 所有决策过程的详细记录 | 最新的决策内容 |
- 专业领域知识库 | 快速查询所需的信息 |
- 收藏的资料或清单 | — |
| 随时间增长的数据 | 数据的摘要或概要 |

**原则：** 内置内存用于快速获取基本信息；`~/memory/` 文件夹用于存储更详细和大量的数据。

---

## 查找信息的方法

### 当文件数量较少（<50 个）时
```bash
# Grep is fast enough
grep -r "keyword" ~/memory/
```

### 当文件数量较多（50 个以上）时
使用索引文件进行查找：

```
1. ~/memory/INDEX.md → find category
2. ~/memory/{category}/INDEX.md → find item
3. ~/memory/{category}/{item}.md → read details
```

### 当文件数量非常多（500 个以上）时
如果支持语义搜索或分层索引，可以使用相应的方法进行查找：

```
~/memory/projects/INDEX.md → "web projects in web/"
~/memory/projects/web/INDEX.md → "alpha project"
~/memory/projects/web/alpha.md → details
```

---

## 维护工作

### 每周（5 分钟）
- 如果有新内容添加，更新 `INDEX.md` 文件
- 将已完成或不再使用的数据归档

### 每月（15 分钟）
- 检查各分类文件夹的文件数量
- 对内容过多的分类进行拆分
- 删除过时的数据

### 当系统运行缓慢时
- 检查 `INDEX.md` 文件的大小（确保其不超过 100 行）
- 将大型分类文件夹拆分为子分类
- 将旧内容归档

---

## 常见问题及解决方法

- **切勿修改内置内存**：请勿直接修改智能助手的工作区内存文件或 `MEMORY.md` 文件。此系统与内置内存是并行运行的。
- **务必维护索引文件**：没有索引文件会导致查找信息变得非常耗时。请始终确保索引文件的存在。
- **避免使用过大的单一分类文件夹**：一个文件夹内存放过多文件会导致查找效率降低。请将其拆分为子分类。
- **避免批量写入数据**：用户分享信息时，请立即写入文件，切勿等待。
- **注意数据安全**：请勿将所有数据同步到新系统；仅同步需要整理的内容。

---

## 安全性与隐私保护

**数据存储位置：** 所有数据都存储在用户设备上的 `~/memory/` 文件夹中。
- 无需使用任何外部服务。
- 不会发送任何数据到外部。

**此技能不会执行以下操作：**
- 访问智能助手的内置内存（仅在数据同步时读取数据）
- 将数据发送到任何外部服务器
- 也不会存储用户的敏感信息（如密码等）。

---

## 相关技能

如果用户同意安装，请使用以下命令进行扩展功能：
- `clawhub install <slug>`：安装 `decide`（决策追踪功能）
- `escalate`（判断何时需要人工介入）
- `learn`（自适应学习功能）

## 用户反馈

- 如果觉得此功能有用，请给 `memory` 功能点赞（使用 `clawhub star` 功能）
- 为了保持功能更新，请定期运行 `clawhub sync` 命令。