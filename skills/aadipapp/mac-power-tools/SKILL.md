---
name: MacPowerTools
description: 一套专为macOS用户设计的强大工具集，集系统清理功能与安全可靠的Android文件传输功能于一体。
author: tempguest
version: 1.0.0
license: MIT
---
# MacPowerTools

MacPowerTools 将开发人员和高级用户所需的各种实用工具整合到一个统一的工具集中。

## 功能

### 系统清理
- **回收站清空**：清空回收站中的文件。
- **缓存清理**：删除 `~/Library/Caches` 中超过 7 天的旧缓存文件。
- **下载文件清理**：删除超过 30 天的下载文件。
- **安全机制**：默认采用“模拟执行”模式（`--dry-run`），以防止意外删除文件。

### 安全文件传输
- **Android 设备传输**：通过 ADB 将文件传输到 Android 设备。
- **文件完整性检查**：在传输前后验证文件的 SHA256 校验和。
- **防止覆盖**：检查目标设备上是否存在同名文件，以避免意外覆盖。

## 命令

- `cleanup [--force]`：执行系统清理操作。如果不使用 `--force` 选项，程序将以模拟模式运行。
- `transfer <source_file> [--dest <remote_path>] [--force]`：将文件安全地传输到连接的 Android 设备。

## 使用示例

```bash
# Clean up system (Dry Run)
cleanup

# Actually delete files
cleanup --force

# Transfer a file to Android
transfer ./release_build.apk --dest /sdcard/Builds/
```