---
name: mongodb-atlas
description: 浏览 MongoDB Atlas 管理 API 的详细规范，并在提供凭据的情况下执行相关操作。
homepage: https://www.mongodb.com/docs/api/doc/atlas-admin-api-v2/
metadata: {"clawdbot":{"emoji":"🍃","requires":{"bins":["node"],"env":["ATLAS_CLIENT_ID","ATLAS_CLIENT_SECRET"]},"primaryEnv":""}}
---

# MongoDB Atlas 管理 API

这是一个用于浏览 MongoDB Atlas 的 OpenAPI 规范的工具。
**注意：** 如果在环境中配置了 `ATLAS_CLIENT_ID` 和 `ATLAS_CLIENT_SECRET`，该工具还可以执行实际的 API 调用。如果没有这些凭据，它将仅作为只读的文档浏览器使用。

## 命令

### 1. 列出 API 目录
列出所有可用的 API 类别，或根据关键词进行过滤。

```bash
node {baseDir}/scripts/atlas-api.mjs catalog # list all categories
node {baseDir}/scripts/atlas-api.mjs catalog Clusters
```

### 2. 获取 API 详情
获取特定操作 ID 的完整端点定义（方法、路径、参数）。

```bash
node {baseDir}/scripts/atlas-api.mjs detail listClusterDetails
```

### 3. 获取数据模型定义
获取复杂类型的数据模型架构。

```bash
node {baseDir}/scripts/atlas-api.mjs schema "#/components/schemas/ApiError"
```

### 4. 执行实时 API 调用
对 Atlas API 发起实际的 HTTP 请求。

**脚本示例：** `node {baseDir}/scripts/atlas-call.mjs <METHOD> <ENDPOINT> [flags]`

#### ⚠️ 强制性安全协议
**对于任何会改变状态的操作（POST、PUT、PATCH、DELETE）：**
1. **停止并审核**：切勿立即执行该命令。
2. **预览**：首先使用 `--dry-run` 来验证请求数据内容和端点。
3. **确认**：向用户显示完整的命令和 JSON 请求体。
4. **执行**：只有在获得用户的明确批准后，才能使用 `--yes` 来执行该命令。

#### 使用示例

**1. 只读（安全模式）**

```bash
node {baseDir}/scripts/atlas-call.mjs GET groups/{groupId}/clusters
```

**2. 创建/修改（风险较高 - 需要批准）**

```bash
node {baseDir}/scripts/atlas-call.mjs POST groups/{groupId}/clusters \
  --data '{"name":"DemoCluster", "providerSettings":{...}}' \
  --dry-run
```

#### 选项
* `-d, --data <json>`：请求体字符串（请确保正确进行 JSON 转义）。
* `-p, --params <json>`：查询参数。
* `--dry-run`：打印请求详情但不执行（建议用于验证）。
* `--yes`：跳过交互式确认（请谨慎使用）。

#### 环境要求
需要设置 `ATLAS_CLIENT_ID` 和 `ATLAS_CLIENT_SECRET`。

## 核心类别
（使用 `catalog` 命令可查看 50 多个类别的完整列表）

* **集群** / **云备份**
* **项目** / **组织**
* **数据库用户** / **自定义数据库角色**
* **警报** / **警报配置**
* **监控和日志** / **事件**
* **网络对等** / **私有端点服务**
* **无服务器实例**
* **访问跟踪** / **审计**