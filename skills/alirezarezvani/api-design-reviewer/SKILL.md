# API设计审核工具

**级别：** 高级  
**类别：** 工程 / 架构  
**维护者：** Claude Skills团队  

## 概述  

API设计审核工具提供对API设计的全面分析和审核，重点关注REST规范、最佳实践和行业标准。该工具通过自动化代码检查、破坏性变更检测以及设计评分机制，帮助工程团队构建一致、可维护且设计良好的API。  

## 核心功能  

### 1. API代码检查与规范分析  
- **资源命名规范**：强制使用驼峰式（camelCase）命名资源，使用kebab-case命名字段  
- **HTTP方法使用**：验证GET、POST、PUT、PATCH、DELETE方法的使用是否正确  
- **URL结构**：分析端点模式，确保其符合RESTful设计原则  
- **状态码合规性**：确保使用正确的HTTP状态码  
- **错误响应格式**：验证错误响应结构的一致性  
- **文档完整性**：检查是否存在缺失的描述或文档遗漏  

### 2. 破坏性变更检测  
- **端点删除**：检测被移除或弃用的端点  
- **响应结构变更**：识别响应结构的修改  
- **字段删除**：跟踪API响应中被移除或重命名的字段  
- **字段类型变更**：捕捉可能影响客户端功能的字段类型变更  
- **新增必填字段**：标记可能破坏现有集成的新必填字段  
- **状态码变更**：检测预期的状态码是否发生变化  

### 3. API设计评分与评估  
- **一致性分析**（30%）：评估命名规范、响应模式和结构的一致性  
- **文档质量**（20%）：评估API文档的完整性和清晰度  
- **安全性实现**（20%）：审查认证、授权和安全头部  
- **可用性设计**（15%）：分析易用性、可发现性和开发者体验  
- **性能优化**（15%）：评估缓存、分页和效率机制  

## REST设计原则  

### 资源命名规范  
```
✅ Good Examples:
- /api/v1/users
- /api/v1/user-profiles
- /api/v1/orders/123/line-items

❌ Bad Examples:
- /api/v1/getUsers
- /api/v1/user_profiles
- /api/v1/orders/123/lineItems
```  

### HTTP方法使用  
- **GET**：获取资源（安全、幂等操作）  
- **POST**：创建新资源（非幂等操作）  
- **PUT**：替换整个资源（幂等操作）  
- **PATCH**：部分资源更新（不一定幂等）  
- **DELETE**：删除资源（幂等操作）  

### URL结构最佳实践  
```
Collection Resources: /api/v1/users
Individual Resources: /api/v1/users/123
Nested Resources: /api/v1/users/123/orders
Actions: /api/v1/users/123/activate (POST)
Filtering: /api/v1/users?status=active&role=admin
```  

## 版本控制策略  

### 1. URL版本控制（推荐）  
```
/api/v1/users
/api/v2/users
```  
**优点**：清晰、明确，易于路由  
**缺点**：可能导致URL数量增加，增加缓存复杂性  

### 2. 请求头版本控制  
```
GET /api/users
Accept: application/vnd.api+json;version=1
```  
**优点**：URL更简洁，便于内容协商  
**缺点**：不太直观，手动测试难度较大  

### 3. 媒体类型版本控制  
```
GET /api/users
Accept: application/vnd.myapi.v1+json
```  
**优点**：符合RESTful设计，支持多种数据表示形式  
**缺点**：实现复杂，难度较高  

### 4. 查询参数版本控制  
```
/api/users?version=1
```  
**优点**：实现简单  
**缺点**：不符合RESTful设计原则，可能被忽略  

## 分页模式  

### 基于偏移量的分页  
```json
{
  "data": [...],
  "pagination": {
    "offset": 20,
    "limit": 10,
    "total": 150,
    "hasMore": true
  }
}
```  

### 基于游标的分页  
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTIzfQ==",
    "hasMore": true
  }
}
```  

### 基于页码的分页  
```json
{
  "data": [...],
  "pagination": {
    "page": 3,
    "pageSize": 10,
    "totalPages": 15,
    "totalItems": 150
  }
}
```  

## 错误响应格式  

### 标准错误结构  
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid parameters",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email address is not valid"
      }
    ],
    "requestId": "req-123456",
    "timestamp": "2024-02-16T13:00:00Z"
  }
}
```  

### HTTP状态码使用  
- **400 Bad Request**：请求语法或参数无效  
- **401 Unauthorized**：需要认证  
- **403 Forbidden**：访问被拒绝（已认证但权限不足）  
- **404 Not Found**：资源未找到  
- **409 Conflict**：资源冲突（重复或版本不匹配）  
- **422 Unprocessable Entity**：语法正确但存在语义错误  
- **429 Too Many Requests**：超出请求速率限制  
- **500 Internal Server Error**：服务器内部错误  

## 认证与授权机制  

### 承载令牌认证  
```
Authorization: Bearer <token>
```  

### API密钥认证  
```
X-API-Key: <api-key>
Authorization: Api-Key <api-key>
```  

### OAuth 2.0流程  
```
Authorization: Bearer <oauth-access-token>
```  

### 基于角色的访问控制（RBAC）  
```json
{
  "user": {
    "id": "123",
    "roles": ["admin", "editor"],
    "permissions": ["read:users", "write:orders"]
  }
}
```  

## 速率限制实现  

### 请求头  
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```  

### 超过速率限制时的响应  
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 3600
  }
}
```  

## HATEOAS（超媒体作为应用状态引擎）  
```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "_links": {
    "self": { "href": "/api/v1/users/123" },
    "orders": { "href": "/api/v1/users/123/orders" },
    "profile": { "href": "/api/v1/users/123/profile" },
    "deactivate": { 
      "href": "/api/v1/users/123/deactivate",
      "method": "POST"
    }
  }
}
```  

## 示例实现  
```
POST /api/v1/payments
Idempotency-Key: 123e4567-e89b-12d3-a456-426614174000
```  

## 幂等性  

- **GET**：始终是安全且幂等的操作  
- **PUT**：应具有幂等性（替换整个资源）  
- **DELETE**：应具有幂等性（结果相同）  
- **PATCH**：可能具有幂等性，也可能不具有  

### 幂等性验证机制  
```
Cache-Control: public, max-age=3600
ETag: "123456789"
Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT
```  

## 向后兼容性指南  

- **非破坏性变更**：  
  - 在请求中添加可选字段  
  - 在响应中添加字段  
  - 添加新端点  
  - 将必填字段设为可选  
  - 添加新的枚举值（并妥善处理兼容性问题）  

- **破坏性变更**：  
  - 从响应中移除字段  
  - 将可选字段设为必填  
  - 修改字段类型  
  - 移除端点  
  - 修改URL结构  
  - 修改错误响应格式  

## OpenAPI/Swagger验证  

### 必需组件  
- **API信息**：标题、描述、版本  
- **服务器信息**：基础URL和描述  
- **路径定义**：所有端点及其对应的HTTP方法  
- **参数定义**：查询参数、路径参数和请求头参数  
- **请求/响应模式**：完整的数据模型  
- **安全定义**：认证方案  
- **错误响应**：标准错误格式  

### 最佳实践  
- 使用一致的命名规范  
- 为所有组件提供详细说明  
- 为复杂对象提供示例  
- 定义可重用的组件和模式  
- 验证是否符合OpenAPI规范  

## 性能优化考虑  

### 缓存策略  
```yaml
- name: API Linting
  run: python scripts/api_linter.py openapi.json

- name: Breaking Change Detection
  run: python scripts/breaking_change_detector.py openapi-v1.json openapi-v2.json

- name: API Scorecard
  run: python scripts/api_scorecard.py openapi.json
```  

### 高效数据传输  
- 使用适当的HTTP方法  
- 实现字段选择（如`?fields=id,name,email`）  
- 支持压缩（gzip）  
- 实现高效的分页机制  
- 使用ETags进行条件性请求  

### 资源优化  
- 避免N+1查询  
- 实现批量操作  
- 对复杂操作使用异步处理  
- 支持部分更新（PATCH）  

## 安全最佳实践  

### 输入验证  
- 验证所有输入参数  
- 对用户数据进行清洗  
- 使用参数化查询  
- 实现请求大小限制  

### 认证与安全  
- 在所有接口中使用HTTPS  
- 实现安全的令牌存储  
- 支持令牌过期和刷新  
- 使用强密码认证机制  

### 授权控制  
- 实施最小权限原则  
- 使用基于资源的权限控制  
- 支持细粒度访问控制  
- 审计访问行为  

## 工具与脚本  

### `api_linter.py`  
- 分析API规范是否符合REST规范和最佳实践。  
  - 支持OpenAPI/Swagger规范验证  
  - 检查命名规范  
  - 验证HTTP方法的使用  
  - 确保错误格式的一致性  
  - 检查文档的完整性  

### `breaking_change_detector.py`  
- 比较API规范版本，识别破坏性变更。  
  - 检测端点的增减  
  - 跟踪字段的修改  
  - 生成迁移指南  
  - 评估变更的影响严重程度  

### `api_scorecard.py**  
- 提供API设计质量的综合评分。  
  - 多维度评分  
  - 提供详细的改进建议  
  - 以字母等级（A-F）评估质量  
  - 支持基准测试和进度跟踪  

## 集成示例  

### CI/CD集成  
```yaml
- name: API Linting
  run: python scripts/api_linter.py openapi.json

- name: Breaking Change Detection
  run: python scripts/breaking_change_detector.py openapi-v1.json openapi-v2.json

- name: API Scorecard
  run: python scripts/api_scorecard.py openapi.json
```  

### 提交前钩子（Pre-commit Hooks）  
```bash
#!/bin/bash
python engineering/api-design-reviewer/scripts/api_linter.py api/openapi.json
if [ $? -ne 0 ]; then
  echo "API linting failed. Please fix the issues before committing."
  exit 1
fi
```  

## 最佳实践总结  

1. **一致性优先**：保持命名、响应格式和模式的一致性  
2. **文档编写**：提供全面、最新的API文档  
3. **版本控制**：制定清晰的版本控制策略以支持API演进  
4. **错误处理**：实现一致且信息丰富的错误响应  
5. **安全性**：从设计阶段就考虑安全性  
6. **性能优化**：从一开始就考虑可扩展性和效率  
7. **向后兼容性**：减少破坏性变更，并提供迁移路径  
8. **测试**：实施全面的测试，包括契约测试  
9. **监控**：监控API的使用情况和性能  
10. **开发者体验**：优先考虑易用性和清晰的文档  

## 需避免的常见反模式  

- **基于动词的URL**：使用名词表示资源，而非操作  
- **不一致的响应格式**：保持标准的响应结构  
- **过度嵌套**：避免深度嵌套的资源层次结构  
- **忽略HTTP状态码**：根据不同场景使用正确的状态码  
- **错误信息不清晰**：提供明确、可操作的错误信息  
- **缺乏分页功能**：所有列表端点都应支持分页  
- **无版本控制**：从一开始就规划API的演进  
- **暴露内部结构**：设计API时考虑外部使用，而非内部便利性  
- **未实施速率限制**：保护API免受滥用和过载  
- **测试不足**：全面测试所有方面，包括错误情况和边缘情况  

## 结论  

API设计审核工具为构建、审核和维护高质量的REST API提供了全面的框架。通过遵循这些指南并使用相关工具，开发团队可以创建出一致、文档齐全、安全且易于维护的API。  

定期使用代码检查工具、破坏性变更检测工具和评分工具，可以确保API质量的持续提升，并在整个开发生命周期中保持其高质量。