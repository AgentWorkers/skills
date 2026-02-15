---
name: github-action-gen
description: **将纯英文的 SKILL.md 文件转换为中文（简体中文）：**  
**生成 GitHub Actions 工作流**  
**用于设置持续集成（CI）环境时使用。**  

**说明：**  
- 本任务要求将包含技术细节的 SKILL.md 文件中的英文内容翻译成中文（简体中文），同时保持技术内容的准确性和格式的一致性。  
- 特别注意：代码示例、命令和 URL 需要保持原样不变。  
- 如果代码块中的注释具有解释性，建议也一并翻译。  
- 确保翻译后的文档结构和组织方式与原文相同。  

**示例 SKILL.md 文件内容（部分）：**  
```markdown
# 生成 GitHub Actions 工作流  
## 准备工作  
1. 在 GitHub 仓库中创建一个新的 `github/workflows` 目录（如果尚不存在）。  
2. 在 `github/workflows` 目录下创建一个名为 `main.yml` 的文件。  

## main.yml 文件内容（示例）  
```yaml
name: My GitHub Actions Workflow

on:
  trigger: pull

steps:
  - name: Check for changes
    run: git status

  - name: Install dependencies
    run: |
      curl -sL https://raw.githubusercontent.com/gohub.io/setup-github-action-v2.1.0/install.sh | bash
      curl -sL https://raw.githubusercontent.com/gohub.io/setup-github-action-v2.1.0/setup.sh | bash
      pip install --upgrade pip

  - name: Set up environment variables
    run: |
      echo "export PATH=$PATH:/usr/local/bin:$PATH"
      echo "export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.8:$PYTHONPATH"
      echo "export GO111BIN=/usr/local/go111/bin"
      echo "export GO111SDK=/usr/local/go111/bin"
      echo "export GO111MODULES=$GO111BIN/bin"
      echo "export GO111MODULES_PATH=/usr/local/go111/bin"
      echo "export GO111MODULES_ROOT=/usr/local/go111"
      echo "export GO111GOROOT=/usr/local/go111"
      echo "export GO111GOROOT/bin=$GOROOT/bin"
      echo "export PATH=$PATH:$GOROOT/bin:$GO111BIN:$GO111MODULES_PATH:$GO111GOROOT/bin"
```

**翻译后的中文内容（简体中文）：**  
**生成 GitHub Actions 工作流**  
**用于设置持续集成（CI）环境时使用。**  

**步骤说明：**  
1. 在 GitHub 仓库中创建一个名为 `github/workflows` 的新目录（如果尚不存在）。  
2. 在 `github/workflows` 目录下创建一个名为 `main.yml` 的文件。  

**main.yml 文件内容（示例）：**  
```yaml
name: 我的 GitHub Actions 工作流

on:
  trigger: pull

steps:
  - 名称：检查是否有更改
    run: git status

  - 名称：安装依赖项
    run: |
      curl -sL https://raw.githubusercontent.com/gohub.io/setup-github-action-v2.1.0/install.sh | bash
      curl -sL https://raw.githubusercontent.com/gohub.io/setup-github-action-v2.1.0/setup.sh | bash
      pip install --upgrade pip

  - 名称：设置环境变量
    run: |
      echo "export PATH=$PATH:/usr/local/bin:$PATH"
      echo "export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.8:$PYTHONPATH"
      echo "export GO111BIN=/usr/local/go111/bin"
      echo "export GO111SDK=/usr/local/go111/bin"
      echo "export GO111MODULES=$GO111BIN/bin"
      echo "export GO111MODULES_PATH=/usr/local/go111/bin"
      echo "export GO111GOROOT=/usr/local/go111"
      echo "export GO111GOROOT/bin=$GOROOT/bin"
      echo "export PATH=$PATH:$GOROOT/bin:$GO111BIN:$GO111MODULES_PATH:$GO111GOROOT/bin"
```

（注：实际使用中，您可能需要根据具体需求修改 `main.yml` 文件中的内容。）
---

# GitHub Action Generator

不要再从 StackOverflow 上复制工作流 YAML 代码了。只需描述您的需求，即可获得一个可用的 GitHub Actions 工作流。

**一个命令，零配置，立即生效。**

## 快速入门

```bash
npx ai-github-action "test and deploy on push to main"
```

## 功能介绍

- 生成完整的 GitHub Actions 工作流文件
- 支持常见的操作模式，如测试（test）、构建（build）和部署（deploy）
- 采用缓存机制以提高运行速度
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
- **快速失败检测**：先执行快速检查
- **使用矩阵构建（matrix builds）**：同时测试多个 Node.js 版本

## 适用场景

- 为新仓库设置持续集成（CI）环境
- 添加部署自动化功能
- 创建自定义工作流
- 学习 GitHub Actions 的语法

## 属于 LXGIC Dev Toolkit 的一部分

LXGIC Studio 开发了 110 多款免费开发者工具，这款工具也不例外。无需付费、无需注册，免费版本也不需要 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-github-action --help
```

## 工作原理

该工具会根据您提供的简单描述自动生成包含正确触发器（triggers）、任务（jobs）和步骤（steps）的 GitHub Actions YAML 代码。它能够识别不同工作流的常见模式和最佳实践。

## 许可证

MIT 许可证。永久免费，可随意使用。