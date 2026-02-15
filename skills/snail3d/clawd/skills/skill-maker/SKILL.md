---
name: skill-maker
description: 创建、打包并发布 Clawdbot 技能（Skills）。该过程会生成 SKILL.md 文件、样板代码（boilerplate code）、README 文档，并准备可用于 GitHub 和 Skill Hub 的可发布压缩文件（zip files）。
---

# 🛠️ Skill Maker

这是一个用于从想法到发布的过程中创建和打包 Clawdbot 技能的工具。

## 功能介绍

1. **向您询问关于技能的相关信息**（例如：技能名称、功能、触发条件、可执行的命令等）。
2. **生成包含元数据的 SKILL.md 文件**。
3. **自动生成必要的代码模板**（如脚本、程序入口点等）。
4. **生成用于 GitHub 的 README.md 文档**。
5. **将所有生成的文件打包成一个可发布的 zip 文件**。

## 使用方法

```bash
node ~/clawd/skills/skill-maker/trigger.js
```

或者直接对 Clawd 说：“创建一个新技能”。

## 技能创建流程

```
You describe skill → Skill Maker generates files → You review/edit → Zip ready for GitHub/Skill Hub
```

## 生成的结构

```
your-skill/
├── SKILL.md           # Skill metadata + documentation
├── README.md          # GitHub readme
├── scripts/           # Main scripts (if needed)
├── references/        # Docs/references (optional)
└── *.zip              # Publishable package
```

## 发布流程

1. 使用 Skill Maker 创建技能。
2. 将生成的文件推送到 GitHub（作为仓库）。
3. 从 GitHub 或本地下载 zip 文件。
4. 将 zip 文件上传到 Skill Hub（clawdhub.com）。

## 已创建的技能示例：

- **pomodoro**：带有任务跟踪功能的计时器。
- **skill-defender**：安全扫描工具。
- **skill-maker**：这个工具本身！

## 注意事项：

- 所有的代码提交都会包含一个“Buy Me a Coffee”的链接。
- 默认存储路径：`~/clawd/skills/`。
- 打包后的 zip 文件已经包含了 `.gitattributes` 文件，可以直接用于上传到 GitHub。

---

由 Clawd 使用 💜 构建 | ☕ https://www.buymeacoffee.com/snail3d