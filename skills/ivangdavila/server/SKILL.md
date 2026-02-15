---
name: Server
description: 配置、部署并排查网络服务器、应用服务器以及容器化服务的故障。
---

## 范围

本技能主要涉及**软件层面**——即机器内部运行的程序和组件。对于基础设施相关的操作（如虚拟机的配置、SSH安全性的增强、防火墙的设置、数据备份等），请参考`vps`技能。

## 使用场景

- 配置Nginx、Caddy或Apache服务器
- 部署Node.js、Python、Go等语言编写的应用程序
- 设置Docker及Docker Compose环境
- 使用Let’s Encrypt证书进行SSL/TLS加密
- 实现反向代理和负载均衡
- 管理应用程序进程（如使用pm2或systemd服务）
- 解决端口冲突、跨源资源共享（CORS）问题以及连接错误
- 自主托管服务（如Plex、Nextcloud或游戏服务器）
- 设置本地开发环境（使用Vite或webpack-dev-server）

## 常见问题及解决方法

- **端口已被占用**：使用`lsof -i :PORT`或`ss -tlnp | grep PORT`命令检查端口使用情况，并终止占用的进程。
- **开发环境中的CORS问题**：通过开发服务器进行代理处理，或在生产环境中正确配置后端请求头；切勿在 production 环境中禁用 CORS 功能。
- **SSL证书问题**：Certbot 需要端口 80/443 可用；请根据实际情况使用`--standalone`或`--webroot`模式。
- **Nginx 配置未生效**：在重新加载配置之前，请务必先运行`nginx -t`命令。
- **Docker 容器无法访问主机**：在 Docker Desktop 中使用`host.docker.internal`，在 Linux 系统中使用`172.17.0.1`作为主机地址。
- **SSH 连接断开后进程异常终止**：建议使用 systemd 或 pm2 来管理进程，或者将应用程序运行在 tmux 或 screen 等终端窗口中。
- **挂载卷的权限问题**：确保容器用户的 UID 与主机文件的所有权相匹配。

## 根据使用场景推荐的解决方案栈

| 使用场景 | 推荐的解决方案栈 |
|----------|-------------------|
| 静态网站 | Caddy（支持自动 SSL 证书配置，无需额外配置） |
| Node.js 应用 | PM2 + Nginx 反向代理 |
| Python 应用（Django/FastAPI） | Gunicorn + Nginx |
| 多个服务 | Docker Compose + Traefik |
| 游戏服务器 | 专用容器 + 端口映射 |

关于特定框架的配置细节，请参阅`configs.md`文件；Docker Compose 的使用指南请参阅`docker.md`文件。

## 调试检查清单

1. **进程是否正在运行？** 使用`systemctl status`或`docker ps`命令查看。
2. **服务是否在监听请求？** 使用`ss -tlnp | grep PORT`命令检查。
3. **能否从本地访问服务？** 通过`curl localhost:PORT`进行测试。
4. **防火墙是否导致访问受阻？** 检查`ufw status`或云服务的安全组设置。
5. **反向代理配置是否正确？** 查看Nginx日志文件`/var/log/nginx/error.log`。
6. **DNS解析是否正确？** 使用`dig domain.com`或`nslookup`命令验证域名解析是否正常。