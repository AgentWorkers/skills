# 斯普林特回顾会议引导者

帮助团队开展结构化的回顾会议，确保会议产生具体的行动项，而不仅仅是模糊的“我们应该更好地沟通”之类的建议。

## 功能概述

1. **收集团队反馈**：涵盖四个方面：哪些方面做得好，哪些方面做得不好，哪些让我们感到困惑，接下来应该尝试什么。
2. **根据反馈的频率和影响对问题进行分类和优先级排序**。
3. **生成具体的行动项**，包括负责人、截止日期和成功标准。
4. **生成回顾报告**，以便与利益相关者分享。
5. **分析跨多个斯普林特中的重复性问题**。

## 使用方法

向工具发送以下指令：
- `Run a retrospective for Sprint 24` — 启动完整的回顾会议流程。
- `Quick retro: [粘贴团队反馈]` — 将原始反馈处理成结构化的输出结果。
- `Compare last 3 retros` — 分析过去三次回顾会议中反复出现的问题和未完成的行动项。

## 支持的框架

- **Start/Stop/Continue**：经典框架，适用于任何规模的团队。
- **4Ls**：喜欢（Liked）、学到（Learned）、缺乏（Lacked）、渴望（Longed For）。
- **Mad/Sad/Glad**：用于评估团队情绪状态。
- **Sailboat**：风（有利因素）、锚（障碍）、岩石（风险）、岛屿（目标）。
- **DAKI**：删除（Drop）、添加（Add）、保留（Keep）、改进（Improve）。

## 输出格式

```markdown
# Sprint [N] Retrospective — [Date]

## Top Themes
1. [Theme] — mentioned by X people, impact: HIGH/MED/LOW

## Action Items
| # | Action | Owner | Due | Success Criteria |
|---|--------|-------|-----|------------------|
| 1 | ...    | ...   | ... | ...              |

## Patterns (vs. previous sprints)
- [Recurring issue] — appeared in 3/5 last retros
- [Improvement] — resolved since Sprint N-2
```

## 使用建议

- 在斯普林特结束后的24小时内进行回顾会议，此时团队成员的记忆还比较清晰。
- 每次斯普林特最多设定3-5个行动项，否则行动项可能无法得到有效执行。
- 为每个行动项指定一个具体的负责人，避免责任不明确的情况。
- 在每次新的回顾会议开始时，回顾上一次会议中制定的行动项的执行情况。

---

由 [AfrexAI](https://afrexai-cto.github.io/context-packs/) 开发——专为业务团队设计的AI辅助工具包。每个行业工具包售价47美元，或购买完整套餐仅需197美元。