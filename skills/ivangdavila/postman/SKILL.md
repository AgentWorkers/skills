---
name: Postman
slug: postman
version: 1.0.0
homepage: https://clawic.com/skills/postman
description: 使用 Postman 的集合（collections）、环境（environments）以及 Newman CLI 来构建、测试和自动化 API。
metadata: {"clawdbot":{"emoji":"📮","requires":{"bins":["newman"]},"os":["linux","darwin","win32"],"install":[{"id":"npm","kind":"npm","package":"newman","bins":["newman"],"label":"Install Newman (npm)"}]}}
changelog: Initial release with collections, environments, and Newman automation.
---
## 设置（Setup）

如果 `~/postman/` 目录不存在，请静默读取 `setup.md` 文件，然后按照文件中的指示进行设置。

## 使用场景（When to Use）

用户需要测试 API、创建 Postman 集合、管理环境，或使用 Newman 运行自动化 API 测试。

## 架构（Architecture）

数据存储在 `~/postman/` 目录下。具体结构请参考 `memory-template.md` 文件。

```
~/postman/
├── memory.md           # Projects, preferences, common patterns
├── collections/        # Postman collection JSON files
└── environments/       # Environment JSON files
```

## 快速参考（Quick Reference）

| 主题 | 文件           |
|-------|--------------|
| 设置     | `setup.md`        |
| 内存模板   | `memory-template.md`    |
| 集合格式   | `collections.md`     |
| Newman 自动化 | `newman.md`      |

## 核心规则（Core Rules）

### 1. 首先定义集合结构（Define the collection structure first）

在创建请求之前，先定义集合的结构：
- 文件夹层次结构应反映 API 的组织结构。
- 使用描述性的名称，例如 `Users > Create User`，而不是 `POST 1`。
- 将相关的接口端点逻辑地分组在一起。

### 2. 始终使用环境变量（Always use environment variables）

不要将会在不同环境中变化的值硬编码到代码中：
```json
{
  "key": "base_url",
  "value": "https://api.example.com",
  "enabled": true
}
```
在请求中使用 `{{base_url}}`。常见的环境配置包括 `dev`、`staging` 和 `prod`。

### 3. 在预请求脚本中处理身份验证（Handle authentication in pre-request scripts）

将身份验证逻辑放在预请求脚本中，而不是手动处理：
```javascript
// Get token and set for collection
pm.sendRequest({
    url: pm.environment.get("auth_url"),
    method: 'POST',
    body: { mode: 'raw', raw: JSON.stringify({...}) }
}, (err, res) => {
    pm.environment.set("token", res.json().access_token);
});
```

### 4. 必须进行测试断言（Test assertions are required）

每个请求都至少需要包含基本的断言逻辑：
```javascript
pm.test("Status 200", () => pm.response.to.have.status(200));
pm.test("Has data", () => pm.expect(pm.response.json()).to.have.property("data"));
```

### 5. 使用 Newman 进行持续集成/持续交付（Use Newman for CI/CD）

使用 Newman 无界面地运行测试集：
```bash
newman run collection.json -e environment.json --reporters cli,json
```
退出代码为 0 表示所有测试均通过。可以将 Newman 集成到持续集成（CI）或持续交付（CD）流程中。

## 集合格式（Collection Format）

### 最小化集合结构（Minimal collection structure）

```json
{
  "info": {
    "name": "My API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get Users",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/users",
        "header": [
          { "key": "Authorization", "value": "Bearer {{token}}" }
        ]
      }
    }
  ]
}
```

### 包含测试的集合（Collections with tests）

```json
{
  "name": "Create User",
  "request": {
    "method": "POST",
    "url": "{{base_url}}/users",
    "body": {
      "mode": "raw",
      "raw": "{\"name\": \"{{$randomFullName}}\", \"email\": \"{{$randomEmail}}\"}",
      "options": { "raw": { "language": "json" } }
    }
  },
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test('Created', () => pm.response.to.have.status(201));",
          "pm.test('Has ID', () => pm.expect(pm.response.json().id).to.exist);"
        ]
      }
    }
  ]
}
```

## 环境配置格式（Environment configuration format）

```json
{
  "name": "Development",
  "values": [
    { "key": "base_url", "value": "http://localhost:3000", "enabled": true },
    { "key": "token", "value": "", "enabled": true }
  ]
}
```

## Newman 命令（Newman commands）

| 任务        | 命令                          |
|------------|------------------------------|
| 基本运行      | `newman run collection.json`            |
| 带环境变量    | `newman run collection.json -e dev.json`       |
| 指定文件夹    | `newman run collection.json --folder "Users"`     |
| 迭代执行    | `newman run collection.json -n 10`         |
| 使用数据文件    | `newman run collection.json -d data.csv`       |
| 生成 HTML 报告   | `newman run collection.json -r htmlextra`       |
| 失败时退出    | `newman run collection.json --bail`         |

## 常见问题（Common issues）

- **硬编码的 URL**：这会导致在不同环境间测试失败。请始终使用 `{{base_url}}`。
- **缺少断言**：虽然测试会显示“通过”，但实际上没有验证任何内容。请添加状态码和响应体检查。
- **在集合中存储敏感信息**：这可能导致凭据泄露。请使用环境变量或 `.gitignore` 文件来隐藏敏感文件。
- **依赖关系混乱**：这可能导致测试结果不稳定。请明确使用 `setNextRequest()` 方法或使测试相互独立。
- **缺少 `Content-Type` 标头**：这会导致 POST/PUT 请求失败。请始终设置 `Content-Type: application/json`。

## 动态变量（Dynamic variables）

Postman 提供了一些内置的动态变量用于测试数据：

| 变量          | 示例值                         |
|-----------------|-------------------------------|
| `{{$randomFullName}}` | "Jane Doe"                     |
| `{{$randomEmail}}` | "jane@example.com"                   |
| `{{$randomUUID}}` | "550e8400-e29b-..."                 |
| `{{$timestamp}}` | 1234567890                     |
| `{{$randomInt}}` | 42                           |

## 将 OpenAPI 导入 Postman（Importing OpenAPI to Postman）

导入 OpenAPI 或 Swagger 规范的方法：
1. 将 OpenAPI 数据导出为 JSON 或 YAML 格式。
2. 在 Postman 中选择“Import” > “File” > “Select spec”。
3. Postman 会自动生成包含所有接口端点的集合。

或者通过命令行工具实现：
```bash
npx openapi-to-postmanv2 -s openapi.yaml -o collection.json
```

## 安全性与隐私（Security & Privacy）

- 所有数据都存储在本地（Data is stored locally）：
  - 集合和环境配置文件位于 `~/postman/` 目录下。
- Newman 在本地运行（Newman runs locally）。

**注意：**  
- 该技能**不**会将集合数据发送到外部服务，也不会将 API 凭据存储在 `memory.md` 文件中。

## 相关技能（Related skills）

如果用户需要，可以使用以下命令进行额外安装：
- `clawhub install <slug>`：安装相关工具。
  - `api`：用于处理 REST API 请求。
  - `json`：用于 JSON 数据的解析和验证。
  - `ci-cd`：用于实现持续集成和持续交付流程的自动化。

## 反馈（Feedback）

- 如果觉得本文档有用，请给它点赞（`clawhub star postman`）。
- 为了保持信息更新，请执行 `clawhub sync` 命令。