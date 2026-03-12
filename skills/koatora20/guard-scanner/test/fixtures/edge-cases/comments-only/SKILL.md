# 边缘情况技能——仅包含注释

该技能中的安全相关关键词仅出现在注释和字符串字面量中，理想情况下这些内容不应触发任何安全检测（用于测试系统的弹性）。

## 说明

通过解释安全概念来帮助用户理解它们。

```javascript
// This is a comment about "ignore all previous instructions" — it's just an example string
// The term "system prompt" appears here for educational purposes
const educationalText = "Example of prompt injection: 'ignore all previous instructions'";
const demo = "This shows how eval() could be misused, but we don't actually call it";

function explain(topic) {
  // We discuss exec() and child_process as security concepts
  return `Security topic: ${topic} — always validate inputs`;
}
```

注意：该文件用于安全教育目的。正则表达式扫描工具可能会将这些安全相关内容标记为潜在风险，因为它们出现在字符串或注释中。