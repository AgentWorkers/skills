---
name: pr-writer
description: 根据你的分支差异（branch diff），生成 Pull Request（PR）的标题和描述。这在你需要快速编写 Pull Request 描述时非常有用。
---

# PR 编写助手

编写 PR 描述是一项没人愿意做，但大家都能从中受益的任务。当你完成一个功能模块的开发后，虽然很清楚具体做了哪些修改，但将这些修改转化为清晰、易懂的 PR 标题和描述却显得非常繁琐。这款工具可以自动读取你的 Git 差异文件（diff），并为你完成全部的工作。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-pr-desc
```

## 功能简介

- 读取当前分支与基础分支（默认为 `main`）之间的差异
- 生成一个简洁明了的 PR 标题，准确概括所做的修改
- 编写详细的 PR 描述，说明修改的内容及原因
- 支持通过 `--base` 标志指定自定义的基础分支
- 适用于任何 Git 仓库，无需任何额外配置

## 使用示例

```bash
# Generate PR description against main branch
npx ai-pr-desc

# Generate against a different base branch
npx ai-pr-desc --base develop

# Generate against a release branch
npx ai-pr-desc --base release/v2.0
```

## 最佳实践

- **先提交代码再使用该工具**：该工具会对比已提交的代码，因此请确保你的代码已经提交完毕
- **保持分支的专注性**：专注于单一功能的分支通常能生成更优质的 PR 描述
- **审核输出结果**：虽然 AI 已经完成了 90% 的工作，但请花 30 秒时间根据团队的风格稍作调整
- **结合持续集成（CI）使用**：将工具的输出结果通过管道（pipe）传递到 GitHub 的 CLI 或 API 调用中，实现 PR 生成的自动化

## 适用场景

- 你刚刚完成一个功能模块，需要快速提交 PR
- 你正在处理多个 PR，不想为每个 PR 都手动编写描述
- 团队要求提供详细的 PR 描述，但你更希望尽快发布代码
- 你希望团队内的 PR 描述保持一致且结构规范

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本无付费门槛、无需注册，也不需要 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-pr-desc --help
```

## 工作原理

该工具通过 `simple-git` 获取当前分支与基础分支之间的差异数据，然后将这些数据发送给 OpenAI 进行分析。OpenAI 会根据分析结果生成相应的 PR 标题和描述。输出结果会直接显示在终端中，你可以将其复制到 PR 文档中。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。