---
name: cron-backup
description: 设置具有版本跟踪和清理功能的定时自动备份机制。适用于以下场景：  
1. 需要定期备份目录或文件的用户；  
2. 需要监控文件版本变化并在文件更新时自动备份的用户；  
3. 需要自动清理旧备份以节省存储空间的用户；  
4. 需要为配置文件、代码仓库或用户数据制定备份策略的用户。
---

# Cron 备份

支持自动备份调度、版本检测以及智能清理功能。

## 快速入门

### 一次性备份
```bash
# Backup a directory with timestamp
./scripts/backup.sh /path/to/source /path/to/backup/dir

# Backup with custom name
./scripts/backup.sh /path/to/source /path/to/backup/dir my-backup
```

### 每日备份
```bash
# Set up daily backup at 2 AM
./scripts/setup-cron.sh daily /path/to/source /path/to/backup/dir "0 2 * * *"
```

### 基于版本变化的备份
```bash
# Backup only when version changes
./scripts/backup-versioned.sh /path/to/source /path/to/version/file /path/to/backup/dir
```

### 清理旧备份
```bash
# Keep only last 7 days of backups
./scripts/cleanup.sh /path/to/backup/dir 7
```

## 核心功能

### 1. 目录备份
- 生成带有时间戳的 tar.gz 压缩文件
- 保留文件的权限和目录结构
- 排除常见的临时文件（如 node_modules、.git 文件等）

### 2. 基于版本变化的备份
- 监控版本文件或命令输出
- 仅在版本发生变化时执行备份
- 非常适用于软件更新场景

### 3. 定时执行
- 集成系统 cron 服务
- 支持自定义调度规则
- 记录备份执行结果

### 4. 自动清理
- 删除超过 N 天的旧备份文件
- 仅保留最少数量的备份文件
- 防止磁盘空间耗尽

## 脚本

所有脚本位于 `scripts/` 目录中：
- `backup.sh`：执行单次备份
- `backup-versioned.sh`：基于版本变化的备份
- `setup-cron.sh`：设置 cron 任务
- `cleanup.sh`：清理旧备份文件
- `list-backups.sh`：列出所有可用备份文件

## 备份文件命名规则

备份文件的名字遵循以下格式：`{名称}_YYYYMMDD_HHMMSS.tar.gz`
示例：
- `openclabak_20260204_101500.tar.gz`
- `myapp_20260204_000000.tar.gz`

## 工作流程

### 设置自动备份

1. **确定备份策略**
   - 备份哪些文件或目录
   - 将备份文件存储在哪里
   - 备份的频率
   - 备份文件的保留策略（保留多少天）

2. **执行首次备份**
   ```bash
   ./scripts/backup.sh /source /backup
   ```

3. **设置定时任务**
   ```bash
   ./scripts/setup-cron.sh daily /source /backup "0 2 * * *"
   ```

4. **配置备份清理规则**
   ```bash
   ./scripts/setup-cron.sh cleanup /backup "" "0 3 * * *" 7
   ```

### 基于版本变化的备份流程

对于会更新版本的软件（如 OpenClaw）：
1. **获取当前版本信息**
   - 命令：`openclaw --version`
   - 保存版本信息到文件：`/path/to/version.txt`

2. **设置基于版本的备份机制**
   ```bash
   ./scripts/backup-versioned.sh /app /app/version.txt /backups/app
   ```

3. **安排版本检查任务**
   ```bash
   ./scripts/setup-cron.sh versioned /app /backups/app "0 */6 * * *"
   ```

## 常见备份策略

### 模式 1：每日用户数据备份
```bash
# Backup workspace daily, keep 30 days
./scripts/setup-cron.sh daily /home/user/workspace /backups/workspace "0 2 * * *"
./scripts/setup-cron.sh cleanup /backups/workspace "" "0 3 * * *" 30
```

### 模式 2：基于版本变化的应用程序备份
```bash
# Backup when application updates
./scripts/setup-cron.sh versioned /opt/myapp /backups/myapp "0 */6 * * *"
./scripts/setup-cron.sh cleanup /backups/myapp "" "0 4 * * 0" 10
```

### 模式 3：多目录备份
```bash
# Backup multiple directories
./scripts/backup.sh /home/user/.config /backups/config
./scripts/backup.sh /home/user/projects /backups/projects
```

## Cron 定时格式

标准 cron 格式：`分钟 小时 日 月 星期`

常见调度示例：
- 每天凌晨 2 点：`0 2 * * *`
- 每 6 小时备份一次：`0 */6 * * *`
- 每周日备份一次：`0 0 * * 0`
- 每 30 分钟备份一次：`*/30 * * * *`

## 备份清理策略

- **基于时间**：保留备份文件 N 天
- **基于文件数量**：仅保留最近的 N 个备份文件
- **综合策略**：默认保留至少 7 天的备份文件，但至少保留 3 个版本

## 常见问题及解决方法

- **权限问题**：确保脚本可执行（使用 `chmod +x scripts/*.sh`）
- **Cron 任务未运行**：检查 cron 服务状态（`systemctl status cron`）
- **磁盘空间不足**：手动清理旧备份或调整备份保留策略
- **备份失败**：确认源目录存在且可读