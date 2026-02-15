---
name: azure-proxy
description: 通过一个轻量级的本地代理来启用 OpenClaw 与 Azure OpenAI 的集成。当您将 Azure OpenAI 配置为模型提供者时，或者在 OpenClaw 中遇到与 Azure OpenAI 相关的 404 错误时，或者需要使用 Azure 信用（例如 Visual Studio 订阅）来支持 OpenClaw 的子代理时，都可以使用此方法。该方法解决了由于 `api-version` 查询参数问题而导致的直接集成失败的问题。
---

# Azure OpenAI 代理（用于 OpenClaw）

这是一个轻量级的 Node.js 代理，用于连接 Azure OpenAI 和 OpenClaw。

## 问题

OpenClaw 构建的 API URL 的格式如下：
```javascript
const endpoint = `${baseUrl}/chat/completions`;
```

而 Azure OpenAI 的要求是：
```
https://{resource}.openai.azure.com/openai/deployments/{model}/chat/completions?api-version=2025-01-01-preview
```

当 `api-version` 被包含在 `baseUrl` 中时，OpenClaw 的路径处理机制会导致该 URL 无法正确解析。

## 快速设置

### 1. 配置并运行代理

```bash
# Set your Azure details
export AZURE_OPENAI_ENDPOINT="your-resource.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"
export AZURE_OPENAI_API_VERSION="2025-01-01-preview"

# Run the proxy
node scripts/server.js
```

### 2. 配置 OpenClaw 提供者

在 `~/.openclaw/openclaw.json` 文件中添加以下配置：
```json
{
  "models": {
    "providers": {
      "azure-gpt4o": {
        "baseUrl": "http://127.0.0.1:18790",
        "apiKey": "YOUR_AZURE_API_KEY",
        "api": "openai-completions",
        "authHeader": false,
        "headers": {
          "api-key": "YOUR_AZURE_API_KEY"
        },
        "models": [
          { "id": "gpt-4o", "name": "GPT-4o (Azure)" }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "models": {
        "azure-gpt4o/gpt-4o": {}
      }
    }
  }
}
```

**注意：** 将 `authHeader` 设置为 `false` — Azure 使用的是 `api-key` 头部信息，而不是 Bearer 令牌。

### 3. （可选）用于子代理（Subagents）

通过将自动化任务路由到 Azure 来节省 Azure 资源：

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": "azure-gpt4o/gpt-4o"
      }
    }
  }
}
```

## 作为 systemd 服务运行

复制模板并进行相应配置：

```bash
mkdir -p ~/.config/systemd/user
cp scripts/azure-proxy.service ~/.config/systemd/user/

# Edit the service file with your Azure details
nano ~/.config/systemd/user/azure-proxy.service

# Enable and start
systemctl --user daemon-reload
systemctl --user enable azure-proxy
systemctl --user start azure-proxy
```

## 环境变量

| 变量          | 默认值        | 描述                          |
|----------------|-------------|---------------------------------------------|
| `AZURE_PROXY_PORT`   | `18790`       | 本地代理端口                          |
| `AZURE_PROXY_BIND`    | `127.0.0.1`     | 代理绑定地址                        |
| `AZURE_OPENAI_ENDPOINT` | —           | Azure 资源主机名                        |
| `AZURE_OPENAI_DEPLOYMENT` | `gpt-4o`       | 部署名称                          |
| `AZURE_OPENAI_API_VERSION` | `2025-01-01-preview` | API 版本                          |

## 健康检查

```bash
curl http://localhost:18790/health
# {"status":"ok","deployment":"gpt-4o"}
```

## 故障排除

- **404 资源未找到：** 确认端点主机名和部署名称与 Azure 门户中的信息一致。
- **401 未经授权：** API 密钥错误或已过期。
- **内容过滤错误：** Azure 有严格的内容过滤机制，某些在 OpenAI 上可以正常使用的请求可能会被阻止。