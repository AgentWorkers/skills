---
name: checksum
description: 这是一个命令行工具（CLI），用于生成和验证文件的加密校验和（MD5、SHA1、SHA256）。该工具支持对目录进行递归处理，并能够直接从文件中验证其校验和。
---
# 校验和工具

这是一个专用的命令行工具（CLI），用于确保文件完整性。您可以使用该工具来验证下载的文件、检查文件是否发生变化，或为发布的文件生成校验和。

## 主要功能

- **多种算法支持：** 支持 `md5`（默认）、`sha1`、`sha256`、`sha512` 算法。
- **递归哈希计算：** 可为整个目录生成校验和。
- **文件验证：** （计划中）能够将文件与校验和列表进行比对。
- **JSON 输出：** 以机器可读的格式输出结果，便于集成到其他脚本中。

## 使用方法

### 计算文件校验和

```bash
node skills/checksum/index.js --file <path> [--algo <md5|sha1|sha256>]
```

示例：
```bash
node skills/checksum/index.js --file package.json --algo sha256
# Output: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  package.json
```

### 递归计算目录校验和

```bash
node skills/checksum/index.js --dir <path> [--algo <md5|sha1|sha256>] [--json]
```

示例：
```bash
node skills/checksum/index.js --dir src/ --algo sha1 --json > checksums.json
```

## 为什么选择这个工具而不是 `md5sum`？

- **跨平台兼容：** 只要安装了 Node.js，即可在任何操作系统（Linux、macOS、Windows）上使用。
- **无需依赖系统组件：** 不依赖于 `coreutils` 等系统工具的安装。
- **JSON 输出格式：** 输出结果为 JSON 格式，便于在其他脚本中解析和使用。