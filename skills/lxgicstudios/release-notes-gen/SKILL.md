---
name: release-notes-gen
description: 将 Git 历史记录转换为可读的发布说明。在发布版本时使用这些说明。
---

# 生成发布说明的工具

提交信息是为开发者准备的，而发布说明则是为用户准备的。这个工具可以将你混乱的 Git 日志转换成清晰、分类整齐的发布说明。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-release-notes --from v1.0.0
```

## 工作原理

- 读取提交记录或变更日志文件
- 按类别对变更内容进行分组
- 清除技术术语，使其更易于理解
- 支持多种表达风格（正式或非正式）

## 使用示例

```bash
# From git history
npx ai-release-notes --from v1.0.0

# Make it fun
npx ai-release-notes --from v1.0.0 --tone fun

# Between two tags
npx ai-release-notes --from v1.0.0 --to v2.0.0

# From changelog file
npx ai-release-notes --changelog CHANGELOG.md
```

## 最佳实践

- **针对目标用户撰写**：用户并不关心内部的代码重构细节
- **突出显示会导致问题的变更**：确保用户能够注意到这些变更
- **将相关的变更归类在一起**：例如功能更新、错误修复、性能改进等
- **保持格式一致**：每次发布时都使用相同的格式

## 适用场景

- 发布 GitHub 版本更新
- 撰写关于软件更新的博客文章
- 与用户沟通
- 制作营销用的变更日志

## 本工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-release-notes --help
```

## 工作机制

该工具会读取你的 Git 历史记录或变更日志，解析其中的技术变更内容，并将其转换成用户易于理解的语言。同时支持多种表达风格（从正式到非正式）。

## 许可证

采用 MIT 许可证，永久免费。你可以随意使用该工具。