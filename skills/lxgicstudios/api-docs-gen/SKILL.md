---
name: api-docs-gen
description: 从路由文件生成API文档。当您需要快速生成Markdown格式或OpenAPI规范时，可以使用此方法。
---

# API 文档生成器

您的 API 拥有 50 个端点，但目前没有任何文档。该工具会读取您的路由文件，并自动生成相应的文档，这些文档可以是供人类阅读的 Markdown 格式，也可以是供工具使用的 OpenAPI 规范格式。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-api-docs ./src/routes/
```

## 功能介绍

- 扫描您的路由文件并提取端点信息
- 生成结构清晰的 Markdown 文档
- 生成符合 OpenAPI 3.0 标准的文档（适用于 Swagger 等工具）
- 自动记录请求和响应的数据结构

## 使用示例

```bash
# Generate markdown docs
npx ai-api-docs ./src/routes/
# → API_DOCS.md

# Generate OpenAPI spec
npx ai-api-docs ./src/routes/ --format openapi -o spec.yaml

# Custom output path
npx ai-api-docs ./src/api/ -o docs/api.md

# Scan multiple directories
npx ai-api-docs ./routes ./handlers
```

## 最佳实践

- **保持路由结构清晰**：代码越简洁，生成的文档质量越高
- **使用 TypeScript**：类型信息有助于提升文档的准确性
- **进行审核和编辑**：AI 可帮助构建正确的结构，您只需补充具体内容
- **在代码更改时重新生成文档**：将此过程纳入持续集成（CI）流程中

## 适用场景

- 继承了一个没有 API 文档的代码库
- 在发布 MVP 产品时，文档编写是最后考虑的事项
- 需要快速生成 Swagger 用户界面
- 为新开发者介绍您的 API

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-api-docs --help
```

## 工作原理

该工具会解析您的路由文件，提取 HTTP 方法、路径和处理程序代码。随后利用 GPT-4o-mini 生成请求和响应的数据结构，添加描述，并根据 Markdown 或 OpenAPI 标准对文档进行格式化。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。