---
name: memory-tiers
version: 0.1.0
description: 针对AI代理的分层内存管理机制——采用LRU（Least Recently Used）缓存来存储上下文数据。系统支持热区、温区和冷区三种存储层级，并具备自动晋升（将数据从冷区提升到温区或热区）、降级（将数据从热区或温区降级到冷区）以及访问跟踪的功能。
---
# 内存分层机制

这是一个为AI代理设计的分层内存系统。其原理类似于CPU缓存层次结构，但适用于处理上下文窗口（context window）中的数据。

## 架构

```
MEMORY.md (Tier 1 — Hot)          ← Always loaded, ~100 lines max
  ↕ promote (accessed) / demote (stale 7+ days)
memory/tier2-recent.md (Warm)     ← On-demand, last 30 days
  ↕ promote / demote (stale 30+ days)
memory/tier3-archive.md (Cold)    ← Search only, deep history
  ↕
memory/YYYY-MM-DD.md (Raw)        ← Immutable daily logs
```

## 脚本

所有脚本均位于`scripts/`目录中（相对于当前SKILL.md文件）。

### 监控内存访问
定期扫描会话记录（session transcripts），以检测对内存文件的读写/搜索操作。

```bash
node scripts/track.js                    # scan last 24h
node scripts/track.js --since 72         # scan last 72 hours
```

**输出：**将访问数据（包括每个文件和每个部分的访问时间）更新到`state/access-log.json`文件中。

### 运行维护任务
根据访问模式，将内存部分在不同层级之间进行升降级。

```bash
node scripts/maintain.js --dry-run       # preview changes
node scripts/maintain.js                 # apply changes
node scripts/maintain.js --demote-days-t1 5   # custom T1 demotion threshold
```

**规则：**
- 如果某个T1层中的部分在7天内未被访问，则将其降级到T2层。
- 如果某个T2层中的部分在30天内未被访问，则将其降级到T3层。
- 如果T2层或T3层中的部分在过去的24小时内被访问过，则将其升级到T1层。

### 手动升降级
可以手动将某个部分在不同层级之间进行移动。

```bash
node scripts/promote.js --list                           # show all sections
node scripts/promote.js --section "LARC" --from 3 --to 1  # promote
node scripts/promote.js --section "TextWeb" --from 1 --to 2 # demote
```

### 健康报告
显示当前各层的内存占用情况、数据陈旧程度以及相应的优化建议。

```bash
node scripts/report.js                   # pretty-printed
node scripts/report.js --json            # machine-readable
```

## 心跳机制集成
将此内存分层机制集成到您的心跳检测（heartbeat）系统中（每隔几小时执行一次检测）：

```markdown
## Memory Maintenance
1. Run `node <skill_dir>/scripts/track.js` to update access tracking
2. Run `node <skill_dir>/scripts/maintain.js --dry-run` to check for needed changes
3. If changes look good, run without --dry-run
4. Run `node <skill_dir>/scripts/report.js` to verify health
```

## 状态文件
- `state/access-log.json`：记录每个文件和每个部分的访问时间戳及访问次数。
- `state/maintenance-log.json`：记录所有维护操作的历史记录。

## 各层规则

| 规则 | 阈值 | 操作 |
|------|-----------|--------|
| T1层数据陈旧 | 7天内未被访问 | 降级到T2层 |
| T2层数据陈旧 | 30天内未被访问 | 降级到T3层 |
| T2/T3层数据被访问 | 在过去24小时内被访问过 | 升级到T1层 |
| T1层文件过大（超过100行） | 降级访问频率最低的部分 |
| 日志文件 | 日终后未被修改 | 作为数据来源的权威记录 |

## 文件格式规范
各层内存文件应包含以下文件头信息：

```markdown
# MEMORY.md — Working Memory (Tier 1)
<!-- last_maintained: YYYY-MM-DD -->
<!-- tier: 1 — hot context -->
```

各部分内容应使用`##`或`###`作为标记。维护脚本会依据这些标记来识别可进行升降级的文件单元。

在`MEMORY.md`文件中，`## Index → Deeper Tiers`这一部分必须位于文件末尾，因为它提供了指向较低层级内容的引用。