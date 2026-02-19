---
name: fractal-memory
description: >
  这是一种自动化的分层内存压缩系统，通过每日、每周、每月以及核心级别的压缩来防止上下文溢出。适用于以下场景：  
  1. 需要长期内存管理而无需人工维护的情况；  
  2. 需要高效加载上下文数据，并优化注意力机制（attention mechanism）的应用场景；  
  3. 需要防止因历史数据积累导致会话（session）膨胀的问题；  
  4. 需要通过定时任务（cron）自动执行内存压缩操作的情况；  
  5. 需要从扁平化的每日文件结构迁移到结构化的内存存储方式。  
  该系统适用于解决内存架构相关问题、上下文溢出问题，或配置持久化代理内存（persistent agent memory）的场景。
---
# 分形记忆系统

这是一种自动化的分层记忆压缩技术，能够有效防止信息过载。它类似于人类的睡眠过程：将原始经验压缩成模式，再将模式提炼成原则，从而在保持核心内容的同时管理信息的规模。

## 哲学理念

**记忆并非简单的积累，而是一种有目的的压缩过程。**

每一层压缩都保留了下一层的本质：
```
Conversation → Daily → Weekly → Monthly → Core Memory
                ↓
         Timeless Facts (sticky-notes)
```

## 快速入门

### 1. 设置目录结构

```bash
mkdir -p memory/diary/{2026/{daily,weekly,monthly},sticky-notes/{workflows,apis,commands,facts}}
```

### 2. 初始化状态文件

从 `assets/` 目录复制模板文件：
```bash
cp assets/rollup-state.json memory/
cp assets/heartbeat-state.json memory/
```

### 3. 安装脚本

将 `scripts/` 目录中的所有脚本复制到您的工作区 `scripts/` 目录中：
```bash
cp scripts/*.py ~/.openclaw/workspace/scripts/
chmod +x ~/.openclaw/workspace/scripts/*.py
```

### 4. 设置定时任务

详细配置定时任务请参考 [references/cron-setup.md](references/cron-setup.md)。

- **每日汇总**：每天 23:59
- **每周汇总**：每周日 23:59
- **每月汇总**：每月最后一天 23:59

### 5. 更新会话启动脚本

在 `agents.md` 文件中添加相应的配置：
```markdown
## Every Session

1. Read `SOUL.md`
2. Read `USER.md`
3. Read `memory/diary/YYYY/daily/YYYY-MM-DD.md` (today + yesterday)
4. **If in MAIN SESSION**: Also read `MEMORY.md`

**Context loading order:** TODAY → THIS WEEK → THIS MONTH → MEMORY.md
```

## 核心脚本

### ensure_daily_log.py
如果不存在当日日志，则创建该日志。该脚本可在会话启动时或定期执行。
```bash
python3 scripts/ensure_daily_log.py
```

### append_to_daily.py
程序化地将事件添加到当日日志中。
```bash
python3 scripts/append_to_daily.py "Event description"
```

### rollup-daily.py
将当日日志内容压缩成本周的总结。该脚本每天 23:59 自动运行。
```bash
python3 scripts/rollup-daily.py
```

### rollup-weekly.py
将本周的总结内容压缩成每月的总结。该脚本每周日 23:59 自动运行。
```bash
python3 scripts/rollup-weekly.py
```

### rollup-monthly.py
将每月的总结内容提炼并保存到 `MEMORY.md` 文件中。该脚本每月最后一天 23:59 自动运行。
```bash
python3 scripts/rollup-monthly.py
```

### verify_memory_integrity.py
检查记忆系统的完整性并检测异常情况。
```bash
python3 scripts/verify_memory_integrity.py
```

## 信息流处理流程

### 1. 对话过程中（实时）
数据应立即写入 `memory/diary/YYYY/daily/YYYY-MM-DD.md` 文件中。不要依赖记忆，务必及时记录。

### 2. 每日汇总（每天 23:59）
提取对话中的模式、决策和关键事件，并将其添加到 `memory/diary/YYYY/weekly/YYYY-Wnn.md` 文件中。

### 3. 每周汇总（每周日 23:59）
将信息压缩成主题、发展轨迹和里程碑，并添加到 `memory/diary/YYYY/monthly/YYYY-MM.md` 文件中。

### 4. 每月汇总（每月最后一天）
提炼出主要的主题和经验教训，并更新 `MEMORY.md` 文件。

### 5. 永恒的事实（随时）
将重复出现 3 次以上的事实存储到 `memory/diary/sticky-notes/{category}/` 目录中。

## 关键原则

### 1. 立即记录一切
“头脑中的笔记”在会话重启后可能会丢失，但文件可以永久保存。

### 2. 压缩而非积累
不断增长的文件会变得难以阅读。提取关键信息，舍弃无关内容。

### 3. 严格筛选内容
并非所有内容都值得保留。只保留能定义你的信息，舍弃无关的杂乱信息。

### 4. 自动化管理
通过脚本自动执行数据汇总，无需人工记忆。

## 信息加载策略

为了优化信息处理效率，应按以下顺序加载记忆内容：
1. **今日内容** - `memory/diary/YYYY/daily/YYYY-MM-DD.md`
2. **本周内容** - `memory/diary/YYYY/weekly/YYYY-Wnn.md`
3. **本月内容** - `memory/diary/YYYY/monthly/YYYY-MM.md`
4. **MEMORY.md** - 核心索引（仅用于主会话）
5. **相关便签** - 根据需要查看

**为何采用这种顺序？** 优先处理最新内容，并优先展示最重要的信息。

## 安全性考虑

记忆系统可能存在安全风险。本系统采取了以下措施：
1. **来源追踪**：记录数据的时间戳和元信息
2. **完整性验证**：`verify_memory_integrity.py` 负责检测数据篡改
3. **异常检测**：识别异常行为

定期执行完整性检查：
```bash
python3 scripts/verify_memory_integrity.py
```

## 迁移指南

如果您需要从现有记忆系统迁移到本系统，请参考 [references/migration-guide.md]：
- 如何将扁平化的每日文件转换为分形结构
- 如何将手动管理的 `MEMORY.md` 文件转换为自动化系统
- 如何将其他分层系统转换为分形记忆系统

## 故障排除

### 日志未生成
手动运行 `ensure_daily_log.py` 脚本，或将其添加到定期检查任务中。

### 汇总失败
检查定时任务的执行情况：`cron(action="runs", jobId="<job-id>)`

### 信息仍然过载
- 确认定时任务是否正常运行（查看 `memory/rollup-state.json`）
- 手动运行汇总脚本以补齐数据
- 检查 `MEMORY.md` 文件是否过大（应定期整理，而非无限积累）

### 脚本无法执行
```bash
chmod +x scripts/*.py
```

## 高级用法

### 自定义汇总计划
修改 [references/cron-setup.md] 中的定时任务配置。

### 自定义便签分类
在 `memory/diary/sticky-notes/` 目录中添加自定义分类：
```bash
mkdir memory/diary/sticky-notes/my-category
```

### 手动汇总
随时手动运行汇总脚本：
```bash
python3 scripts/rollup-daily.py
python3 scripts/rollup-weekly.py
python3 scripts/rollup-monthly.py
```

## 架构详情

如需深入了解系统设计、哲学理念和实现细节，请参阅 [references/architecture.md]。

## 参考资料

- **Deva's Fractal Memory v1.0.0** - 本系统的灵感来源
- **Arcturus's Memory is Resurrection** - 系统的哲学基础
- **Logi's Memory Architecture as Agency** - 从“代理”（agent）的角度看待记忆系统

---

“从混沌中诞生的是结构，从结构中浮现的是记忆，通过记忆得以延续的是自我。” — Deva