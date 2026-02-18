---
name: researchvault
description: "本地优先的研究任务调度引擎。负责管理任务状态、任务合成过程，以及可选的后台服务（如 MCP/Watchdog）。"
homepage: https://github.com/lraivisto/ResearchVault
disable-model-invocation: true
user-invocable: true
metadata:
  openclaw:
    emoji: "🦞"
    install:
      - id: vault-venv
        kind: exec
        command: python3 -m venv .venv && . .venv/bin/activate && pip install -e .
        label: Initialize ResearchVault (Standard)
    requires:
      python: ">=3.13"
      env:
        RESEARCHVAULT_DB:
          description: "Optional: Custom path to the SQLite database file."
          required: false
        BRAVE_API_KEY:
          description: "Optional: Brave Search API key."
          required: false
        SERPER_API_KEY:
          description: "Optional: Serper API key."
          required: false
        SEARXNG_BASE_URL:
          description: "Optional: SearXNG base URL."
          required: false
        RESEARCHVAULT_PORTAL_TOKEN:
          description: "Optional: static portal token. If unset, start_portal.sh sources/generates .portal_auth and exports this env var."
          required: false
        RESEARCHVAULT_PORTAL_SCAN_OPENCLAW:
          description: "Optional: set to '1' to request OpenClaw workspace DB scan."
          required: false
        RESEARCHVAULT_PORTAL_ALLOWED_DB_ROOTS:
          description: "Optional: comma-separated absolute DB roots. Default: ~/.researchvault,/tmp."
          required: false
        RESEARCHVAULT_PORTAL_INJECT_SECRETS:
          description: "Optional: set to '1' to inject configured provider env vars into vault subprocesses."
          required: false
        RESEARCHVAULT_PORTAL_STATE_DIR:
          description: "Optional: portal state directory (default ~/.researchvault/portal)."
          required: false
        RESEARCHVAULT_PORTAL_HOST:
          description: "Optional: backend bind host."
          required: false
        RESEARCHVAULT_PORTAL_PORT:
          description: "Optional: backend bind port."
          required: false
        RESEARCHVAULT_PORTAL_FRONTEND_HOST:
          description: "Optional: frontend bind host."
          required: false
        RESEARCHVAULT_PORTAL_FRONTEND_PORT:
          description: "Optional: frontend bind port."
          required: false
        RESEARCHVAULT_PORTAL_CORS_ORIGINS:
          description: "Optional: comma-separated CORS origins for backend."
          required: false
        RESEARCHVAULT_PORTAL_RELOAD:
          description: "Optional: set to 'true' for backend auto-reload."
          required: false
        RESEARCHVAULT_PORTAL_COOKIE_SECURE:
          description: "Optional: set to 'true' to mark auth cookie Secure."
          required: false
        RESEARCHVAULT_PORTAL_PID_DIR:
          description: "Optional: start_portal.sh PID/log directory."
          required: false
        RESEARCHVAULT_PORTAL_SHOW_TOKEN:
          description: "Optional: set to '1' to print tokenized portal URLs."
          required: false
        RESEARCHVAULT_SEARCH_PROVIDERS:
          description: "Optional: search provider order override."
          required: false
        RESEARCHVAULT_WATCHDOG_INGEST_TOP:
          description: "Optional: watchdog ingest top-k override."
          required: false
        RESEARCHVAULT_VERIFY_INGEST_TOP:
          description: "Optional: verify ingest top-k override."
          required: false
        RESEARCHVAULT_MCP_TRANSPORT:
          description: "Optional: MCP server transport override."
          required: false
        REQUESTS_CA_BUNDLE:
          description: "Optional: custom CA bundle for HTTPS verification."
          required: false
        SSL_CERT_FILE:
          description: "Optional: custom CA certificate file."
          required: false
---
# ResearchVault 🦞

**以本地数据为中心的研究编排引擎。**

ResearchVault负责管理代理的持久状态、数据合成以及自主验证功能。

## 安全性与隐私（以本地数据为主）

- **本地存储**：所有数据都存储在本地 SQLite 数据库（`~/.researchvault/research_vault.db`）中，不进行云同步。
- **网络访问控制**：仅针对用户请求的研究任务或 Brave Search（如果已配置）才会发起出站连接。
- **SSRF（安全套接字层转发）防护**：默认情况下会严格限制内部网络访问，禁止使用本地/私有 IP 地址（如 `localhost`、`10.0.0.0/8` 等）。可以通过 `--allow-private-networks` 参数来覆盖这一设置。
- **需要手动启用的服务**：后台监控工具和 MCP 服务器位于 `scripts/services/` 目录中，必须手动启动。
- **严格限制模型行为**：设置 `disable-model-invocation: true` 可以防止模型自动启动后台任务。

## 安装

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 快速入门

1. **初始化项目**：
   ```bash
   python scripts/vault.py init --objective "Analyze AI trends" --name "Trends-2026"
   ```

2. **导入数据**：
   ```bash
   python scripts/vault.py scuttle "https://example.com" --id "trends-2026"
   ```

3. **自主策略执行**：
   ```bash
   python scripts/vault.py strategy --id "trends-2026"
   ```

## 门户（需手动启用）

需要手动启动门户：

```bash
./start_portal.sh
```

- **后端地址**：`127.0.0.1:8000`
- **前端地址**：`127.0.0.1:5173`
- **后端认证**：严格依赖 `RESEARCHVAULT_PORTAL_TOKEN` 进行身份验证。
- `./start_portal.sh` 脚本会在启动后端服务前加载并生成 `.portal_auth` 文件，并导出 `RESEARCHVAULT_PORTAL_TOKEN`。
- 使用令牌登录：访问地址格式为 `#token=<token>`（令牌来自 `.portal_auth` 文件）。
- 允许访问的数据库目录由 `RESEARCHVAULT_PORTAL_ALLOWED_DB_ROOTS` 控制（默认为 `~/.researchvault` 和 `/tmp`）。
- 只有在 `RESEARCHVAULT_PORTAL_SCAN_OPENCLAW=1` 且 `~/.openclaw/workspace` 位于允许的数据库目录内时，才会执行 OpenClaw 工作空间扫描。
- 提供者密钥（`BRAVE_API_KEY`、`SERPER_API_KEY`、`SEARXNG_BASE_URL`）仅通过环境变量传递，并且仅在 `RESEARCHVAULT_PORTAL_INJECT_SECRETS=1` 时才会被注入到子进程中。
- 支持通过以下两种方式访问门户：
  - `http://127.0.0.1:5173/#token=<token>`
  - `http://localhost:5173/#token=<token>`
- 可用的操作命令：
   ```bash
./start_portal.sh --status
./start_portal.sh --stop
```

**与 CLI 的安全性一致**：
- 默认情况下会阻止 SSRF 攻击（禁止访问私有网络/本地网络/本地链接目标）。
- 门户中的 “允许私有网络” 设置与 CLI 命令 `--allow-private-networks` 具有相同的效果。

## 可选服务（需手动启动）

- **MCP 服务器**：`python scripts/services/mcp_server.py`
- **监控工具**：`python scripts/services/watchdog.py --once`

## 项目维护与信息来源

- **维护者**：lraivisto
- **许可证**：MIT 许可证
- **问题反馈**：[GitHub 问题列表](https://github.com/lraivisto/ResearchVault/issues)
- **安全性**：详见 [SECURITY.md](SECURITY.md) 文件。