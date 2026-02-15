---
name: release-gen
description: 根据提交历史记录生成语义版本号（semantic version numbers）和 Git 标签（git tags）。在准备发布版本时可以使用这些信息。
---

# Release Gen

判断是应该发布一个重大版本（major）、次要版本（minor）还是补丁版本（patch）是一件繁琐的事情。这个工具会分析自上次创建标签以来的所有提交记录，然后确定合适的版本更新方式，并生成相应的标签以及更新变更日志（changelog）。

**只需一个命令，无需任何配置设置，即可使用。**

## 快速入门

```bash
npx ai-release
```

## 功能介绍

- 分析自上次创建标签以来的所有提交记录，以确定版本更新方式
- 遵循语义化版本命名规则（major.minor.patch）
- 生成带有注释的 Git 标签
- 生成变更日志条目
- 支持常规的提交格式，但也能兼容任何类型的提交方式

## 使用示例

```bash
# Analyze and suggest version bump
npx ai-release

# Create the release (tag + changelog)
npx ai-release --create

# Force a specific bump type
npx ai-release --bump major

# Preview without making changes
npx ai-release --dry-run

# Include pre-release tag
npx ai-release --prerelease beta
```

## 最佳实践

- **使用常规的提交格式**（如 `feat:`、`fix:`、`BREAKING CHANGE:`）：这有助于提高分析的准确性
- **先进行测试运行**：在创建标签之前，先查看实际效果
- **审核变更日志**：虽然 AI 能够很好地整理内容，但你可能仍需要对其进行编辑
- **仅在主分支（main branch）上创建标签**：避免在功能分支（feature branches）上发布版本

## 适用场景

- 准备发布新版本，需要确定版本号
- 希望自动化发布流程
- 手动生成变更日志会浪费大量时间
- 需要确保团队成员之间使用一致的标签命名规则

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能直接使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行此工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-release --help
```

## 工作原理

该工具会读取自上次创建标签以来的所有 Git 提交记录（如果没有标签，则从第一个提交开始）。根据提交的影响程度对它们进行分类：重大变更会导致版本号升级为“major”，新功能会导致版本号升级为“minor”，修复问题会导致版本号升级为“patch”。随后，工具会生成带有注释的标签，并将其添加到变更日志文件中。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。