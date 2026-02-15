# SOTA Tracker

**这是一个权威的、开源的AI模型最新技术（State-of-the-Art, SOTA）数据库。**

数据每日自动从 [LMArena](https://lmarena.ai)、[Artificial Analysis](https://artificialanalysis.ai) 和 [HuggingFace](https://huggingface.co) 更新。

## 项目存在的意义

AI模型每周都有新的发布，手动跟踪这些模型的更新情况几乎是不可能的。本项目旨在：
1. **整理权威的数据**——包括 LMArena 的 Elo 排名以及针对视频/图像/音频模型的手动审核结果；
2. **通过 GitHub Actions 每日更新数据库**；
3. **提供多种数据导出格式**（JSON、CSV、SQLite），方便用户在自己的项目中使用；
4. **提供多种访问接口**——静态文件、REST API 或 MCP 服务器。

## 快速入门：如何使用数据

### 选项 1：下载 JSON/CSV 数据

```bash
# Latest data (updated daily)
curl -O https://raw.githubusercontent.com/romancircus/sota-tracker-mcp/main/data/sota_export.json
curl -O https://raw.githubusercontent.com/romancircus/sota-tracker-mcp/main/data/sota_export.csv
```

### 选项 2：克隆代码并在本地查询数据

```bash
git clone https://github.com/romancircus/sota-tracker-mcp.git
cd sota-tracker-mcp

# Query with sqlite3
sqlite3 data/sota.db "SELECT name, sota_rank FROM models WHERE category='llm_api' ORDER BY sota_rank LIMIT 10"

# List forbidden/outdated models
sqlite3 data/sota.db "SELECT name, reason, replacement FROM forbidden"
```

### 选项 3：结合 Claude Code 使用（推荐）

对于 Claude Code 用户，推荐使用 **静态文件嵌入** 的方式（这种方式比使用 MCP 服务器更节省 API 带宽）：

```bash
# Set up daily auto-update of CLAUDE.md
cp scripts/update_sota_claude_md.py ~/scripts/

# Enable systemd timer (runs at 6 AM daily)
systemctl --user enable --now sota-update.timer

# Or run manually
python ~/scripts/update_sota_claude_md.py --update
```

通过这种方式，您可以直接将 SOTA 模型的相关信息嵌入到您的 `~/.claude/CLAUDE.md` 文件中。

### 选项 4：使用 REST API

```bash
# Start the API server
uvicorn rest_api:app --host 0.0.0.0 --port 8000

# Query endpoints
curl "http://localhost:8000/api/v1/models?category=llm_api"
curl "http://localhost:8000/api/v1/forbidden"
curl "http://localhost:8000/api/v1/models/FLUX.1-dev/freshness"
```

### 选项 5：使用 MCP 服务器（可选）

虽然支持 MCP 服务器，但默认是关闭的（使用 MCP 服务器会消耗更多的 API 带宽）。如需启用，请按照以下步骤操作：

```bash
# Edit .mcp.json to add the server config
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "sota-tracker": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
EOF
```

## 数据来源

| 数据来源 | 提供的数据类型 | 更新频率 |
|--------|------------------|------------------|
| [LMArena](https://lmarena.ai/leaderboard) | 大语言模型（LLM）Elo 排名（基于 600 万条人类评分） | 每日 |
| [Artificial Analysis](https://artificialanalysis.ai) | LLM 基准测试结果、模型定价信息 | 每日 |
| [HuggingFace](https://huggingface.co) | 模型下载信息、模型热度排名 | 每日 |
| 手动审核数据 | 视频、图像、音频模型 | 根据需要更新 |

## 分类

| 分类 | 描述 | 2026 年 2 月的顶级模型 |
|----------|-------------|----------------------|
| `llm_api` | 云端大语言模型 API | Gemini 3 Pro、Grok 4.1、Claude Opus 4.5 |
| `llm_local` | 本地大语言模型 | Qwen3、Llama 3.3、DeepSeek-V3 |
| `llm_coding` | 专注于代码生成的大语言模型 | Qwen3-Coder、DeepSeek-V3 |
| `image_gen` | 图像生成模型 | Z-Image-Turbo、FLUX.2-dev、Qwen-Image |
| `video` | 视频生成模型 | LTX-2、Wan 2.2、HunyuanVideo 1.5 |
| `video2audio` | 视频转音频模型 | MMAudio V2 Large |
| `tts` | 文本转语音模型 | ChatterboxTTS、F5-TTS |
| `stt` | 语音转文本模型 | Whisper Large v3 |
| `embeddings` | 向量嵌入模型 | BGE-M3 |

## REST API 端点

| 端点 | 功能描述 |
|----------|-------------|
| `GET /api/v1/models?category=X` | 获取指定分类下的最新模型信息 |
| `GET /api/v1/models/:name/freshness` | 检查模型是否为最新版本 |
| `GET /api/v1/forbidden` | 获取需要避免使用的过时模型列表 |
| `GET /api/v1/compare?model_a=X&model_b=Y` | 比较两个模型 |
| `GET /api/v1/recent?days=30` | 获取过去 N 天内发布的模型 |
| `GET /api/v1/recommend?task=chat` | 根据任务需求推荐模型 |
| `GET /health` | 检查系统运行状态 |

## 运行自己的数据抓取脚本

```bash
# Install dependencies
pip install -r requirements.txt
pip install playwright
playwright install chromium

# Run all scrapers
python scrapers/run_all.py --export

# Output:
# data/sota_export.json
# data/sota_export.csv
# data/lmarena_latest.json
```

## 使用 GitHub Actions 自动更新数据

该项目通过 GitHub Actions 实现以下功能：
- **每日**：从所有数据来源抓取最新数据，更新数据库，并提交更改；
- **每周**：生成包含 JSON/CSV 数据的版本，并发布到仓库。

若要在您的代码仓库中启用自动更新功能，请按照以下步骤操作：
1. 克隆本项目；
2. 进入项目设置 → Actions，启用相关的工作流程；
3. 数据将在 UTC 时间 6 点自动更新。

## 项目文件结构

```
sota-tracker-mcp/
├── server.py                    # MCP server (optional)
├── rest_api.py                  # REST API server
├── init_db.py                   # Database initialization + seeding
├── requirements.txt             # Dependencies
├── data/
│   ├── sota.db                  # SQLite database
│   ├── sota_export.json         # Full JSON export
│   ├── sota_export.csv          # CSV export
│   └── forbidden.json           # Outdated models list
├── scrapers/
│   ├── lmarena.py               # LMArena scraper (Playwright)
│   ├── artificial_analysis.py   # AA scraper (Playwright)
│   └── run_all.py               # Unified runner
├── fetchers/
│   ├── huggingface.py           # HuggingFace API
│   └── cache_manager.py         # Smart caching
└── .github/workflows/
    └── daily-scrape.yml         # GitHub Actions workflow
```

## 如何贡献代码

如果您发现某个模型未被收录或排名有误，可以：
1. **手动添加数据**：修改 `init_db.py` 文件并提交 Pull Request；
2. **改进数据抓取脚本**：修改 `scrapers/` 目录下的相关文件；
3. **添加新的数据来源**：开发新的数据抓取脚本，并更新 `run_all.py` 文件。

详细开发指南和 Pull Request 提交流程请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 与 OpenCode / Agents.md 的集成

该项目支持更新 OpenCode 代理相关的 `agents.md` 文件：

```bash
# Update your agents.md with latest SOTA data
python update_agents_md.py

# Minimal version (top 1 model per category, lightweight)
python update_agents_md.py --minimal

# Custom categories and limit
python update_agents_md.py --categories llm_local image_gen --limit 3

# Force refresh from sources first
python update_agents_md.py --refresh
```

### 自动化更新

您可以通过 cron 任务或 systemd 定时任务来实现数据的每日自动更新：

```cron
# ~: crontab -e
@daily python ~/Apps/sota-tracker-mcp/update_agents_md.py
```

或者使用 systemd 服务：

```bash
# ~/.config/systemd/user/sota-update.service
[Unit]
Description=Update SOTA models for agents
After=network.target

[Service]
ExecStart=%h/Apps/sota-tracker-mcp/update_agents_md.py

[Install]
WantedBy=default.target

# ~/.config/systemd/user/sota-update.timer
[Unit]
Description=Daily SOTA data update
OnCalendar=daily
AccuracySec=1h

[Install]
WantedBy=timers.target

# Enable
systemctl --user enable --now sota-update.timer
```

完整的使用指南请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 数据来源与版权声明

本项目汇总了来自第三方来源的 **公开可用的基准测试数据**。我们不对这些数据的排名、Elo 分数或测试结果拥有所有权。

### 数据来源的使用许可

| 数据来源 | 提供的数据类型 | 使用许可 |
|--------|------|------------|
| [LMArena](https://lmarena.ai) | 聊天机器人竞技场 Elo 排名 | `robots.txt: Allow: /` |
| [Artificial Analysis](https://artificialanalysis.ai) | LLM 基准测试结果 | `robots.txt: Allow: /`（明确允许 AI 爬虫访问） |
| [HuggingFace](https://huggingface.co) | 模型元数据、模型下载信息 | 公开 API |
| [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm-leaderboard) | 开源大语言模型基准测试结果 | CC-BY 许可协议 |

### 免责声明

- 所有的基准测试分数和排名结果均属于其原始来源的知识产权；
- 本项目仅提供数据汇总和工具支持，不生成新的基准测试数据；
- 为减轻服务器负担，数据每天仅抓取一次；
- 如果您是数据来源的提供者且希望自己的数据不被收录，请提交问题。

## 公平使用原则

- 本项目仅汇总事实性数据（不受版权保护）；
- 通过提供 API 服务、统一的数据格式和过时模型列表等方式增加数据价值；
- 所有数据来源都会在文档中明确标注；
- 本项目不会与数据来源进行商业竞争；
- 严格遵守所有数据来源的 robots.txt 许可规定。

## 许可协议

本项目采用 MIT 许可协议。代码部分遵循 MIT 许可协议；数据部分归属于其原始来源（详见上述数据来源说明）。