# 技能：HTN Planner

## 描述
这是一个用于构建层次化任务网络（Hierarchical Task Network, HTN）的规划工具及可视化工具。它支持使用 JSON 格式定义任务域和问题，利用 Mermaid 图表库可视化任务分解结构，并能够模拟任务的执行过程。

## 使用方法
```bash
# Visualize a plan
node skills/htn-planner/index.js --action visualize --domain domain.json --problem problem.json --output plan.mmd

# Simulate execution
node skills/htn-planner/index.js --action simulate --domain domain.json --problem problem.json
```

## 输入格式（JSON）
### 任务域
```json
{
  "tasks": {
    "root": { "type": "compound", "methods": ["m1", "m2"] },
    "m1": { "type": "method", "subtasks": ["t1", "t2"] },
    "t1": { "type": "primitive", "action": "do_something" }
  }
}
```

### 问题描述
```json
{
  "state": { "loc": "home" },
  "goal": ["root"]
}
```