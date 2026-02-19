---
name: curated-search
description: 针对精选技术文档的域限制全文搜索功能
version: 1.0.7
author: qsmtco
license: MIT
homepage: https://github.com/openclaw/curated-search
metadata:
  openclaw:
    requires:
      bins: ["node"]
    emoji: "🔍"
---
# 精选搜索功能（Curated Search Skill）

## 概述  
该功能允许在经过筛选的技术文档白名单（如MDN、Python文档等）上进行领域限制的全文搜索，提供纯净、权威的搜索结果，且不会包含网络垃圾信息。  

## 外部接口  
在搜索过程中，该功能**不会**调用任何外部网络接口。爬虫在构建索引时（一次性设置）可以选择性地发起HTTP请求，但这些请求由用户通过`npm run crawl`命令发起，并且会遵守配置的白名单规则。  

## 安全性与隐私  
- **搜索完全在本地进行**：索引构建完成后，所有查询都在本地执行，不会有任何数据离开用户的机器。  
- **爬取操作是可选的，并且仅针对白名单中的域名**：爬虫仅访问用户在`config.yaml`中明确列出的域名，并尊重`robots.txt`文件中的规则以及可配置的延迟设置。  
- **无数据传输**：不会向外部传输任何使用数据。  
- **配置信息**：从本地的`config.yaml`文件和`data/`目录下的索引文件中读取。  

## 模型调用说明  
`curated-search.search`工具**仅在用户明确请求时**才会被调用**，它不会自动运行。当用户需要搜索精选索引时，OpenClaw会调用该工具的处理程序（`scripts/search.js`）。  

## 信任声明  
使用该功能即表示您信任该工具仅在本地运行，并且只会爬取您允许的域名。该功能不会将您的查询或工作区数据发送给任何第三方。在安装前，请查看其开源实现代码。  

---

## 工具：`curated-search.search`  
用于搜索精选索引。  

### 参数  
| 参数名 | 类型 | 是否必填 | 默认值 | 说明 |  
|------|------|----------|---------|-------------|  
| `query` | 字符串 | 是 | — | 搜索查询词 |  
| `limit` | 数字 | 否 | 5 | 最大搜索结果数量（受`config.max_limit`限制，通常为100条） |  
| `domain` | 字符串 | 否 | `null` | 过滤特定域名（例如：`docs.python.org`） |  
| `min_score` | 数字 | 否 | 最低相关性得分（0.0–1.0）；用于过滤低质量的结果 |  
| `offset` | 数字 | 否 | 分页偏移量（跳过前N条结果） |  

### 返回结果  
返回一个包含结果对象的JSON数组：  

**字段说明：**  
- `title`：文档标题（已清洗处理）  
- `url`：文档的原始URL  
- `snippet`：内容摘录（约200个字符）  
- `domain`：文档所在的域名  
- `score`：BM25相关性得分（得分越高表示相关性越强；范围为0–1）  
- `crawled_at`：页面被爬取时的Unix时间戳  

### 示例调用方式  

### 错误处理  
如果发生错误，工具会以非零状态退出，并在标准错误输出（stderr）中打印错误信息：  

### 常见错误代码及解决方法：  
| 错误代码 | 错误原因 | 建议的解决方法 |  
|------|---------|---------------|  
| `config_missing` | 配置文件未找到 | 指定`--config`参数的路径，或确保`config.yaml`文件存在 |  
| `config_invalid` | YAML格式解析失败 | 检查`config.yaml`的语法是否正确 |  
| `config_missing_index_path` | 未设置索引文件路径 | 在`config.yaml`中添加`index.path`字段 |  
| `index_not_found` | 索引文件缺失 | 运行`npm run crawl`命令重建索引 |  
| `index_corrupted` | 索引文件损坏或格式不正确 | 重新运行`npm run crawl`重建索引 |  
| `index_init_failed` | 索引初始化失败 | 检查权限并重新安装依赖项 |  
| `missing_query` | 未提供查询参数 | 必须提供`--query`参数 |  
| `query_too_long` | 查询字符串超过1000个字符 | 缩短查询内容 |  
| `limit_exceeded` | 请求结果数量超过`config.max_limit` | 调整`limit`值 |  
| `invalid_domain` | 域名过滤规则格式错误 | 使用正确的格式（如`docs.python.org`） |  
| `conflicting_flags` | 同时使用了互斥的参数（例如`--stats`和`--query`） | 正确使用参数 |  
| `stats_failed` | 无法获取索引统计信息 | 确保索引文件可访问 |  
| `search_failed` | 搜索过程中出现错误 | 检查查询内容和索引文件的完整性 |  

## 配置说明  
请编辑技能目录下的`config.yaml`文件。主要配置项包括：  
- `domains`：允许访问的域名列表（必填）  
- `seeds`：爬取的起始URL地址  
- `crawl`：爬取深度、延迟时间、超时设置、最大获取文档数量  
- `content`：内容的最小长度和最大长度  
- `index`：索引文件的路径  
- `search`：默认搜索结果数量、最大结果数量、最低相关性得分阈值  

更多配置详情请参阅`README.md`。  

## 支持资源  
- 完整文档：`README.md`  
- 技术规范：`specs/`  
- 构建指南：`PLAN.md`  
- 贡献者指南：`CONTRIBUTING.md`  
- 问题反馈：请在GitHub上或通过OpenClaw维护者联系我们