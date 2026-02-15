---
name: changelog-gen
description: 从 Git 历史记录中生成变更日志。当您需要快速生成发布说明时，可以使用此功能。
---

# 变更日志生成器

手动编写变更日志非常繁琐。这个工具可以读取两个 Git 参考引用（refs）之间的历史记录，并生成格式规范的变更日志条目。再也不用复制粘贴提交信息了。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-changelog --from v1.0.0 --to v2.0.0
```

## 功能介绍

- 读取任意两个 Git 参考引用（标签、分支、提交）之间的历史记录
- 将提交信息分类为“新增”、“修改”、“修复”或“删除”
- 将杂乱的提交信息整理成易于阅读的条目
- 生成适合用于 `CHANGELOG.md` 文件的 Markdown 格式内容

## 使用示例

```bash
# Between two tags
npx ai-changelog --from v1.0.0 --to v2.0.0

# From a tag to HEAD
npx ai-changelog --from v1.0.0 --to HEAD

# Write directly to file
npx ai-changelog --from v1.0.0 --to v2.0.0 -o CHANGELOG.md

# Specific commit range
npx ai-changelog --from abc123 --to def456
```

## 最佳实践

- **为版本添加标签**：这会让生成变更日志变得更加容易
- **编写规范的提交信息**：提交的内容质量直接影响生成的变更日志质量
- **审核生成的日志**：虽然 AI 可能会错误分类某些更改，但审核仍然很重要
- **在发布前运行该工具**：将其作为发布流程的一部分

## 适用场景

- 准备发布版本时需要生成变更日志
- 你忘记维护变更日志，需要补录相关信息
- 希望所有版本的变更日志格式保持一致
- 为 GitHub 版本生成发布说明

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-changelog --help
```

## 工作原理

该工具会读取你指定的 Git 参考引用之间的提交记录，收集所有提交信息，并将这些信息发送给 GPT-4o-mini。AI 会解析这些提交信息，理解每个更改的具体内容，并将其按照规范的格式（如 Keep a Changelog 格式）进行整理。

## 许可证

MIT 许可证。永久免费使用，你可以随意使用该工具。