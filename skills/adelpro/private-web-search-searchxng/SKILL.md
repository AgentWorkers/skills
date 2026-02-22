---
name: private-web-search-searchxng
description: 使用 SearXNG 自主托管私有网络搜索引擎。适用于需要保护隐私、外部 API 被屏蔽、希望进行无追踪搜索或避免使用付费搜索 API 的场景。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["docker", "curl", "jq"] },
        "install":
          [
            {
              "id": "docker",
              "kind": "bin",
              "command": "docker --version",
              "label": "Docker required",
            },
          ],
      },
  }
---
# Private Web Search (SearXNG)

这是一个尊重用户隐私的、可自托管的元搜索引擎，专为AI代理设计。

## 快速部署

```bash
# 1. Start container
docker run -d --name searxng -p 8080:8080 -e BASE_URL=http://localhost:8080/ searxng/searxng

# 2. Enable JSON API
docker exec searxng sed -i 's/  formats:/  formats:\n    - json/' /etc/searxng/settings.yml
docker restart searxng

# 3. Verify
curl -sL "http://localhost:8080/search?q=test&format=json" | jq '.results[0]'
```

## 使用方法

### 基本搜索

```bash
curl -sL "http://localhost:8080/search?q=YOUR_QUERY&format=json" | jq '.results[:10]'
```

### 使用辅助脚本

```bash
./scripts/search.sh "openclaw ai" 5
```

### 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| SEARXNG_PORT | 8080 | 容器端口 |
| SEARXNG_HOST | localhost | 服务器主机 |
| BASE_URL | http://localhost:8080 | 公共访问地址 |

## 支持的搜索引擎

Google、Bing、DuckDuckGo、Brave、Startpage、Wikipedia等。

## 管理

```bash
docker start searxng   # Start
docker stop searxng    # Stop
docker logs searxng    # View logs
docker rm searxng -f   # Remove
```

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 无搜索结果 | 查看 `docker logs searxng` 日志 |
| 403 禁止访问 | 启用 JSON 格式（步骤 2） |
| 连接失败 | 运行 `docker start searxng` 命令启动服务 |