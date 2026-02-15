---
name: huggingface-trends
description: **从 Hugging Face 监控并获取热门模型**  
支持按任务、库以及流行度指标进行筛选。适用于用户想要查看热门 AI 模型、比较模型受欢迎程度，或按任务/库探索热门模型的场景。支持导出为 JSON 格式以及格式化输出。
---

# Hugging Face 流行模型

## 快速入门

获取最流行的模型：

```bash
scripts/hf_trends.py -n 10 -p http://172.28.96.1:10808
```

## 核心功能

### 获取流行模型

基本用法：

```bash
# Get top 10 trending models
scripts/hf_trends.py -n 10 -p http://172.28.96.1:10808

# Get top 5 most liked models
scripts/hf_trends.py -n 5 -s likes -p http://172.28.96.1:10808

# Get most downloaded models
scripts/hf_trends.py -n 10 -s downloads -p http://172.28.96.1:10808
```

### 按任务筛选模型

根据特定的 AI 任务筛选模型：

```bash
# Text generation models
scripts/hf_trends.py -n 10 -t text-generation -p http://172.28.96.1:10808

# Image classification models
scripts/hf_trends.py -n 10 -t image-classification -p http://172.28.96.1:10808

# Translation models
scripts/hf_trends.py -n 10 -t translation -p http://172.28.96.1:10808
```

常见任务筛选选项：
- `text-generation` - 大语言模型
- `image-classification` - 视觉模型
- `image-to-text` - 多模态模型
- `translation` - 机器翻译
- `summarization` - 文本摘要
- `question-answering` - 问答模型

### 按库筛选模型

根据机器学习框架筛选模型：

```bash
# PyTorch models only
scripts/hf_trends.py -n 10 -l pytorch -p http://172.28.96.1:10808

# TensorFlow models only
scripts/hf_trends.py -n 10 -l tensorflow -p http://172.28.96.1:10808

# JAX models
scripts/hf_trends.py -n 10 -l jax -p http://172.28.96.1:10808
```

### 导出到 JSON

将结果保存以供进一步分析：

```bash
# Export to JSON file
scripts/hf_trends.py -n 10 -j trending_models.json -p http://172.28.96.1:10808

# Export with specific filters
scripts/hf_trends.py -n 20 -t text-generation -j text_models.json -p http://172.28.96.1:10808
```

### 代理配置

该脚本需要一个 HTTP 代理来访问 Hugging Face API（因网络限制）。

使用 `-p` 标志：

```bash
scripts/hf_trends.py -p http://172.28.96.1:10808
```

对于大多数使用 v2rayN 的 WSL2 环境：
- 代理 URL：`http://172.28.96.1:10808`
- 或使用动态 IP：`http://$(ip route show | grep default | awk '{print $3}'):10808`

## 命令行选项

| 标志 | 长格式 | 描述 | 默认值 |
|------|-----------|-------------|---------|
| `-n` | `--limit` | 获取的模型数量 | 10 |
| `-s` | `--sort` | 排序方式：按流行度、点赞数、下载次数、创建时间 | 按流行度排序 |
| `-t` | `--task` | 按任务/流程筛选 | 无 |
| `-l` | `--library` | 按库筛选（pytorch、tensorflow、jax） | 无 |
| `-j` | `--json` | 将结果导出到 JSON 文件 | 无 |
| `-p` | `--proxy` | HTTP 请求的代理 URL | 无 |

## 输出格式

脚本以结构化格式显示模型信息：

```
🤖 Hugging Face 热门模型 (5 个)
============================================================
1. moonshotai/Kimi-K2.5
   ⭐ 2.0K likes   📥 647.6K downloads
   📊 Task: image-text-to-text   📚 Library: transformers
   📅 Created: 2026-01-01   Updated: N/A
...
```

### 模型信息

每个模型条目包括：
- **模型 ID**：完整的 Hugging Face 模型名称
- **点赞数**：模型的受欢迎程度（指标）
- **下载次数**：总下载量
- **任务**：主要任务/流程（例如：文本生成）
- **库**：使用的机器学习框架（transformers、pytorch、tensorflow）
- **创建/更新时间**：模型的创建或更新日期

## 使用场景

### 日常监控

每天检查流行模型，了解新发布的模型：

```bash
# Create cron job for daily monitoring
0 9 * * * cd /home/ltx/.openclaw/workspace && \
  /home/ltx/.openclaw/workspace/skills/huggingface-trends/scripts/hf_trends.py \
  -n 20 -p http://172.28.96.1:10808 >> /tmp/hf-trends.log 2>&1
```

### 任务特定研究

探索特定 AI 任务的流行模型：

```bash
# Research trending text generation models
scripts/hf_trends.py -n 15 -t text-generation -s likes -p http://172.28.96.1:10808

# Find popular image-to-text models
scripts/hf_trends.py -n 15 -t image-to-text -s downloads -p http://172.28.96.1:10808
```

### 框架特定分析

按机器学习框架比较模型：

```bash
# Compare PyTorch vs TensorFlow popularity
scripts/hf_trends.py -n 20 -l pytorch -j pytorch_models.json -p http://172.28.96.1:10808
scripts/hf_trends.py -n 20 -l tensorflow -j tensorflow_models.json -p http://172.28.96.1:10808
```

## 与 OpenClaw 的集成

在 OpenClaw 会话中使用该脚本：

```python
# Fetch trending models programmatically
from skills.huggingface-trends.scripts import hf_trends

fetcher = hf_trends.HuggingFaceTrends(proxy="http://172.28.96.1:10808")
models = fetcher.fetch_trending_models(limit=10)

# Format for display
output = fetcher.format_models(models)
print(output)
```

## 故障排除

### 网络错误

**问题**：“网络无法到达”或连接错误

**解决方案**：确保使用 `-p` 标志指定代理：
```bash
scripts/hf_trends.py -p http://172.28.96.1:10808
```

检查 Windows 上是否正在运行 v2rayN 代理。

### 结果为空

**问题**：“未找到模型”

**解决方案**：尝试不同的筛选条件或增加获取数量：
```bash
scripts/hf_trends.py -n 50 -p http://172.28.96.1:10808
```

### 依赖项缺失

**问题**：“requests 包未安装”

**解决方案**：安装所需的依赖项：
```bash
pip install requests
```

## 技术说明

- **API 限制**：Hugging Face 的公共 API 没有提供专门的流行模型查询端点，因此脚本会获取最近的模型并按受欢迎程度进行排序。
- **代理要求**：由于网络限制，所有请求都必须通过代理进行。脚本支持 HTTP 代理配置。
- **速率限制**：公共 API 有速率限制，请避免连续发送过多请求。
- **数据更新**：模型数据来自 Hugging Face API，最新更改可能需要一段时间才能反映在结果中。

## 参考资料

有关模型元数据和可用筛选条件的更多详细信息，请参阅 [Hugging Face API 文档](https://huggingface.co/docs/huggingface_hub/guides/models)。