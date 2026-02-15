---
name: onboard-gen
description: 为新开发者生成入职培训文档。在为新团队成员安排入职流程时使用此文档。
---

# 新员工入职指南

新成员加入了您的团队，他们需要花费两周时间来熟悉团队的工作环境和各项流程。这款工具能够根据您的代码库自动生成入职指南，内容包括项目架构概述、设置步骤以及核心开发概念等，帮助新员工快速投入工作。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-onboard ./src
```

## 功能介绍

- 扫描您的代码库，生成入门指南；
- 制作架构文档，说明各个组件之间的交互关系；
- 提供包含环境变量和依赖项的安装说明；
- 记录代码中的关键概念、开发模式和规范；
- 根据常见疑问生成常见问题解答（FAQ）。

## 使用示例

```bash
# Generate onboarding docs for your project
npx ai-onboard ./src

# Include specific focus areas
npx ai-onboard ./src --focus auth,database,api

# Output as a single markdown file
npx ai-onboard ./src --output ONBOARDING.md
```

## 最佳实践

- **从项目根目录运行**：该工具需要 `package.json` 和配置文件来获取项目信息；
- **保持 `README.md` 文件的更新**：如果存在的话，工具会使用该文件作为补充信息；
- **审核并自定义内容**：可以添加团队特有的信息，如 Slack 工作群组、会议安排等；
- **每季度重新生成文档**：随着代码库的更新，入职指南也需要及时更新。

## 适用场景

- 新员工即将在下周加入团队；
- 需要为开源项目生成开发者文档；
- 现有的入职指南已经过时（例如提到了已弃用的服务）；
- 需要从零开始搭建团队知识库。

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本完全无限制使用，无需支付费用或注册账号，也无需 API 密钥。我们只提供实用、高效的工具。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-onboard --help
```

## 工作原理

该工具会分析项目结构，读取 `package.json` 和配置文件等关键文件，并抽取源代码中的关键信息，从而生成清晰易懂的文档。它专注于新员工真正需要了解的内容。

## 许可协议

采用 MIT 许可协议，永久免费。您可以自由使用该工具。