---
name: web-search
description: 此技能适用于用户需要在网上搜索信息、查找当前内容、查阅新闻文章、搜索图片或查找视频的情况。它使用基于 DuckDuckGo (DDGS) 的命令行工具（CLI）来返回格式清晰的结果，这些结果可以以纯文本或 JSON 的形式呈现。
---

# Web 搜索（duckse）

## 概述

使用 `duckse` 可以基于 DDGS（Distributed Data Gathering System）进行网页元搜索。该技能支持以下类型的数据搜索：
- 文本（`text`）
- 新闻（`news`）
- 图片（`images`）
- 视频（`videos`）
- 书籍（`books`）

同时提供以下功能：
- 时间过滤、地区过滤、安全搜索（`safe search`）以及后端选择
- 可以选择简洁的输出格式（默认）或 JSON 格式（`--json`）
- 通过重定向获取最终 URL（`--expand-url`）

## 何时使用此技能

当用户需要执行以下操作时，可以使用此技能：
- 进行通用网页搜索
- 查找最新新闻或特定主题
- 搜索图片或视频
- 根据提供的 URL 进行快速信息检索
- 基于网页结果进行事实核查

## 先决条件

请确保 `duckse` 已经安装：

```bash
duckse --help
```

如果尚未安装，请执行以下操作进行安装：

```bash
curl -sSL https://raw.githubusercontent.com/dwirx/duckse/main/scripts/install.sh | bash
```

## 核心命令

### 1. 基本网页搜索

```bash
duckse "<query>"
```

示例：

```bash
duckse "python asyncio tutorial"
```

### 2. 限制搜索结果数量

```bash
duckse "<query>" --max-results <N>
```

示例：

```bash
duckse "machine learning frameworks" --max-results 20
```

### 3. 时间过滤

```bash
duckse "<query>" --timelimit <d|w|m|y>
```

示例：

```bash
duckse "artificial intelligence news" --type news --timelimit w
```

### 4. 新闻搜索

```bash
duckse "<query>" --type news
```

示例：

```bash
duckse "climate change" --type news --timelimit w --max-results 15
```

### 5. 图片搜索

```bash
duckse "<query>" --type images
```

示例：

```bash
duckse "sunset over mountains" --type images --max-results 20
```

图片过滤示例：

```bash
duckse "landscape photos" --type images --size Large
duckse "abstract art" --type images --color Blue
duckse "icons" --type images --type-image transparent
duckse "wallpapers" --type images --layout Wide
```

### 6. 视频搜索

```bash
duckse "<query>" --type videos
```

示例：

```bash
duckse "python tutorial" --type videos --max-results 15
```

视频过滤示例：

```bash
duckse "cooking recipes" --type videos --duration short
duckse "documentary" --type videos --resolution high
```

### 7. 书籍搜索

```bash
duckse "<query>" --type books --backend annasarchive
```

示例：

```bash
duckse "sea wolf jack london" --type books --max-results 10
```

### 8. 地区过滤与安全搜索

```bash
duckse "<query>" --region us-en --safesearch moderate
```

示例：

```bash
duckse "local news" --type news --region us-en --safesearch on
```

### 9. JSON 输出与最终 URL

- JSON 输出示例：

```bash
duckse "quantum computing" --json
```

- 最终 URL 解析示例：

```bash
duckse "beritakan di indonesia hari ini" --expand-url --max-results 5
```

## 支持的后端类型

- 文本：`bing, brave, duckduckgo, google, grokipedia, mojeek, yandex, yahoo, wikipedia, auto`
- 图片：`duckduckgo, auto`
- 视频：`duckduckgo, auto`
- 新闻：`bing, duckduckgo, yahoo, auto`
- 书籍：`annasarchive, auto`

## 常见使用场景

- **研究主题**：用于查找相关资料
- **当前事件监控**：实时获取新闻或事件信息
- **事实核查**：验证网页内容

## 快速参考

命令格式：

```bash
duckse "<query>" [options]
```

常用选项：
- `--type` （`text` | `images` | `videos` | `news` | `books`）
- `--max-results`：限制搜索结果数量
- `--timelimit` （`d` | `w` | `m` | `y`）：指定时间范围（天/周/月/年）
- `--region`：指定搜索地区
- `--safesearch` （`on` | `moderate` | `off`）：启用/禁用安全搜索
- `--backend`：选择搜索后端
- `--json`：输出 JSON 格式
- `--expand-url`：获取包含链接的完整 URL
- `--proxy`：设置代理服务器
- `--timeout`：设置请求超时时间
- `--verify`：验证搜索结果

## 最佳实践

- 使用具体的查询关键词
- 使用 `--timelimit` 获取最新信息
- 如需完整 URL，使用 `--expand-url`
- 为自动化流程选择 `--json` 格式
- 根据需求调整 `--max-results`（建议设置为 10-20）

## 常见问题解决方法

- **命令未找到**：添加 `PATH` 环境变量：`export PATH="$HOME/.local/bin:$PATH"`
- 后端无效：请检查后端列表是否正确
- 搜索结果为空：检查查询语句或时间过滤条件
- 请求超时/网络问题：尝试重新搜索，或增加 `--timeout` 参数，或使用代理服务器
- 在本地开发时（未全局安装二进制文件）：参考 **开发回退方案**（参见 **Code Block 26**）

```bash
uv run python main.py "<query>" [opsi yang sama]
```