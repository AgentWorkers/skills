---
name: cloud-functions
description: >
  **CloudBase云函数开发完整指南**  
  本指南支持 Event Functions（基于 Node.js 的函数）和 HTTP Functions（多语言 Web 服务）的开发。内容涵盖运行时选择、部署、日志记录、函数调用、scf_bootstrap、SSE（Server-Side Encryption，服务器端加密）、WebSocket 以及 HTTP 访问配置等关键环节。
alwaysApply: false
---
# 云函数开发

在开发、部署和管理 CloudBase 云函数时，请使用此技能。CloudBase 支持两种类型的云函数：

- **事件函数（Event Functions）**：由事件（如 SDK 调用、定时器）触发的传统无服务器函数
- **HTTP 函数（HTTP Functions）**：由 HTTP 请求触发的 Web 服务函数，支持多种编程语言

## 何时使用此技能

当您需要执行以下操作时，请使用此技能：

- 创建和部署事件函数（使用 Node.js）
- 创建和部署 HTTP 函数（使用 Node.js/Python/Go/Java）
- 了解运行时限制并进行选择
- 查询函数日志并监控执行情况
- 从应用程序中调用云函数
- 配置 HTTP 访问权限
- 实现 SSE（服务器发送事件，Server-Sent Events）或 WebSocket

**不适用的场景：**
- CloudRun 后端服务（请使用 `cloudrun-development` 技能）
- 复杂的基于容器的服务（请使用 `cloudrun-development` 技能）
- 数据库操作（请使用相应的数据库技能）

## 如何使用此技能（针对编码代理）

1. **选择合适的函数类型**
   - **事件函数**：适用于 SDK 调用、定时任务或基于事件的场景
   - **HTTP 函数**：适用于 Web API、REST 服务、SSE 或 WebSocket 场景

2. **了解运行时限制**
   - 函数创建后 **无法更改** 运行时
   - 必须在创建时选择正确的运行时
   - 如果需要更改运行时，必须先删除函数再重新创建

3. **正确部署函数**
   - **MCP 工具**：使用 `createFunction` 并指定 `type: "Event"` 或 `type: "HTTP"`
   - **CLI**：使用 `tcb fn deploy`（事件函数）或 `tcb fn deploy --httpFn`（HTTP 函数）
   - HTTP 函数需要在函数目录中包含 `scf/bootstrap` 文件
   - 提供正确的 `functionRootPath`（函数文件夹的父目录）

4. **正确查询日志**
   - 使用 `getFunctionLogs` 获取日志列表（基本信息）
   - 使用 `getFunctionLogDetail` 和 `RequestId` 获取详细日志
   - 注意时间范围限制（最多 1 天）

---

## 函数类型比较

| 特性 | 事件函数（Event Function） | HTTP 函数（HTTP Function） |
|---------|---------------------------|----------------------------|
| 触发方式 | 基于事件（SDK、定时器） | HTTP 请求 |
| 入口点 | `exports.main = async (event, context) => {}` | Web 服务器（Express/Flask/Gin 等） |
| 端口 | 不需要指定端口 | **必须监听 9000 端口** |
| 启动文件 | 不需要 | 需要 `scf/bootstrap` 文件 |
| 连接方式 | 短连接 | 支持长连接 |
| 支持的语言 | 仅支持 Node.js | 支持 Node.js、Python、Go、Java |
| 协议 | 不支持 | 支持 HTTP、SSE、WebSocket |

---

## 核心知识 - 事件函数

### 运行时环境

**⚠️ 重要提示：** 函数创建后无法更改运行时**

一旦使用特定运行时创建了云函数，就无法更改该运行时。如果需要更换运行时，请执行以下操作：
1. 删除现有函数
2. 使用新的运行时重新创建函数

**支持的 Node.js 运行时：**
- `Nodejs18.15`（默认值，推荐使用）
- `Nodejs16.13`
- `Nodejs14.18`
- `Nodejs12.16`
- `Nodejs10.15`
- `Nodejs8.9`

**运行时选择指南：**
- **新项目**：建议使用 `Nodejs18.15`（默认值，最新版本）
- 仅在依赖项需要特定 Node.js 版本时选择旧版本
- 考虑安全更新和支持周期
- 在部署前使用所选运行时进行充分测试

### 事件函数结构

事件函数需要：
- **函数目录**：包含函数代码
  - 必须有 `index.js` 文件（或指定的入口文件）
  - 必须导出处理程序：`exports.main = async (event, context) => {}`
  - 包含包含依赖项的 `package.json` 文件

- **函数根目录**：包含所有函数目录的父目录
  - 例如：如果函数位于 `/project/cloudfunctions/myFunction/`，则 `functionRootPath` 应为 `/project/cloudfunctions/`
  **注意**：根目录中 **不能包含函数名称**

- **入口点**：默认为 `index.js` 和 `exports.main`
  - 可以通过 `handler` 参数进行自定义

### 事件函数部署

**创建新函数：**
使用 `createFunction` 工具（具体参数请参阅 MCP 工具文档）：
- **重要提示**：务必明确指定 `func.runtime`（默认为 `Nodejs18.15`）
- 提供 `functionRootPath`（函数文件夹的父目录的绝对路径）
- 使用 `force=true` 选项覆盖现有函数

**更新函数代码：**
使用 `updateFunctionCode` 工具：
- **注意**：仅更新代码，**无法更改运行时**
- 如果需要更改运行时，必须先删除函数再重新创建

**部署最佳实践：**
- 创建函数时始终明确指定运行时
- 使用绝对路径作为 `functionRootPath`
- **不要上传 `node_modules` 文件**——依赖项会自动安装
- 尽可能在部署前进行本地测试
- 使用环境变量进行配置，避免使用硬编码值

---

## 核心知识 - HTTP 函数

### HTTP 函数概述

HTTP 函数专为 Web 服务场景优化，支持标准的 HTTP 请求/响应模式。

**关键特性：**
- **必须监听 9000 端口**（平台要求）
- 需要 `scf/bootstrap` 启动脚本
- 支持多种编程语言：Node.js、Python、Go、Java
- 支持 HTTP、SSE、WebSocket 协议

### `scf/bootstrap` 启动脚本

**⚠️ 重要提示：** HTTP 函数必须使用 `scfbootstrap` 文件**

| 要求 | 说明 |
|-------------|-------------|
| 文件名**：** 必须为 `scfbootstrap`（不带扩展名） |
| 权限**：** 必须具有执行权限（`chmod +x scfbootstrap`） |
| 端口**：** 必须在 9000 端口启动服务器 |
| 行结束符**：** 必须使用 LF（Unix），而不是 CRLF（Windows） |

**示例：**
```bash
# Node.js
#!/bin/bash
node index.js

# Python
#!/bin/bash
export PYTHONPATH="./third_party:$PYTHONPATH"
/var/lang/python310/bin/python3.10 app.py

# Go
#!/bin/bash
./main

# Java
#!/bin/bash
java -jar *.jar
```

### HTTP 函数结构与示例

**Node.js 示例（使用 Express）：**
```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => res.json({ message: 'Hello!' }));
app.listen(9000);  // Must be port 9000
```

### HTTP 函数部署

**MCP 工具：**
```javascript
createFunction({
  func: {
    name: "myHttpFunction",
    type: "HTTP",           // Required for HTTP Function
    protocolType: "HTTP",   // "HTTP" (default) or "WS" (WebSocket)
    timeout: 60
  },
  functionRootPath: "/path/to/functions",
  force: false
})
```

**CLI：**
```bash
tcb fn deploy <name> --httpFn        # HTTP Function
tcb fn deploy <name> --httpFn --ws   # With WebSocket
```

**注意：**
- 函数类型 **创建后无法更改**
- HTTP 函数不会自动安装依赖项；需要手动添加 `node_modules` 文件

### 调用 HTTP 函数

**方法 1：HTTP API（使用访问令牌）**
```bash
curl -L 'https://{envId}.api.tcloudbasegateway.com/v1/functions/{name}?webfn=true' \
  -H 'Authorization: Bearer <TOKEN>'
```
**注意**：必须包含 `webfn=true` 参数

**方法 2：HTTP 访问服务（自定义域名）**

使用 `createFunctionHTTPAccess` MCP 工具配置 HTTP 访问：
```javascript
createFunctionHTTPAccess({
  name: "myHttpFunction",
  type: "HTTP",           // "HTTP" for HTTP Function
  path: "/api/hello",     // Trigger path
  // domain: "your-domain.com"  // Optional custom domain
})
```

```bash
# Access via default domain
curl https://{envId}.{region}.app.tcloudbase.com/{path}

# Access via custom domain
curl https://your-domain.com/{path}
```

| 方法 | 是否需要认证 | 适用场景 |
|--------|--------------|----------|
| HTTP API (`?webfn=true`) | 是（需要Bearer Token） | 服务器间通信 |
| HTTP 访问服务 | 可选 | 浏览器、公共 API |

### SSE 和 WebSocket 支持

**SSE（服务器发送事件，Server-Sent Events）：** 默认启用，用于服务器到客户端的实时数据流（例如 AI 聊天、进度更新）。
```javascript
// Server
res.setHeader('Content-Type', 'text/event-stream');
res.write(`data: ${JSON.stringify({ content: 'Hello' })}\n\n`);

// Client
const es = new EventSource('https://your-domain/stream');
es.onmessage = (e) => console.log(JSON.parse(e.data));
```

**WebSocket：** 通过 `createFunction` 中的 `protocolType: "WS"` 启用。支持双向实时通信。

| 限制 | 值 |
|-------|-------|
| 空闲超时**：** 10 到 7200 秒 |
| 最大消息大小**：** 256KB |

---

### 函数日志

**查询日志：**

**主要方法：** 使用 `getFunctionLogs` 和 `getFunctionLogDetail` 工具（详见 MCP 工具文档）。

**备用方法（备用方案）：** 如果这些工具不可用，可以使用 `callCloudApi`：
- **获取日志列表**：使用 `GetFunctionLogs` 操作：
```
callCloudApi({
  service: "tcb",
  action: "GetFunctionLogs",
  params: {
    EnvId: "{envId}",
    FunctionName: "functionName",
    Offset: 0,
    Limit: 10,
    StartTime: "2024-01-01 00:00:00",
    EndTime: "2024-01-01 23:59:59",
    LogRequestId: "optional-request-id",
    Qualifier: "$LATEST"
  }
})
```

- **获取日志详情**：使用 `GetFunctionLogDetail` 操作（需要步骤 1 中的 RequestId）：
```
callCloudApi({
  service: "tcb",
  action: "GetFunctionLogDetail",
  params: {
    StartTime: "2024-01-01 00:00:00",
    EndTime: "2024-01-01 23:59:59",
    LogRequestId: "request-id-from-log-list"
  }
})
```

**日志查询限制：**
- `Offset` 和 `Limit` 的总和不能超过 10000
- `StartTime` 和 `EndTime` 的时间范围不能超过 1 天
- 对于较长的时间范围，需要分页查询

**日志查询最佳实践：**
- 在 1 天的时间范围内查询日志
- 使用 `RequestId` 进行特定调用的调试
- 结合列表查询和详细查询以获取完整调试信息
- 部署后检查日志以验证函数行为

### 调用事件函数

**从 Web 应用程序调用：**
```javascript
import cloudbaseSDK from "@cloudbase/js-sdk";

const cloudbase = cloudbaseSDK.init({
  env: 'your-env-id',
  region: 'ap-shanghai',
  accessKey: 'your-access-key'
});

// Call event function
const result = await cloudbase.callFunction({
  name: "functionName",
  data: { /* function parameters */ }
});
```

**从小程序调用：**
```javascript
wx.cloud.callFunction({
  name: "functionName",
  data: { /* function parameters */ }
}).then(res => {
  console.log(res.result);
});
```

**从 Node.js 后端调用：**
```javascript
const cloudbase = require("@cloudbase/node-sdk");

const app = cloudbase.init({
  env: "your-env-id"
});

const result = await app.callFunction({
  name: "functionName",
  data: { /* function parameters */ }
});
```

**通过 HTTP API 调用：**

使用 CloudBase HTTP API 调用事件函数：
- 端点：`https://{envId}.api.tcloudbasegateway.com/v1/functions/{functionName}``
- 需要认证令牌（Bearer Token）
- 详情请参阅 `http-api` 技能

### HTTP 访问配置（针对事件函数）

**HTTP 访问与 HTTP API 的区别：**
- **HTTP API**：使用 CloudBase API 端点并需要认证令牌
- **HTTP 访问**：创建直接的 HTTP/HTTPS 端点，用于标准 REST API 访问

**创建 HTTP 访问：**

**主要方法：** 使用 `createFunctionHTTPAccess` 工具（详见 MCP 工具文档）。

**备用方法（备用方案）：** 如果该工具不可用，可以使用 `callCloudApi` 和 `CreateCloudBaseGWAPI`：

```
callCloudApi({
  service: "tcb",
  action: "CreateCloudBaseGWAPI",
  params: {
    EnableUnion: true,
    Path: "/api/users",
    ServiceId: "{envId}",
    Type: 6,
    Name: "functionName",
    AuthSwitch: 2,
    PathTransmission: 2,
    EnableRegion: true,
    Domain: "*"  // Use "*" for default domain, or custom domain name
  }
})
```

**关键参数：**
- `Type`：函数类型（必填）
- `AuthSwitch`：是否需要认证（1 表示需要认证）
- `Domain`：默认域名，或指定自定义域名

**访问地址：** `https://{envId}.{region}.app.tcloudbase.com/{path}` 或 `https://{domain}/{path}`

### 函数配置**

**环境变量：**

在创建或更新函数时通过 `func.envVariables` 设置：
```javascript
{
  envVariables: {
    "DATABASE_URL": "mysql://...",
    "API_KEY": "secret-key"
  }
}
```

**⚠️ 重要提示：** 更新环境变量时的注意事项**

在更新现有函数的环境变量时：
1. **必须先使用 `getFunctionList` 和 `action=detail` 查询当前环境变量**
2. **必须将新环境变量与现有环境变量合并**
3. **不要直接覆盖** 现有环境变量（否则会删除未包含在更新中的变量）

**正确的更新方式：**
```javascript
// 1. First, get current function details
const currentFunction = await getFunctionList({
  action: "detail",
  name: "functionName"
});

// 2. Merge existing envVariables with new ones
const mergedEnvVariables = {
  ...currentFunction.EnvVariables,  // Existing variables
  ...newEnvVariables                 // New/updated variables
};

// 3. Update with merged variables
await updateFunctionConfig({
  funcParam: {
    name: "functionName",
    envVariables: mergedEnvVariables
  }
});
```

**为什么这很重要：**
- 直接覆盖环境变量会导致未包含在更新中的变量被删除
- 如果删除了关键环境变量，可能会导致函数无法正常运行
- 在进行部分更新时，请务必保留现有配置

**超时配置：**

通过 `func.timeout`（单位：秒）设置超时：
- 默认超时时间因运行时而异
- 最大超时时间取决于运行时版本
- 设置超时时请考虑函数的执行时间

**定时器触发：**

通过 `func.triggers` 配置：
- 类型：`timer`（仅支持此类型）
- 配置：Cron 表达式（7 个字段：秒、分钟、小时、日期、星期、月份、年份）
- 例如：`"0 0 2 1 * * *"` - 每月 1 日凌晨 2:00
- `0 30 9 * * * *` - 每天上午 9:30

**VPC 配置：**

用于访问 VPC 资源：
```javascript
{
  vpc: {
    vpcId: "vpc-xxxxx",
    subnetId: "subnet-xxxxx"
  }
}
```

## MCP 工具参考

**函数管理：**
- `getFunctionList`：列出函数或获取函数详情
- `createFunction`：创建云函数（通过 `type` 参数支持事件函数和 HTTP 函数）
  - `type: "Event"`：事件函数（默认值）
  - `type: "HTTP"`：HTTP 函数
  - `protocolType: "WS"`：为 HTTP 函数启用 WebSocket
- `updateFunctionCode`：更新函数代码（运行时无法更改）
- `updateFunctionConfig`：更新函数配置（**注意**：更新环境变量时，必须先查询并合并现有值以避免覆盖）

**日志记录：**
- `getFunctionLogs`：获取函数日志列表（基本信息）
- `getFunctionLogDetail`：通过 RequestId 获取详细日志内容
- `callCloudApi`（备用方案）：如果直接工具不可用，可以使用 `GetFunctionLogs` 和 `GetFunctionLogDetail` 操作

**HTTP 访问：**
- `createFunctionHTTPAccess`：为函数创建 HTTP 访问（通过 `type` 参数支持事件函数和 HTTP 函数）
- `callCloudApi`（备用方案）：如果直接工具不可用，可以使用 `CreateCloudBaseGWAPI` 操作

**触发器：**
- `manageFunctionTriggers`：创建或删除函数触发器

**CLI 命令：**
- `tcb fn deploy <name>`：部署事件函数
- `tcb fn deploy <name> --httpFn`：部署 HTTP 函数
- `tcb fn deploy <name> --httpFn --ws`：部署带有 WebSocket 的 HTTP 函数
- `tcb fn deploy --all`：部署配置中的所有函数

## 常见模式

### 错误处理**
```javascript
exports.main = async (event, context) => {
  try {
    // Function logic
    return {
      code: 0,
      message: "Success",
      data: result
    };
  } catch (error) {
    return {
      code: -1,
      message: error.message,
      data: null
    };
  }
};
```

### 环境变量使用**
```javascript
exports.main = async (event, context) => {
  const apiKey = process.env.API_KEY;
  const dbUrl = process.env.DATABASE_URL;
  
  // Use environment variables
};
```

### 数据库操作**
```javascript
const cloudbase = require("@cloudbase/node-sdk");

const app = cloudbase.init({
  env: process.env.ENV_ID
});

exports.main = async (event, context) => {
  const db = app.database();
  const result = await db.collection("users").get();
  return result;
};
```

## 最佳实践**

### 通用最佳实践**
1. **运行时选择**：始终明确指定运行时，新项目建议使用 `Nodejs18.15`
2. **代码组织**：保持函数功能单一、用途明确
3. **错误处理**：始终实现适当的错误处理
4. **环境变量**：使用环境变量进行配置，避免硬编码敏感信息
5. **日志记录**：添加有意义的日志以便调试
6. **测试**：尽可能在部署前进行本地测试
7. **安全性**：为 HTTP 访问实现认证/授权
8. **性能**：优化冷启动时间，对数据库使用连接池
9. **监控**：定期检查日志并监控函数性能
10. **文档**：记录函数参数和返回值

### HTTP 函数的特定最佳实践**
1. **端口配置**：始终监听 9000 端口
2. **scf/bootstrap**：确保文件权限正确，行结束符使用 LF
3. **健康检查**：添加 `/health` 端点以进行监控
4. **CORS**：配置 CORS 头以支持浏览器访问
5. **优雅关闭**：正确处理进程信号
6. **依赖项**：将 `node_modules` 文件包含在包中，或使用依赖层（HTTP 函数不自动安装依赖项）
7. **超时**：为长时间运行的 SSE/WebSocket 连接设置适当的超时
8. **错误响应**：返回适当的 HTTP 状态码和错误信息

### 事件函数与 HTTP 函数的选择**

| 场景 | 推荐函数类型 |
|----------|-----------------|
| SDK/小程序调用**：** 事件函数 |
| 定时任务（cron）**：** 事件函数 |
| REST API / Web 服务**：** HTTP 函数 |
| SSE 流媒体（例如 AI 聊天）**：** HTTP 函数 |
| WebSocket 实时通信**：** HTTP 函数 |
| 文件上传/下载**：** HTTP 函数 |
| 多语言支持**：** HTTP 函数 |

## 相关技能**

- `cloudrun-development`：用于基于容器的后端服务
- `http-api`：用于 HTTP API 调用
- `cloudbase-platform`：用于了解 CloudBase 平台的其他功能