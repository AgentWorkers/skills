---
name: mux
description: "**Mux Video**：通过 REST API 管理资产、直播流、播放 ID 以及分析数据"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["MUX_TOKEN_ID", "MUX_TOKEN_SECRET"]}, "primaryEnv": "MUX_TOKEN_ID", "homepage": "https://www.agxntsix.ai"}}
---
# 🎬 Mux

Mux 是一个用于管理视频资源、直播流、播放ID以及相关分析数据的工具，它通过 REST API 提供相应的接口。

## 必需参数

| 参数 | 是否必需 | 说明 |
|--------|---------|-----------|
| `MUX_TOKEN_ID` | ✅ | API 令牌 ID |
| `MUX_TOKEN_SECRET` | ✅ | API 令牌密钥 |

## 快速入门

```bash
# List assets
python3 {{baseDir}}/scripts/mux.py assets --limit <value>

# Get asset
python3 {{baseDir}}/scripts/mux.py asset-get id <value>

# Create asset
python3 {{baseDir}}/scripts/mux.py asset-create --url <value> --playback_policy <value>

# Delete asset
python3 {{baseDir}}/scripts/mux.py asset-delete id <value>

# Get input info
python3 {{baseDir}}/scripts/mux.py asset-input-info id <value>

# List playback IDs
python3 {{baseDir}}/scripts/mux.py asset-playback-ids id <value>

# List live streams
python3 {{baseDir}}/scripts/mux.py live-streams

# Get live stream
python3 {{baseDir}}/scripts/mux.py live-stream-get id <value>
```

## 所有命令

| 命令 | 说明 |
|--------|-----------|
| `assets` | 列出所有资源 |
| `asset-get` | 获取特定资源信息 |
| `asset-create` | 创建新资源 |
| `asset-delete` | 删除资源 |
| `asset-input-info` | 获取资源输入信息 |
| `asset-playback-ids` | 列出所有播放ID |
| `live-streams` | 列出所有直播流 |
| `live-stream-get` | 获取特定直播流信息 |
| `live-stream-create` | 创建新的直播流 |
| `live-stream-delete` | 删除直播流 |
| `live-stream-reset-key` | 重置直播流密钥 |
| `uploads` | 列出所有上传文件 |
| `upload-create` | 创建新的上传任务 |
| `views` | 获取视频观看次数 |
| `metrics` | 获取统计数据 |
| `monitoring` | 监控相关指标 |

## 输出格式

所有命令默认以 JSON 格式输出。若需要可读性更强的输出格式，可添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/mux.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-----------|
| `{{baseDir}}/scripts/mux.py` | 主要的命令行工具（包含所有命令） |

## 致谢

Mux 由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关内容也发布在 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi) 上。  
Mux 是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)