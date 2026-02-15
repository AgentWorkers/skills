---
name: swagger-gen
description: 从 Express 路由生成 OpenAPI 规范。在文档编写过程中可以使用这一功能来描述 API 的详细信息。
---

# Swagger Generator

您的 API 目前还没有文档。该工具会读取您的 Express 路由信息，并自动生成完整的 OpenAPI 3.0 规范。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-swagger ./src/routes/
```

## 功能介绍

- 读取您的 Express 路由文件
- 生成 OpenAPI 3.0 规范
- 为请求和响应的数据结构添加文档说明
- 支持与 Swagger UI 集成使用

## 使用示例

```bash
# Generate from routes
npx ai-swagger ./src/routes/

# Single file
npx ai-swagger ./src/routes/users.ts -o docs/api.yaml
```

## 最佳实践

- **定期更新**：当路由发生变化时重新生成文档
- **添加描述**：明确说明每个端点的功能
- **提供示例**：展示请求的示例数据
- **记录错误情况**：不仅记录成功的请求，也记录失败的请求

## 适用场景

- 生成 API 文档
- 配置 Swagger UI
- 帮助 API 使用者快速上手
- 采用 API 首先的设计模式（API-first design）

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无付费门槛、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-swagger --help
```

## 工作原理

该工具会解析您的 Express 路由定义，提取端点、方法及处理函数代码，然后生成包含正确类型和描述信息的 OpenAPI 规范。

## 许可证

采用 MIT 许可协议。永久免费，可自由使用。