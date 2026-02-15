---
name: canva
version: 1.0.0
description: |
  Manage Canva designs, assets, and folders via the Connect API.
  
  WHAT IT CAN DO:
  - List/search/organize designs and folders
  - Export finished designs (PNG/PDF/JPG)
  - Upload images to asset library
  - Autofill brand templates with data
  - Create blank designs (doc/presentation/whiteboard/custom)
  
  WHAT IT CANNOT DO:
  - Add content to designs (text, shapes, elements)
  - Edit existing design content
  - Upload documents (images only)
  - AI design generation
  
  Best for: asset pipelines, export automation, organization, template autofill.
  Triggers: /canva, "upload to canva", "export design", "list my designs", "canva folder".
author: clawdbot
license: MIT
metadata:
  clawdbot:
    emoji: "🎨"
    triggers: ["/canva"]
    requires:
      env:
        - CANVA_CLIENT_ID
        - CANVA_CLIENT_SECRET
    primaryEnv: CANVA_CLIENT_ID
    homepage: https://canva.dev/docs/connect/
---

# Canva Connect

通过 Connect API 管理 Canva 的设计、资产和文件夹。

## 该功能的用途（及不可用的功能）

| 可以执行 | 不能执行 |
|-----------|--------------|
| 列出/搜索设计 | 向设计中添加内容 |
| 创建空白设计 | 编辑现有设计的内容 |
| 导出设计（PNG/PDF/JPG） | 上传文档（仅限图片） |
| 创建/管理文件夹 | 生成 AI 设计 |
| 在文件夹间移动项目 | |
| 上传图片作为资产 | |
| 自动填充品牌模板 | |

## 实际使用场景

**1. 资产管理流程** 🖼️
```
Generate diagram → upload to Canva → organize in project folder
```

**2. 导出自动化** 📤
```
Design finished in Canva → export via CLI → use in docs/website
```

**3. 设计组织** 📁
```
Create project folders → move related designs → keep Canva tidy
```

**4. 自动填充品牌模板** 📋
```
Set up template in Canva → pass data via API → get personalized output
```

## 快速入门

```bash
# Authenticate (opens browser for OAuth)
{baseDir}/scripts/canva.sh auth

# List your designs
{baseDir}/scripts/canva.sh designs list

# Create a new design
{baseDir}/scripts/canva.sh designs create --type doc --title "My Document"

# Export a design
{baseDir}/scripts/canva.sh export <design_id> --format pdf
```

## 设置

### 1. 创建 Canva 集成

1. 访问 [canva.com/developers/integrations](https://canva.com/developers/integrations)
2. 点击 **创建集成**
3. 设置权限范围：
   - `design:content`（读取 + 写入）
   - `design:meta`（读取）
   - `asset`（读取 + 写入）
   - `brandtemplate:meta`（读取）
   - `brandtemplate:content`（读取）
   - `profile`（读取）
4. 设置 OAuth 重定向地址：`http://127.0.0.1:3001/oauth/redirect`
5. 记录 **客户端 ID** 并生成 **客户端密钥**

### 2. 配置环境

将以下配置添加到 `~/.clawdbot/clawdbot.json` 文件的 `skills.entries` 部分：

```json
{
  "skills": {
    "entries": {
      "canva": {
        "clientId": "YOUR_CLIENT_ID",
        "clientSecret": "YOUR_CLIENT_SECRET"
      }
    }
  }
}
```

或者通过设置环境变量来实现：

```bash
export CANVA_CLIENT_ID="your_client_id"
export CANVA_CLIENT_SECRET="your_client_secret"
```

### 3. 认证

```bash
{baseDir}/scripts/canva.sh auth
```

系统会打开浏览器进行 OAuth 同意流程。令牌存储在 `~/.clawdbot/canva-tokens.json` 文件中。

## 命令

### 认证
| 命令 | 描述 |
|---------|-------------|
| `auth` | 启动 OAuth 流程（打开浏览器） |
| `auth status` | 检查认证状态 |
| `auth logout` | 清除存储的令牌 |

### 设计
| 命令 | 描述 |
|---------|-------------|
| `designs list [--limit N]` | 列出你的设计 |
| `designs get <id>` | 获取设计详情 |
| `designs create --type <type> --title <title>` | 创建新设计 |
| `designs delete <id>` | 将设计移至回收站 |

**设计类型：`doc`, `presentation`, `whiteboard`, `poster`, `instagram_post`, `facebook_post`, `video`, `logo`, `flyer`, `banner`

### 导出
| 命令 | 描述 |
|---------|-------------|
| `export <design_id> --format <fmt>` | 导出设计 |
| `export status <job_id>` | 检查导出任务的状态 |

**格式：`pdf`, `png`, `jpg`, `gif`, `pptx`, `mp4`

### 资产
| 命令 | 描述 |
|---------|-------------|
| `assets list` | 列出上传的资产 |
| `assets upload <file> [--name <name>]` | 上传资产 |
| `assets get <id>` | 获取资产详情 |
| `assets delete <id>` | 删除资产 |

### 品牌模板
| 命令 | 描述 |
|---------|-------------|
| `templates list` | 列出品牌模板 |
| `templates get <id>` | 获取模板详情 |
| `autofill <template_id> --data <json>` | 使用数据自动填充模板 |

### 文件夹
| 命令 | 描述 |
|---------|-------------|
| `folders list` | 列出文件夹 |
| `folders create <name>` | 创建文件夹 |
| `folders get <id>` | 获取文件夹内容 |

### 用户
| 命令 | 描述 |
|---------|-------------|
| `me` | 获取当前用户信息 |

## 示例

### 创建并导出海报
```bash
# Create
{baseDir}/scripts/canva.sh designs create --type poster --title "Event Poster"

# Export as PNG
{baseDir}/scripts/canva.sh export DAF... --format png --output ./poster.png
```

### 上传品牌资产
```bash
# Upload logo
{baseDir}/scripts/canva.sh assets upload ./logo.png --name "Company Logo"

# Upload multiple
for f in ./brand/*.png; do
  {baseDir}/scripts/canva.sh assets upload "$f"
done
```

### 自动填充模板
```bash
# List available templates
{baseDir}/scripts/canva.sh templates list

# Autofill with data
{baseDir}/scripts/canva.sh autofill TEMPLATE_ID --data '{
  "title": "Q1 Report",
  "subtitle": "Financial Summary",
  "date": "January 2026"
}'
```

## API 参考

基础 URL：`https://api.canva.com/rest`

详细端点文档请参阅 [references/api.md](references/api.md)。

## 故障排除

### 令牌过期
```bash
{baseDir}/scripts/canva.sh auth  # Re-authenticate
```

### 请求速率限制
API 对每个端点有请求速率限制。脚本会自动处理超时重试。

### 权限范围缺失
如果操作失败并返回 403 错误，请确保你的集成已启用所需的权限范围。

## 数据文件

| 文件 | 用途 |
|------|---------|
| `~/.clawdbot/canva-tokens.json` | OAuth 令牌（已加密） |
| `~/.clawdbot/canva-cache.json` | 响应缓存 |