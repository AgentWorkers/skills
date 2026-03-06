---
name: MinIO S3 (Object Storage)
slug: minio
version: 1.0.0
homepage: https://clawic.com/skills/minio
description: 使用 mc 工作流、策略控制、复制机制以及具备事故应对能力的运行手册（runbooks）来部署、保护并管理 MinIO 对象存储服务。
changelog: Initial release with MinIO deployment, policy, replication, and recovery playbooks for object storage operations.
metadata: {"clawdbot":{"emoji":"🗂️","requires":{"bins":["mc","curl","openssl"]},"os":["linux","darwin","win32"],"configPaths":["~/minio/"]}}
---
## 设置（Setup）

首次使用时，请阅读 `setup.md` 文件，以了解激活边界、环境默认值以及在对存储桶、策略或复制设置进行修改之前的确认规则。

## 使用场景（When to Use）

当用户需要部署 MinIO、执行存储桶生命周期操作、配置访问策略、规划对象保留策略或处理故障恢复时，请使用此技能。

该技能适用于单节点实验室环境、分布式生产集群、兼容 S3 的迁移任务，以及在数据持久性和访问正确性至关重要的操作故障排查场景中。

## 架构（Architecture）

MinIO 的相关配置文件存储在 `~/minio/` 目录下。具体结构及状态信息请参考 `memory-template.md` 文件。

```text
~/minio/
|-- memory.md              # Activation preferences and approval model
|-- environments.md        # Endpoint map, topology, and region notes
|-- buckets.md             # Bucket inventory, versioning, lifecycle, lock mode
|-- identities.md          # Users, groups, policies, and credential rotation state
`-- incidents.md           # Outages, corruption events, and validated recovery steps
```

## 快速参考（Quick Reference）

根据当前任务的需求，仅使用所需的文件。

| 主题 | 文件名           |
|-------|-----------------|
| 设置与激活行为 | setup.md           |
| 内存结构与状态模型 | memory-template.md       |
| 部署与拓扑选择 | deployment-patterns.md     |
| 存储桶、IAM 与操作流程 | mc-operations.md       |
| 安全加固、备份与灾难恢复 | hardening-dr.md        |

## 核心规则（Core Rules）

### 1. 在执行任何命令前先确定系统架构
- 在制定计划之前，明确系统是单节点架构、分布式架构还是租户模式。
- 验证端点、区域和存储布局，确保命令针对正确的环境执行。

### 2. 执行写操作前需获得明确确认
- 删除存储桶、修改对象生命周期规则、更换策略或调整复制设置等操作均需用户明确确认。
- 在执行修改操作前，确认操作范围、预期影响及回滚方案。

### 3. 采用“先读取后写入”的操作流程
- 在执行写操作（如 `mc admin info`、`mc ls`、`mc policy ls`）之前，先执行读取操作。
- 保存命令执行结果，以便在操作后对比预期状态与实际状态。

### 4. 实施最小权限原则
- 默认使用基于存储桶和前缀的权限控制，避免使用宽泛的访问权限。
- 每次进行涉及安全性的更改后，更新访问密钥并验证策略绑定。

### 5. 在维护期间保护数据持久性功能
- 在进行重大更新前，检查数据版本控制、对象锁定机制、保留策略及复制状态。
- 除非有书面确认，否则切勿禁用数据持久性相关功能。

### 6. 通过 API 行为验证操作结果
- 除了依赖命令返回的退出码外，还需通过独立检查（如对象列表、对象写入测试、策略模拟等）来确认操作是否成功。
- 如果数据路径和授权路径均通过验证，才视为操作成功。

### 7. 记录操作上下文以供后续参考
- 更新 `~/minio/` 目录中的配置信息，包括环境限制、安全默认设置及故障处理经验。
- 仅保留可复用的操作上下文，切勿存储敏感信息或原始凭据。

## 常见错误（Common Traps）

- 将 MinIO 当作普通的 S3 服务使用（未检查部署模式）→ 在分布式环境中命令可能正常执行，但行为会出错。
- 在未读取现有策略绑定的情况下直接替换策略 → 可能导致权限滥用或系统锁定。
- 在未验证数据版本控制和时间同步的情况下启用复制功能 → 会导致复制数据不一致或冲突。
- 在未进行测试的情况下执行对象生命周期操作 → 可能导致数据丢失。
- 跳过操作前的数据备份 → 在系统故障时无法可靠地恢复数据。
- 仅依赖端点是否可达来判断 TLS 连接是否有效 → 由于信任链问题，客户端可能无法正常通信。

## 外部端点（External Endpoints）

| 端点          | 发送的数据        | 功能                |
|-----------------|------------------|----------------------|
| https://<minio-endpoint>    | S3 API 请求（对象和元数据操作） | 对用户管理的 MinIO 进行对象和桶操作       |
| https://<minio-endpoint>/minio/admin | 管理 API （集群管理和身份验证） | 集群状态监控、IAM 配置及操作控制       |
| https://min.io/docs     | 文档查询           | 命令行为和配置详情           |

**注意：** 无其他数据会被发送到外部。

## 安全性与隐私（Security & Privacy）

**离开您机器的数据：**
- 发往用户管理的 MinIO 端点的请求（用于对象、存储桶和 IAM 操作的数据）。
- 从官方 MinIO 文档中获取的可选文档内容。

**留在本地的数据：**
- 存储在 `~/minio/` 目录中的操作上下文信息。
- 操作计划记录、故障日志及经过审批的操作脚本。

**注意事项：**
- 该技能不会执行未指定的端点请求。
- 不会在内存文件中存储原始凭据。
- 未经明确确认，不会批准任何可能破坏系统或更改权限的操作。
- 不会自动修改 `SKILL.md` 或相关辅助文件。

## 信任机制（Trust）

在执行已批准的操作时，该技能会向 MinIO 端点及可选的文档服务发送数据。
**仅当您信任已配置的 MinIO 基础设施及其凭证处理机制时，才建议安装该技能。**

## 相关技能（Related Skills）
- 使用 `clawhub install <slug>` 安装相关工具：
  - `s3`：跨多种存储提供商的 S3 兼容对象存储解决方案。
  - `cloud-storage`：适用于混合云和本地环境的存储架构方案。
  - `backups`：备份验证及优先恢复的操作流程。
  - `infrastructure`：基础设施规划及生产操作基准。
  - `docker`：容器化部署及服务生命周期管理工具。

## 反馈建议（Feedback）
- 如该技能对您有帮助，请给予好评（例如：`clawhub star minio`）。
- 为保持信息更新，请定期执行 `clawhub sync` 命令。