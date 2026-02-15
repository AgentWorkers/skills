---
name: k8s-gen
description: 从 `docker-compose` 文件或纯文本描述中生成 Kubernetes 配置文件（manifests）。在将应用程序部署到 Kubernetes 集群时使用这些配置文件。
---

# Kubernetes Manifest Generator

别再手动编写 YAML 了！这个工具可以将您的 `docker-compose` 文件或简单的描述转换为适用于生产环境的 Kubernetes 配置文件（包括 Deployment、Service、ConfigMap 等）。只需一个命令，无需任何额外的配置，即可完成转换。

**快速入门**

```bash
npx ai-k8s "nginx with 3 replicas, exposed on port 80"
```

## 功能介绍

- 自动将 `docker-compose.yml` 文件转换为 Kubernetes 配置文件
- 生成 Deployment、Service、ConfigMap 和 Secret 等资源对象
- 设置合理的资源限制和健康检查机制
- 输出格式清晰、可直接使用 `kubectl apply` 命令应用的 YAML 文件
- 支持具有复杂网络架构的多服务系统

## 使用示例**

```bash
# Generate from a description
npx ai-k8s "postgres database with persistent volume"

# Convert docker-compose to K8s
npx ai-k8s --compose docker-compose.yml

# Full app stack
npx ai-k8s "node app with redis cache and postgres db, 3 replicas each"
```

## 最佳实践

- **从简单开始**：先生成一个服务，验证其功能是否正常，再逐步增加复杂性
- **检查资源限制**：虽然工具会设置合理的默认值，但请根据实际工作负载进行调整
- **使用命名空间**：通过 `--namespace` 标志来组织部署资源
- **为配置文件添加版本控制**：将生成的 YAML 文件提交到 Git，视其为代码进行版本管理

## 适用场景

- 如果您熟悉 Docker，但对 Kubernetes 的 YAML 格式感到困惑
- 需要将 `docker-compose` 配置迁移到 Kubernetes 环境
- 需要快速原型化新的部署方案，而不想编写繁琐的 YAML 代码
- 希望通过生成的示例来学习 Kubernetes 的概念

## 本工具属于 LXGIC 开发工具包的一部分

LXGIC Studios 开发了 110 多款免费开发者工具，这款工具就是其中之一。免费版本完全无付费门槛、无需注册，也不需要 API 密钥，只需使用 `npx` 命令即可运行。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-k8s --help
```

## 工作原理

该工具会分析您的 `docker-compose` 文件或配置描述，理解其中的服务及其之间的关系，然后生成符合 Kubernetes 规范的配置文件。它将 Docker 中的概念（如卷、端口等）映射到 Kubernetes 中对应的资源类型（如 `PersistentVolumeClaim`、`Service` 等）。

## 许可证

采用 MIT 许可协议，永久免费使用。您可以随意使用该工具。