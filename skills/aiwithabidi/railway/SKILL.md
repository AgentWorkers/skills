---
name: railway
description: "铁路部署平台——项目、服务、部署、变量。应用程序托管的命令行界面（CLI）。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🚂", "requires": {"env": ["RAILWAY_API_TOKEN"]}, "primaryEnv": "RAILWAY_API_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 🚂 Railway

应用部署——包括项目、服务、部署过程以及相关变量管理。

## 主要功能

- **项目**：创建、列出、查询项目信息
- **服务**：列出项目中的服务
- **部署**：查看部署状态
- **变量**：管理环境变量

## 系统要求

| 变量 | 必需性 | 说明 |
|----------|----------|-------------|
| `RAILWAY_API_TOKEN` | ✅ | Railway API 的密钥/令牌 |

## 快速入门

```bash
python3 {baseDir}/scripts/railway.py projects
python3 {baseDir}/scripts/railway.py project <id>
python3 {baseDir}/scripts/railway.py services <project-id>
python3 {baseDir}/scripts/railway.py me
```

## 致谢

本工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码仓库位于 [GitHub](https://github.com/aiwithabidi)。  
本工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)