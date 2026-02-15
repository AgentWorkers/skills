---
name: cascadeflow
description: 将 CascadeFlow 设置为 OpenClaw 的自定义提供者，整个过程只需简单的复制粘贴操作即可完成。当用户希望快速安装、进行预设选择（仅使用 OpenAI、仅使用 Anthropic、或同时使用两者）、设置 OpenClaw 模型的别名，以及为流处理和代理循环配置安全的生产级默认参数时，可以使用此方法。
---

# CascadeFlow：降低成本与延迟

使用 CascadeFlow 作为 OpenClaw 提供者，通过级联方式降低成本和延迟。保持设置简单，然后通过一次健康检查（health check）和一次聊天通话（chat call）来验证配置是否正确。

## 快速入门

1. 安装：
```bash
git clone https://github.com/lemony-ai/cascadeflow.git
cd cascadeflow
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[openclaw,providers]"
```

2. 选择一个预设配置文件：
- `examples/configs/anthropic-only.yaml`
- `examples/configs/openai-only.yaml`
- `examples/configs/mixed-anthropic-openai.yaml`

3. 在 `.env` 文件中添加相关配置键：
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

5. 配置 OpenClaw 提供者：
- `baseUrl`: `http://127.0.0.1:8084/v1`
- `api`: `openai-completions`
- `model`: `cascadeflow`

6. 设置别名并使用：
- 在 OpenClaw 配置中，将 `cascadeflow/cascadeflow` 设置为别名 `cflow`。
- 通过 `/model cflow` 来调用相关服务。
- `/cascade` 命令仅在 OpenClaw 中进行了配置时才可用。

## 用户可获得的特性

- 通过级联方式降低成本和延迟。
- 支持在启用流式处理（streaming）的情况下进行级联操作。
- 支持在多步骤代理循环（multi-step agent loops）中进行级联。
- 支持与 OpenAI 兼容的 `/v1/chat/completions` 传输协议。
- 通过预设模型实现基于领域（domain-specific）的级联功能。

## 安全默认设置

- 将本地地址绑定到 `127.0.0.1`。
- 使用认证令牌（auth tokens）进行 API 和统计数据的访问。
- 将所有外部访问通过 TLS 反向代理（TLS reverse proxy）进行保护。

## 完整文档

- 详细配置和验证方法请参阅：`references/clawhub_publish_pack.md`。
- 有关产品列表和定位策略的文档请参阅：`references/market_positioning.md`。