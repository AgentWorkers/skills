---
name: subskill-generation-rule
description: 定义并执行项目组织规则，以生成子技能（subskills）。将生成的推荐结果（recommendation outputs）保存在 `data/` 目录下，将新的功能脚本（feature scripts）放置在 `subskills/<feature>/` 目录中。如果需要，可以在每个功能文件夹内添加 `SKILL.md` 文件，以保持主技能根目录（main skill root）的整洁。
---

# 子技能生成规则

请将以下规则应用于未来的更新：

1. 将新生成的推荐/结果文件存储在 `data/` 目录中。
2. 将新生成的代码脚本放在 `subskills/<feature>/` 目录下。
3. 在 `subskills/` 目录下为每个功能创建一个单独的文件夹。
4. 当需要提供功能的使用说明时，在相应的功能文件夹中添加 `SKILL.md` 文件。
5. 避免将一次性使用的脚本和生成的文件添加到主技能目录（即技能根目录）中。

推荐的文件结构：

```text
<skill>/
  SKILL.md
  config.json
  data/
  subskills/
    <feature-a>/
      SKILL.md
      *.py
    <feature-b>/
      SKILL.md
      *.py
```

## 使用场景

- 创建新的子技能
- 整理现有的功能
- 强制执行文件存放规范
- 保持技能根目录的整洁