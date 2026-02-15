---
name: github-copilot-cli
description: **GitHub Copilot CLI的高效日常使用方法（适用于高级工程师）**  
在规划、编写代码、审查代码或执行一系列Copilot CLI命令时，可充分利用GitHub Copilot CLI来探索代码库、起草代码修改方案、调试问题，从而加速工作流程，同时确保不破坏项目的整体架构设计。
---

# GitHub Copilot CLI – 高效的工作流程

## 前置内容格式检查（请先执行此步骤）
GitHub Copilot 对前置内容的格式要求非常严格，哪怕是一个多余的空格都可能导致格式错误。

在提交或发布代码之前，请执行以下操作：
```bash
# Basic sanity check (no output = good)
python - <<'PY'
import yaml,sys
with open('SKILL.md') as f:
    yaml.safe_load(f.read())
print('Frontmatter OK')
PY
```

需要记住的规则：
- 关键字（如 `name`、`description`）前不允许有前导空格
- 使用空格而非制表符
- 前置内容应保持简洁，仅包含 `name` 和 `description` 两个字段

---

## 心理模型
将 Copilot CLI 视为一个由你协调的精英专家团队：
- 一个 Copilot 实例可以扮演前端工程师的角色
- 一个扮演后端工程师的角色
- 一个扮演测试员/质量保证（QA）的角色
- 一个扮演基础设施或重构专家的角色

当为 Copilot 明确分配角色时，它在编码和架构设计方面表现出色。而你的角色则是 **技术总监/协调者**：
- 明确目标和约束条件
- 让各个 Copilot 实例提出解决方案
- 关注各种权衡和潜在冲突
- 在必要时将决策或风险上报给你

---

## 你应该实际使用的核心命令

### 1. 询问关于代码库的问题
```bash
gh copilot explain "What does this service do?" --path src/
```
在熟悉代码库或休息后重新获取代码上下文时使用此命令。

---

### 2. 生成针对性的代码修改建议
```bash
gh copilot suggest "Add logging when translation fallback is used" --path services/translation
```
**最佳实践**：
- 将请求描述为具体的代码修改内容（即“代码差异”，而非功能需求）
- 确保请求针对特定的目录

---

### 3. 在特定约束条件下进行调试
```bash
gh copilot suggest "Why might this function return null under load?" --path src/choreo
```
根据提示内容手动查看相关代码以进行调试。

---

### 4. 先测试再编码
```bash
gh copilot suggest "Write failing tests for punctuation correction on voice transcription" --path tests/
```
之后自行迭代以实现修复。

---

## 有效的提示语句示例

### ✅ 正确的提示（明确角色）
- “作为后端工程师，请为 X 代码编写一个最小的修复方案”
- “作为测试员，请添加防护措施，确保 Y 情况不会发生”
- “作为基础设施专家，请重构这段代码以提高安全性，而非仅追求速度”

### ❌ 错误的提示
- “从头到尾实现功能 X”
- “重构整个服务”
- “使代码具备生产环境适用性”

---

## 多个 Copilot 实例的协作流程（推荐）

1. **分解问题（技术总监的职责）**
   - 明确目标和约束条件
   - 将问题分解为前端、后端、测试和基础设施方面的问题

2. **提出解决方案（各 Copilot 实例的职责）**
```bash
gh copilot suggest "As a backend engineer, propose a minimal fix for mixed-language carryover" --path src/

gh copilot suggest "As a tester, write failing tests for mixed-language carryover" --path tests/
```

3. **相互验证（不同 Copilot 实例之间的讨论）**
   - 比较各个方案
   - 发现潜在的不一致或假设

4. **上报问题（给你）**
   - 指出各种权衡因素和风险
   - 请求你的决策

5. **最终确定（由你完成）**
   - 应用修改
   - 优化代码命名
   - 有意识地进行代码合并

---

## 何时不应使用 Copilot CLI
在以下情况下，Copilot CLI 不应作为最终决策依据：
- 当产品或组织层面的权衡优先于代码的正确性时
- 需要跨仓库或跨团队协作时
- 涉及安全、隐私或合规性决策时
- 当代码的正确性依赖于实际运行环境的行为时

在这些情况下，Copilot 仍可以提供修改建议，但最终决策仍需由你做出。

---

## 黄金法则
Copilot 是一个辅助工具，而非决策的最终决定者。

使用 Copilot 的目的是：
- 生成多种实现方案
- 揭露潜在的假设
- 从多个角度验证想法的可行性

最终决策权仍在你手中：
- 你负责确定代码的最终用途
- 你需承担相关风险
- 你负责合并修改后的代码

Copilot 可以加速思考过程，但它不能替代你的判断力。