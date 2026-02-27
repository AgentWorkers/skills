---
name: afrexai-self-hosting-mastery
description: 一个完整的自托管和家庭实验室操作系统。能够部署、保护、监控以及维护具有生产级可靠性的自托管服务。适用于搭建家庭服务器、Docker基础设施、反向代理、备份系统，以及评估SaaS的自托管替代方案。
---
# 自主托管精通

这是一个完整的系统，用于构建和运行可靠的自主托管基础设施——从第一台服务器到多节点的家庭实验室。

## 第1阶段：基础设施评估

### 服务器配置 YAML

```yaml
server_profile:
  name: ""
  hardware:
    cpu: ""              # e.g., "Intel i5-12400" or "Raspberry Pi 5"
    ram_gb: 0
    storage:
      - device: ""       # e.g., "/dev/sda"
        type: ""         # ssd | hdd | nvme
        size_gb: 0
        role: ""         # boot | data | backup
    network: ""          # 1gbe | 2.5gbe | 10gbe
  os: ""                 # debian | ubuntu | proxmox | unraid | truenas
  location: ""           # home | closet | rack | colo | vps
  power:
    ups: false
    wattage_idle: 0
    wattage_load: 0
    monthly_cost_estimate: ""  # electricity
  network:
    public_ip: ""        # static | dynamic | cgnat
    domain: ""
    dns_provider: ""     # cloudflare | duckdns | custom
    isp_ports_open: true # some ISPs block 80/443
  goals:
    - ""                 # media server, smart home, dev environment, etc.
  budget_monthly: ""     # electricity + domain + any VPS
```

### 硬件选择矩阵

| 预算 | 内存 | 存储 | 适用场景 | 示例硬件 |
|--------|-----|---------|----------|-----------------|
| $0 | 4-8GB | 64GB+ | Pi-hole、AdGuard、小型工具 | Raspberry Pi 4/5 |
| $50-150 | 8-16GB | 256GB+ | Docker主机、5-10个服务 | 二手SFF PC（Dell Optiplex、Lenovo Tiny） |
| $150-400 | 16-32GB | 1TB+ | NAS + 服务、媒体服务器 | Mini PC（Intel NUC、Beelink） |
| $400-800 | 32-64GB | 4TB+ | 全功能家庭实验室、虚拟机+容器 | 二手企业级服务器（Dell R720、HP DL380） |
| $800+ | 64GB+ | 10TB+ | 多节点、Proxmox集群 | 多个节点、专用NAS |

### 自主托管与SaaS的选择

在决定自主托管之前，请考虑以下问题：
1. **数据敏感性** —— 保留本地数据重要吗？（密码、健康数据、财务数据 = 需要）
2. **可靠性需求** —— 你能忍受偶尔的停机吗？（电子邮件 = 风险较高，媒体文件 = 可以）
3. **维护预算** —— 你每月有2-4小时的时间进行更新吗？
4. **技能水平** —— 你能调试Docker/网络问题吗？
5. **成本比较** —— SaaS的费用是否低于每月10美元？对于小额节省，通常不值得自主托管。

**必须自主托管的服务**：密码管理器、DNS/广告拦截器、VPN、书签、笔记
**通常建议自主托管的服务**：媒体服务器、文件同步、照片备份、监控、Git
**需要慎重考虑的服务**：电子邮件（传输问题）、日历（同步复杂）、聊天（对可用性要求高）
**不太值得自主托管的服务**：搜索引擎（资源消耗大）、社交媒体（没有网络效应）

---

## 第2阶段：操作系统与虚拟化

### 操作系统选择指南

| 操作系统 | 适用场景 | 学习曲线 | 备注 |
|----|----------|---------------|-------|
| Debian 12 | 仅用于Docker主机 | 较低 | 稳定、简洁、易于使用 |
| Ubuntu Server 24.04 | 适合初学者，文档丰富 | 较低 | 包含更多软件包，但snap管理有争议 |
| Proxmox VE | 适用于虚拟机+容器 | 中等 | 免费，具备企业级功能，支持ZFS |
| Unraid | 适用于NAS + Docker + 虚拟机 | 中等 | 价格在$59-129之间，用户界面友好，支持奇偶校验阵列 |
| TrueNAS Scale | 适用于ZFS NAS + Docker | 中等 | 免费，优先使用ZFS，应用程序不断更新 |
| NixOS | 适用于可复制的配置 | 高难度 | 基于声明式配置，学习曲线较陡 |

### Proxmox快速设置

```bash
# Post-install essentials
# 1. Remove enterprise repo (if no subscription)
sed -i 's/^deb/#deb/' /etc/apt/sources.list.d/pve-enterprise.list
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
apt update && apt upgrade -y

# 2. Create a Docker LXC (lightweight container)
# Download template: Datacenter → Storage → CT Templates → Download → debian-12
# Create CT: 2 cores, 2GB RAM, 32GB disk, bridge vmbr0
# Inside CT: install Docker
apt install -y curl
curl -fsSL https://get.docker.com | sh

# 3. Enable IOMMU for GPU passthrough (if needed)
# Edit /etc/default/grub: GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on"
# update-grub && reboot
```

### 虚拟机（VM）与LXC与Docker的选择

| 因素 | 虚拟机（VM） | LXC | Docker |
|--------|----|-----|--------|
| 隔离性 | 完全隔离（独立内核） | 部分隔离（共享内核） | 进程级隔离 |
| 开销 | 较高（基础开销1-2GB） | 较低（50-200MB） | 最小开销 |
| 适用场景 | 需要不同操作系统、GPU直通、不可信任的工作负载 | 专用服务主机、需要ZFS数据集 | 大多数服务 |
| 应避免的情况 | 内存有限 | 需要Windows系统、自定义内核 | 需要状态ful数据库（使用LXC/VM）

**规则**：90%的服务使用Docker；Docker主机或需要隔离环境时使用LXC；需要Windows系统、特殊内核需求或GPU直通时使用虚拟机。

---

## 第3阶段：Docker基础设施

### Docker Compose项目结构

```
/opt/stacks/           # or ~/docker/
├── traefik/
│   ├── docker-compose.yml
│   ├── .env
│   ├── config/
│   │   └── traefik.yml
│   └── data/
│       ├── acme.json          # chmod 600
│       └── dynamic/
├── monitoring/
│   ├── docker-compose.yml
│   ├── .env
│   └── config/
├── media/
│   ├── docker-compose.yml
│   ├── .env
│   └── config/
├── productivity/
│   ├── docker-compose.yml
│   ├── .env
│   └── config/
└── scripts/
    ├── backup.sh
    ├── update-all.sh
    └── health-check.sh
```

### Docker Compose最佳实践

```yaml
# Template: production-grade service
services:
  app:
    image: vendor/app:1.2.3           # ALWAYS pin version
    container_name: app               # Explicit name
    restart: unless-stopped           # Auto-restart
    networks:
      - proxy                         # Traefik network
      - internal                      # Backend network
    volumes:
      - ./config:/config              # Bind mount for config
      - app-data:/data                # Named volume for data
    environment:
      - TZ=Europe/London              # Always set timezone
      - PUID=1000                     # Match host user
      - PGID=1000
    env_file:
      - .env                          # Secrets in .env (gitignored)
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`app.example.com`)"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"
      - "traefik.http.services.app.loadbalancer.server.port=8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 512M               # Prevent OOM cascades
    security_opt:
      - no-new-privileges:true        # Security hardening
    read_only: true                   # Where possible
    tmpfs:
      - /tmp

volumes:
  app-data:

networks:
  proxy:
    external: true
  internal:
```

### Docker安全检查清单

- [ ] 固定所有镜像版本（生产环境中不要使用`:latest`）
- [ ] 为所有服务设置`restart: unless-stopped`
- [ ] 使用`.env`文件存储敏感信息（不要在Docker Compose中硬编码）
- [ ] 为所有容器设置内存限制
- [ ] 使用`security_opt: no-new-privileges:true`
- [ ] 在可能的情况下使用`read_only: true`并将/tmp设置为tmpfs
- [ ] 为每个服务创建独立的Docker网络
- [ ] 不要将数据库端口暴露到0.0.0.0
- [ ] 以非root用户权限运行容器（使用PUID/PGID或`user:`）
- [ ] 启用Docker内容信任：`export DOCKER_CONTENT_TRUST=1`
- [ ] 每月清理未使用的镜像/卷：`docker system prune -af`
- [ ] 为所有持久化数据使用命名卷（而非匿名卷）
- [ ] 为每个容器设置`TZ`环境变量

---

## 第4阶段：反向代理与SSL

### 反向代理选择

| 代理 | 适用场景 | SSL支持 | 配置方式 | 学习曲线 |
|-------|----------|-----|-------------|---------------|
| Traefik | 原生Docker代理，自动发现 | 自动配置（支持ACME） | 需要YAML配置文件 | 中等难度 |
| Caddy | 简单易用，支持自动SSL | 内置SSL支持 | 需要Caddyfile配置文件 | 低难度 |
| Nginx Proxy Manager | 提供图形化界面 | 自动配置 | 需要Web界面 | 非常简单 |
| Nginx（手动配置） | 提供最大程度的控制 | 需要手动配置或使用certbot | 高难度 |

**推荐**：对于Docker高级用户，使用Traefik；对于初学者，使用Caddy；对于简单需求，可以使用NPM。

### Traefik生产环境配置

```yaml
# traefik/config/traefik.yml
api:
  dashboard: true
  insecure: false

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"
    http:
      tls:
        certResolver: letsencrypt

certificatesResolvers:
  letsencrypt:
    acme:
      email: you@example.com
      storage: /data/acme.json
      # Use DNS challenge if ISP blocks port 80
      # dnsChallenge:
      #   provider: cloudflare
      httpChallenge:
        entryPoint: web

providers:
  docker:
    exposedByDefault: false    # Explicit opt-in per service
    network: proxy
  file:
    directory: /data/dynamic
    watch: true

log:
  level: WARN

accessLog:
  filePath: /data/access.log
  bufferingSize: 100
```

### Cloudflare Tunnel（零端口转发）

当使用CGNAT或ISP阻止某些端口时，可以通过Cloudflare Tunnel来暴露服务，而无需打开防火墙：

```yaml
# cloudflared/docker-compose.yml
services:
  cloudflared:
    image: cloudflare/cloudflared:2024.1.0
    container_name: cloudflared
    restart: unless-stopped
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=${CF_TUNNEL_TOKEN}
    networks:
      - proxy
```

**何时使用Cloudflare Tunnel与端口转发**：
- 使用CGNAT且没有公共IP地址时 → 使用Tunnel
- ISP阻止80/443端口时 → 使用Tunnel或DNS挑战机制
- 安全性优先时 → 使用Tunnel（避免开放端口）
- 性能优先时 → 直接使用端口转发（延迟更低）
- 仅限局域网访问时 → 可以使用Tailscale/WireGuard

---

## 第5阶段：基础服务堆栈

### 第1层——首先部署的服务（基础部分）

| 服务 | 功能 | 镜像 | 内存需求 | 备注 |
|---------|---------|-------|-----|-------|
| Traefik/Caddy | 反向代理+SSL | traefik:v3.0 | 64MB | 作为所有服务的入口 |
| Pi-hole/AdGuard | DNS+广告拦截 | pihole/pihole | 128MB | 全局广告拦截 |
| Authelia/Authentik | SSO+双因素认证 | authelia/authelia | 128MB | 为没有内置认证功能的服务提供安全保护 |
| Uptime Kuma | 监控工具 | louislam/uptime-kuma | 128MB | 监控系统运行状态 |
| Watchtower | 自动更新工具 | containrrr/watchtower | 32MB | 可选，部分用户更喜欢手动配置 |

### 第2层——核心服务

| 服务 | 功能 | 替代方案 | 内存需求 |
|---------|---------|-----|-----|
| Vaultwarden | 密码管理器 | Bitwarden | 64MB |
| Nextcloud | 文件同步+办公工具 | Seafile（轻量级替代方案） | 512MB |
| Immich | 照片备份工具 | PhotoPrism | 1-4GB |
| Jellyfin | 媒体服务器 | Plex（功能较少） | 512MB-2GB |
| Paperless-ngx | 文档管理工具 | - | 256MB |
| Home Assistant | 智能家居控制 | - | 512MB |

### 第3层——高级用户专属服务

| 服务 | 功能 | 内存需求 | |
|---------|---------|-----|
| Gitea/Forgejo | Git托管服务 | 256MB |
| n8n | 工作流程自动化工具 | 256MB |
| Grafana + Prometheus | 统计指标与仪表盘 | 512MB |
| Tandoor | 食谱管理工具 | 256MB |
| Mealie | 餐饮计划工具 | 128MB |
| Linkwarden/Hoarder | 书签管理工具 | 256MB |
| Stirling PDF | PDF处理工具 | 512MB |
| IT-Tools | 开发者辅助工具 | 64MB |

### 内存规划

```
Total RAM needed ≈ OS base (1-2GB) + sum of service RAM + 20% headroom
Example 16GB server:
  OS + Docker:     2 GB
  Traefik:         0.1 GB
  Pi-hole:         0.1 GB
  Authelia:        0.1 GB
  Uptime Kuma:     0.1 GB
  Vaultwarden:     0.1 GB
  Nextcloud:       0.5 GB
  Immich:          2.0 GB
  Jellyfin:        1.0 GB
  Paperless:       0.3 GB
  Home Assistant:  0.5 GB
  ──────────────────────
  Total:           6.8 GB → 8.2 GB with headroom
  Available:       ~7.8 GB free for more services
```

---

## 第6阶段：网络与DNS

### DNS架构设计

```
Internet → Cloudflare DNS → Your Public IP → Router → Server
                                                        ↓
                                             Reverse Proxy (Traefik)
                                                        ↓
                                     ┌──────────────────┼──────────────────┐
                                     ↓                  ↓                  ↓
                                app.domain.com   files.domain.com   media.domain.com
```

### 分离DNS（实现本地访问，避免NAT转发）

```
# Pi-hole/AdGuard: Local DNS rewrites
# Point *.home.example.com → 192.168.1.100 (server LAN IP)
# External: Cloudflare points to public IP
# Result: LAN traffic stays local, external goes through internet
```

### 远程访问的VPN解决方案

| 解决方案 | 类型 | 适用场景 | 复杂度 |
|----------|------|----------|-----------|
| Tailscale | Mesh VPN | 设置最简单，支持多设备 | 非常简单 |
| WireGuard | 点对点VPN | 性能高，控制能力强 | 中等难度 |
| Headscale | 自主托管的Tailscale版本 | 提供隐私保护，无供应商限制 | 中等难度 |

**推荐**：对于初学者，建议从Tailscale开始（3用户免费）。如需更多控制，可升级到Headscale。

### 防火墙规则（UFW）

```bash
# Default deny incoming
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (change port from 22!)
ufw allow 2222/tcp comment 'SSH'

# Allow HTTP/HTTPS for reverse proxy
ufw allow 80/tcp comment 'HTTP redirect'
ufw allow 443/tcp comment 'HTTPS'

# Allow local network for discovery
ufw allow from 192.168.1.0/24 comment 'LAN'

# Enable
ufw enable
```

---

## 第7阶段：备份策略

### 实施3-2-1备份策略

```
3 copies:  Live data + Local backup + Remote backup
2 media:   SSD/HDD (server) + External drive or NAS
1 offsite: Cloud (Backblaze B2, Wasabi) or second location
```

### 备份脚本模板

```bash
#!/bin/bash
# /opt/stacks/scripts/backup.sh
set -euo pipefail

BACKUP_DIR="/mnt/backup/docker"
STACKS_DIR="/opt/stacks"
DATE=$(date +%Y-%m-%d_%H%M)
RETENTION_DAYS=30

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }

# 1. Stop services that need consistent backups
log "Stopping database services..."
cd "$STACKS_DIR/productivity" && docker compose stop db

# 2. Backup Docker volumes
log "Backing up volumes..."
for vol in $(docker volume ls -q); do
    docker run --rm \
        -v "$vol":/source:ro \
        -v "$BACKUP_DIR/volumes":/backup \
        alpine tar czf "/backup/${vol}_${DATE}.tar.gz" -C /source .
done

# 3. Backup compose files and configs
log "Backing up configs..."
tar czf "$BACKUP_DIR/configs/stacks_${DATE}.tar.gz" \
    --exclude='*.log' \
    --exclude='node_modules' \
    "$STACKS_DIR"

# 4. Restart services
log "Restarting services..."
cd "$STACKS_DIR/productivity" && docker compose start db

# 5. Cleanup old backups
log "Cleaning up backups older than ${RETENTION_DAYS} days..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

# 6. Sync to remote (Backblaze B2 example)
# rclone sync "$BACKUP_DIR" b2:my-backups/docker/ --transfers 4

# 7. Verify
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log "Backup complete. Total size: $BACKUP_SIZE"

# 8. Send notification (optional)
# curl -s "https://ntfy.sh/my-backups" -d "Backup complete: $BACKUP_SIZE"
```

### 备份计划

| 备份内容 | 备份频率 | 备份保留时间 | 备份方法 |
|------|-----------|-----------|--------|
| Docker卷 | 每天凌晨3点 | 30天 | 使用脚本和cron任务 |
| Compose配置文件 | 每天凌晨3点 | 90天 | 使用脚本和cron任务 |
| 数据库备份 | 每6小时一次 | 7天 | 使用pg_dump/mysqldump命令 |
| 全盘镜像 | 每月一次 | 3个月 | 使用Clonezilla/dd工具 |
| 离线备份 | 每天凌晨5点 | 60天 | 使用rclone备份到B2/Wasabi云存储 |

### 备份验证（每月进行）

- [ ] 从上周的备份中随机选择一份进行验证 |
- [ ] 在测试虚拟机/容器中恢复数据 |
- [ ] 验证数据完整性（检查文件数量、数据库记录数量） |
- [ ] 记录恢复过程的时间 |
- [ ] 将验证结果记录在backup-verification.md文件中 |

---

## 第8阶段：监控与警报

### 监控系统（使用Docker Compose）

```yaml
# monitoring/docker-compose.yml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    volumes:
      - uptime-data:/app/data
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.uptime.rule=Host(`status.example.com`)"

  prometheus:
    image: prom/prometheus:v2.49.0
    container_name: prometheus
    restart: unless-stopped
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'

  grafana:
    image: grafana/grafana:10.3.0
    container_name: grafana
    restart: unless-stopped
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}

  node-exporter:
    image: prom/node-exporter:v1.7.0
    container_name: node-exporter
    restart: unless-stopped
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.49.0
    container_name: cadvisor
    restart: unless-stopped
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro

volumes:
  uptime-data:
  prometheus-data:
  grafana-data:
```

### 警报规则

| 指标 | 警报阈值 | 严重程度 | 应对措施 |
|--------|---------|----------|--------|
| 磁盘使用率 | >80% | >90% | 清理或扩展磁盘空间 |
| 内存使用率 | >85% | >95% | 查找内存泄漏问题并增加内存 |
| CPU使用率持续过高 | >80%（持续5分钟） | >95%（持续5分钟） | 检查并修复问题 |
| 容器重启频率 | 每小时超过2次 | 每小时超过5次 | 检查日志并解决根本原因 |
| SSL证书过期 | 小于14天 | 小于3天 | 更新证书 |
| 备份时间过长 | 超过26小时 | 超过48小时 | 检查备份脚本和cron设置 |

### 通知渠道

| 通知方式 | 服务 | 适用场景 |
|---------|---------|----------|
| 推送通知 | ntfy.sh（适用于自主托管环境） | 移动设备通知 |
| 聊天工具 | Discord/Slack webhook | 团队内部通知 |
| 电子邮件 | Uptime Kuma内置通知 | 形式化通知 |
| 仪表盘 | Grafana + Uptime Kuma | 可视化监控 |

---

## 第9阶段：安全加固

### 服务器安全加固检查清单

```bash
# 1. SSH hardening
# /etc/ssh/sshd_config
Port 2222                          # Change default port
PermitRootLogin no                 # No root SSH
PasswordAuthentication no          # Key-only
MaxAuthTries 3
AllowUsers yourusername

# 2. Install fail2ban
apt install fail2ban -y
systemctl enable fail2ban

# 3. Automatic security updates
apt install unattended-upgrades -y
dpkg-reconfigure -plow unattended-upgrades

# 4. Disable unused services
systemctl list-unit-files --state=enabled
# Disable anything you don't need
```

### 认证机制设计

```
Internet → Traefik → Authelia/Authentik → Service
                         ↓
                    Check: authenticated?
                    Yes → Forward to service
                    No → Redirect to login page + 2FA
```

**Authelia**（轻量级，支持YAML配置）——适合小型系统 |
**Authentik**（提供完整身份验证功能，支持Web界面）——适合多用户/多服务环境，支持SAML/OIDC协议

### 安全评分（0-100分）

| 评估维度 | 权重 | 分数 |
|-----------|--------|-------------|
| SSH安全配置（密钥管理、非root用户权限） | 15分 | 默认值为0，满分15分 |
| 防火墙配置（默认拒绝访问） | 15分 | 默认值为0，满分15分 |
| 使用反向代理（避免直接暴露端口） | 15分 | 默认值为0，满分15分 |
| 所有服务均使用SSL/TLS | 10分 | 默认值为0，满分10分 |
| 所有服务均启用身份验证 | 15分 | 默认值为0，满分15分 |
| 容器安全设置（限制权限） | 10分 | 默认值为0，满分10分 |
| 自动更新功能 | 10分 | 默认值为0，满分10分 |
| 秘密信息管理（使用`.env文件，避免硬编码） | 10分 | 默认值为0，满分10分 |

**评分标准**：0-40分表示脆弱；41-70分表示可接受；71-90分表示良好；91-100分表示高度安全。

---

## 第10阶段：维护与更新

### 更新策略

**选项A：手动更新（推荐用于关键服务）**
```bash
# Update script: /opt/stacks/scripts/update-all.sh
#!/bin/bash
set -euo pipefail

STACKS_DIR="/opt/stacks"
LOG="/var/log/docker-updates.log"

for stack in "$STACKS_DIR"/*/; do
    if [ -f "$stack/docker-compose.yml" ]; then
        echo "[$(date)] Updating $(basename $stack)..." | tee -a "$LOG"
        cd "$stack"
        docker compose pull 2>&1 | tee -a "$LOG"
        docker compose up -d 2>&1 | tee -a "$LOG"
    fi
done

docker image prune -f | tee -a "$LOG"
echo "[$(date)] Update complete" | tee -a "$LOG"
```

**选项B：使用Watchtower（自动更新——请谨慎使用）**
```yaml
services:
  watchtower:
    image: containrrr/watchtower:1.7.1
    container_name: watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_SCHEDULE=0 0 4 * * MON  # Monday 4 AM
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_NOTIFICATIONS=shoutrrr
      - WATCHTOWER_NOTIFICATION_URL=discord://webhook
      - WATCHTOWER_LABEL_ENABLE=true    # Only update labeled containers
    # Add label to containers: com.centurylinklabs.watchtower.enable=true
```

### 每周维护任务

- [ ] 检查Uptime Kuma的运行状态 |
- [ ] 查看磁盘使用情况（`df -h`命令） |
- [ ] 检查容器健康状况（`docker ps --filter health=unhealthy`） |
- [ ] 查看fail2ban的禁用记录（`fail2ban-client status`） |
- [ ] 检查备份日志（最近一次成功的备份记录） |
- [ ] 检查Docker日志中的错误信息（`docker logs --since 7d <container>`） |
- [ ] 清理未使用的资源（`docker system prune -f`）

### 每月维护任务

- [ ] 更新所有容器镜像（先查看变更日志） |
- [ ] 更新主机操作系统（`apt update && apt upgrade`） |
- [ ] 测试备份恢复功能 |
- [ ] 更新密码和配置文件 |
- [ ] 检查SSL证书的有效期 |
- [ ] 查看Grafana仪表盘中的数据趋势 |
- [ ] 清理未使用的Docker网络和卷资源 |

---

## 第11阶段：高级技巧

### 多节点架构设计

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Node 1    │     │   Node 2    │     │   Node 3    │
│ (Proxy/DNS) │────│ (Services)  │────│   (NAS)     │
│ Traefik     │     │ Apps        │     │ TrueNAS     │
│ Pi-hole     │     │ Databases   │     │ NFS/SMB     │
│ Authelia    │     │ Media       │     │ Backup      │
└─────────────┘     └─────────────┘     └─────────────┘
       ↑                   ↑                   ↑
       └───────── Tailscale Mesh ──────────────┘
```

### Docker Compose版本要求（Compose v2.20及以上）

```yaml
# Shared fragments
include:
  - path: ../common/traefik-labels.yml
  - path: ../common/logging.yml

services:
  app:
    # inherits common configs
```

### 使用GitOps管理家庭实验室环境

```
homelab-configs/           # Git repo
├── .github/
│   └── workflows/
│       └── deploy.yml     # CI: lint + push to server
├── stacks/
│   ├── traefik/
│   ├── monitoring/
│   └── media/
├── scripts/
└── README.md
```

**工作流程**：在本地编辑Compose配置文件 → 提交更改 → 通过Webhook推送到服务器 → 使用CI工具部署
**推荐工具**：Flux/ArgoCD（功能较强），或简单的`git pull && docker compose up -d`命令

### 硬件冗余方案

| 组件 | 解决方案 | 成本 |
|-----------|----------|------|
| 电源供应 | 不间断电源（如APC Back-UPS 600VA+） | 60-150美元 |
| 存储 | RAID1/ZFS镜像（避免使用RAID0） | 需要额外购买硬盘 |
| 网络 | 双网卡、管理型交换机 | 30-100美元 |
| 服务器 | 第二台服务器（备用或作为活动节点） | 100-400美元 |

**规则**：RAID仅用于提高数据可靠性，不能替代备份措施；它只能防止硬盘故障，无法防止数据被勒索软件破坏或丢失。

---

## 第12阶段：故障排除

### 常见问题及解决方法

### 常见问题与解决步骤

```
Service not accessible?
├── Can you ping the server? → No → Network/firewall issue
├── Is the container running? (`docker ps`) → No → Check logs: `docker logs <name>`
├── Is the port exposed? (`docker port <name>`) → No → Check compose ports/networks
├── Is Traefik routing? (Check Traefik dashboard) → No → Check labels, network
├── Is DNS resolving? (`dig app.example.com`) → No → Check DNS provider
└── SSL error? → Check acme.json permissions (chmod 600), cert resolver logs
```

### Docker调试命令

```bash
# Container not starting
docker logs <name> --tail 50
docker inspect <name> | jq '.[0].State'

# Network issues
docker network ls
docker network inspect <network>
docker exec <name> ping other-container

# Resource issues
docker stats                          # Live resource usage
docker system df                      # Disk usage
docker volume ls -f dangling=true     # Orphaned volumes

# Nuclear options (use carefully)
docker compose down && docker compose up -d    # Full restart
docker system prune -af --volumes              # Clean EVERYTHING
```

### 性能优化建议

| 问题症状 | 可能原因 | 解决方法 |
|---------|-------------|-----|
| 文件访问速度慢 | 数据库使用的是HDD | 将数据库迁移到SSD |
| CPU空闲时间过高 | 监控频率过高 | 增加数据采集间隔 |
| 容器因内存不足而崩溃 | 未设置内存限制 | 设置`deploy.resources.limits.memory` |
| Nextcloud运行缓慢 | 缺少Redis缓存 | 添加Redis容器 |
| Jellyfin性能不佳 | 未启用硬件转码功能 | 启用GPU直通 |
| Docker构建过程缓慢 | 未启用层级缓存 | 使用多阶段构建流程并配置`.dockerignore`文件 |

---

## 服务配置快速参考

### Vaultwarden（密码管理器）

```yaml
services:
  vaultwarden:
    image: vaultwarden/server:1.30.5
    container_name: vaultwarden
    restart: unless-stopped
    volumes:
      - vaultwarden-data:/data
    environment:
      - SIGNUPS_ALLOWED=false       # Disable after creating your account
      - WEBSOCKET_ENABLED=true
      - ADMIN_TOKEN=${ADMIN_TOKEN}  # Generate: openssl rand -base64 48
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.vault.rule=Host(`vault.example.com`)"
```

### Immich（照片备份工具）

```yaml
# Use their official docker-compose.yml from:
# https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml
# Key settings:
# - Set UPLOAD_LOCATION to a large storage mount
# - Enable hardware transcoding if GPU available
# - Set IMMICH_MACHINE_LEARNING_URL for face detection
```

### Paperless-ngx（文档管理工具）

```yaml
services:
  paperless:
    image: ghcr.io/paperless-ngx/paperless-ngx:2.4
    container_name: paperless
    restart: unless-stopped
    volumes:
      - paperless-data:/usr/src/paperless/data
      - paperless-media:/usr/src/paperless/media
      - ./consume:/usr/src/paperless/consume  # Drop PDFs here
      - ./export:/usr/src/paperless/export
    environment:
      - PAPERLESS_OCR_LANGUAGE=eng
      - PAPERLESS_TIME_ZONE=Europe/London
      - PAPERLESS_ADMIN_USER=${ADMIN_USER}
      - PAPERLESS_ADMIN_PASSWORD=${ADMIN_PASS}
```

---

## 家庭实验室质量评估（0-100分）

| 评估维度 | 权重 | 分数 |
|-----------|--------|----------|-------------|-----------------|
| 安全性 | 20% | 使用默认密码、开放端口 | 配置防火墙和SSL、使用强密码、启用双因素认证 |
| 备份 | 20% | 无备份措施 | 仅本地备份、未经过测试 | 实施3-2-1备份策略、每月进行验证 |
| 监控 | 15% | 无监控工具 | 仅使用Uptime Kuma | 配备完整的监控系统（指标、日志记录） |
| 文档记录 | 10% | 无文档记录 | 为每个服务/端口编写文档、定期更新文档 |
| 更新频率 | 10% | 很少更新 | 手动更新、定期安排更新 |
| 可靠性 | 10% | 系统经常崩溃 | 配备UPS、自动重启机制、定期检查系统健康状况 |
| 性能 | 10% | 系统运行缓慢、经常崩溃 | 配置适当的内存限制、使用SSD、启用硬件转码 |
| 可扩展性 | 10% | 依赖单台服务器 | 无扩展计划 | 配置了多节点架构 |

---

## 10个常见的自主托管错误

| 缺误 | 修正方法 |
|---|---------|-----|
| 1 | 使用`:latest`标签 | 固定镜像版本（例如：`image:1.2.3`） |
| 2 | 不进行备份 | 实施3-2-1备份策略，并定期测试恢复过程 |
| 3 | 直接暴露服务端口 | 所有服务都通过反向代理访问 |
| 4 | 使用默认密码 | 立即更改密码，并使用密码管理工具 |
| 5 | 未配置监控 | 至少使用Uptime Kuma进行基本监控，使用Grafana进行详细监控 |
| 6 | 认为RAID等于备份 | RAID主要用于保护硬盘，而非数据 |
| 7 | 一开始就过度设计系统 | 从小规模开始，根据实际需求逐步增加复杂性 |
| 8 | 未编写文档 | 为每个服务、每个端口、每个定时任务都编写详细的文档 |
| 9 | 忽视更新 | 必须定期更新软件和硬件 |
| 10 | 以root用户权限运行容器 | 使用非root用户权限运行容器，并限制SSH访问权限 |

---

## 常用命令

| 命令 | 功能 |
|-----|---------|
| "设置新服务" | 指导用户根据安全最佳实践创建Compose配置文件 |
| "审计我的家庭实验室安全配置" | 进行安全检查 |
| "规划我的备份策略" | 为系统设计3-2-1备份方案 |
| "我的容器经常崩溃" | 指导用户根据故障排除流程解决问题 |
| "帮助我设置Traefik代理" | 生成适用于生产环境的Traefik配置文件并配置SSL |
| "比较不同的NAS解决方案" | 根据需求选择合适的NAS产品 |
| "优化我的Docker配置" | 检查Compose配置文件中的安全性和性能设置 |
| "设置监控系统" | 部署Uptime Kuma、Grafana监控工具 |
| "规划硬件升级" | 根据实际需求评估硬件配置 |
| "从云环境迁移到自主托管环境" | 制定迁移计划并处理数据迁移和服务映射 |
| "设置远程访问方案" | 比较不同的VPN服务，并选择合适的远程访问方案 |

---

---

## 自主托管实用建议