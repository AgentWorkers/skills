---
name: Infrastructure
slug: infrastructure
version: 1.0.1
description: 设计、配置并连接跨服务器、网络和服务的云资源。
changelog: User-driven credential model, explicit tool requirements
metadata: {"clawdbot":{"emoji":"🏗️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 范围

本技能：
- ✅ 指导架构决策
- ✅ 提供用户可执行的配置命令
- ✅ 文档化基础设施模式

**以用户为中心的模型：**
- 用户在需要时提供云服务凭证
- 用户运行配置命令
- 本技能提供决策指导并生成相应的命令

**本技能不执行以下操作：**
- ❌ 直接存储或访问云服务凭证
- ❌ 自动运行配置命令
- ❌ 未经用户确认的情况下修改基础设施

**实施方式：** 用户运行本技能提供的命令，或使用 `server` 技能来执行这些命令。

## 快速参考

| 主题 | 文件 |
|-------|------|
| 架构模式 | `patterns.md` |
| 提供商相关命令 | `providers.md` |
| 备份策略 | `backups.md` |

## 核心规则

### 1. 用户运行命令
本技能生成命令，由用户执行：
```
Agent: "To create the server, run:
        hcloud server create --name web1 --type cx21 --image ubuntu-24.04
        
        This requires HCLOUD_TOKEN in your environment."
User: [runs command]
```

### 2. 必需工具（用户自行安装）
| 提供商 | 工具 | 安装方式 |
|----------|------|---------|
| Hetzner | `hcloud` | 使用 `brew install hcloud` 安装 |
| AWS | `aws` | 使用 `brew install awscli` 安装 |
| DigitalOcean | `doctl` | 使用 `brew install doctl` 安装 |
| Docker | `docker` | 安装 Docker Desktop |

### 3. 凭证处理
- 用户将凭证设置到自己的环境变量中
- 本技能从不存储或记录凭证信息
- 命令会引用环境变量：`$HCLOUD_TOKEN`、`$AWS_ACCESS_KEY_ID`

### 4. 架构建议

| 阶段 | 推荐方案 |
|-------|-------------|
| MVP 阶段 | 单个虚拟专用服务器（VPS）+ Docker Compose |
| 扩展阶段 | 专用数据库+负载均衡器 |
| 扩展到多区域阶段 | 多区域部署+内容分发网络（CDN） |

### 5. 决策框架
| 问题 | 答案 |
|----------|--------|
| 如何构建基础设施？ | ✅ 请使用本技能 |
| 是否需要添加更多服务器？ | ✅ 请使用本技能 |
| 如何配置 Nginx？ | 请使用 `server` 技能 |
| 如何编写 Dockerfile？ | 请使用 `docker` 技能 |

### 6. 备份策略
| 数据类型 | 备份方法 | 备份频率 |
|------|--------|-----------|
| 数据库 | 使用 `pg_dump` 备份到 S3/B2 | 每日 |
| 磁盘卷 | 创建快照 | 每周 |
| 配置文件 | 使用 Git 进行版本控制 | 每次修改后 |