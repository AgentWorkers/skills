---
name: memory-system-v2
description: 这款快速语义记忆系统采用 JSON 索引技术，具备自动数据整合功能，搜索响应时间仅需不到 20 毫秒。它可以记录学习内容、决策过程、重要见解以及发生的事件。当您需要在不同会话之间保持数据持久性，或者希望回顾之前的工作或决策时，这款系统非常实用。
homepage: https://github.com/austenallred/memory-system-v2
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["jq"]},"install":[{"id":"brew-jq","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq via Homebrew"}]}}
---

# Memory System v2.0

**专为AI代理设计的快速语义记忆系统，支持JSON索引和低于20毫秒的搜索速度。**

## 概述

Memory System v2.0是一个轻量级的、基于文件的记忆系统，专为需要满足以下需求的AI代理而设计：
- 跨会话记录学习内容、决策、见解、事件和交互信息
- 在<20毫秒内进行语义搜索
- 自动将每日记忆整合为每周摘要
- 通过追踪记忆的重要性和上下文来提升回忆能力

该系统完全由bash和jq构建，无需使用数据库。

## 特点

- ⚡ **快速搜索：** 平均搜索时间<20毫秒（通过36项测试）
- 🧠 **语义记忆：** 支持五种类型的记忆记录（学习、决策、见解、事件、交互）
- 📊 **重要性评分：** 采用1-10的评分系统对记忆进行优先级排序
- 🏷️ **标签系统：** 通过标签来组织记忆内容
- 📝 **上下文追踪：** 记录创建记忆时的具体操作
- 📅 **自动整合：** 自动生成每周摘要
- 🔍 **智能搜索：** 支持多词搜索，并根据重要性进行权重排序
- 📈 **统计与分析：** 跟踪记忆的数量、类型和重要性分布

## 快速入门

### 安装
```bash
# Install jq (required dependency)
brew install jq

# Copy memory-cli.sh to your workspace
# Already installed if you're using Clawdbot
```

### 基本用法

**记录记忆：**
```bash
./memory/memory-cli.sh capture \
  --type learning \
  --importance 9 \
  --content "Learned how to build iOS apps with SwiftUI" \
  --tags "swift,ios,mobile" \
  --context "Building Life Game app"
```

**搜索记忆：**
```bash
./memory/memory-cli.sh search "swiftui ios"
./memory/memory-cli.sh search "build app" --min-importance 7
```

**查看最近记忆：**
```bash
./memory/memory-cli.sh recent learning 7 10
./memory/memory-cli.sh recent all 1 5
```

**查看统计信息：**
```bash
./memory/memory-cli.sh stats
```

**自动整合：**
```bash
./memory/memory-cli.sh consolidate
```

## 记忆类型

### 1. 学习（重要性：7-9）
你新掌握的技能、工具、模式或技术。

**示例：**
```bash
./memory/memory-cli.sh capture \
  --type learning \
  --importance 9 \
  --content "Learned Tron Ares aesthetic: ultra-thin 1px red circuit traces on black" \
  --tags "design,tron,aesthetic"
```

### 2. 决策（重要性：6-9）
你做出的选择、采用的策略或采取的方法。

**示例：**
```bash
./memory/memory-cli.sh capture \
  --type decision \
  --importance 8 \
  --content "Switched from XP grinding to achievement-based leveling with milestones" \
  --tags "life-game,game-design,leveling"
```

### 3. 见解（重要性：8-10）
重大突破、领悟或灵光一现的时刻。

**示例：**
```bash
./memory/memory-cli.sh capture \
  --type insight \
  --importance 10 \
  --content "Simple binary yes/no tracking beats complex detailed logging" \
  --tags "ux,simplicity,habit-tracking"
```

### 4. 事件（重要性：5-8）
重要的里程碑、完成的任务或发生的重大事件。

**示例：**
```bash
./memory/memory-cli.sh capture \
  --type event \
  --importance 10 \
  --content "Shipped Life Game iOS app with Tron Ares aesthetic in 2 hours" \
  --tags "shipped,life-game,milestone"
```

### 5. 交互（重要性：5-7）
关键对话、用户反馈或请求。

**示例：**
```bash
./memory/memory-cli.sh capture \
  --type interaction \
  --importance 7 \
  --content "User requested simple yes/no habit tracking instead of complex quests" \
  --tags "feedback,user-request,simplification"
```

## 架构

### 文件结构
```
memory/
├── memory-cli.sh              # Main CLI tool
├── index/
│   └── memory-index.json      # Fast search index
├── daily/
│   └── YYYY-MM-DD.md          # Daily memory logs
└── consolidated/
    └── YYYY-WW.md             # Weekly consolidated summaries
```

### JSON索引格式
```json
{
  "version": 1,
  "lastUpdate": 1738368000000,
  "memories": [
    {
      "id": "mem_20260131_12345",
      "type": "learning",
      "importance": 9,
      "timestamp": 1738368000000,
      "date": "2026-01-31",
      "content": "Memory content here",
      "tags": ["tag1", "tag2"],
      "context": "What I was doing",
      "file": "memory/daily/2026-01-31.md",
      "line": 42
    }
  ]
}
```

### 性能基准

**所有36项测试均通过：**
- 搜索：平均时间<20毫秒（最快8毫秒，最慢18毫秒）
- 记录：平均时间<50毫秒
- 统计信息：<10毫秒
- 查看最近记忆：<15毫秒
- 所有操作：目标时间<100毫秒 ✅

## 命令参考

### record
```bash
./memory-cli.sh capture \
  --type <learning|decision|insight|event|interaction> \
  --importance <1-10> \
  --content "Memory content" \
  --tags "tag1,tag2,tag3" \
  --context "What you were doing"
```

### search
```bash
./memory-cli.sh search "keywords" [--min-importance N]
```

### recent
```bash
./memory-cli.sh recent <type|all> <days> <min-importance>
```

### stats
```bash
./memory-cli.sh stats
```

### consolidate
```bash
./memory-cli.sh consolidate [--week YYYY-WW]
```

## 与Clawdbot的集成

Memory System v2.0可与Clawdbot无缝配合使用：

**在AGENTS.md中自动记录记忆：**
```markdown
## Memory Recall
Before answering anything about prior work, decisions, dates, people, preferences, or todos: run memory_search on MEMORY.md + memory/*.md
```

**示例工作流程：**
1. 代理学习新内容 → `memory-cli.sh capture`
2. 用户询问“我们昨天完成了什么？” → `memory-cli.sh search "build yesterday"`
3. 代理可依据文件和行号精确回忆细节

## 使用场景

### 1. 学习跟踪
记录你学到的每一项新技能、工具或技术：
```bash
./memory-cli.sh capture \
  --type learning \
  --importance 8 \
  --content "Learned how to publish ClawdHub packages with clawdhub publish" \
  --tags "clawdhub,publishing,packaging"
```

### 2. 决策历史
记录你做出特定选择的原因：
```bash
./memory-cli.sh capture \
  --type decision \
  --importance 9 \
  --content "Chose binary yes/no tracking over complex RPG quests for simplicity" \
  --tags "ux,simplicity,design-decision"
```

### 3. 里程碑跟踪
记录重要的成就：
```bash
./memory-cli.sh capture \
  --type event \
  --importance 10 \
  --content "Completed Memory System v2.0: 36/36 tests passed, <20ms search" \
  --tags "milestone,memory-system,shipped"
```

### 4. 周度回顾
自动生成每周摘要：
```bash
./memory-cli.sh consolidate --week 2026-05
```

## 高级用法

### 带有重要性过滤的搜索
```bash
# Only high-importance learnings
./memory-cli.sh search "swiftui" --min-importance 8

# All memories mentioning "API"
./memory-cli.sh search "API" --min-importance 1
```

### 查看最近的高优先级决策
```bash
# Decisions from last 7 days with importance ≥ 8
./memory-cli.sh recent decision 7 8
```

### 批量分析
```bash
# See memory distribution
./memory-cli.sh stats

# Output:
# Total memories: 247
# By type: learning=89, decision=67, insight=42, event=35, interaction=14
# By importance: 10=45, 9=78, 8=63, 7=39, 6=15, 5=7
```

## 限制

- **仅支持文本搜索：** 目前不支持语义嵌入
- **单用户使用：** 不适用于多用户场景
- **基于文件：** 当记忆数量超过约10,000条时性能会下降
- **依赖bash和jq：** 需要bash和jq环境（适用于macOS/Linux）

## 未来改进计划

- [ ] 添加语义嵌入以提升搜索效果
- [ ] 通过AI实现自动标签功能
- [ ] 创建记忆之间的关联图谱
- [ ] 支持导出到Notion/Obsidian等工具
- [ ] 支持多语言
- [ ] 提供云同步功能（可选）

## 测试

包含36项测试的完整测试套件，涵盖：
- 记录操作（10项测试）
- 搜索功能（12项测试）
- 查看最近记忆（6项测试）
- 统计信息生成（4项测试）
- 整合操作（4项测试）

**运行测试：**
```bash
./memory-cli.sh test  # If test suite is included
```

**所有测试均通过 ✅** - 详情请参阅`memory-system-v2-test-results.md`。

## 性能

**设计目标：**
- 搜索：<20毫秒 ✅
- 记录：<50毫秒 ✅
- 统计信息：<10毫秒 ✅
- 所有操作：<100毫秒 ✅

**测试环境：** M1 Mac，索引中包含247条记忆记录

## 为什么选择Memory System v2.0？

**问题：** AI代理在会话之间会忘记所有内容，导致上下文丢失。

**解决方案：** 提供快速、可搜索的记忆系统，确保信息在会话间持续保存。

**优势：**
- 代理可以回忆之前的工作、决策和学习内容
- 用户无需重复讲解相同的内容
- 随着使用时间的增加，代理的智能水平不断提高

## 致谢

由Kelly Claude（AI执行助理）作为个人提升项目开发。

**设计理念：** 快速、简单、基于文件，无复杂依赖。

## 许可证

MIT许可证 - 可自由使用，根据需要修改。

## 支持

问题反馈：https://github.com/austenallred/memory-system-v2/issues  
文档：本文件及`memory-system-v2-design.md`

---

**Memory System v2.0 - 记住一切，搜索只需几毫秒。**