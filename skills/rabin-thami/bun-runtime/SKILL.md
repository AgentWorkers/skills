---
name: bun-runtime
description: Bun运行时提供了针对文件系统、进程和网络操作的功能。当您需要执行特定于Bun的操作（如`Bun.file()`、`Bun.write()`或`Bun.glob()`）以实现优化的文件处理，或者在使用Bun的原生进程/网络API时，可以使用这些功能。这些功能会在请求Bun运行时特性、通过Bun进行文件操作，或执行高性能I/O任务时被触发。
---

# Bun 运行时

Bun 运行时提供了用于文件系统、进程和网络任务的原生操作功能。

## 使用场景

在以下情况下可以使用这些功能：
- 使用 Bun 的原生文件 API（`Bun.file()`、`Bun.write()`、`Bun.glob()`）
- 需要在 Bun 环境中实现优化的 I/O 操作
- 运行 Bun 特定的进程命令
- 使用 Bun 的 `fetch` 功能发起网络请求

## 文件系统操作

### 读取文件

```bash
scripts/bun-fs.sh read /path/to/file.txt
```

返回 JSON 格式的数据：`{"content": "文件内容"}`

### 写入文件

```bash
scripts/bun-fs.sh write /path/to/file.txt "content here"
```

会自动创建父目录。
返回 JSON 格式的数据：`{"written": true, "path": "/path/to/file.txt"}`

### 查找文件

```bash
scripts/bun-glob.sh "/tmp/*.txt"
```

返回 JSON 格式的数据：`{"files": ["/tmp/file1.txt", "/tmp/file2.txt"], "count": 2}`

## 进程操作

### 执行命令

```bash
scripts/bun-process.sh "ls -la"
```

运行 shell 命令并返回输出结果。

## 网络操作

### HTTP 请求

```bash
scripts/bun-fetch.sh "https://api.example.com" "GET"
```

使用 Bun 的 `fetch` 功能发起 HTTP 请求。

## 注意事项：
- 所有脚本均使用 Bun 的原生 API 以提高性能
- 文件操作会自动处理编码问题
- 错误会以清晰的消息形式返回