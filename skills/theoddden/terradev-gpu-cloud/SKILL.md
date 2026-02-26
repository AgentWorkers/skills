---
name: terradev-gpu-cloud
description: 跨云GPU资源调配：采用NUMA对齐的拓扑优化方案，实现Kubernetes（K8s）集群的快速创建；支持实时查询11家以上云服务提供商的定价信息，能在几秒钟内配置到最便宜的GPU资源；支持自动完成GPU与网络接口（NIC）的配对，从而快速搭建生产环境中的K8s集群；当本地GPU资源达到上限时，可无缝切换至云资源进行计算。BYOAPI（Bring Your Own API）技术确保您的API密钥始终安全地保存在本地设备上，无需担心数据泄露风险。
version: 1.0.0
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - TERRADEV_RUNPOD_KEY
        - TERRADEV_VASTAI_KEY
        - TERRADEV_AWS_ACCESS_KEY_ID
        - TERRADEV_AWS_SECRET_ACCESS_KEY
        - TERRADEV_AWS_DEFAULT_REGION
        - TERRADEV_GCP_PROJECT_ID
        - TERRADEV_GCP_CREDENTIALS_PATH
        - TERRADEV_AZURE_SUBSCRIPTION_ID
        - TERRADEV_AZURE_CLIENT_ID
        - TERRADEV_AZURE_CLIENT_SECRET
        - TERRADEV_AZURE_TENANT_ID
        - TERRADEV_ORACLE_USER_OCID
        - TERRADEV_ORACLE_FINGERPRINT
        - TERRADEV_ORACLE_PRIVATE_KEY_PATH
        - TERRADEV_ORACLE_TENANCY_OCID
        - TERRADEV_ORACLE_REGION
        - TERRADEV_LAMBDA_API_KEY
        - TERRADEV_COREWEAVE_API_KEY
        - TERRADEV_CRUSOE_API_KEY
        - TERRADEV_TENSORDOCK_API_KEY
        - HF_TOKEN
      bins:
        - terradev
        - python3
      optionalBins:
        - kubectl
        - docker
      anyBins:
        - kubectl
        - docker
    primaryEnv: TERRADEV_RUNPOD_KEY
    emoji: "🚀"
    homepage: https://github.com/theoddden/Terradev
    install:
      - kind: uv
        package: terradev-cli
        bins: [terradev]
      - kind: uv
        package: "terradev-cli[all]"
        bins: [terradev]
        note: "Optional: Install with all cloud provider SDKs"
---
# Terradev GPU Cloud — 为 OpenClaw 提供跨云 GPU 资源管理服务

Terradev GPU Cloud 是一个基于 Terradev CLI 的云 GPU 资源管理工具，它帮助用户从 11 家以上的云服务提供商中寻找最便宜的 GPU，创建 Kubernetes 集群，部署推理端点，并管理云计算资源——所有这些操作都通过自然语言指令完成。

**BYOAPI**：所有 API 密钥都保存在用户的本地设备上，不会通过第三方进行代理。

## 凭据要求

### 最小配置（仅支持 RunPod）
```bash
export TERRADEV_RUNPOD_KEY=your_runpod_api_key
```

### 全面多云配置（可选）
```bash
# AWS
export TERRADEV_AWS_ACCESS_KEY_ID=your_key
export TERRADEV_AWS_SECRET_ACCESS_KEY=your_secret
export TERRADEV_AWS_DEFAULT_REGION=us-east-1

# GCP
export TERRADEV_GCP_PROJECT_ID=your_project
export TERRADEV_GCP_CREDENTIALS_PATH=/path/to/service-account.json

# Azure
export TERRADEV_AZURE_SUBSCRIPTION_ID=your_sub
export TERRADEV_AZURE_CLIENT_ID=your_client
export TERRADEV_AZURE_CLIENT_SECRET=your_secret
export TERRADEV_AZURE_TENANT_ID=your_tenant

# Additional providers (optional)
export TERRADEV_VASTAI_KEY=your_key
export TERRADEV_ORACLE_USER_OCID=your_ocid
# ... etc for other providers
```

### 可选依赖项
- **kubectl**：仅用于 Kubernetes 集群命令
- **docker**：仅用于本地容器操作
- **Cloud SDKs**：随 `terradev-cli[all]` 自动安装

## 功能介绍

### 1. GPU 价格查询
当用户询问 GPU 价格、可用性或希望比较不同云服务提供商的价格时：
```bash
# Get real-time prices across all providers
terradev quote -g <GPU_TYPE>

# Filter by specific providers
terradev quote -g <GPU_TYPE> -p runpod,vastai,lambda

# Quick-provision the cheapest option
terradev quote -g <GPU_TYPE> --quick
```

支持的 GPU 类型：H100、A100、A10G、L40S、L4、T4、RTX4090、RTX3090、V100

示例响应：
- “帮我找到最便宜的 H100 GPU” → `terradev quote -g H100`
- “比较 A100 GPU 的价格” → `terradev quote -g A100`
- “获取每小时费用低于 2 美元的 GPU” → `terradev quote -g A100` 然后筛选结果

### 2. GPU 资源分配
当用户希望实际启动 GPU 实例时：
```bash
# Provision cheapest instance
terradev provision -g <GPU_TYPE>

# Provision multiple GPUs in parallel across clouds
terradev provision -g <GPU_TYPE> -n <COUNT> --parallel 6

# Dry run — show the plan without launching
terradev provision -g <GPU_TYPE> -n <COUNT> --dry-run

# Set a max price ceiling
terradev provision -g <GPU_TYPE> --max-price 2.50
```

示例响应：
- “启动 4 个 H100 GPU 实例” → `terradev provision -g H100 -n 4 --parallel 6`
- “获取一个价格合理的 A100 GPU” → `terradev provision -g A100`
- “显示 8 个 GPU 的总费用” → `terradev provision -g A100 -n 8 --dry-run`

### 3. Kubernetes GPU 集群
当用户需要包含 GPU 节点的 Kubernetes 集群时：
```bash
# Create a multi-cloud K8s cluster with GPU nodes
terradev k8s create <CLUSTER_NAME> --gpu <GPU_TYPE> --count <N> --multi-cloud --prefer-spot

# List clusters
terradev k8s list

# Get cluster info
terradev k8s info <CLUSTER_NAME>

# Destroy cluster
terradev k8s destroy <CLUSTER_NAME>
```

拓扑优化（自动完成，无需手动配置 kubelet）：
- GPU 和其网卡被放置在同一个 PCIe 스위치后面，以消除跨插槽的延迟
- 在分配过程中优化 GPU 与网卡的配对，以获得最大的节点间带宽
- 使用 Karpenter NodeClass 实现优先选择便宜的 GPU 节点进行调度
- 当 GPU 使用率达到 90% 时，KEDA 会自动触发扩展
- 采用 CNI-first 的插件顺序来处理 EKS v21 的竞态条件
- 支持多云节点池（AWS + GCP + CoreWeave）

示例响应：
- “创建一个包含 4 个 H100 GPU 的 Kubernetes 集群” → `terradev k8s create my-cluster --gpu H100 --count 4 --multi-cloud --prefer-spot`
- “我需要一个用于训练的集群” → `terradev k8s create training-cluster --gpu A100 --count 8 --prefer-spot`
- “销毁我的集群” → `terradev k8s destroy <cluster_name>`

### 4. 推理端点部署（InferX）
当用户希望部署模型以供推理使用时：
```bash
# Deploy a model to InferX serverless platform
terradev inferx deploy --model <MODEL_ID> --gpu-type <GPU>

# Check endpoint status
terradev inferx status

# List deployed models
terradev inferx list

# Get cost analysis
terradev inferx optimize
```

示例响应：
- “部署 Llama 2 模型进行推理” → `terradev inferx deploy --model meta-llama/Llama-2-7b-hf --gpu-type a10g`
- “我的推理任务费用是多少？” → `terradev inferx optimize`

### 5. 在 HuggingFace Spaces 上部署模型
当用户希望公开分享模型时：
```bash
# Deploy any HF model to Spaces
terradev hf-space <SPACE_NAME> --model-id <MODEL_ID> --template <TEMPLATE>

# Templates: llm, embedding, image
```

所需工具：`pip install "terradev-cli[hf]"` 和 `HF_TOKEN` 环境变量

示例响应：
- “将我的模型部署到 HuggingFace Spaces” → `terradev hf-space my-model --model-id <model> --template llm`
- “公开分享这个模型” → `terradev hf-space my-demo --model-id <model> --hardware a10g-large --sdk gradio`

### 6. 本地 GPU 资源不足时的云扩展
当用户的本地 GPU 资源已满或需要更多计算资源时：
**步骤 1**：确定需求
- 哪种 GPU 类型适合他们的本地硬件？
- 需要额外多少个 GPU？
- 用途是训练还是推理？

**步骤 2**：查询并分配资源
```bash
# Find cheapest overflow capacity
terradev quote -g A100

# Provision overflow instances
terradev provision -g A100 -n 2 --parallel 6

# Or one-command Docker workload
terradev run --gpu A100 --image pytorch/pytorch:latest -c "python train.py"

# Keep an inference server alive
terradev run --gpu H100 --image vllm/vllm-openai:latest --keep-alive --port 8000
```

**步骤 3**：将任务连接到云资源
```bash
# Execute commands on provisioned instances
terradev execute -i <instance-id> -c "python train.py"

# Stage datasets near compute
terradev stage -d ./my-dataset --target-regions us-east-1,eu-west-1
```

### 7. 实例管理
当用户需要查看或管理正在运行的实例时：
```bash
# View all instances and costs
terradev status --live

# Stop/start/terminate instances
terradev manage -i <instance-id> -a stop
terradev manage -i <instance-id> -a start
terradev manage -i <instance-id> -a terminate

# Cost analytics
terradev analytics --days 30

# Find cheaper alternatives
terradev optimize
```

### 8. 云服务提供商配置
当用户需要配置云服务提供商时：
```bash
# Quick setup instructions for any provider
terradev setup runpod --quick
terradev setup aws --quick
terradev setup vastai --quick

# Configure credentials (stored locally, never transmitted)
terradev configure --provider runpod
terradev configure --provider aws
terradev configure --provider vastai
```

支持的云服务提供商：RunPod、Vast.ai、AWS、GCP、Azure、Lambda Labs、CoreWeave、TensorDock、Oracle Cloud、Crusoe Cloud、DigitalOcean、HyperStack

## 重要规则

1. **BYOAPI**：始终提醒用户 API 密钥需保存在本地，Terradev 不会代理任何凭据。
2. **先进行模拟测试**：对于成本较高的操作（如多 GPU 资源分配），建议先使用 `--dry-run` 选项。
3. **优先选择便宜的云资源**：默认设置为 `--prefer-spot` 以节省成本，但会提醒用户长时间训练任务可能存在中断风险。
4. **透明定价**：在分配资源前始终提供价格报价。
5. **安全第一**：未经用户确认，不会自动进行资源分配，会先展示详细的计划。
6. **优先使用本地资源**：如果用户有本地 GPU 资源，建议优先使用。

## 价格信息

典型 GPU 价格（实时变动）：
- **H100（80GB）**：1.50–4.00 美元/小时（RunPod/Lambda 最便宜）
- **A100（80GB）**：1.00–3.00 美元/小时
- **A10G（24GB）**：0.50–1.50 美元/小时
- **T4（16GB）**：0.20–0.75 美元/小时
- **RTX 4090（24GB）**：0.30–0.80 美元/小时

相同硬件的价格在不同云服务提供商之间可能有很大差异。Terradev 会同时查询所有提供商，以实时找到最优惠的价格。

## 安装说明
```bash
pip install terradev-cli
# With all providers + HF Spaces:
pip install "terradev-cli[all]"
```

## 链接
- GitHub：https://github.com/theoddden/Terradev
- PyPI：https://pypi.org/project/terradev-cli/
- 文档：https://theodden.github.io/Terradev/