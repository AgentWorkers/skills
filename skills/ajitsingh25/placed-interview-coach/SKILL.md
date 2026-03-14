---
name: placed-interview-coach
description: 此技能适用于用户希望进行“模拟面试”、“面试练习”、“面试准备”、“系统设计面试”、“行为面试”、“STAR故事分享”或“面试辅导”的情况，同时也适用于希望通过placed.exidian.tech上的Placed职业平台来准备技术面试的用户。
version: 1.0.0
metadata: {"openclaw":{"emoji":"🎯","homepage":"https://placed.exidian.tech","requires":{"env":["PLACED_API_KEY"]},"primaryEnv":"PLACED_API_KEY"}}
---
# Placed 面试辅导工具

Placed 平台提供基于人工智能的面试准备服务。

## 前提条件

需要安装 Placed MCP 服务器。安装方法如下：
```json
{
  "mcpServers": {
    "placed": {
      "command": "npx",
      "args": ["-y", "@exidian/placed-mcp"],
      "env": {
        "PLACED_API_KEY": "your-api-key",
        "PLACED_BASE_URL": "https://placed.exidian.tech"
      }
    }
  }
}
```
请在 https://placed.exidian.tech/settings/api 获取您的 API 密钥。

## 可用工具

- `start_interview_session` — 为特定职位开始模拟面试
- `continue_interview_session` — 回答问题并获取实时反馈
- `get_interview_feedback` — 获取详细的面试表现分析
- `list_interview_cases` — 浏览系统设计案例
- `start_system_design` — 开始系统设计面试（支持 URL 缩短、Twitter、Netflix、Uber 等主题）
- `get_behavioral_questions` — 获取 STAR 格式的行为面试问题
- `save_story_to_bank` — 保存 STAR 面试案例以供多次面试使用

## 面试类型

### 技术面试（编程）

- **开始模拟面试**：
  ```
start_interview_session(
  resume_id="your-resume-id",
  job_title="Senior Software Engineer",
  difficulty="hard",
  company="Google"
)
```

- **回答问题**：
  ```
continue_interview_session(
  session_id="session-123",
  user_answer="I would use a hash map to store key-value pairs for O(1) lookup..."
)
```

- **获取表现反馈**：
  ```
get_interview_feedback(session_id="session-123")
```

### 系统设计面试

- **查看可用案例**：
  ```
list_interview_cases()
# Returns: Design Twitter, Design URL Shortener, Design Netflix, Design Uber, etc.
```

- **开始系统设计面试**：
  ```
start_system_design(
  case_id="design-twitter",
  difficulty="senior"
)
```

**系统设计框架**：
  1. **需求分析** — 功能性需求和非功能性需求
  2. **高层架构** — 组件、数据流、API 设计
  3. **数据库设计** — 数据库模式、索引、复制、分片
  4. **可扩展性** — 负载均衡、缓存、内容分发网络（CDN）、水平扩展
  5. **容错性** — 冗余机制、故障转移、监控
  6. **权衡** — CAP 定理（一致性、可用性、分区容错性）

### 行为面试

- **获取目标职位的行为面试问题**：
  ```
get_behavioral_questions(
  target_role="Engineering Manager",
  focus_categories=["leadership", "conflict-resolution", "failure"]
)
```

**STAR 回答方法**：
  - **情境描述**：描述面试背景和具体情境
  - **任务说明**：说明你的职责和面临的挑战
  - **行动步骤**：详细说明你的具体操作
  - **结果与指标**：说明行动的结果及相关指标

### STAR 面试案例库

- **保存面试案例**：
  ```
save_story_to_bank(
  situation="Led team through major refactor",
  task="Reduce technical debt while shipping features",
  action="Created phased plan, mentored junior devs, set clear milestones",
  result="30% faster deployments, improved morale, reduced bugs by 25%",
  category="leadership"
)
```

## 面试流程

1. **准备阶段**：研究公司信息，查阅简历，利用相关资源进行练习
2. **开始面试**：使用简历和目标职位信息开始模拟面试
3. **回答问题**：边思考边回答问题，并解释你的思考过程
4. **获取反馈**：每回答完一个问题后，查看反馈意见
5. **反复练习**：多次练习，改进薄弱环节
6. **保存案例**：将 STAR 面试案例保存到数据库中，以便后续面试使用

## 技巧建议

**技术面试**：
- 在开始编写代码之前先明确需求
- 讨论各种权衡因素（如时间与空间、简洁性与优化之间的平衡）
- 用实际例子测试你的解决方案
- 清晰地解释你的思考过程

**系统设计面试**：
- 从需求和约束条件出发进行设计
- 绘制图表并解释各个组件
- 分析可扩展性的瓶颈
- 考虑可能的故障场景

**行为面试**：
- 一致地使用 STAR 回答方法
- 提供具体的指标和结果
- 展示自己的成长和学习过程
- 保持真实和诚恳的态度