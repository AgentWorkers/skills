---
name: agent-memory-templates
version: 1.0.0
description: "这些内存模板已经过生产环境的测试，适用于AI代理程序。其中包括SOUL.md个性模板、内存检查点配置、观察型记忆设置，以及100个用于引导AI代理行为的提示语。这些模板由ClawVault的开发者团队开发。"
metadata:
  openclaw:
    emoji: "🧠"
---
# 代理内存模板

这些模板经过生产环境的测试，可用于构建具有内存功能的AI代理。

## 包含的内容

### 免费模板
- 内存检查点模板
- 会话交接模板
- 上下文恢复机制模板
- 日志生成器模板
- 决策记录格式模板

### 高级内容
如需获取完整的100个提示语句、12种人格模板以及完整的内存架构文档：

- **100个高级提示语句（9美元）**：https://whop.com/checkout/plan_W7BJwJmYlXsjF
- **完整套餐（47美元）**：https://whop.com/checkout/plan_umnonnlgKVjvo
- **免费提示语句预览**：https://prompts.versatlygroup.com
- **免费快速参考指南**：https://cheatsheet.versatlygroup.com

## 快速入门

```bash
# Use the memory checkpoint pattern
clawvault checkpoint --working-on "your task" --focus "key details"

# Use the session handoff
clawvault sleep "what you accomplished" --next "what's next"

# Recovery on wake
clawvault wake
```

## 由Versatly开发
https://store.versatlygroup.com | https://clawvault.dev