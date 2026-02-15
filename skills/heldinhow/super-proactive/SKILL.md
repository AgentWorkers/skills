# 超级主动型智能代理（Super Proactive Agent）

**这是专为AI代理设计的终极主动式与记忆管理系统。**它将11项高评分技能的最佳特性整合到了一个统一的架构中。

---

## 为什么选择这个技能？

大多数AI代理只是被动地等待用户的指令。而这个技能能让你的代理变成一个主动的合作伙伴，具备以下能力：
- 在未被请求的情况下主动预测用户的需求
- 记住所有重要的信息
- 自主执行后台任务
- 随时间不断提升自身能力

---

## 架构概述

```
workspace/
+-- MEMORY.md              # Long-term memory (curated learnings)
+-- SESSION-STATE.md       # Working buffer (HOT - survives flush)
+-- memory/
|   +-- YYYY-MM-DD.md     # Daily logs (episodic)
+-- QUEUE.md              # Task queue (Ready/In Progress/Done)
+-- skills/               # Procedural memory
```

---

## 核心特性

### 1. WAL协议（Write-Ahead Logging，预写日志）

在响应用户请求之前，代理会先将关键信息写入`SESSION-STATE.md`文件中。每一个决策、修改以及重要细节都会被立即记录下来。

```bash
# Example: Log a decision
echo "$(date) - Decision: Using model for generation" >> SESSION-STATE.md
```

### 三级记忆系统

- **情景记忆**（`memory/YYYY-MM-DD.md`）：当天发生的事情
- **语义记忆**（`MEMORY.md`）：长期存储的知识
- **程序性记忆**（`skills/`）：执行任务的步骤

### 2. 自主运行的定时任务（Crons）

无需人工提示，代理会自动执行以下后台任务：
- 每30分钟：检查任务队列、系统状态和内存使用情况
- 每4小时：研究相关主题并更新知识
- 每天18点：生成每日总结并进行数据清理

### 3. 工作缓冲区

`SESSION-STATE.md`文件在系统重启后仍能保留数据。始终通过该文件来获取：
- 当前项目的上下文信息
- 待处理的任务
- 正在执行的任务

### 4. 任务队列（QUEUE.md）

任务队列包含以下状态：
- **待处理**：需要执行的任务
- **进行中**：当前正在处理的任务
- **已完成**：已经完成的任务
- **阻塞中**：等待进一步处理的任务

---

## 快速设置步骤

### 1. 文件结构

在工作区创建以下文件：
```bash
mkdir -p memory/$(date +%Y-%m-%d)
touch SESSION-STATE.md QUEUE.md
```

### 2. 更新`HEARTBEAT.md`文件
```markdown
## Every Heartbeat (~30 min)
- [ ] Check QUEUE.md for Ready tasks
- [ ] Process queue if In Progress empty
- [ ] Verify services

## Every 4 Hours
- [ ] Research topic
- [ ] Update memory

## Daily (18:00 UTC)
- [ ] Summary, cleanup
```

### 3. 首先查询记忆

在回答用户问题之前，务必先查询记忆系统中的相关信息。

---

## 使用示例

### 检查任务队列
```bash
# Read current queue
cat QUEUE.md
```

### 添加新任务
```markdown
## Ready
- Research topic
```

### 记录决策过程
```bash
echo "$(date) - Decision: Updated configuration" >> SESSION-STATE.md
```

---

## 最佳实践

1. **立即记录**：如果信息重要，请立即将其写入日志。
2. **先查询再回答**：不要猜测，先在记忆系统中查找相关信息。
3. **利用会话信息**：始终通过`SESSION-STATE.md`来维护工作上下文。
4. **定期整理日志**：每周查看`MEMORY.md`文件，总结关键信息。
5. **保持主动性**：主动预测用户需求，而不是被动等待指令。

---

## 组合来源

| 技能名称 | 评分 | 适用场景 |
|---------|------|---------|
| elite-longterm-memory | 3.617 | 长期记忆管理 |
| proactive-agent | 3.520 | 主动行为与定时任务管理 |
| memory-setup | 3.536 | 系统配置 |
| memory-hygiene | 3.530 | 数据清理与优化 |
| agent-autonomy-kit | 3.483 | 任务调度机制 |
| agent-memory | 3.490 | 代理内存管理 |
| neural-memory | 3.481 | 神经网络辅助的记忆机制 |
| cognitive-memory | - | 类人类记忆功能 |
| proactive-solvr | 3.437 | 问题解决能力 |
| proactive-tasks | 3.379 | 任务分配与执行 |
| memory-manager | - | 内存资源管理 |

---

## 作者

**Super Proactive**：由Clawdinho整合自11项高评分的OpenClaw技能而成

---

## 版本信息

**v1.0.0**：首次合并发布的版本