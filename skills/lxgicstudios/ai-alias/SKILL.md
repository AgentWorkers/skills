---
name: alias-gen
description: 根据您的命令历史记录生成 shell 别名，以便简化终端工作流程。
---

# Shell 别名生成器

该工具会分析您的命令历史记录，并为您经常使用的命令推荐别名。例如，您可以输入 `gco` 代替 `git checkout`。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-alias
```

## 功能介绍

- 读取您的 shell 历史记录（支持 bash、zsh、fish）
- 找出您频繁输入的长命令
- 生成易于记忆的别名
- 生成适用于您当前环境的正确 shell 语法
- 将相关的命令组合在一起

## 使用示例

```bash
# Analyze and suggest aliases
npx ai-alias

# Generate for specific shell
npx ai-alias --shell zsh

# From specific commands
npx ai-alias "docker compose up, git status, npm run dev"
```

## 使用建议

- **别名应简短**：2-4 个字符最为理想
- **易于记忆**：例如使用 `gc` 代替 `git commit`
- **避免冲突**：不要覆盖现有的命令
- **做好文档记录**：在别名文件中添加注释

## 适用场景

- 当您发现自己每天都在重复输入相同的命令时
- 在新机器上设置环境时
- 教授他人您的工作流程时
- 审查自己最常使用的命令时

## 本工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也无需 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-alias --help
```

## 工作原理

该工具会解析您的 shell 历史记录文件，统计命令的使用频率，过滤掉包含敏感数据的命令，并生成相应的别名定义。它采用的命名规则使得别名易于记忆。

## 许可证

采用 MIT 许可协议，永久免费使用。您可以随心所欲地使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-alias](https://github.com/lxgicstudios/ai-alias)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)