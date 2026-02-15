---
name: ci-gen
description: 从您的项目中生成 GitHub Actions 工作流。在从零开始设置持续集成/持续部署（CI/CD）时可以使用这些工作流。
---

# CI 生成器

从零开始设置 CI/CD 需要花费大量时间：查阅文档、复制示例代码，以及手动调整 YAML 配置文件。而这个工具能够自动分析你的项目，并生成合适的 CI/CD 工作流程。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-ci
```

## 功能介绍

- 自动扫描你的项目，识别所使用的语言和开发框架；
- 生成完整的 GitHub Actions 工作流程；
- 配置代码检查（linting）、测试、构建（building）和部署（deployment）环节；
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
- **缓存依赖项**：显著提升构建速度；
- **快速检测错误**：先运行快速检查（如代码格式检查），再执行耗时的测试；
- **仔细查看输出结果**：在提交代码前确保了解整个流程的运作方式。

## 适用场景

- 新项目启动时，需要立即启用 CI 流程；
- 从其他 CI 系统迁移到 GitHub Actions；
- 需要一个可定制的起点来构建自己的 CI 环境；
- 不确定现代 CI 工作流程应包含哪些步骤。

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本完全无限制使用，无需注册或提供 API 密钥。这些工具都能稳定运行。

**了解更多：**
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

该工具会分析你的 `package.json` 文件、配置文件以及项目结构，以确定项目使用的语言、开发框架、测试设置和构建流程。随后会生成一个包含相应任务（jobs）、缓存策略（caching）和部署配置的 GitHub Actions 工作流程 YAML 文件。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-ci](https://github.com/lxgicstudios/ai-ci)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)