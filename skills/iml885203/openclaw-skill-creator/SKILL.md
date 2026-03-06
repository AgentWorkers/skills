---
name: openclaw-skill-creator
description: Create, improve, or evaluate OpenClaw skills (SKILL.md). Use when: (1) designing a new skill from scratch, (2) improving an existing skill's description for better triggering accuracy, (3) evaluating whether a skill description would trigger correctly, (4) reviewing the skill library for quality issues. NOT for: creating Claude Code / Codex skills (those use a different format), editing skill scripts/assets unrelated to skill design.
---

# OpenClaw 技能创建工具

这是一个用于创建和迭代优化 OpenClaw 技能的工具——灵感来源于 Anthropic 的技能创建工具，并根据 OpenClaw 的技能格式进行了适配。

## OpenClaw 技能架构

技能由一个包含 `SKILL.md` 文件的目录以及可选资源组成。

**自定义技能**（用户创建的技能）通常存储在 OpenClaw 工作区中：
```
<workspace>/skills/<skill-name>/
```

**内置技能** 随 OpenClaw 安装程序一起提供。

工作区中的自定义技能优先于同名的内置技能。

### 最小结构

```
<skill-name>/
├── SKILL.md          ← required
└── scripts/          ← optional, executable helpers
```

无需进行任何打包步骤；该目录本身即代表一个技能。

### SKILL.md 格式

```yaml
---
name: skill-name
description: <trigger description — the most important field>
---

# Skill Name

Instructions for the agent...
```

前言部分仅包含 `name` 和 `description` 两个字段，不包含其他字段。

在脚本或说明中可以使用 `{baseDir}` 来引用技能所在的目录：
```bash
python3 {baseDir}/scripts/my_script.py
```

---

## 编写技能描述（最关键的部分）

`description` 字段是触发技能的唯一依据。除非技能被主动调用，否则其内容永远不会被读取。

### 核心原则：

1. **明确提示**：智能体往往不会主动使用某些技能。因此，描述应更具引导性，列出该技能必须使用的具体场景。
2. **明确使用场景与不适用场景**：清晰的结构有助于减少技能被误触发或误判的情况。
3. **包含触发短语**：列出用户常用的表达方式；如果用户使用其他语言进行交流，也应包含相应的短语。
4. **描述功能及使用场景**：不仅要说明技能的功能，还要说明使用它的时机。

### 模板

```
<what the skill does>. Use when: (1) <context 1>, (2) <context 2>, (3) phrases like "<example phrase>". NOT for: <anti-patterns>.
```

### 示例（修改前 vs 修改后）

❌ 修改前：`“使用开始/停止计时器来记录每个项目的工作时间。”`

✅ 修改后：`“用于记录工作时间并生成生产力报告。当用户需要开始/停止计时器、记录项目工作时间或生成时间报告时，可以使用此技能——例如：‘开始计时器’、‘记录我的工作时间’、‘我这周工作了多久’。**不适用于**：日历安排、任务管理。`

---

## 技能创建流程：

### 1. 理解用户需求

询问用户：
- 该技能应该让智能体实现什么功能？
- 该技能应在什么情况下被触发？用户会如何表达这个需求？
- 预期的输出是什么？
- 这个技能是否需要脚本支持，还是仅用于提供指导？

每次只询问一两个问题，避免让用户感到困惑。

### 2. 探讨特殊情况

在编写技能描述之前，需要了解以下内容：
- 输入格式、特殊情况、可能出现的错误情况
- 技能依赖的外部资源（如 API、CLI、文件）
- 该技能不应该执行的操作（这对于明确“不适用场景”非常重要）

### 3. 编写 SKILL.md 文件

- 保持描述内容在 300 行以内，简洁明了
- 仅包含智能体还不知道的信息
- 将详细的参考资料放入 `references/` 文件中，并在 SKILL.md 中添加引用链接
- 如果有重复出现的代码，将其放入 `scripts/` 文件中

### 4. 测试描述的有效性

手动测试技能描述的准确性：
- 编写 5–10 个测试用例（包括应该触发技能的情况和不应该触发的情况）
- 对每个用例询问：“仅根据描述，我是否会选择使用这个技能？”
- 如果正确率低于 80%，则需要改进描述

### 5. 迭代优化

在技能实际应用后：
- 如果技能经常在不应触发时被调用，说明描述过于狭窄，需要添加更多触发短语
- 如果技能在无关请求时也被触发，说明描述过于宽泛，需要添加“不适用场景”
- 如果描述内容过长，可以考虑将其拆分为多个 `references/` 文件

---

## 优化现有技能

当需要优化现有技能时：

1. 阅读当前的 `SKILL.md` 文件
2. 根据上述原则检查描述内容
3. 提出新的描述方案，并说明改进的理由
- 可以运行测试脚本来比较优化前后的触发准确性
- 只有在用户确认后才能进行更新

---

## 技能质量检查清单

在最终确定技能内容之前，请确保满足以下要求：
- [ ] `name` 采用小写驼峰命名法，长度不超过 64 个字符
- [ ] `description` 中包含具体的使用场景
- [ ] `description` 中包含“不适用场景”以防止误判
- [ ] 描述内容不超过 300 行
- [ ] 不包含 README、CHANGELOG 或其他辅助文档（保持技能的简洁性）
- [ ] 脚本已经过测试并且可以正常使用
- [ ] `references/` 文件中的链接清晰，并附有使用说明