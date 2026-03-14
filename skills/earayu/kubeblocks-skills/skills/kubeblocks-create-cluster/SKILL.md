---
name: kubeblocks-create-cluster
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上使用通用的 `Cluster CR` 模板创建数据库集群。该模板支持所有类型的插件（MySQL、PostgreSQL、Redis、MongoDB、Kafka、Elasticsearch、Milvus、Qdrant 等），并可配置多种拓扑结构。适用于用户需要部署、创建或管理新的数据库集群的场景——尤其是对于那些没有专门插件功能的系统。对于 MySQL、PostgreSQL、Redis、MongoDB 或 Kafka，建议使用相应的插件（`kubeblocks-addon-mysql`、`kubeblocks-addon-postgresql`、`kubeblocks-addon-redis`、`kubeblocks-addon-mongodb`、`kubeblocks-addon-kafka`），这些插件会提供具体的拓扑配置建议和优化的默认设置。请注意：此模板不适用于现有数据库集群的管理（请参阅第二天的操作指南）。
---
# 在 KubeBlocks 上创建数据库集群

## 概述

KubeBlocks 使用 `Cluster` CR（自定义资源）来声明性地创建和管理数据库集群。一个 YAML 模板可以应用于所有支持的插件——MySQL、PostgreSQL、Redis、MongoDB、Kafka 等。

官方文档：https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/create-and-connect-a-mysql-cluster  
完整文档索引：https://kubeblocks.io/llms-full.txt

## 先决条件

- 已经安装了 KubeBlocks 的运行中的 Kubernetes 集群。如果没有，请使用以下命令：
  - [创建本地 Kubernetes 集群](../kubeblocks-create-local-k8s-cluster/SKILL.md)  
  - [安装 KubeBlocks](../kubeblocks-install/SKILL.md)  
- 目标的插件必须已经安装（使用 `helm list -n kb-system | grep kb-addon` 进行检查）

## 工作流程

```
- [ ] Step 1: Determine addon and topology
- [ ] Step 2: Apply Cluster CR
- [ ] Step 3: Verify cluster is running
- [ ] Step 4: Connect to the cluster
```

## 第一步：确定插件和拓扑结构

询问用户需要使用哪种数据库引擎。根据下表选择正确的 `clusterDef`、`topology` 和 `componentSpecs` 值。

### 常见插件快速参考

| 插件 | clusterDef | Topology | 组件名称 | 默认端口 | serviceVersion |
|-------|-----------|----------|----------------|-------------|----------------|
| MySQL (ApeCloud) | apecloud-mysql | apecloud-mysql | mysql | 3306 | 8.0.30 |
| MySQL (Community) | mysql | mysql-replication | mysql | 3306 | 8.0.33 |
| PostgreSQL | postgresql | postgresql | postgresql | 5432 | 14.8.0 |
| Redis | redis | redis-cluster | redis | 6379 | 7.2.4 |
| MongoDB | mongodb | mongodb-replicaset | mongodb | 27017 | 6.0.16 |
| Kafka | kafka | kafka-combined | kafka-combine | 9092 | 3.7.2 |

> **注意：** 不同版本的插件可能会导致拓扑结构和版本号发生变化。请运行 `kubectl get clusterdefinitions` 和 `kubectl get componentversions` 以查看您的环境中可用的选项。

如果用户需要特定插件的 **详细拓扑选项或高级配置**，请参考相应的插件文档（例如：`kubeblocks-addon-mysql`、`kubeblocks-addon-postgresql`、`kubeblocks-addon-redis`、`kubeblocks-addon-mongodb`、`kubeblocks-addon-kafka`）。

## 第二步：应用集群 CR

### 通用集群模板

根据上面的插件表格替换占位符值：

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: <cluster-name>
  namespace: <namespace>
spec:
  clusterDef: <addon>
  topology: <topology>
  terminationPolicy: Delete
  componentSpecs:
    - name: <component>
      serviceVersion: "<version>"
      replicas: <N>
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### 示例：创建一个包含 3 个副本的 MySQL 集群

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-cluster
  namespace: default
spec:
  clusterDef: apecloud-mysql
  topology: apecloud-mysql
  terminationPolicy: Delete
  componentSpecs:
    - name: mysql
      serviceVersion: "8.0.30"
      replicas: 3
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### 示例：创建一个包含 2 个副本的 PostgreSQL 集群

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: pg-cluster
  namespace: default
spec:
  clusterDef: postgresql
  topology: postgresql
  terminationPolicy: Delete
  componentSpecs:
    - name: postgresql
      serviceVersion: "14.8.0"
      replicas: 2
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### 示例：创建一个包含 2 个分片的 Redis 集群

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-cluster
  namespace: default
spec:
  clusterDef: redis
  topology: redis-cluster
  terminationPolicy: Delete
  componentSpecs:
    - name: redis
      serviceVersion: "7.2.4"
      replicas: 2
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### 应用 YAML 文件

将 YAML 文件保存到文件中（例如 `cluster.yaml`），然后应用该文件。

应用之前，请先进行干运行（dry-run）验证：

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

如果干运行报告错误，请修复 YAML 文件后再继续。

```bash
kubectl apply -f cluster.yaml
```

或者直接在线应用 YAML 文件。应用之前，请先进行干运行验证：

```bash
kubectl apply -f - --dry-run=server <<'EOF'
# paste YAML here
EOF
```

如果干运行报告错误，请修复 YAML 文件后再继续。

```bash
kubectl apply -f - <<'EOF'
# paste YAML here
EOF
```

## 第三步：验证集群是否正在运行

监控集群状态，直到其变为 “Running”：

```bash
kubectl get cluster <cluster-name> -n <namespace> -w
```

> **成功条件：** `.status.phase` = `Running`  
> **通常所需时间：** 1-5 分钟  
> **如果超过 10 分钟仍未成功：** 使用 `kubectl describe cluster <cluster-name> -n <namespace>` 进行检查。

检查所有 Pod 是否已准备好：

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

预期输出（以包含 3 个副本的 MySQL 集群为例）：

```
NAME                    READY   STATUS    RESTARTS   AGE
mysql-cluster-mysql-0   4/4     Running   0          2m
mysql-cluster-mysql-1   4/4     Running   0          90s
mysql-cluster-mysql-2   4/4     Running   0          60s
```

如果 Pod 仍未运行，请查看相关事件：

```bash
kubectl describe cluster <cluster-name> -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | grep <cluster-name>
```

## 第四步：连接到集群

### 获取连接凭据

KubeBlocks 会自动生成包含连接凭据的 Secret：

```bash
kubectl get secret <cluster-name>-conn-credential -n <namespace> -o jsonpath='{.data.username}' | base64 -d
kubectl get secret <cluster-name>-conn-credential -n <namespace> -o jsonpath='{.data.password}' | base64 -d
```

### 为本地访问设置端口转发

```bash
# MySQL
kubectl port-forward svc/<cluster-name>-mysql -n <namespace> 3306:3306

# PostgreSQL
kubectl port-forward svc/<cluster-name>-postgresql -n <namespace> 5432:5432

# Redis
kubectl port-forward svc/<cluster-name>-redis -n <namespace> 6379:6379

# MongoDB
kubectl port-forward svc/<cluster-name>-mongodb -n <namespace> 27017:27017
```

## 决策树

```
User wants to create a cluster
├── Which addon?
│   ├── MySQL       → clusterDef: apecloud-mysql or mysql
│   ├── PostgreSQL  → clusterDef: postgresql
│   ├── Redis       → clusterDef: redis
│   ├── MongoDB     → clusterDef: mongodb
│   ├── Kafka       → clusterDef: kafka
│   └── Other       → kubectl get clusterdefinitions
├── How many replicas?
│   ├── Dev/test    → 1 replica, terminationPolicy: Delete
│   └── Production  → 3+ replicas, terminationPolicy: DoNotTerminate
└── Resource sizing?
    ├── Dev/test    → 0.5 CPU, 0.5Gi memory, 20Gi storage
    └── Production  → 2+ CPU, 4Gi+ memory, 100Gi+ storage
```

## 终止策略

| 策略 | 行为 | 推荐使用场景 |
|--------|----------|-----------------|
| `DoNotTerminate` | 阻止集群删除；需要手动修改配置 | 生产环境 |
| `Delete` | 删除集群和 PVC，保留备份 | 开发/测试环境 |
| `WipeOut` | 删除所有资源（包括备份） | 临时环境 |

> **重要提示：** 对于生产环境，请始终使用 `DoNotTerminate` 策略，以防止意外删除集群。

## 故障排除

**集群在 “Creating” 或 “Updating” 状态中卡住：**
- 检查插件是否已安装：`helm list -n kb-system | grep kb-addon`
- 查看 Pod 的事件：`kubectl describe pod <pod-name> -n <namespace>`
- 检查资源是否可用：`kubectl describe nodes`

**镜像拉取错误：**
- 验证镜像注册库。如果在中国，请确保插件使用的是阿里云的镜像注册库。

**资源不足：**
- 减少 `resources.requests` 的值，或向集群中添加更多节点。

有关代理安全最佳实践（干运行、状态确认、生产环境保护）的详细信息，请参阅 [safety-patterns.md](../../references/safety-patterns.md)。

## 参考文档

有关 `Cluster CR` 字段的详细说明以及更多插件示例，请参阅 [reference.md](references/reference.md)。