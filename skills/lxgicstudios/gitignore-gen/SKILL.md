---
name: gitignore-gen
description: 通过分析您的项目来生成 `.gitignore` 文件。在设置新的仓库时可以使用该文件。
---

# Gitignore 生成器

别再复制粘贴那些通用的 `.gitignore` 模板了。这个工具会扫描你的项目，并生成一个真正符合你项目需求的 `.gitignore` 文件。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-gitignore
```

## 功能介绍

- 扫描你的项目，识别项目中使用的语言和框架；
- 生成一个完整的 `.gitignore` 文件；
- 包括 IDE 相关文件、构建输出文件以及敏感信息（如配置文件）；
- 不使用通用的模板，只生成你实际需要的内容。

## 使用示例

```bash
# Preview what it'll generate
npx ai-gitignore --preview

# Write the .gitignore
npx ai-gitignore

# Custom output path
npx ai-gitignore --output ./my-project/.gitignore
```

## 最佳实践

- **忽略构建输出文件**：确保 `dist/build` 文件夹被排除在版本控制之外；
- **忽略环境配置文件**：`.env`、`.env.local` 等；
- **忽略 IDE 配置文件**：`.vscode`、`.idea` 等；
- **忽略操作系统生成的文件**：`.DS_Store`、`Thumbs.db` 等。

## 适用场景

- 新项目启动时；
- 向现有项目中添加新的语言或框架时；
- 当当前的 `.gitignore` 文件过于混乱、需要清理时；
- 不确定项目使用了哪些文件时。

## 本工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。完全免费，无需注册或支付 API 密钥，工具本身即可直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-gitignore --help
```

## 工作原理

该工具会扫描 `package.json`、`Cargo.toml`、`go.mod` 等配置文件，以确定项目中使用的语言和框架。然后生成一个 `.gitignore` 文件，涵盖这些语言和框架常见的文件排除规则。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用该工具。