---
name: sys-guard-linux-remediator
description: 基于主机的Linux事件响应与修复技能，重点在于精确的威胁检测、符合取证要求的数据收集、防火墙控制（iptables/nftables）、系统完整性验证，以及在保持系统稳定性的前提下进行有控制的修复操作。
metadata:
  author: Edwin Kairu (ekairu@cmu.edu)
---
# Linux威胁缓解与事件修复（强化版）

本技能提供了一个结构化且具备取证意识的框架，用于在安全事件发生期间或之后分析和保护Linux主机。

其主要特点包括：

- 非破坏性的证据收集
- 准确的威胁检测
- 兼容防火墙的威胁遏制机制
- 完整性验证
- 可控且可逆的修复过程
- 根据操作系统特性使用相应的命令

---

# 环境背景

## 支持的系统

- Debian / Ubuntu
- RHEL / CentOS / Rocky / Alma
- Fedora
- Arch Linux（提供有限的包管理指导）

## 执行前提

- 使用`bash`或POSIX `sh` shell
- 拥有root权限或sudo权限
- 具有主机级访问权限（非容器限制环境）
- 建议使用基于systemd的系统

> ⚠️ 如果在Docker、Kubernetes、LXC或其他容器中运行，防火墙、审计和服务的命令可能无法准确反映主机系统的实际状态。

---

# 防火墙架构认知

现代Linux系统可能使用以下防火墙工具：

- `iptables-legacy`
- `iptables-nft`（兼容性封装）
- 原生的`nftables`
- `firewalld`（RHEL系列系统的默认防火墙）

## 识别防火墙后端

```bash
iptables --version
which nft
systemctl status firewalld
```

如果系统使用`nftables`：

```bash
nft list ruleset
```

请注意：`iptables -L`命令并不能完全反映防火墙的所有规则状态。

---

# 不同操作系统的日志记录方式

| 操作系统 | 主要日志文件 |
|--------------|------------------|
| Ubuntu/Debian | `/var/log/syslog` |
| RHEL/CentOS/Fedora | `/var/log/messages` |
| 所有基于systemd的系统 | `journalctl` |

建议始终使用`journalctl`进行日志记录。

---

# 强化版的操作工具包

## 1. 网络检查

### 监听服务
```bash
ss -tulpn
```

### 活动连接
```bash
ss -antp | grep ESTABLISHED
```

### 防火墙状态

#### 使用`iptables`
```bash
iptables -L -n -v --line-numbers
iptables -S
```

#### 使用`nftables`
```bash
nft list ruleset
```

### 本地服务枚举
```bash
ss -lntup
```

除非必要，否则避免对`localhost`进行全范围扫描。

### 保守的网络扫描
```bash
nmap -sV -T3 -p- localhost
```

### 数据包捕获（快速截图）
```bash
tcpdump -i any -nn -c 100
```

---

## 2. 进程与运行时分析

### 进程树
```bash
ps auxww --forest
```

### 高CPU/内存使用情况
```bash
top
```

### 打开的文件描述符
```bash
lsof -p <PID>
```

### 系统调用跟踪（注意：可能影响性能）
```bash
strace -p <PID>
```

> ⚠️ 使用`strace`时可能会改变进程行为。在系统被入侵的情况下请谨慎使用。

### 内核模块
```bash
lsmod
```

### 内核日志
```bash
dmesg | tail -50
```

---

## 3. 根套件与恶意软件扫描

### 根套件扫描工具
```bash
rkhunter --check
chkrootkit
```

> 可能会产生误报。请手动验证扫描结果。

### 有针对性的杀毒扫描
```bash
clamscan -r /home
```

请谨慎使用；大规模扫描会增加I/O操作，并可能改变文件访问时间戳。

### Lynis系统审计工具
```bash
lynis audit system
```

---

## 4. 文件完整性与包验证

### AIDE（初始化后使用）

### 安装：
```bash
apt install aide
# or
dnf install aide
```

### 初始化：
```bash
aideinit
mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
```

### 运行检查：
```bash
aide --check
```

### RHEL包验证
```bash
rpm -Va
```

### Debian包验证
```bash
apt install debsums
debsums -s
```

---

## 5. 取证分析（Didier Stevens工具集）

### 安装：
```bash
sudo mkdir -p /opt/forensics
sudo wget -P /opt/forensics https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/base64dump.py
sudo wget -P /opt/forensics https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/re-search.py
sudo wget -P /opt/forensics https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/zipdump.py
sudo wget -P /opt/forensics https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/1768.py
sudo wget -P /opt/forensics https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/pdf-parser.py
sudo wget -P /opt/forensics https://raw.githubusercontent.com/DidierStevens/DidierStevensSuite/master/oledump.py
sudo chmod +x /opt/forensics/*.py
```

### 解码Base64编码
```bash
python3 /opt/forensics/base64dump.py file.txt
```

### 搜索IOC（Indicator of Compromise，威胁标识）
```bash
python3 /opt/forensics/re-search.py -n ipv4 logfile
```

### 检查ZIP文件（无需解压）
```bash
python3 /opt/forensics/zipdump.py suspicious.zip
```

### 提取Cobalt Strike信标文件
```bash
python3 /opt/forensics/1768.py payload.bin
```

### 检查Office/PDF文档
```bash
python3 /opt/forensics/pdf-parser.py file.pdf
python3 /opt/forensics/oledump.py file.doc
```

> 仅进行静态检查。切勿执行可疑文件。

---

## 6. 认证与用户活动

### 当前会话
```bash
who -a
```

### 登录历史记录
```bash
last -a
```

### SSH登录失败记录
Ubuntu/Debian：
```bash
journalctl -u ssh.service | grep "Failed password"
```

RHEL/Fedora：
```bash
journalctl -u sshd.service | grep "Failed password"
```

### sudo使用情况
```bash
journalctl _COMM=sudo
```

### 审计日志
```bash
ausearch -m USER_AUTH,USER_LOGIN,USER_CHAUTHTOK
```

---

# 可控的修复措施

## 阻止IP地址

### 使用`iptables`（立即生效）
```bash
iptables -I INPUT 1 -s <IP> -j DROP
```

### 使用`nftables`
```bash
nft add rule inet filter input ip saddr <IP> drop
```

如果系统使用`firewalld`：
```bash
firewall-cmd --add-rich-rule='rule family="ipv4" source address="<IP>" drop'
```

---

## 保持防火墙规则持久化

### 使用`iptables`（Debian系统）
```bash
netfilter-persistent save
```

### 手动保存防火墙规则
```bash
iptables-save > /etc/iptables/rules.v4
```

### 使用`firewalld`
```bash
firewall-cmd --runtime-to-permanent
```

### 使用`nftables`
```bash
nft list ruleset > /etc/nftables.conf
```

---

## 进程遏制策略

推荐的升级步骤：

1. 观察系统行为
2. 使用`kill -TERM <PID>`终止异常进程
3. 如有必要，使用`kill -STOP <PID>`进行进一步分析
4. 仅在必要时使用`kill -KILL <PID>`强制终止进程

避免使用`killall`或`pkill`命令。

---

## 服务隔离

```bash
systemctl stop <service>
systemctl disable <service>
systemctl mask <service>
```

---

# 持久化机制与后门检查

### Cron作业
```bash
crontab -l
ls -lah /etc/cron*
```

### systemd的持久化设置
```bash
ls -lah /etc/systemd/system/
```

### 启动脚本
```bash
cat /etc/rc.local
```

---

# SELinux（RHEL/Fedora系统）

### 检查SELinux状态：
```bash
getenforce
```

### 查看系统拒绝操作
```bash
ausearch -m AVC
```

---

# 取证规范

1. 绝不执行可疑的二进制文件。
2. 在删除任何文件之前先保存证据：
```bash
sha256sum file
mkdir -p /root/quarantine
mv file /root/quarantine/file.vir
```

3. 记录所有的修复步骤：
   - 时间戳
   - 执行的命令
   - 实际结果

---

# 使用示例

## 常规审计

- 运行`lynis audit system`进行系统审计
- 检查是否存在未知的监听服务
- 确认系统二进制文件是否被修改

## 面对活跃威胁时

- 识别高CPU消耗的进程
- 捕获网络数据包
- 提取文件哈希值
- 通过防火墙阻止恶意连接
- 保存恶意文件

## 对于可疑文件

- 使用`zipdump`提取文件内容
- 计算文件哈希值
- 将文件移至隔离区
- 在日志中查找文件执行尝试的记录

---

# 安全防护措施

以下安全措施是强制性的，适用于所有修复操作：

- 这些措施旨在防止操作失误导致的系统故障，保持证据的完整性，并确保事件响应过程的可控性和可逆性。

---

## 1. 状态验证（修改前后的对比）

在执行任何修复命令之前：

1. 记录时间戳（UTC格式）：
   ```bash
   date -u
   ```

2. 运行以下命令以获取当前系统状态：
   - 网络状态：`ss -tulpn`
   - 活动连接：`ss -antp`
   - 防火墙（iptables）：`iptables -L -n -v`
   - 防火墙（nftables）：`nft list ruleset`
   - firewalld：`firewall-cmd --list-all`

修复完成后：

3. 重新运行上述命令，比较系统状态的变化，确认：
   - 是否达到了预期效果
   - 是否有服务中断
   - 管理权限是否受到影响（例如，SSH访问是否仍然可用）

切勿在未验证效果的情况下假设命令已经成功执行。

---

## 2. 禁用通配符和广泛的进程终止命令

为防止系统遭受严重损害：

- 绝对不要使用以下命令：
  - `rm -rf *`
  - `rm -rf /`
  - `killall`
  - 使用广泛的`pkill`命令
  - 在敏感目录中使用通配符删除文件

- 始终使用绝对文件路径（例如：`/tmp/malware.bin`）
- 明确指定要终止的进程ID（`kill -TERM <PID>`）
- 在修改文件之前先使用`ls -lah <file>`确认文件是否存在

在事件响应过程中，严禁使用通配符删除文件或使用广泛的进程终止命令。

---

## 3. 持久化机制与后门检查

在遏制恶意进程或服务后，立即检查系统是否存在持久化机制：

### 检查Cron作业
```bash
crontab -l
ls -lah /etc/cron*
```

### systemd服务与定时任务
```bash
systemctl list-unit-files --type=service
systemctl list-timers --all
ls -lah /etc/systemd/system/
```

### 启动脚本
```bash
ls -lah /etc/init.d/
cat /etc/rc.local
```

### 用户级别的持久化设置
```bash
ls -lah ~/.config/systemd/user/
```

### SSH后门

在清除恶意文件后：

- 进行文件完整性验证：
  ```bash
  aide --check
  ```
  - 在RHEL系列系统中：
  ```bash
  rpm -Va
  ```
  - 在Debian系列系统中：
  ```bash
  debsums -s
  ```

只有在彻底清除所有持久化机制后，才能认为威胁已被清除。

---

## 4. 防火墙规则的安全性与持久化

### A. 防止系统锁定

在修改防火墙规则之前：

1. 确认SSH监听端口的状态：
   ```bash
   ss -tulpn | grep ssh
   ```

2. 确保存在以下规则：
   - 允许当前管理IP地址访问SSH端口

切勿在未确认SSH访问规则存在的情况下设置默认的拒绝策略。

---

### B. 规则的临时性与持久性

防火墙规则的更改通常是临时性的，重启后可能会失效：

#### 使用`iptables`（Debian/Ubuntu）：
规则仅在运行时生效，需要手动保存：

```bash
iptables-save > /etc/iptables/rules.v4
```

#### 使用`netfilter-persistent`工具：
```bash
netfilter-persistent save
```

#### 使用RHEL的旧版`iptables`服务：
```bash
service iptables save
```

#### 使用`firewalld`：
规则会在系统重启后保持持久化：

```bash
firewall-cmd --runtime-to-permanent
```

#### 使用`nftables`：
确保规则被持久化：

```bash
nft list ruleset > /etc/nftables.conf
```

记录以下信息：
- 规则的临时性或持久性
- 规则的保存位置
- 重启后的规则状态（如适用）

---

## 5. 销毁前的取证保存

在删除或终止任何系统组件之前：

1. 计算文件的哈希值：
   ```bash
   sha256sum <file>
   ```

2. 将文件移至隔离区：
   ```bash
   mkdir -p /root/quarantine
   mv <file> /root/quarantine/<file>.vir
   ```

3. 记录以下信息：
   - 时间戳（UTC格式）
   - 文件的原始路径
   - 文件的哈希值
   - 采取隔离措施的原因

除非绝对必要，否则避免使用`kill -9`命令。推荐使用以下方法：
- `kill -TERM <PID>`
- 如果需要进一步取证分析，使用`kill -STOP <PID>`
- 仅在最后不得已的情况下使用`kill -KILL <PID>`

---

## 6. 操作记录要求

所有修复操作都必须包括以下信息：

- 操作时间（`date -u`）
- 执行的命令
- 操作理由
- 实际结果
- 风险等级的更新（如适用）

没有记录的修复操作是不符合规范的。

---

## 7. 最小化影响原则

所有操作应遵循以下原则：

- 仅进行必要的最小程度修改
- 尽可能实现操作的可逆性
- 避免全局性的配置更改
- 除非有明确理由，否则不要重启系统服务
- 在系统被入侵期间，除非有明确的范围限制，否则不要进行全系统扫描

首先进行隔离，然后有针对性地清除威胁，最后谨慎地恢复系统。