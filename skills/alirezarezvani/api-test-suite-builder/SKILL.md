---
name: "api-test-suite-builder"
description: "API测试套件构建器（API Test Suite Builder）"
---
# API测试套件构建器

**级别：** 强大  
**类别：** 工程  
**领域：** 测试 / API质量  

---

## 概述  

该工具能够扫描各种框架（Next.js应用路由器、Express、FastAPI、Django REST）中的API路由定义，并自动生成全面的测试套件，涵盖身份验证、输入验证、错误代码、分页、文件上传和速率限制等方面。生成的测试文件可直接用于Vitest+Supertest（Node.js）或Pytest+httpx（Python）进行测试。  

---

## 核心功能  

- **路由检测**：扫描源代码文件以提取所有API端点。  
- **身份验证覆盖**：验证令牌的有效性、过期情况以及是否缺少身份验证头部信息。  
- **输入验证**：检查字段是否缺失、类型是否错误、是否超出范围。  
- **错误代码检测**：为每个路由生成400/401/403/404/422/500等错误代码对应的测试用例。  
- **分页功能**：测试首页、末页、空页以及页面数据量过大的情况。  
- **文件上传**：验证文件上传是否成功、文件大小是否超出限制、MIME类型是否正确以及文件内容是否为空。  
- **速率限制**：检测是否超出单用户或全局的速率限制。  

---

## 使用场景  

- **新增API**：在编写实现代码之前生成测试框架（采用测试驱动开发TDD）。  
- **无测试的旧API**：扫描并生成基础测试用例。  
- **API契约审查**：验证现有测试是否与当前路由定义一致。  
- **发布前回归测试**：确保所有路由至少有基本的测试用例。  
- **安全审计准备**：生成针对恶意输入的测试用例。  

---

## 路由检测  

### Next.js应用路由器  
```bash
# Find all route handlers
find ./app/api -name "route.ts" -o -name "route.js" | sort

# Extract HTTP methods from each route file
grep -rn "export async function\|export function" app/api/**/route.ts | \
  grep -oE "(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)" | sort -u

# Full route map
find ./app/api -name "route.ts" | while read f; do
  route=$(echo $f | sed 's|./app||' | sed 's|/route.ts||')
  methods=$(grep -oE "export (async )?function (GET|POST|PUT|PATCH|DELETE)" "$f" | \
    grep -oE "(GET|POST|PUT|PATCH|DELETE)")
  echo "$methods $route"
done
```  

### Express  
```bash
# Find all router files
find ./src -name "*.ts" -o -name "*.js" | xargs grep -l "router\.\(get\|post\|put\|delete\|patch\)" 2>/dev/null

# Extract routes with line numbers
grep -rn "router\.\(get\|post\|put\|delete\|patch\)\|app\.\(get\|post\|put\|delete\|patch\)" \
  src/ --include="*.ts" | grep -oE "(get|post|put|delete|patch)\(['\"][^'\"]*['\"]"

# Generate route map
grep -rn "router\.\|app\." src/ --include="*.ts" | \
  grep -oE "\.(get|post|put|delete|patch)\(['\"][^'\"]+['\"]" | \
  sed "s/\.\(.*\)('\(.*\)'/\U\1 \2/"
```  

### FastAPI  
```bash
# Find all route decorators
grep -rn "@app\.\|@router\." . --include="*.py" | \
  grep -E "@(app|router)\.(get|post|put|delete|patch)"

# Extract with path and function name
grep -rn "@\(app\|router\)\.\(get\|post\|put\|delete\|patch\)" . --include="*.py" | \
  grep -oE "@(app|router)\.(get|post|put|delete|patch)\(['\"][^'\"]*['\"]"
```  

### Django REST框架  
```bash
# urlpatterns extraction
grep -rn "path\|re_path\|url(" . --include="*.py" | grep "urlpatterns" -A 50 | \
  grep -E "path\(['\"]" | grep -oE "['\"][^'\"]+['\"]" | head -40

# ViewSet router registration
grep -rn "router\.register\|DefaultRouter\|SimpleRouter" . --include="*.py"
```  

---

## 测试生成规则  

### 身份验证测试  

对于每个需要身份验证的API端点，生成以下测试用例：  
| 测试用例 | 预期状态码 |  
|-----------|----------------|  
| 未提供身份验证头部信息 | 401 |  
| 令牌格式错误 | 401 |  
| 令牌有效但用户角色错误 | 403 |  
| 令牌过期 | 401 |  
| 令牌有效但用户角色正确 | 2xx |  
| 使用已删除用户的令牌 | 401 |  

### 输入验证  

对于所有带有请求体的POST/PUT/PATCH请求，生成以下测试用例：  
| 测试用例 | 预期状态码 |  
|-----------|----------------|  
| 请求体为空（`{}`） | 400或422 |  
| 缺少必填字段（每次缺少一个字段） | 400或422 |  
| 类型错误（预期为整数但实际为字符串） | 400或422 |  
| 值超出范围（例如：小于最小值） | 400或422 |  
| 值低于最小值 | 2xx |  
| 值高于最大值 | 2xx |  
| 字符串字段中存在SQL注入攻击 | 400或200（经过安全处理后）  
| 字符串字段中存在XSS攻击 | 400或200（经过安全处理后）  
| 必填字段为空值 | 400或422 |  

---

## 测试文件示例  
→ 详情请参阅`references/example-test-files.md`  

## 从路由扫描生成测试  

使用该工具时，请按照以下步骤操作：  
1. 使用上述命令扫描代码中的API路由。  
2. 阅读每个路由处理函数的代码，了解：  
   - 预期的请求体结构  
   - 身份验证要求（中间件、装饰器）  
   - 返回类型和状态码  
   - 业务规则（例如权限检查）  
3. 根据上述规则为每个路由组生成测试文件。  
4. 为测试用例起描述性名称（例如：“当令牌过期时返回401状态码”）。  
5. 使用测试数据工厂（factories/fixtures）生成测试数据，切勿硬编码ID。  
6. 不仅验证状态码，还要验证响应内容的格式。  

---

## 常见问题  

- **仅测试正常路径**：80%的错误存在于异常路径中，应优先测试这些路径。  
- **测试数据ID硬编码**：使用测试数据工厂，因为ID可能在不同环境中发生变化。  
- **测试之间存在状态依赖**：确保在`afterEach`或`afterAll`中清理测试状态。  
- **测试实现逻辑而非行为**：测试API返回的结果，而非其实现方式。  
- **缺少边界值测试**：在分页和速率限制场景中，边界值错误非常常见。  
- **未测试令牌过期情况**：过期的令牌与无效令牌的行为不同。  
- **忽略Content-Type字段**：测试API是否能够正确处理错误的Content-Type（例如：期望接收JSON但实际收到XML）。  

## 最佳实践  

- 每个API端点对应一个描述性测试块，以便于故障排查和阅读。  
- 仅加载必要的数据，避免加载整个数据库。  
- 使用`beforeAll`进行初始化操作，使用`afterAll`进行清理工作（避免在每个测试前执行耗时的操作）。  
- 验证具体的错误信息或字段内容，而不仅仅是状态码。  
- 确保敏感信息（如密码、密钥）不会出现在响应中。  
- 对于身份验证测试，分别测试“缺少身份验证头部信息”和“令牌无效”的情况。  
- 最后生成速率限制相关的测试用例，因为它们可能与其他测试套件同时运行时产生干扰。