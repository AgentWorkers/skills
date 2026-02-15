---
description: 分析磁盘使用情况，查找大型或陈旧的文件，并提供安全的清理建议。
---

# 磁盘清理工具

该工具用于分析磁盘使用情况，并识别需要清理的文件或文件夹。

## 使用说明

1. **文件系统概述**：
   ```bash
   df -h --output=source,size,used,avail,pcent,target | grep -v tmpfs
   ```

2. **目录分析**（占用最多空间的目录）：
   ```bash
   du -sh /path/* 2>/dev/null | sort -rh | head -20
   ```

3. **查找大文件**：
   ```bash
   find /path -type f -size +100M -exec ls -lh {} \; 2>/dev/null | sort -k5 -rh | head -20
   ```

4. **查找旧文件**（90 天以上未修改的文件）：
   ```bash
   find /path -type f -mtime +90 -size +10M -exec ls -lh {} \; 2>/dev/null | sort -k5 -rh
   ```

5. **常见的清理目标**：
   ```bash
   # Package caches
   du -sh ~/.cache/pip ~/.npm/_cacache ~/.cache/yarn 2>/dev/null
   # Docker
   docker system df 2>/dev/null
   # Logs
   du -sh /var/log/* 2>/dev/null | sort -rh | head -10
   # Trash
   du -sh ~/.local/share/Trash 2>/dev/null
   # Temp
   du -sh /tmp 2>/dev/null
   ```

6. **报告格式**：
   ```
   💾 Disk Report — /home (85% used, 12GB free)

   ## Top Space Users
   | Path | Size | Last Modified |
   |------|------|---------------|
   | ~/Downloads | 8.2 GB | various |
   | ~/.cache | 3.1 GB | today |

   ## Cleanup Suggestions
   | Action | Saves | Command | Risk |
   |--------|-------|---------|------|
   | Clear npm cache | ~1.2 GB | npm cache clean --force | 🟢 Safe |
   | Docker prune | ~4.5 GB | docker system prune -a | 🟡 Review |
   | Old logs | ~800 MB | find /var/log -mtime +30 -delete | 🟡 Review |
   ```

## 安全性注意事项

- **切勿自动删除文件**——始终显示删除命令，让用户进行确认；
- 如果可能，优先使用 `trash` 命令而非 `rm` 命令（因为 `trash` 命令允许恢复文件）；
- 扫描时跳过 `/proc`、`/sys`、`/dev` 目录；
- 不要扫描用户没有权限访问的目录。

## 特殊情况处理

- **权限问题**：使用 `2>/dev/null` 来忽略权限错误；对于无法访问的目录，应记录相关信息；
- **符号链接**：使用 `-not -type l` 选项以避免重复计算符号链接所指向的文件；
- **已挂载的驱动器**：请识别出已挂载的驱动器，避免误删外部存储设备中的文件。

## 所需工具

- 标准的 Unix 工具：`du`、`df`、`find`、`sort`；
- 不需要任何 API 密钥。