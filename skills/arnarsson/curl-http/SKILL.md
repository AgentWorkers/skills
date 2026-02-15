---
name: curl-http
description: 用于HTTP请求、API测试和文件传输的基本curl命令。
homepage: https://curl.se/
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["curl"]}}}
---

# curl - HTTP客户端

这是一个用于发送HTTP请求和传输数据的命令行工具。

## 基本请求

### GET请求
```bash
# Simple GET request
curl https://api.example.com

# Save output to file
curl https://example.com -o output.html
curl https://example.com/file.zip -O  # Use remote filename

# Follow redirects
curl -L https://example.com

# Show response headers
curl -i https://example.com

# Show only headers
curl -I https://example.com

# Verbose output (debugging)
curl -v https://example.com
```

### POST请求
```bash
# POST with data
curl -X POST https://api.example.com/users \
  -d "name=John&email=john@example.com"

# POST JSON data
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'

# POST from file
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d @data.json

# Form upload
curl -X POST https://api.example.com/upload \
  -F "file=@document.pdf" \
  -F "description=My document"
```

### 其他HTTP方法
```bash
# PUT request
curl -X PUT https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane"}'

# DELETE request
curl -X DELETE https://api.example.com/users/1

# PATCH request
curl -X PATCH https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email":"newemail@example.com"}'
```

## 请求头与身份验证

### 自定义请求头
```bash
# Add custom header
curl -H "User-Agent: MyApp/1.0" https://example.com

# Multiple headers
curl -H "Accept: application/json" \
     -H "Authorization: Bearer token123" \
     https://api.example.com
```

### 身份验证
```bash
# Basic auth
curl -u username:password https://api.example.com

# Bearer token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com

# API key in header
curl -H "X-API-Key: your_api_key" \
  https://api.example.com

# API key in URL
curl "https://api.example.com?api_key=your_key"
```

## 高级功能

### 超时与重试
```bash
# Connection timeout (seconds)
curl --connect-timeout 10 https://example.com

# Max time for entire operation
curl --max-time 30 https://example.com

# Retry on failure
curl --retry 3 https://example.com

# Retry delay
curl --retry 3 --retry-delay 5 https://example.com
```

### Cookies
```bash
# Send cookies
curl -b "session=abc123" https://example.com

# Save cookies to file
curl -c cookies.txt https://example.com

# Load cookies from file
curl -b cookies.txt https://example.com

# Both save and load
curl -b cookies.txt -c cookies.txt https://example.com
```

### 代理
```bash
# Use HTTP proxy
curl -x http://proxy.example.com:8080 https://api.example.com

# With proxy authentication
curl -x http://proxy:8080 -U user:pass https://api.example.com

# SOCKS proxy
curl --socks5 127.0.0.1:1080 https://api.example.com
```

### SSL/TLS
```bash
# Ignore SSL certificate errors (not recommended for production)
curl -k https://self-signed.example.com

# Use specific SSL version
curl --tlsv1.2 https://example.com

# Use client certificate
curl --cert client.crt --key client.key https://example.com

# Show SSL handshake details
curl -v https://example.com 2>&1 | grep -i ssl
```

## 响应处理

### 输出格式
```bash
# Silent mode (no progress bar)
curl -s https://api.example.com

# Show only HTTP status code
curl -s -o /dev/null -w "%{http_code}" https://example.com

# Custom output format
curl -w "\nTime: %{time_total}s\nStatus: %{http_code}\n" \
  https://example.com

# Pretty print JSON (with jq)
curl -s https://api.example.com | jq '.'
```

### 范围请求
```bash
# Download specific byte range
curl -r 0-1000 https://example.com/large-file.zip

# Resume download
curl -C - -O https://example.com/large-file.zip
```

## 文件操作

### 下载文件
```bash
# Download file
curl -O https://example.com/file.zip

# Download with custom name
curl -o myfile.zip https://example.com/file.zip

# Download multiple files
curl -O https://example.com/file1.zip \
     -O https://example.com/file2.zip

# Resume interrupted download
curl -C - -O https://example.com/large-file.zip
```

### 上传文件
```bash
# FTP upload
curl -T file.txt ftp://ftp.example.com/upload/

# HTTP PUT upload
curl -T file.txt https://example.com/upload

# Form file upload
curl -F "file=@document.pdf" https://example.com/upload
```

## 测试与调试

### API测试
```bash
# Test REST API
curl -X GET https://api.example.com/users
curl -X GET https://api.example.com/users/1
curl -X POST https://api.example.com/users -d @user.json
curl -X PUT https://api.example.com/users/1 -d @updated.json
curl -X DELETE https://api.example.com/users/1

# Test with verbose output
curl -v -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass"}'
```

### 性能测试
```bash
# Measure request time
curl -w "Total time: %{time_total}s\n" https://example.com

# Detailed timing
curl -w "\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nTransfer: %{time_starttransfer}s\nTotal: %{time_total}s\n" \
  -o /dev/null -s https://example.com
```

### 常见调试技巧
```bash
# Show request and response headers
curl -v https://api.example.com

# Trace request
curl --trace-ascii trace.txt https://api.example.com

# Include response headers in output
curl -i https://api.example.com
```

## 常用模式

**快速JSON API测试：**
```bash
curl -s https://api.github.com/users/octocat | jq '{name, bio, followers}'
```

**带进度条的下载：**
```bash
curl -# -O https://example.com/large-file.zip
```

**POST JSON并提取字段：**
```bash
curl -s -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"user":"test","pass":"secret"}' | jq -r '.token'
```

**检查URL是否可访问：**
```bash
if curl -s --head --fail https://example.com > /dev/null; then
  echo "Site is up"
else
  echo "Site is down"
fi
```

**并行下载：**
```bash
for i in {1..10}; do
  curl -O https://example.com/file$i.jpg &
done
wait
```

## 有用的参数

- `-X`：HTTP方法（GET、POST、PUT、DELETE等）
- `-d`：要发送的数据（POST/PUT）
- `-H`：自定义请求头
- `-o`：输出文件
- `-O`：将输出文件保存为远程文件名
- `-L`：跟随重定向
- `-i`：在输出中包含请求头
- `-I`：仅输出请求头
- `-v`：详细输出
- `-s`：静默模式
- `-S`：即使在静默模式下也显示错误信息
- `-f`：在HTTP错误时静默失败
- `-k`：忽略SSL安全检查
- `-u`：基本身份验证
- `-F`：多部分表单数据
- `-b`：发送Cookies
- `-c`：保存Cookies
- `-w`：自定义输出格式

## 使用技巧

- 在脚本中使用`-s`选项以隐藏进度条
- 结合使用`-sS`选项实现静默模式但显示错误信息
- 使用`-L`选项处理重定向（例如，缩短的URL）
- 使用`-v`选项进行调试
- 使用`jq`工具处理JSON响应
- 将常用请求保存为shell别名或脚本
- 使用`--config`选项处理复杂的重复请求

## 文档

官方文档：https://curl.se/docs/
手册：`man curl`
HTTP方法：https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods