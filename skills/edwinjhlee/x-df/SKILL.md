---
name: x-df
description: >
  **改进版的 `df` 命令：** 结合了磁盘使用情况和挂载信息的功能。支持输出 CSV、TSV 格式的数据，并具备文件系统类型检测功能。  
  **依赖关系：** 该命令属于 `x-cmd` 模块。请先安装 `x-cmd`（具体安装方法请参阅相关文档）。
license: Apache-2.0
compatibility: POSIX Shell

metadata:
  author: Li Junhao
  version: "1.0.2"
  category: x-cmd-extension
  tags: [x-cmd, system, df, disk, storage]
---
# x df - 磁盘空闲空间查看器

> 一个增强版的 `df` 命令，它将 `df` 和 `mount` 的输出结果以多种格式进行整合。

---

## 快速入门

```bash
# Interactive disk usage viewer (default in TTY)
x df

# TSV format output (default when piped)
x df | cat
```

---

## 主要特性

- **联合输出**：结合了 `df` 和 `mount` 命令的输出信息
- **多种格式支持**：TSV、CSV、TUI 应用程序格式以及原始数据格式
- **跨平台兼容**：支持 Linux、macOS 和 Windows
- **自动检测**：在 TTY 环境下以交互式模式显示结果；通过管道传输时输出为 TSV 格式

---

## 输出字段

### Linux / Windows

| 字段 | 描述 | 示例 |
|-------|-------------|---------|
| `Filesystem` | 设备路径 | `/dev/sda1` |
| `Type` | 文件系统类型 | `ext4`, `ntfs` |
| `Size` | 总大小 | `500G` |
| `Used` | 已使用空间 | `200G` |
| `Avail` | 可用空间 | `300G` |
| `Use%` | 使用百分比 | `40%` |
| `Mounted_path` | 挂载点 | `/`, `/home` |
| `Mounted_attr` | 挂载属性 | `rw,relatime` |

### macOS（额外字段）

| 字段 | 描述 | 示例 |
|-------|-------------|---------|
| `Capacity` | 容量百分比 | `40%` |
| `iused` | 已使用的 inode 数 | `1000000` |
| `ifree` | 可用的 inode 数 | `9000000` |
| `%iused` | inode 使用率 | `10%` |

---

## 命令参数

| 命令 | 描述 |
|---------|-------------|
| `x df` | 自动模式：TTY 环境下以交互式方式显示；通过管道传输时输出为 TSV 格式 |
| `x df --app` | 以 TUI 界面显示结果 |
| `x df --csv` | 以 CSV 格式输出 |
| `x df --tsv` | 以 TSV 格式输出 |
| `x df --raw` | 以原始系统命令格式输出 |
| `x df --numeric` | 以纯数字形式显示大小 |

---

## 使用示例

### 基本用法

```bash
# Interactive view (TTY)
x df

# TSV format
x df --tsv

# CSV format
x df --csv
```

### 过滤与数据处理

```bash
# Find large filesystems (>100GB)
x df --tsv | awk -F'\t' 'NR>1 && $3 > 100'

# Check specific mount point
x df --tsv | grep "/home"

# Get usage percentages only
x df --tsv | awk -F'\t' '{print $1, $6}'
```

### 数据处理示例

```bash
# Convert to JSON via csv
x df --csv | x csv tojson

# SQL-like query on disk usage
x df --csv | x csv sql "SELECT * WHERE Use% > 80"
```

---

## 平台说明

### Linux
- 使用 `df` 命令以及 `/proc/mounts` 或 `mount` 命令获取磁盘信息
- 支持所有功能

### macOS
- 使用 `df` 命令以及 `mount` 命令获取磁盘信息
- 提供额外的 inode 信息（如已使用的 inode 数、可用的 inode 数以及 inode 使用率）

### Windows
- 使用 `wmic` 或 PowerShell 的 `Get-Volume` 命令获取磁盘信息
- 支持所有功能

---

## 与原生 `df` 的对比

| 命令 | 输出内容 |
|---------|--------|
| `df -h` | 基本的磁盘使用情况 |
| `mount` | 挂载信息 |
| `x df` | 结合了文件系统类型和挂载属性的详细信息 |

```bash
# Native df
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       500G  200G  300G  40% /

# x df (combined with mount info)
$ x df --tsv
Filesystem    Type    Size    Used    Avail   Use%    Mounted_path    Mounted_attr
/dev/sda1     ext4    500G    200G    300G    40%     /               rw,relatime
```

---

## 相关文档

- 原生 `df(1)` 命令手册页
- 原生 `mount(8)` 命令手册页