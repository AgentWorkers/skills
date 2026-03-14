---
name: kubeblocks-create-local-k8s-cluster
metadata:
  version: "0.1.0"
description: 使用 Kind、Minikube 或 k3d 创建一个本地的 Kubernetes 测试集群。该过程包括工具的安装、集群的创建、多节点的配置以及集群功能的验证。适用于用户需要本地 Kubernetes 集群进行测试或开发的情况，或者当用户没有现有的 Kubernetes 集群时。**不适用于生产环境的集群配置（请使用云服务提供商的工具，如 EKS、AKS、GKE）**，也不适用于安装 KubeBlocks（请参阅 kubeblocks-install）。
---
# 创建本地 Kubernetes 测试集群

## 概述

使用 Kind、Minikube 或 k3d 创建一个本地 Kubernetes 集群，用于开发和测试。这三个工具都在本地机器上的 Docker 容器中运行 Kubernetes。

官方文档：https://kubeblocks.io/docs/preview/user_docs/references/prepare-a-local-k8s-cluster

## 工具比较

| 特性 | Kind | Minikube | k3d |
|---------|------|----------|-----|
| 运行引擎 | Docker 中的 Kubernetes | 虚拟机或 Docker | Docker 中的 Kubernetes |
| 支持多节点 | 可以（通过配置） | 有限 | 可以（通过参数） |
| 资源消耗 | 低 | 中等 | 低 |
| 启动速度 | 快 | 较慢 | 快 |
| 适用场景 | 持续集成/持续交付（CI/CD）、测试 | 学习、本地开发 | 轻量级测试 |

**推荐工具：** Kind（广泛使用，轻量级，易于配置多节点）

## 工作流程

```
- [ ] Step 1: Check Docker is running
- [ ] Step 2: Choose and install a tool
- [ ] Step 3: Create a cluster
- [ ] Step 4: Verify the cluster
```

## 第一步：检查 Docker

这三个工具都需要 Docker。请验证 Docker 是否已安装并正在运行：

```bash
docker info > /dev/null 2>&1
```

如果 Docker 未安装，请提示用户先进行安装：
- macOS/Windows：https://www.docker.com/products/docker-desktop/
- Linux：https://docs.docker.com/engine/install/

## 第二步：选择并安装工具

询问用户偏好使用哪个工具。如果没有特别偏好，建议使用 **Kind**。

### Kind

```bash
# macOS
brew install kind

# Linux (amd64)
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Linux (arm64)
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-arm64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/kind

# Windows
choco install kind
```

### Minikube

```bash
# macOS
brew install minikube

# Linux (rpm-based)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-latest.x86_64.rpm
sudo rpm -Uvh minikube-latest.x86_64.rpm

# Linux (deb-based)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb

# Windows
choco install minikube
```

### k3d

```bash
# macOS
brew install k3d

# Linux
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash

# Windows
choco install k3d
```

## 第三步：创建集群

### Kind（默认推荐）

**单节点集群（最简单）：**

```bash
kind create cluster --name kb-test
```

**多节点集群（适用于 KubeBlocks）：**

创建一个配置文件 `kind-config.yaml`：

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

然后创建集群：

```bash
kind create cluster --name kb-test --config kind-config.yaml
```

### Minikube

```bash
# Single-node (default)
minikube start

# With Docker driver (recommended)
minikube start --driver=docker

# With more resources
minikube start --driver=docker --cpus=4 --memory=8192
```

### k3d

```bash
# Single-node
k3d cluster create kb-test

# Multi-node (1 server + 2 agents)
k3d cluster create kb-test --servers 1 --agents 2
```

## 第四步：验证集群

```bash
kubectl get nodes
```

（Kind 多节点集群的示例输出）

```
NAME                    STATUS   ROLES           AGE   VERSION
kb-test-control-plane   Ready    control-plane   30s   v1.31.0
kb-test-worker          Ready    <none>          20s   v1.31.0
kb-test-worker2         Ready    <none>          20s   v1.31.0
```

同时验证 `kubectl` 的上下文是否设置正确：

```bash
kubectl config current-context
```

## 删除集群

当不再需要集群时：

```bash
# Kind
kind delete cluster --name kb-test

# Minikube
minikube delete

# k3d
k3d cluster delete kb-test
```

## 下一步

集群启动后，您可以使用 [install-kubeblocks](../kubeblocks-install/SKILL.md) 文档来安装 KubeBlocks。