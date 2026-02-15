---
name: script-gen
description: 使用 AI 生成 `package.json` 脚本。在设置 npm 脚本时可以使用这些脚本。
---

# 脚本生成器

`package.json` 中的脚本功能非常强大，但编写它们却相当繁琐。只需描述您的需求，系统便会自动生成合适的 npm 脚本。

**一个命令，零配置，立即生效。**

## 快速入门

```bash
npx ai-script "lint, test, build, deploy"
```

## 功能介绍

- 为您的工作流程生成 npm 脚本
- 支持复杂的脚本链
- 包含预处理/后处理钩子
- 适用于任何开发工具

## 使用示例

```bash
# Basic workflow
npx ai-script "lint, test, build, deploy"

# Docker workflow
npx ai-script "docker build, docker push, k8s deploy"

# Full CI
npx ai-script "typecheck, lint, test:unit, test:e2e, build, deploy:staging"
```

## 最佳实践

- **使用预处理/后处理钩子**：在测试前运行代码检查（lint）
- **保持脚本的可组合性**：将脚本拆分成独立的小模块
- **为复杂脚本添加文档说明**：编写清晰的注释
- **在本地进行测试**：在持续集成（CI）流程之前先运行脚本

## 适用场景

- 设置新项目的脚本
- 添加持续集成/持续部署（CI/CD）命令
- 标准化工作流程
- 学习 npm 脚本的开发模式

## 本工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需额外安装，直接使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-script --help
```

## 工作原理

该工具会根据您的工作流程描述自动生成符合规范的 npm 脚本，同时能够识别常见的开发模式并确保脚本之间的协同性。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/npm-script-gen](https://github.com/lxgicstudios/npm-script-gen)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)