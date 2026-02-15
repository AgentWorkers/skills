# 自适应学习代理

**实时从错误和修正中学习，通过捕捉失败情况、用户反馈以及成功模式不断改进。**

免费且开源（MIT许可证）• 无依赖项 • 本地运行

---

## 🚀 为什么需要这个技能？

### 问题描述
使用Claude或任何AI代理时，都会遇到以下情况：
- 需要修正的错误
- API的意外行为
- 通过实验发现的更好方法
- 使用过程中暴露的知识空白

但目前没有系统化的方法可以从这些情况中学习，并在下次使用时应用这些知识。

### 解决方案
**自适应学习代理**能够自动捕捉每一个错误、修正以及成功的模式。然后在再次遇到类似问题时，会检索相关的学习内容。

### 实际应用场景
- **错误发现**：记录一次错误，以后再也不用为此烦恼
- **提示优化**：跟踪哪些提示变体最有效
- **API集成**：记住API的独特行为和解决方法
- **工作流程改进**：记录快捷方式和最佳实践
- **团队知识**：跨项目导出和分享学习成果

---

## ✨ 你将获得什么

### 四大核心功能

**1. 记录学习内容**
```python
agent.record_learning(
    content="Use claude-sonnet for 90% of tasks—faster and cheaper",
    category="technique",
    context="Model selection"
)
```
捕捉成功的模式、见解和最佳实践。

**2. 记录错误**
```python
agent.record_error(
    error_description="JSON parsing failed on null values",
    context="Processing API response",
    solution="Add null check before parsing"
)
```
自动记录失败情况及其解决方案。

**3. 搜索和检索学习内容**
```python
results = agent.search_learnings("JSON parsing")
recent = agent.get_recent_learnings(limit=5)
by_category = agent.get_learnings_by_category("bug-fix")
```
需要时立即找到相关知识。

**4. 查看总结**
```python
summary = agent.get_learning_summary()
print(agent.format_learning_summary())
```
一目了然地了解你学到了什么。

### 主要特性
✅ **无依赖项** - 纯Python代码，可在任何地方运行
✅ **仅本地存储** - 所有数据都存储在你的机器上，无需上传
✅ **MIT许可证** - 可免费使用、修改、分叉和重新分发
✅ **自动分类** - 错误会被转化为学习内容
✅ **搜索和过滤** - 可按关键词或类别查找知识
✅ **导出功能** - 以JSON格式分享学习成果
✅ **无需API密钥** - 完全无需外部凭证

---

## 📊 实际示例

```python
from adaptive_learning_agent import AdaptiveLearningAgent

# Initialize agent
agent = AdaptiveLearningAgent()

# Day 1: Discover a bug
agent.record_error(
    error_description="Anthropic API rejects prompts with excessive newlines",
    context="Testing prompt with formatted lists",
    solution="Use \\n.strip() to clean whitespace before sending"
)

# Day 2: Same bug, but now you have the solution
similar_errors = agent.search_learnings("newlines")
# Result: [Previous learning with solution] ✅

# Week 1: Document successful pattern
agent.record_learning(
    content="Always use temperature=0 for deterministic output in tests",
    category="best-practice",
    context="Prompt engineering"
)

# Get weekly summary
summary = agent.get_learning_summary()
print(f"You've recorded {summary['total_learnings']} learnings this week!")
print(f"Resolved {summary['error_statistics']['resolved']} errors")
```

---

## 🔧 安装
无需安装！该技能仅使用纯Python代码，没有任何依赖项。

```bash
# Copy the adaptive_learning_agent.py file to your project
# Or import it directly:

from adaptive_learning_agent import AdaptiveLearningAgent
```

---

## 💡 使用场景

### 软件开发
记录你发现的错误及其解决方法。下次遇到类似错误时，可以直接使用已有的解决方案。

```python
agent.record_error(
    error_description="Port 8000 already in use",
    context="Running local dev server",
    solution="Use `lsof -i :8000` to find process, then kill it"
)
```

### 提示工程
跟踪适用于特定场景的提示技巧。

```python
agent.record_learning(
    content="Chain-of-thought works better for math problems, direct answers for facts",
    category="technique"
)
```

### API集成
记住每个API的独特行为和解决方法。

```python
agent.record_learning(
    content="OpenAI API requires explicit 'assistant' role messages",
    category="api-endpoint",
    context="Chat completion endpoint"
)
```

### 团队知识
导出学习成果并与团队或未来项目共享。

```python
agent.export_learnings("team_learnings.json")
# Share this file with teammates
```

### 持续改进
在开始重要任务之前，回顾已学到的内容，避免重复犯错。

```python
summary = agent.get_learning_summary()
unresolved = summary['error_statistics']['unresolved']
if unresolved > 0:
    print(f"⚠️ {unresolved} unresolved errors—review before proceeding")
```

---

## 📚 分类
记录学习内容时，可以选择以下分类：

| 分类 | 用途 |
|----------|---------|
| **技术** | 工作方法、途径、策略 |
| **错误修复** | 错误及其解决方案 |
| **API端点** | API的特定行为和特性 |
| **限制** | 约束条件、边界 |
| **最佳实践** | 推荐的模式和标准 |
| **错误处理** | 如何处理特定类型的错误 |

---

## 🎯 来源
记录学习内容时，请指定来源：
- `user-correction` - 用户指出问题所在
- `error-discovery` - 你找到了错误的解决方法
- `successful-pattern` | 你发现了有效的解决方案
- `user-feedback` | 用户提出了改进建议

---

## 📖 API参考

### 核心方法

#### `record_learning(content, category, source, context)`
记录一个成功的模式或见解。

**参数：**
- `content` (str, 必需)：学到的内容
- `category` (str)：上述分类之一
- `source` (str)：上述来源类型之一
- `context` (str)：关于该内容的上下文（可选）

**返回：** 包含ID和时间戳的`Learning`对象

#### `record_error(error_description, context, solution, prevention_tip)`
记录错误及其解决方案（可选）。

**参数：**
- `error_description` (str, 必需)：出错的原因
- `context` (str, 必需)：尝试的操作
- `solution` (str)：解决方法
- `prevention_tip` (str)：如何预防错误

**返回：** 包含ID的`Error`对象

#### `search_learnings(query)`
按关键词或类别搜索学习内容。

**参数：**
- `query` (str)：搜索词

**返回：** 按相关性排序的`Learning`对象列表

#### `get_recent_learnings(limit)`
获取最新的学习内容。

**参数：**
- `limit` (int)：返回的数量（默认：10）

**返回：** 最新的`Learning`对象列表

#### `get_learning_summary()`
获取学习内容和错误的综合总结。

**返回：** 包含统计信息和最新条目的字典

#### `export_learnings(output_file)`
将所有学习内容和错误导出为JSON文件。

**参数：**
- `output_file` (str)：JSON文件的保存路径（默认：`learnings_export.json`）

---

## 🔒 隐私与安全
- ✅ **无数据传输** - 无数据发送到外部
- ✅ **仅本地存储** - 所有数据存储在机器上的`.adaptive_learning/`目录
- ✅ **无需API调用** - 完全离线运行
- ✅ **无需认证** - 无需账户、密钥或登录
- ✅ **完全透明** - 源代码公开且开源

---

## 🤝 贡献
该技能采用MIT许可证，由社区维护。我们鼓励你：
- 分支仓库
- 提交改进和功能
- 将其集成到你的项目中
- 与他人分享学习成果

---

## 📝 更新日志

### [1.0.0] - 2026-02-14

#### ✨ 初始版本
- **核心学习系统** - 记录和检索学习内容
- **错误跟踪** - 捕捉错误及其解决方案
- **搜索功能** - 按关键词或类别查找学习内容
- **本地存储** - 所有数据保存在本地
- **导出功能** - 以JSON文件形式分享学习成果
- **无依赖项** - 纯Python代码，无需外部包
- **MIT许可证** - 可免费使用、修改和重新分发
- **简洁的API** - 简单、符合Python风格的接口

---

## 📞 支持
- **GitHub**：https://github.com/clawhub-skills/adaptive-learning-agent
- **问题与贡献**：在GitHub上提交问题或拉取请求
- **社区**：分享你的学习成果和改进方案！

---

## 📄 许可证
**MIT许可证** - 免费且开源

你可以自由使用、修改、分叉和重新分发。详细信息请参阅[LICENSE.md](LICENSE.md)。

```
Copyright © 2026 UnisAI Community
```

---

**最后更新时间**：2026年2月14日
**当前版本**：1.0.0
**状态**：活跃且由社区维护

免费使用、修改和分叉。无任何限制。