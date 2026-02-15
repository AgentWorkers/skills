---
name: terraform-gen
description: 生成 Terraform 基础设施配置文件。在配置云资源时使用这些文件。
---

# Terraform 生成器

Terraform 的语法较为冗长。通过描述您的基础设施，即可自动生成相应的 `.tf` 文件。

**仅需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-terraform "3 EC2 instances behind load balancer"
```

## 功能介绍

- 生成 Terraform 配置文件
- 支持 AWS、GCP、Azure 云服务
- 包含变量和输出结果
- 确保资源之间的依赖关系正确设置

## 使用示例

```bash
# AWS setup
npx ai-terraform "3 EC2 instances behind load balancer"

# Database
npx ai-terraform "RDS PostgreSQL with read replica"

# Kubernetes
npx ai-terraform "EKS cluster with 3 node groups"
```

## 最佳实践

- **使用模块**：实现基础设施的复用
- **将配置文件存储在 S3 中**：避免使用本地存储
- **使用变量**：避免使用硬编码的值
- **在应用更改前先进行规划**：务必仔细审查所有修改内容

## 适用场景

- 新建基础设施时
- 学习 Terraform 语法时
- 快速原型设计时
- 生成基础配置文件时

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。无需付费、无需注册，免费版本也不需要 API 密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-terraform --help
```

## 工作原理

该工具会根据您提供的基础设施描述，自动生成包含正确资源、变量和输出结果的 Terraform HCL 代码，并能够理解相应的云服务 API。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。