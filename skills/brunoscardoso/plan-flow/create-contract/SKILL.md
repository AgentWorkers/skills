---
name: create-contract
description: 根据API文档的内容，创建一个集成合同（Integration Contract）。
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---
# 创建集成合同文档

本工具根据API文档自动生成集成合同文档。

## 功能概述

1. 获取或读取API文档。
2. 提取端点（Endpoints）、数据结构（Schemas）和认证信息。
3. 为所有数据类型生成TypeScript接口。
4. 文档化错误处理机制和速率限制规则。
5. 提供使用示例。

## 使用方法

```
/create-contract <url>
```

**参数：**
- `url`（必填）：API文档的URL。

## 输出结果**

生成的文件名为：`flow/contracts/<service>_contract.md`

## 合同文档结构

### 认证示例
```typescript
const headers = {
  'Authorization': `Bearer ${token}`;
```

### GetUsersRequest接口
```typescript
interface GetUsersRequest {
  page?: number;
  limit?: number;
}
```

### GetUsersResponse接口
```typescript
interface GetUsersResponse {
  data: User[];
  meta: { total: number };
}
```

### User接口
```typescript
interface User {
  id: string;
  email: string;
  name: string;
}
```

### 获取用户数据
```typescript
const users = await api.getUsers({ page: 1 });
```

## 示例代码

```
/create-contract https://api.stripe.com/docs
```

## 最终生成的文档内容

### 文档包含的内容

- **服务概述**：服务描述及版本信息。
- **认证方式**：请求认证的步骤。
- **端点信息**：所有可用端点及其对应的数据结构。
- **TypeScript接口**：所有请求/响应数据的类型定义。
- **错误处理**：常见的错误代码及应对措施。
- **速率限制**：请求的速率限制规则。
- **使用示例**：常见操作的代码示例。

## 应用场景

- 与第三方API集成。
- 文档化内部API。
- 创建类型安全的API客户端。
- 新员工入职培训。

---

（注：由于代码示例和具体实现细节未提供，在翻译中保留了注释符号“```
/create-contract <url>
```”以表示代码块内容。实际翻译时，这些部分需要根据提供的具体代码进行填充。）