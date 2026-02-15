---
name: docker-writer
description: 扫描您的项目并生成一个优化后的 Dockerfile。当您需要快速将项目容器化时，可以使用这个 Dockerfile。
---

# Docker Writer

编写 Dockerfile 并不难，但编写高质量的 Dockerfile 却需要一定的技巧。例如：如何实现多阶段构建、合理利用层缓存、以及如何减小镜像的大小。大多数人通常只是从 Stack Overflow 上复制粘贴代码片段就认为任务完成了。而这个工具会扫描你的项目，识别你使用的运行时环境和依赖项，然后自动生成一个经过优化的 Dockerfile。它处理了那些繁琐的步骤，让你可以专注于项目的发布工作。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-dockerfile
```

## 工作原理

- 扫描你的项目目录，确定项目使用的语言、框架及依赖项。
- 生成包含合适基础镜像和构建步骤的 Dockerfile。
- 支持使用 `--optimize` 标志进行优化后的多阶段构建。
- 提供预览功能，让你在正式编写文件之前先进行查看。
- 适用于 Node.js、Python、Go 等常见项目类型。

## 使用示例

```bash
# Generate Dockerfile for current project
npx ai-dockerfile

# Preview without writing to disk
npx ai-dockerfile --preview

# Generate optimized multi-stage build
npx ai-dockerfile --optimize

# Specify project directory and output path
npx ai-dockerfile --dir ./my-app --output docker/Dockerfile
```

## 最佳实践

- **务必先预览**：在编写 Dockerfile 之前，使用 `--preview` 选项进行预览。确认基础镜像、构建步骤以及暴露的端口是否适合你的项目需求。
- **在生产环境中使用 `--optimize`**：多阶段构建可以生成更小的镜像。虽然默认设置适用于开发环境，但在部署时建议使用 `--optimize`。
- **检查 `.dockerignore` 文件**：虽然工具会自动生成 Dockerfile，但你仍需要手动配置 `.dockerignore` 文件，以排除 `node_modules` 等不必要的文件。
- **测试构建结果**：生成 Dockerfile 后，请运行 `docker build` 命令进行测试。虽然输出结果通常没问题，但在某些特殊情况下可能仍需手动调整。

## 适用场景

- 首次将项目容器化时。
- 需要使用多阶段构建但忘记了相关语法时。
- 需要快速搭建可运行的容器原型时。
- 需要将从未被容器化的项目迁移到 Docker 环境中时。

## 工作方式

该工具会扫描项目目录中的 `package.json`、`requirements.txt`、`go.mod` 等依赖文件，识别你的技术栈，并将这些信息传递给 AI 模型，从而生成针对你项目的定制 Dockerfile。通过使用 `--optimize` 选项，工具会生成将构建过程和运行时过程分开的多阶段构建方案。

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-dockerfile --help
```

## 属于 LXGIC 开发工具包

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本完全无付费门槛、无需注册或 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具，无需遵守任何额外限制。