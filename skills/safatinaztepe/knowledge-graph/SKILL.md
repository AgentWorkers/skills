---
name: knowledge-graph
description: 维护 Clawdbot 的复合知识图谱（位于 `life/areas/**` 目录下），具体方法包括：添加或替换基础数据（`items.json` 文件中的内容）、重新生成实体摘要（`summary.md` 文件），并确保所有实体ID的一致性。当需要对知识图谱进行确定性更新（而非手动修改 JSON 文件）时，可以使用此方法。
---

# 知识图谱（基于文件的）

使用随附的 Python 脚本来安全地更新 `life/areas/**` 文件。

## 命令

- 添加新事实：
  ```bash
python3 skills/knowledge-graph/scripts/kg.py add \
  --entity people/safa \
  --category status \
  --fact "Runs Clawdbot on a Raspberry Pi" \
  --source conversation
```

- 替换旧事实（将旧事实标记为已替换，并创建新事实）：
  ```bash
python3 skills/knowledge-graph/scripts/kg.py supersede \
  --entity people/safa \
  --old safa-002 \
  --category status \
  --fact "Moved Clawdbot from Pi to a Mac mini"
```

- 从有效的事实中重新生成实体摘要：
  ```bash
python3 skills/knowledge-graph/scripts/kg.py summarize --entity people/safa
```

## 注意事项
- 实体存储在路径 `life/areas/<kind>/<slug>/` 下。
- 事实数据存储在 `items.json` 文件中（以数组形式）。
- 摘要信息存储在 `summary.md` 文件中。
- 每个实体的 ID 都是自增的，格式为 `<slug>-001`、`<slug>-002` 等。
- 请勿直接删除事实数据，而是使用替换操作来更新它们。