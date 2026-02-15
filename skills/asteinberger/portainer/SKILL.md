---
name: portainer
description: 通过 Portainer API 控制 Docker 容器和容器组：可以列出容器、启动/停止/重启容器、查看日志，以及从 Git 仓库重新部署容器组。
metadata: {"clawdbot":{"emoji":"🐳","requires":{"bins":["curl","jq"],"env":["PORTAINER_API_KEY"]},"primaryEnv":"PORTAINER_API_KEY"}}
---

# 🐳 Portainer 技能

```
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🐳  P O R T A I N E R   C O N T R O L   C L I  🐳      ║
    ║                                                           ║
    ║       Manage Docker containers via Portainer API          ║
    ║            Start, stop, deploy, redeploy                  ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
```

> “Docker 容器？那对我来说小菜一碟。” 🐸

---

## 📖 这个技能的作用是什么？

**Portainer 技能** 允许你通过 Portainer 的 REST API 来控制你的 Docker 基础设施。无需使用 Web UI，即可管理容器、容器组（Stacks）和部署任务。

**功能包括：**
- 📊 **状态** — 检查 Portainer 服务器的状态
- 🖥️ **端点（Endpoints）** — 列出所有 Docker 环境
- 📦 **容器（Containers）** — 列出、启动、停止、重启容器
- 📚 **容器组（Stacks）** — 列出和管理 Docker Compose 容器组
- 🔄 **重新部署（Redeploy）** — 从 Git 中拉取代码并重新部署容器组
- 📜 **日志（Logs）** — 查看容器日志

---

## ⚙️ 需求

| 需求 | 详细信息 |
|------|---------|
| **Portainer** | 版本 2.x 及以上，且支持 API 访问 |
| **工具** | `curl`, `jq` |
| **认证** | API 访问令牌 |

### 设置

1. **从 Portainer 获取 API 令牌：**
   - 登录 Portainer Web UI
   - 点击用户名 → 我的账户（My Account）
   - 向下滚动至 “访问令牌”（Access Tokens） → 添加访问令牌
   - 复制令牌（此令牌之后将无法再次查看！）

2. **配置凭据：**
   ```bash
   # Add to ~/.clawdbot/.env
   PORTAINER_URL=https://your-portainer-server:9443
   PORTAINER_API_KEY=ptr_your_token_here
   ```

3. **设置完成！** 🚀

---

## 🛠️ 命令

### `status` — 检查 Portainer 服务器状态

```bash
./portainer.sh status
```

**输出：**
```
Portainer v2.27.3
```

---

### `endpoints` — 列出所有 Docker 环境

```bash
./portainer.sh endpoints
```

**输出：**
```
3: portainer (local) - ✓ online
4: production (remote) - ✓ online
```

---

### `containers` — 列出所有容器

```bash
# List containers on default endpoint (4)
./portainer.sh containers

# List containers on specific endpoint
./portainer.sh containers 3
```

**输出：**
```
steinbergerraum-web-1    running    Up 2 days
cora-web-1               running    Up 6 weeks
minecraft                running    Up 6 weeks (healthy)
```

---

### `stacks` — 列出所有容器组

```bash
./portainer.sh stacks
```

**输出：**
```
25: steinbergerraum - ✓ active
33: cora - ✓ active
35: minecraft - ✓ active
4: pulse-website - ✗ inactive
```

---

### `stack-info` — 查看容器组详情

```bash
./portainer.sh stack-info 25
```

**输出：**
```json
{
  "Id": 25,
  "Name": "steinbergerraum",
  "Status": 1,
  "EndpointId": 4,
  "GitConfig": "https://github.com/user/repo",
  "UpdateDate": "2026-01-25T08:44:56Z"
}
```

---

### `redeploy` — 从 Git 中拉取代码并重新部署容器组 🔄

```bash
./portainer.sh redeploy 25
```

**操作步骤：**
1. 从 Git 中拉取最新代码
2. 如有需要，重新构建容器
3. 重启容器组

---

### `start` / `stop` / `restart` — 控制容器的运行状态

```bash
# Start a container
./portainer.sh start steinbergerraum-web-1

# Stop a container
./portainer.sh stop steinbergerraum-web-1

# Restart a container
./portainer.sh restart steinbergerraum-web-1

# Specify endpoint (default: 4)
./portainer.sh restart steinbergerraum-web-1 4
```

**输出：**
```
✓ Container 'steinbergerraum-web-1' restarted
```

---

### `logs` — 查看容器日志

```bash
# Last 100 lines (default)
./portainer.sh logs steinbergerraum-web-1

# Last 50 lines
./portainer.sh logs steinbergerraum-web-1 4 50
```

---

## 🎯 示例工作流程

### 🚀 “部署网站更新”
```bash
# After merging PR
./portainer.sh redeploy 25
./portainer.sh logs steinbergerraum-web-1 4 20
```

### 🔧 “调试容器”
```bash
./portainer.sh containers
./portainer.sh logs cora-web-1
./portainer.sh restart cora-web-1
```

### 📊 “系统概览”
```bash
./portainer.sh status
./portainer.sh endpoints
./portainer.sh containers
./portainer.sh stacks
```

---

## 🔧 故障排除

### ❌ “需要认证 / 未找到仓库”

**问题：** 由于认证错误导致容器组重新部署失败

**解决方法：** 容器组配置中需要 `repositoryGitCredentialID` 参数。脚本会自动从现有配置中读取该参数。

---

### ❌ “找不到容器”

**问题：** 容器名称不匹配

**解决方法：** 使用 `./portainer.sh containers` 文件中提供的完整容器名称：
- 请使用完整名称，例如 `steinbergerraum-web-1` 而不是 `steinbergerraum`
- 容器名称区分大小写

---

### ❌ “必须设置 PORTAINER_URL 和 PORTAINER_API_KEY”

**问题：** 凭据未配置

**解决方法：**
```bash
# Add to ~/.clawdbot/.env
echo "PORTAINER_URL=https://your-server:9443" >> ~/.clawdbot/.env
echo "PORTAINER_API_KEY=ptr_your_token" >> ~/.clawdbot/.env
```

---

## 🔗 与 Clawd 的集成

```
"Redeploy the website"
→ ./portainer.sh redeploy 25

"Show me running containers"
→ ./portainer.sh containers

"Restart the Minecraft server"
→ ./portainer.sh restart minecraft

"What stacks do we have?"
→ ./portainer.sh stacks
```

---

## 📜 更新日志

| 版本 | 日期 | 更改内容 |
|---------|------|---------|
| 1.0.0 | 2026-01-25 | 初始发布 |

---

## 🐸 致谢

```
  @..@
 (----)
( >__< )   "Containers are just fancy lily pads
 ^^  ^^     for your code to hop around!"
```

**作者：** Andy Steinberger（在 Clawdbot Owen the Frog 的帮助下完成）  
**技术支持：** [Portainer](https://portainer.io/) API  
**所属项目：** [Clawdbot](https://clawdhub.com) 技能库

---

<div align="center">

**专为 Clawdbot 社区精心制作**

*Ribbit!* 🐸

</div>