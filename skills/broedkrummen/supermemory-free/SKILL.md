---
name: supermemory-free
description: 使用 Supermemory.ai 的免费 tier 进行云知识备份和检索。将高价值的见解存储在云端，并在本地内存不足时进行检索。该服务使用标准的 `/v3/documents` 和 `/v3/search` 端点（不包含仅限 Pro 订阅者的功能）。
---
# Supermemory Free — 云知识备份

使用 **免费 tier API** 将重要的知识和见解备份到 Supermemory.ai 的云端。  
仅使用 `/v3/documents`（存储）和 `/v3/search`（检索）接口，不使用仅限 Pro 用户的端点。

## 先决条件

请在 `.env` 文件中配置相关环境变量。  
```
SUPERMEMORY_OPENCLAW_API_KEY="sm_..."
```

## 工具

### supermemory_cloud_store  
将知识内容存储到云端。  
```bash
python3 skills/supermemory-free/store.py "Your knowledge string here"

# With optional container tag (namespace/filter)
python3 skills/supermemory-free/store.py "knowledge string" --tag openclaw

# With metadata
python3 skills/supermemory-free/store.py "knowledge string" --tag fixes --source "session"

# Output raw JSON
python3 skills/supermemory-free/store.py "knowledge string" --json
```

**使用场景：**  
- 用户请求永久保存某些信息  
- 重要的配置或设置信息  
- 已解决的问题及解决方案  
- 需要在不同会话间保持一致的关键事实  

---

### supermemory_cloud_search  
在云端搜索相关知识。  
```bash
python3 skills/supermemory-free/search.py "your query"

# With container tag filter
python3 skills/supermemory-free/search.py "your query" --tag openclaw

# More results
python3 skills/supermemory-free/search.py "your query" --limit 10

# Higher precision (less noise)
python3 skills/supermemory-free/search.py "your query" --threshold 0.7

# Search across ALL tags
python3 skills/supermemory-free/search.py "your query" --no-tag
```

**使用场景：**  
- 本地内存（如 MEMORY.md 文件或每日日志）中找不到所需信息  
- 用户提及很久以前的内容  
- 需要在不同会话间查找信息  
- 询问“你记得……吗？”之类的问题  

---

### 自动捕获（Cron 任务）  
定期扫描最近会话的日志，并自动将有价值的见解推送到 Supermemory 云端。  
```bash
# Run manually
python3 skills/supermemory-free/auto_capture.py

# Dry run (show what would be captured, no upload)
python3 skills/supermemory-free/auto_capture.py --dry-run

# Scan last N days (default: 3)
python3 skills/supermemory-free/auto_capture.py --days 7

# Force re-upload even if already seen
python3 skills/supermemory-free/auto_capture.py --force

# Verbose mode
python3 skills/supermemory-free/auto_capture.py --verbose
```

**安装 Cron 任务（每天凌晨 2:00 UTC 运行）：**  
```bash
bash skills/supermemory-free/install_cron.sh
```

**删除 Cron 任务：**  
```bash
bash skills/supermemory-free/install_cron.sh --remove
```

**检查 Cron 任务状态：**  
```bash
bash skills/supermemory-free/install_cron.sh --status
```

---

## 自动捕获的内容  
自动捕获脚本根据以下规则识别日志中的“有价值”见解：  

| 规则 | 标签 | 示例 |
|---------|-------|---------|
| 已解决的错误/修复方案 | `fix` | `通过执行……修复了 SSL 证书错误` |
| 错误信息 | `error` | `异常：端口 5432 上的连接被拒绝` |
| 配置路径 | `config` | `/etc/nginx/sites-available/default` |
| API/端点信息 | `api` | `端点：POST /v3/documents 用于存储` |
| 用户偏好设置 | `preference` | `用户更喜欢使用 Python 而不是 Node.js 编写脚本` |
| 做出的决策 | `decision` | `决定使用 PostgreSQL……` |
| 学到的知识 | `insight` | `了解到……的 Cron 语法` |
| 安装/配置操作 | `setup` | `安装了 nginx，并进行了配置` |
| 列表项内容 | `bullet` | `- 关键发现：X 比 Y 更有效` |

**去重机制：**  
已上传的文件会被记录在 `.capture_state.json` 文件中，重复上传是安全的。  

---

## 容器标签  
使用 `--tag` 为知识内容添加命名空间：  

| 标签 | 用途 |  
|-----|---------|  
| `openclaw` | 通用 OpenClaw 会话相关知识（默认标签） |
| `fixes` | 错误修复方案 |
| `config` | 配置和设置信息 |
| `user-prefs` | 用户偏好设置 |
| `projects` | 项目特定知识 |

---

## 文件列表  
| 文件名 | 用途 |  
|------|---------|  
| `store.py` | CLI 工具：将知识内容上传到云端 |
| `search.py` | CLI 工具：在云端搜索知识 |
| `auto_capture.py` | Cron 脚本：自动分析日志文件 |
| `install_cron.sh` | 安装/删除/检查 Cron 任务的状态 |
| `.capture_state.json` | 用于记录去重状态的文件（自动生成，需添加到 gitignore 文件夹） |
| `SKILL.md` | 本文档文件 |
| `_meta.json` | 技能文档的元数据 |

---

## API 信息  
- **基础 URL：** `https://api.supermemory.ai`  
- **存储接口：** `POST /v3/documents`  
- **搜索接口：** `POST /v3/search`  
- **认证方式：** 使用 `SUPERMEMORY_OPENCLAW_API_KEY` 生成的令牌进行身份验证  
- **免费 tier 的使用限制：** 请访问 https://console.supermemory.ai 查看当前配额  
- **注意：** 代码中包含了兼容 Cloudflare 的请求头，可避免 1010 错误（访问被拒绝）。  

## 故障排除  
- **HTTP 403/1010 访问被拒绝：**  
  脚本中包含了正确的 `User-Agent`、`Origin` 和 `Referer` 请求头，以满足 Cloudflare 的要求。如果问题仍然存在，请确认 API 密钥的有效性（访问 https://console.supermemory.ai）。  
- **未找到日志文件：**  
  自动捕获功能会查找 `memory/YYYY-MM-DD.md` 文件。请确保您的知识内容每天都被记录到该文件中。  
- **重新上传所有数据：**  
  删除 `.capture_state.json` 文件，或使用 `--force` 参数忽略去重结果。