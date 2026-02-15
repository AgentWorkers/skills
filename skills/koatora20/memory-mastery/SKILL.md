# 记忆管理 - OpenClaw 内存系统

**一个支持跨会话持久化上下文的三层内存架构**

## 功能简介

本技能为 OpenClaw 代理实现了结构化的内存管理系统，通过三层架构帮助代理在会话之间保持上下文和连贯性：

- **L1（每日日志）**：`memory/YYYY-MM-DD.md` - 仅用于追加内容的每日笔记
- **L2（长期记忆）**：`MEMORY.md` - 经过整理的、永久性的知识库
- **L3（向量搜索）**：`memory_search` - 通过 memory-core 插件实现的语义搜索

## 为何需要这个系统

**不使用该系统时：**
- 代理在每次会话开始时都会“重置”，忘记之前的对话内容
- 重启后上下文会丢失
- 会反复出现关于偏好设置、过去决策和项目状态的问题
- 无法搜索过去发生的事情

**使用该系统后：**
- 所有会话中的数据都能被持久化保存
- 每日日志记录所有重要内容
- 可以通过向量搜索快速找到相关信息
- 系统会自动提示在数据压缩前保存重要信息
- 保护隐私（`MEMORY.md` 仅在私有会话中加载）

## 安装前准备

### 先决条件

- OpenClaw 工作区已初始化
- 具有对工作区目录的写入权限
- （可选）用于 L3 向量搜索的 memory-core 插件
- （可选）用于向量搜索的嵌入 API 密钥

### 诊断检查

运行审计脚本以查看当前的内存状态：

```bash
bash scripts/audit.sh
```

脚本将输出 JSON 数据，包括：
- `MEMORY.md` 是否存在及其大小
- `memory/` 目录是否存在及文件数量
- `memory_search` 功能是否可用

## 优点与缺点

### ✅ 优点

1. **持久化上下文**：代理在不同会话间能够记住信息
2. **双层存储机制**：每日日志用于存储原始数据，整理后的记忆用于存储关键信息
3. **语义搜索**：可以根据内容含义而非关键词查找相关记忆
4. **自动保存机制**：系统会在数据压缩前提示保存重要内容
5. **每周维护**：定期审查有助于保持内存内容的更新
6. **隐私保护**：`MEMORY.md` 仅在私有会话中加载

### ⚠️ 缺点

1. **`MEMORY.md` 可能会变得很大**：随着时间推移文件可能膨胀，增加令牌使用量
2. **嵌入 API 成本**：L3 向量搜索需要外部 API（如 Voyage）
3. **磁盘占用**：每日日志会不断累积（可通过归档来缓解）
4. **需要维护**：如果定期不审查，L2 中的内容可能会过时
5. **需要手动管理**：需要定期从每日日志中更新 `MEMORY.md`

## 安装步骤

### 交互式设置

**重要提示：此操作会修改您的工作区。请在继续前确认。**

1. 查看诊断结果：
   ```bash
   bash scripts/audit.sh
   ```

2. 了解以下变化：
   - 会创建 `memory/` 目录（如果不存在）
   - 会从模板创建 `MEMORY.md`（并备份现有文件）
   - 会将内存管理规则添加到 `AGENTS.md` 中
   - 会将维护任务添加到 `HEARTBEAT.md` 中

3. 运行设置脚本：
   ```bash
   bash scripts/setup.sh /Users/ishikawaryuuta/.openclaw/workspace
   ```

4. 脚本会：
   - 显示其执行计划
   - 请求您的确认（输入 `y/n`）
   - 在修改前备份现有文件
   - 报告操作结果

### 创建/修改的内容

**创建的内容：**
- `memory/` 目录
- `MEMORY.md`（如果不存在，则创建；现有文件会被备份）

**修改的内容：**
- `AGENTS.md`：添加内存管理规则
- `HEARTBEAT.md`：添加每周维护任务

**备份：**
- 现有文件会以 `.backup-TIMESTAMP` 为后缀进行备份

## 使用方法

### 日常工作流程

**在每次会话开始时**：
- 代理应阅读 `memory/YYYY-MM-DD.md`（今天的日志及昨天的日志）
- 仅在工作主会话中阅读 `MEMORY.md`

**在会话进行中**：
- 随着操作的发生，将内容写入 `memory/YYYY-MM-DD.md`
- 对于重要的决策或见解，更新 `MEMORY.md`

**在数据压缩前**：
- 系统会提示代理保存重要信息到内存中

### 每周维护

**运行维护脚本**：
```bash
bash scripts/maintenance.sh
```

该脚本会扫描过去 7 天的每日日志，并建议哪些内容应整合到 `MEMORY.md` 中。

**手动维护**：
1. 阅读建议的内容
2. 将精选的见解更新到 `MEMORY.md` 中
3. 从 `MEMORY.md` 中删除过时的信息

### 内存搜索（L3）

如果您安装了 memory-core 插件：

```javascript
// Search for relevant memories
memory_search("project decisions about X")
```

该插件利用向量嵌入技术，在所有内存文件中查找语义上相似的内容。

## 文件结构

```
workspace/
├── MEMORY.md                    # L2: Long-term curated memory
├── memory/                      # L1: Daily logs
│   ├── 2026-02-09.md
│   ├── 2026-02-10.md
│   └── heartbeat-state.json     # Heartbeat tracking
├── AGENTS.md                    # Includes memory rules
└── HEARTBEAT.md                 # Includes maintenance tasks
```

## 维护脚本

### audit.sh
**用途**：诊断当前的内存状态
**使用方法**：`bash scripts/audit.sh`
**输出**：内存系统状态的 JSON 总结

### setup.sh
**用途**：在工作区中安装内存管理系统
**使用方法**：`bash scripts/setup.sh <workspace_path>`
**安全性**：不会破坏现有文件，会进行备份，并会请求用户确认

### maintenance.sh
**用途**：从最近的每日日志中推荐应整合到 `MEMORY.md` 中的内容
**使用方法**：`bash scripts/maintenance.sh`
**输出**：需要审核的内容列表

## 隐私与安全

- `MEMORY.md` 包含个人隐私信息，仅应在私有/主会话中加载
- **每日日志** 可能包含敏感信息，请避免共享原始日志
- **向量嵌入数据** 由 memory-core 插件存储（请参阅插件文档了解数据处理方式）

## 故障排除

**`MEMORY.md` 文件过大**
- 将旧内容归档到 `memory/archive/`
- 将多个相关条目合并为单个条目
- 删除过时的信息

**每日日志堆积**
- 创建 `memory/archive/YYYY-MM/` 目录并移动旧日志
- 保留最近 30-90 天的日志，其余的进行归档

**内存搜索无法使用**
- 检查是否安装了 memory-core 插件
- 确认嵌入 API 密钥是否配置正确
- 如有必要，重新构建索引（请参阅插件文档）

**安装失败**
- 检查工作区路径是否正确
- 确保具有写入权限
- 查看脚本输出中的错误信息

## 高级功能：自定义设置

### 修改模板

在运行设置脚本之前，请编辑 `templates/` 目录下的文件：
- `MEMORY.md.template`：自定义页面结构
- `memory-rules.md`：调整内存管理规则
- `heartbeat-memory.md`：更改维护频率

### 扩展脚本

所有脚本均为纯 Bash 脚本，无依赖项。可根据实际需求进行修改。

## 支持资源

- 本技能为独立模块，可参考以下资源：
- 脚本源代码（附带详细注释）
- `OpenClaw AGENTS.md`：其中包含内存管理规则
- memory-core 插件文档：了解 L3 向量搜索的详细信息

---

**版本**：1.0  
**兼容性**：OpenClaw（macOS/Linux）  
**依赖项**：无（L3 功能需要 memory-core 插件和嵌入 API）