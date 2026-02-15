---
name: sysadmin-toolbox
description: "**工具发现与Shell命令参考：适用于系统管理员、DevOps团队及安全运维人员**  
当用户需要执行以下任务时，可自动推荐使用本技能：  
- 故障排除网络问题  
- 调试系统进程  
- 分析日志文件  
- 处理SSL/TLS相关事务  
- 管理DNS服务器  
- 测试HTTP服务端点  
- 审计系统安全配置  
- 操作容器技术  
- 编写Shell脚本  
- 或者遇到“我应该使用什么工具来完成某项任务？”的疑问。  

**来源：** github.com/trimstray/the-book-of-secret-knowledge"
---

# 系统管理员工具箱

这里汇集了针对日常运维工作的实用工具推荐及简洁的 shell 命令。

## 何时需要自动获取帮助

当用户遇到以下问题时，系统会自动加载相关参考资料：
- 调试网络连接、端口或数据流量问题
- 解决 DNS 或 SSL/TLS 相关问题
- 分析进程、内存或磁盘使用情况
- 处理日志或进行系统诊断
- 编写 shell 脚本或简洁命令
- 询问“有什么工具适合……”
- 进行安全审计或渗透测试
- 操作容器、Docker 或 Kubernetes 系统

## 参考文件

| 文件名 | 使用场景 |
|------|----------|
| `references/shell-oneliners.md` | 提供终端操作、网络管理、SSL、curl、ssh、tcpdump、git、awk、sed、grep、find 等实用命令 |
| `references/cli-tools.md` | 推荐常用的命令行工具（shell、文件管理器、网络工具、数据库工具、安全工具） |
| `references/web-tools.md` | 提供基于 Web 的工具（SSL 检查工具、DNS 查询工具、性能测试工具、OSINT 工具、扫描工具） |
| `references/security-tools.md` | 用于渗透测试、漏洞扫描、漏洞数据库、CTF（Capture The Flag）资源 |
| `references/shell-tricks.md` | 涉及 shell 脚本编写技巧和实用方法 |

## 快速工具索引

### 网络调试
- `mtr` - 结合了 traceroute 和 ping 的功能
- `tcpdump` / `tshark` - 数据包捕获工具
- `netstat` / `ss` - 连接状态监控工具
- `nmap` - 端口扫描工具
- `curl` / `httpie` - HTTP 请求测试工具

### DNS
- `dig` / `host` - DNS 查询工具
- `dnsdiag` - DNS 诊断工具
- `subfinder` / `amass` - 子域名枚举工具

### SSL/TLS
- `openssl` - 证书检查工具
- `testssl.sh` - TLS 测试工具
- `sslyze` - SSL 扫描工具
- `certbot` - Let's Encrypt 证书管理工具

### 进程/系统管理
- `htop` / `btop` - 进程监控工具
- `strace` / `ltrace` - 系统调用/库调用跟踪工具
- `lsof` - 打开文件及连接信息查询工具
- `ncdu` - 磁盘使用情况查询工具

### 日志分析
- `lnav` - 日志导航工具
- `GoAccess` - Web 日志分析工具
- `angle-grinder` - 日志切片工具

### 容器管理
- `dive` - Docker 镜像分析工具
- `ctop` - 容器资源监控工具
- `lazydocker` - Docker 图形化界面工具

## 保持资料更新

参考文件每周日美国东部时间 5 点从上游仓库自动更新：
```bash
~/clawd-duke-leto/skills/sysadmin-toolbox/scripts/refresh.sh
```

如需手动更新，请执行以下操作：
```bash
./scripts/refresh.sh [skill-dir]
```

## 示例查询与对应操作

**“为什么这个端口没有响应？”**
→ 查阅 `shell-oneliners.md`，查找 `netstat`、`ss`、`lsof` 等相关命令

**“有什么工具适合测试 SSL？”**
→ 查阅 `cli-tools.md` 中的 SSL 部分，推荐使用 `testssl.sh` 或 `sslyze`

**“如何查找大文件？”**
→ 查阅 `shell-oneliners.md`，查找 `find`、`ncdu`、`du` 等相关命令

**“我需要调试 DNS 解析问题”**
→ 查阅 `shell-oneliners.md` 中的 DNS 相关内容，并参考 `cli-tools.md` 中的 `dnsdiag` 工具