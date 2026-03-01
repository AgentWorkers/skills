---
name: mac-cleaner
description: 分析并安全地清理 macOS 上的磁盘空间。适用于用户询问 Mac 存储空间问题、系统数据占用过多空间、需要清理磁盘以释放空间或管理存储空间的情况。该工具可清理缓存文件、iOS 模拟器数据、Xcode 数据、垃圾桶文件以及浏览器缓存。适合所有日常使用 macOS 的用户。
---
# Mac 清理工具

安全地分析并释放 macOS 上的磁盘空间。专为日常使用 Mac 的用户设计——无需任何技术知识。

## 使用场景

- “我的 Mac 显示系统数据占用了太多空间”
- “如何释放磁盘空间？”
- “为什么我的磁盘满了？”
- “清理 Mac 的存储空间”
- “是什么占用了我的磁盘空间？”

## 该工具涵盖的内容

| 类别 | 可以安全清理的内容 | 备注 |
|----------|---------------|-------|
| 用户缓存 | ✅ 可以 | 应用程序的临时文件 |
| iOS 模拟器 | ✅ 可以 | 未使用的模拟器设备 |
| Xcode 生成的数据 | ✅ 可以 | 编译生成的文件（可重新生成） |
| 浏览器缓存 | ✅ 可以 | Chrome、Safari、Firefox 的缓存 |
| 系统日志 | ✅ 仅清理旧日志 | 7 天以上的日志，需要 sudo 权限 |
| 回收站 | ✅ 可以 | 清空回收站 |
| iOS 备份 | ⚠️ 请确认 | 检查是否需要保留备份 |
| Parallels 虚拟机 | ⚠️ 请确认 | 仅在不需要 Windows 虚拟机时清理 |
| Time Machine 快照 | ⚠️ 请确认 | 可以删除旧快照 |

## 绝对不能删除的内容

- `/System` 文件夹的内容
- `/Library/Extensions` 或内核扩展程序
- `/private/var/db`（系统数据库）
- 正在使用的 iOS 备份文件
- 正在使用的 Parallels 虚拟机

## 快速入门

### 分析（安全模式，只读）

```bash
bash scripts/mac-cleanup.sh analyze
```

显示磁盘使用情况并识别占用大量空间的文件，但不会进行任何更改。

### 清理（需要用户确认）

```bash
bash scripts/mac-cleanup.sh clean
```

在用户确认后执行安全清理操作。

## 清理的内容

1. **用户缓存** (`~/Library/Caches/*`)
   - 应用程序的临时文件、缩略图、下载的内容
   - 安全：应用程序会自动重新生成这些文件

2. **Xcode 生成的数据** (`~/Library/Developer/Xcode/DerivedData/*`)
   - 编译生成的文件和中间文件
   - 安全：下次编译时会重新生成

3. **iOS 模拟器**（仅针对未使用的模拟器）
   - 旧的 iOS 模拟器镜像
   - 安全：可以通过 Xcode 重新下载

4. **浏览器缓存**
   - Chrome、Safari、Firefox 的缓存文件
   - 安全：重新加载网站后，登录会话会保留

5. **旧系统日志**（7 天以上的日志）
   - 需要 sudo 权限
   - 保留最近的日志以供调试使用

6. **回收站**
   - 清空回收站
   - 用户已经决定删除这些文件

## 对于需要手动处理的较大文件

如果脚本检测到需要手动处理的较大文件：

### iOS 设备备份（`~/Library/Application Support/MobileSync/Backup`）

```bash
# List backups
ls -lah ~/Library/Application\ Support/MobileSync/Backup/

# Delete specific backup (use folder name from above)
rm -rf ~/Library/Application\ Support/MobileSync/Backup/[FOLDER_NAME]
```

或者使用 **Finder → 位置 → [你的 iPhone] → 管理备份**

### Time Machine 本地快照

```bash
# List snapshots
tmutil listlocalsnapshots /

# Delete all local snapshots
sudo tmutil deletelocalsnapshots /

# Or delete specific date
sudo tmutil deletelocalsnapshots 2024-01-15-123456
```

### Parallels 虚拟机

打开 **Parallels Desktop**：
- 右键点击虚拟机 → **释放磁盘空间**（最安全的方法）
- 或者如果不需要 Windows 虚拟机，可以选择 **删除**

### WeChat / 大型应用程序

在应用程序内部进行清理：
- WeChat：设置 → 通用 → 存储 → 管理
- Telegram：设置 → 数据和存储 → 存储使用情况
- Slack：帮助 → 故障排除 → 清除缓存

## 需要手动检查的较大文件夹

| 路径 | 文件内容 | 是否可以安全删除？ |
|------|-----------|-----------------|
| `~/Downloads` | 下载的文件 | 请先检查 |
| `~/Movies` | 视频文件 | 请先检查 |
| `~/Parallels` | Windows 虚拟机 | 仅在不使用时删除 |
| `~/Library/Containers/com.tencent.xinWeChat` | WeChat 数据 | 通过 WeChat 应用程序进行清理 |
| `~/Library/Application Support` | 应用程序数据 | 根据应用程序情况判断是否可以删除 |

## 预期效果

对于日常使用 Mac 的用户：
- **普通用户**：释放 2-5 GB 磁盘空间
- **开发者**：释放 20-50 GB 磁盘空间（Xcode、模拟器相关文件）
- **经常使用消息应用程序的用户**：释放 50-100 GB 磁盘空间（WeChat、Telegram）
- **使用虚拟机的用户**：释放 50-200 GB 磁盘空间（如果删除了 Parallels 虚拟机）

## 故障排除

### 出现 “操作不被允许” 的错误

授予 Terminal 完整的磁盘访问权限：
1. 系统设置 → 隐私与安全 → 完整磁盘访问权限
2. 添加 Terminal（或 iTerm）到应用程序列表
3. 重新启动 Terminal

### 清理后没有释放太多空间

再次运行分析模式：
```bash
bash scripts/mac-cleanup.sh analyze
```

检查以下内容：
- iOS 设备备份（通常占用 50-200 GB 磁盘空间）
- Parallels 虚拟机（每个虚拟机可能占用 20-100 GB 磁盘空间）
- WeChat/Telegram 数据（可能占用 100 GB 以上）
- Time Machine 快照（可能会累积大量空间）

这些文件在删除前需要手动确认是否需要删除。

## 参考资料

- Apple 的存储空间管理文档：https://support.apple.com/guide/mac-help/check-storage-space-mchlc03eb677/mac
- 安全的 macOS 清理方法：https://support.apple.com/en-us/HT202083