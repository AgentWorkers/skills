---
name: runpodctl
description: 使用 `runpodctl` CLI 来管理 `RunPod` GPU Pod、无服务器端点（serverless endpoints）、模板（templates）、网络卷（network volumes）以及模型（models）。当用户需要列出/创建/停止/删除 Pod、管理无服务器端点、检查 GPU 的可用性或管理 `RunPod` 资源时，可以使用该工具。
metadata:
  openclaw:
    emoji: 🖥️
    requires:
      bins:
        - runpodctl
---
# RunPod CLI 技能

用于管理 RunPod 上的 GPU Pod、无服务器端点（serverless endpoints）、模板（templates）、网络卷（network volumes）以及模型（models）。

> **二进制文件路径：** `~/.local/bin/runpodctl`
> **命令名称拼写：** “Runpod”（首字母大写），实际使用的命令是 `runpodctl`（首字母小写）。

## 设置（首次使用）

如果尚未配置 API 密钥：
```bash
~/.local/bin/runpodctl config set --apiKey YOUR_API_KEY
```
API 密钥：https://runpod.io/console/user/settings

检查设置是否正确：
```bash
~/.local/bin/runpodctl user
```

## Pod

```bash
~/.local/bin/runpodctl pod list               # List running pods
~/.local/bin/runpodctl pod list --all         # All pods including stopped
~/.local/bin/runpodctl pod get <pod-id>       # Pod details + SSH info
~/.local/bin/runpodctl pod create --template-id runpod-torch-v21 --gpu-id "NVIDIA RTX 4090"
~/.local/bin/runpodctl pod start <pod-id>
~/.local/bin/runpodctl pod stop <pod-id>
~/.local/bin/runpodctl pod restart <pod-id>
~/.local/bin/runpodctl pod delete <pod-id>
```

## GPU 与模板

```bash
~/.local/bin/runpodctl gpu list                          # Available GPUs + prices
~/.local/bin/runpodctl template list --type official     # Official templates
~/.local/bin/runpodctl template search pytorch           # Search templates
~/.local/bin/runpodctl template get <template-id>        # Template details
```

## 无服务器端点

```bash
~/.local/bin/runpodctl serverless list
~/.local/bin/runpodctl serverless get <endpoint-id>
~/.local/bin/runpodctl serverless create --name "x" --template-id "tpl_abc"
~/.local/bin/runpodctl serverless update <endpoint-id> --workers-max 5
~/.local/bin/runpodctl serverless delete <endpoint-id>
```

## 网络卷

```bash
~/.local/bin/runpodctl network-volume list
~/.local/bin/runpodctl network-volume create --name "x" --size 100 --data-center-id "US-GA-1"
~/.local/bin/runpodctl network-volume delete <volume-id>
```

## 模型

```bash
~/.local/bin/runpodctl model list
~/.local/bin/runpodctl model list --name "llama"
~/.local/bin/runpodctl model add --name "my-model" --model-path ./model
```

## 账户

```bash
~/.local/bin/runpodctl user          # Account info + balance
```

## 访问 Pod

Pod 的暴露端口可以通过以下地址访问：`https://<pod-id>-<port>.proxy.runpod.net`

## 注意事项：

- 在执行命令时，请始终使用完整的路径 `~/.local/bin/runpodctl`，因为在沙箱环境中可能无法加载 `PATH` 环境变量。
- 创建 Pod 时必须指定 `--template-id` 或 `--image` 参数。
- GPU 的名称必须完全匹配（例如：“NVIDIA RTX 4090” 或 “NVIDIA A100 80GB PCIe”）。