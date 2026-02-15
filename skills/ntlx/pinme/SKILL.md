---
name: pinme
description: |
  Deploy static websites to IPFS with a single command using PinMe CLI.
  Use when: (1) User wants to deploy a built frontend project, (2) Need to upload static files (dist/build/out/public) to IPFS, (3) Requesting preview URL for a deployed site.
  Supports: Vite, React, Vue, Next.js, Angular, Create React App, and static sites.
  Output: Preview URL (https://pinme.eth.limo/#/preview/*) after successful upload.
---

# PinMe – 零配置前端部署工具

只需一个命令，即可将静态网站部署到 IPFS 网络中。无需服务器、无需账户，也无需任何设置。

## 使用场景

当用户需要：
- 部署、上传或发布前端项目
- 获取已构建网站的预览地址
- 提到 PinMe 或 IPFS 部署时

## 快速入门

```bash
# Install PinMe
npm install -g pinme

# Deploy (auto-detects static directory)
pinme upload dist

# Get preview URL
# https://pinme.eth.limo/#/preview/*
```

## 核心工作流程

### 1. 检查前提条件
```bash
# Check Node.js version (requires 16.13.0+)
node --version

# Verify pinme is installed
pinme --version
```

### 2. 确定静态文件目录
PinMe 会按优先级自动检测以下目录：
| 目录          | 使用的框架/工具         |
|---------------|-------------------|
| `dist/`        | Vite、Vue CLI、Angular        |
| `build/`        | Create React App       |
| `out/`        | Next.js（静态文件导出）       |
| `public/`       | 静态网站文件目录        |

**验证规则：**
- ✅ 该文件夹必须存在。
- ✅ 必须包含 `index.html` 文件。
- ✅ 文件夹中必须包含实际的静态文件（CSS、JS、图片等）。

### 3. 执行部署
```bash
# Deploy dist directory (most common)
pinme upload dist

# Deploy specific directory
pinme upload build

# Upload and bind to custom domain (requires Plus)
pinme upload dist --domain my-site
```

### 4. 返回结果
仅返回预览地址：`https://pinme.eth.limo/#/preview/*`

## 命令参考

| 命令            | 描述                        |
|------------------|-----------------------------|
| `pinme upload <目录>`    | 将静态文件上传到 IPFS                |
| `pinme upload <目录> --domain <域名>` | 上传文件并绑定域名                |
| `pinme import <CAR 文件>`    | 导入 CAR 文件                    |
| `pinme export <CID>`     | 将 IPFS 内容导出为 CAR 文件            |
| `pinme list`       | 显示上传历史记录                |
| `pinme rm <哈希值>`     | 从 IPFS 中删除文件                |
| `pinme set-appkey`     | 设置用于身份验证的 AppKey                |
| `pinme my-domains`    | 查看拥有的域名                    |
| `pinme --version`     | 显示版本信息                    |

## 上传限制

| 类型            | 免费计划                |
|------------------|-------------------------|
| 单个文件        | 200MB                     |
| 整个目录        | 1GB                        |

## 错误处理

| 错误类型           | 解决方案                         |
|------------------|-----------------------------------|
| Node.js 版本过低       | 升级到 16.13.0 或更高版本                |
| 命令未找到        | 运行 `npm install -g pinme`                |
| 文件夹不存在        | 检查路径，可以使用 `ls` 命令                |
| 上传失败          | 检查网络连接，重试                   |
| 身份验证失败        | 运行 `pinme set-appkey`                  |

## 程序化部署流程

1. **检查环境**：`node --version`（确保 Node.js 版本 >= 16.13.0）
2. **安装 PinMe**：`npm install -g pinme`
3. **检测静态文件目录**：检查 `dist/`、`build/`、`out/`、`public/`
4. **验证文件**：确认目录中包含 `index.html`
5. **执行部署**：`pinme upload <目录>`
6. **返回结果**：仅返回预览地址

**禁止的操作：**
- ❌ 禁止上传 `node_modules`、`.env`、`.git` 文件
- ❌ 禁止上传源代码目录（`src/`）
- ❌ 禁止上传配置文件（如 `package.json` 等）
- ❌ 禁止上传不存在或为空的文件夹

## GitHub Actions 集成示例

```yaml
name: Deploy to PinMe
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci && npm run build
      - run: npm install -g pinme
      - run: pinme set-appkey "${{ secrets.PINME_APPKEY }}"
      - run: pinme upload dist --domain "${{ secrets.DOMAIN }}"
```

## 机器可读的配置文件

```json
{
  "tool": "pinme",
  "requirements": {
    "node_version": ">=16.13.0"
  },
  "install": "npm install -g pinme",
  "upload": "pinme upload {{directory}}",
  "upload_with_domain": "pinme upload {{directory}} --domain {{domain}}",
  "validDirectories": ["dist", "build", "out", "public"],
  "requiredFiles": ["index.html"],
  "excludePatterns": ["node_modules", ".env", ".git", "src"],
  "limits": {
    "single_file": "200MB",
    "total_directory": "1GB"
  },
  "output": "preview_url",
  "preview_url_format": "https://pinme.eth.limo/#/preview/*",
  "fixed_domain_format": "https://*.pinit.eth.limo"
}
```

## 资源链接

- **官方网站**：https://pinme.eth.limo/
- **GitHub 仓库**：https://github.com/glitternetwork/pinme
- **AppKey**：https://pinme.eth.limo/（可在控制面板获取）