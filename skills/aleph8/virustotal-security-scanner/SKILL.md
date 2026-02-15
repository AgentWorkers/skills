---
name: virustotal-security-scanner
description: 使用 VirusTotal API 通过 curl 或 Python 工具扫描文件和 URL。检查文件哈希值，上传文件，并管理相关评论。
homepage: https://www.virustotal.com/
metadata: {"clawdbot":{"emoji":"🦠","requires":{"bins":["curl","jq","sha256sum","python3"],"env":["VT_API_KEY"]}}}
---

# VirusTotal 扫描器技能

可以使用标准系统工具（如 `curl`）或 Python 工具与 VirusTotal API 进行交互。

## 设置

1. 获取您的 API 密钥：https://www.virustotal.com/gui/user/[your-username]/apikey
2. 设置环境变量：
   ```bash
   export VT_API_KEY="your-api-key-here"
   ```

## 隐私警告

**重要提示**：此技能涉及将数据发送到 VirusTotal（一个公开的威胁情报服务）。
1. **未经用户明确同意，切勿上传文件。**
2. **不要在评论或描述中包含个人身份信息（PII）。**
3. **请告知用户**，上传的文件将会与安全社区共享，其他研究人员也可以下载这些文件。

## 最佳实践：缓存结果

为了避免不必要的 API 调用并遵守使用限制，建议将 JSON 结果缓存在本地。可以使用 `~/.vt/` 目录来存储这些报告。

```bash
# Create cache directory
mkdir -p ~/.vt

# Save a report to cache
HASH="your-file-hash"
curl --request GET \
     --url "https://www.virustotal.com/api/v3/files/$HASH" \
     --header "accept: application/json" \
     --header "x-apikey: $VT_API_KEY" > ~/.vt/$HASH.json

# Query the cache instead of the API (if jq available)
cat ~/.vt/$HASH.json | jq '.data.attributes.last_analysis_stats'
```

## 使用方法：使用 `curl`（推荐方法）

### 1. 计算文件的 SHA256 哈希值（检查文件是否存在）
计算文件的 SHA256 哈希值，以确认该文件是否已在 VirusTotal 的数据库中。

```bash
# Linux
sha256sum /path/to/file

# MacOS
shasum -a 256 /path/to/file

# Windows (PowerShell)
Get-FileHash /path/to/file -Algorithm SHA256
```

### 2. 检查文件报告
检查某个文件的哈希值是否已在 VirusTotal 的数据库中。

```bash
curl --request GET \
     --url "https://www.virustotal.com/api/v3/files/{hash}" \
     --header "accept: application/json" \
     --header "x-apikey: $VT_API_KEY"
```

### 3. 上传文件
**隐私提示**：仅在没有用户明确许可的情况下上传文件。

#### 小文件（< 32MB）
```bash
curl --request POST \
     --url "https://www.virustotal.com/api/v3/files" \
     --header "accept: application/json" \
     --header "x-apikey: $VT_API_KEY" \
     --form "file=@/path/to/file"
```

#### 大文件（> 32MB）
首先获取一个唯一的上传 URL：
```bash
curl --request GET \
     --url "https://www.virustotal.com/api/v3/files/upload_url" \
     --header "accept: application/json" \
     --header "x-apikey: $VT_API_KEY"
```
然后将该文件上传到该 URL：
```bash
curl --request POST \
     --url "{upload_url_from_previous_step}" \
     --header "accept: application/json" \
     --header "x-apikey: $VT_API_KEY" \
     --form "file=@/path/to/large_file"
```

### 4. 文件评论
**隐私警告**：请勿在评论中包含个人身份信息或敏感数据。提供关于文件来源或下载者的相关信息会很有帮助。

#### 获取评论
```bash
curl --request GET \
     --url "https://www.virustotal.com/api/v3/files/{hash}/comments?limit=10" \
     --header "accept: application/json" \
     --header "x-apikey: $VT_API_KEY"
```

#### 添加评论
```bash
curl --request POST \
     --url "https://www.virustotal.com/api/v3/files/{hash}/comments" \
     --header "accept: application/json" \
     --header "content-type: application/json" \
     --header "x-apikey: $VT_API_KEY" \
     --data '{"data": {"type": "comment", "attributes": {"text": "File found in /tmp directory via downloader script."}}}'
```

### 5. URL 扫描

#### 扫描一个 URL
```bash
curl --request POST \
     --url "https://www.virustotal.com/api/v3/urls" \
     --header "accept: application/json" \
     --header "content-type: application/x-www-form-urlencoded" \
     --header "x-apikey: $VT_API_KEY" \
     --data "url={url_to_analyze}"
```

#### 获取 URL 报告
注意：URL 的标识通常是其 SHA256 哈希值。

```bash
curl --request GET \
     --url "https://www.virustotal.com/api/v3/urls/{url_id_or_hash}" \
     --header "accept: application/json" \
     --header "x-apikey: $VT_API_KEY"
```

## 使用方法：Python 工具

如果系统缺少相应的库，或者您更喜欢使用 Python，可以使用提供的辅助脚本。

### 安装要求
```bash
pip install requests
```

### 1. 计算哈希值
```bash
python3 vt-scanner/calc_hash.py /path/to/file
```

### 2. API 客户端（`vt_client.py`）
该脚本封装了 API 的各个接口，便于使用。

#### 检查文件
```bash
python3 vt-scanner/vt_client.py check-file {hash}
```

#### 上传文件
自动处理小文件和大文件的上传流程。

```bash
python3 vt-scanner/vt_client.py upload-file /path/to/file
```

#### 获取评论
```bash
# For a file
python3 vt-scanner/vt_client.py get-comments {file_hash}

# For a URL
python3 vt-scanner/vt_client.py get-comments {url_id} --url
```

#### 添加评论
```bash
python3 vt-scanner/vt_client.py add-comment {id} "Your comment here"
```

#### 扫描 URL
```bash
python3 vt-scanner/vt_client.py scan-url "http://example.com"
```

#### 查看 URL 报告
```bash
python3 vt-scanner/vt_client.py check-url {url_id}
```