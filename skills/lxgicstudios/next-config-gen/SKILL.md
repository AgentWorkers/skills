---
name: next-config-gen
description: 生成符合最佳实践的 Next.js 配置文件。在配置 Next.js 项目时可以使用该配置文件。
---

# Next Config Generator

`next.config.js` 文件包含了大量的配置选项。这个工具会读取你的项目，并自动生成一个包含合理默认值以及你实际所需功能的配置文件。

**只需一个命令，即可完成配置设置。**非常简单易用。

## 快速入门

```bash
npx ai-next-config
```

## 功能介绍

- 分析你的 Next.js 项目结构
- 生成优化后的 `next.config.mjs` 配置文件
- 设置图片域名、重写规则和响应头信息
- 配置符合最佳实践的默认设置

## 使用示例

```bash
# Generate from current project
npx ai-next-config

# Output as CommonJS
npx ai-next-config -o next.config.js
```

## 最佳实践

- **启用严格模式**：有助于尽早发现潜在问题
- **配置图片域名**：外部图片需要被允许访问
- **设置安全响应头**：确保使用 HTTPS、CSP 等安全策略
- **谨慎使用重写规则**：它们可能会影响页面缓存

## 适用场景

- 新建 Next.js 项目时
- 升级到最新版本的 Next.js 时
- 需要添加图片优化等功能时
- 需要清理混乱的配置文件时

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行此工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-next-config --help
```

## 工作原理

该工具会读取你的 `package.json` 文件和项目结构，以了解你正在使用的功能。然后根据这些信息生成一个包含图片设置、响应头配置、重写规则以及实验性功能的 `next.config.mjs` 文件。

## 许可证

采用 MIT 许可协议。永久免费使用，你可以随意使用这个工具。