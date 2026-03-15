---
name: "memory-pro"
description: "该技能利用本地向量数据库对您的内存文件进行语义搜索。"
version: "2.5.0"
metadata:
  openclaw:
    requires:
      bins:
        - "bash"
        - "lsof"
        - "openclaw"
        - "python"
        - "python3"
      env:
        - "HOME"
        - "MEMORY_PRO_API_URL"
        - "MEMORY_PRO_BM25_PATH"
        - "MEMORY_PRO_BM25_WEIGHT"
        - "MEMORY_PRO_CANDIDATE_POOL"
        - "MEMORY_PRO_CORE_FILES"
        - "MEMORY_PRO_DAILY_SCOPE"
        - "MEMORY_PRO_DATA_DIR"
        - "MEMORY_PRO_DUAL_HIT_BONUS"
        - "MEMORY_PRO_ENABLE_MMR"
        - "MEMORY_PRO_HARD_MIN_SCORE"
        - "MEMORY_PRO_INDEX_PATH"
        - "MEMORY_PRO_LENGTH_NORM_ALPHA"
        - "MEMORY_PRO_LENGTH_NORM_ANCHOR"
        - "MEMORY_PRO_META_PATH"
        - "MEMORY_PRO_MMR_LAMBDA"
        - "MEMORY_PRO_MMR_SIM_THRESHOLD"
        - "MEMORY_PRO_MODE"
        - "MEMORY_PRO_PORT"
        - "MEMORY_PRO_RECENCY_HALF_LIFE_DAYS"
        - "MEMORY_PRO_RECENCY_WEIGHT"
        - "MEMORY_PRO_RERANK_API_KEY"
        - "MEMORY_PRO_RERANK_BLEND"
        - "MEMORY_PRO_RERANK_ENDPOINT"
        - "MEMORY_PRO_RERANK_MODEL"
        - "MEMORY_PRO_RERANK_PROVIDER"
        - "MEMORY_PRO_RERANK_SAMPLE_PCT"
        - "MEMORY_PRO_RERANK_TIMEOUT_MS"
        - "MEMORY_PRO_RERANK_TOPN"
        - "MEMORY_PRO_SCOPE_STRICT"
        - "MEMORY_PRO_SENTENCES_PATH"
        - "MEMORY_PRO_TIMEOUT"
        - "MEMORY_PRO_VECTOR_WEIGHT"
        - "OPENCLAW_HOME"
        - "OPENCLAW_NETWORK_DRIVE"
        - "OPENCLAW_WORKSPACE"
      config:
        - ".env"
        - "/skills/memory-pro/data/INDEX.json"
        - "/skills/memory-pro/data/state.json"
        - "/skills/memory-pro/v2/eval_queries.json"
        - "/tmp/memory_pro_benchmark.json"
        - "/tmp/memory_pro_hybrid.json"
        - "/tmp/memory_pro_vector.json"
        - "INDEX.json"
        - "args.json"
        - "eval_queries.json"
        - "r.json"
        - "response.json"
        - "state.json"
        - "v2/eval_queries.json"
    primaryEnv: "HOME"
    envVars:
      -
        name: "HOME"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_API_URL"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_BM25_PATH"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_BM25_WEIGHT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_CANDIDATE_POOL"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_CORE_FILES"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_DAILY_SCOPE"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_DATA_DIR"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_DUAL_HIT_BONUS"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_ENABLE_MMR"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_HARD_MIN_SCORE"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_INDEX_PATH"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_LENGTH_NORM_ALPHA"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_LENGTH_NORM_ANCHOR"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_META_PATH"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_MMR_LAMBDA"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_MMR_SIM_THRESHOLD"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_MODE"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_PORT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RECENCY_HALF_LIFE_DAYS"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RECENCY_WEIGHT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_API_KEY"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_BLEND"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_ENDPOINT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_MODEL"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_PROVIDER"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_SAMPLE_PCT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_TIMEOUT_MS"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_RERANK_TOPN"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_SCOPE_STRICT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_SENTENCES_PATH"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_TIMEOUT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "MEMORY_PRO_VECTOR_WEIGHT"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "OPENCLAW_HOME"
        required: true
        description: "Credential used by memory-pro."
      -
        name: "OPENCLAW_NETWORK_DRIVE"
        required: false
        description: "Optional network drive/docs root."
      -
        name: "OPENCLAW_WORKSPACE"
        required: true
        description: "Credential used by memory-pro."
---
# Memory Pro (v2)

该技能通过使用本地向量数据库，实现对内存文件的语义搜索功能。

## 架构（v2）

- **服务**：以 `systemd` 用户服务的形式运行（名称为 `memory-pro.service`）。
- **端口**：`8001`（为确保稳定性而硬编码）。
- **引擎**：FAISS + Sentence-Transformers（版本为 `all-MiniLM-L6-v2`）。
- **数据来源**：
  - 每日日志：`${OPENCLAW_WORKSPACE}/memory/*.md`
  - 核心文件：`MEMORY.md`、`SOUL.md`、`STATUS.md`、`AGENTS.md`、`USER.md`（位于工作空间根目录下）。
- **索引**：存储在 `${OPENCLAW_WORKSPACE}/skills/memory-pro/v2/memory.index` 文件中。

## 使用方法

### 1. 语义搜索（推荐方式）
使用 Python 脚本查询该服务。

```bash
# Basic search
python3 scripts/search_semantic.py "What did I do yesterday?"

# JSON output
python3 scripts/search_semantic.py "project updates" --json
```

### 2. 手动重建索引
该服务会在重启时自动重建索引。如需强制更新索引，请执行以下操作：

```bash
systemctl --user restart memory-pro.service
```
*注意：服务重启需要约 15-20 秒来完成索引重建和模型加载。客户端脚本具有自动重试机制。*

### 3. 服务管理

```bash
# Check status
systemctl --user status memory-pro.service

# Stop service
systemctl --user stop memory-pro.service

# View logs
journalctl --user -u memory-pro.service -f
```

## 故障排除

### “连接失败”
- 可能是服务已停止或正在重启中。
- 检查服务状态：`systemctl --user status memory-pro.service`。
- 如果服务正在重启，请等待 15 秒。客户端脚本会自动尝试重试，最多重试 20 秒。

### “索引大小不一致”
- 这表示 `memory.index` 文件与 `sentences.txt` 文件之间的数据不一致。
- **解决方法**：重启服务。启动脚本 `start.sh` 会在启动 API 之前自动运行 `build_index.py` 来修复此问题。

### “端口已被占用”
- 端口 8001 被某个后台进程占用。
- **解决方法**：使用 `kill $(lsof -t -i:8001)` 命令终止占用该端口的进程，然后重启服务。