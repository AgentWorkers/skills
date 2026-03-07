---
name: openclaw-self-clone-everything
description: Clone and deploy OpenClaw to a new VPS. Use when you need to install OpenClaw on a fresh remote server via SSH. Steps: (1) Verify SSH access (IP, user, password/key), (2) Install OpenClaw via official non-interactive script, (3) Copy ~/.openclaw data, (4) Prompt to update credentials (e.g., Telegram bot token).
---

# 将 OpenClaw 部署到新的 VPS

**概述：**  
使用 SSH 和非交互式安装程序将 OpenClaw 部署到新的 VPS，然后复制您的 `~/.opencl` 工作区，并验证/更新凭据。

## 先决条件  
- 具有对新 VPS 的 SSH 访问权限：IP 地址、用户名和密码（或 SSH 密钥）  
- 新 VPS 运行支持的 Linux 发行版（请参考官方文档进行确认）  
- 确保新 VPS 具有出站连接能力（以便下载安装程序）  

**安全提示：**  
当系统提示输入密码时，避免将密码硬编码到脚本中；建议使用密码提示或基于 SSH 密钥的身份验证方式。  

## 操作步骤  

### 第 1 步：验证 SSH 连接  
- 从当前环境测试对新 VPS 的访问是否正常。  
- **示例（交互式登录测试）：**  
  ```bash
  ssh USER@VPS_IP
  ```  
  （请将 `USER` 替换为实际提供的用户名，将 `VPS_IP` 替换为目标 IP 地址。）  
- 验证成功后，退出 SSH 会话。  

如果使用 SSH 密钥进行身份验证，请确保私钥可用，并设置适当的权限（例如 600）。  

### 第 2 步：通过非交互式脚本安装 OpenClaw  
- 在新 VPS 上以非交互式模式运行官方安装程序：  
  ```bash
  ssh USER@VPS_IP 'bash -c "$(curl -fsSL https://openclaw.ai/install.sh)" -- --no-onboard'
  ```  
  **说明：**  
  `-no-onboard` 选项会跳过交互式设置向导，直接执行安装过程。  

如果新 VPS 禁用了 `curl` 或无法访问 `https://openclaw.ai`，请先下载安装程序到本地，再使用 `scp` 将其传输到新 VPS，之后再运行 `bash install.sh --no-onboard`。  

### 第 3 步：将 `~/.opencl` 从源环境复制到新 VPS  
- **源路径（当前环境）：** `~/.openclaw`  
- **目标目录（新 VPS）：** `~/.openclaw`  
- 创建压缩文件，将其传输到新 VPS 并解压：  
  ```bash
  # Compress (on source)
  cd ~ && tar czf openclaw-data.tar.gz --exclude='*.log' --exclude='cache' --exclude='node_modules/.cache' .openclaw

  # Transfer
  scp openclaw-data.tar.gz USER@VPS_IP:~/

  # Extract (on new VPS)
  ssh USER@VPS_IP 'rm -rf ~/.openclaw && tar xzf ~/openclaw-data.tar.gz -C ~/'

  # Cleanup (optional, on both sides)
  rm openclaw-data.tar.gz
  ssh USER@VPS_IP 'rm ~/openclaw-data.tar.gz'
  ```  

**注意事项：**  
- 请仔细检查要复制的内容，避免复制不必要的临时文件或缓存文件。  
- 示例中排除了 `*.log`、`cache` 和 `node_modules/.cache` 文件以减小压缩包的大小；请根据您的目录结构进行调整。  
- 这是一次性传输，无需持续同步数据。  

### 第 4 步：更新或验证新 VPS 上的凭据（可选）  
- 提示用户：“您是否需要更新新 VPS 上的凭据（例如 Telegram 机器人令牌、API 密钥）？”  
- 如果用户回答“否”或“跳过”，则直接进入第 5 步；  
- 如果用户同意更新，请检查并修改新 `~/.opencl` 目录中的敏感设置：  
  - Telegram 机器人令牌和 API 密钥（通常位于 `~/.openclaw/config.*` 或相关配置文件中）  
  - 提供商凭据（如有）、Webhook 信息和服务地址  

**凭据获取方式：**  
- 查看 `~/.openclaw/config` 或相关配置文件以获取令牌和服务标识符。  
- 参考提供商提供的具体配置文件或环境设置。  

### 第 5 步：（可选）在新 VPS 上重启 OpenClaw 服务  
- ⚠️ 此步骤仅重启新 VPS 上的 OpenClaw 服务，不会影响当前环境。  
- 根据需要重启新 VPS 上的 OpenClaw 服务：  
  ```bash
  ssh USER@VPS_IP 'sudo systemctl restart openclaw || openclaw restart || echo "Restart manually per your system"'
  ```  
- 通过查看日志或访问 OpenClaw 的 Web 界面来确认服务是否正常运行。  

## 安装后的检查  
- 确认新 VPS 上已成功部署 OpenClaw：  
  - 检查服务状态（例如：`ssh USER@VPS_IP 'sudo systemctl status openclaw'`）。  
- 查看日志以检查是否有错误（例如：`ssh USER@VPS_IP 'journalctl -u openclaw -n 50'`）。  
- 确认工作区和代理程序在新 VPS 上正确显示。  
- 通过简单请求或健康检查来测试与提供商/Telegram 机器人的连接是否正常。  

**安全与维护建议：**  
- 定期更新环境特定的凭据或令牌。  
- 限制 SSH 访问权限：禁用密码认证，使用基于密钥的身份验证方式，并配置防火墙规则。  
- 确保源环境和新 VPS 上的 OpenClaw 都保持最新版本。  

**故障排除：**  
- 如果安装程序在 SSH 过程中失败，请检查出站连接是否正常以及是否具备必要的工具（`curl` 和 `bash`）。  
- 如果遇到 `rsync` 错误，请确认目标目录存在且具有写入权限。  
- 如需缩小日志输出范围，可以适当调整命令参数。  
- 如果凭据不匹配，请在新 VPS 上更新相应的值。  
- 避免将敏感信息提交到版本控制系统中，建议使用环境变量或专门的密钥管理工具。