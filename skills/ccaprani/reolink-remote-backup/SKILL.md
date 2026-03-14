---
name: reolink-remote-backup
description: 当摄像头采用远程连接（4G/5G/LTE）且家庭网络环境受限（使用CGNAT或被锁定的路由器）时，需要设置可靠的异地Reolink摄像头备份方案。该备份方案可用于指导架构设计、配置VPS中继服务、实现FTP/FTPS数据传输、进行本地或NAS设备间的数据同步，以及处理数据上传过程中的故障（如权限问题、路径问题等）。
---
# Reolink远程备份方案

通过以下方式实现可靠的备份功能：

1. 使用Reolink相机的FTP/FTPS上传功能将数据传输到VPS服务器；
2. 从VPS服务器将数据下载到本地NAS或本地存储设备中；
3. 实施数据保留策略并进行健康检查（确保备份系统的正常运行）。

当直接将相机数据传输到家庭网络中的存储设备不切实际时，可以使用此方案。

## 需要收集的信息：

- 相机型号及硬件版本；
- 应用程序或客户端是否提供了FTP/FTPS上传选项；
- VPS服务器的IP地址及SSH访问方式；
- 本地存储路径（NAS挂载点）；
- 所需的数据下载间隔（默认为10分钟）；
- 数据在VPS服务器上的保留时长（默认为30天）。

## 工作流程：

### 1) 验证系统架构限制：

- 如果家庭网络中的数据传输路径受到限制（例如使用CGNAT），建议使用VPS服务器作为数据中转站；
- 确保NAS设备不直接连接到公共互联网；
- 使用从VPS服务器到本地设备的自动数据下载功能（切勿依赖VPS服务器主动将数据推送至家庭网络中的存储设备）。

### 2) 配置VPS服务器的备份功能：

在VPS服务器上以root用户身份运行`scripts/setup_vps_vsftpd.sh`脚本：
- 安装vsftpd服务器软件及ufw防火墙；
- 创建名为`reolinkftp`的专用用户账户用于数据传输；
- 设置`/srv/reolink/incoming`目录用于存储上传的文件；
- 打开用于FTP数据传输的被动端口。

### 3) 配置本地数据下载功能：

在本地计算机上运行`scripts/setup_local_pull.sh`脚本：
- 在`/home/$USER/bin`目录下创建`reolink_pull.sh`脚本；
- 使用systemd服务管理工具创建一个定时任务，确保数据下载功能能够持续运行（`Persistent=true`选项）。

### 4) 设置数据保留策略：

在VPS服务器上运行`scripts/setup_vps_retention.sh`脚本，以便在本地数据同步中断时自动清理旧文件。

### 5) 验证备份效果：

- 触发相机的FTP上传操作；
- 确认上传的文件已保存在VPS服务器的`/srv/reolink/incoming`目录中；
- 手动运行一次本地数据下载脚本，确认文件已下载到目标路径；
- 使用`systemctl --user list-timers | grep reolink-pull`命令检查定时任务是否正在正常运行。

## 故障排除：

请参考`references/troubleshooting.md`文件，了解如何根据错误代码和日志信息进行故障排查。

**快速检查方法：**
- 检查VPS服务器的服务状态：`systemctl status vsftpd`
- 查看VPS服务器的日志文件：`journalctl -u vsftpd -n 120 --no-pager`
- 查看FTP服务器的日志文件：`tail -n 120 /var/log/vsftpd.log`
- 检查本地NAS设备的挂载状态：`mountpoint -q <mountpath>`

## 安全基线要求：

- 使用SSH密钥进行VPS服务器的远程管理；
- 将负责数据传输的FTP用户与系统管理员用户分离；
- 完成初步调试后，优先使用FTPS传输方式；
- 强制执行数据保留策略，防止VPS服务器磁盘空间被占用；
- 定期更换在聊天记录或日志中可能暴露的敏感信息（如密码等）。