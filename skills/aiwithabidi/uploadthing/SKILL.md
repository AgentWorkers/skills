---
name: uploadthing
description: "**Uploadthing 文件托管服务**：通过 Uploadthing API 实现文件的上传、列表管理和查询功能。支持简单的文件上传，并提供自动的 CDN 分发服务；同时支持文件元数据的存储与查询以及文件使用情况的跟踪记录。该服务专为 AI 代理程序设计，仅依赖 Python 标准库，无任何额外依赖项。可用于文件上传、文件托管、CDN 分发、媒体内容管理以及 Web 应用程序中的文件存储需求。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📤", "requires": {"env": ["UPLOADTHING_SECRET"]}, "primaryEnv": "UPLOADTHING_SECRET", "homepage": "https://www.agxntsix.ai"}}
---
# 📤 Uploadthing

Uploadthing 是一个文件托管服务，允许您通过 Uploadthing API 上传、列出和管理文件。

## 主要功能

- **文件上传**：支持上传带有元数据的文件。
- **文件列表**：可以按条件过滤并查看已上传的文件。
- **文件删除**：根据文件键删除文件。
- **URL 生成**：为文件生成 CDN 链接。
- **使用情况跟踪**：记录文件的存储和带宽使用情况。
- **文件元数据**：包括文件名、大小、类型和上传日期。
- **批量操作**：一次删除多个文件。
- **应用配置**：允许您配置应用程序的相关设置。

## 必需参数

| 参数 | 是否必填 | 说明 |
|--------|--------|-------------------|
| `UPLOADTHING_SECRET` | ✅ | 用于访问 Uploadthing API 的密钥/令牌 |

## 快速入门

```bash
# List uploaded files
python3 {baseDir}/scripts/uploadthing.py files --limit 50
```

```bash
# Upload a file
python3 {baseDir}/scripts/uploadthing.py upload document.pdf
```

```bash
# Delete files
python3 {baseDir}/scripts/uploadthing.py delete --keys file_key1,file_key2
```

```bash
# Get usage stats
python3 {baseDir}/scripts/uploadthing.py usage
```



## 命令说明

### `files`
列出已上传的文件。
```bash
python3 {baseDir}/scripts/uploadthing.py files --limit 50
```

### `upload`
上传文件。
```bash
python3 {baseDir}/scripts/uploadthing.py upload document.pdf
```

### `delete`
删除文件。
```bash
python3 {baseDir}/scripts/uploadthing.py delete --keys file_key1,file_key2
```

### `usage`
获取文件的使用情况统计信息。
```bash
python3 {baseDir}/scripts/uploadthing.py usage
```

### `app-info`
获取应用程序的配置信息。
```bash
python3 {baseDir}/scripts/uploadthing.py app-info
```

### `url`
获取文件的 URL。
```bash
python3 {baseDir}/scripts/uploadthing.py url file_key
```

### `rename`
重命名文件。
```bash
python3 {baseDir}/scripts/uploadthing.py rename file_key "new-name.pdf"
```


## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出，请添加 `--human` 参数。

```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/uploadthing.py files --limit 5

# Human-readable
python3 {baseDir}/scripts/uploadthing.py files --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|------|--------|
| `{baseDir}/scripts/uploadthing.py` | 主要的命令行工具，用于执行所有 Uploadthing 操作 |

## 数据政策

本服务 **从不将数据存储在本地**。所有请求都会直接发送到 Uploadthing API，结果会直接返回到标准输出（stdout）。您的文件将保存在 Uploadthing 的服务器上。

## 致谢
---
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
该功能属于 OpenClaw 代理的 **AgxntSix Skill Suite** 套件的一部分。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)