---
name: mirage-proxy
description: 安装并配置 `mirage-proxy`，作为 OpenClaw LLM API 调用的透明 PII（个人身份信息）/ secrets（机密信息）过滤工具。该工具支持二进制安装、配置代理提供商、自动重启功能，并能实现多模型数据的路由处理。
---
# OpenClaw 的 mirage-proxy

mirage-proxy 是一个用于在 OpenClaw 与大型语言模型（LLM）提供商之间实现透明数据传输的中间件。它能够将敏感数据替换为看似合理的伪造数据，从而确保 LLM 模型无法获取到用户的真实信息。

GitHub: https://github.com/chandika/mirage-proxy

## 快速安装

运行自带的安装脚本：

```bash
bash ~/.openclaw/workspace/skills/mirage-proxy/setup.sh
```

该脚本会下载二进制文件，创建一个自动重启的代理服务，并验证其是否正常运行。

卸载方法：`bash ~/.openclaw/workspace/skills/mirage-proxy/setup.sh --uninstall`

## 配置 OpenClaw 提供商

安装成功后，请修改 OpenClaw 的配置文件。保留原有的提供商配置，同时添加 mirage-proxy 的配置选项，以便在需要时立即切换到 mirage-proxy：

```json5
{
  "models": {
    "mode": "merge",
    "providers": {
      "mirage-anthropic": {
        "baseUrl": "http://127.0.0.1:8686/anthropic",
        "api": "anthropic-messages",
        "apiKey": "${ANTHROPIC_API_KEY}",
        "models": [
          { "id": "claude-opus-4-6", "name": "Claude Opus 4.6 (mirage)", "api": "anthropic-messages", "reasoning": true, "input": ["text", "image"], "cost": {"input":0,"output":0,"cacheRead":0,"cacheWrite":0}, "contextWindow": 200000, "maxTokens": 32000 },
          { "id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6 (mirage)", "api": "anthropic-messages", "reasoning": true, "input": ["text", "image"], "cost": {"input":0,"output":0,"cacheRead":0,"cacheWrite":0}, "contextWindow": 200000, "maxTokens": 16000 },
          { "id": "claude-haiku-3-6", "name": "Claude Haiku 3.6 (mirage)", "api": "anthropic-messages", "reasoning": false, "input": ["text", "image"], "cost": {"input":0,"output":0,"cacheRead":0,"cacheWrite":0}, "contextWindow": 200000, "maxTokens": 8192 }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "models": {
        "anthropic/claude-opus-4-6": { "alias": "anthropic-opus" },
        "anthropic/claude-sonnet-4-6": { "alias": "anthropic-sonnet" },
        "anthropic/claude-haiku-3-6": { "alias": "anthropic-haiku" },
        "mirage-anthropic/claude-opus-4-6": { "alias": "mirage-opus" },
        "mirage-anthropic/claude-sonnet-4-6": { "alias": "mirage-sonnet" },
        "mirage-anthropic/claude-haiku-3-6": { "alias": "mirage-haiku" }
      }
    }
  }
}
```

### OpenAI / Codex（基于 OAuth 的提供商）

对于不使用 API 密钥的环境变量（即基于 OAuth 的提供商），请直接覆盖 OpenClaw 内置的提供商配置中的 `baseUrl`，而无需创建自定义提供商：

```json5
{
  "models": {
    "mode": "merge",
    "providers": {
      "openai-codex": {
        "baseUrl": "http://127.0.0.1:8686"
      }
    }
  }
}
```

**注意：** 除非容器环境中确实存在 `OPENAI_API_KEY` 环境变量，否则切勿在自定义提供商配置中添加 `"apiKey": "${OPENAI_API_KEY}"`，否则 OpenClaw 在启动时可能会崩溃。

## 模型别名

配置完成后，可以使用 `/model` 参数来切换不同的模型：

| 别名 | 路由 |
|---|---|
| `anthropic-opus` | 直接连接到 Anthropic 模型 |
| `mirage-opus` | 通过 mirage-proxy 中转后连接到 Anthropic 模型 |
| `anthropic-sonnet` | 直接连接到 Anthropic 模型 |
| `mirage-sonnet` | 通过 mirage 中转后连接到 Anthropic 模型 |
| `codex` | 直接连接到 OpenAI 模型（或根据 `baseUrl` 的配置进行中转） |

## 数据持久化

mirage-proxy 会在 OpenClaw 重启时被关闭。有两种解决方案：

**推荐方案：使用 Docker 入口点：**
```yaml
# docker-compose.yml
command: sh -c "nohup /home/node/.openclaw/workspace/start-mirage.sh > /dev/null 2>&1 & exec openclaw start"
```

**备用方案：使用心跳检测机制：**
在 `HEARTBEAT.md` 文件中添加以下代码：
```
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8686/
```
如果检测到错误（如连接失败）或心跳检测失败，通过 `start-mirage.sh` 命令重启 mirage-proxy：

## 验证配置是否正确

```bash
# Proxy running?
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8686/
# Expect 502 (up, no path matched)

# Check redaction stats
tail -20 ~/.openclaw/workspace/mirage-proxy.log
# Look for: 🛡️ SECRET (AWS Access Key) [40 chars] → AKIA••••
```