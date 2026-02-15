---
name: nodetool
description: **视觉AI工作流构建器：ComfyUI与n8n的结合**  
适用于大型语言模型（LLM）代理、检索-生成（RAG）流程以及多模态数据流的处理。该工具以本地化为核心设计，采用开源许可证（AGPL-3.0）进行发布。  

**主要特点：**  
- **高效集成**：ComfyUI与n8n深度整合，为LLM代理、RAG流程及多模态数据流提供一站式解决方案。  
- **本地优先策略**：强调数据的本地处理能力，提升系统响应速度和稳定性。  
- **开源特性**：遵循AGPL-3.0许可证，鼓励社区贡献与创新。  

**适用场景：**  
- **LLM应用开发**：帮助开发者快速构建基于大型语言模型的应用程序。  
- **检索-生成（RAG）系统**：实现高效的信息检索与内容生成功能。  
- **多模态数据处理**：支持多种数据格式的统一管理和分析。  

**技术优势：**  
- **灵活的配置选项**：提供丰富的配置选项，以满足不同应用场景的需求。  
- **强大的扩展性**：支持插件扩展，便于功能升级与定制。  
- **易用性**：采用直观的用户界面，降低使用门槛。  

**合作伙伴与开发者支持：**  
- **官方文档与社区**：提供详细的官方文档和活跃的开发者社区，确保用户能够快速上手。  

**下载与安装：**  
访问[官方网站](...)下载并安装ComfyUI，了解更多关于该工具的详细信息。
---

# NodeTool

这是一个视觉AI工作流构建工具，它结合了ComfyUI基于节点的灵活性和n8n的自动化能力，允许用户在本地机器上构建大型语言模型（LLM）代理、检索式问答（RAG）管道以及多模态数据流。

## 快速入门

```bash
# See system info
nodetool info

# List workflows
nodetool workflows list

# Run a workflow interactively
nodetool run <workflow_id>

# Start of chat interface
nodetool chat

# Start of web server
nodetool serve
```

## 安装

### Linux / macOS

快速的一行安装命令：

```bash
curl -fsSL https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.sh | bash
```

如果需要指定自定义安装目录：

```bash
curl -fsSL https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.sh | bash --prefix ~/.nodetool
```

**非交互式模式（自动安装，无需提示）：**

这两个安装脚本都支持静默安装：

```bash
# Linux/macOS - use -y
curl -fsSL https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.sh | bash -y

# Windows - use -Yes
irm https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.ps1 | iex; .\install.ps1 -Yes
```

**非交互式模式的特点：**
- 所有确认提示都会被自动跳过
- 安装过程无需用户输入
- 非常适合持续集成/持续部署（CI/CD）管道或自动化设置

### Windows

快速的一行安装命令：

```powershell
irm https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.ps1 | iex
```

如果需要指定自定义安装目录：

```powershell
.\install.ps1 -Prefix "C:\nodetool"
```

**非交互式模式：**

```powershell
.\install.ps1 -Yes
```

## 核心命令

### 工作流

用于管理和执行NodeTool的工作流：

```bash
# List all workflows (user + example)
nodetool workflows list

# Get details for a specific workflow
nodetool workflows get <workflow_id>

# Run workflow by ID
nodetool run <workflow_id>

# Run workflow from file
nodetool run workflow.json

# Run with JSONL output (for automation)
nodetool run <workflow_id> --jsonl
```

### 运行选项

以不同的模式执行工作流：

```bash
# Interactive mode (default) - pretty output
nodetool run workflow_abc123

# JSONL mode - streaming JSON for subprocess use
nodetool run workflow_abc123 --jsonl

# Stdin mode - pipe RunJobRequest JSON
echo '{"workflow_id":"abc","user_id":"1","auth_token":"token","params":{}}' | nodetool run --stdin --jsonl

# With custom user ID
nodetool run workflow_abc123 --user-id "custom_user_id"

# With auth token
nodetool run workflow_abc123 --auth-token "my_auth_token"
```

### 资产

用于管理工作流资产（节点、模型、文件）：

```bash
# List all assets
nodetool assets list

# Get asset details
nodetool assets get <asset_id>
```

### 包

用于管理NodeTool的包（导出工作流、生成文档）：

```bash
# List packages
nodetool package list

# Generate documentation
nodetool package docs

# Generate node documentation
nodetool package node-docs

# Generate workflow documentation (Jekyll)
nodetool package workflow-docs

# Scan directory for nodes and create package
nodetool package scan

# Initialize new package project
nodetool package init
```

### 作业

用于管理后台作业的执行：

```bash
# List jobs for a user
nodetool jobs list

# Get job details
nodetool jobs get <job_id>

# Get job logs
nodetool jobs logs <job_id>

# Start background job for workflow
nodetool jobs start <workflow_id>
```

### 部署

将NodeTool部署到云平台（RunPod、GCP、Docker）：

```bash
# Initialize deployment.yaml
nodetool deploy init

# List deployments
nodetool deploy list

# Add new deployment
nodetool deploy add

# Apply deployment configuration
nodetool deploy apply

# Check deployment status
nodetool deploy status <deployment_name>

# View deployment logs
nodetool deploy logs <deployment_name>

# Destroy deployment
nodetool deploy destroy <deployment_name>

# Manage collections on deployed instance
nodetool deploy collections

# Manage database on deployed instance
nodetool deploy database

# Manage workflows on deployed instance
nodetool deploy workflows

# See what changes will be made
nodetool deploy plan
```

### 模型管理

用于发现和管理AI模型（HuggingFace、Ollama）：

```bash
# List cached HuggingFace models by type
nodetool model list-hf <hf_type>

# List all HuggingFace cache entries
nodetool model list-hf-all

# List supported HF types
nodetool model hf-types

# Inspect HuggingFace cache
nodetool model hf-cache

# Scan cache for info
nodetool admin scan-cache
```

### 管理员

用于维护模型缓存并清理不必要的数据：

```bash
# Calculate total cache size
nodetool admin cache-size

# Delete HuggingFace model from cache
nodetool admin delete-hf <model_name>

# Download HuggingFace models with progress
nodetool admin download-hf <model_name>

# Download Ollama models
nodetool admin download-ollama <model_name>
```

### 聊天与服务器

提供交互式聊天和Web界面：

```bash
# Start CLI chat
nodetool chat

# Start chat server (WebSocket + SSE)
nodetool chat-server

# Start FastAPI backend server
nodetool serve --host 0.0.0.0 --port 8000

# With static assets folder
nodetool serve --static-folder ./static --apps-folder ./apps

# Development mode with auto-reload
nodetool serve --reload

# Production mode
nodetool serve --production
```

### 代理

用于启用基于HTTPS的反向代理：

```bash
# Start proxy server
nodetool proxy

# Check proxy status
nodetool proxy-status

# Validate proxy config
nodetool proxy-validate-config

# Run proxy daemon with ACME HTTP + HTTPS
nodetool proxy-daemon
```

### 其他命令

```bash
# View settings and secrets
nodetool settings show

# Generate custom HTML app for workflow
nodetool vibecoding

# Run workflow and export as Python DSL
nodetool dsl-export

# Export workflow as Gradio app
nodetool gradio-export

# Regenerate DSL
nodetool codegen

# Manage database migrations
nodetool migrations

# Synchronize database with remote
nodetool sync
```

## 使用场景

### 工作流执行

运行NodeTool工作流并获取结构化的输出：

```bash
# Run workflow interactively
nodetool run my_workflow_id

# Run and stream JSONL output
nodetool run my_workflow_id --jsonl | jq -r '.[] | "\(.status) | \(.output)"'
```

### 包创建

为自定义包生成文档：

```bash
# Scan for nodes and create package
nodetool package scan

# Generate complete documentation
nodetool package docs
```

### 部署

将NodeTool实例部署到云端：

```bash
# Initialize deployment config
nodetool deploy init

# Add RunPod deployment
nodetool deploy add

# Deploy and start
nodetool deploy apply
```

### 模型管理

检查和管理缓存的AI模型：

```bash
# List all available models
nodetool model list-hf-all

# Inspect cache
nodetool model hf-cache
```

## 安装

### Linux / macOS

快速的一行安装命令：

```bash
curl -fsSL https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.sh | bash
```

如果需要指定自定义安装目录：

```bash
curl -fsSL https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.sh | bash --prefix ~/.nodetool
```

**非交互式模式（自动安装，无需提示）：**

这两个安装脚本都支持静默安装：

```bash
# Linux/macOS - use -y
curl -fsSL https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.sh | bash -y

# Windows - use -Yes
irm https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.ps1 | iex; .\install.ps1 -Yes
```

**非交互式模式的特点：**
- 所有确认提示都会被自动跳过
- 安装过程无需用户输入
- 非常适合持续集成/持续部署（CI/CD）管道或自动化设置

### Windows

快速的一行安装命令：

```powershell
irm https://raw.githubusercontent.com/nodetool-ai/nodetool/refs/heads/main/install.ps1 | iex
```

如果需要指定自定义安装目录：

```powershell
.\install.ps1 -Prefix "C:\nodetool"
```

**非交互式模式：**

```powershell
.\install.ps1 -Yes
```

## 安装内容

安装程序会设置以下内容：
- **micromamba** — Python包管理器（conda的替代品）
- **NodeTool环境** — 在`~/.nodetool/env`中创建Conda环境
- **Python包** — 从NodeTool注册表中安装`nodetool-core`和`nodetool-base`
- **封装脚本** — 用户可以从任何终端使用`nodetool`命令行工具

### 环境配置

安装完成后，以下变量会自动配置：

```bash
# Conda environment
export MAMBA_ROOT_PREFIX="$HOME/.nodetool/micromamba"
export PATH="$HOME/.nodetool/env/bin:$HOME/.nodetool/env/Library/bin:$PATH"

# Model cache directories
export HF_HOME="$HOME/.nodetool/cache/huggingface"
export OLLAMA_MODELS="$HOME/.nodetool/cache/ollama"
```

## 系统信息

用于查看NodeTool环境和已安装的包：

```bash
nodetool info
```

输出信息包括：
- NodeTool版本
- Python版本
- 平台/架构
- 已安装的AI模型（OpenAI、Anthropic、Google、HuggingFace、Ollama、fal-client）
- 环境变量
- API密钥的状态