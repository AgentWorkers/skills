---
name: env-sync
description: 从您的 `.env` 文件中生成 `.env.example` 文件。在为新开发者提供培训或引导时可以使用该文件。
---

# 环境变量同步（Env Sync）

你的 `.env` 文件中包含了 30 个环境变量，但几乎没人知道其中一半变量的具体用途。这个工具会生成一个格式规范的 `.env.example` 文件，其中所有的敏感信息（如密码、API 密钥等）都会被移除。

**只需一个命令，无需任何配置，即可完成同步。**

## 快速入门

```bash
npx ai-env-sync
```

## 功能介绍

- 读取所有的 `.env` 文件（包括 `.env`、`.env.local` 和 `.env.development`）
- 移除敏感值，但保留变量名
- 为每个变量添加说明性注释
- 生成一个格式整洁的 `.env.example` 文件

## 使用示例

```bash
# Generate .env.example
npx ai-env-sync

# Specify project directory
npx ai-env-sync ./my-project
```

## 最佳实践

- **在提交代码前运行该工具**：确保 `.env.example` 文件与实际 `.env` 文件保持一致
- **集成到持续集成（CI）流程中**：验证 `.env.example` 文件的格式是否正确
- **将相关变量分组**：便于统一配置
- **明确区分必填和可选变量**：并非所有变量都需要设置值

## 适用场景

- 新团队成员入职时的环境配置指导
- 设置持续集成/持续部署（CI/CD）环境
- 记录环境配置要求
- 确保 `.env.example` 文件始终是最新的

## 本工具属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。完全免费，无需注册，免费版本也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-env-sync --help
```

## 工作原理

该工具会读取你的 `.env` 文件，识别其中的变量，并利用 GPT-4o-mini 为每个变量生成详细的说明性文本。敏感信息会被替换为占位符（如 `your_api_key_here`）。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用该工具。