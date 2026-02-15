---
name: security-dashboard
description: OpenClaw 和 Linux 服务器基础设施的实时安全监控仪表板。该仪表板可监控网关状态、网络安全状况、系统公开程度、系统更新情况、SSH 访问情况、TLS 证书以及资源使用情况。
---

# 安全监控面板技能  
（Security Monitoring Dashboard Skill）  

这是一个用于 OpenClaw 和 Linux 服务器基础设施的实时安全监控面板。  

## 主要功能  
- **OpenClaw 安全性监控：** 网关状态、绑定配置、身份验证、会话信息、版本跟踪  
- **网络安全：** Tailscale 连接状态、公共端口、防火墙状态、活跃连接数  
- **公开暴露风险：** 端口绑定分析、面板安全性评估、暴露程度判定  
- **系统安全性：** 系统更新信息、运行时间、负载情况、登录失败记录  
- **SSH 与访问控制：** 密码认证状态、fail2ban 配置、被禁止的 IP 地址、活跃会话  
- **证书与 TLS：** Caddy 服务器状态、TLS 配置、WireGuard 加密设置  
- **资源使用情况：** CPU/内存/磁盘使用率、配置文件权限  

## 安装步骤  

### 1. 安装该技能  
```bash
cd /root/clawd/skills/security-dashboard
sudo ./scripts/install.sh
```  

安装过程将：  
- **询问用户偏好：** 是否以专用用户（推荐）或 root 用户身份运行  
- 如果非 root 用户，创建具有有限 sudo 权限的 `openclaw-dashboard` 用户  
- 创建带有安全加固功能的 systemd 服务  
- 配置仅绑定到本地主机（127.0.0.1）  
- 在端口 18791 上启动监控面板  
- 设置系统启动时自动启动该服务  

**安全提示：** 建议以具有有限 sudo 权限的专用用户身份运行该服务。监控面板仅在需要执行安全检查（如 fail2ban、防火墙配置、systemctl 命令）时才需要 root 权限，无需完全的 root 权限。  

### 2. 访问监控面板  
**仅限本地主机（默认为安全模式）：**  
通过 SSH 端口转发访问：  
```bash
ssh -L 18791:localhost:18791 root@YOUR_SERVER_IP
```  
然后访问：`http://localhost:18791`  

## 使用方法  
- **启动/停止/重启监控面板：**  
```bash
sudo systemctl start security-dashboard
sudo systemctl stop security-dashboard
sudo systemctl restart security-dashboard
```  
- **查看面板状态：**  
```bash
sudo systemctl status security-dashboard
```  
- **查看日志：**  
```bash
sudo journalctl -u security-dashboard -f
```  
- **获取原始安全数据：**  
```bash
curl http://localhost:18791/api/security | jq
```  

## 安全加固措施  
该监控面板遵循最佳安全实践，以最小化攻击面：  

### 推荐使用专用用户  
安装脚本会创建一个具有 **有限 sudo 权限** 的 `openclaw-dashboard` 用户：  
- ✅ 无 shell 访问权限（`/bin/false`）  
- ✅ 无个人目录  
- ✅ 仅允许执行特定的 sudo 命令（如 fail2ban、防火墙配置、systemctl 命令）  
- ✅ 无法执行任意命令  

### systemd 安全加固  
该服务运行时受到严格的安全限制：  
```ini
NoNewPrivileges=true      # Cannot escalate privileges
PrivateTmp=true          # Isolated tmp directory
ProtectSystem=strict     # Read-only filesystem except skill dir
ProtectHome=true         # No access to /home
ReadWritePaths=...       # Only skill directory is writable
Restart=on-failure       # Restart only on crashes (not always)
```  

### 网络绑定设置  
- **默认设置：** 仅绑定到本地主机（127.0.0.1）  
- 无法通过非 SSH 隧道或 VPN 从外部访问  
- 无公开暴露风险  

### 不建议以 root 用户身份运行  
如果在安装时选择 root 用户：  
- ⚠️ 一旦被攻击，将获得完整系统访问权限  
- ⚠️ 无法实现权限分离  
- ⚠️ 仅适用于受信任的、隔离的环境  

在生产环境中，请务必使用专用用户。  

## 配置选项  

### 更改端口号  
编辑 `/root/clawd/skills/security-dashboard/server.js` 文件：  
```javascript
const PORT = 18791; // Change this
```  
然后重启服务：  
```bash
sudo systemctl restart security-dashboard
```  

### 更改绑定地址  
- **默认设置：** 仅绑定到本地主机（127.0.0.1）  
- **备选设置：** 绑定到所有网络接口（0.0.0.0，仅适用于使用 Tailscale 的环境）  
编辑 `server.js` 文件的第 445 行：  
```javascript
server.listen(PORT, '127.0.0.1', () => {
  // Change '127.0.0.1' to '0.0.0.0' if needed
});
```  
**注意：** 仅在通过 Tailscale 或防火墙保护的环境下才能将绑定地址设置为 0.0.0.0！  

### 自定义监控指标  
可以在 `server.js` 文件中添加自定义监控指标：  
- `getOpenClawMetrics()`：OpenClaw 相关指标  
- `getNetworkMetrics()`：网络安全指标  
- `getSystemMetrics()`：系统级指标  
- `getPublicExposure()`：端口/绑定配置分析  

## 监控面板各部分说明  

### 🦞 OpenClaw 安全性  
- 网关运行状态  
- 绑定配置（本地/公共网络）  
- 身份验证令牌长度及模式  
- 活跃会话数及子代理数量  
- 技能（Skill）数量  
- 当前版本及更新可用性  

### 🌐 网络安全  
- Tailscale 连接状态及 IP 地址  
- 公共端口数量  
- 防火墙状态（UFW/Firewalld）  
- 活跃的 TCP 连接数  

### 🌍 公开暴露风险  
- 暴露程度（优秀/最低/警告/高）  
- 公共端口详细信息  
- Kanban 板绑定状态  
- OpenClaw 网关绑定状态  
- Tailscale 的激活/关闭状态  
- 安全建议  

### 🖥️ 系统安全性  
- 可用的系统更新  
- 服务器运行时间  
- 平均负载  
- 24 小时内的登录失败记录  
- root 进程数量  

### 🔑 SSH 与访问控制  
- SSH 服务状态  
- 密码认证状态（启用/禁用）  
- fail2ban 配置  
- 被禁止的 IP 地址数量  
- 活跃的 SSH 会话  

### 📜 证书与 TLS  
- Caddy 服务器状态  
- TLS 功能的启用/禁用  
- WireGuard 加密状态  

### 📊 资源使用情况  
- CPU/内存/磁盘使用率  
- 配置文件权限（应为 600）  

## 安全警报  
监控面板会生成实时警报：  
- **严重警告（红色）：** 网关令牌长度过短（< 32 个字符）  
- SSH 密码认证功能启用  
- 配置文件权限不安全（非 600 权限）  
- 防火墙未启用（UFW/Firewalld 不运行）  
- fail2ban 功能未启用（SSH 暴力破解保护未激活）  
- **警告（黄色）：** Tailscale 连接中断  
- 有 20 多个系统更新可用  
- 24 小时内有 10 次以上登录失败  
- 磁盘使用率超过 80%  
- **信息提示（蓝色）：** 未使用 Tailscale 时网关暴露  

## 集成方式  
- **晨间报告：** 将安全状态信息添加到晨间报告中  
- **心跳检测：** 监控严重警报  
- **警报通知：** 将警报信息发送到通知系统  

## 架构说明  
- **后端：** Node.js HTTP 服务器  
- **前端：** 纯 JavaScript（无框架）  
- **端口：** 18791（可配置）  
- **绑定地址：** 仅绑定到本地主机（127.0.0.1）  
- **服务管理：** 使用 systemd 管理  

**相关文件：**  
- `server.js`：主要后端逻辑（数据收集与 API 接口）  
- `public/index.html`：监控面板用户界面  
- `lib/`：共享工具库（如需使用）  

## 所需依赖库  
- Node.js（版本 18 及以上）  
- `systemctl`：服务管理工具  
- `ss`：套接字统计工具  
- `ufw` 或 `firewalld`：防火墙检查工具  
- `tailscale`：VPN 状态检测工具（可选）  
- `fail2ban`：禁止访问记录工具（可选）  
- `openclaw`：网关监控工具  

所有依赖库均为标准 Linux 工具，除 OpenClaw 本身外。  

## 故障排除  
- **监控面板无法加载？**  
  1. 检查服务状态：```bash
   sudo systemctl status security-dashboard
   ```  
  2. 查看日志：```bash
   sudo journalctl -u security-dashboard -n 50
   ```  
  3. 确认端口是否正在监听：```bash
   ss -tlnp | grep 18791
   ```  
  4. 直接测试 API 接口：```bash
   curl http://localhost:18791/api/security
   ```  

- **网关状态显示为“未知”？**  
  1. 确认 OpenClaw 网关正在运行：```bash
  pgrep -f openclaw-gateway
  ```  
  2. 检查 OpenClaw 配置文件是否存在：```bash
  cat ~/.openclaw/openclaw.json
  ```  

- **指标显示为“未知”？**  
  1. 可能需要 sudo 权限来执行某些命令  
  2. 检查脚本的执行权限  
  3. 确认相关文件路径存在（如会话数据、配置文件等）  

## 卸载该技能  
```bash
sudo systemctl stop security-dashboard
sudo systemctl disable security-dashboard
sudo rm /etc/systemd/system/security-dashboard.service
sudo systemctl daemon-reload
```  
卸载后请删除对应的技能目录：```bash
rm -rf /root/clawd/skills/security-dashboard
```  

## 发布方式  
若需将此技能发布到 ClawdHub，可参考相关文档。  

## 许可证  
该技能采用 MIT 许可协议。  

**作者说明：**  
由 Erdma 为 Brian Christner 的基础设施监控项目开发。