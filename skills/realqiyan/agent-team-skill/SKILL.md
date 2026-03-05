---
name: agent-team
description: Manage team member information including skills, roles, and work assignments. Use when: (1) listing team members, (2) adding or updating member profiles, (3) checking member expertise for task assignment, (4) managing team division and collaboration.
---

# 代理团队管理

用于管理团队成员的信息，包括他们的技能、角色和工作分配。

## 命令

所有命令均通过 `team.py` 脚本执行：

```bash
python3 scripts/team.py <command> [options]
```

### 列出成员

以表格格式列出所有团队成员：

```bash
python3 scripts/team.py list
```

输出示例：
```
+-------------+--------+------------+---------+------------------+------------------+------------------+
| Agent ID    | Name   | Role       | Enabled | Tags             | Expertise        | Not Good At      |
+-------------+--------+------------+---------+------------------+------------------+------------------+
| agent-001   | Alice  | Developer  | true    | backend, api     | python, go       | frontend         |
| agent-002   | Bob    | Designer   | true    | ui, ux           | figma, css       | backend          |
+-------------+--------+------------+---------+------------------+------------------+------------------+
```

### 添加/更新成员

添加新成员或更新现有成员：

```bash
python3 scripts/team.py update \
  --agent-id "agent-001" \
  --name "Alice" \
  --role "Backend Developer" \
  --enabled true \
  --tags "backend,api,database" \
  --expertise "python,go,postgresql" \
  --not-good-at "frontend,design"
```

参数：

| 参数 | 描述 | 是否必填 |
|-----------|-------------|----------|
| --agent-id | 成员唯一标识符 | 是 |
| --name | 成员姓名 | 是 |
| --role | 角色/职位 | 是 |
| --enabled | 启用状态（true/false） | 是 |
| --tags | 标签（用逗号分隔） | 是 |
| --expertise | 技能（用逗号分隔） | 是 |
| --not-good-at | 弱项（用逗号分隔） | 是 |

### 重置数据

清除所有团队数据并恢复到初始状态：

```bash
python3 scripts/team.py reset
```

这将团队数据重置为 `{"team": {}}`。

## 数据存储

团队数据存储在 `~/.agent-team/team.json` 文件中。如果该文件不存在，系统会自动创建它。

## 使用场景

- **团队建设**：记录所有团队成员及其技能信息。
- **任务分配**：根据成员的技能和标签分配任务。
- **能力评估**：了解每个成员的优势和劣势。
- **团队协作**：快速找到具有特定技能的成员。