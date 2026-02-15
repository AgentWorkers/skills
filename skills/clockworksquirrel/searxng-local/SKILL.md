---
name: searxng
description: 使用自托管的 SearXNG 实例在网络上进行搜索。SearXNG 是一款尊重用户隐私的元搜索引擎，能够汇总来自多个搜索引擎的结果。
metadata:
  clawdbot:
    config:
      optionalEnv:
        - SEARXNG_URL
---

# SearXNG 搜索工具

使用您自托管的 SearXNG 实例来搜索网页。这是一个注重隐私的元搜索引擎，能够整合来自 Google、DuckDuckGo、Brave、Startpage 以及 70 多个其他搜索引擎的结果。

## 先决条件

SearXNG 需要在本地或服务器上运行。快速搭建 Docker 环境的方法如下：
```bash
mkdir -p ~/Projects/searxng/searxng
cd ~/Projects/searxng

# Create docker-compose.yml
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

# Create settings.yml with JSON API enabled
cat > searxng/settings.yml << 'EOF'
use_default_settings: true
server:
  secret_key: "change-me-to-random-string"
  bind_address: "0.0.0.0"
  port: 8080
search:
  safe_search: 0
  autocomplete: "google"
  default_lang: "en"
  formats:
    - html
    - json
EOF

# Start SearXNG
docker compose up -d
```

## 配置

设置 SearXNG 的 URL（默认为 http://localhost:8080）：
```bash
export SEARXNG_URL="http://localhost:8080"
```

## 使用示例

### 基本搜索
```bash
curl "http://localhost:8080/search?q=your+query&format=json" | jq '.results[:5]'
```

### 按类别搜索
```bash
# General web search
curl "http://localhost:8080/search?q=query&categories=general&format=json"

# Images
curl "http://localhost:8080/search?q=query&categories=images&format=json"

# News
curl "http://localhost:8080/search?q=query&categories=news&format=json"

# Videos
curl "http://localhost:8080/search?q=query&categories=videos&format=json"

# IT/Tech documentation
curl "http://localhost:8080/search?q=query&categories=it&format=json"

# Science/Academic
curl "http://localhost:8080/search?q=query&categories=science&format=json"
```

### 按语言/地区搜索
```bash
curl "http://localhost:8080/search?q=query&language=en-US&format=json"
curl "http://localhost:8080/search?q=query&language=de-DE&format=json"
```

### 分页显示结果
```bash
# Page 2 (results 11-20)
curl "http://localhost:8080/search?q=query&pageno=2&format=json"
```

## 结果格式

每个搜索结果包含以下信息：
- `title`：结果标题
- `url`：结果链接
- `content`：结果片段/描述
- `engines`：返回该结果的搜索引擎列表
- `score`：相关性评分（分数越高，相关性越强）
- `category`：结果所属的类别

## Shell 函数

将以下代码添加到您的 `.zshrc` 或 `.bashrc` 文件中：
```bash
searxng() {
  local query="$*"
  local url="${SEARXNG_URL:-http://localhost:8080}"
  curl -s "${url}/search?q=$(echo "$query" | sed 's/ /+/g')&format=json" | \
    jq -r '.results[:10][] | "[\(.score | floor)] \(.title)\n    \(.url)\n    \(.content // "No description")\n"'
}
```

使用方法：`searxng how to make sourdough bread`

## Docker 管理

```bash
# Start
cd ~/Projects/searxng && docker compose up -d

# Stop
docker compose down

# View logs
docker compose logs -f searxng

# Restart
docker compose restart
```

## 故障排除

**容器无法启动：**
检查日志以确定问题原因。

**JSON 格式无法正常使用：**
确保您的 `settings.yml` 文件中配置了 `formats: [html, json]`。

**没有找到结果：**
可能是某些搜索引擎设置了访问限制。请查看日志以获取错误信息。

## 为什么选择 SearXNG？

- **隐私保护**：不进行用户跟踪，无广告，不收集用户数据。
- **结果整合**：汇集来自 70 多个搜索引擎的结果。
- **自托管**：所有数据都保存在您的设备上。
- **API 支持**：提供 JSON 格式的输出，便于自动化操作。
- **免费**：无需购买 API 密钥，也没有访问限制。