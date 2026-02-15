---
name: android-transfer-secure
description: **安全地将文件从 macOS 传输到 Android，并进行校验和验证以及路径验证。**
author: tempguest
version: 0.1.0
license: MIT
---
# 安全的 Android 文件传输

此技能可让您以高安全标准将文件传输到 Android 设备：
- **校验和验证**：通过比较 SHA256 哈希值来确保数据完整性。
- **路径验证**：防止目录遍历和未经授权的路径访问。
- **覆盖保护**：防止设备上的数据意外丢失。

## 命令

- `transfer`：将文件推送到连接的 Android 设备。