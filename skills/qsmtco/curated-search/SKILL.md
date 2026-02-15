# 精选搜索功能

## 概述
该功能支持在经过筛选的文档白名单（如MDN、Python文档等）上进行领域限定的全文搜索，提供纯净、权威的搜索结果，同时过滤掉网页垃圾内容。

## 工具：curated-search.search

用于搜索这些精选的文档。

### 参数

| 名称 | 类型 | 是否必填 | 默认值 | 说明 |
|------|------|---------|---------|-------------|
| `query` | 字符串 | 是 | — | 搜索查询词 |
| `limit` | 数字 | 否 | 5 | 最大返回结果数量（受`config.max_limit`限制，通常为100条） |
| `domain` | 字符串 | 否 | `null` | 过滤特定域名（例如：`docs.python.org`） |
| `min_score` | 数字 | 否 | 最小相关性得分（0.0–1.0）；用于过滤质量较低的匹配结果 |
| `offset` | 数字 | 否 | 0 | 分页偏移量（跳过前N条结果） |

### 返回结果

返回一个包含结果对象的JSON数组：

```json
[
  {
    "title": "Python Tutorial",
    "url": "https://docs.python.org/3/tutorial/",
    "snippet": "Python is an easy to learn, powerful programming language...",
    "domain": "docs.python.org",
    "score": 0.87,
    "crawled_at": 1707712345678
  }
]
```

**字段说明：**
- `title` — 文档标题（已清洗）
- `url` — 文档的原始URL（标准格式）
- `snippet` — 文档内容的摘录（约200个字符）
- `domain` — 文档来源的域名
- `score` — BM25相关性得分（得分越高表示相关性越强；范围为0–1）
- `crawled_at` — 页面被爬取的Unix时间戳

### 示例代理调用

```
search CuratedSearch for "python tutorial"
search CuratedSearch for "async await" limit=3 domain=developer.mozilla.org
search CuratedSearch for "linux man page" min_score=0.3
```

### 错误处理

如果发生错误，工具将以非零状态退出，并在标准错误输出（stderr）中打印错误信息：

```json
{
  "error": "index_not_found",
  "message": "Search index not found. The index has not been built yet.",
  "suggestion": "Run the crawler first: npm run crawl",
  "details": { "path": "data/index.json" }
}
```

**常见错误代码：**

| 代码 | 含义 | 建议的解决方法 |
|------|---------|---------------|
| `config_missing` | 配置文件未找到 | 指定`--config`参数的路径，或确保`config.yaml`文件存在 |
| `config_invalid` | YAML解析失败 | 检查`config.yaml`的语法 |
| `config_missing_index_path` | 未设置索引文件路径 | 在配置文件中添加`index.path` |
| `index_not_found` | 索引文件缺失 | 运行`npm run crawl`命令重建索引 |
| `index_corrupted` | 索引文件损坏或不兼容 | 重新运行`npm run crawl`重建索引 |
| `index_init_failed` | 索引初始化失败 | 检查权限并重新安装依赖项 |
| `missing_query` | 未提供查询参数 | 必须提供`--query`参数 |
| `query_too_long` | 查询长度超过1000个字符 | 缩短查询内容 |
| `limit_exceeded` | 请求的返回结果数量超过`config.max_limit` | 减少请求结果数量 |
| `invalid_domain` | 域名过滤格式错误 | 使用正确的格式（如`docs.python.org`） |
| `conflicting_flags` | 同时使用了互斥的参数（例如`--stats`和`--query`） | 正确使用参数 |
| `stats_failed` | 无法获取索引统计信息 | 确保索引文件可访问 |
| `search_failed` | 搜索过程中出现错误 | 检查查询内容和索引的完整性 |

## 配置

请在技能目录下编辑`config.yaml`文件。主要配置项包括：

- `domains` — 允许的域名列表（必填）
- `seeds` — 爬取的起始URL
- `crawl` — 爬取深度、延迟、超时时间、最大文档数量
- `content` — 文档内容的最小长度和最大长度
- `index` — 索引文件的路径
- `search` — 默认返回结果数量、最大返回结果数量、最小相关性得分

详细配置说明请参阅`README.md`。

## 支持文档

- 完整的文档说明：`README.md`
- 技术规格：`specs/`
- 构建指南：`PLAN.md`
- 贡献者指南：`CONTRIBUTING.md`
- 问题报告：请在GitHub上提交问题（或联系OpenClaw维护者）