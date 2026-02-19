---
name: zfs
description: "在 OpenZFS（适用于 Linux 和 macOS）系统中，用户需要执行以下操作时，可以使用本文档：创建或管理 ZFS 池（pool）、配置 ZFS 数据集（dataset）及其属性、设置快照（snapshot）或复制功能（通过 `zfs send/recv` 命令）、优化 ZFS 性能（通过调整 ARC（Automatic Recycle）、记录大小（recordsize）、压缩设置以及特殊虚拟设备（vdev）等选项）、排查出现故障的 ZFS 池问题、配置 ZFS 加密功能、规划基于 ZFS 的存储架构，以及其他与 ZFS、ZFS 池（zpool）相关的管理任务。"
---
# ZFS管理

## 重要提示：生产环境中禁止使用基于文件的池（File-Backed Pools）

**强烈建议不要在生产环境中使用基于文件的池（例如循环回环设备，loopback devices）**。大语言模型（LLMs）通常会默认使用 `truncate -s 10G /tmp/disk.img` + `zpool create tank /tmp/disk.img` 的方式来创建池，因为这种方式易于演示。然而，这种做法会牺牲ZFS的自我修复功能、I/O性能以及数据写入的可靠性。

基于文件的池仅适用于学习或持续集成（CI）测试场景。除非明确处于测试环境中，否则应始终使用真实的块设备（block devices）：

```bash
# Linux — always use /dev/disk/by-id/ for stable names
zpool create tank mirror \
  /dev/disk/by-id/scsi-SATA_WDC_WD40EFRX_WD-WCC4E1234567 \
  /dev/disk/by-id/scsi-SATA_WDC_WD40EFRX_WD-WCC4E7654321

# macOS
zpool create tank mirror /dev/disk2 /dev/disk3
```

如果用户明确要求进行测试或演示，可以使用基于文件的池，但需在文档中注明该设置不适用于生产环境。

## 池管理

### 创建池

创建池时，务必指定 `ashift=12`（对于某些NVMe设备可指定为 `13`），以确保与物理扇区大小相匹配：

```bash
# Mirror (2-disk, 50% usable, best performance)
zpool create -o ashift=12 tank mirror /dev/disk/by-id/disk1 /dev/disk/by-id/disk2

# raidz2 (minimum recommended for production data)
zpool create -o ashift=12 tank raidz2 \
  /dev/disk/by-id/disk{1..6}

# Multiple vdevs (better performance than single wide vdev)
zpool create -o ashift=12 tank \
  mirror /dev/disk/by-id/disk1 /dev/disk/by-id/disk2 \
  mirror /dev/disk/by-id/disk3 /dev/disk/by-id/disk4
```

### 扩展和修改池

```bash
# Add vdev (cannot be undone — plan carefully)
zpool add tank mirror /dev/disk/by-id/new1 /dev/disk/by-id/new2

# Replace disk (starts resilver)
zpool replace tank /dev/disk/by-id/old /dev/disk/by-id/new

# Add cache (L2ARC), log (SLOG), or special vdev
zpool add tank cache /dev/disk/by-id/nvme-cache
zpool add tank log mirror /dev/disk/by-id/nvme-log1 /dev/disk/by-id/nvme-log2
zpool add tank special mirror /dev/disk/by-id/nvme-special1 /dev/disk/by-id/nvme-special2
```

## 数据集管理

### 使用推荐默认设置创建数据集

```bash
# Always set compression. Inherit from parent when possible.
zfs set compression=lz4 tank
zfs set atime=off tank
zfs set xattr=sa tank          # Linux only — faster extended attributes

# Create dataset hierarchy
zfs create tank/data
zfs create -o recordsize=8K tank/data/postgres
zfs create -o recordsize=1M tank/data/media
zfs create -o recordsize=1M tank/data/backups
```

### 加密

```bash
# Create encrypted dataset (cannot encrypt existing data)
zfs create -o encryption=aes-256-gcm -o keyformat=passphrase tank/secure

# Key from file (for automation)
zfs create -o encryption=aes-256-gcm -o keyformat=raw \
  -o keylocation=file:///etc/zfs/keys/tank-secure.key tank/secure

# Load/unload keys
zfs load-key tank/secure
zfs unload-key tank/secure
```

## 快照

```bash
# Create
zfs snapshot tank/data@daily_$(date +%Y-%m-%d)
zfs snapshot -r tank@daily_$(date +%Y-%m-%d)   # recursive

# List
zfs list -t snapshot -o name,used,refer -s creation

# Access (read-only, no mount needed)
ls /tank/data/.zfs/snapshot/daily_2024-01-15/

# Rollback
zfs rollback tank/data@daily_2024-01-15

# Destroy
zfs destroy tank/data@old-snapshot
```

## 健康检查

运行内置的健康检查脚本，以快速获取池的状态信息：

```bash
bash scripts/zfs_health_check.sh           # all pools
bash scripts/zfs_health_check.sh tank       # specific pool
```

该脚本会显示池的当前状态、容量使用情况（超过80%时的警告信息）、设备错误信息，以及基于文件的虚拟设备（vdevs）的清理状态。

## 参考文件

有关特定主题的详细指南，请参阅以下文档：

- **[properties.md](references/properties.md)** — 完整的ZFS属性参考（包括池、数据集、压缩和加密设置）。在设置或推荐属性值时请参考此文档。
- **[workload-tuning.md](references/workload-tuning.md)** — 根据工作负载类型提供关于记录大小、压缩算法、去重策略、ARC（Automatic Recycle）、SLOG（Segmented Log）、L2ARC（Logical Second ARC）等功能的配置建议。在调整性能或规划池拓扑结构时请参考此文档。其中还包含了生产环境与测试环境之间的使用差异。
- **[replication.md](references/replication.md)** — 介绍快照功能、ZFS的数据发送/接收机制、通过SSH进行的远程复制、加密传输方式，以及同步对象（syncoid）/安全对象（sanoid）的自动化复制方案。在设置备份或复制策略时请参考此文档。
- **[troubleshooting.md](references/troubleshooting.md)** — 涵盖池性能下降时的恢复方法、清理错误处理、数据损坏问题、性能诊断技巧，以及常见的使用错误。在排查或解决问题时请参考此文档。
- **[platform-notes.md](references/platform-notes.md)** — 介绍Linux与macOS之间的差异（包括安装流程、设备命名规则、内核集成方式、挂载行为等）。当用户使用macOS或需要了解平台特定注意事项时，请参考此文档。