---
name: kubeblocks
version: "0.2.0"
description: 使用 KubeBlocks 在 Kubernetes 上配置和管理生产级数据库。当用户需要数据库（如 MySQL、PostgreSQL、Redis、MongoDB、Kafka、Elasticsearch、Milvus、Qdrant、RabbitMQ 或其他数据基础设施），并且已经拥有或愿意搭建 Kubernetes 环境时，可以使用此技能。相关请求包括：“我需要一个数据库”、“设置 MySQL”、“部署用于 RAG 的向量数据库”、“我需要一个消息队列”，以及其他涉及数据库配置、扩展、备份、恢复、监控或故障排除的操作。此外，在用户明确提及 KubeBlocks 或希望管理由 KubeBlocks 管理的数据库集群时，也应使用此技能。
compatibility:
  required_tools:
    - kubectl
    - helm
  optional_tools:
    - npx
  notes: Requires access to a Kubernetes cluster (kubeconfig). For local development, the skill can create a cluster using Kind, Minikube, or k3d.
---
# KubeBlocks — 在 Kubernetes 上简化数据库管理

## 适用场景

当用户需要使用数据库，并且已经拥有（或愿意搭建）Kubernetes 环境时；当用户请求在 Kubernetes 上“设置”、“创建”、“部署”或“配置”数据库时；当用户在部署或操作过程中提到特定的数据库引擎（如 MySQL、PostgreSQL、Redis、MongoDB、Kafka、Elasticsearch、Milvus、Qdrant、RabbitMQ 等）时；当用户需要对 Kubernetes 上的数据库进行操作（如扩展、备份、恢复、监控、故障转移、参数调整等）时；当用户正在排查由 KubeBlocks 管理的数据库问题时；或者当用户直接提及 KubeBlocks 时，都可以使用此技能。

**不适用场景**：如果用户仅需要现有数据库服务的连接字符串（例如 AWS RDS、Google Cloud SQL），或者希望通过 Docker Compose 直接运行数据库而不使用 Kubernetes，则不适用此技能。如果用户还没有 Kubernetes 集群但希望搭建一个，本技能集也包含了创建本地 Kubernetes 集群以供开发和测试的步骤。

## 什么是 KubeBlocks？

KubeBlocks 是一个 Kubernetes 运算符，可以在任何 Kubernetes 集群上管理 30 多种数据库引擎。它提供了一个统一的 API，覆盖了从数据库的配置和扩展到备份、恢复以及监控等全生命周期的管理流程，支持关系型、NoSQL、流式、向量和图型数据库。

- 官方文档：https://kubeblocks.io/docs/preview/user_docs/overview/introduction  
- 完整的 LLM 文档索引：https://kubeblocks.io/llms-full.txt  
- GitHub 仓库：https://github.com/apecloud/kubeblocks  

## 快速状态检查

在执行任何操作之前，请先验证当前的状态：

```bash
# Check if KubeBlocks is installed
kubectl -n kb-system get pods

# List all database clusters across namespaces
kubectl get cluster -A

# Check KubeBlocks version
helm list -n kb-system | grep kubeblocks
```

如果尚未安装 KubeBlocks，请先执行 [install-kubeblocks](skills/kubeblocks-install/SKILL.md) 操作。如果完全没有 Kubernetes 集群，请先执行 [create-local-k8s-cluster](skills/kubeblocks-create-local-k8s-cluster/SKILL.md) 操作。

## 技能目录

根据用户的实际需求选择相应的技能。每个技能都包含详细的操作指南、YAML 模板、步骤流程以及故障排除方法。

### 入门

| 用户需求 | 对应技能 |
|---|---|
| 创建本地 Kubernetes 测试集群 | [create-local-k8s-cluster](skills/kubeblocks-create-local-k8s-cluster/SKILL.md) |
| 安装 KubeBlocks 运算符 | [install-kubeblocks](skills/kubeblocks-install/SKILL.md) |
| 安装/管理数据库引擎插件 | [manage-addons](skills/kubeblocks-manage-addons/SKILL.md) |

### 创建数据库

| 用户需求 | 对应技能 |
|---|---|
| 创建 MySQL 集群 | [addon-mysql](skills/kubeblocks-addon-mysql/SKILL.md) |
| 创建 PostgreSQL 集群 | [addon-postgresql](skills/kubeblocks-addon-postgresql/SKILL.md) |
| 创建 Redis 集群 | [addon-redis](skills/kubeblocks-addon-redis/SKILL.md) |
| 创建 MongoDB 集群 | [addon-mongodb](skills/kubeblocks-addon-mongodb/SKILL.md) |
| 创建 Kafka 集群 | [addon-kafka](skills/kubeblocks-addon-kafka/SKILL.md) |
| 创建 Elasticsearch 集群 | [addon-elasticsearch](skills/kubeblocks-addon-elasticsearch/SKILL.md) |
| 创建 Milvus（向量数据库）集群 | [addon-milvus](skills/kubeblocks-addon-milvus/SKILL.md) |
| 创建 Qdrant（向量数据库）集群 | [addon-qdrant](skills/kubeblocks-addon-qdrant/SKILL.md) |
| 创建 RabbitMQ 集群 | [addon-rabbitmq](skills/kubeblocks-addon-rabbitmq/SKILL.md) |
| 创建其他类型的数据库 | [create-cluster](skills/kubeblocks-create-cluster/SKILL.md) |
| 删除数据库集群 | [delete-cluster](skills/kubeblocks-delete-cluster/SKILL.md) |

### 日常操作

| 用户需求 | 对应技能 |
|---|---|
| 停止/启动/重启集群 | [cluster-lifecycle](skills/kubeblocks-cluster-lifecycle/SKILL.md) |
| 横向扩展集群资源（CPU/内存） | [vertical-scaling](skills/kubeblocks-vertical-scaling/SKILL.md) |
| 增加/减少副本或分片 | [horizontal-scaling](skills/kubeblocks-horizontal-scaling/SKILL.md) |
| 扩展存储空间 | [volume-expansion](skills/kubeblocks-volume-expansion/SKILL.md) |
| 修改数据库参数 | [reconfigure-parameters](skills/kubeblocks-reconfigure-parameters/SKILL.md) |
| 切换主从节点 | [switchover](skills/kubeblocks-switchover/SKILL.md) |
| 升级数据库引擎版本 | [minor-version-upgrade](skills/kubeblocks-minor-version-upgrade/SKILL.md) |
| 重建故障副本 | [rebuild-replica](skills/kubeblocks-rebuild-replica/SKILL.md) |
| 升级 KubeBlocks 运算符 | [upgrade-kubeblocks](skills/kubeblocks-upgrade/SKILL.md) |

### 数据保护

| 用户需求 | 对应技能 |
|---|---|
| 备份集群数据 | [backup](skills/kubeblocks-backup/SKILL.md) |
| 从备份中恢复数据 | [restore](skills/kubeblocks-restore/SKILL.md) |

### 安全与网络配置

| 用户需求 | 对应技能 |
|---|---|
| 管理数据库密码/账户 | [manage-accounts](skills/kubeblocks-manage-accounts/SKILL.md) |
| 配置 TLS/mTLS 加密 | [configure-tls](skills/kubeblocks-configure-tls/SKILL.md) |
| 外部访问服务（使用 LoadBalancer/NodePort） | [expose-service](skills/kubeblocks-expose-service/SKILL.md) |

### 监控与可见性

| 用户需求 | 对应技能 |
|---|---|
| 设置监控系统（Prometheus/Grafana） | [setup-monitoring](skills/kubeblocks-setup-monitoring/SKILL.md) |

### 故障排除

| 用户需求 | 对应技能 |
|---|---|
| 集群无法正常运行、出现错误、卡顿或死循环 | [troubleshoot](skills/kubeblocks-troubleshoot/SKILL.md) |

## 决策流程

当需要进一步明确用户的操作意图时，请参考以下流程：

```
User needs a database
├─ Is KubeBlocks installed?
│  ├─ No  → Do they have a K8s cluster?
│  │        ├─ No  → create-local-k8s-cluster → install-kubeblocks
│  │        └─ Yes → install-kubeblocks
│  └─ Yes → Continue below
│
├─ Create a database
│  ├─ Is the engine addon installed?
│  │  ├─ No  → manage-addons → then create cluster
│  │  └─ Yes → Which engine?
│  │           ├─ MySQL/PG/Redis/MongoDB/Kafka/ES/Milvus/Qdrant/RabbitMQ → addon-{engine}
│  │           └─ Other → create-cluster (generic)
│  └─ Don't know which engine? → Recommend based on use case:
│     ├─ Relational / SQL         → addon-postgresql or addon-mysql
│     ├─ Cache / session store    → addon-redis
│     ├─ Document store           → addon-mongodb
│     ├─ Event streaming          → addon-kafka
│     ├─ Full-text search / logs  → addon-elasticsearch
│     ├─ Vector similarity / RAG  → addon-milvus or addon-qdrant
│     └─ Message queue            → addon-rabbitmq or addon-kafka
│
├─ Operate an existing database
│  ├─ Scale CPU/Memory      → vertical-scaling
│  ├─ Add/remove replicas   → horizontal-scaling
│  ├─ Expand disk            → volume-expansion
│  ├─ Change DB config       → reconfigure-parameters
│  ├─ Switchover primary     → switchover
│  ├─ Upgrade DB version     → minor-version-upgrade
│  ├─ Rebuild failed replica → rebuild-replica
│  ├─ Stop / Start / Restart → cluster-lifecycle
│  └─ Delete permanently     → delete-cluster
│
├─ Protect data
│  ├─ Backup                 → backup
│  └─ Restore / PITR         → restore
│
├─ Secure the database
│  ├─ Manage passwords       → manage-accounts
│  ├─ Enable TLS/SSL         → configure-tls
│  └─ Expose externally      → expose-service
│
├─ Monitor                   → setup-monitoring
├─ Upgrade KubeBlocks itself → upgrade-kubeblocks
└─ Something is broken       → troubleshoot
```

## 数据库引擎推荐指南

当用户需要使用数据库但尚未选择具体引擎时，可以根据其使用场景进行推荐：

| 使用场景 | 推荐引擎 | 原因 |
|---|---|---|
| Web 应用后端、关系型数据、SQL | PostgreSQL | 最通用，生态系统完善 |
| 与旧版本应用程序兼容、支持 MySQL 协议 | MySQL | 适用于依赖 MySQL 的应用程序 |
| 缓存、会话管理、速率限制 | Redis | 响应时间极短，API 简单 |
| 数据结构灵活、适合文档存储 | MongoDB | 无固定结构，支持水平扩展 |
| 事件流处理、日志分析 | Kafka | 高吞吐量，数据持久有序 |
| 全文搜索、日志分析 | Elasticsearch | 倒排索引，强大的查询语言 |
| 人工智能嵌入、相似性搜索 | Milvus 或 Qdrant | 专为向量数据设计的索引 |
| 任务队列、发布/订阅消息 | RabbitMQ | 路由灵活，支持多种协议 |

## 术语解释

### “扩展”相关术语的区分

| 用户表达 | 对应操作 |
|-----------|-------|
| “scale up”/“more CPU”/“more memory”/“resize” | 横向扩展（增加资源） |
| “add replicas”/“more nodes”/“scale out”/“add shards” | 横向扩展（增加副本/节点） |
| “more disk”/“more storage”/“expand volume” | 扩展存储空间 |

### “删除”与“停止”的区别

| 用户表达 | 对应操作 |
|-----------|-------|
| “delete”/“remove”/“destroy”/“drop”（永久删除） | [delete-cluster](技能) |
| “stop”/“pause”/“shut down”（暂时停止，数据保留） | [cluster-lifecycle](技能) |

### “升级”相关术语的区分

| 用户表达 | 对应操作 |
|-----------|-------|
| “upgrade MySQL/PG version”/“patch database” | [minor-version-upgrade](技能) | 升级数据库版本 |
| “upgrade KubeBlocks”/“update operator” | [upgrade-kubeblocks](技能) | 升级 KubeBlocks 运算符 |

## 安全最佳实践

在执行任何修改集群的操作之前，请务必参考 [安全最佳实践](references/safety-patterns.md)：
- **先进行模拟测试**：在任何实际操作前，务必使用 `kubectl apply --dry-run=server` 进行模拟测试。
- **确认后再执行破坏性操作**：删除、扩展、停止或更改终止策略等操作需要用户明确确认，并列出所有受影响的资源和备份方案。
- **处理敏感信息**：某些命令（如 `kubectl get secret ... -o jsonpath`）会暴露数据库密码。仅在用户明确要求时执行这些命令，并提醒输出内容包含敏感信息。
- **谨慎使用生产环境命令**：使用 `kubectl exec` 进入数据库 Pod 会直接访问生产数据，请在执行前务必获得用户确认。
- **特殊操作需谨慎**：对于设置了 `terminationPolicy: DoNotTerminate` 的集群，应格外小心。建议在进行高风险操作（如升级、切换或配置调整）前先进行数据备份。

## 常用调试命令

```bash
kubectl describe cluster <cluster-name> -n <namespace>
kubectl get opsrequest -n <namespace>
kubectl get component -n <namespace>
kubectl logs -n <namespace> <pod-name> -c <container-name>
kubectl -n kb-system logs -l app.kubernetes.io/name=kubeblocks --tail=100
```

## 文档链接

| 资源 | 链接 |
|---|---|
| 产品简介 | https://kubeblocks.io/docs/preview/user_docs/overview/introduction |
| 支持的插件 | https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons |
| 完整的 LLM 文档索引 | https://kubeblocks.io/llms-full.txt |
| GitHub 仓库 | https://github.com/apecloud/kubeblocks |
| 版本更新记录 | https://github.com/apecloud/kubeblocks/releases |