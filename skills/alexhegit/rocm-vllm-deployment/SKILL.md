---
name: rocm_vllm_deployment
description: 在 AMD ROCm GPU 上部署可用于生产环境的 vLLM（大语言模型）。该部署方案集成了环境自动检查、模型参数检测、Docker Compose 部署、健康状态验证以及功能测试等功能，并采用了全面的日志记录和安全最佳实践。
version: 1.0.0
author: Alex He <heye_dev@163.com>
timeout: 3600s
platform: Linux (AMD GPU ROCm)
tags:
  - LLM
  - Deployment
  - AMD
  - ROCm
  - Docker Compose
  - vLLM
  - Automation
  - EnvCheck
  - AutoRepair
---
# ROCm vLLM 部署技能

这是一套专为在 AMD ROCm GPU 上使用 Docker Compose 部署 vLLM 推理服务而设计的自动化方案，适用于生产环境。

## 特点

- **环境自动检查**：检测并修复缺失的依赖项。
- **模型参数检测**：自动读取 config.json 文件以获取最佳配置。
- **显存估算**：在部署前计算所需内存。
- **安全令牌处理**：从不将令牌写入 compose 文件。
- **结构化输出**：所有日志和测试结果按模型分别保存。
- **部署报告**：为每次部署生成易于阅读的摘要。
- **健康状态验证**：自动进行健康检查和功能测试。
- **故障排除指南**：提供常见问题及解决方法。

## 环境前提条件

**推荐（适用于生产环境）：** 将以下内容添加到 `~/.bash_profile` 中：

```bash
# HuggingFace authentication token (required for gated models)
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Model cache directory (optional)
export HF_HOME="$HOME/models"

# Apply changes
source ~/.bash_profile
```

**测试时不需要**：即使未设置这些环境变量，技能也能正常运行：
- **HF_TOKEN**：可选——公共模型无需此令牌；受限制的模型在下载时会因令牌问题而失败。
- **HF_HOME**：可选——默认值为 `/root/.cache/huggingface/hub`。

### 环境变量检测

**优先级顺序：**
1. **显式参数**（最高优先级）：在任务或请求中提供的参数（例如，`hf_token: "xxx"`）。
2. **环境变量**：已在 shell 中设置或来自父进程的环境变量。
3. **~/.bash_profile**：用于加载环境变量的配置文件。
4. **默认值**（最低优先级）：`HF_HOME` 的默认值为 `/root/.cache/huggingface/hub`。

| 变量 | 是否必需 | 如果缺失 |
|----------|----------|------------|
| `HF_TOKEN` | **条件性必需** | 不提供令牌时仍可继续（公共模型可用；受限制的模型在下载时会因令牌问题而失败） |
| `HF_HOME` | 不必需 | **警告 + 默认值** | 使用 `/root/.cache/huggingface/hub` |

**原则：** 配置错误导致立即失败；认证错误在下载时失败。

---

## 辅助脚本

**位置：** `<skill-dir>/scripts/`

### check-env.sh

在部署前验证并加载环境变量。

**使用方法：**
```bash
# Basic check (HF_TOKEN optional, HF_HOME optional with default)
./scripts/check-env.sh

# Strict mode (HF_HOME required, fails if not set)
./scripts/check-env.sh --strict

# Quiet mode (minimal output, for automation)
./scripts/check-env.sh --quiet

# Test with environment variables
HF_TOKEN="hf_xxx" HF_HOME="/models" ./scripts/check-env.sh
```

**退出码：**
| 代码 | 含义 |
|------|---------|
| 0 | 环境检查完成（变量已加载或使用默认值） |
| 2 | 严重错误（例如，无法加载 ~/.bash_profile） |

**注意：** 此脚本是可选的。您也可以直接运行 `source ~/.bash_profile`。

---

### generate-report.sh

在成功部署后生成易于阅读的部署报告。

**使用方法：**
```bash
./scripts/generate-report.sh <model-id> <container-name> <port> <status> [model-load-time] [memory-used]

# Example:
./scripts/generate-report.sh \
  "Qwen-Qwen3-0.6B" \
  "vllm-qwen3-0-6b" \
  "8001" \
  "✅ Success" \
  "3.6" \
  "1.2"
```

**参数：**
| 参数 | 是否必需 | 描述 |
|-----------|----------|-------------|
| `model-id` | 是 | 模型 ID（`/` 会被替换为 `-`） |
| `container-name` | 是 | Docker 容器名称 |
| `port` | 是 | API 端点的主机端口 |
| `status` | 是 | 部署状态（例如，“✅ 成功”） |
| `model-load-time` | 否 | 模型加载时间（以秒为单位） |
| `memory-used` | 否 | 内存使用量（以 GiB 为单位） |

**输出路径：** `$HOME/vllm-compose/<model-id>/DEPLOYMENT_REPORT.md`

**退出码：**
| 代码 | 含义 |
|------|---------|
| 0 | 报告生成成功 |
| 1 | 缺少必需参数 |
| 2 | 输出目录未找到 |

**集成：** 此脚本会在部署工作流的 **第 7 阶段** 自动执行。

---

## 输入格式

| 参数 | 类型 | 是否必需 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| model_id | 字符串 | 是 | - | HuggingFace 模型 ID |
| docker_image | 字符串 | 否 | `rocm/vllm-dev:nightly` | vLLM Docker 镜像 |
| tensor_parallel_size | 整数 | 否 | 1 | 使用的 GPU 数量 |
| port | 整数 | 否 | 9999 | API 服务器端口 |
| hf_home | 字符串 | 否 | `${HF_HOME}` 或 `/root/.cache/huggingface/hub` | 模型缓存目录 |
| hf_token | 秘密值 | 条件性 | `${HF_TOKEN}` | HuggingFace 令牌（公共模型可选；受限制的模型必需） |
| max_model_len | 整数 | 否 | 自动检测 | 最大序列长度 |
| gpu_memory_utilization | 浮点数 | 否 | 0.85 | GPU 内存利用率 |
| auto_install | 布尔值 | 否 | true | 是否自动安装依赖项 |
| log_level | 字符串 | 否 | INFO | 日志详细程度 |

## 输出结构

**所有部署相关文件必须保存在：**
```
$HOME/vllm-compose/<model-id-slash-to-dash>/
```

将模型 ID 中的 `/` 替换为 `-` 以生成目录名称：
- `openai/gpt-oss-20b` → `$HOME/vllm-compose/openai-gpt-oss-20b/`
- `Qwen/Qwen3-Coder-Next-FP8` → `$HOME/vllm-compose/Qwen-Qwen3-Coder-Next-FP8/`

**每个模型的目录结构：**
```
$HOME/vllm-compose/<model-id>/
├── deployment.log          # Full deployment logs (stdout + stderr)
├── test-results.json       # Functional test results (JSON format)
├── docker-compose.yml      # Generated Docker Compose file
├── .env                    # HF_TOKEN environment (chmod 600, optional)
└── DEPLOYMENT_REPORT.md    # Human-readable deployment summary
```

**文件要求：**
- `deployment.log` — 记录部署过程中的所有容器日志。
- `test-results.json` — 保存功能测试请求的 API 响应。
- `DEPLOYMENT_REPORT.md` — 在第 7 阶段生成。

**执行流程**

### 第 0 阶段：环境检查与自动修复

**步骤 0.1：加载环境变量**

```bash
# Source ~/.bash_profile to load HF_HOME and HF_TOKEN
source ~/.bash_profile

# If HF_HOME is not defined, it defaults to /root/.cache/huggingface/hub
```

如果 `HF_HOME` 未在 `~/.bash_profile` 中定义，其默认值为 `/root/.cache/huggingface/hub`。

**步骤 0.2：创建输出目录**
- 创建：`$HOME/vllm-compose/<model-id>/`

**步骤 0.3：初始化日志记录**
- 所有输出文件保存到：`$HOME/vllm-compose/<model-id>/deployment.log`

**步骤 0.4：系统检查**
- 检查操作系统和包管理器。
- 检查 Python、pip、huggingface_hub。
- 检查 Docker 和 docker-compose。
- 检查 ROCm 工具（rocm-smi/amd-smi）。
- 检查 GPU 访问权限（/dev/kfd, /dev/dri）。
- 确保有至少 20GB 的磁盘空间。

### 第 1 阶段：模型下载

**使用第 0 阶段中的 `HF_HOME`（环境变量或默认值）：**

```bash
# Download model to HF_HOME
huggingface-cli download <model_id> --local-dir "$HF_HOME/hub/models--<org>--<model>"

# Or use snapshot_download via Python:
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='<model_id>', cache_dir='$HF_HOME')"
```

**认证处理：**

| 情况 | 行为 |
|----------|----------|
| 公共模型 + 无令牌 | ✅ 下载成功 |
| 公共模型 + 提供令牌 | ✅ 下载成功 |
| 受限制的模型 + 无令牌 | ❌ 下载失败，显示“需要认证”错误 |
| 受限制的模型 + 无效令牌 | ❌ 下载失败，显示“令牌无效”错误 |
| 受限制的模型 + 有效令牌 | ✅ 下载成功 |

**认证失败时：**
```bash
echo "ERROR: Model download failed - authentication required"
echo "This model requires a valid HF_TOKEN."
echo ""
echo "Please add to ~/.bash_profile:"
echo "  export HF_TOKEN=\"hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\""
echo "Then run: source ~/.bash_profile"
exit 1
```

- 在 `HF_HOME/hub/models--<org>--<model-name>/` 中查找模型路径。
- 将下载进度记录到 `deployment.log`。

### 第 2 阶段：模型参数检测**
- 从模型配置文件中读取参数。
- 自动检测：`max_model_len`、`hidden_size`、`num_attention_heads`、`num_hidden_layers`、`vocab_size`、`dtype`。
- 验证 `TP_size` 是否能被 `attention_heads` 整除。
- 估算显存需求。

### 第 3 阶段：Docker Compose 配置

**在输出目录中生成以下文件：**

- **docker-compose.yml** → `$HOME/vllm-compose/<model-id>/docker-compose.yml`
  - 将 `HF_HOME` 指定为卷（对模型仅读）。
- **.env** → `$HOME/vllm-compose/<model-id>/.env`（可选）
  - 内容：`HF_TOKEN=<value>` |
  - 权限：`chmod 600` |
  - 仅当用户明确请求持久化令牌存储时才创建。

**卷挂载示例：**
```yaml
volumes:
  - ${HF_HOME}:/root/.cache/huggingface/hub:ro
  - /dev/kfd:/dev/kfd
  - /dev/dri:/dev/dri
```

**重要提示：** Docker Compose 会在运行时从主机环境读取 `${HF_HOME}`。在运行 `docker compose` 之前，请执行 `source ~/.bash_profile`。

### 第 4 阶段：容器启动**

**重要提示：** 在部署前，请拉取最新镜像以确保更新：
```bash
docker pull rocm/vllm-dev:nightly
```

**注意：** 默认端口为 9999。在运行 `docker compose` 之前，请检查端口是否已被占用：`ss -tlnp | grep :<port>`。如果端口已被占用，请在 `docker-compose.yml` 中指定其他端口。

- 在运行时传递 `HF_TOKEN`：`HF_TOKEN=$HF_TOKEN docker compose up -d`
- 等待容器初始化完成。

### 第 5 阶段：健康状态验证**
- 检查容器状态。
- 测试 `/health` 端点。
- 测试 `/v1/models` 端点。

### 第 6 阶段：功能测试**
- 通过 `/v1/chat/completions` API 运行完成测试。
- **将结果保存到：** `$HOME/vllm-compose/<model-id>/test-results.json`
- 确保响应包含有效的完成结果。
- **在以下文件都存在时，部署视为完成：**
  - `deployment.log`
  - `test-results.json`

### 第 7 阶段：生成部署报告**

**使用辅助脚本生成易于阅读的部署报告。**

**步骤 7.1：提取部署指标**

```bash
# Parse deployment.log for metrics
MODEL_LOAD_TIME=$(grep -o "model loading took [0-9.]* seconds" deployment.log | grep -o '[0-9.]*' || echo "N/A")
MEMORY_USED=$(grep -o "took [0-9.]* GiB memory" deployment.log | grep -o '[0-9.]*' || echo "N/A")
```

**步骤 7.2：生成报告**

```bash
# Execute the report generation script
<skill-dir>/scripts/generate-report.sh \
  "<model-id>" \
  "<container-name>" \
  "<port>" \
  "<status>" \
  "$MODEL_LOAD_TIME" \
  "$MEMORY_USED"

# Example:
./scripts/generate-report.sh \
  "Qwen-Qwen3-0.6B" \
  "vllm-qwen3-0-6b" \
  "8001" \
  "✅ Success" \
  "3.6" \
  "1.2"
```

**输出文件：** `$HOME/vllm-compose/<model-id>/DEPLOYMENT_REPORT.md`

**报告内容：**
- 输出结构验证（文件清单）。
- 部署摘要表（健康状态、测试结果、指标）。
- 测试结果（请求/响应预览）。
- 环境配置。
- 快速操作命令。

**完成标准：**
- `DEPLOYMENT_REPORT.md` 存在于输出目录中。
- 报告包含所有必需的部分。
- 所有文件检查均显示为“✅”。

## 安全最佳实践

1. **切勿将令牌提交到版本控制** — 将 `.env` 文件添加到 `.gitignore`。
2. **使用权限设置为 600 的 `.env` 文件** — 仅限所有者访问。
3. **在日志中隐藏令牌** — 只显示前 10 个字符：`${TOKEN:0:10}...`。
4. **在运行时传递令牌** — `HF_TOKEN=$HF_TOKEN docker compose up -d`。
5. **在生产环境中将令牌存储在 `~/.bash_profile` 中** — 将 `HF_TOKEN` 设置在用户的 shell 配置文件中。
6. **为受限制的模型设置令牌** — 在下载时验证令牌；在生产环境中将其设置到 `~/.bash_profile` 中。

## 故障排除

### 环境变量相关问题

| 问题 | 解决方案 |
|-------|----------|
| `HF_TOKEN` 未设置 | 在 `~/.bash_profile` 中添加 `export HF_TOKEN="hf_xxx"`，然后执行 `source ~/.bash_profile`。或通过参数提供。 |
| `HF_HOME` 未设置 | 默认值为 `/root/.cache/huggingface/hub`。在生产环境中，将 `export HF_HOME="/path"` 添加到 `~/.bash_profile` 中。 |
| 未找到 `~/.bash_profile` | 创建 `~/.bash_profile` 并设置环境变量。 |
| 更改未生效 | 执行 `source ~/.bash_profile` 或重启终端。 |
| 提供了 `HF_TOKEN` 但下载仍失败 | 令牌可能无效或无法访问模型。请在 https://huggingface.co/settings/tokens 验证令牌。 |

### 模型下载相关问题

| 问题 | 解决方案 |
|-------|----------|
| “需要认证”（受限制的模型） | 在 `~/.bash_profile` 中设置 `HF_TOKEN` 或通过参数提供。确保令牌具有访问模型的权限。 |
| 未找到模型 | 确认模型 ID 是否正确（区分大小写）。检查模型是否存在于 HuggingFace 上。 |
| 下载超时 | 检查网络连接。大型模型可能需要更多时间。 |

### 部署相关问题

| 问题 | 解决方案 |
|-------|----------|
| 未找到 hf CLI | 使用 `pip install huggingface_hub` 安装它。 |
| Docker Compose 失败 | 使用 `docker compose`（不要使用连字符）。 |
| 无法访问 GPU | 将用户添加到 `render` 组：`sudo usermod -aG render $USER` |
| 端口已被占用 | 更改 `port` 参数。 |
| 内存不足（OOM） | 降低 `gpu_memory_utilization` 的值。

## 清理

```bash
cd $HOME/vllm-compose/<model-id>
docker compose down
```

## 状态检查

**检查部署状态和日志：**

```bash
# View deployment directory
ls -la $HOME/vllm-compose/<model-id>/

# View live logs
tail -f $HOME/vllm-compose/<model-id>/deployment.log

# View test results
cat $HOME/vllm-compose/<model-id>/test-results.json

# Check container status
docker ps | grep <model-id>

# Verify environment variables
echo "HF_TOKEN: ${HF_TOKEN:0:10}..."
echo "HF_HOME: $HF_HOME"
```

## 快速启动（生产环境）

**步骤 1：将环境变量添加到 `~/.bash_profile`**

```bash
# Required: HuggingFace token
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Recommended: Custom model storage path (production)
export HF_HOME="/data/models/huggingface"

# Apply changes
source ~/.bash_profile
```

**步骤 2：验证环境是否准备就绪**

```bash
# Source ~/.bash_profile to load variables
source ~/.bash_profile

# Expected output:
# === Environment Ready ===
# Summary:
#   HF_TOKEN: hf_xxxxxx...
#   HF_HOME:  /data/models/huggingface
```

**步骤 3：运行部署**

```bash
# The skill will automatically:
# 1. Source ~/.bash_profile to load HF_HOME and HF_TOKEN
# 2. Use HF_TOKEN and HF_HOME from environment (or ~/.bash_profile, or defaults)
# 3. Proceed without token for public models
# 4. Fail at download time with clear error if gated model requires token
```

## 版本历史

| 版本 | 更改内容 |
|---------|---------|
| 1.0.0 | 初始版本 |