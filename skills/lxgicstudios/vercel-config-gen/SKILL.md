---
name: vercel-config-gen
description: 生成优化的 Vercel 配置文件。在部署到 Vercel 时使用该配置文件。
---

# Vercel 配置生成器

Vercel 提供了许多配置选项。该工具会为您的项目生成一个优化后的 `vercel.json` 文件。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-vercel-config
```

## 功能介绍

- 分析您的项目结构
- 生成 `vercel.json` 配置文件
- 设置响应头、重写规则和重定向规则
- 配置构建相关设置

## 使用示例

```bash
# Generate config
npx ai-vercel-config
```

## 最佳实践

- **设置安全响应头**（如 HTTPS、CSP 等）
- **配置缓存**（确保静态资源能够被缓存）
- **为单页应用（SPA）使用重写规则**（实现客户端路由）
- **设置函数部署区域**（将函数部署得离用户更近）

## 适用场景

- 首次使用 Vercel 进行部署时
- 优化现有的部署配置
- 添加自定义响应头
- 设置重定向规则

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本完全无限制使用，无需支付费用、注册账号或获取 API 密钥。这些工具都能正常工作。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-vercel-config --help
```

## 工作原理

该工具会读取您的项目结构和 `package.json` 文件，以了解您要部署的内容，然后根据您的框架需求生成相应的 `vercel.json` 配置文件。

## 许可证

采用 MIT 许可协议。永久免费，您可以自由使用该工具。