---
name: vercel
slug: vercel-deployment
version: 1.0.0
description: 部署和管理 Vercel 项目，包括关联仓库、环境变量（env vars）以及域名。
---
# Vercel — 部署和管理项目

## 设置新项目

```bash
cd <project-root>   # must be the directory with .git
npx vercel link      # link to Vercel project
npx vercel git connect  # connect GitHub repo for auto-deploys
```

请从仓库根目录（包含 `.git` 文件的目录）运行 `vercel git connect` 命令，切勿在子目录中执行该命令。

## 设置环境变量

**切勿使用 `echo` 命令** — 因为该命令会在输出末尾添加 `\n` 字符：
```bash
printf 'value' | npx vercel env add VAR_NAME production
```

## 检查域名

```bash
cd any-vercel-project && npx vercel domains ls
```

完整的域名列表请参阅该文件夹中的 `domains.md` 文件。