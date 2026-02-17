---
name: curated-search
description: 针对精选的技术文档，提供基于域名限制的全文搜索功能。
metadata:
  openclaw:
    requires:
      bins: ["node"]
---
# 精选搜索功能

## 概述  
该功能支持在预先筛选好的技术文档白名单（如MDN、Python文档等）中进行领域限制的全文搜索，提供纯净、权威的搜索结果，同时过滤掉网络垃圾内容。

## 工具：curated-search.search  
用于搜索这些精选的文档。

### 参数  
| 名称 | 类型 | 是否必填 | 默认值 | 说明 |  
|------|------|---------|---------|-------------|  
| `query` | 字符串 | 是 | — | 搜索查询词 |  
| `limit` | 数字 | 否 | 5 | 最大返回结果数量（受`config.max_limit`限制，通常为100条） |  
| `domain` | 字符串 | 否 | `null` | 过滤特定域名（例如：`docs.python.org`） |  
| `min_score` | 数字 | 否 | 最低相关性得分（0.0–1.0）；用于过滤低质量结果 |  
| `offset` | 数字 | 否 | 0 | 分页偏移量（跳过前N条结果） |  

### 返回结果  
返回一个包含结果对象的JSON数组：  

**字段说明：**  
- `title`：文档标题（已清洗处理）  
- `url`：文档的原始URL  
- `snippet`：文档内容的摘录（约200个字符）  
- `domain`：文档的域名  
- `score`：基于BM25算法计算的相关性得分（得分越高越好；范围为0–1）  
- `crawled_at`：页面被爬取的Unix时间戳  

### 示例代理调用  

### 错误处理  
如果发生错误，工具将以非零状态退出，并将错误信息以JSON格式输出到标准错误流（stderr）：  

### 常见错误代码及解决方法：  
| 代码 | 错误原因 | 建议解决方法 |  
|------|---------|---------------|  
| `config_missing` | 配置文件未找到 | 指定`--config`参数或确保`config.yaml`文件存在 |  
| `config_invalid` | YAML格式解析失败 | 检查`config.yaml`的语法是否正确 |  
| `config_missing_index_path` | 未设置索引文件路径 | 在配置文件中添加`index.path`字段 |  
| `index_not_found` | 索引文件缺失 | 运行`npm run crawl`命令重建索引 |  
| `index_corrupted` | 索引文件损坏或格式不正确 | 重新运行`npm run crawl`重建索引 |  
| `index_init_failed` | 索引初始化失败 | 检查权限并重新安装依赖项 |  
| `missing_query` | 未提供查询参数 | 必须提供`--query`参数 |  
| `query_too_long` | 查询字符串超过1000个字符 | 缩短查询内容 |  
| `limit_exceeded` | 请求的结果数量超过配置限制 | 调整`limit`参数 |  
| `invalid_domain` | 域名格式错误 | 使用正确的域名格式（如`docs.python.org`） |  
| `conflicting_flags` | 同时使用了相互冲突的参数（例如`--stats`和`--query`） | 正确使用参数 |  
| `stats_failed` | 无法获取索引统计信息 | 确保索引文件可访问 |  
| `search_failed` | 搜索过程中出现错误 | 检查查询内容和索引文件的完整性 |  

## 配置方式  
请编辑技能目录下的`config.yaml`文件。主要配置项包括：  
- `domains`：允许搜索的域名列表（必填）  
- `seeds`：用于爬取的起始URL地址  
- `crawl`：爬取深度、延迟、超时时间、最大抓取文档数量  
- `content`：内容的最小长度和最大长度  
- `index`：索引文件的路径  
- `search`：默认返回结果数量、最大返回结果数量、最低相关性得分  

详细配置说明请参阅`README.md`文件。  

## 帮助资源  
- 完整文档：`README.md`  
- 技术规格：`specs/`  
- 构建指南：`PLAN.md`  
- 贡献者指南：`CONTRIBUTING.md`  
- 问题反馈：请在GitHub上提交问题（或联系OpenClaw维护者）