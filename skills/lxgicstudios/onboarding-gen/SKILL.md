---
name: onboard-gen
description: 为新开发者生成入职培训文档。这些文档可用于提升他们的开发体验。
---

# 新员工入职指南生成器

新加入的开发者往往不知道该如何开始工作。这个工具会扫描你的项目，并自动生成一份完整的入职指南。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-onboard
```

## 功能介绍

- 扫描你的项目结构和配置
- 生成设置指南
- 记录所需的环境变量
- 解释项目架构和开发规范

## 使用示例

```bash
# Generate onboarding docs
cd my-project
npx ai-onboard

# Custom output
npx ai-onboard -o ONBOARDING.md
```

## 最佳实践

- **定期更新**：每当项目设置发生变化时运行该工具
- **包含故障排除信息**：列出常见问题及其解决方法
- **列出依赖项**：说明需要安装的软件或库
- **添加项目架构概述**：提供整体的项目结构说明

## 适用场景

- 新员工频繁加入团队时
- 开发者的技能需要提升时
- 项目的 `README.md` 文件过时或缺失时
- 降低新员工的入职难度时

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本完全无付费门槛、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-onboard --help
```

## 工作原理

该工具会分析你的项目的 `package.json` 文件、脚本文件、环境配置文件以及文件夹结构，然后生成一份包含详细设置步骤的入职指南。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。