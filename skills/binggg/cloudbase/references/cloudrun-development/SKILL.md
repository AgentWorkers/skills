---
name: cloudrun-development
description: CloudBase 运行后端开发规则（函数模式/容器模式）：在部署需要长时间连接、多语言支持、自定义环境或 AI 代理开发的后端服务时，请使用此规则。
alwaysApply: false
---
## 何时使用此技能

当您需要进行**CloudBase Run后端服务开发**时，请使用此技能，特别是在以下情况下：

- **需要长时间连接功能**：WebSocket、SSE或服务器推送（server push）。
- **需要长时间运行或持续运行的进程**：这些任务不适合使用云函数（cloud functions）或后台作业（background jobs）。
- **需要自定义运行时环境或系统依赖**：例如自定义镜像（custom images）或特定的系统库（specific system libraries）。
- **需要支持多种语言或任意框架**：如Java、Go、PHP、.NET、Python、Node.js等。
- **需要稳定且具备弹性扩展能力的外部服务**：按需付费（pay-as-you-go），并且能够降级到0资源使用量（scale down to 0）。
- **需要私有或内部网络访问**：VPC/PRIVATE网络访问，或者通过小程序（mini-program）进行内部直接连接（internal direct connection）。
- **需要开发AI代理**：基于CloudRun的功能模式（Function mode）来开发个性化的AI应用程序。

**请勿用于以下情况**：
- **简单的云函数**（请使用云函数开发方式）。
- **仅用于前端的应用程序**。
- **数据库模式设计**（请使用专门的数据模型创建技能）。

---

## 如何使用此技能（针对编程代理）

1. **选择合适的模式**
   - **功能模式（Function mode）**：最快上手的方式，内置HTTP/WebSocket/SSE支持，固定端口为3000，支持本地运行。
   - **容器模式（Container mode）**：支持任何语言和运行时环境，需要Dockerfile，工具不支持本地运行。

2. **遵循必备要求**
   - 必须监听`PORT`环境变量（容器中的实际端口）。
   - 服务应该是无状态的（stateless），数据需要写入外部存储（如数据库、缓存等）。
   - 请求之外不应有后台的持久线程或进程。
   - 尽量减少依赖项，使用轻量级的镜像（slim images），以降低冷启动时间和部署时间。
   - 遵循资源限制：内存（Mem）应为CPU容量的两倍（例如，0.25 vCPU对应0.5 GB内存）。
   - 访问控制：对于Web场景，仅启用公共网络；对于小程序，建议关闭公共网络以使用内部直接连接。

3. **正确使用工具**
   - **读取操作**：`queryCloudRun`（用于列出、查看详细信息或使用模板）。
   - **写入操作**：`manageCloudRun`（用于初始化、下载、运行、部署、删除或创建代理）。
   - 对于`targetPath`参数，始终使用绝对路径。
   - 在执行删除操作时，务必设置`force: true`。

4. **遵循工作流程**
   - 初始化项目 → 检查/生成Dockerfile（针对容器模式） → 在本地运行（仅限功能模式） → 配置访问权限 → 部署 → 验证。

---

# CloudBase Run AI开发规则

本指南为AI助手和工程协作提供了“何时使用、如何使用”以及工具使用流程的详细说明。

## 1. 何时使用CloudBase Run（使用场景）

- **需要长时间连接功能**：WebSocket、SSE或服务器推送。
- **需要长时间运行或持续运行的进程**：这些任务不适合使用云函数或后台作业。
- **需要自定义运行时环境或系统依赖**：例如自定义镜像或特定系统库。
- **需要支持多种语言或任意框架**：如Java、Go、PHP、.NET、Python、Node.js等。
- **需要稳定且具备弹性扩展能力的外部服务**：按需付费，能够根据需求调整资源使用量。
- **需要私有或内部网络访问**：VPC/PRIVATE网络访问，或者通过小程序进行内部直接连接。
- **需要开发AI代理**：基于CloudRun的功能模式来开发个性化的AI应用程序。

## 2. 模式选择（快速对比）

- **功能模式（Function mode）**：最快上手的方式，内置HTTP/WebSocket/SSE支持，固定端口3000，工具支持本地运行。
- **容器模式（Container mode）**：支持任何语言和运行时环境，需要Dockerfile，工具不支持本地运行。

### 模式对比表

| 特征 | 功能模式 | 容器模式 |
| --- | --- | --- |
| 语言/框架 | 可使用Node.js（通过`@cloudbase/functions-framework`） | 支持任何语言和运行时环境（如Java、Go、PHP、.NET、Python、Node.js等） |
| 运行时 | 通过函数框架加载运行时代码 | 通过Docker镜像启动进程 |
| 端口 | 固定为3000 | 应用程序监听的端口由平台在部署时指定 |
| Dockerfile | 不需要 | 必须提供Dockerfile并进行本地构建 |
| 本地运行 | 支持（工具内置） | 不支持（建议使用Docker进行调试） |
| 常见场景 | 适用于WebSocket/SSE流式响应、表单/文件处理、低延迟场景，以及每个实例运行多个函数 | 适用于具有复杂系统依赖或需要迁移现有容器化应用程序的场景 |

## 3. 开发要求

- 必须监听`PORT`环境变量（容器中的实际端口）。
- 服务应该是无状态的，数据需要写入外部存储（如数据库、缓存等）。
- 请求之外不应有后台的持久线程或进程。
- 尽量减少依赖项，使用轻量级的镜像，以降低冷启动时间和部署时间。
- 遵循资源限制：内存（Mem）应为CPU容量的两倍（例如，0.25 vCPU对应0.5 GB内存）。
- 访问控制：对于Web场景，仅启用公共网络；对于小程序，建议关闭公共网络以使用内部直接连接。

## 4. 工具（简单说明及读写操作）

- **读取操作**（`queryCloudRun`）：
  - `list`：列出所有服务，可按名称或类型过滤。
  - `detail`：查看服务的当前配置、版本和访问地址。
  - `templates`：提供可用的模板。
- **写入操作**（`manageCloudRun`）：
  - `init`：创建本地项目（可选模板）。
  - `download`：将现有服务代码下载到本地。
  - `run`：在本地运行服务（仅限功能模式）。
  - `deploy`：将本地代码部署到CloudRun。
  - `delete`：删除服务（需要明确确认）。
  - `createAgent`：创建AI代理（基于CloudRun的功能模式）。
- **重要参数**：
  - `targetPath`：本地目录路径（必须是绝对路径）。
  - `serverConfig`：部署参数（如CPU、内存、实例数量、访问类型和环境变量等）。
  - `runOptions`：指定本地运行端口和临时环境变量（功能模式），支持`runMode: 'normal' | 'agent'`。
  - `agentConfig`：代理配置（如代理名称、标签、描述和模板）。
  - 删除操作时必须设置`force: true`，否则操作不会执行。

## 5. 核心工作流程（先理解步骤，再查看示例）

1. **选择模式**：
   - 如果需要支持多种语言或现有的容器化应用程序/Docker环境，选择“容器模式”。
   - 如果需要长时间连接、流式数据传输、低延迟或同时运行多个函数，优先选择“功能模式”。

2. **初始化本地项目**：
   - 通常可以使用`init`模板（功能模式和容器模式都可以从模板开始）。
   - 对于容器模式，必须“检查或生成Dockerfile”：
     - Node.js的简单示例：
       ```dockerfile
       FROM node:18-alpine
       WORKDIR /app
       COPY package*.json ./
       RUN npm ci --omit=dev
       COPY . .
       ENV NODE_ENV=production
       EXPOSE 3000
       CMD ["node","server.js"]
       ```
     - Python的简单示例：
       ```dockerfile
       FROM python:3.11-slim
       WORKDIR /app
       COPY requirements.txt ./
       RUN pip install -r requirements.txt --no-cache-dir
       COPY . .
       ENV PORT=3000
       EXPOSE 3000
       CMD ["python","app.py"]
       ```

3. **在本地运行**（仅限功能模式）：
   - 可以使用`npm run dev/start`或通过入口文件启动程序。

4. **配置访问权限**：
   - 根据需要设置`OpenAccessTypes`（WEB/VPC/PRIVATE）；为Web场景配置安全域和认证。

5. **部署**：
   - 在部署时指定CPU、内存、实例数量等参数。

6. **验证**：
   - 使用`detail`命令确认访问地址和配置是否符合预期。

### 示例工具调用

1) **查看模板和服务**：
```json
{ "name": "queryCloudRun", "arguments": { "action": "templates" } }
```
```json
{ "name": "queryCloudRun", "arguments": { "action": "detail", "detailServerName": "my-svc" } }
```

2) **初始化项目**：
```json
{ "name": "manageCloudRun", "arguments": { "action": "init", "serverName": "my-svc", "targetPath": "/abs/ws/my-svc", "template": "helloworld" } }
```

3) **下载代码**（可选）：
```json
{ "name": "manageCloudRun", "arguments": { "action": "download", "serverName": "my-svc", "targetPath": "/abs/ws/my-svc" } }
```

4) **在本地运行**（仅限功能模式）：
```json
{ "name": "manageCloudRun", "arguments": { "action": "run", "serverName": "my-svc", "targetPath": "/abs/ws/my-svc", "runOptions": { "port": 3000 } } }
```

5) **部署**：
```json
{ "name": "manageCloudRun", "arguments": { "action": "deploy", "serverName": "my-svc", "targetPath": "/abs/ws/my-svc", "serverConfig": { "OpenAccessTypes": ["WEB"], "Cpu": 0.5, "Mem": 1, "MinNum": 0, "MaxNum": 5 } } }
```

6) **创建AI代理**（可选）：
```json
{ "name": "manageCloudRun", "arguments": { "action": "createAgent", "serverName": "my-agent", "targetPath": "/abs/ws/agents", "agentConfig": { "agentName": "MyAgent", "botTag": "demo", "description": "My agent", "template": "blank" } } }
```

7) **运行代理**（可选）：
```json
{ "name": "manageCloudRun", "arguments": { "action": "run", "serverName": "my-agent", "targetPath": "/abs/ws/agents/my-agent", "runOptions": { "port": 3000, "runMode": "agent" } } }
```

## 6. 最佳实践（强烈推荐）

- 尽量使用私有网络（VPC）或小程序的`callContainer`方式，减少公共网络的暴露风险。
- Web应用程序必须使用CloudBase Web SDK进行认证；小程序应通过平台进行认证。
- 通过环境变量管理敏感信息；为开发/测试/生产环境分别配置设置。
- 在部署前后使用`queryCloudRun.detail`验证配置和访问权限。
- 使用可重用的镜像层，保持镜像体积小；监控应用程序的启动延迟和内存使用情况。
- 在开发AI代理时，使用`@cloudbase/aiagent-framework`，该框架支持SSE流式响应，BotId格式为`ibot-{name}-{tag}`。

## 7. 快速故障排除**

- **访问失败**：检查`OpenAccessTypes`、域名和端口设置，以及实例是否已降级到0资源使用量。
- **部署失败**：检查Dockerfile的构建日志、镜像大小以及CPU和内存的使用情况。
- **本地运行失败**：仅功能模式支持本地运行；需要`package.json`中的`dev`/`start`脚本或`index.js`/`app.js`/`server.js`文件。
- **性能问题**：减少依赖项和初始化时间；适当增加`MinNum`参数以优化冷启动性能。
- **代理运行失败**：检查`@cloudbase/aiagent-framework`的依赖项以及BotId的格式。

## 8. 功能模式CloudRun（功能模式）的关键点

- **定义**：CloudRun结合函数框架（`@cloudbase/functions-framework`）和函数代码，使容器服务开发变得像编写云函数一样简单。
- **适用场景**：需要WebSocket、SSE、文件上传、流式响应；需要长时间运行的任务或与数据库/消息队列交互；需要每个实例运行多个函数并共享内存，以及需要更好的日志记录和调试功能。
- **代理模式**：基于功能模式开发AI代理，使用`@cloudbase/aiagent-framework`，支持SSE流式响应和个性化AI应用程序。
- **工具支持**：仅功能模式支持本地运行（通过`manageCloudRun`和`run`命令进行操作）；部署通过`manageCloudRun`完成；查询通过`queryCloudRun`实现。
- **迁移建议**：由于与云函数的调用链和运行时环境不同，迁移时可能需要稍作修改（包括客户端调用方式）。
- **可移植性**：基于函数框架，可以在本地、主机或Docker环境中运行；非CloudRun环境需要自行管理构建和部署过程。

## 9. 服务调用方法（示例）

### 当启用公共Web网络时的HTTP直接访问：
```bash
curl -L "https://<your-service-domain>"
```

### 微信小程序（推荐使用内部直接连接，关闭公共网络）：
```js
// app.js (ensure wx.cloud.init() is called)
const res = await wx.cloud.callContainer({
  config: { env: "<envId>" },
  path: "/",
  method: "GET",
  header: { "X-WX-SERVICE": "<serviceName>" }
});
```

### Web应用（需要配置安全域和认证）：
```js
import cloudbase from "@cloudbase/js-sdk";

const app = cloudbase.init({ env: "<envId>" });  // Collect user's phone number into variable `phoneNum` by providing a input UI

const auth = app.auth();

// Send SMS code
const verificationInfo = await auth.getVerification({
  phone_number: `+86 ${phoneNum}`,
});

// Collect user's phone number into variable `verificationCode` by providing a input UI 

// Sign in
await auth.signInWithSms({
  verificationInfo,
  verificationCode,
  phoneNum,
});

const res = await app.callContainer({
  name: "<serviceName>", method: "POST", path: "/api",
  header: { "Content-Type": "application/json" },
  data: { key: "value" }
});
```

// Web JS SDK初始化必须同步进行：
// - 始终使用`import cloudbase from "@cloudbase/js-sdk";`
// - 不要使用动态导入语句（如`import "@cloudbase/js-sdk")`，也不要使用`initCloudBase()`等异步包装器。

### Node.js（服务器端/云函数内部调用）：
```js
import tcb from "@cloudbase/node-sdk";
const app = tcb.init({});
const res = await app.callContainer({
  name: "<serviceName>", method: "GET", path: "/health",
  timeout: 5000
});
```

### 建议**

- 小程序/服务器端应优先使用内部网络（VPC/PRIVATE）进行调用，以减少暴露风险。
- Web应用需要启用公共网络、配置安全域，并使用SDK进行认证。