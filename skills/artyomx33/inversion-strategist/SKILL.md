---
name: inversion-strategist
description: 将问题反过来思考——不要问“如何成功”，而要问“如何肯定会失败”，然后避开那些可能导致失败的道路。当用户提到“反转”、“逆向思考”、“采取相反的方法”、“这种情况会如何失败”、“如何避免失败”、“不应该做什么”、“反目标”或“确保失败”时，就可以使用这种思考方式。
---

# 逆向策略师（Inversion Strategist）

## 核心原则

“总是采取逆向思维。”——卡尔·雅可比（Carl Jacobi）

与其问：“我该如何实现目标X？”
不如问：“什么行为会确保我无法实现目标X？”
然后，系统性地避免这些行为。

## 实施步骤：

1. **明确目标**
2. **进行逆向思考**：“什么行为会导致失败？”
3. **列出可能导致失败的各种情况**（7-10种，包括明显和隐蔽的）
4. **分类**：致命性错误、造成损害的行为、令人烦恼的行为
5. **制定相应的规避策略**
6. **创建反检查清单（anti-checklist）**

## 输出格式

```
GOAL: [What you want]
INVERTED: "How would I guarantee failure at [goal]?"

FAILURE PATHS:

🔴 FATAL:
• [Path] → AVOID BY: [Strategy]

🟡 DAMAGING:
• [Path] → AVOID BY: [Strategy]

🟢 ANNOYING:
• [Path] → AVOID BY: [Strategy]

ANTI-CHECKLIST:
□ Never [behavior]
□ Never [behavior]

PRO-CHECKLIST:
□ Always [opposite of failure]
□ Always [opposite of failure]
```

## 查理·芒格的智慧

“像我们这样的人之所以能够获得长期的优势，是因为我们始终努力避免犯愚蠢的错误，而不是试图变得非常聪明。”

“只要告诉我我可能会死在哪里，我就永远不会去那里。”

## 集成方式：

该策略可与以下工具/方法结合使用：
- **first-principles-decomposer**：在逆向思考后，从基本原理出发重新构建系统
- **pre-mortem-analyst**：通过逆向思维找出潜在问题，并进行压力测试
- **six-thinking-hats**：其中“黑帽思维”（Black Hat Thinking）是一种简化版的逆向分析方法；将这两种方法结合使用可进行全面的分析

---
有关Artem特定应用中的逆向思维案例，请参阅 references/examples.md 文件。