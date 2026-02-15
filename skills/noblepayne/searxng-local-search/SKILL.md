---
name: searxng-web-search
description: 使用 SearXNG 在网络上进行搜索。当您需要获取最新信息、研究某个主题、查找文档、验证事实，或查询超出您知识范围的内容时，可以使用它。该工具会返回带有标题、URL 和内容片段的排名结果。
metadata:
  openclaw:
    requires:
      bins: ["bb"]
      env: ["SEARXNG_URL"]
    emoji: "🔍"
    nix:
      plugin: "babashka"
---

# SearXNG 网页搜索

使用自托管的 SearXNG 实例进行网页搜索。该功能通过 SearXNG 的 JSON API 提供网页搜索结果，同时具备内置的速率限制、错误处理和结果格式化功能。

## 使用场景

当您需要以下操作时，可以使用此功能：
- 查找当前信息或最新新闻
- 研究超出您知识范围的主题
- 查阅文档或技术参考资料
- 验证事实或检查当前状态
- 查找特定主题的 URL 或资源
- 搜索代码示例或解决方案

## 配置

将 `SEARXNG_URL` 环境变量设置为您的 SearXNG 实例地址：

```bash
export SEARXNG_URL="http://localhost:8888"
```

如果未设置，则使用默认地址（http://localhost:8888）。

## 使用方法

使用以下命令执行搜索：

```bash
bb scripts/search.clj "your search query"
```

### 高级选项

可以通过 JSON 传递额外参数：

```bash
bb scripts/search.clj "your query" '{"category": "news", "time_range": "day", "num_results": 10}'
```

可用参数：
- `category` - 按类别过滤：general（综合）、news（新闻）、images（图片）、videos（视频）、it（技术）、science（科学）
- `time_range` - 时间范围：day（当天）、week（一周）、month（一个月）、year（一年）
- `language` - 语言代码（默认：en）
- `num_results` - 返回的结果数量（默认：5）

## 输出格式

脚本以文本形式返回格式化后的搜索结果：

```
Search Results for "your query"
Found 42 total results

1. Result Title [Score: 1.85]
   URL: https://example.com/page
   Description snippet from the page...
   Engines: google, bing

2. Another Result [Score: 1.62]
   ...
```

## 错误处理

脚本能够优雅地处理以下常见错误：
- 网络超时（超时时间为 30 秒）
- SearXNG 无法使用（显示清晰错误信息）
- 无效查询（显示错误详情）
- 速率限制（返回 429 错误代码）
- 没有结果（显示提示信息）

## 速率限制

脚本实现了基本的速率限制机制：
- 请求之间至少间隔 1 秒
- 使用文件系统来记录请求状态（文件名：`.searxng-last-request`）
- 防止恶意刷取行为

## 示例

### 基本搜索
```bash
bb scripts/search.clj "NixOS configuration"
```

### 新闻搜索
```bash
bb scripts/search.clj "AI developments" '{"category": "news", "time_range": "week"}'
```

### 技术搜索
```bash
bb scripts/search.clj "babashka http client" '{"category": "it", "num_results": 3}'
```

### 仅显示最新结果
```bash
bb scripts/search.clj "product launch" '{"time_range": "day"}'
```

## 故障排除

**“SEARXNG_URL 未设置”**
- 设置环境变量：`export SEARXNG_URL="http://localhost:8888"`

**连接超时**
- 检查 SearXNG 是否正在运行：`curl $SEARXNG_URL/search?q=test&format=json`
- 检查防火墙设置
- 查看服务状态：`systemctl status searx`

**没有结果**
- 尝试使用更宽泛的查询条件
- 移除过滤条件后重新尝试
- 查看 SearXNG 日志：`journalctl -u searx -n 50`

**速率限制错误**
- 在每次搜索之间等待几秒钟
- 脚本会自动确保至少间隔 1 秒

## 实现说明

搜索脚本（`scripts/search.clj`）使用了以下工具：
- `babashka.http-client` 用于发送 HTTP 请求
- Clojure 的 `cheshire.core` 用于解析 JSON 数据
- 基于文件系统的速率限制机制
- 30 秒的超时设置，并附带相应的错误提示信息
- 对搜索结果进行评分和排序，优先显示最佳结果

有关详细的 API 文档，请参阅 `references/api-guide.md`。