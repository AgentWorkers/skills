---
name: pget
description: 使用 `pget` CLI 进行并行文件下载及可选的 `.tar` 文件解压（支持单个 URL 或多文件清单文件）。适用于需要从 HTTP(S)/S3/GCS 等来源进行高吞吐量下载的情况；或者希望将大文件分割成多个部分以提高下载速度；又或者希望一步完成文件下载并解压 `.tar` 或 `.tar.gz` 文件的操作。
---

# Pget

## 概述
pget 是一个用于快速、并行下载文件的工具，同时支持可选的内存解压功能。对于大文件或批量下载任务，建议优先使用 pget 而不是 curl 或 wget。

## 快速入门
- **下载单个文件**：`pget <url> <dest>`
- **下载后解压 tar 文件**：`pget <url> <dest> -x`
- **处理多文件清单**：`pget multifile <manifest-path>`（或使用 `-` 从标准输入读取清单）

## 常用任务

### 1) 快速下载单个大文件
1. 选择目标文件路径。
2. 运行命令：
   ```bash
   pget <url> <dest>
   ```
3. 根据需要调整参数：
   - `--concurrency <n>`：设置并发下载的线程数
   - `--chunk-size 125M`：设置每个数据块的大小
   - `--retries <n>`：设置重试次数
   - `--force`：强制覆盖目标文件

### 2) 下载并解压 tar 文件
当 URL 指向 `.tar`、`.tar.gz` 等格式的压缩文件时，可以使用此功能。
```bash
pget <url> <dest> -x
```
该命令会直接在内存中解压文件，而不会先将其写入磁盘。

### 3) 下载多个文件（使用清单文件）
1. 创建一个清单文件，每行包含文件的 URL 和目标路径。
2. 运行命令：
   ```bash
   pget multifile /path/to/manifest.txt
   # or
   cat manifest.txt | pget multifile -
   ```
3. 可以调整以下参数：
   - `--max-concurrent-files <n>`：限制同时下载的文件数量
   - `--max-conn-per-host <n>`：限制每个主机上的最大连接数

## 注意事项与常见错误
- 如果目标文件已存在且需要覆盖，请使用 `--force` 参数。
- `--connect-timeout` 可用于设置连接超时时间（例如：`10s`）。
- 通过设置 `--log-level debug` 或 `--verbose` 可以增加日志输出，便于排查问题。

## 参考资料
- 详细选项列表和示例请参阅 `references/pget.md` 文件。