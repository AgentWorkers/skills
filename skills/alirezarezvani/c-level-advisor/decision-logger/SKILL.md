---
name: decision-logger
description: "双层内存架构用于管理董事会决策：  
- 第一层（Layer 1）存储原始会议记录；  
- 第二层（Layer 2）存储已通过的决策内容。  
该架构适用于在董事会会议结束后记录决策结果、使用 `/cs:decisions` 查看过往决策，或通过 `/cs:review` 检查逾期未处理的行动项。  
该功能会在创始人批准流程的第五阶段（Phase 5）后，由 `board-meeting` 技能自动触发执行。"
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: decision-memory
  updated: 2026-03-05
  python-tools: scripts/decision_tracker.py
---
# 决策记录系统（Decision Logging System）

该系统采用双层内存架构：

- **第一层（Layer 1）**：存储所有会议记录。  
  - 包括所有参与者的发言内容、第三阶段的评审意见以及第四阶段的综合结论。  
  - 所有辩论内容（包括被否决的论点）均保存在此层。  
  - **仅会在创始人的明确请求下自动加载**，且保存90天后会被归档（路径：`memory/board-meetings/archive/YYYY/`）。

- **第二层（Layer 2）**：仅存储创始人批准的决策内容。  
  - 包括最终确定的决策、后续需要执行的行动项以及用户提出的修改建议。  
  - 在每次董事会会议开始时自动从第一层加载到第二层。  
  - 决策内容永远不会被删除，只会被新的决策覆盖。  
  - 由首席运营官（Chief of Staff）负责管理第二层的内容，代理人员无权直接修改。

## 命令操作

| 命令                | 功能                        |
|------------------|---------------------------|
| `/cs:decisions`     | 查看最近10条被批准的决策            |
| `/cs:decisions --all`    | 查看所有决策记录                |
| `/cs:decisions --owner CMO` | 按所有者筛选决策                |
| `/cs:decisions --topic pricing` | 按关键词搜索决策                |
| `/cs:review`      | 查看7天内需要执行的行动项            |
| `/cs:review --overdue`   | 查看逾期未处理的行动项            |

## 双层架构详解

### 第一层（Layer 1）——原始会议记录  
**存储位置：`memory/board-meetings/YYYY-MM-DD-raw.md`**  
- 包含所有会议中的发言内容、评审意见及最终决策结果。  
- **永远不会自动加载**，仅由创始人请求时才会被读取。  
- 90天后会被归档至 `memory/board-meetings/archive/YYYY/`。

### 第二层（Layer 2）——已批准的决策  
**存储位置：`memory/board-meetings/decisions.md`**  
- 仅包含创始人批准的决策、后续行动项及用户提出的修改建议。  
- 在每次董事会会议开始时自动从第一层加载到第二层。  
- 决策内容只能追加，永远不会被删除。  
- 由首席运营官负责管理第二层的内容。

## 决策记录格式

---

## 冲突检测机制  
在记录决策之前，首席运营官会检查以下情况：  
1. **禁止重复记录已被否决的提案**。  
2. **避免同一议题出现相互矛盾的决策**。  
3. **确保同一行动项不会被分配给不同的人**。  

**若发现冲突，将采取以下措施：**  
---

**禁止重复记录已被否决的提案（DO_NOT_RESURFACE机制）：**  
---

## 记录流程（第五阶段之后）  
1. 创始人批准最终的决策结果。  
2. 将原始会议记录写入第一层（`YYYY-MM-DD-raw.md`）。  
3. 检查第二层（`decisions.md`）中是否存在冲突。  
4. 若发现冲突，等待创始人解决。  
5. 将已批准的决策内容追加到第二层（`decisions.md`）。  
6. 确认决策已记录、行动项已跟踪，并标记相关条目为“禁止重复记录”。  

## 行动项的完成标记  

已完成的任务永远不会被删除。所有历史记录都是重要的参考依据。  

## 文件结构  

---

## 参考资源  
- `templates/decision-entry.md`：包含单条决策记录的模板及字段规范。  
- `scripts/decision_tracker.py`：用于解析命令行输入、跟踪逾期任务及检测冲突的脚本。