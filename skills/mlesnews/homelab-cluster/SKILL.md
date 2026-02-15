---
name: homelab-cluster
description: |
  Manage multi-tier AI inference clusters for homelabs. Health monitoring, expert MoE routing,
  automatic node recovery, and model deployment across Ollama and llama.cpp nodes. Covers GPU
  memory planning, Docker volume strategies for large models, sequential startup patterns to
  avoid CUDA deadlocks, and unified API gateways via LiteLLM.
version: "1.0.0"
license: MIT
metadata:
  author: mlesnews
  org: Lumina Homelab
  domain: luminahomelab.ai
  emoji: "🏠"
  tags:
    - homelab
    - infrastructure
    - llm
    - gpu
    - monitoring
    - ollama
    - llama-cpp
    - compute-cluster
    - litellm
    - docker
---

# 家庭实验室集群管理

本文档介绍了如何管理一个由多层GPU和CPU推理节点组成的AI计算集群。该集群由[Lumina Homelab](https://luminahomelab.ai)开发并经过实际测试。

## 使用场景

当您的应用程序需要执行以下操作时，可以使用此功能：
- 监控分布式模型端点的运行状态
- 将推理请求路由到性能最佳的模型
- 自动恢复故障节点
- 规划模型之间的GPU内存分配
- 在异构硬件上部署模型

## 架构模式

一个家庭实验室集群通常包含2-3个层级：
| 层次 | 典型硬件 | 运行时环境 | 功能 |
|------|-----------------|---------|------|
| **本地层** | 主GPU（RTX 4090/5090） | Ollama | 快速推理、嵌入计算 |
| **远程层** | 辅助GPU（RTX 3090/4090） | llama.cpp或Ollama | 分布式推理 |
| **NAS/CPU层** | Synology、RPi或其他CPU节点 | Ollama | 轻量级模型、备用方案 |

在集群的前端部署了一个**LiteLLM代理**，它为所有层级提供统一的OpenAI兼容API。

## 运行状态监控

您可以配置针对每个端点的超时时间来检查所有端点的运行状态：

```bash
# Define endpoints with tier labels
ENDPOINTS = {
    "local/ollama": {"url": "http://localhost:11434/api/tags", "tier": "LOCAL"},
    "remote/mark-i": {"url": "http://REMOTE_IP:3009/v1/models", "tier": "REMOTE", "timeout": 8},
    "gateway/litellm": {"url": "http://localhost:8080/health/liveliness", "tier": "GATEWAY"},
}

# For each endpoint: GET with timeout, check HTTP 200
# Classify: HEALTHY / DEGRADED / DOWN per tier
# Overall prognosis based on tier health
```

**重要提示：** 使用`/health/liveliness`来查询LiteLLM的运行状态，而不是`/health`——后者会尝试连接所有模型节点，如果某个节点无法访问可能会导致系统挂起。

## 基于任务的模型路由

根据任务类型将请求路由到最合适的模型：

```
Task Categories:
  code     → Coder model (Qwen2.5-Coder-7B or similar)
  reason   → Reasoning model (DeepSeek-R1-Distill or similar)
  chat     → General model (Qwen2.5-14B or similar)
  vision   → Vision model (Qwen2.5-VL or similar)
  fast     → Smallest available model for quick responses
  embed    → Embedding model (nomic-embed-text or similar)

Router logic:
  1. Classify task from prompt
  2. Check health of preferred model
  3. Fallback to next-best if unavailable
  4. Return model endpoint + metadata
```

## Docker部署（在远程节点上运行llama.cpp）

**关键提示：** 使用Docker卷而非绑定挂载

对于文件大小超过1.5GB的模型，在Windows Docker主机上应使用Docker卷：
```bash
# Create a Docker volume for model storage
docker volume create models-vol

# Copy models INTO the volume
docker run --rm -v models-vol:/models -v /host/path:/src alpine cp /src/model.gguf /models/

# Run container FROM volume (not bind mount)
docker run -d --gpus all -v models-vol:/models -p 3009:8000 \
  -e MODEL_PATH=/models/model.gguf your-llamacpp-image
```

**原因：** Windows的绑定挂载方式会通过gRPC-FUSE/9P桥接机制进行数据传输，在处理大型文件时可能导致GPU张量加载失败。而Docker卷使用Linux的原生ext4文件系统，可以完全避免这个问题。

## 容器启动顺序

切勿同时启动多个GPU容器：

```bash
# WRONG — causes CUDA initialization deadlock
docker start mark-i mark-iii mark-iv mark-vi &

# RIGHT — sequential with health check between each
for container in mark-v mark-iii mark-iv mark-vi mark-i; do
  docker restart $container
  sleep 5
  # Verify health before starting next
  curl -s http://localhost:PORT/v1/models || echo "Warning: $container slow to start"
done
```

## GPU内存规划

确保模型的运行需求不会超出系统的VRAM容量：

```
Example for 24GB GPU:
  14B model (Q4_K_M)  →  9.0 GB, 28 GPU layers
  7B coder            →  4.4 GB, full GPU
  8B reasoning        →  4.6 GB, full GPU
  1.5B fast coder     →  1.1 GB, full GPU
  1.7B fast chat      →  1.0 GB, full GPU
  ─────────────────────────────
  Total:               20.1 GB (~84% utilized)

  Remaining: CPU-only containers for 32B+ models
```

## 节点自动恢复

当远程节点出现故障（如Docker桌面崩溃或重启）时，系统应能够自动恢复节点服务：

```
Recovery sequence:
  1. Health check fails for remote tier
  2. Check if SSH is responsive (node is up but Docker is down)
  3. If SSH works: restart Docker Desktop via SSH
  4. If SSH fails: create RDP session to wake the machine
  5. Wait for Docker + sequential container restart
  6. Re-check health
```

**重要提示：** 绝不要以明文形式存储恢复所需的凭据。请使用安全存储解决方案（如Azure Key Vault、HashiCorp Vault等），并通过标准输入（stdin）传递敏感信息，切勿将其作为CLI参数传递。

## LiteLLM网关配置

所有层级都使用统一的API接口：

```yaml
model_list:
  # Local Ollama models
  - model_name: local/chat
    litellm_params:
      model: ollama/qwen2.5:32b
      api_base: http://localhost:11434

  # Remote llama.cpp models (need openai/ prefix)
  - model_name: remote/mark-i
    litellm_params:
      model: openai/qwen2.5-14b-instruct
      api_base: http://REMOTE_IP:3009/v1
      api_key: "not-needed"

  # NAS Ollama models
  - model_name: nas/coder
    litellm_params:
      model: ollama/qwen2.5-coder:7b
      api_base: http://NAS_IP:11434
```

**关键注意事项：** llama.cpp端点的模型名称前必须加上`openai/`前缀，同时`api_base`路径中必须包含`/v1`，以确保与LiteLLM的兼容性。

## 参考链接：
- **Lumina Homelab：** [luminahomelab.ai](https://luminahomelab.ai)
- **X/Twitter：** [@HK47LUMINA](https://x.com/HK47LUMINA)
- **GitHub：** [mlesnews](https://github.com/mlesnews)