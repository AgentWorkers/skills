---
name: nginx-config-creator
description: "创建一个标准的 Nginx/OpenResty 反向代理配置文件，并重新加载 Web 服务器。该配置文件包含安全检查功能以及对环境变量的支持。主要参数包括服务名称、域名和端口号。"
metadata:
  openclaw:
    requires:
      bins: ["bash", "docker"]
---

# Nginx 配置生成器（企业级）

该技能可自动生成 Nginx/OpenResty 反向代理配置文件，兼具易用性和安全性，支持环境变量配置，并内置了关键的安全检查机制。

## 主要功能

- **环境变量支持**：通过读取环境变量来简化配置命令的编写过程。
- **安全检查**：内置“熔断”（熔断器）机制，在应用配置之前会先对其进行测试；如果测试失败，系统会自动回滚配置，从而避免导致 Web 服务器停机。

## 建议的先决条件

为确保最佳使用体验，建议在主机系统上设置以下环境变量：

- `NGINX_CONFIG_PATH`：Nginx 的 `conf.d` 目录的绝对路径。
- `NGINX_CONTAINER_NAME`：正在运行的 Nginx/OpenResty Docker 容器的名称。

如果这些环境变量未设置，则必须通过命令行参数提供。

## 核心脚本：`scripts/create-and-reload.sh`

该脚本负责完成整个配置生成过程。

### **命令行参数**

- `--service-name`：（必选）服务的简称（例如：`grafana`）。
- `--domain`：（必选）服务的根域名（例如：`example.com`）。
- `--port`：（必选）服务运行的本地端口（例如：`3000`）。
- `--config-path`：（可选）Nginx 的 `conf.d` 目录路径。该参数会覆盖 `NGINX_CONFIG_PATH` 环境变量的设置。
- `--container-name`：（可选）Nginx Docker 容器的名称。该参数会覆盖 `NGINX_CONTAINER_NAME` 环境变量的设置。

### **输出结果**

- **成功时**：会打印详细的操作步骤及成功信息。
- **失败时**：会向标准错误输出（stderr）显示详细的错误信息并退出。如果在配置测试过程中出现错误，还会显示 `nginx -t` 命令的输出结果。

### **执行流程**

1. **解析参数与环境变量**：脚本从命令行参数和环境变量中获取所有必要的路径和名称。
2. **生成配置文件**：在目标目录中创建 `.conf` 文件。
3. **测试配置**：在指定的 Docker 容器内执行 `nginx -t` 命令进行配置验证。
4. **根据测试结果采取相应操作**：
    - 如果测试通过，脚本会通过 `nginx -s reload` 命令重新加载 Nginx 服务。
    - 如果测试失败，脚本会自动删除生成的配置文件并报告错误。
5. **反馈结果**：向用户显示最终的配置生成结果。

### **使用示例**

**场景 1：环境变量已预先设置**

```bash
# Set for future convenience
export NGINX_CONFIG_PATH="/path/to/your/nginx/conf.d"
export NGINX_CONTAINER_NAME="your_nginx_container"

# Now, the command is very simple:
bash skills/nginx-config-creator/scripts/create-and-reload.sh \
  --service-name "grafana" \
  --domain "example.com" \
  --port "3000"
```

**场景 2：未使用环境变量（所有信息均通过命令行参数提供）**

```bash
bash skills/nginx-config-creator/scripts/create-and-reload.sh \
  --service-name "grafana" \
  --domain "example.com" \
  --port "3000" \
  --config-path "/path/to/your/nginx/conf.d" \
  --container-name "your_nginx_container"
```

### **错误处理策略**

- **缺少参数**：如果缺少必要的参数或环境变量，脚本会立即退出并显示错误信息。
- **`nginx -t` 命令失败**：该工具具有安全性设计，不会尝试重新加载有问题的配置文件。它会自动清理错误并显示具体的错误信息，确保在线运行的 Web 服务器不会受到影响。