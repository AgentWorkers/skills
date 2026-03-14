---
name: kubeblocks-addon-elasticsearch
metadata:
  version: "0.1.0"
description: 在 KubeBlocks 上部署和管理 Elasticsearch 集群，以实现全文搜索、日志分析以及可观测性功能。当用户提到 Elasticsearch、ELK 堆栈、搜索引擎、日志分析、Kibana 或明确希望创建 Elasticsearch 集群时，可使用此功能。支持创建单节点（开发/测试）和多节点集群，并提供相应的连接方法。目前 KubeBlocks 不支持备份/恢复功能。如需创建适用于所有引擎的通用集群，请参阅 `kubeblocks-create-cluster`。对于后续的操作（如扩展集群规模、增加存储空间等），请使用相应的操作技能。
---
# 在 KubeBlocks 上部署 Elasticsearch

## 概述

使用 KubeBlocks 在 Kubernetes 上部署 Elasticsearch 集群。Elasticsearch 是一个分布式、基于 RESTful 的搜索引擎，支持全文搜索、日志分析和可观测性功能。它支持单节点（开发/测试）和多节点拓扑结构。

官方文档：https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/01-overview  
快速入门：https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/02-quickstart  
操作指南：https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/  

**注意：** 目前 KubeBlocks 不支持 Elasticsearch 的备份和恢复功能。

## 先决条件

- 已安装 KubeBlocks 的运行中 Kubernetes 集群（请参阅 [install-kubeblocks](../kubeblocks-install/SKILL.md)）  
- 必须启用 Elasticsearch 插件：  

```bash
# Check if elasticsearch addon is installed
helm list -n kb-system | grep elasticsearch

# Install if missing
helm install kb-addon-elasticsearch kubeblocks/elasticsearch --namespace kb-system --version 1.0.0
```  

## 可用的拓扑结构  

| 拓扑结构 | 默认值 | 组件 | 使用场景 |  
|---|---|---|---|  
| 单节点 | elasticsearch | 开发/测试环境：单个节点承担所有角色 |  
| 多节点 | elasticsearch | 生产环境：至少需要 2 个副本 |  

Elasticsearch 使用单一拓扑结构，组件名称为 `elasticsearch`。对于单节点模式，请在配置文件中设置 `replicas: 1` 并配置 `mode: "single-node"`。在生产环境中，建议使用 `replicas: 3` 或更多副本。  

## 支持的版本  

| 主版本 | 示例版本 |  
|---|---|  
| 6.x | `6.8.23` |  
| 7.x | `7.10.2`, `7.10.1`, `7.8.1`, `7.7.1` |  
| 8.x | `8.15.5`, `8.8.2`, `8.1.3` |  

可用版本列表：`kubectl get cmpv elasticsearch`  

## 工作流程  

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (single-node or multi-node)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect and verify
```  

## 第 1 步：确保插件已安装  

```bash
helm list -n kb-system | grep elasticsearch
```  

如果插件未安装：  
```bash
helm install kb-addon-elasticsearch kubeblocks/elasticsearch --namespace kb-system --version 1.0.0
```  

## 第 2 步：创建命名空间  

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```  

## 第 3 步：创建集群  

### 单节点（开发/测试）  

单个节点承担所有角色（主节点、数据节点、数据导入节点）。适用于开发环境：  

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: es-singlenode
  namespace: demo
spec:
  clusterDef: elasticsearch
  terminationPolicy: Delete
  componentSpecs:
    - name: elasticsearch
      serviceVersion: "8.8.2"
      replicas: 1
      configs:
        - name: es-cm
          variables:
            mode: "single-node"
      resources:
        limits: {cpu: "1", memory: "2Gi"}
        requests: {cpu: "1", memory: "2Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```  

### 多节点（生产环境）  

通过多个副本实现高可用性和数据分片分布：  

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: es-cluster
  namespace: demo
spec:
  clusterDef: elasticsearch
  terminationPolicy: Delete
  componentSpecs:
    - name: elasticsearch
      serviceVersion: "8.8.2"
      replicas: 3
      resources:
        limits: {cpu: "1", memory: "2Gi"}
        requests: {cpu: "1", memory: "2Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```  

**关键点：**  
- 对于多节点集群，不要设置 `mode: "single-node"`  
- 主节点的副本数量应为奇数（例如 3 或 5）以满足法定人数要求  
- 默认端口：9200（HTTP），9300（传输协议）  

### 使用 dry-run 进行测试  

根据 [安全最佳实践](../../references/safety-patterns.md)，在正式应用之前务必先进行 dry-run：  

```bash
kubectl apply -f cluster.yaml --dry-run=server
```  

如果 dry-run 成功：  
```bash
kubectl apply -f cluster.yaml
```  

## 第 4 步：等待集群启动完成  

```bash
kubectl -n demo get cluster <cluster-name> -w
```  

**成功条件：** 集群状态显示为 `Running`。通常需要 1–5 分钟。如果 10 分钟后仍未启动，请检查问题：  

```bash
kubectl describe cluster <cluster-name> -n demo
kubectl get events -n demo --sort-by='.lastTimestamp' | grep <cluster-name>
```  

检查相关 Pod 的状态：  
```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```  

## 第 5 步：连接并验证集群  

### 端口转发  

```bash
kubectl -n demo port-forward svc/<cluster-name>-elasticsearch-http 9200:9200
```  

### 集群健康检查  

预期状态：`"status" : "green"` 或 `"yellow"`（单节点情况下 `"yellow"` 也是可接受的）。  

### 查看集群信息  

```bash
curl -s http://localhost:9200
```  

## 故障排除  

**集群在创建过程中卡住：**  
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```  

**Pod 无法启动：**  
```bash
kubectl -n demo logs <elasticsearch-pod>
kubectl -n demo describe pod <elasticsearch-pod>
```  

**内存不足：**  
- 增加 `resources.limits.memory` 和 `resourcesrequests.memory` 的值  
- 生产环境建议至少配置 2 GiB 的内存  

**单节点集群显示为黄色状态：**  
- 这是正常现象，因为单节点无法分配额外的副本。建议使用多节点集群以获得绿色状态。  

## 日常维护操作  

**注意：** 目前 KubeBlocks 不支持 Elasticsearch 的备份和恢复功能。  

| 操作 | 所需技能 | 外部文档 |  
|---|---|---|  
| 停止/启动/重启集群 | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |  
| 调整 CPU/内存资源 | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |  
| 增加/减少副本数量 | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |  
| 扩展存储空间 | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |  
| 公开集群服务 | [expose-service](../kubeblocks-expose-service/SKILL.md) | [文档](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |  

## 安全最佳实践  

请遵循 [safety-patterns.md](../../references/safety-patterns.md) 中的建议：在应用前进行 dry-run，监控集群状态后确认结果，并在删除资源前执行必要的检查。