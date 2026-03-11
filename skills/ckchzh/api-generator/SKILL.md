---
name: api-generator
description: "**API代码生成器**  
该工具能够生成RESTful接口、GraphQL模式、OpenAPI/Swagger文档、API客户端、模拟服务器（mock servers）、认证机制（authentication）、速率限制（rate limiting）以及测试套件（test suites）。支持使用的命令包括：`rest`、`graphql`、`swagger`、`client`、`mock`、`auth`、`rate-limit`、`test`。适用于后端开发（backend development）和API框架搭建（API scaffolding），可用于生成各种接口相关资源。"
---
# ⚡ API 生成器

从零开始生成可用于生产环境的 API 代码框架。REST、GraphQL、身份验证、测试——所有功能都集成在一个工具中。

## 使用方法

```bash
bash scripts/apigen.sh <command> <resource_name> [options]
```

## 命令

### 核心功能生成
- **rest** `<名称>` — RESTful CRUD 端点（基于 Express.js）
- **graphql** `<名称>` — GraphQL 类型、查询和 mutation 的规范
- **swagger** `<名称>` — OpenAPI 3.0 规范文档

### 工具类
- **client** `<名称>` — Python API 客户端类
- **mock** `<名称>` — 基于内存存储的模拟 API 服务器
- **auth** `<类型>` — 身份验证机制（`jwt` / `oauth` / `apikey`）
- **rate-limit** `<类型>` — 速率限制器（`token-bucket` / `sliding-window`）
- **test** `<名称>` — Jest + Supertest API 测试套件

## 示例

```bash
bash scripts/apigen.sh rest user          # RESTful user endpoints
bash scripts/apigen.sh graphql product    # GraphQL product schema
bash scripts/apigen.sh auth jwt           # JWT authentication
bash scripts/apigen.sh test order         # Order API tests
```

## 输出结果

所有生成的代码都会输出到标准输出（stdout）。可以直接复制到你的项目文件中或将其导入项目中使用。
生成的代码包含完整的注释，可以作为项目的起点。