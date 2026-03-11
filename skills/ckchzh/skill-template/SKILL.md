---
name: skill-template
description: "OpenClaw 技能模板生成器：用于创建技能框架、验证结构、优化 SKILL.md 文件内容、生成命令框架、提供使用技巧，并发布相关检查清单及示例技能。支持的功能包括：创建新技能、验证技能结构、优化现有技能内容、提供使用建议、发布技能信息以及生成示例代码。适用于技能开发、AgentSkill 的编写及新技能的创建过程。"
---
# 🧩 技能模板

> 专为 OpenClaw 技能开发者设计。该模板可与现有的技能创建工具（下载量超过 3 万次）相媲美。

## 为什么需要这个技能模板？

创建 OpenClaw 技能需要遵循特定的目录结构和规范。如果手动完成这些步骤，很容易遗漏关键的部分。技能模板可以自动化整个流程——从生成基础框架到进行发布前的检查。

## 命令

```bash
bash scripts/skill-tmpl.sh <command> <skill_name> [options]
```

### 🚀 创建阶段
| 命令 | 用途 |
|---------|---------|
| `create <名称>` | 生成完整的技能目录（包括 SKILL.md、tips.md 和脚本文件） |
| `commands <名称>` | 生成用于编写 Bash 命令的模板 |
| `tips <名称>` | 生成 tips.md 模板 |
| `examples` | 查看示例技能以获取参考 |

### ✅ 验证阶段
| 命令 | 用途 |
|---------|---------|
| `validate <目录>` | 根据规范检查技能目录的结构 |
| `enhance <目录>` | 分析技能文件并提出改进建议 |
| `publish <目录>` | 进行发布前的全面检查 |

## 推荐的工作流程

1. 使用 `create` 命令生成基础框架 → 使用 `commands` 命令编写逻辑 → 使用 `tips` 命令添加实用建议 |
2. 完成后：执行 `validate` 和 `enhance` 命令进行验证和优化 → 最后执行 `publish` 命令进行发布 |
3. 可以通过查看 `examples` 文件来学习其他优秀技能的编写方法

## 标准的技能结构

```
my-skill/
├── SKILL.md          # Required: frontmatter + docs
├── tips.md           # Recommended: usage tips
└── scripts/
    └── main.sh       # Recommended: executable script
```