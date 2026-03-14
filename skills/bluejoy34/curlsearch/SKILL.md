---
name: curl-search
description: "使用 `curl` 和多个搜索引擎（百度、谷歌、必应、DuckDuckGo）进行网页搜索。当用户请求搜索、查找或查询在线信息时，该功能会被激活。该系统具备安全增强措施，包括输入内容清洗、命令注入防护以及 URL 编码功能。"
metadata:
  requirements:
    binaries:
      - curl
      - python3
    os:
      - linux
      - darwin
      - win32
  security:
    input_sanitization: true
    command_injection_protection: true
    url_encoding: true
  version: "2.0.0"
  author: "bluejoy34"
  license: "MIT"
---
# Curl搜索技巧

使用`curl`结合多个搜索引擎进行网络搜索。当专用的搜索API不可用时，这是一个轻量级的替代方案。

## 支持的搜索引擎

| 支持的搜索引擎 | 别名 | 说明 |
|------------|---------|-------------------|
| Baidu       | bd       | 适用于中国，默认选项 |
| Google      | g       | 在中国需要使用代理/VPN |
| Bing        | b       | 微软Bing搜索引擎 |
| DuckDuckGo    | ddg      | 注重用户隐私的搜索引擎 |

## 使用示例

```
Search for OpenClaw tutorial
Google search AI development
Find Python tutorials with bing
```

## 所需软件

- **curl**：命令行HTTP客户端
- **python3**：用于URL编码

## 安全特性

本技巧包含以下安全增强功能：

### 1. 输入清洗
移除可能被利用的危险shell元字符：
```bash
sanitize_input() {
    local input="$1"
    echo "$input" | sed 's/[^a-zA-Z0-9 \_\-\.\~\x{4e00}-\x{9fff}]//g'
}
```

### 2. 命令注入防护
- 验证用户选择的搜索引擎
- 将搜索结果数量限制在1-50条以内
- 在清洗输入后检查输入是否为空

### 3. URL编码
使用Python的`urllib.parse`模块，并设置`safe=''`参数来正确编码特殊字符。

## 安装方法

```bash
# Install via ClawHub
clawhub install curl-search

# Or manually
cd your-skills-dir
tar -xzf curl-search.tar.gz
```

## 配置方法

- 设置默认搜索引擎：
```bash
export SEARCH_ENGINE=google
```

- 设置搜索结果的最大数量：
```bash
export MAX_RESULTS=5
```

## 限制事项

- 搜索结果来自公共搜索引擎
- 可能会被反爬虫机制阻止
- 在中国使用Google需要代理/VPN

## 版本历史

- **2.0.0**：添加了安全增强功能
  - 输入清洗
  - 命令注入防护
  - URL编码改进
- **1.0.0**：初始版本