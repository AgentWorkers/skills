---
name: segment
description: "**Segment**：通过配置（Config）和跟踪（Tracking）API来管理源文件、目标文件、事件以及跟踪计划。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "📊", "requires": {"env": ["SEGMENT_ACCESS_TOKEN", "SEGMENT_WRITE_KEY"]}, "primaryEnv": "SEGMENT_ACCESS_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---
# 📊 分段管理

**Segment** — 通过配置（Config）和跟踪（Tracking）API来管理来源（sources）、目标（destinations）、事件（events）以及跟踪计划（tracking plans）。

## 所需参数

| 参数 | 是否必填 | 说明 |
|----------|----------|-------------|
| `SEGMENT_ACCESS_TOKEN` | ✅ | 配置API令牌 |
| `SEGMENT_WRITE_KEY` | ✅ | 源写入密钥（source write key） |

## 快速入门

```bash
# List sources
python3 {{baseDir}}/scripts/segment.py sources

# Get source
python3 {{baseDir}}/scripts/segment.py source-get id <value>

# Create source
python3 {{baseDir}}/scripts/segment.py source-create --name <value> --catalog_name <value>

# Delete source
python3 {{baseDir}}/scripts/segment.py source-delete id <value>

# List destinations
python3 {{baseDir}}/scripts/segment.py destinations

# Get destination
python3 {{baseDir}}/scripts/segment.py destination-get id <value>

# List warehouses
python3 {{baseDir}}/scripts/segment.py warehouses

# List source catalog
python3 {{baseDir}}/scripts/segment.py catalog-sources
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `sources` | 列出所有来源 |
| `source-get` | 获取特定来源信息 |
| `source-create` | 创建新的来源 |
| `source-delete` | 删除来源 |
| `destinations` | 列出所有目标 |
| `destination-get` | 获取特定目标信息 |
| `warehouses` | 列出所有仓库 |
| `catalog-sources` | 列出来源目录 |
| `catalog-destinations` | 列出目标目录 |
| `tracking-plans` | 列出所有跟踪计划 |
| `tracking-plan-get` | 获取特定跟踪计划信息 |
| `spaces` | 列出所有空间（spaces） |
| `functions` | 列出所有功能（functions） |
| `track` | 发送跟踪事件 |
| `identify` | 发送识别请求 |

## 输出格式

所有命令默认以JSON格式输出。若需可读的格式化输出，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/segment.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/segment.py` | 主要命令行工具（CLI），包含所有命令 |

## 致谢

本工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)