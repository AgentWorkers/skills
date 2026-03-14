---
name: http-api-cloudbase
description: 使用 CloudBase HTTP API，可以通过 HTTP 协议从不使用 SDK 的后端或脚本中访问 CloudBase 平台的功能（数据库、认证、云函数、云托管、云存储、人工智能）。
alwaysApply: false
---
## 何时使用此技能

当您需要通过**原始HTTP API**调用**CloudBase平台功能**时，请使用此技能，例如：

- 非Node后端（Go、Python、Java、PHP等）
- 使用curl或语言HTTP客户端的集成测试或管理脚本
- 通过MySQL RESTful API直接进行数据库操作
- 通过HTTP调用云函数
- 任何不适合使用SDK或不希望使用SDK的场景

**请勿**在以下情况下使用此技能**：
- 使用`@cloudbase/js-sdk`的前端Web应用程序（请使用**CloudBase Web**技能）
- 使用`@cloudbase/node-sdk`的Node.js代码（请使用**CloudBase Node**技能）
- 身份验证流程（请使用**CloudBase Auth HTTP API**技能处理特定于身份验证的端点）

## 如何使用此技能（对于编码代理）

1. **明确场景**
   - 确认此代码将直接调用HTTP端点（而非SDK）。
   - 询问以下信息：
     - `env` – CloudBase环境ID
     - 身份验证方法（AccessToken、API Key或Publishable Key）
   - 确认需要哪个CloudBase功能（数据库、函数、存储等）。
   - **对于用户身份验证**：如果没有指定特定方法，**始终默认使用手机短信验证**——这是对中国用户最友好且最安全的选择。

2. **确定基础URL**
   - 根据地区（国内或国际）使用正确的域名。
   - 默认为国内上海地区。

3. **设置身份验证**
   - 根据使用场景选择适当的身份验证方法。
   - 在请求中添加`Authorization: Bearer <token>`头部。

4. **参考OpenAPI Swagger文档**
   - **必须使用`searchKnowledgeBase`工具**来获取OpenAPI规范
   - 使用`mode=openapi`并指定`apiName`：
     - `mysqldb` - MySQL RESTful API
     - `functions` - Cloud Functions API
     - `auth` - 身份验证API
     - `cloudrun` - CloudRun API
     - `storage` - 存储API
   - 示例：`searchKnowledgeBase({ mode: "openapi", apiName: "mysqldb" })`
   - 解析返回的YAML内容以了解确切的端点路径、参数、请求/响应模式
   - **切勿自行发明端点或参数**——始终参考swagger文档

---

## 概述

CloudBase HTTP API是一组通过HTTP协议访问CloudBase平台功能的接口，支持数据库、用户身份验证、云函数、云托管、云存储、AI等。

## OpenAPI Swagger文档

**⚠️ 重要提示：始终使用`searchKnowledgeBase`工具来获取OpenAPI Swagger规范**

在实现任何HTTP API调用之前，您应该：

1. **使用`searchKnowledgeBase`工具来获取OpenAPI文档**：
   ```
   searchKnowledgeBase({ mode: "openapi", apiName: "<api-name>" })
   ```

2. **可用的API名称**：
   - `mysqldb` - MySQL RESTful API
   - `functions` - Cloud Functions API
   - `auth` - 身份验证API
   - `cloudrun` - CloudRun API
   - `storage` - 存储API

3. **解析并使用swagger文档**：
   - 提取确切的端点路径和HTTP方法
   - 了解必需和可选参数
   - 查看请求/响应模式
   - 检查身份验证要求
   - 验证错误响应格式

## 先决条件

在开始之前，请确保您已经：

1. **创建并激活了CloudBase环境**
2. **拥有身份验证凭据**（AccessToken、API Key或Publishable Key）

## 身份验证和授权

CloudBase HTTP API需要身份验证。根据您的使用场景选择适当的身份验证方法：

### AccessToken身份验证

**适用环境**：客户端/服务器
**用户权限**：已登录用户的权限

**获取方法**：使用`searchKnowledgeBase({ mode: "openapi", apiName: "auth" })`来获取身份验证API规范

### API Key

**适用环境**：服务器
**用户权限**：管理员权限

- **有效期**：长期有效
- **获取方法**：从[CloudBase平台/ApiKey管理页面](https://tcb.cloud.tencent.com/dev?#/identity/token-management)获取

> ⚠️ 警告：Token是身份验证的关键凭据。请妥善保管。API Key不得用于客户端代码。

### Publishable Key

**适用环境**：客户端/服务器
**用户权限**：匿名用户权限

- **有效期**：长期有效
- **获取方法**：从[CloudBase平台/ApiKey管理页面](https://tcb.cloud.tencent.com/dev?#/identity/token-management)获取

> 💡 注意：可以在浏览器中显示，用于请求公开可访问的资源，从而有效减少MAU（每月活跃用户数）。

## API端点URL

CloudBase HTTP API使用统一的域名进行API调用。域名根据环境区域而有所不同。

### 国内地区

对于位于**国内地区**（如上海`ap-shanghai`）的环境，请使用：

```text
https://{your-env}.api.tcloudbasegateway.com
```

将`{your-env}`替换为实际的环境ID。例如，如果环境ID是`cloud1-abc`：

```text
https://cloud1-abc.api.tcloudbasegateway.com
```

### 国际地区

对于位于**国际地区**（如新加坡`ap-singapore`）的环境，请使用：

```text
https://{your-env}.api.intl.tcloudbasegateway.com
```

将`{your-env}`替换为实际的环境ID。例如，如果环境ID是`cloud1-abc`：

```text
https://cloud1-abc.api.intl.tcloudbasegateway.com
```

## 在请求中使用身份验证

将token添加到请求头部：

```http
Authorization: Bearer <access_token/apikey/publishable_key>
```

:::警告 注意
在实际进行调用时，请将包含尖括号`< >`的整个部分替换为您获得的token。例如，如果获得的token是`eymykey`，则填写为：

```http
Authorization: Bearer eymykey
```

:::

## 使用示例

### 云函数调用示例

```bash
curl -X POST "https://your-env-id.api.tcloudbasegateway.com/v1/functions/YOUR_FUNCTION_NAME" \
  -H "Authorization: Bearer <access_token/apikey/publishable_key>" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "age": 25}'
```

有关详细的API规范，请始终下载并参考上述提到的OpenAPI Swagger文件。

## MySQL RESTful API

MySQL RESTful API通过HTTP端点提供所有MySQL数据库操作。

### 基础URL模式

支持三种域名访问模式：

1. `https://{envId}.api.tcloudbasegateway.com/v1/rdb/rest/{table}`
2. `https://{envId}.api.tcloudbasegateway.com/v1/rdb/rest/{schema}/{table}`
3. `https://{envId}.api.tcloudbasegateway.com/v1/rdb/rest/{instance}/{schema}/{table}`

其中：
- `envId`是环境ID
- `instance`是数据库实例标识符
- `schema`是数据库名称
- `table`是表名称

如果使用系统数据库，**建议使用模式1**。

### 请求头部

| 头部 | 参数 | 描述 | 示例 |
|--------|-----------|-------------|---------|
| Accept | `application/json`, `application/vnd.pgrst.object+json` | 控制数据返回格式 | `Accept: application/json` |
| Content-Type | `application/json`, `application/vnd.pgrst.object+json` | 请求内容类型 | `Content-Type: application/json` |
| Prefer | 根据操作类型的不同而变化 | - `return=representation`：写入操作，返回数据体和头部<br>- `return=minimal`：写入操作，仅返回头部（默认）<br>- `count=exact`：读取操作，指定数量<br>- `resolution=merge-duplicates`：插入操作，合并冲突<br>- `resolution=ignore-duplicates`：插入操作，忽略冲突 | `Prefer: return=representation` |
| Authorization | `Bearer <token>` | 身份验证token | `Authorization: Bearer <access_token>` |

### 查询记录

**GET** `/v1/rdb/rest/{table}`

**查询参数**：
- `select`：字段选择，支持`*`或字段列表，支持联合查询（如`class_id(grade,class_number)` |
- `limit`：限制返回的数量
- `offset`：分页偏移量
- `order`：排序字段，格式为`field.asc`或`field.desc`

**示例**：

```bash
# Before URL encoding
curl -X GET 'https://your-env.api.tcloudbasegateway.com/v1/rdb/rest/course?select=name,position&name=like.%张三%&title=eq.文章标题' \
  -H "Authorization: Bearer <access_token>"

# After URL encoding
curl -X GET 'https://your-env.api.tcloudbasegateway.com/v1/rdb/rest/course?select=name,position&name=like.%%E5%BC%A0%E4%B8%89%&title=eq.%E6%96%87%E7%AB%A0%E6%A0%87%E9%A2%98' \
  -H "Authorization: Bearer <access_token>"
```

**响应头部**：
- `Content-Range`：数据范围，例如`0-9/100`（0=起始位置，9=结束位置，100=总记录数）

### 插入记录

**POST** `/v1/rdb/rest/{table}`

**请求体**：JSON对象或对象数组

> 💡 **关于 `_openid` 的说明**：当用户已登录（使用AccessToken身份验证）时，`_openid`字段会**由服务器自动填充**当前用户的身份信息。在INSERT操作中无需手动设置此字段——服务器会根据已验证用户的会话自动填充。

**示例**：

```bash
curl -X POST 'https://your-env.api.tcloudbasegateway.com/v1/rdb/rest/course' \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "name": "数学",
    "position": 1
  }'
```

### 更新记录

**PATCH** `/v1/rdb/rest/{table}`

**请求体**：包含要更新字段的JSON对象

**示例**：

```bash
curl -X PATCH 'https://your-env.api.tcloudbasegateway.com/v1/rdb/rest/course?id=eq.1' \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "name": "高等数学",
    "position": 2
  }'
```

> ⚠️ **重要**：UPDATE操作需要WHERE子句。使用查询参数`?id=eq.1`来指定条件。

### 删除记录

**DELETE** `/v1/rdb/rest/{table}`

**示例**：

```bash
curl -X DELETE 'https://your-env.api.tcloudbasegateway.com/v1/rdb/rest/course?id=eq.1' \
  -H "Authorization: Bearer <access_token>"
```

> ⚠️ **重要**：DELETE操作需要WHERE子句。使用查询参数来指定条件。

### 错误代码和HTTP状态码

| 错误代码 | HTTP状态码 | 描述 |
|------------|-------------|-------------|
| INVALID_PARAM | 400 | 请求参数无效 |
| INVALID_REQUEST | 400 | 请求内容无效：缺少权限字段、SQL执行错误等 |
| INVALID_REQUEST | 406 | 不符合单条记录返回的要求 |
| PERMISSION_DENIED | 401, 403 | 身份验证失败：401表示身份验证失败，403表示授权失败 |
| RESOURCE_NOT_FOUND | 404 | 数据库实例或表未找到 |
| SYS_ERR | 500 | 内部系统错误 |
| OPERATION_FAILED | 503 | 无法建立数据库连接 |
| RESOURCE_UNAVAILABLE | 503 | 由于某些原因数据库不可用 |

### 响应格式

1. 所有POST、PATCH、DELETE操作：如果请求头部包含`Prefer: return=representation`，则表示有响应体；否则只有响应头部。
2. POST、PATCH、DELETE的响应体通常是JSON数组类型`[]`。如果请求头部指定了`Accept: application/vnd.pgrst.object+json`，则返回JSON对象类型`{}`。
3. 如果指定了`Accept: application/vnd.pgrst.object+json`但数据量超过1个，则会返回错误。

### URL编码

在进行请求时，请执行URL编码。例如：

**原始请求**：

```shell
curl -i -X GET 'https://{{host}}/v1/rdb/rest/course?select=name,position&name=like.%张三%&title=eq.文章标题'
```

**编码后的请求**：

```shell
curl -i -X GET 'https://{{host}}/v1/rdb/rest/course?select=name,position&name=like.%%E5%BC%A0%E4%B8%89%&title=eq.%E6%96%87%E7%AB%A0%E6%A0%87%E9%A2%98'
```

## 在线调试工具

CloudBase平台提供了一个[在线调试工具](/http-api/basic/online-api-call)，您可以在不编写代码的情况下测试API接口：

1. 访问API文档页面
2. 找到调试工具入口
3. 输入环境ID和请求参数
4. 点击发送请求以查看响应

## API文档参考

**⚠️ 始终使用`searchKnowledgeBase`工具来获取OpenAPI Swagger规范：**

使用`searchKnowledgeBase({ mode: "openapi", apiName: "<api-name>" })`，其中`<api-name>`包括以下API名称：
- `auth` - 身份验证API
- `mysqldb` - MySQL RESTful API
- `functions` - Cloud Functions API
- `cloudrun` - CloudRun API
- `storage` - 存储API

**如何使用OpenAPI文档**：
1. 使用`searchKnowledgeBase`工具和相应的`apiName`
2. 解析返回的YAML内容以提取：
   - 端点路径（例如 `/v1/rdb/rest/{table}`）
   - HTTP方法（GET、POST、PATCH、DELETE）
   - 路径参数、查询参数、请求体模式
   - 响应模式和状态码
   - 身份验证要求
3. 使用提取的信息构建准确的API调用
4. **切勿假设端点结构**——始终根据swagger文档进行验证

## 常见模式

### 可重用的Shell变量

```bash
env="your-env-id"
token="your-access-token-or-api-key"
base="https://${env}.api.tcloudbasegateway.com"
```

### 常见请求模式

```bash
curl -X GET "${base}/v1/rdb/rest/table_name" \
  -H "Authorization: Bearer ${token}" \
  -H "Content-Type: application/json"
```

### 错误处理

始终检查HTTP状态码和错误响应格式：

```json
{
  "code": "ERROR_CODE",
  "message": "Error message details",
  "requestId": "request-unique-id"
}
```

## 常见身份验证流程

> **🌟 重要提示：默认身份验证方法**
>
> 当用户未指定特定的注册/登录方法时，**始终使用手机短信验证**作为默认和推荐的方法。因为它：
> - ✅ 对中国用户来说最友好
> - ✅ 不需要记住密码
> - ✅ 适用于新用户（注册）和现有用户（登录）
> - ✅ 具有OTP验证，安全性最高
> - ✅ 在CloudBase中默认支持

### 手机号码验证码登录（原生应用程序）⭐ 推荐

这是**原生移动应用程序（iOS/Android/Flutter/React Native）**的首选身份验证流程：

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Step 1: Send Verification Code                                        │
│  POST /auth/v1/verification                                             │
│  Body: { "phone_number": "+86 13800138000", "target": "ANY" }          │
│  ⚠️ IMPORTANT: phone_number MUST include "+86 " prefix WITH SPACE      │
│  Response: { "verification_id": "xxx", "expires_in": 600 }             │
│  📝 SAVE verification_id for next step!                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  Step 2: Verify Code                                                    │
│  POST /auth/v1/verification/verify                                      │
│  Body: { "verification_id": "<saved_id>", "verification_code": "123456" }│
│  Response: { "verification_token": "xxx" }                              │
│  📝 SAVE verification_token for login!                                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  Step 3: Sign In with Token                                             │
│  POST /auth/v1/signin                                                   │
│  Body: { "verification_token": "<saved_token>" }                        │
│  Response: { "access_token": "xxx", "refresh_token": "xxx" }           │
└─────────────────────────────────────────────────────────────────────────┘
```

**⚠️ 重要说明：**
1. **电话号码格式**：必须为`"+86 13800138000"`，国家代码后需加空格
2. **保存 `verification_id`**：从第一步返回，第二步需要它
3. **保存 `verification_token`**：从第二步返回，第三步需要它

## 最佳实践

1. **对于包含特殊字符的查询参数，始终使用URL编码**
2. **对于UPDATE和DELETE操作，务必使用WHERE子句**
3. **使用适当的`Prefer`头部来控制响应格式**
4. **通过检查状态码和错误响应来优雅地处理错误**
5. **妥善保管token**——切勿在客户端代码中暴露API Key**
6. **根据使用场景选择适当的身份验证方法**：
   - 使用AccessToken进行用户特定操作
   - 使用API Key进行服务器端管理操作
   - 使用Publishable Key进行公共/匿名访问
7. **电话号码格式**：始终使用国际格式`"+86 13800138000"`
8. **验证流程**：保存第一步发送的`verification_id`，并在第二步中使用它