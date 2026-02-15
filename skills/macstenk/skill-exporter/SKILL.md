---
name: skill-exporter
description: 将 Clawdbot 的技能导出为独立的、可部署的微服务。当您希望将某个技能容器化（使用 Docker），部署到 Railway 或 Fly.io，或创建一个独立的 API 服务时，可以使用此功能。该功能会生成 Dockerfile、FastAPI 包装器、requirements.txt 文件、部署配置文件，以及可选的 LLM 客户端集成相关文件。
license: MIT
compatibility: Requires python3. Works with any AgentSkills-compatible agent.
metadata:
  author: MacStenk
  version: "1.0.0"
  clawdbot:
    emoji: "📦"
    requires:
      bins:
        - python3
---

# 技能导出器（Skill Exporter）

将 Clawdbot 的技能转换为可独立部署的微服务。

## 工作流程

```
Clawdbot Skill (tested & working)
         ↓
    skill-exporter
         ↓
Standalone Microservice
         ↓
Railway / Fly.io / Docker
```

## 使用方法

### 导出技能

```bash
python3 {baseDir}/scripts/export.py \
  --skill ~/.clawdbot/skills/instagram \
  --target railway \
  --llm anthropic \
  --output ~/projects/instagram-service
```

### 参数选项

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--skill` | 技能目录的路径 | 必需 |
| `--target` | 部署目标：`railway`、`fly`、`docker` | `docker` |
| `--llm` | LLM（大语言模型）提供商：`anthropic`、`openai`、`none` | `none` |
| `--output` | 输出目录 | `./<技能名称>-service` |
| `--port` | API 端口 | `8000` |

### 部署目标

- **railway**：生成 `railway.json` 文件、优化的 Dockerfile 以及健康检查脚本 |
- **fly**：生成 `fly.toml` 文件，支持多区域部署 |
- **docker**：生成通用的 Dockerfile 和 `docker-compose.yml` 文件 |

### LLM 集成

当设置 `--llm` 时，会生成 `llm_client.py` 文件，其中包含：
- 标题/提示生成功能 |
- 决策辅助工具 |
- 速率限制和错误处理机制 |

## 生成的内容

```
<skill>-service/
├── Dockerfile
├── docker-compose.yml
├── api.py              # FastAPI wrapper
├── llm_client.py       # If --llm specified
├── requirements.txt
├── .env.example
├── railway.json        # If --target railway
├── fly.toml            # If --target fly
└── scripts/            # Copied from original skill
    └── *.py
```

## 要求

源技能必须满足以下条件：
- 包含具有有效元数据（frontmatter）的 `SKILL.md` 文件 |
- `scripts/` 目录中至少有一个可执行的脚本 |
- 脚本应为可调用的函数形式（而不仅仅是内联代码）

## 导出后的操作

1. 将 `.env.example` 文件复制到 `.env` 文件，并填写相应的配置信息 |
2. 在本地进行测试：`docker-compose up` |
3. 部署服务：`railway up` 或 `fly deploy`