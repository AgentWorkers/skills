---
name: rest-to-graphql
description: 将 REST API 路由转换为 GraphQL 模型。这在迁移 API 或添加 GraphQL 层时非常有用。
---

# REST到GraphQL转换器

你有一个REST API，想要将其转换为GraphQL吗？只需将这个工具指向你的API路由，它就能生成包含类型、查询和mutation的完整GraphQL模式。无需任何手动转换。

**一个命令即可完成转换，无需任何配置。**  

## 快速入门

```bash
npx ai-rest-to-graphql ./src/routes
```

## 功能介绍

- 分析你的REST端点并生成相应的GraphQL模式  
- 将CRUD操作转换为GraphQL的查询和mutation  
- 生成TypeScript类型文件  
- 将REST资源映射到具有正确关系的GraphQL类型  
- 提供调用现有REST处理函数的resolver stub（示例代码）  

## 使用示例

```bash
# Convert routes directory
npx ai-rest-to-graphql ./src/routes

# Single resource
npx ai-rest-to-graphql ./src/routes/users.ts

# Include resolver implementations
npx ai-rest-to-graphql ./src/routes --with-resolvers

# Output to specific file
npx ai-rest-to-graphql ./src/routes -o ./schema.graphql

# Keep REST as datasource
npx ai-rest-to-graphql ./src/routes --wrap-rest
```

## 最佳实践  

- **从核心资源开始转换**：不要一次性转换所有内容  
- **检查生成的类型**：虽然AI会自动映射字段，但请手动核对字段之间的关系  
- **作为迁移指南使用**：输出结果会显示API在GraphQL中的对应结构  
- **考虑使用网关（gateway）方案**：用GraphQL包装REST接口，而不是直接替换它们  

## 适用场景  

- 为现有的REST API添加GraphQL支持  
- 了解你的API在GraphQL中的表现形式  
- 在微服务架构中构建统一的接口层（BFF，Backend-Frontend Gateway）  
- 通过查看自己的数据模型来学习GraphQL  

## 属于LXGIC开发工具包的一部分  

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本无需支付费用、注册或API密钥，直接可以使用这些工具。  

**了解更多信息：**  
- GitHub: https://github.com/LXGIC-Studios  
- Twitter: https://x.com/lxgicstudios  
- Substack: https://lxgicstudios.substack.com  
- 官网: https://lxgic.dev  

## 使用要求  

无需安装，只需使用`npx`命令运行即可。建议使用Node.js 18及以上版本。  

```bash
npx ai-rest-to-graphql --help
```

## 工作原理  

该工具解析你的REST路由定义，以理解你的资源及其操作方式。它将GET请求映射为查询，将POST/PUT/DELETE请求映射为mutation，并根据请求和响应的模式推断出数据类型结构。  

## 许可证  

采用MIT许可证，永久免费。你可以自由使用该工具。