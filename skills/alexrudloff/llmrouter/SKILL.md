---
name: llmrouter
description: 这款智能大型语言模型（LLM）代理可以根据任务的复杂性将请求路由到相应的模型。对于简单任务，它会使用成本更低的模型来节省成本。该代理已通过Anthropic、OpenAI、Gemini、Kimi/Moonshot和Ollama等模型进行了测试。
homepage: https://github.com/alexrudloff/llmrouter
metadata: {"openclaw":{"emoji":"🔀","homepage":"https://github.com/alexrudloff/llmrouter","os":["darwin","linux"],"requires":{"bins":["python3"],"anyBins":["pip","pip3"]},"primaryEnv":"ANTHROPIC_API_KEY"}}
---

# LLM Router

这是一个智能代理，它根据请求的复杂性对请求进行分类，并将它们路由到相应的LLM（大型语言模型）。对于简单的任务，它会使用成本较低、运行速度较快的模型；而对于复杂的任务，则会使用成本较高的模型。

**该代理与[OpenClaw](https://github.com/openclaw/openclaw)配合使用**，通过将简单请求路由到较小的模型来减少令牌的使用量和API费用。

**测试情况：**已与Anthropic、OpenAI、Google Gemini、Kimi/Moonshot和Ollama进行了兼容性测试。

## 快速入门

### 先决条件

1. **Python 3.10及以上版本**，并安装了pip
2. **Ollama**（可选——仅在使用本地分类功能时需要）
3. **Anthropic API密钥**或Claude Code OAuth令牌（或其他提供商的密钥）

### 安装

```bash
# Clone if not already present
git clone https://github.com/alexrudloff/llmrouter.git
cd llmrouter

# Create virtual environment (required on modern Python)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Pull classifier model (if using local classification)
ollama pull qwen2.5:3b

# Copy and customize config
cp config.yaml.example config.yaml
# Edit config.yaml with your API key and model preferences
```

### 验证安装

```bash
# Start the server
source venv/bin/activate
python server.py

# In another terminal, test health endpoint
curl http://localhost:4001/health
# Should return: {"status": "ok", ...}
```

### 启动服务器

```bash
python server.py
```

**参数说明：**
- `--port PORT`：监听的端口（默认：4001）
- `--host HOST`：绑定的主机（默认：127.0.0.1）
- `--config PATH`：配置文件路径（默认：config.yaml）
- `--log`：启用详细日志记录
- `--openclaw`：启用OpenClaw兼容性（会在系统提示中显示模型的实际名称）

## 配置

请编辑`config.yaml`文件以自定义配置：

### 模型路由

```yaml
# Anthropic routing
models:
  super_easy: "anthropic:claude-haiku-4-5-20251001"
  easy: "anthropic:claude-haiku-4-5-20251001"
  medium: "anthropic:claude-sonnet-4-20250514"
  hard: "anthropic:claude-opus-4-20250514"
  super_hard: "anthropic:claude-opus-4-20250514"

# OpenAI routing
models:
  super_easy: "openai:gpt-4o-mini"
  easy: "openai:gpt-4o-mini"
  medium: "openai:gpt-4o"
  hard: "openai:o3-mini"
  super_hard: "openai:o3"

# Google Gemini routing
models:
  super_easy: "google:gemini-2.0-flash"
  easy: "google:gemini-2.0-flash"
  medium: "google:gemini-2.0-flash"
  hard: "google:gemini-2.0-flash"
  super_hard: "google:gemini-2.0-flash"
```

**注意：**推理模型会自动被检测到，并使用正确的API参数。

### 分类器

有三种方式用于分类请求的复杂性：

- **本地模式（默认）**：免费，但需要安装Ollama：
```yaml
classifier:
  provider: "local"
  model: "qwen2.5:3b"
```

- **Anthropic**：使用Haiku模型，速度快且成本低：
```yaml
classifier:
  provider: "anthropic"
  model: "claude-haiku-4-5-20251001"
```

- **OpenAI**：使用GPT-4o-mini模型：
```yaml
classifier:
  provider: "openai"
  model: "gpt-4o-mini"
```

- **Google**：使用Gemini模型：
```yaml
classifier:
  provider: "google"
  model: "gemini-2.0-flash"
```

- **Kimi**：使用Moonshot模型：
```yaml
classifier:
  provider: "kimi"
  model: "moonshot-v1-8k"
```

如果您的机器无法运行本地模型，可以选择使用远程模型（anthropic/openai/google/kimi）。

### 支持的提供商

- `anthropic:claude-*`：Anthropic的Claude模型（已测试）
- `openai:gpt-*`, `openai:o1-*`, `openai:o3-*`：OpenAI的模型（已测试）
- `google:gemini-*`：Google的Gemini模型（已测试）
- `kimi:kimi-k2.5`, `kimi:moonshot-*`：Kimi/Moonshot的模型（已测试）
- `local:model-name`：本地的Ollama模型（已测试）

## 复杂性等级

| 等级 | 使用场景 | 默认模型 |
|-------|----------|---------------|
| super_easy | 问候语、确认信息 | Haiku |
| easy | 简单的问答、提醒 | Haiku |
| medium | 编程、邮件处理、研究 | Sonnet |
| hard | 复杂的推理、调试 | Opus |
| super_hard | 系统架构设计、证明 | Opus |

## 自定义分类规则

请编辑`ROUTES.md`文件以调整消息的分类方式。分类器会读取该文件中的规则来确定请求的复杂性等级。

## API使用

该代理提供了与OpenAI兼容的API接口：

```bash
curl http://localhost:4001/v1/chat/completions \
  -H "Authorization: Bearer $ANTHROPIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llm-router",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## 分类测试

```bash
python classifier.py "Write a Python sort function"
# Output: medium

python classifier.py --test
# Runs test suite
```

## 作为macOS服务运行

请创建`~/Library/LaunchAgents/com.llmrouter.plist`文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.llmrouter</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/llmrouter/venv/bin/python</string>
        <string>/path/to/llmrouter/server.py</string>
        <string>--openclaw</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/path/to/llmrouter</string>
    <key>StandardOutPath</key>
    <string>/path/to/llmrouter/logs/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/llmrouter/logs/stderr.log</string>
</dict>
</plist>
```

**重要提示：**请将`/path/to/llmrouter`替换为实际的安装路径。必须使用虚拟环境（venv）中的Python，而不是系统自带的Python。

```bash
# Create logs directory
mkdir -p ~/path/to/llmrouter/logs

# Load the service
launchctl load ~/Library/LaunchAgents/com.llmrouter.plist

# Verify it's running
curl http://localhost:4001/health

# To stop/restart
launchctl unload ~/Library/LaunchAgents/com.llmrouter.plist
launchctl load ~/Library/LaunchAgents/com.llmrouter.plist
```

## OpenClaw配置

请在`~/.openclaw/openclaw.json`文件中将该代理添加为可用提供商：

```json
{
  "models": {
    "providers": {
      "localrouter": {
        "baseUrl": "http://localhost:4001/v1",
        "apiKey": "via-router",
        "api": "openai-completions",
        "models": [
          {
            "id": "llm-router",
            "name": "LLM Router (Auto-routes by complexity)",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

**注意：**由于实际费用取决于代理选择的模型，因此此处将费用设置为0。代理会记录每个请求所使用的模型。

### 设置为默认模型（可选）

若希望所有代理默认使用该代理，请进行以下设置：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "localrouter/llm-router"
      }
    }
  }
}
```

## 使用OAuth令牌

如果`config.yaml`文件中使用了来自OpenClaw的Anthropic OAuth令牌（位于`~/.openclaw/auth-profiles.json`文件中），该代理会自动处理Claude Code身份验证相关的头部信息。

### OpenClaw兼容模式（必需）

**如果与OpenClaw一起使用，请务必使用`--openclaw`参数启动服务器：**

```bash
python server.py --openclaw
```

此参数启用以下OpenClaw所需的兼容性功能：
- 在响应中显示实际使用的模型名称
- 正确处理工具名称和ID的映射，以确保请求能够正确路由

如果不使用此参数，使用该代理时可能会出现错误。

## 常见操作

- **检查服务器状态**：`curl http://localhost:4001/health`
- **查看当前配置**：`cat config.yaml`
- **测试分类功能**：`python classifier.py "your message"`
- **运行分类测试**：`python classifier.py --test`
- **重启服务器**：先停止服务器，然后再次运行`python server.py`
- **查看日志**（如果作为服务运行）：`tail -f logs/stdout.log`

## 故障排除

- **“externally-managed-environment”错误**：Python 3.11及以上版本需要虚拟环境。请创建一个虚拟环境。
- **端口4001连接失败**：请确保服务器正在运行。
- **分类结果错误**：请编辑`ROUTES.md`文件以调整分类规则。分类器会依据该文件中的规则来确定请求的复杂性。
- **Ollama相关错误/“模型未找到”**：请确保Ollama正在运行，并且模型已正确加载。
- **OAuth令牌无法使用**：请确认`config.yaml`文件中的令牌以`sk-ant-oat`开头。该代理会自动检测OAuth令牌并添加必要的身份验证头部信息。
- **LaunchAgent无法启动**：请检查日志，并确保路径路径是绝对路径。