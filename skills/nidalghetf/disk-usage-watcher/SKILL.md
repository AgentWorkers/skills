# 磁盘使用情况监控工具

## 描述
该工具用于监控指定路径下的磁盘空间和 inode 使用情况，并在达到预设阈值时发送警报。这对于防止磁盘空间耗尽至关重要。

## 使用方法
该工具可以由用户直接调用，也可以通过 cron 任务每 15 分钟自动运行。

### 示例命令：
- `check_disk_space_on_root_partition`：检查根分区的磁盘空间
- `monitor_all_mount_points_and_alert_at_85percent`：监控所有挂载点，并在磁盘使用率达到 85% 时发送警报
- `show_disk_usage_statistics`：显示磁盘使用统计信息

## 输入参数：
- `threshold_percent`（数字）：当磁盘使用率超过此百分比时触发警报（默认值：85%）
- `inode_threshold`（数字）：当 inode 使用率超过此百分比时触发警报（默认值：85%）
- `paths`（数组）：需要监控的具体路径（默认值：所有已挂载的分区）
- `alert_on_failure`（布尔值）：如果检查失败是否发送警报（默认值：true）

## 输出结果：
- `status`（字符串）：`success` 或 `failure`
- `details`（对象）：包含磁盘使用情况信息（包括挂载点、使用百分比以及触发的警报）

## 依赖库：
- `openclaw/exec`：用于执行 `df` 命令
- `openclaw/notify`：用于发送警报

## 测试说明
```bash
openclaw call disk-usage-watcher --params '{"paths": ["/"]}'
```