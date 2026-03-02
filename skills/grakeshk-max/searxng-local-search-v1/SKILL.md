---
name: searxng
description: 使用自托管的 SearXNG 实例在网络上进行搜索。SearXNG 是一个尊重用户隐私的元搜索引擎，它能够汇总来自多个搜索引擎的结果。
metadata:
  clawdbot:
    config:
      optionalEnv:
        - SEARXNG_URL
tools:
  - name: search
    description: Search the web using the self-hosted SearXNG instance.
    args:
      - name: query
        type: string
        description: Search query
      - name: categories
        type: string
        description: Search categories (general, images, news, videos, it, science)
        default: general
    command:
      kind: http
      method: GET
      url: ${SEARXNG_URL:-http://localhost:8080}/search
      query:
        q: ${query}
        categories: ${categories}
        format: json
---
# SearXNG 搜索技巧

使用您自己托管的 SearXNG 实例在网络上进行搜索。  
SearXNG 是一款尊重用户隐私的元搜索引擎，它汇集了来自 Google、DuckDuckGo、Brave、Startpage 以及许多其他搜索引擎的结果。

---

## 先决条件

- SearXNG 已在本地或服务器上运行。  
- 快速的 Docker 设置方法：  
  ```bash
mkdir -p ~/Projects/searxng/searxng
cd ~/Projects/searxng

cat > docker-compose.yml << 'EOF'
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080/
    restart: unless-stopped
EOF

cat > searxng/settings.yml << 'EOF'
use_default_settings: true
server:
  secret_key: "change-me-to-random-string"
  bind_address: "127.0.0.1"
  port: 8080
search:
  safe_search: 0
  autocomplete: "google"
  default_lang: "en"
  formats:
    - html
    - json
EOF

docker compose up -d
```  

---

## 配置

设置 SearXNG 的 URL（可选，默认为 http://localhost:8080）：  
```bash
export SEARXNG_URL="http://localhost:8080"
```  

---

## 响应格式

每个搜索结果包含以下信息：  
- `title`：结果标题  
- `url`：结果的链接  
- `content`：结果片段/描述  
- `engines`：返回该结果的搜索引擎  
- `score`：相关性评分  
- `category`：结果所属的类别  

---

## 安全注意事项：  
- 默认绑定地址为 `127.0.0.1`，以防止公开访问。  
- 请用一个强随机值替换默认的 `secret_key`。  
- 请确保 SearXNG 通过 HTTPS 和身份验证机制才能被公开访问。  
- 该技巧仅使用 HTTP 请求，不会执行任何 shell 命令。  

---

## 为什么选择 SearXNG？  
- 首先考虑用户隐私（无跟踪、无广告）  
- 能汇集 70 多个搜索引擎的结果  
- 可以自行托管  
- 支持 JSON API  
- 无需使用 API 密钥或设置请求速率限制