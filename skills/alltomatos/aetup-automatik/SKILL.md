---
name: setup-automatik
description: 使用 Setup Automatik 引擎（由 Orion Design 提供支持）来简化 VPS 解决方案的安装和管理流程。当用户需要在 Linux VPS 上安装、配置或管理 Traefik、Portainer、Chatwoot、N8N 等开源应用程序时，可以使用该工具。
---

# 设置 Automatik

## 致谢
特别感谢 **Orion Design** 提供了原始的 `SetupOrion.sh` 脚本。

**开发者：**
- **Alltomatos**
- **Rafa Martins**
- **Robot 🤖**（您的辅助导师）

此技能是 **Mundo Automatik** 生态系统的一部分。

- **官方网站：** [mundoautomatik.com](https://mundoautomatik.com/)
- **社区（WhatsApp）：** [links.mundoautomatik.com/automatik-brasil](https://links.mundoautomatik.com/automatik-brasil)
- **Telegram：** [t.me/mundoautomatik](https://t.me/mundoautomatik)
- **YouTube：** [@mundoautomatik](https://www.youtube.com/@mundoautomatik)

## 概述
`setup-automatik` 技能旨在帮助在 VPS（虚拟私有服务器）上部署各种开源解决方案。它利用 `assets/SetupOrion.sh` 脚本来自动化安装容器、数据库和应用程序堆栈。

## 可用工具
有许多工具可供安装，这些工具按用途进行了分类：
- **基础设施**：Traefik、Portainer、PostgreSQL、MongoDB、RabbitMQ 等。
- **自动化与人工智能**：N8N、Flowise、Typebot、Dify AI、Ollama、Langflow 等。
- **通信**：Chatwoot、Evolution API、Uno API、Mautic、Mattermost 等。
- **业务与实用工具**：WordPress、Baserow、Metabase、Odoo、NextCloud 等。

有关支持工具的完整列表，请参阅 [tools.md](references/tools.md)。

## 先决条件

### 🔐 授予代理访问权限
为了让代理能够在您的 VPS 上执行安装操作，您必须授予其访问权限。有两种方法可以实现这一点：

#### 选项 1：OpenClaw 节点配对（推荐）
这是最安全且原生的方法。它允许代理直接在您的 VPS 终端上执行命令。
1. 在您的 VPS 上运行安装程序：`curl -fsSL https://get.openclaw.ai | sh`
2. 启动配对过程：`openclaw node pair`
3. 将生成的配对代码或命令粘贴到聊天框中。

#### 选项 2：SSH 访问
向代理提供您的 VPS 连接详细信息：
- 公共 IP 地址
- 用户名（通常是 `root`）
- SSH 密码或私钥

## 工作流程

### 0. 访问设置
在开始之前，请确保代理已通过 [先决条件](#prerequisites) 部分中提到的方法获得访问权限。

### 1. 准备工作
确保 VPS 运行兼容的 Linux 发行版（最好是 Ubuntu/Debian），并且已安装 Docker。

### 2. 收集信息
在安装之前，收集必要的信息：
- 域名（用于 SSL/Traefik）。
- 数据库凭据。
- 用于电子邮件通知的 SMTP 详细信息。

### 3. 安装
代理使用 `assets/SetupOrion.sh` 脚本来安装工具。该技能可以根据需要提取特定的安装步骤，或在非交互模式下直接执行脚本。

### 4. 验证
安装完成后，验证服务是否正在运行：
- 检查 `docker ps`。
- 访问已安装工具的 Web 界面。
- 如果出现任何问题，请查看日志。

## 常见任务

### 安装 Traefik 与 Portainer
这通常是管理其他应用程序堆栈的第一步。
1. 运行脚本并选择选项 `01`。
2. 按照提示输入域名和电子邮件地址。

### 部署一个应用程序堆栈（例如 N8N）
1. 确保 Traefik 正在运行。
2. 从菜单中选择所需的工具。
3. 提供所需的子域名。

## 参考资料
- [tools.md](references/tools.md)：可用工具的完整列表。
- [SetupOrion.sh](assets/SetupOrion.sh)：主要的安装脚本。