---
name: dns-networking
description: 调试DNS解析和网络连接问题。适用于排查DNS故障、测试端口连通性、诊断防火墙规则、使用`curl`的详细模式检查HTTP请求、配置`/etc/hosts`文件，以及解决代理和证书相关问题。
metadata: {"clawdbot":{"emoji":"🌐","requires":{"anyBins":["dig","nslookup","curl","ping","nc"]},"os":["linux","darwin","win32"]}}
---

# DNS与网络

本章节介绍如何调试DNS解析、网络连接以及HTTP相关的问题。内容包括使用`dig`/`nslookup`命令、端口测试、防火墙规则检查、`curl`诊断工具、`/etc/hosts`文件配置、代理设置以及证书相关问题的排查方法。

## 使用场景

- DNS名称无法解析或解析为错误的IP地址
- 连接被拒绝或超时错误
- 需要诊断防火墙或安全组规则的影响
- HTTP请求失败且原因不明
- 代理配置出现问题
- SSL/TLS证书出现错误
- 需要测试服务之间的网络连接

## DNS调试

### 查询DNS记录

```bash
# A record (IP address)
dig example.com
dig +short example.com

# Specific record types
dig example.com MX        # Mail servers
dig example.com CNAME     # Aliases
dig example.com TXT       # Text records (SPF, DKIM, etc.)
dig example.com NS        # Name servers
dig example.com AAAA      # IPv6 address
dig example.com SOA       # Start of Authority

# Query a specific DNS server
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Trace the full resolution path
dig +trace example.com

# Reverse lookup (IP → hostname)
dig -x 93.184.216.34

# nslookup (simpler, works everywhere)
nslookup example.com
nslookup example.com 8.8.8.8    # Query specific server
nslookup -type=MX example.com

# host (simplest)
host example.com
host -t MX example.com
```

### 检查DNS记录的传播情况

```bash
# Query multiple public DNS servers
for dns in 8.8.8.8 1.1.1.1 9.9.9.9 208.67.222.222; do
    echo -n "$dns: "
    dig +short @"$dns" example.com
done

# Check TTL (time to live)
dig example.com | grep -E '^\S+\s+\d+\s+IN\s+A'
# The number is TTL in seconds
```

### 本地DNS问题排查

```bash
# Check /etc/resolv.conf (which DNS server the system uses)
cat /etc/resolv.conf

# Check /etc/hosts (local overrides)
cat /etc/hosts

# Flush DNS cache
# macOS:
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
# Linux (systemd-resolved):
sudo systemd-resolve --flush-caches
# Windows:
ipconfig /flushdns

# Check if systemd-resolved is running (Linux)
resolvectl status
```

### `/etc/hosts`文件的配置与使用

```bash
# /etc/hosts — local DNS overrides (no TTL, instant)

# Point a domain to localhost (for development)
127.0.0.1    myapp.local
127.0.0.1    api.myapp.local

# Block a domain
0.0.0.0      ads.example.com

# Test a migration (point domain to new server before DNS change)
203.0.113.50    example.com
203.0.113.50    www.example.com

# Multiple names for one IP
192.168.1.100   db.local redis.local cache.local
```

## 端口与网络连接测试

### 测试端口是否开放

```bash
# nc (netcat) — most reliable
nc -zv example.com 443
nc -zv -w 5 example.com 80    # 5 second timeout

# Test multiple ports
for port in 22 80 443 5432 6379; do
    nc -zv -w 2 example.com $port 2>&1
done

# /dev/tcp (bash built-in, no extra tools needed)
timeout 3 bash -c 'echo > /dev/tcp/example.com/443' && echo "Open" || echo "Closed"

# curl (also tests HTTP)
curl -sI -o /dev/null -w "%{http_code}" https://example.com

# Test from inside a Docker container
docker exec my-container nc -zv db 5432
```

### 网络路径诊断

```bash
# traceroute (show network hops)
traceroute example.com

# mtr (continuous traceroute with stats — best for finding packet loss)
mtr example.com
mtr -r -c 20 example.com   # Report mode, 20 packets

# ping
ping -c 5 example.com

# Show local network interfaces
ip addr show          # Linux
ifconfig              # macOS / older Linux

# Show routing table
ip route show         # Linux
netstat -rn           # macOS
route -n              # Linux (older)
```

### 检查系统正在监听的端口

```bash
# What's listening on which port (Linux)
ss -tlnp
ss -tlnp | grep :8080

# macOS
lsof -i -P -n | grep LISTEN
lsof -i :8080

# Older Linux
netstat -tlnp
netstat -tlnp | grep :8080

# Which process is using a port
lsof -i :3000
fuser 3000/tcp   # Linux
```

## `curl`诊断工具

### 详细请求日志查看

```bash
# Full verbose output (headers, TLS handshake, timing)
curl -v https://api.example.com/endpoint

# Show timing breakdown
curl -o /dev/null -s -w "
    DNS:        %{time_namelookup}s
    Connect:    %{time_connect}s
    TLS:        %{time_appconnect}s
    TTFB:       %{time_starttransfer}s
    Total:      %{time_total}s
    Status:     %{http_code}
    Size:       %{size_download} bytes
" https://api.example.com/endpoint

# Show response headers only
curl -sI https://api.example.com/endpoint

# Follow redirects and show each hop
curl -sIL https://example.com

# Resolve a domain to a specific IP (bypass DNS)
curl --resolve example.com:443:203.0.113.50 https://example.com

# Use a specific network interface
curl --interface eth1 https://example.com
```

### 常见HTTP问题的调试方法

```bash
# Test with different HTTP versions
curl --http1.1 https://example.com
curl --http2 https://example.com

# Test with specific TLS version
curl --tlsv1.2 https://example.com
curl --tlsv1.3 https://example.com

# Ignore certificate errors (debugging only)
curl -k https://self-signed.example.com

# Send request with custom Host header (virtual hosts)
curl -H "Host: example.com" https://203.0.113.50/

# Test CORS preflight
curl -X OPTIONS -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -v https://api.example.com/endpoint
```

## 防火墙基础知识

### Linux系统下的`iptables`

```bash
# List all rules
sudo iptables -L -n -v

# Allow incoming on port 80
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Allow incoming from specific IP
sudo iptables -A INPUT -s 203.0.113.0/24 -p tcp --dport 22 -j ACCEPT

# Block incoming on a port
sudo iptables -A INPUT -p tcp --dport 3306 -j DROP

# Save rules (persist across reboot)
sudo iptables-save > /etc/iptables/rules.v4
```

### Ubuntu/Debian系统下的`ufw`（更简单的防火墙管理工具）

```bash
# Enable
sudo ufw enable

# Allow/deny
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 203.0.113.0/24 to any port 22
sudo ufw deny 3306

# Check status
sudo ufw status verbose

# Reset all rules
sudo ufw reset
```

### macOS系统下的防火墙设置

```bash
# Check status
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Enable
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on

# Allow an application
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/local/bin/myapp
```

## 代理配置

### 环境变量的设置与使用

```bash
# Set proxy for most CLI tools
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1,.internal.example.com

# For curl specifically
export http_proxy=http://proxy.example.com:8080  # lowercase also works

# With authentication
export HTTPS_PROXY=http://user:password@proxy.example.com:8080
```

### 通过代理进行网络请求

```bash
# curl with explicit proxy
curl -x http://proxy.example.com:8080 https://httpbin.org/ip

# SOCKS proxy
curl --socks5 localhost:1080 https://httpbin.org/ip

# Verify your external IP through proxy
curl -x http://proxy:8080 https://httpbin.org/ip
curl https://httpbin.org/ip  # Compare with direct

# Test proxy connectivity
curl -v -x http://proxy:8080 https://example.com 2>&1 | grep -i "proxy\|connect"
```

### 常见的代理配置问题

```bash
# Node.js fetch/undici does NOT respect HTTP_PROXY
# Use undici ProxyAgent or node-fetch with http-proxy-agent

# Git through proxy
git config --global http.proxy http://proxy:8080
git config --global https.proxy http://proxy:8080
# Remove:
git config --global --unset http.proxy

# npm through proxy
npm config set proxy http://proxy:8080
npm config set https-proxy http://proxy:8080

# pip through proxy
pip install --proxy http://proxy:8080 package-name
```

## 证书问题排查

```bash
# Check certificate from a server
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | \
  openssl x509 -noout -subject -issuer -dates

# Check expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -enddate

# Download certificate chain
openssl s_client -showcerts -connect example.com:443 < /dev/null 2>/dev/null | \
  awk '/BEGIN CERT/,/END CERT/' > chain.pem

# Verify a certificate against CA bundle
openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt server.pem

# Check certificate for a specific hostname (SNI)
openssl s_client -connect cdn.example.com:443 -servername cdn.example.com

# Common error: "certificate has expired"
# Check the date on the server:
date
# If the system clock is wrong, certs will appear invalid
```

## 快速诊断脚本

```bash
#!/bin/bash
# net-check.sh — Quick network diagnostics
TARGET="${1:?Usage: net-check.sh <hostname> [port]}"
PORT="${2:-443}"

echo "=== Network Check: $TARGET:$PORT ==="

echo -n "DNS resolution: "
IP=$(dig +short "$TARGET" | head -1)
[[ -n "$IP" ]] && echo "$IP" || echo "FAILED"

echo -n "Ping: "
ping -c 1 -W 3 "$TARGET" > /dev/null 2>&1 && echo "OK" || echo "FAILED (may be blocked)"

echo -n "Port $PORT: "
nc -zv -w 5 "$TARGET" "$PORT" 2>&1 | grep -q "succeeded\|open" && echo "OPEN" || echo "CLOSED/FILTERED"

if [[ "$PORT" == "443" || "$PORT" == "8443" ]]; then
    echo -n "TLS: "
    echo | openssl s_client -connect "$TARGET:$PORT" -servername "$TARGET" 2>/dev/null | \
      grep -q "Verify return code: 0" && echo "VALID" || echo "INVALID/ERROR"

    echo -n "Certificate expiry: "
    echo | openssl s_client -connect "$TARGET:$PORT" 2>/dev/null | \
      openssl x509 -noout -enddate 2>/dev/null | sed 's/notAfter=//'
fi

echo "=== Done ==="
```

## 使用技巧

- `dig +short`是从命令行快速查询DNS记录的最快方法。使用`@8.8.8.8`可以绕过本地DNS缓存。
- `nc -zv`是最简单的端口连接测试工具；如果`nc`不可用，可以使用`bash`的`/dev/tcp`命令。
- `curl`的`-w`格式化选项可以显示请求的详细信息（包括耗时），有助于诊断HTTP请求的延迟问题（包括DNS解析、连接建立和TLS握手的时间）。
- DNS记录的传播速度取决于TTL（Time To Live）值。在确认DNS更改生效前，可以使用`dig`命令查看当前的TTL值。
- 修改`/etc/hosts`文件后，设置会立即生效（无需等待TTL更新时间）。在更改DNS设置前，可以使用它来测试域名解析是否正常。
- 当遇到“连接被拒绝”的错误时，首先使用`nc`检查端口是否开放，然后使用`ss -tlnp`或`lsof -i`命令确认目标服务是否正在监听。
- `mtr`比`traceroute`更适合诊断数据包丢失问题，因为它可以连续显示数据包在传输过程中的丢失情况。
- Node.js、Python的`requests`库等许多工具并不会自动使用`HTTP_PROXY`环境变量。请查阅相关工具的文档以确认代理设置是否生效。

## 注意事项

- 在使用这些工具时，请确保已正确配置系统环境变量，并根据具体操作系统和工具的文档进行操作。