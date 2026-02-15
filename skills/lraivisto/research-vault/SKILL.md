---
name: researchvault
description: "高速度研究编排引擎。负责管理代理的持久状态、合成过程以及自主验证功能。"
metadata:
  {
    "openclaw":
      {
        "requires": { "python": ">=3.13", "bins": ["uv"] },
        "install":
          [
            {
              "id": "vault-venv",
              "kind": "exec",
              "command": "uv venv && uv pip install -e .",
              "label": "Initialize ResearchVault Environment",
            },
          ],
      },
  }
---

# ResearchVault 🦞

一个用于自主研究的智能状态管理工具。

## 核心功能

- **研究资料库（The Vault）**：使用 SQLite 本地存储研究资料（`artifacts`）、研究发现（`findings`）以及相关链接（`links`）。
- **并行推理（Divergent Reasoning）**：创建分支（`branches`）和假设（`hypotheses`）以探索不同的研究路径。
- **综合引擎（Synthesis Engine）**：利用本地嵌入数据（local embeddings）自动发现新的研究链接。
- **主动验证（Active Verification）**：通过 `verification_missions` 实现代理（agents）的自我纠错功能。
- **MCP 服务器（MCP Server）**：支持代理间的协作。
- **监控模式（Watchdog Mode）**：持续在后台监控 URL 和查询请求。

## 工作流程

### 1. 项目初始化
```bash
uv run python scripts/vault.py init --id "metal-v1" --name "Suomi Metal" --objective "Rising underground bands"
```

### 2. 多源数据导入（Multi-Source Ingestion）
```bash
uv run python scripts/vault.py scuttle "https://reddit.com/r/metal" --id "metal-v1"
```

### 3. 数据综合与验证（Synthesis & Verification）
```bash
# Link related findings
uv run python scripts/vault.py synthesize --id "metal-v1"

# Plan verification for low-confidence data
uv run python scripts/vault.py verify plan --id "metal-v1"
```

### 4. MCP 服务器（MCP Server）
```bash
uv run python scripts/vault.py mcp --transport stdio
```

## 系统要求

需要 Python 3.13 和 `uv` 这两个软件包。