---
name: static-files
description: >
  Host static files on subdomains with optional authentication. Use when you need to
  serve HTML, images, CSS, JS, or any static content on a dedicated subdomain. Supports
  file upload, basic auth, quota management, and automatic SSL via Caddy. Commands
  include sf sites (create/list/delete), sf upload (files/directories), sf files (list/delete).
---

# 静态文件托管

将静态内容托管在 `*.{domain}` 子域名上，并自动启用 SSL 加密。

## 快速参考

```bash
# Create site
sf sites create mysite
# → https://mysite.498as.com

# Upload file
sf upload ./index.html mysite

# Upload directory  
sf upload ./dist mysite

# Add authentication
sf sites auth mysite admin:secretpass123

# List files
sf files mysite

# Delete file
sf files mysite delete path/to/file.txt

# Delete site
sf sites delete mysite
```

## 环境配置

```bash
export SF_API_URL=http://localhost:3000   # API endpoint
export SF_API_KEY=sk_xxxxx                # Your API key
```

## 工作流程

### 部署静态网站

```bash
# 1. Create the site
sf sites create docs

# 2. Upload the build directory
sf upload ./build docs

# 3. Verify
curl -I https://docs.498as.com
```

### 保护文件共享

```bash
# 1. Create site with auth
sf sites create private
sf sites auth private user:strongpassword

# 2. Upload sensitive files
sf upload ./reports private

# 3. Share URL + credentials
# https://private.498as.com (user / strongpassword)
```

### 更新现有文件

```bash
# Overwrite existing file
sf upload ./new-version.pdf mysite --overwrite

# Or delete and re-upload
sf files mysite delete old-file.pdf
sf upload ./new-file.pdf mysite
```

## 命令行接口（CLI）命令

### sites

| 命令 | 描述 |
|---------|-------------|
| `sf sites list` | 列出所有站点 |
| `sf sites create <name>` | 创建新站点 |
| `sf sites delete <name>` | 删除站点及其所有文件 |
| `sf sites auth <name> <user:pass>` | 设置基本认证信息 |
| `sf sites auth <name> --remove` | 移除认证信息 |

### upload

```bash
sf upload <path> <site> [subdir] [--overwrite] [--json]
```

- `path`：要上传的文件或目录路径 |
- `site`：目标站点名称 |
- `subdir`：可选的子目录 |
- `--overwrite`：覆盖现有文件 |
- `--json`：以 JSON 格式输出结果 |

### files

| 命令 | 描述 |
|---------|-------------|
| `sf files <site>` | 列出所有文件 |
| `sf files <site> delete <path>` | 删除指定文件 |

### stats

```bash
sf stats              # Global stats
sf stats <site>       # Site-specific stats
```

## API 端点

基础 URL：`$SF_API_URL`，请求头需包含 `Authorization: Bearer $SF_API_KEY`

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | `/sites` | 列出所有站点 |
| POST | `/sites` | 创建新站点 |
| DELETE | `/sites/{name}` | 删除站点 |
| PATCH | `/sites/{name}` | 更新站点认证信息 |
| GET | `/sites/{name}/files` | 列出站点文件 |
| POST | `/sites/{name}/files` | 上传文件 |
| DELETE | `/sites/{name}/files/{path}` | 删除文件 |
| GET | `/stats` | 获取全局统计信息 |
| GET | `/stats/{name}` | 获取站点统计信息 |
| GET | `/health` | 进行健康检查 |

## 限制条件

- **站点名称**：只能使用小写字母、数字和连字符，长度最多 63 个字符 |
- **文件大小**：默认为 50MB（可配置） |
- **每个站点的配额**：默认为 100MB |
- **API 密钥的请求速率限制**：每分钟 100 次请求 |

## 故障排除

### “无法连接到 API”
```bash
# Check service status
systemctl status kleo-static-files

# Check if port is listening
curl http://localhost:3000/health
```

### “API 密钥无效”
```bash
# Verify key is set
echo $SF_API_KEY

# Create new key if needed
bun run /opt/kleo-static-files/scripts/create-key.ts "new-key"
```

### “超出配额”
```bash
# Check current usage
sf stats mysite

# Delete unused files
sf files mysite delete large-file.zip
```

### 站点无法通过 HTTPS 访问”
```bash
# Verify DNS points to server
dig mysite.498as.com

# Check Caddy config
cat /etc/caddy/sites.d/static-files.caddy

# Resync Caddy
bun run /opt/kleo-static-files/scripts/sync-caddy.ts --reload
```

## 安装

### 服务器端安装（在主机上运行一次）

```bash
curl -fsSL https://raw.githubusercontent.com/498AS/kleo-static-files/main/install.sh | sudo bash
```

安装程序会生成一个 JSON 文件，其中包含从 `KLEO_SF_CONFIG_BEGIN` 到 `KLEO_SF_CONFIG_END` 之间的配置信息。解析该文件可获取 `api_url` 和 `api_key`。

### 安装完成后

```bash
export SF_API_URL=http://localhost:3000
export SF_API_KEY=sk_xxxxx  # from installer output
```

### 检查状态

```bash
sudo /opt/kleo-static-files/install.sh --status
```

有关手动安装的详细信息，请参阅 [references/install.md](references/install.md)。