---
name: diff-summarizer
description: 生成易于人类阅读的 Git 差异摘要。当您需要解释发生了哪些更改时，可以使用这种方法。
---

# 差异摘要工具（Diff Summarizer）

Git 差异文件能清晰地显示哪些内容发生了变化，但很难理解这些变化的具体原因。逐行查看那些红色和绿色的代码来理解一系列变更的实际含义，实在是一件非常麻烦的事情。这款工具可以将 Git 差异文件转换成易于理解的中文摘要，非常适合用于变更日志（changelogs）、Pull Request（PR）的描述，或者快速了解最近几次提交的变更内容。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-diff-summary
```

## 功能介绍

- 读取 Git 差异文件并生成清晰、易于阅读的摘要
- 支持任何 Git 参考对象（如 HEAD~3、分支名称、提交哈希值）
- 按文件和变更影响程度对变更进行分类和总结
- 如果未提供参考对象，工具会默认统计未提交的变更
- 生成的摘要可以直接复制到 PR 描述中

## 使用示例

```bash
# Summarize uncommitted changes
npx ai-diff-summary

# Summarize last 3 commits
npx ai-diff-summary HEAD~3

# Compare against main branch
npx ai-diff-summary main

# Summarize a specific commit
npx ai-diff-summary abc123
```

## 最佳实践

- **用于 PR 描述**：在提交 PR 之前，先用该工具处理主分支的差异文件，然后将生成的摘要直接复制到 PR 描述中。审阅者会因此感到非常方便。
- **生成变更日志**：针对最新发布的标签运行该工具，为用户生成易于阅读的变更日志。
- **保持差异文件的大小适中**：与代码审查类似，较小的差异文件能生成更准确的摘要。如果需要总结 500 个文件的变更，输出内容的效果会大打折扣。
- **结合提交信息使用**：该工具生成的摘要能补充提交信息中可能缺失的上下文信息，两者结合使用可提供更完整的文档。

## 适用场景

- 在编写 PR 描述时，不想手动列出所有变更内容
- 从多个提交中生成发布说明
- 在审阅他人分支的代码之前，快速了解其中发生了哪些变更
- 在离开项目一段时间后，快速了解项目的最新进展

## 工作原理

该工具会使用您提供的 Git 参考对象（或默认使用未提交的变更）来执行 `git diff` 命令，然后将差异结果发送给 AI 模型进行处理。AI 模型会解析这些变更，并生成按影响程度和文件分类的摘要。

## 系统要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。该工具必须位于 Git 仓库内部。

```bash
npx ai-diff-summary --help
```

## 属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多款免费开发工具之一。所有工具均免费提供，无需注册或支付 API 密钥。只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。