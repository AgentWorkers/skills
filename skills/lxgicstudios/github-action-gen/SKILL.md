---
name: github-action-gen
description: **将纯英文的SKILL.md文件转换为中文（简体）：**  
**生成GitHub Actions工作流**  
**用途：** 在设置持续集成（CI）时使用。  

**说明：**  
GitHub Actions是一种自动化工作流工具，允许你在GitHub仓库中自动化执行特定的任务，如构建、测试、部署等。本指南将教你如何使用纯英文描述来生成GitHub Actions的工作流脚本。这些脚本通常包含一系列命令和配置，用于定义工作流的执行顺序和条件。  

**示例：**  
假设你有一个名为`build.yml`的文件，其中包含以下内容：  
```yaml
name: Build Application
on: push
jobs:
  build:
    steps:
      - name: Install Dependencies
        uses: actions/install-nodejs@v12
        with:
          node_version: '14.17.1'
      - name: Set Up Development Environment
        uses: actions/setup-node@v12
        with:
          node_version: '14.17.1'
      - name: Install Package
        uses: actions/install-package@v12
        with:
          package: 'your-package-name'
      - name: Run Tests
        uses: actions/test@v12
        with:
          package: 'your-test-package'
```

**转换后的中文版本：**  
```yaml
**生成GitHub Actions工作流**  
**用途：** 用于配置持续集成（CI）流程。  

**说明：**  
- `name: Build Application`：工作流的名称。  
- `on: push`：触发条件：当仓库被推送时自动执行该工作流。  
- `jobs`: 包含工作流的详细步骤。  
  - `build`: 主要工作流步骤：  
    - `name: Install Dependencies`：安装依赖项。  
      - `uses: actions/install-nodejs@v12`：使用GitHub Actions提供的`install-nodejs`工具安装Node.js。  
      - `with`: 指定安装的Node.js版本（例如：`14.17.1`）。  
    - `name: Set Up Development Environment`：设置开发环境。  
      - `uses: actions/setup-node@v12`：再次使用`install-nodejs`工具安装Node.js。  
      - `with`: 指定Node.js版本。  
    - `name: Install Package`：安装项目所需的软件包。  
      - `uses: actions/install-package@v12`：使用`install-package`工具安装指定的软件包。  
    - `name: Run Tests`：运行测试。  
      - `uses: actions/test@v12`：使用`test`工具运行测试。  
      - `with`: 指定需要测试的软件包。
---

# GitHub Actions 生成器

不要再从 StackOverflow 上复制工作流 YAML 代码了。只需描述您的需求，即可获得一个可用的 GitHub Actions 工作流。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-github-action "test and deploy on push to main"
```

## 功能介绍

- 生成完整的 GitHub Actions 工作流文件
- 支持常见的操作模式，如测试（test）、构建（build）和部署（deploy）
- 提供缓存功能，以加快运行速度
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

- **使用 secrets（机密信息）**：切勿将凭据硬编码到代码中
- **缓存依赖项**：每次运行时均可节省大量时间
- **快速失败处理**：先进行快速检查
- **使用矩阵构建（matrix builds）**：同时测试多个 Node.js 版本

## 适用场景

- 为新仓库设置持续集成（CI）流程
- 添加部署自动化功能
- 创建自定义工作流
- 学习 GitHub Actions 的语法

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。无需付费、无需注册，免费版本也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-github-action --help
```

## 工作原理

该工具会根据您提供的纯文本描述，自动生成包含正确触发器（triggers）、任务（jobs）和步骤（steps）的 GitHub Actions YAML 代码。该工具能够识别不同工作流的常见模式和最佳实践。

## 许可协议

采用 MIT 许可协议。永久免费，可随意使用。