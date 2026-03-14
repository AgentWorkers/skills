---
name: kubeblocks-install
metadata:
  version: "0.1.0"
description: 通过 Helm 在任何 Kubernetes 集群上安装 KubeBlocks 运算符。该过程包括版本选择、环境检测（本地开发环境与生产环境、中国大陆网络与全球网络）、镜像注册表配置、先决条件检查以及安装后的验证。当用户需要安装、部署或配置 KubeBlocks 时，请使用此操作。请注意：此操作不适用于升级现有的 KubeBlocks 安装（请参阅 KubeBlocks 官方升级文档），也不适用于卸载 KubeBlocks（请参阅本文档中的“卸载”部分），更不适用于在安装后创建数据库集群（请参阅 kubeblocks-create-cluster 或 kubeblocks-addon-* 相关技能）。
---
# 安装 KubeBlocks Operator

## 概述

KubeBlocks 是一个用于管理数据库（MySQL、PostgreSQL、Redis、MongoDB、Kafka 等）的 Kubernetes Operator。本文档将指导您如何将 KubeBlocks Operator 安装到任意 Kubernetes 集群上。

官方文档：https://kubeblocks.io/docs/preview/user_docs/overview/install-kubeblocks  
完整文档索引：https://kubeblocks.io/llms-full.txt  

## 工作流程

请复制以下检查清单并记录安装进度：  
```
- [ ] Step 1: Check prerequisites
- [ ] Step 2: Determine version
- [ ] Step 3: Detect network environment
- [ ] Step 4: Install CRDs
- [ ] Step 5: Install KubeBlocks via Helm
- [ ] Step 6: Verify installation
```  

## 第 1 步：检查先决条件  

安装 KubeBlocks Operator 需要一个已存在的 Kubernetes 集群。如果用户没有集群，请先引导他们参考 [创建本地 Kubernetes 集群](../kubeblocks-create-local-k8s-cluster/SKILL.md) 的文档。  

执行以下检查，并自动安装任何缺失的工具：  

### 1a: kubectl  
```bash
kubectl version --client 2>/dev/null
```  
如果命令执行失败（提示未找到 kubectl），请安装它：  
```bash
# macOS
brew install kubectl

# Linux (amd64)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/

# Linux (arm64)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
```  

### 1b: Helm（版本 3 或更高）  
```bash
helm version --short 2>/dev/null
```  
如果命令执行失败（提示未找到 Helm），请安装它：  
```bash
# macOS
brew install helm

# Linux (script, works on amd64/arm64)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```  

### 1c: 验证集群访问权限  
```bash
kubectl get nodes
```  
如果验证失败，说明用户无法访问 Kubernetes 集群。**请在此处停止操作**，并告知用户：  
- 对于本地测试，请使用 [创建本地 Kubernetes 集群](../kubeblocks-create-local-k8s-cluster/SKILL.md) 的文档。  
- 对于生产环境，请确保 kubeconfig 配置正确（位于 `~/.kube/config` 或 `$KUBECONFIG` 文件中）。  

**最低资源要求**：  
- 控制平面（Control Plane）：1 个节点，4 核心，4GB 内存，50GB 存储空间  
- 数据平面（Data Plane）：2-3 个节点，每个节点配备 2 核心，4GB 内存和 50GB 存储空间  

## 第 2 步：确定版本  

询问用户是否需要特定版本。如果没有指定版本，请下载最新稳定版本：  
```bash
# Get latest stable version
curl -s https://api.github.com/repos/apecloud/kubeblocks/releases/latest | grep '"tag_name"' | cut -d'"' -f4
```  
要查看所有可用版本，请执行：  
```bash
# Via GitHub API
curl -s https://api.github.com/repos/apecloud/kubeblocks/tags | grep '"name"' | head -20 | cut -d'"' -f4

# Or via Helm (after adding repo)
helm search repo kubeblocks/kubeblocks --versions
```  
已知稳定版本：v1.0.2、v1.0.1、v1.0.0、v0.9.5、v0.9.4、v0.9.3、v0.9.2、v0.9.1、v0.9.0  

**务必告知用户正在安装的具体版本。**  

## 第 3 步：检测网络环境  

确定要使用哪个镜像仓库（Image Registry）。  

**默认设置（全局访问，可使用 docker.io）：**  
- 镜像仓库：`docker.io`  
- 命名空间：`apecloud`  

**中国内地（无法访问或访问速度较慢的情况）：**  
- 镜像仓库：`apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com`  
- 命名空间：`apecloud`  

**检测方法：** 询问用户或进行快速测试：  
```bash
# Test docker.io connectivity (timeout 5s)
curl -sS --connect-timeout 5 https://registry-1.docker.io/v2/ > /dev/null 2>&1 && echo "docker.io: reachable" || echo "docker.io: unreachable, use China mirror"
```  

## 第 4 步：安装 CRDs（Custom Resource Definitions）  
```bash
# Replace {VERSION} with the chosen version, e.g. v1.0.2
kubectl create -f https://github.com/apecloud/kubeblocks/releases/download/{VERSION}/kubeblocks_crds.yaml
```  
**对于 Kubernetes 版本低于 1.23 的集群**，请添加 `--validate=false` 参数：  
```bash
kubectl create -f https://github.com/apecloud/kubeblocks/releases/download/{VERSION}/kubeblocks_crds.yaml --validate=false
```  

## 第 5 步：通过 Helm 安装 KubeBlocks  

### 5a: 添加 Helm 仓库  
```bash
helm repo add kubeblocks https://apecloud.github.io/helm-charts
helm repo update
```  

### 5b: 安装 KubeBlocks  
**全局网络（可访问 docker.io）：**  
```bash
helm install kubeblocks kubeblocks/kubeblocks \
  --namespace kb-system --create-namespace \
  --version {VERSION} \
  --set image.registry=docker.io \
  --set dataProtection.image.registry=docker.io \
  --set addonChartsImage.registry=docker.io
```  
**中国内地网络：**  
```bash
helm install kubeblocks kubeblocks/kubeblocks \
  --namespace kb-system --create-namespace \
  --version {VERSION} \
  --set image.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com \
  --set dataProtection.image.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com \
  --set addonChartsImage.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com
```  

### 常见额外选项  
有关所有选项的详细信息，请参阅 [reference.md](references/reference.md)。  

## 第 6 步：验证安装结果  

如果 Pod 未运行，请检查相关事件日志：  
```bash
kubectl -n kb-system describe pods
kubectl -n kb-system get events --sort-by='.lastTimestamp'
```  

## 故障排除  

**安装 CRD 时出现 `x-kubernetes-validations` 错误：**  
- 如果使用的是 Kubernetes 版本低于 1.23，请在 `kubectl create` 命令中添加 `--validate=false` 参数。  

**镜像拉取失败：**  
- 检查镜像仓库的访问情况；如果位于中国内地，请切换到对应的镜像仓库。  
- 验证镜像仓库设置：`helm get values kubeblocks -n kb-system`  

**Helm 安装超时：**  
- 检查节点资源利用率：`kubectl describe nodes`  
- 在资源受限的环境中，可以省略默认添加的插件：`--set autoInstalledAddons="{}"`  

**KubeBlocks 已经安装：**  
- 检查现有安装情况：`helm list -n kb-system | grep kubeblocks`  
- 如需升级，请执行：`helm upgrade kubeblocks kubeblocks/kubeblocks --namespace kb-system --version {VERSION}`  

## 卸载  

有关卸载的详细说明，请参阅 [reference.md](references/reference.md)。  

快速卸载方法：  
```bash
# Delete all clusters and backups first
kubectl get cluster -A
kubectl delete cluster --all -A

# Uninstall addons
helm list -n kb-system | grep kb-addon | awk '{print $1}' | xargs -I {} helm -n kb-system uninstall {}

# Uninstall KubeBlocks
helm uninstall kubeblocks --namespace kb-system

# Remove CRDs
kubectl get crd -o name | grep kubeblocks.io | xargs kubectl delete
```