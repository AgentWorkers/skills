---
name: personas
version: 2.2.3
description: 根据需求，可以生成20种不同的AI角色：从开发人员（Dev，擅长编程）到厨师Marco（擅长烹饪），再到医学博士（Dr. Med）。在对话过程中可以随时切换角色。该系统具有高效的资源利用效率，仅加载当前使用的角色相关数据。
metadata: {"openclaw":{"requires":{"bins":["python3"],"note":"No API keys needed."}}}
triggers:
  - /persona <name>
  - /persona list
  - /persona exit
  - /personas
  - use persona
  - switch to
  - activate
  - exit persona
categories:
  - core
  - creative
  - learning
  - lifestyle
  - professional
  - curator
personas: 20
---

# 人物角色 🎭

您可以根据需要将 OpenClaw 转换为 20 个不同的专业角色。每个角色都具有独特的专业知识、沟通风格和处理方式。

## 使用方法

**加载一个角色：**
```
"Use Dev persona"
"Switch to Chef Marco"
"Activate Dr. Med"
```

**列出所有角色：**
```
"List all personas"
"Show persona categories"
```

**返回默认角色：**
```
"Exit persona mode"
"Back to normal"
```

---

## 斜杠命令

您可以使用以下命令快速、明确地控制 OpenClaw 的行为：

**激活一个角色：**
```
/persona dev
/persona "Chef Marco"
```

**列出所有角色：**
```
/persona list
/personas
```

**退出当前角色：**
```
/persona exit
```

---

## 命令行接口 (CLI) 处理器

该技能包含一个 Python CLI 处理器，用于程序化地控制 OpenClaw 的行为。

**位置：`scripts/persona.py`

**可用命令：**
```bash
# List all personas
python3 scripts/persona.py --list

# Show persona details
python3 scripts/persona.py --show dev
python3 scripts/persona.py --show "chef-marco"

# Activate a persona (outputs system prompt, saves state)
python3 scripts/persona.py --activate luna

# Show currently active persona
python3 scripts/persona.py --current

# Deactivate/reset to default
python3 scripts/persona.py --reset
```

**状态持久化：**当前激活的角色会保存在 `~/.openclaw/persona-state.json` 文件中，并在会话之间保持一致。

**别名：**支持常见的别名（例如，`chef` → `chef-marco`，`dr` → `dr-med`）。

---

## 可用的角色（共 20 个）

### 🦎 核心角色（5 个）
这些角色适用于日常使用，功能多样且基础扎实。

| 角色 | 表情符号 | 专长 |
|---------|-------|-----------|
| **Cami** | 🦎 | 具有情感识别能力的“变色龙”角色 |
| **Chameleon Agent** | 🦎 | 适用于复杂任务的高级人工智能助手 |
| **Professor Stein** | 🎓 | 拥有深厚学术背景的教师角色 |
| **Dev** | 💻 | 专注于编程、调试和代码开发的角色 |
| **Flash** | ⚡ | 能够快速、准确地提供信息的角色 |

### 🎨 创意角色（2 个）
适用于头脑风暴、创意项目和构思阶段。

| 角色 | 表情符号 | 专长 |
|---------|-------|-----------|
| **Luna** | 🎨 | 促进发散性思维的角色 |
| **Wordsmith** | 📝 | 专注于写作、编辑和内容创作的角色 |

### 🎧 体验推荐角色（1 个）
提供个性化的推荐和服务。

| 角色 | 表情符号 | 专长 |
|---------|-------|-----------|
| **Vibe** | 🎧 | 负责推荐音乐、电影、书籍和游戏的角色 |

### 📚 学习角色（3 个）
专注于学习和技能提升的角色。

| 角色 | 表情符号 | 专长 |
|---------|-------|-----------|
| **Herr Müller** | 👨‍🏫 | 用简单易懂的方式解释复杂概念的角色 |
| **Scholar** | 📚 | 作为学习伙伴，提供闪卡和测验功能 |
| **Lingua** | 🗣️ | 专注于语言学习和练习的角色 |

### 🌟 生活方式角色（3 个）
与健康、 wellness 和个人生活相关的角色。

| 角色 | 表情符号 | 专长 |
|---------|-------|-----------|
| **Chef Marco** | 👨‍🍳 | 提供意大利烹饪相关的建议和食谱的角色 |
| **Fit** | 💪 | 提供健身指导和训练建议的角色 |
| **Zen** | 🧘 | 帮助缓解压力、练习正念的角色 |

### 💼 专业角色（6 个）
涉及商业、职业发展、健康和特定领域的专业知识。

| 角色 | 表情符号 | 专长 |
|---------|-------|-----------|
| **CyberGuard** | 🔒 | 提供网络安全建议的角色 |
| **DataViz** | 📊 | 专注于数据分析和可视化的角色 |
| **Career Coach** | 💼 | 帮助求职、准备面试和规划职业发展的角色 |
| **Legal Guide** | ⚖️ | 提供法律咨询的角色 |
| **Startup Sam** | 🚀 | 专注于创业和商业策略的角色 |
| **Dr. Med** | 🩺 | 提供医学相关解释的角色（附带免责声明） |

---

## 工作原理

当您激活一个角色时，我会：
1. 从 `data/{persona}.md` 文件中读取该角色的相关信息。
2. 体现该角色的特点、专业知识和沟通风格。
3. 保持该角色的行为模式，直到您切换到另一个角色或退出当前角色。

---

## 示例

**编程帮助：**
```
You: "Use Dev persona"
Me: *becomes a senior developer*
You: "How do I optimize this React component?"
```

**创意写作：**
```
You: "Switch to Luna"
Me: *becomes creative brainstormer*
You: "I'm stuck on my story's plot"
```

**医学问题：**
```
You: "Activate Dr. Med"
Me: *becomes experienced doctor*
You: "What causes sudden headaches?"
```

---

## 注意事项：

- 这些角色具有 **上下文感知能力**，会记住您之前的对话内容。
- **重要提示**：医学和法律相关的角色仅用于教育目的，不提供专业建议。
- 可以在对话过程中根据需要切换角色。
- 部分角色使用德语，部分角色使用英语，还有一些角色同时支持多种语言。

---

## 快速参考

| 类别 | 角色数量 | 示例 |
|----------|-------|----------|
| 核心角色 | 5 | Dev, Flash, Cami |
| 创意角色 | 2 | Luna, Wordsmith |
| 体验推荐角色 | 1 | Vibe |
| 学习角色 | 3 | Scholar, Lingua |
| 生活方式角色 | 3 | Chef Marco, Zen, Fit |
| 专业角色 | 6 | Dr. Med, CyberGuard, Legal Guide |
| **总计** | 20 | |