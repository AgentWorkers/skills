---
name: cascadeflow
description: >
  **OpenClaw原生域名级级联功能**  
  适用于需要通过级联方式降低成本/延迟、实现基于域名的模型分配、利用OpenClaw原生事件处理机制，以及配置相关命令（如 `/model cflow` 和可选的 `/cascade stats` 命令）的场景。
---
# CascadeFlow：降低成本与延迟 | 支持17种领域特定模型 + 与OpenClaw原生事件集成

使用CascadeFlow作为OpenClaw的提供者，通过级联方式降低成本和延迟。您可以配置多达17种领域特定的模型（用于编码、网络搜索、推理等），并支持OpenClaw原生的事件处理功能。这些模型会按顺序执行（先使用小型模型，必要时再使用验证模型）。设置过程简单，只需进行一次健康检查（health check）和一次聊天测试即可完成配置。

## 为何使用它

- 通过级联使用起草器（drafter）和验证器（verifier）来减少成本。
- 支持运行17种以上领域特定的模型（包括编码、推理、网络搜索等）。
- 支持流式处理（streaming）和多步骤代理循环（multi-step agent loops）。
- 通过处理OpenClaw原生的事件/领域信号，实现更智能的模型选择。

## 安全默认设置

- 从PyPI安装该软件包，并在首次运行前验证其完整性。
- 默认情况下，服务器仅允许访问本地地址（localhost）。
- 对聊天和统计端点使用明确的认证令牌（生产环境推荐）。
- 远程访问需通过TLS/反向代理，并使用强加密令牌进行保护。
- 使用最小权限的提供者密钥（测试密钥与生产密钥分开）。

## 工作原理

1. OpenClaw通过兼容OpenAI的`/v1/chat/completions`接口向CascadeFlow发送请求。
2. CascadeFlow读取提示上下文以及OpenClaw原生的事件/领域元数据（例如`metadata.method`、`metadata.event`和`channel/category`等）。
3. CascadeFlow选择一对适合当前任务的领域特定模型（先使用小型模型）。
4. 如果模型生成的结果质量符合要求，会返回起草器的答案（从而节省成本并降低延迟）。
5. 如果结果质量未达标，系统会启动验证模型并返回最终答案。
6. 流式处理和多步骤代理循环同样支持这种级联机制。

### 优势

- 在不需要验证模型时避免不必要的验证操作，从而降低平均成本。
- 对于简单和中等复杂度的任务，能够显著降低延迟。
- 在处理复杂任务时，通过验证模型的机制保证更高的答案质量。
- 通过理解OpenClaw原生的事件和领域信息，提升系统的整体运行效率。

## 快速入门

您可以让您的OpenClaw代理为您配置CascadeFlow作为自定义提供者，使其支持OpenClaw原生事件和领域特定功能：

1. 安装并验证软件包：
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade "cascadeflow[openclaw]>=0.7,<0.8"
python -m pip show cascadeflow
python -m pip download --no-deps "cascadeflow[openclaw]>=0.7,<0.8" -d /tmp/cascadeflow_pkg
python -m pip hash /tmp/cascadeflow_pkg/cascadeflow-*.whl
```

**可选配置选项：**
```bash
python -m pip install --upgrade "cascadeflow[openclaw,anthropic]>=0.7,<0.8"   # Anthropic-only preset
python -m pip install --upgrade "cascadeflow[openclaw,openai]>=0.7,<0.8"      # OpenAI-only preset
python -m pip install --upgrade "cascadeflow[openclaw,providers]>=0.7,<0.8"   # Mixed preset
```

2. 选择预设配置和凭证：
- 预设配置文件：`examples/configs/anthropic-only.yaml`、`examples/configs/openai-only.yaml`、`examples/configs/mixed-anthropic-openai.yaml`
- 提供者密钥：`ANTHROPIC_API_KEY=...` 和/或 `OPENAI_API_KEY=...`（根据所选配置文件设置）
- 服务认证令牌：`--auth-token ...` 和 `--stats-auth-token ...`（生产环境推荐；建议使用随机生成的较长字符串）
3. 启动服务器（默认使用本地地址）：
```bash
set -a; source .env; set +a
python3 -m cascadeflow.integrations.openclaw.openai_server \
  --host 127.0.0.1 --port 8084 \
  --config examples/configs/anthropic-only.yaml \
  --auth-token local-openclaw-token \
  --stats-auth-token local-stats-token
```

**可选的运行时配置：**
```bash
# Observe first (recommended): log decisions, no blocking
python3 -m cascadeflow.integrations.openclaw.openai_server \
  --host 127.0.0.1 --port 8084 \
  --config examples/configs/anthropic-only.yaml \
  --harness-mode observe

# Enforce mode with limits
python3 -m cascadeflow.integrations.openclaw.openai_server \
  --host 127.0.0.1 --port 8084 \
  --config examples/configs/anthropic-only.yaml \
  --harness-mode enforce \
  --harness-budget 1.0 \
  --harness-max-tool-calls 12 \
  --harness-max-latency-ms 3500 \
  --harness-compliance strict
```

4. 配置OpenClaw提供者：
- `baseUrl`：`http://<cascadeflow-host>:8084/v1`（默认值：`http://127.0.0.1:8084/v1`）
- 如果使用远程服务器：`http://<server-ip>:8084/v1` 或 `https://<domain>/v1`（需通过TLS/反向代理）
- `api`：`openai-completions`
- `model`：`cascadeflow`
- `apiKey`：与`--auth-token`参数相同的密钥

## 命令行操作

- `/model cflow`：使用别名`cflow`切换OpenClaw的默认模型。
- `/cascade`：根据OpenClaw的配置，执行自定义级联操作。
- `/cascade savings`：查看自定义的成本统计信息。
- `/cascade health`：查看服务的运行状态。

## 相关资源

- 完整的配置指南：`references/clawhub_publish_pack.md`
- 市场定位策略文档：`references/market_positioning.md`
- 官方文档：`https://github.com/lemony-ai/cascadeflow/blob/main/docs/guides/openclaw_provider.md`
- GitHub仓库：`https://github.com/lemony-ai/cascadeflow`