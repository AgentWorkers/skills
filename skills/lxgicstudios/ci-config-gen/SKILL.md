---
name: ci-gen
description: 从您的项目中生成 GitHub Actions 工作流。在从头开始设置持续集成/持续部署（CI/CD）流程时可以使用这些工作流。
---

# CI 生成器

从零开始搭建持续集成（CI）/持续部署（CD）系统通常需要花费大量时间来阅读文档、复制示例代码，并手动修改 YAML 配置文件。这款工具能够自动分析你的项目结构，为你生成合适的持续集成工作流程。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-ci
```

## 功能介绍

- 自动扫描项目以识别使用的语言和开发框架；
- 生成完整的 GitHub Actions 工作流程；
- 配置代码检查（linting）、测试、构建（building）和部署（deployment）流程；
- 支持多种部署目标。

## 使用示例

```bash
# Generate workflow for current project
npx ai-ci

# Specify deploy target
npx ai-ci --deploy vercel

# Preview without writing
npx ai-ci --preview

# Different targets
npx ai-ci --deploy netlify
npx ai-ci --deploy aws
npx ai-ci --deploy docker
npx ai-ci --deploy fly
```

## 最佳实践

- **从简单开始**：根据实际需求逐步增加复杂性；
- **缓存依赖项**：显著加快构建速度；
- **快速反馈错误**：先运行快速检查（如代码格式检查），再运行耗时的测试；
- **仔细查看输出结果**：在提交代码前确保理解工具的实际操作内容。

## 适用场景

- 新项目启动且需要立即启用持续集成功能；
- 从其他 CI 系统迁移到 GitHub Actions；
- 需要一个可定制的起点来构建持续集成系统；
- 不清楚现代持续集成工作流程应包含哪些步骤。

## 属于 LXGIC 开发工具包

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本完全无付费门槛、无需注册账号，也不需要 API 密钥。这些工具都能直接使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-ci --help
```

## 工作原理

该工具会分析你的 `package.json` 文件、配置文件以及项目结构，以确定项目使用的语言、开发框架、测试设置和构建步骤。随后，它会生成一个包含相应任务、缓存配置和部署设置的 GitHub Actions 工作流程 YAML 文件。

## 许可协议

采用 MIT 许可协议，永久免费。你可以自由使用这款工具。