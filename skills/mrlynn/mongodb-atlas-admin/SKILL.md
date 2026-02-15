---
name: mongodb-atlas-admin
description: "通过 Atlas Admin API v2 管理 MongoDB Atlas 集群、项目、用户、备份和警报。适用场景包括：  
(1) 创建、扩展或删除 Atlas 集群；  
(2) 管理数据库用户和 IP 访问列表；  
(3) 配置备份、快照和恢复任务；  
(4) 设置警报并进行监控；  
(5) 管理项目和组织；  
(6) 查看集群指标和日志。  
使用此功能需要 Atlas API 密钥（公共/私有）或服务账户凭证。"
metadata: {"clawdbot":{"emoji":"🍃","requires":{"bins":["curl","jq"]},"author":{"name":"Michael Lynn","github":"mrlynn","website":"https://mlynn.org","linkedin":"https://linkedin.com/in/mlynn"}}}
---

# MongoDB Atlas 管理

通过 Atlas 管理 API v2 以编程方式管理 MongoDB Atlas 基础设施。

## 认证

Atlas API 支持使用 API 密钥的 HTTP Digest 认证，或使用服务账户的 OAuth2 认证。

### API 密钥（较旧但更简单）

```bash
# Set credentials
export ATLAS_PUBLIC_KEY="your-public-key"
export ATLAS_PRIVATE_KEY="your-private-key"

# All requests use digest auth
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" \
  --digest \
  --header "Accept: application/vnd.atlas.2025-03-12+json" \
  --header "Content-Type: application/json" \
  "https://cloud.mongodb.com/api/atlas/v2/..."
```

### 服务账户（推荐使用 OAuth2）

```bash
# Get access token
TOKEN=$(curl -s --request POST \
  "https://cloud.mongodb.com/api/oauth/token" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --data "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}" \
  | jq -r '.access_token')

# Use token (valid 1 hour)
curl --header "Authorization: Bearer ${TOKEN}" \
  --header "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/..."
```

## 快速参考

| 任务 | 端点 | 方法 |
|------|----------|--------|
| 列出项目 | `/groups` | GET |
| 创建项目 | `/groups` | POST |
| 列出集群 | `/groups/{groupId}/clusters` | GET |
| 创建集群 | `/groups/{groupId}/clusters` | POST |
| 获取集群信息 | `/groups/{groupId}/clusters/{clusterName}` | GET |
| 更新集群 | `/groups/{groupId}/clusters/{clusterName}` | PATCH |
| 删除集群 | `/groups/{groupId}/clusters/{clusterName}` | DELETE |
| 列出数据库用户 | `/groups/{groupId}/databaseUsers` | GET |
| 创建数据库用户 | `/groups/{groupId}/databaseUsers` | POST |
| 列出 IP 访问权限 | `/groups/{groupId}/accessList` | GET |
| 添加 IP 访问权限 | `/groups/{groupId}/accessList` | POST |

---

## 集群

### 列出项目中的所有集群

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters"
```

### 获取集群详细信息

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters/${CLUSTER_NAME}"
```

### 创建集群（M10+ 版本）

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X POST "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters" \
  -d '{
    "name": "my-cluster",
    "clusterType": "REPLICASET",
    "replicationSpecs": [{
      "regionConfigs": [{
        "providerName": "AWS",
        "regionName": "US_EAST_1",
        "priority": 7,
        "electableSpecs": {
          "instanceSize": "M10",
          "nodeCount": 3
        }
      }]
    }]
  }'
```

### 创建免费 tier 集群（M0 版本）

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X POST "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters" \
  -d '{
    "name": "free-cluster",
    "clusterType": "REPLICASET",
    "replicationSpecs": [{
      "regionConfigs": [{
        "providerName": "TENANT",
        "backingProviderName": "AWS",
        "regionName": "US_EAST_1",
        "priority": 7,
        "electableSpecs": {
          "instanceSize": "M0",
          "nodeCount": 3
        }
      }]
    }]
  }'
```

### 调整集群规模（更改实例大小）

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X PATCH "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters/${CLUSTER_NAME}" \
  -d '{
    "replicationSpecs": [{
      "regionConfigs": [{
        "providerName": "AWS",
        "regionName": "US_EAST_1",
        "priority": 7,
        "electableSpecs": {
          "instanceSize": "M20",
          "nodeCount": 3
        }
      }]
    }]
  }'
```

### 删除集群

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -X DELETE "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters/${CLUSTER_NAME}"
```

### 暂停/恢复集群运行

```bash
# Pause (M10+ only)
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X PATCH "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters/${CLUSTER_NAME}" \
  -d '{"paused": true}'

# Resume
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X PATCH "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters/${CLUSTER_NAME}" \
  -d '{"paused": false}'
```

---

## 项目（组）

### 列出所有项目

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups"
```

### 创建项目

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X POST "https://cloud.mongodb.com/api/atlas/v2/groups" \
  -d '{
    "name": "my-project",
    "orgId": "YOUR_ORG_ID"
  }'
```

### 删除项目

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -X DELETE "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}"
```

---

## 数据库用户

### 列出数据库用户

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/databaseUsers"
```

### 创建数据库用户

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X POST "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/databaseUsers" \
  -d '{
    "databaseName": "admin",
    "username": "myuser",
    "password": "securePassword123!",
    "roles": [{
      "databaseName": "admin",
      "roleName": "readWriteAnyDatabase"
    }]
  }'
```

### 删除数据库用户

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -X DELETE "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/databaseUsers/admin/${USERNAME}"
```

---

## IP 访问权限

### 列出 IP 访问记录

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/accessList"
```

### 添加 IP 地址

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X POST "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/accessList" \
  -d '[{
    "ipAddress": "192.168.1.1",
    "comment": "Office IP"
  }]'
```

### 允许所有 IP 访问（仅限开发用途！）

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X POST "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/accessList" \
  -d '[{
    "cidrBlock": "0.0.0.0/0",
    "comment": "Allow all - DEV ONLY"
  }]'
```

---

## 备份与快照

### 列出快照

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters/${CLUSTER_NAME}/backup/snapshots"
```

### 按需创建快照

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X POST "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters/${CLUSTER_NAME}/backup/snapshots" \
  -d '{
    "description": "Pre-deployment snapshot",
    "retentionInDays": 7
  }'
```

### 从快照中恢复数据

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  -H "Content-Type: application/json" \
  -X POST "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/clusters/${CLUSTER_NAME}/backup/restoreJobs" \
  -d '{
    "snapshotId": "SNAPSHOT_ID",
    "deliveryType": "automated",
    "targetClusterName": "restored-cluster",
    "targetGroupId": "${GROUP_ID}"
  }'
```

---

## 警报

### 列出警报配置

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/alertConfigs"
```

### 获取当前激活的警报

```bash
curl --user "${ATLAS_PUBLIC_KEY}:${ATLAS_PRIVATE_KEY}" --digest \
  -H "Accept: application/vnd.atlas.2025-03-12+json" \
  "https://cloud.mongodb.com/api/atlas/v2/groups/${GROUP_ID}/alerts?status=OPEN"
```

---

## 实例规格

| 规格等级 | vCPUs | RAM | 存储空间 | 适用场景 |
|------|-------|-----|---------|----------|
| M0 | 共享资源 | 共享资源 | 512 MB | 免费 tier，开发/学习用途 |
| M2 | 共享资源 | 共享资源 | 2 GB | 小型开发项目 |
| M5 | 共享资源 | 共享资源 | 5 GB | 大型开发项目 |
| M10 | 2 个 vCPU | 2 GB | 10 GB | 开发/测试环境，低流量 |
| M20 | 2 个 vCPU | 4 GB | 轻量级生产环境 |
| M30 | 2 个 vCPU | 8 GB | 40 GB | 生产环境 |
| M40 | 4 个 vCPU | 16 GB | 80 GB | 高流量生产环境 |
| M50 | 8 个 vCPU | 32 GB | 160 GB | 大型生产环境 |
| M60+ | 16 个以上 vCPU | 64 GB 以上 | 企业级环境 |

---

## 辅助脚本

为方便使用，可参考 `scripts/atlas.sh` 脚本：

```bash
# Usage
./scripts/atlas.sh <command> [args]

# Examples
./scripts/atlas.sh projects list
./scripts/atlas.sh clusters list <project-id>
./scripts/atlas.sh clusters create <project-id> <name> <size> <region>
./scripts/atlas.sh clusters delete <project-id> <name>
./scripts/atlas.sh clusters pause <project-id> <name>
./scripts/atlas.sh users list <project-id>
./scripts/atlas.sh users create <project-id> <username> <password>
```

---

## 环境变量

```bash
# Required
export ATLAS_PUBLIC_KEY="..."
export ATLAS_PRIVATE_KEY="..."

# Optional (for service accounts)
export ATLAS_CLIENT_ID="..."
export ATLAS_CLIENT_SECRET="..."

# Common IDs
export ATLAS_ORG_ID="..."      # Organization ID
export ATLAS_GROUP_ID="..."    # Project/Group ID
```

---

## API 参考

- **基础 URL:** `https://cloud.mongodb.com/api/atlas/v2`
- **请求头:** `application/vnd.atlas.2025-03-12+json`
- **完整文档:** https://www.mongodb.com/docs/atlas/reference/api-resources-spec/v2/
- **OpenAPI 规范:** https://github.com/mongodb/atlas-sdk-go/blob/main/openapi/atlas-api.yaml

有关端点的详细文档，请参阅 `references/api-endpoints.md`。

---

## 作者

**Michael Lynn** — MongoDB 的首席开发顾问

- 🌐 网站: [mlynn.org](https://mlynn.org)
- 🐙 GitHub: [@mrlynn](https://github.com/mrlynn)
- 💼 LinkedIn: [linkedin.com/in/mlynn](https://linkedin.com/in/mlynn)

欢迎在 GitHub 上提出问题或贡献代码！