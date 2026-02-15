---
name: docker-sandbox
description: 创建并管理基于 Docker 的沙箱化虚拟机环境，以确保代理程序的安全执行。适用于运行不受信任的代码、探索软件包或隔离代理工作负载的场景。该环境支持 Claude、Codex、Copilot、Gemini 和 Kiro 等代理程序，并提供了网络代理控制功能。
metadata: {"clawdbot":{"emoji":"🐳","requires":{"bins":["docker"]},"primaryEnv":"","homepage":"https://docs.docker.com/desktop/features/sandbox/","os":["linux","darwin","win32"]}}
---

# Docker沙箱

使用Docker Desktop的沙箱功能，在**隔离的虚拟机环境中**运行代理程序和命令。每个沙箱都拥有自己的轻量级虚拟机，具备文件系统隔离、网络代理控制以及通过virtiofs挂载的工作区功能。

## 使用场景

- 在全局安装之前，探索**不可信的软件包**或相关技术
- 安全地运行来自外部来源的**任意代码**
- 在不危及主机系统的情况下测试**可能造成破坏的操作**
- 隔离需要网络访问控制的**代理工作负载**
- 为实验创建**可复现的环境**

## 系统要求

- Docker Desktop 4.49及以上版本，并安装了`docker sandbox`插件
- 需要验证Docker沙箱的版本信息

## 快速入门

### 为当前项目创建沙箱

```bash
docker sandbox create --name my-sandbox claude .
```

此操作会创建一个虚拟机隔离的沙箱环境：
- 通过virtiofs将当前目录挂载到沙箱中
- 预先安装了Node.js、git和标准开发工具
- 配置了具有允许列表控制功能的网络代理

### 在沙箱内运行命令

```bash
docker sandbox exec my-sandbox node --version
docker sandbox exec my-sandbox npm install -g some-package
docker sandbox exec -w /path/to/workspace my-sandbox bash -c "ls -la"
```

### 直接运行代理程序

```bash
# Create and run in one step
docker sandbox run claude . -- -p "What files are in this project?"

# Run with agent arguments after --
docker sandbox run my-sandbox -- -p "Analyze this codebase"
```

## 命令参考

### 沙箱的生命周期

```bash
# Create a sandbox (agents: claude, codex, copilot, gemini, kiro, cagent)
docker sandbox create --name <name> <agent> <workspace-path>

# Run an agent in sandbox (creates if needed)
docker sandbox run <agent> <workspace> [-- <agent-args>...]
docker sandbox run <existing-sandbox> [-- <agent-args>...]

# Execute a command
docker sandbox exec [options] <sandbox> <command> [args...]
  -e KEY=VAL          # Set environment variable
  -w /path            # Set working directory
  -d                  # Detach (background)
  -i                  # Interactive (keep stdin open)
  -t                  # Allocate pseudo-TTY

# Stop without removing
docker sandbox stop <sandbox>

# Remove (destroys VM)
docker sandbox rm <sandbox>

# List all sandboxes
docker sandbox ls

# Reset all sandboxes
docker sandbox reset

# Save snapshot as reusable template
docker sandbox save <sandbox>
```

### 网络控制

沙箱内置了网络代理，用于控制出站网络访问。

```bash
# Allow specific domains
docker sandbox network proxy <sandbox> --allow-host example.com
docker sandbox network proxy <sandbox> --allow-host api.github.com

# Block specific domains
docker sandbox network proxy <sandbox> --block-host malicious.com

# Block IP ranges
docker sandbox network proxy <sandbox> --block-cidr 10.0.0.0/8

# Bypass proxy for specific hosts (direct connection)
docker sandbox network proxy <sandbox> --bypass-host localhost

# Set default policy (allow or deny all by default)
docker sandbox network proxy <sandbox> --policy deny  # Block everything, then allowlist
docker sandbox network proxy <sandbox> --policy allow  # Allow everything, then blocklist

# View network activity
docker sandbox network log <sandbox>
```

### 自定义模板

```bash
# Use a custom container image as base
docker sandbox create --template my-custom-image:latest claude .

# Save current sandbox state as template for reuse
docker sandbox save my-sandbox
```

## 工作区挂载

主机上的工作区路径会通过virtiofs挂载到沙箱中。沙箱内的路径结构与主机保持一致：

| 主机操作系统 | 主机路径 | 沙箱路径 |
|---|---|---|
| Windows | `H:\Projects\my-app` | `/h/Projects/my-app` |
| macOS | `/Users/me/projects/my-app` | `/Users/me/projects/my-app` |
| Linux | `/home/me/projects/my-app` | `/home/me/projects/my-app` |

代理程序的根目录为`/home/agent/`，其中包含一个链接到`workspace/`的目录。

## 沙箱内的环境配置

每个沙箱虚拟机都包含以下软件：
- **Node.js**（v20.x LTS）
- **Git**（最新版本）
- **Python**（系统默认安装）
- **curl**、**wget**等标准Linux工具
- **npm**（全局安装目录位于`/usr/local/share/npm-global/`）
- **Docker套接字**（位于`/run/docker.sock`，支持Docker-in-Docker功能）

### 代理配置（自动设置）

```
HTTP_PROXY=http://host.docker.internal:3128
HTTPS_PROXY=http://host.docker.internal:3128
NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/proxy-ca.crt
SSL_CERT_FILE=/usr/local/share/ca-certificates/proxy-ca.crt
```

**注意**：Node.js的`fetch`函数默认不尊重`HTTP_PROXY`环境变量。对于使用`fetch`的npm包，需要创建一个`require`钩子来设置代理：

```javascript
// /tmp/proxy-fix.js
const proxy = process.env.HTTPS_PROXY || process.env.HTTP_PROXY;
if (proxy) {
  const { ProxyAgent } = require('undici');
  const agent = new ProxyAgent(proxy);
  const origFetch = globalThis.fetch;
  globalThis.fetch = function(url, opts = {}) {
    return origFetch(url, { ...opts, dispatcher: agent });
  };
}
```

使用以下命令运行脚本：`node -r /tmp/proxy-fix.js your-script.js`

## 常见问题解决方法

### “客户端版本太旧”
请将Docker Desktop升级到4.49及以上版本。沙箱插件要求Docker引擎API版本达到v1.44或更高。

### 沙箱内“fetch操作失败”
Node.js的`fetch`函数不使用代理设置。请使用上述的`proxy-fix.js`钩子，或改用`curl`来发送请求：

```bash
docker sandbox exec my-sandbox curl -sL https://api.example.com/data
```

### Windows（Git Bash / MSYS2）下的路径转换
Git Bash会将路径`/path`转换为`C:/Program Files/Git/path`。在命令前添加相应的路径前缀：

```bash
MSYS_NO_PATHCONV=1 docker sandbox exec my-sandbox ls /home/agent
```

### 更新Docker后沙箱无法启动
```bash
docker sandbox reset  # Clears all sandbox state
```