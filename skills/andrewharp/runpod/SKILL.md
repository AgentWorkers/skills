---
name: runpod
description: 管理 RunPod GPU 云实例：创建、启动、停止实例，以及通过 SSH 和 API 连接到这些实例。适用于需要使用 RunPod 基础设施、GPU 实例，或需要对远程 GPU 机器进行 SSH 访问的场景。该工具负责处理实例的生命周期管理、SSH 代理连接、文件系统挂载以及 API 请求。使用前请确保已安装 `runpodctl`（可通过 `brew install runpod/runpodctl/runpodctl` 命令安装）。
---

# RunPod 技能

用于管理 RunPod 的 GPU 云实例、SSH 连接以及文件系统访问。

## 先决条件

```bash
brew install runpod/runpodctl/runpodctl
runpodctl config --apiKey "your-api-key"
```

**SSH 密钥：** `runpodctl` 会在 `~/.runpod/ssh/` 目录下管理 SSH 密钥：

```bash
runpodctl ssh add-key
```

您可以在以下链接查看和管理密钥：https://console.runpod.io/user/settings

**挂载脚本配置：**
挂载脚本会首先检查 `~/.ssh/runpod_key` 文件，如果找不到该文件，则会使用 `runpodctl` 的默认密钥。您可以通过以下方式覆盖默认配置：
```bash
export RUNPOD_SSH_KEY="$HOME/.runpod/ssh/RunPod-Key"
```

主机密钥存储在单独的 `~/.runpod/ssh/known_hosts` 文件中（与您的主 SSH 配置文件分离）。该脚本使用 `StrictHostKeyChecking=accept-new` 选项在重新连接时验证主机，并允许新的 RunPod 实例进行连接。

## 快速参考

```bash
runpodctl get pod                    # List pods
runpodctl get pod <id>               # Get pod details
runpodctl start pod <id>             # Start pod
runpodctl stop pod <id>              # Stop pod
runpodctl ssh connect <id>           # Get SSH command
runpodctl send <file>                # Send file to pod
runpodctl receive <code>             # Receive file from pod
```

## 常见操作

### 创建 Pod

```bash
# Without volume
runpodctl create pod --name "my-pod" --gpuType "NVIDIA GeForce RTX 4090" --imageName "runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404"

# With volume (100GB at /workspace)
runpodctl create pod --name "my-pod" --gpuType "NVIDIA GeForce RTX 4090" --imageName "runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404" --volumeSize 100 --volumePath "/workspace"
```

**注意：** 当使用卷（`--volumeSize` 参数）时，务必同时指定 `--volumePath` 参数。如果不指定 `--volumePath`，将会出现问题：
```
error creating container: ... invalid mount config for type "volume": field Target must not be empty
```

### 通过 SSH 连接到 Pod

```bash
# Get SSH command
runpodctl ssh connect <pod_id>

# Connect directly (copy command from above)
ssh -p <port> root@<ip> -i ~/.ssh/runpod_key
```

### 挂载 Pod 的文件系统（使用 SSHFS）

```bash
./scripts/mount_pod.sh <pod_id> [base_dir]
```

默认情况下，文件系统会被挂载到 `~/pods/<pod_id>` 目录下。

**访问文件：**
```bash
ls ~/pods/<pod_id>/
cat ~/pods/<pod_id>/workspace/my-project/train.py
```

**卸载挂载：**
```bash
fusermount -u ~/pods/<pod_id>
```

## 辅助脚本

| 脚本 | 用途 |
|--------|---------|
| `mount_pod.sh` | 通过 SSHFS 挂载 Pod 的文件系统（`runpodctl` 没有相应的命令） |

## Web 服务访问

**代理 URL：**
```
https://<pod_id>-<port>.proxy.runpod.net
```

**常用端口：**
- **8188**：ComfyUI
- **7860**：Gradio
- **8888**：Jupyter
- **8080**：开发工具