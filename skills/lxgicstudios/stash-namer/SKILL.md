---
name: stash-namer
description: 使用 AI 为你的 Git 临时存储（stash）起一个有意义的名称。这样在以后需要查找这些临时存储时会更加方便。
---

# Stash Namer

“WIP”（进行中）和“temp changes”（临时更改）这样的标签根本无法让你了解实际的变更内容。这个工具会根据你实际所做的更改来为你的代码仓库中的临时存储区（stash）命名，从而帮助你快速找到所需的临时存储区，而无需逐一查看它们。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-stash-name
```

## 功能介绍

- 分析你已暂存或未暂存的更改
- 生成一个描述性的临时存储区名称
- 将代码存入对应的临时存储区
- 使 `git stash list` 命令真正发挥其作用（即能够清晰地显示所有临时存储区的内容）

## 使用示例

```bash
# Stash current changes with a good name
npx ai-stash-name

# Preview the name without stashing
npx ai-stash-name --dry-run

# Include untracked files
npx ai-stash-name --include-untracked

# Custom prefix for team conventions
npx ai-stash-name --prefix "WIP:"
```

## 最佳实践

- **为每个临时存储区起名**：带有名称的临时存储区更易于管理。
- **包含相关票号**：使用 `--prefix` 参数加上你的票号作为临时存储区的名称前缀。
- **在使用前先查看内容**：名称能让你清楚地知道临时存储区中包含哪些更改。
- **定期清理旧临时存储区**：虽然这些临时存储区仍有用，但不要让它们堆积太多。

## 适用场景

- 需要快速切换工作环境但不想提交更改。
- 在进行实验时需要保存进度。
- 在不同功能之间同时进行多个未完成的更改。
- 团队使用共享分支时，需要清晰的临时存储区名称。

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-stash-name --help
```

## 工作原理

首先运行 `git diff` 来查看哪些内容发生了更改，然后将差异摘要发送给 GPT（Generative Pre-trained Transformer），从而获得一个简洁且描述性强的临时存储区名称。接着使用 `git stash push -m` 命令将该名称应用于相应的临时存储区。虽然简单，但确实解决了许多实际使用中的麻烦问题。

## 许可证

采用 MIT 许可证。永久免费，你可以随意使用该工具。