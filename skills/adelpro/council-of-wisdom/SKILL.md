---
name: council-of-wisdom
description: 这是一个多智能体协商系统，包含3个核心智能体以及可扩展的附加智能体。在需要时，该系统能够调用用户工作区中的相关功能或技能。
version: 1.3.0
tags: [agents, routing, multi-agent, council, wisdom, orchestration, decision-making, hub]
---
# 智慧委员会（Council of Wisdom）

这是一个多智能体决策平台，包含3个核心智能体以及可扩展的扩展智能体。

## 何时激活

### 自动触发
- 表示决策的词汇：should I（我应该吗？）、should we（我们应该吗？）、better to（最好...）、which option（哪个选项？）
- 表示风险的词汇：dangerous（危险的）、risk（风险）、worried（担心的）、concerned（担忧的）、scared（害怕的）
- 表示分析或思考的词汇：analyze（分析）、compare（比较）、think（思考）、help me（帮助我）
- 明确的指令：council:（召集委员会）

### 自动跳过
```
hello, hi, hey, thanks, thank you
what time, weather, temperature
yes, no, ok, sure
define, what is
```

## 架构
```
Query → Check Skip List
           │
           ▼ (if not skipped)
    ┌──────────────────┐
    │  CORE AGENTS    │ (always run)
    │ - Intent Decoder│
    │ - Risk Checker  │
    │ - Tone Designer │
    └──────────────────┘
           │
           ▼ (if extended triggered)
    ┌──────────────────┐
    │ EXTENDED AGENTS │ (included)
    └──────────────────┘
           │
           ▼
    ┌──────────────────┐
    │ WORKSPACE SKILLS │ (if needed)
    └──────────────────┘
           │
           ▼
    Enriched Response
```

## 核心智能体（始终运行）

### 意图解析器（Intent Decoder）
用户真正想要什么？

### 风险评估器（Risk Checker）
可能会出现什么问题？

### 语气调节器（Tone Designer）
应该如何表达这个结果？

## 扩展智能体（Included Agents）

| 智能体 | 触发关键词 |
|-------|-----------------|
| 系统设计师（System Designer） | api（应用程序编程接口）、database（数据库）、architecture（架构）、system（系统） |
| 复杂性评估器（Complexity Assessor） | complex（复杂的）、analyze（分析）、compare（比较） |
| 价值守护者（Values Guardian） | ethical（伦理的）、moral（道德的）、values（价值观）、fair（公平的） |

## 调用工作区技能（Calling Workspace Skills）
当需要专业技能时，委员会可以调用工作区中的相关技能。

**示例：**
- 查询关于《古兰经》的信息 → 调用 quran-search-engine-mcp
- 查询关于 GitHub 的信息 → 调用 github-mcp
- 查询关于安全性的信息 → 调用 penetration-tester agent

**添加工作区技能的方法：**
1. 技能文件存放在 `workspace/skills/` 目录下
2. 智能体文件存放在 `workspace/agents/` 目录下
3. 委员会会检测到相关关键词并在需要时调用相应的技能

## 添加自定义扩展智能体
在 `agents/` 目录下创建一个新的 `.md` 文件：

```markdown
# Your Agent Name

Trigger: keyword1, keyword2

Your analysis...
```

## 输出结果

### 隐式模式（默认）
技能在后台运行，通过分析生成响应。

### 显式模式（被请求时）
使用前缀 `council:` 来查看完整的分析结果。

## 简单规则（80% 的价值所在）
```
IF query contains: dangerous, risk, worried, scared
THEN: Risk Checker flag = high

IF query contains: frustrated, angry, upset
THEN: Tone = empathetic
```

## SEO 关键词
多智能体（multi-agent）、AI 路由器（AI router）、智能体委员会（agent council）、决策支持（decision support）、AI 协商（AI deliberation）、可扩展平台（extensible hub）、工作区技能（workspace skills）

**应用场景：**
个人 AI 助手、决策支持、风险评估