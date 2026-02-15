---
name: dockerfile-gen
description: 为任何项目生成优化的 Dockerfile
---

# Dockerfile 生成器

该工具会扫描您的项目，并自动生成一个适用于生产环境的 Dockerfile。支持多阶段构建、有效的缓存机制以及最佳的安全实践。

## 快速入门

```bash
npx ai-dockerfile
```

## 功能介绍

- 自动识别您的项目所使用的编程语言（Node.js、Python、Go 等）；
- 生成适合多阶段构建的 Dockerfile；
- 优化层缓存策略；
- 增强系统安全性；
- 自动添加 `.dockerignore` 文件以排除不需要被包含在镜像中的文件。

## 使用示例

```bash
# Generate for current project
npx ai-dockerfile

# Specify base image
npx ai-dockerfile --base node:20-alpine

# Production optimized
npx ai-dockerfile --production

# With compose file
npx ai-dockerfile --compose
```

## 生成内容

- 带有注释的 Dockerfile；
- `.dockerignore` 文件；
- （可选）`docker-compose.yml` 文件；
- 构建指令。

## 主要特性

- 支持多阶段构建，以生成更小的镜像；
- 使用非 root 用户权限进行构建；
- 实现健康检查机制；
- 优化层缓存策略；
- 提供完善的信号处理机制。

## 系统要求

- 需要 Node.js 18.0 及以上版本；
- 需要配置 OPENAI_API_KEY。

## 许可证

采用 MIT 许可证，永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub: [github.com/lxgicstudios/ai-dockerfile](https://github.com/lxgicstudios/ai-dockerfile)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)