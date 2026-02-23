# 将应用程序部署到 SupplyWhy 开发服务器

使用 SSH 和 kubectl 将应用程序部署到 SupplyWhy 开发环境的 EC2 服务器上。

## 指导步骤

请按顺序执行以下步骤。**在继续下一步之前，请确保每一步都成功完成。**

### 第一步：将 SSH 密钥添加到代理（Agent）

运行以下命令以添加 SSH 密钥：

```bash
ssh-add ~/.ssh/supplywhy-dev-key.pem
```

**验证：**命令应输出 `Identity added: ~/.ssh/supplywhy-dev-key.pem` 或类似的内容。如果看到 “Could not open a connection to your authentication agent”，则说明 ssh-agent 可能没有运行；如果看到 “No such file or directory”，则表示密钥文件缺失。

**如果发生以下情况，请停止并通知用户：**密钥无法添加。

### 第二步：测试 SSH 连接

在部署之前，验证 SSH 连接是否正常：

```bash
ssh supplywhy-dev-master "echo 'SSH connection successful'"
```

**验证：**应输出 “SSH connection successful”。如果出现连接超时、权限被拒绝或主机未找到等错误，说明 SSH 连接失败。

**如果发生以下情况，请停止并通知用户：**SSH 连接失败。

### 第三步：更新镜像标签（Image Tag）

如果提供了 `IMAGE_TAG` 参数（`$ARGUMENTS`），请使用新的标签更新 `deployment.yaml` 文件：

```bash
ssh supplywhy-dev-master "sed -i 's|590183820143.dkr.ecr.us-west-2.amazonaws.com/genie:.*|590183820143.dkr.ecr.us-west-2.amazonaws.com/genie:$ARGUMENTS|' genie/deployment.yaml"
```

**验证：**快速检查以确保标签已更新：

```bash
ssh supplywhy-dev-master "grep 'image:' genie/deployment.yaml"
```

输出应显示您提供的新标签。

**如果未提供 `IMAGE_TAG` 参数（使用现有标签进行部署），则跳过此步骤。**

**如果 `sed` 命令失败，请停止并通知用户：**

### 第四步：通过 kubectl 进行部署

通过 SSH 连接到 EC2 服务器，然后运行 `kubectl deployment` 命令：

```bash
ssh supplywhy-dev-master "cd genie && kubectl apply -f deployment.yaml"
```

**验证：**kubectl 的输出应显示资源正在被 “created”（创建）、“configured”（配置）或 “unchanged”（保持不变）。请查看如下内容：
- `deployment.apps/xxx configured`
- `service/xxx unchanged`

**如果发生以下情况，请停止并通知用户：**
- `kubectl` 返回错误（例如 “error: the path does not exist” 或 “connection refused”）
- 任何资源的状态显示为 “error”

### 第五步：验证部署状态

应用更改后，检查部署是否成功进行：

```bash
ssh supplywhy-dev-master "kubectl rollout status deployment -n default --timeout=60s"
```

**验证：**对于成功的部署，应显示 “successfully rolled out”。如果出现超时或错误，说明部署过程中可能存在问题。

**通知用户：**所有部署的最终状态（无论成功还是失败）。

## 成功标准

当满足以下条件时，部署视为成功：
1. SSH 密钥已成功添加
2. 与服务器的 SSH 连接正常
3. 镜像标签已更新（如果提供了参数）
4. `kubectl apply` 命令执行成功且无错误
5. 部署状态显示为成功

## 故障排除

如果部署在任何步骤中失败，请尝试以下方法进行排查：
1. **SSH 密钥问题：**检查 `~/.ssh/supplywhy-dev-key.pem` 文件是否存在，并确保其权限设置为 600。
2. **SSH 连接问题：**检查网络访问权限以及您的 IP 地址是否被安全组允许访问。
3. **`kubectl apply` 错误：**确认 `deployment.yaml` 文件存在于服务器上的 `genie` 文件夹中。
4. **部署失败：**使用 `kubectl logs` 查看 Pod 日志，或使用 `kubectl describe deployment` 查看部署详情。