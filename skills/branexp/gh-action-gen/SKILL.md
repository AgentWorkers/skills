---
name: gh-action-gen
description: **将纯英文的 SKILL.md 文件转换为中文（简体）：**  
**生成 GitHub Actions 工作流**  
**在设置持续集成（CI）时使用。**  

---

**说明：**  
GitHub Actions 是一种自动化工作流工具，用于在 GitHub 仓库中执行特定任务（如构建、测试、部署等）。本文档提供了如何使用纯英文描述来生成 GitHub Actions 工作流的步骤。这些描述通常包含以下内容：  
- **触发条件**：什么事件会触发工作流的执行（例如，代码提交、仓库合并请求等）  
- **步骤**：工作流需要执行的操作（例如，运行测试、部署应用程序等）  
- **依赖项**：工作流所需的工具或服务（例如，Node.js、npm、Docker 等）  

以下是一个简单的示例：  

```markdown
# Example GitHub Actions workflow
name: Build and Deploy Application

on:
  push: 'main'

steps:
  - name: Install Dependencies
    run: npm install

  - name: Build Application
    run: npm run build

  - name: Deploy to GitHub Pages
    run: git push --branch gh-pages
```

**翻译：**  
**生成 GitHub Actions 工作流**  
**用于设置持续集成（CI）**  

---

**说明：**  
- **工作流名称**：工作流的名称，用于识别和区分不同的工作流。  
- **触发条件**：指定在什么情况下执行工作流（例如，当代码仓库中的 `main` 分支被推送时）。  
- **步骤**：工作流需要执行的操作，包括安装依赖项、构建应用程序以及将其部署到 GitHub Pages。  

请注意，实际的工作流描述可能包含更复杂的逻辑和配置，但基本结构保持一致。如果您需要更详细的示例或针对特定场景的指导，请提供更多关于工作流需求的详细信息。
---

# GitHub Actions 生成器

不要再从 StackOverflow 上复制工作流 YAML 代码了。只需描述您的需求，就能获得一个可运行的 GitHub Actions 工作流。

**一个命令，零配置，立即生效。**

## 快速入门

```bash
npx ai-github-action "test and deploy on push to main"
```

## 功能介绍

- 生成完整的 GitHub Actions 工作流文件
- 支持常见的操作模式，如测试、构建、部署
- 配置缓存以提高运行效率
- 支持多个部署目标

## 使用示例

```bash
# Test and deploy
npx ai-github-action "test and deploy on push to main"

# PR checks
npx ai-github-action "run eslint and prettier on PRs" --install

# Docker workflow
npx ai-github-action "build docker image and push to ECR" -o deploy.yml

# Scheduled job
npx ai-github-action "run database backup every night at 2am"
```

## 最佳实践

- **使用 secrets（密钥）**：切勿将凭据硬编码到代码中
- **缓存依赖项**：每次运行时均可节省大量时间
- **快速失败检测**：先执行快速检查
- **使用矩阵构建（matrix builds）**：同时测试多个 Node.js 版本

## 适用场景

- 为新仓库设置持续集成（CI）流程
- 添加部署自动化功能
- 创建自定义工作流
- 学习 GitHub Actions 的语法

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。完全免费，无需注册，免费版本也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可使用。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-github-action --help
```

## 工作原理

该工具会根据您提供的文字描述自动生成包含正确触发器、任务和步骤的 GitHub Actions YAML 代码。它能够识别不同工作流的常见模式和最佳实践。

## 许可证

MIT 许可证。永久免费使用，可随意使用。