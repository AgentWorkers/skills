---
name: compose-gen
description: 通过扫描您的项目来生成 `docker-compose.yml` 文件。在将现有应用程序容器化时可以使用该文件。
---

# Compose Gen

从头开始编写 `docker-compose` 配置文件非常繁琐。这个工具会扫描你的项目，检测所需的服务，并自动生成一个可用的 `docker-compose.yml` 文件。数据库、缓存以及你的应用程序都会被正确地配置好。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-docker-compose
```

## 功能介绍

- 扫描项目以确定所需的服务
- 生成包含正确网络配置的 `docker-compose.yml` 文件
- 根据需要包含数据库、缓存和队列服务
- 设置用于数据持久化的卷
- 添加健康检查（health checks）和依赖关系（depends_on）

## 使用示例

```bash
# Generate for current project
npx ai-docker-compose

# Specify services manually
npx ai-docker-compose --services postgres,redis,app

# Include development overrides
npx ai-docker-compose --with-dev

# Output to specific file
npx ai-docker-compose > docker-compose.yml
```

## 最佳实践

- **使用命名卷**：避免在容器重启时丢失数据
- **添加健康检查**：确保依赖关系能够正确等待服务的启动
- **区分开发环境和生产环境**：使用 `docker-compose.override.yml` 文件来设置开发环境配置
- **固定镜像版本**：使用固定版本的镜像（例如 `postgres:latest` 可能会导致问题）

## 适用场景

- 将现有应用程序容器化
- 不熟悉 `docker-compose` 的语法
- 需要快速搭建本地开发环境
- 需要快速创建新的服务并使用标准配置模板

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本没有任何付费门槛、注册要求或 API 密钥限制，只提供实用的功能。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-docker-compose --help
```

## 工作原理

该工具会扫描 `package.json`、`requirements.txt` 或其他配置文件，以识别你的技术栈。它会识别数据库连接、缓存使用情况以及外部服务依赖关系，并生成包含相应服务、网络配置和卷设置的 `docker-compose.yml` 文件。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。