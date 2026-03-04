---
name: memory-organizer
description: 组织并压缩内存文件，以减少新会话中的上下文加载时间。自动识别重要信息并丢弃冗余内容。
metadata:
  {
    "openclaw": { "emoji": "🧠" }
  }
---
# 内存文件管理工具

这是一个用于整理和压缩内存文件的工具。

## 主要功能

1. **扫描内存文件** - 查看内存目录中的所有文件
2. **分析文件内容** - 识别重要信息（用户设置、项目配置、待办事项）
3. **压缩与整理** - 简化冗长内容，保留核心信息
4. **清理文件** - 删除过时或不必要的文件
5. **安全性** - 通过路径验证防止目录遍历攻击

## 安装

该工具已预安装在 OpenClaw 工作空间中。可以直接使用：

```bash
# Link to local bin (optional)
ln -sf ~/.openclaw/workspace-main/skills/memory-organizer/memory-organizer.js ~/.local/bin/memory-organizer

# Or run directly
node ~/.openclaw/workspace-main/skills/memory-organizer/memory-organizer.js <command>
```

## 工作空间配置

默认工作空间：`~/.openclaw/workspace-main`

自定义工作空间：
```bash
# Via command line
memory-organizer scan --workspace /path/to/workspace

# Via environment variable
OPENCLAW_WORKSPACE=/path/to/workspace memory-organizer scan
```

## 使用场景

- 内存文件过大，导致每次会话加载速度变慢
- 需要提取关键信息并忽略详细内容
- 需要定期维护内存文件

## 命令

### 扫描内存文件

```bash
memory-organizer scan
```

### 按主题分类文件

```bash
memory-organizer classify
```

### 查找重复文件

```bash
memory-organizer redundant
```

### 删除重复文件

```bash
memory-organizer discard redundant --force
```

### 压缩内存文件

```bash
memory-organizer compress 2026-01-01.md        # Keep titles and key lines
memory-organizer compress 2026-01-01.md --titles  # Keep titles only
memory-organizer compress 2026-01-01.md --aggressive  # Aggressive compression
```

### 合并文件到主内存目录

```bash
memory-organizer merge 2026-01-01.md
```

### 查看文件内容

```bash
memory-organizer view 2026-01-01.md
```

### 清理备份文件

```bash
memory-organizer clean
```

## 文件分类

该工具会自动将文件分类为以下几类：

- **用户设置**：名称、时区、个人偏好
- **项目配置**：代理程序、定时任务、工作空间
- **技能**：已安装的工具和技能
- **创收想法**：副业建议、项目计划
- **待办事项**：任务、计划、下一步行动
- **技术笔记**：代码示例、命令、解决方案
- **日常记录**：每日日志、常规操作

## 安全性措施

- **路径验证**：所有文件操作均经过验证，以防止目录遍历攻击
- **文件名限制**：仅允许 `.md` 格式的文件，不允许使用路径分隔符（`..`, `/`, `\`）
- **工作空间隔离**：所有操作仅限于内存文件目录内

## 使用建议

1. 每日或每周运行一次文件整理任务
2. 保留关键信息（用户设置、项目配置、待办事项）
- 删除不必要的日志和临时记录
- 保持 `MEMORY.md` 文件简洁（少于 100 行）

## 推荐的文件结构

```
# User Preferences
- Name, how to address
- Timezone
- Key preferences

# Project Config
- Agent configurations
- Scheduled tasks
- Important file paths

# Todos
- Current tasks
- Next steps
```