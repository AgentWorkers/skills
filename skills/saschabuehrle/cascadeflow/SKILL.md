---
name: cascadeflow
description: 将 CascadeFlow 设置为 OpenClaw 的自定义提供者，整个过程只需简单的复制粘贴操作即可完成。这适用于用户希望快速安装、进行预设选择（仅使用 OpenAI、仅使用 Anthropic 或两者混合）、设置 OpenClaw 模型的别名，以及为流处理和代理循环配置安全的生产环境默认参数的情况。
---
# CascadeFlow：降低成本与延迟 | 支持17种领域特定模型 + 与OpenClaw原生事件集成

使用CascadeFlow作为OpenClaw的提供者，通过级联方式降低使用成本和延迟。您可以配置多达17种领域特定的模型（用于编码、网络搜索、推理等），并支持OpenClaw原生事件的处理；系统会优先使用小型模型进行处理，必要时会启用验证机制。整个设置过程非常简单，只需进行一次健康检查（health check）和一次聊天测试（chat call）即可完成验证。

## 快速入门

您也可以让您的OpenClaw代理为您配置CascadeFlow，使其成为支持OpenClaw原生事件和领域特定功能的自定义提供者：

1. 安装所需组件：
```bash
python3 -m venv .venv
source .venv/bin/activate
# Fastest base setup (OpenClaw integration extras)
pip install "cascadeflow[openclaw]"
```

2. 选择预设配置文件：
- `examples/configs/anthropic-only.yaml`
- `examples/configs/openai-only.yaml`
- `examples/configs/mixed-anthropic-openai.yaml`

3. 在`.env`文件中添加相关配置键：
```bash
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
```

4. 启动服务器：
```bash
set -a; source .env; set +a
python3 -m cascadeflow.integrations.openclaw.openai_server \
  --host 127.0.0.1 \
  --port 8084 \
  --config examples/configs/anthropic-only.yaml \
  --auth-token local-openclaw-token \
  --stats-auth-token local-stats-token
```

5. 配置OpenClaw提供者：
  - `baseUrl`: `http://127.0.0.1:8084/v1`  
  （如果服务器运行在其他地址上，请替换为实际地址，例如：`http://<server-ip>:8084/v1` 或 `https://<domain>/v1` [通过TLS代理访问]）
  - `api`: `openai-completions`
  - `model`: `cascadeflow`

6. 设置别名并使用：
  - 在OpenClaw配置中，将`cascadeflow/cascadeflow`设置为别名`cflow`。
  - 通过`/model cflow`命令来调用该提供者。
  - `/cascade`命令仅在OpenClaw中进行了相应配置时才可用。

## 用户可获得的特性：
- 通过级联方式实现成本和延迟的降低。
- 支持在流式处理（streaming）模式下进行级联操作。
- 支持在多步骤代理循环（multi-step agent loops）中实现级联功能。
- 支持与OpenAI兼容的 `/v1/chat/completions` 通信协议。
- 通过预设模型实现领域特定的级联处理。

## 安全默认设置：
- 将本地地址设置为`127.0.0.1`。
- 使用认证令牌（auth tokens）进行API访问和数据统计。
- 将所有外部接口通过TLS反向代理进行保护。

## 完整文档：
- 详细配置信息和验证方法请参阅 `references/clawhub_publish_pack.md`。
- 有关产品列表和定位信息，请参阅 `references/market_positioning.md`。