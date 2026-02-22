---
name: zvec-local-rag-service
description: 使用 zvec 和 Ollama 嵌入模型来运行一个始终处于运行状态的本地语义搜索服务。当您需要导入 `.txt` 或 `.md` 文件、通过 HTTP 端点（`/health`、`/ingest`、`/search`）执行基于意义的搜索，并在 macOS 上（使用 `launchd`）或手动方式保持服务运行时，可以使用该服务。包含服务代码、`launchd` 模板以及管理脚本。
metadata:
  openclaw:
    requires:
      bins: ["node", "npm", "ollama", "curl"]
    install:
      - id: zvec-deps
        kind: npm
        package: "@zvec/zvec"
        label: "Install zvec Node binding"
---
# zvec-local-rag-service

使用 Ollama 嵌入模型和 zvec 运行本地的 RAG（Rapid Annotation Generator）搜索服务。

## 包含的文件

- `scripts/rag-service.mjs` → HTTP 服务实现代码
- `scripts/manage.sh` → 用于启动、停止、重启、检查服务状态及数据导入的脚本
- `references/launchd.plist.template` → macOS 的 LaunchAgent 配置模板

## 先决条件

- Node.js 18 及以上版本
- Ollama 服务正在运行中
- 嵌入模型（默认值）：`mxbai-embed-large`

模型只需准备一次：

```bash
ollama pull mxbai-embed-large
```

## 快速启动

从技能目录（skill directory）开始操作：

```bash
scripts/manage.sh bootstrap
scripts/manage.sh install-launchd   # writes plist, inspect once
scripts/manage.sh start
scripts/manage.sh health
```

数据导入与搜索功能：

```bash
scripts/manage.sh ingest ./docs
scripts/manage.sh search "your query"
```

## 安装与测试

只需复制并粘贴以下命令即可完成安装和简单测试：

```bash
# 1) prerequisites
ollama pull mxbai-embed-large

# 2) bootstrap and start service
scripts/manage.sh bootstrap
scripts/manage.sh install-launchd
scripts/manage.sh start

# 3) verify health
scripts/manage.sh health

# 4) create tiny test corpus
mkdir -p ./docs
cat > ./docs/sample.md <<'EOF'
Zvec + Ollama enables local semantic search.
EOF

# 5) ingest + query
scripts/manage.sh ingest ./docs
scripts/manage.sh search "local semantic search with ollama"
```

## 端点接口

- `GET /health` → 获取服务状态信息
- `POST /ingest` → 导入数据（格式：`{"dir": "./docs", "reset": true}`）
- `POST /search` → 执行搜索（格式：`{"query": "...", "topk": 5}`）

## 持久化设置（macOS 使用 LaunchAgent）

安装并启用 LaunchAgent：

```bash
scripts/manage.sh install-launchd
scripts/manage.sh start
scripts/manage.sh status
```

卸载 LaunchAgent：

```bash
scripts/manage.sh uninstall-launchd
```

在启用持久化功能之前，请务必检查生成的 `plist` 文件：
- 文件路径：`~/Library/LaunchAgents/com.openclaw.zvec-rag-service.plist`

## 通过环境变量进行配置

- `RAG_HOST` （默认值：`127.0.0.1`）
- `RAG_PORT` （默认值：`8787`）
- `OLLAMA_URL` （默认值：`http://127.0.0.1:11434`）
- `OLLAMA_EMBED_MODEL` （默认值：`mxbai-embed-large`）
- `RAG_BASE_DIR` （默认值：`~/.openclaw/data/zvec-rag-service`）
- `ALLOW_REMOTE_OLLAMA` （默认值：`false`，禁止使用非本地的 OLLAMA 服务）
- `ALLOW_NON_loopBACK_HOST` （默认值：`false`，禁止使用外部可访问的主机）

## 注意事项

- 默认设置为仅使用本地循环回环（loopback）网络进行通信。
- 如果需要使用远程嵌入模型或主机绑定，请通过环境变量明确启用相关选项。
- `launchd` 的管理操作仅适用于 macOS 系统；在非 macOS 系统上，请使用 `scripts/manage.sh start` 命令手动启动服务。