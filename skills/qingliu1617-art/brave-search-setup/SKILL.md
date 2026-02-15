---
name: brave-search-setup
description: 配置 Brave Search API 并解决与网络/代理相关的问题，以支持 web_search 功能。适用于以下情况：  
1. 设置 Brave Search API 密钥；  
2. 解决 web_search 的数据获取失败问题；  
3. 在 macOS 上使用 Clash/V2Ray/Surge 为 OpenClaw 工具配置代理；  
4. 使用 web_search/web_fetch 工具诊断 “数据获取失败” 的错误。
---

# Brave Search 设置与代理配置

配置 Brave Search API 并解决 OpenClaw 网络连接问题。

## 先决条件

- Brave Search API 密钥（从 https://brave.com/search/api/ 获取）
- 安装了 OpenClaw CLI
- 如果使用的是 GFW（中国国家防火墙），则需要安装 macOS 上的代理客户端（如 Clash/V2Ray/Surge）

## 快速设置

### 第一步：配置 API 密钥

```bash
# Option A: Via config.patch (key will be stored securely)
openclaw gateway config.patch --raw '{"tools":{"web":{"search":{"apiKey":"YOUR_BRAVE_API_KEY","enabled":true,"provider":"brave"}}}}'
```

或者直接编辑 `~/.openclaw/openclaw.json` 文件：
```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "brave",
        "apiKey": "YOUR_BRAVE_API_KEY"
      }
    }
  }
}
```

### 第二步：不使用代理进行测试

```bash
openclaw web.search --query "test" --count 1
```

如果测试成功 → 完成。
如果出现 “fetch failed” 的错误 → 继续进行代理配置。

## 代理配置（macOS）

### 第三步：检测代理端口

常见代理端口号：
- Clash：7890（HTTP），7891（SOCKS5），7897（混合端口）
- Surge：6152，6153
- V2Ray：1080，10808

检测实际使用的代理端口：
```bash
# Check if Clash is running
ps aux | grep -i clash

# Find mixed-port from Clash config
cat "~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml" | grep mixed-port

# Or test common ports
for port in 7890 7891 7897 6152 6153 1080 10808; do
  if nc -z 127.0.0.1 $port 2>/dev/null; then
    echo "Port $port is open"
  fi
done
```

### 第四步：设置系统代理

**方法 A：使用 launchctl（推荐，重启后代理设置仍然有效）**
```bash
# Set for current session and future sessions
launchctl setenv HTTPS_PROXY http://127.0.0.1:7897
launchctl setenv HTTP_PROXY http://127.0.0.1:7897
```

**方法 B：通过 Shell 设置环境变量（仅适用于当前会话）**
```bash
export HTTPS_PROXY=http://127.0.0.1:7897
export HTTP_PROXY=http://127.0.0.1:7897
```

**方法 C：将代理设置添加到 Shell 配置文件中（永久生效）**
```bash
echo 'export HTTPS_PROXY=http://127.0.0.1:7897' >> ~/.zshrc
echo 'export HTTP_PROXY=http://127.0.0.1:7897' >> ~/.zshrc
source ~/.zshrc
```

### 第五步：启用代理服务器的重启功能

```bash
openclaw gateway config.patch --raw '{"commands":{"restart":true}}'
```

### 第六步：使用代理重新启动代理服务器

```bash
# Restart to pick up proxy env vars
openclaw gateway restart

# Or use SIGUSR1
kill -USR1 $(pgrep -f "openclaw gateway")
```

### 第七步：验证配置是否正确

```bash
# Test web search
openclaw web.search --query "Brave Search test" --count 1

# Test web fetch
openclaw web.fetch --url "https://api.search.brave.com" --max-chars 100
```

## 故障排除

### 出现 “fetch failed” 错误，但浏览器可以正常访问 Google

**症状**：浏览器可以访问 Google，但 OpenClaw 工具无法正常使用。
**原因**：代理服务器在环境变量设置完成之前就已经启动了。
**解决方法**：在设置好 HTTPS_PROXY 后重新启动代理服务器。

### 重启代理服务器时遇到权限问题

**解决方法**：启用代理服务器的重启命令：
```bash
openclaw gateway config.patch --raw '{"commands":{"restart":true}}'
```

### API 密钥相关问题

**验证密钥是否已正确设置**：
```bash
openclaw gateway config.get | grep -A5 'web.*search'
```

**使用 curl 直接测试 API**：
```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=test&count=1" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

### 混合端口与专用端口

Clash 的 “混合端口”（默认为 7897）同时支持 HTTP 和 SOCKS5 协议。
**如果使用专用端口**：
- HTTP 代理：7890
- SOCKS5 代理：7891（需要分别配置）

## 高级设置：针对特定工具配置代理

并非所有 OpenClaw 工具都会自动使用设置的 HTTPS_PROXY。对于不支持代理的工具，需要手动配置：
```bash
# Use proxychains-ng
brew install proxychains-ng

# Configure
sudo tee /usr/local/etc/proxychains.conf <<EOF
strict_chain
proxy_dns
[ProxyList]
http 127.0.0.1 7897
EOF

# Run with proxy
proxychains4 openclaw web.search --query "test"
```

## 工作流程总结

1. **配置 API 密钥** → 通过 `config.patch` 文件或直接编辑 `openclaw.json`
2. **进行测试** → 如果测试失败，说明需要配置代理
3. **检测代理端口** → 查看 Clash 或 Surge 的配置文件
4. **设置环境变量** → 使用 `launchctl setenv` 或 Shell 命令设置环境变量
5. **重启代理服务器** → 使用 `openclaw gateway restart` 命令重启代理服务器
6. **验证配置** → 运行搜索测试

## 参考资料

- Brave Search API 文档：https://api.search.brave.com/app/docs
- OpenClaw 配置指南：https://docs.openclaw.ai/config
- Clash Verge 项目：https://github.com/clash-verge-rev/clash-verge-rev