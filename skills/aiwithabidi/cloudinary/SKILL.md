---
name: cloudinary
description: "Cloudinary — 通过 REST API 管理图片/视频，支持上传、转换和搜索资源。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "☁️", "requires": {"env": ["CLOUDINARY_API_KEY", "CLOUDINARY_API_SECRET", "CLOUDINARY_CLOUD_NAME"]}, "primaryEnv": "CLOUDINARY_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# ☁️ Cloudinary

Cloudinary 是一个用于管理图片/视频的工具，支持通过 REST API 进行上传、转换和搜索资源。

## 必需配置项

| 变量 | 是否必填 | 说明 |
|----------|----------|-------------|
| `CLOUDINARY_API_KEY` | ✅ | API 密钥 |
| `CLOUDINARY_API_SECRET` | ✅ | API 密码 |
| `CLOUDINARY_CLOUD_NAME` | ✅ | 云服务名称 |

## 快速入门

```bash
# List resources
python3 {{baseDir}}/scripts/cloudinary.py resources --prefix <value> --max_results <value>

# Get resource
python3 {{baseDir}}/scripts/cloudinary.py resource-get public_id <value>

# Upload asset
python3 {{baseDir}}/scripts/cloudinary.py upload --file <value> --folder <value> --public_id <value>

# Delete asset
python3 {{baseDir}}/scripts/cloudinary.py destroy --public_id <value>

# Rename asset
python3 {{baseDir}}/scripts/cloudinary.py rename --from_public_id <value> --to_public_id <value>

# Search assets
python3 {{baseDir}}/scripts/cloudinary.py search --expression <value> --max_results <value>

# List tags
python3 {{baseDir}}/scripts/cloudinary.py tags --prefix <value>

# List root folders
python3 {{baseDir}}/scripts/cloudinary.py folders
```

## 所有命令

| 命令 | 说明 |
|---------|-------------|
| `resources` | 列出所有资源 |
| `resource-get` | 获取特定资源 |
| `upload` | 上传资源 |
| `destroy` | 删除资源 |
| `rename` | 重命名资源 |
| `search` | 搜索资源 |
| `tags` | 列出资源的标签 |
| `folders` | 列出根文件夹 |
| `folder-create` | 创建文件夹 |
| `folder-delete` | 删除文件夹 |
| `transformations` | 列出可用的转换方式 |
| `usage` | 获取使用统计信息 |
| `presets` | 列出上传预设设置 |

## 输出格式

所有命令默认以 JSON 格式输出。若需以易读的格式输出，请添加 `--human` 参数。

```bash
python3 {{baseDir}}/scripts/cloudinary.py <command> --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{{baseDir}}/scripts/cloudinary.py` | 主要的命令行工具（包含所有命令） |

## 致谢

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码源码托管在 [GitHub](https://github.com/aiwithabidi) 上。  
本工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)