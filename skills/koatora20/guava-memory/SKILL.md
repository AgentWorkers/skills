# GuavaMemory — OpenClaw 的情节记忆系统

这是一个基于情节记忆的算法，支持 Q 值评分机制，能够帮助系统记住哪些方法有效，哪些方法无效。

## 功能介绍

- 记录任务执行的详细过程（包括成功/失败情况）以及对应的 Q 值。
- 通过 `memory_search` 功能查询过去的任务记录（该功能兼容 Voyage AI）。
- 将多次成功的操作整合成可复用的技能流程。
- 识别常见的错误模式，以避免重复犯错。

## 快速入门

### 1. 设置记忆存储目录

```bash
mkdir -p memory/episodes memory/skills memory/meta
```

### 2. 初始化索引

```bash
cat > memory/episodes/index.json << 'EOF'
{
  "version": "1.0.0",
  "name": "GuavaMemory",
  "episodes": [],
  "stats": { "total": 0, "avg_q_value": 0, "promotions": 0 },
  "config": {
    "promotion_threshold": 0.85,
    "promotion_min_count": 3,
    "max_episodes_per_search": 3,
    "learning_rate": 0.3
  }
}
EOF
```

### 3. 将相关规则添加到 AGENTS.md 文件中

将以下规则复制并粘贴到您的 AGENTS.md 文件中：

```markdown
### Episodic Memory Rules
1. **Task start** → `memory_search` for related episodes. Use top 3 by Q-value
2. **Task complete** → Record episode in `memory/episodes/ep_YYYYMMDD_NNN.md`
3. **Record content** → Intent, Context, Success pattern, Failure pattern, Q-value, feel
4. **Skill promotion** → 3 successes with same intent & Q≥0.85 → promote to `memory/skills/`
5. **Anti-patterns** → Record failures in `memory/episodes/anti_patterns.md`
6. **No loops** → Record once per task at completion. No mid-task rewrites
7. **Update index** → Keep `memory/episodes/index.json` in sync
```

## 任务记录格式

创建如下结构的文件：`memory/episodes/ep_20260211_001.md`

```markdown
# EP-20260211-001: Short description

## Intent
What you were trying to do

## Context
- domain: what area
- tools: what tools used

## Experience

### ✅ Success Pattern
1. Step one
2. Step two
3. Step three

### ❌ Failure Pattern
- What didn't work and why

## Utility
- reward: 0.0-1.0 (1.0 = one-shot success)
- q_value: 0.0-1.0 (updated over time)
- feel: flow | grind | frustration | eureka
```

## Q 值更新机制

- `1.0`：一次性成功
- `0.7`：经过多次尝试后成功
- `0.3`：虽然成功但过程较为繁琐
- `0.0`：失败，但采用了不同的解决方法
- `-0.5`：失败，问题仍未解决

## 技能优化流程

当某个操作连续成功 3 次以上且 Q 值 ≥ 0.85 时：
1. 将相关任务记录合并到 `memory/skills/skill-name.md` 文件中。
2. 提取最优的操作流程。
3. 将原始任务记录标记为 `status: "graduated"`（已完成优化）。

## 搜索脚本

将 `scripts/ep-search.sh` 复制到您的工作目录中：

```bash
#!/bin/bash
EPISODES_DIR="${HOME}/.openclaw/workspace/memory/episodes"
INDEX="${EPISODES_DIR}/index.json"
echo "🔍 Searching episodes for: $1"
cat "$INDEX" | jq -r '.episodes | sort_by(-.q_value) | .[] | select(.status == "active") | "Q:\(.q_value) | \(.feel) | \(.intent) → \(.file)"'
```

## 系统要求

- 支持 OpenClaw（任意版本）。
- 需要 `jq` 工具（用于执行搜索脚本）。
- 无需其他额外依赖。

## 与 `memory_search` 的配合使用方式

所有任务记录都保存在 `memory/` 目录下的 Markdown 文件中。OpenClaw 的 `memory_search`（Voyage AI）会自动对这些文件进行索引。在搜索任务时，系统会根据语义相似性对记录进行排序，然后通过 Q 值筛选出真正有效的解决方案。