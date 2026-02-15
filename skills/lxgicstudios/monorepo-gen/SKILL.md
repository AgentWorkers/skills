---
name: monorepo-gen
description: 设置 Turborepo 单一仓库结构。在开始使用单一仓库时，请使用此步骤。
---

# 单仓库生成器（Monorepo Generator）

单仓库（Monorepo）虽然功能强大，但正确的设置却颇具挑战性。这款工具能够帮助您快速搭建一个结构完善的 Turborepo 项目，并提供所有必要的配置。

**只需一条命令，无需任何额外配置，即可立即使用。**

## 快速入门

```bash
npx ai-monorepo
```

## 功能介绍

- 在您的项目中设置 Turborepo 结构
- 创建应用程序和包文件夹
- 配置共享的 TypeScript 和 ESLint 规则
- 设置工作区的依赖关系

## 使用示例

```bash
# Set up in current directory
npx ai-monorepo

# Custom target directory
npx ai-monorepo ./my-project
```

## 最佳实践

- **保持包的职责清晰**（每个包只负责特定的功能）
- **使用内部包**（在内部共享代码，无需公开发布）
- **积极利用缓存**（Turborepo 的核心优势在于高效的缓存机制）
- **明确界定依赖关系**（明确哪些包可以依赖于哪些包）

## 适用场景

- 新建单仓库项目
- 从多个仓库迁移到单仓库结构
- 将 Turborepo 集成到现有项目中
- 学习单仓库的开发模式

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发工具之一。免费版本完全无限制使用，无需支付费用、注册账号或申请 API 密钥。这些工具都能直接投入使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需额外安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-monorepo --help
```

## 工作原理

该工具通过 `turbo.json` 文件、工作区配置文件以及共享的配置包来搭建完整的 Turborepo 结构，并为所有包设置构建、测试和代码检查的流程。

## 许可协议

采用 MIT 许可协议，永久免费。您可以自由使用该工具，无需遵守任何限制。