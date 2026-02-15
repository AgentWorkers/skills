---
description: 监控网站的运行时间（uptime），测量响应时间（response times），并检查任何URL的HTTP状态码（HTTP status codes）。
---

# 运行时间监控器

用于检查网站的可用性、响应时间以及HTTP状态码。

## 所需条件

- `curl`（大多数系统已预安装）
- 无需API密钥

## 使用说明

### 单个URL检查
```bash
curl -o /dev/null -s -w "HTTP %{http_code} | DNS: %{time_namelookup}s | Connect: %{time_connect}s | TLS: %{time_appconnect}s | Total: %{time_total}s\n" -L --max-time 10 https://example.com
```

### 批量检查（多个URL）
```bash
for url in https://example.com https://google.com https://github.com; do
  result=$(curl -o /dev/null -s -w "%{http_code} %{time_total}" -L --max-time 10 "$url" 2>/dev/null)
  code=$(echo $result | awk '{print $1}')
  time=$(echo $result | awk '{print $2}')
  echo "$url: HTTP $code (${time}s)"
done
```

### 持续监控
```bash
# Check every 30 seconds for 5 minutes (10 checks)
for i in $(seq 1 10); do
  curl -o /dev/null -s -w "%{http_code} %{time_total}s" --max-time 10 https://example.com
  echo " [$(date +%H:%M:%S)]"
  sleep 30
done
```

### 输出格式
```
## 🌐 Uptime Report — <timestamp>

| URL | Status | Code | DNS | Connect | TLS | Total |
|-----|--------|------|-----|---------|-----|-------|
| example.com | 🟢 Up | 200 | 0.012s | 0.034s | 0.089s | 0.145s |
| broken.com | 🔴 Down | 000 | — | — | — | timeout |
| slow.com | 🟡 Slow | 200 | 0.015s | 0.040s | 0.095s | 3.210s |

**Thresholds**: 🟢 < 1s | 🟡 1–3s | 🔴 > 3s or error
```

## 特殊情况处理

- **重定向**：使用`-L`选项来跟踪重定向。如果最终访问的URL与输入的URL不同，请报告该最终URL。
- **超时**：使用`--max-time 10`选项以避免程序挂起。在这种情况下，将状态报告为“🔴 下线”。
- **自签名证书**：仅当用户明确要求时才使用`-k`选项（这种情况下可能存在安全风险）。
- **非HTTP协议**：该工具仅支持HTTP/HTTPS协议。对于TCP/ping测试，请使用`nc`或`ping`命令。
- **DNS解析失败**：如果`curl`返回代码000，说明DNS解析失败，请相应地报告这一情况。
- **需要HTTP认证**：401/403状态码并不意味着网站“下线”，请注意区分这两种情况。

## 安全性注意事项

- 该工具仅执行GET请求，不会修改任何数据。
- 请勿监控那些需要在URL中包含认证令牌的网站（否则这些令牌会被记录下来）。
- 在发送请求之前，请验证URL的格式是否正确。