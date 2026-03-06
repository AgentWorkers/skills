---
name: synology-dsm
description: 通过 DSM Web API 管理 Synology NAS。支持身份验证、浏览和管理文件（FileStation）、管理下载任务（DownloadStation），以及查询系统信息。当用户提到 Synology、NAS、DSM、FileStation 或 DownloadStation，或者希望与他们的 NAS 设备进行交互时，可以使用该功能。
---
# Synology DSM 技巧

使用 `curl` 通过 DSM Web API 与 Synology NAS 进行交互。

## 先决条件

用户必须设置以下环境变量（或直接提供这些值）：

- `SYNOLOGY_HOST` — NAS 的主机名或 IP 地址（例如：`192.168.1.100`）
- `SYNOLOGY_PORT` — DSM 的端口号（HTTP 为 `5000`，HTTPS 为 `5001`）
- `SYNOLOGY_USER` — DSM 的用户名
- `SYNOLOGY_PASS` — DSM 的密码

基础 URL：`http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi`

> **安全提示**：始终优先使用 HTTPS（端口 5001）。切勿在显示给用户的命令中硬编码凭据——应使用 `$SYNOLOGY_PASS` 来引用凭据。如果用户未设置环境变量，请让他们提供连接详细信息。

## 第 1 步：身份验证

每个会话都以登录开始。使用 `format=sid` 来获取会话 ID。

### 登录

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.API.Auth&version=6&method=login\
&account=$SYNOLOGY_USER&passwd=$SYNOLOGY_PASS\
&session=FileStation&format=sid" | jq .
```

响应：
```json
{"data": {"sid": "YOUR_SESSION_ID"}, "success": true}
```

将获取到的 `sid` 保存下来，用于后续的所有请求：`SID=<响应中的值>`

### 注销

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.API.Auth&version=6&method=logout\
&session=FileStation&_sid=$SID"
```

### 两步验证（2FA）处理

如果登录返回错误代码 `406`，则表示该账户启用了两步验证。请用户提供他们的 OTP 代码，然后在登录请求中添加 `&otp_code=<CODE>`。

### 会话注意事项

- 会话在闲置约 15 分钟后超时
- 如果收到错误代码 `106`（会话超时），请重新进行身份验证
- 完成操作后务必注销以清除会话信息

## 第 2 步：API 发现（可选）

查询 NAS 上所有可用的 API：

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/query.cgi?\
api=SYNO.API.Info&version=1&method=query" | jq .
```

这将返回每个 API 的名称、路径及其支持的版本范围。这对于检查已安装的软件包非常有用。

## 第 3 步：FileStation — 文件管理

所有 FileStation 操作都使用 `_sid=$SID` 进行身份验证。

### 列出共享文件夹（根目录）

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.List&version=2&method=list_share&_sid=$SID" | jq .
```

### 列出文件夹中的文件

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.List&version=2&method=list\
&folder_path=/volume1/homes&additional=size,time&_sid=$SID" | jq .
```

参数：`folder_path`（必填），`offset`，`limit`，`sort_by`（name|size|mtime），`sort_direction`（asc|desc），`additional`（size,time,perm,type）

### 创建文件夹

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.CreateFolder&version=2&method=create\
&folder_path=/volume1/homes&name=new_folder&_sid=$SID" | jq .
```

### 重命名文件或文件夹

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Rename&version=2&method=rename\
&path=/volume1/homes/old_name&name=new_name&_sid=$SID" | jq .
```

### 删除文件或文件夹

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Delete&version=2&method=delete\
&path=/volume1/homes/unwanted_file&_sid=$SID" | jq .
```

对于批量删除操作，可以使用 `method=start` 获取任务 ID，然后通过 `method=status&taskid=<id>` 来查询任务状态。

### 上传文件

```bash
curl -s -X POST \
  -F "api=SYNO.FileStation.Upload" \
  -F "version=2" \
  -F "method=upload" \
  -F "path=/volume1/homes" \
  -F "overwrite=true" \
  -F "file=@/local/path/to/file.txt" \
  -F "_sid=$SID" \
  "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi"
```

### 下载文件

```bash
curl -s -o output_file.txt \
  "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Download&version=2&method=download\
&path=/volume1/homes/file.txt&mode=download&_sid=$SID"
```

### 搜索文件

```bash
# Start search
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Search&version=2&method=start\
&folder_path=/volume1&pattern=*.pdf&_sid=$SID" | jq .
# Returns taskid

# Get results
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.Search&version=2&method=list\
&taskid=<TASK_ID>&_sid=$SID" | jq .
```

### 获取文件/文件夹信息

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.FileStation.List&version=2&method=getinfo\
&path=/volume1/homes/file.txt&additional=size,time&_sid=$SID" | jq .
```

有关 FileStation API 的完整参考，请参阅 [references/filestation-api.md](references/filestation-api.md)。

## 第 4 步：DownloadStation — 下载管理

### 获取 DownloadStation 信息

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Info&version=1&method=getinfo&_sid=$SID" | jq .
```

### 列出所有下载任务

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Task&version=1&method=list\
&additional=transfer&_sid=$SID" | jq .
```

`additional=transfer` 参数可以显示下载/上传的速度和进度。

### 添加下载任务（URL）

```bash
curl -s -X POST \
  -d "api=SYNO.DownloadStation.Task&version=1&method=create\
&uri=https://example.com/file.zip&_sid=$SID" \
  "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi"
```

### 添加下载任务（种子文件）

```bash
curl -s -X POST \
  -F "api=SYNO.DownloadStation.Task" \
  -F "version=1" \
  -F "method=create" \
  -F "file=@/local/path/to/file.torrent" \
  -F "_sid=$SID" \
  "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi"
```

### 暂停/恢复/删除任务

```bash
# Pause
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Task&version=1&method=pause\
&id=<TASK_ID>&_sid=$SID"

# Resume
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Task&version=1&method=resume\
&id=<TASK_ID>&_sid=$SID"

# Delete (force_complete=false keeps downloaded files)
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DownloadStation.Task&version=1&method=delete\
&id=<TASK_ID>&force_complete=false&_sid=$SID"
```

多个任务 ID 可以用逗号分隔：`&id=task1,task2,task3`

有关 DownloadStation API 的完整参考，请参阅 [references/downloadstation-api.md](references/downloadstation-api.md)。

## 第 5 步：系统信息

### 获取 DSM 系统信息

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DSM.Info&version=2&method=getinfo&_sid=$SID" | jq .
```

返回的信息包括：型号、内存、序列号、DSM 版本、运行时间、温度等。

### 获取存储/卷信息

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.Storage.CGI.Storage&version=1&method=load_info&_sid=$SID" | jq .
```

### 获取网络信息

```bash
curl -s "http://$SYNOLOGY_HOST:$SYNOLOGY_PORT/webapi/entry.cgi?\
api=SYNO.DSM.Network&version=1&method=list&_sid=$SID" | jq .
```

## 错误处理

所有 API 的响应格式如下：`{"success": true/false, "data": {...}, "error": {"code": N}}`

### 常见错误代码

| 代码 | 含义 | 处理方式 |
|------|---------|--------|
| 100 | 未知错误 | 重试一次 |
| 101 | 请求错误 | 检查参数 |
| 102 | 不存在该 API | 该软件包未安装 |
| 103 | 不存在该方法 | 检查 API 版本 |
| 104 | 不支持的版本 | 使用较低版本的 API |
| 105 | 没有权限 | 检查用户权限 |
| 106 | 会话超时 | 重新进行身份验证 |
| 107 | 会话中断 | 重新进行身份验证 |

### 与身份验证相关的错误代码

| 代码 | 含义 |
|------|---------|
| 400 | 密码错误 | 重新输入密码 |
| 401 | 账户被禁用 |
| 402 | 没有权限 |
| 406 | 需要输入 OTP 代码 |

有关所有错误代码的详细信息，请参阅 [references/error-codes.md](references/error-codes.md)。

## 工作流程示例

典型的操作流程如下：

1. 登录并获取会话 ID（SID）
2. 执行相关操作（列出文件、添加下载任务等）
3. 完成操作后注销

在继续执行任何操作之前，请始终检查响应中的 `"success": true` 字段。如果遇到错误代码 106 或 107，系统会自动重新登录。