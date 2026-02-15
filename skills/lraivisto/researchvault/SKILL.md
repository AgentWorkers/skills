---
name: researchvault
description: "本地优先的研究调度引擎。负责管理状态、数据合成以及可选的后台服务（如 MCP/Watchdog）。"
homepage: https://github.com/lraivisto/ResearchVault
disable-model-invocation: true
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "python": ">=3.13" },
        "install":
          [
            {
              "id": "vault-venv",
              "kind": "exec",
              "command": "python3 -m venv .venv && . .venv/bin/activate && pip install -e .",
              "label": "Initialize ResearchVault (Standard)",
            },
          ],
        "config":
          {
            "env":
              {
                "RESEARCHVAULT_DB":
                  {
                    "description": "Optional: Custom path to the SQLite database file.",
                    "required": false,
                  },
                "BRAVE_API_KEY":
                  {
                    "description": "Optional: API key for live web search and verification. Set in skills.entries.researchvault.env.BRAVE_API_KEY.",
                    "required": false,
                  },
              },
          },
      },
  }
---

# ResearchVault 🦞

**以本地数据为中心的研究编排引擎。**

ResearchVault 负责管理代理的持久化状态、数据合成以及自动验证功能。

## 安全性与隐私（以本地数据为主）  
- **本地存储**：所有数据都存储在本地 SQLite 数据库（路径：`~/.researchvault/research_vault.db`）中，不进行任何云同步。  
- **网络访问控制**：仅在执行用户请求的研究任务或启用 Brave Search 功能时才会建立出站连接（如配置了相关选项）。  
- **SSRF（安全套接字层转发）加固**：默认情况下会严格限制内部网络访问，屏蔽本地/私有 IP 地址（如 `localhost`、`10.0.0.0/8` 等）。可通过 `--allow-private-networks` 参数来覆盖此设置。  
- **手动启动的服务**：后台监控程序和 MCP 服务器位于 `scripts/services/` 目录中，需要手动启动。  
- **严格限制**：设置 `disable-model-invocation: true` 可防止模型自动启动后台任务。  

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
3. **自动策略执行**：  
   ```bash
   python scripts/vault.py strategy --id "trends-2026"
   ```  

## 可选服务（需手动启动）  
- **MCP 服务器**：`python scripts/services/mcp_server.py`  
- **监控程序**：`python scripts/services/watchdog.py --once`  

## 来源信息与维护  
- **维护者**：lraivisto  
- **许可证**：MIT 许可证  
- **问题反馈**：[GitHub 问题页面](https://github.com/lraivisto/ResearchVault/issues)  
- **安全性说明**：请参阅 [SECURITY.md](SECURITY.md) 文件。