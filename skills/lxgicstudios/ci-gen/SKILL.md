---
name: ci-gen
description: 根据项目分析结果生成 GitHub Actions 的 CI/CD 工作流。在设置自动化管道时可以使用这些工作流。
---

# CI/CD 工作流生成器

只需将此工具指向任意项目，即可立即获得一个可用的 GitHub Actions 工作流。该工具会扫描你的代码库，检测所使用的开发技术栈，并生成一个适合你项目需求的 CI/CD 流程。

**仅需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-ci ./my-project
```

## 功能介绍

- 扫描项目以识别所使用的开发框架、编程语言及依赖项
- 生成包含正确构建和测试步骤的 GitHub Actions 工作流
- 支持缓存机制，以加快 CI 测试的速度
- 根据常见平台自动配置部署流程
- 为 Pull Request（PR）和主分支的推送分别生成不同的工作流

## 使用示例

```bash
# Analyze current directory
npx ai-ci .

# Generate for a specific project
npx ai-ci ./apps/frontend

# Include deployment to Vercel
npx ai-ci . --deploy vercel
```

## 最佳实践

- **查看生成的结果**：虽然 AI 会提供默认的配置，但请根据实际需求进行调整
- **先从测试环节开始**：确保 CI 测试能够正常运行，再逐步添加部署功能
- **正确使用敏感信息**：工作流会引用一些敏感信息，请确保这些信息已添加到 GitHub 账户中
- **保持简单性**：不要过度复杂化你的第一个 CI/CD 流程

## 适用场景

- 新项目启动时，需要快速搭建 CI 环境
- 从其他 CI 系统迁移到 GitHub Actions
- 通过实际示例学习 GitHub Actions 的使用方法
- 在多个仓库中统一 CI 流程

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。完全免费，无需注册或支付 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-ci --help
```

## 工作原理

该工具使用通配符模式扫描项目结构，识别 `package.json`、`requirements.txt`、`Dockerfile` 等配置文件，从而了解项目的开发技术栈。随后会根据扫描结果生成相应的 YAML 格式的工作流文件。

## 许可协议

遵循 MIT 许可协议，永久免费使用。你可以自由地使用该工具。