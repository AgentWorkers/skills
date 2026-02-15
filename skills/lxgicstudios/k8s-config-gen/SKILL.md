---
name: k8s-gen
description: 根据 `docker-compose` 文件或相关描述生成 Kubernetes 配置文件（manifests），用于将应用程序部署到 Kubernetes 集群中。
---

# K8s Generator

将 `docker-compose` 文件转换为 Kubernetes 配置文件其实是一项繁琐的工作（涉及大量的 YAML 代码编辑）。只需提供您的 `docker-compose` 文件，即可获得相应的 Kubernetes 配置文件。

**仅需一个命令，无需任何额外配置，即可完成转换。**

## 快速入门

```bash
npx ai-k8s docker-compose.yml
```

## 功能概述

- 将 `docker-compose` 文件转换为 Kubernetes 配置文件
- 根据用户提供的纯文本描述自动生成相应的 Kubernetes 资源（如 Deployment、Service、ConfigMap 等）
- 支持处理 secrets 和持久化卷（persistent volumes）

## 使用示例

```bash
# From docker-compose
npx ai-k8s docker-compose.yml --namespace production

# From description
npx ai-k8s "3 replicas of a node app with redis and postgres"

# Save output
npx ai-k8s docker-compose.yml -o k8s-manifests.yml
```

## 最佳实践

- **使用命名空间（namespaces）**：合理组织资源
- **设置资源限制（resource limits）**：防止 Pod 过度消耗资源
- **添加健康检查（health checks）**：确保 Pod 的正常运行状态
- **正确使用 secrets**：避免将敏感信息硬编码到配置文件中

## 适用场景

- 从 `docker-compose` 迁移到 Kubernetes
- 设置新的 Kubernetes 部署环境
- 学习 Kubernetes 配置文件的结构
- 在进行详细调整之前快速搭建原型

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。完全免费，无需注册或支付 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-k8s --help
```

## 工作原理

该工具会解析您的 `docker-compose.yml` 文件或相关描述文件，理解其中的服务及其之间的关系，然后自动生成具有正确配置的 Kubernetes 资源。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。