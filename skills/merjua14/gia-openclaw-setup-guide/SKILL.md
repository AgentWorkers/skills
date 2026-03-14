# OpenClaw 设置指南

本指南帮助用户从零开始安装和配置 OpenClaw，内容包括安装流程、通道连接、技能设置以及首个自动化工作流的创建。

## 本指南的作用

本指南将引导新用户完成以下操作：
1. 在他们的计算机（Mac/Linux/Windows WSL）上安装 OpenClaw。
2. 运行入门向导。
3. 连接消息传递通道（Telegram、Discord、WhatsApp、Slack）。
4. 安装并配置所需技能。
5. 设置首个自动化工作流。
6. 配置心跳检测和定时任务（cron jobs）。
7. 设置相关配置文件（如身份文件等）。

## 使用方法

当用户请求 OpenClaw 的设置帮助时，请按照以下步骤操作：

### 第一步：系统检查
```bash
# Check OS and prerequisites
uname -a
node --version  # Need Node.js 18+
git --version
```

### 第二步：安装 OpenClaw
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

### 第三步：连接通道
```bash
# For Telegram (most common)
openclaw channels add telegram
# Follow prompts for bot token from @BotFather

# For Discord
openclaw channels add discord
# Provide bot token from Discord Developer Portal
```

### 第四步：配置身份信息
在工作区创建以下文件：
- `SOUL.md`：代理的个性和行为设置。
- `USER.md`：关于人类的信息。
- `AGENTS.md`：操作流程。
- `IDENTITY.md`：名称、表情符号和头像。

### 第五步：安装技能
```bash
# Browse available skills
openclaw skills search <keyword>

# Install a skill
openclaw skills install <skill-name>
```

### 第六步：设置自动化任务
- 在 OpenClaw 配置文件中设置心跳检测间隔。
- 为重复性任务设置定时任务（cron jobs）。
- 创建 `HEARTBEAT.md` 文件以执行主动行为。

### 第七步：测试首个工作流
向已连接的通道中的代理发送消息，尝试执行以下操作：
- “在网络上搜索 [主题]”。
- “阅读并总结 [文件]”。
- “为 [时间] 设置提醒”。

## 故障排除

### 常见问题
- **Node.js 版本过低**：`nvm install 22 && nvm use 22`
- **权限问题**：`sudo chown -R $USER ~/.openclaw`
- **机器人未响应**：检查 `openclaw status` 和 `openclaw gateway logs` 日志。
- **通道连接失败**：验证令牌信息，检查防火墙/代理设置。

## 确认要求
- Node.js 18 及以上版本（推荐使用 22 版本）。
- 至少 2GB 的内存。
- 支持 macOS、Linux 或安装了 WSL2 的 Windows 系统。
- 需要互联网连接以使用 API 功能。

## 成本
- OpenClaw 本身：免费（开源软件）。
- AI 模型 API：根据使用情况，每月费用约为 5-50 美元。
- 托管服务（可选）：每月费用为 5-20 美元（适用于持续运行的服务）。