---
name: gitea
description: "使用 `tea` CLI 与 Gitea 进行交互。可以通过 `tea issues`、`tea pulls`、`tea releases` 等命令来管理问题（issues）、 Pull Request（PRs）和仓库（repository）的发布（releases）。"
---

# Gitea 使用技巧

使用 `tea` 命令行工具（CLI）与 Gitea 服务器进行交互。当不在 Git 目录中时，可以使用 `--repo owner/repo` 参数；或者使用 `--login instance.com` 参数来指定 Gitea 实例。

## 设置

首次使用前，请先完成登录：
```bash
tea login add
```

查看当前登录的用户：
```bash
tea whoami
```

## 仓库

列出您有权访问的仓库：
```bash
tea repos list
```

创建一个新的仓库：
```bash
tea repos create --name my-repo --description "My project" --init
```

创建一个私有仓库：
```bash
tea repos create --name my-repo --private --init
```

克隆一个仓库：
```bash
tea repos fork owner/repo
```

删除一个仓库：
```bash
tea repos delete --name my-repo --owner myuser --force
```

## 提交请求（Pull Requests）

列出所有未处理的提交请求：
```bash
tea pulls --repo owner/repo
```

查看特定的提交请求：
```bash
tea pr 55 --repo owner/repo
```

将提交请求拉取到本地：
```bash
tea pr checkout 55
```

创建一个新的提交请求：
```bash
tea pr create --title "Feature title" --description "Description"
```

## 问题（Issues）

列出所有未解决的问题：
```bash
tea issues --repo owner/repo
```

查看特定的问题：
```bash
tea issue 189 --repo owner/repo
```

创建一个新的问题：
```bash
tea issue create --title "Bug title" --body "Description"
```

查看某个里程碑下的问题：
```bash
tea milestone issues 0.7.0
```

## 评论（Comments）

在问题或提交请求中添加评论：
```bash
tea comment 189 --body "Your comment here"
```

## 发布版本（Releases）

列出所有已发布的版本：
```bash
tea releases --repo owner/repo
```

创建一个新的版本：
```bash
tea release create --tag v1.0.0 --title "Release 1.0.0"
```

## 自动化任务（CI/CD）

列出仓库的自动化任务相关配置（动作秘密）：
```bash
tea actions secrets list
```

创建一个新的自动化任务配置：
```bash
tea actions secrets create API_KEY
```

列出自动化任务中的变量：
```bash
tea actions variables list
```

设置自动化任务中的变量：
```bash
tea actions variables set API_URL https://api.example.com
```

## Webhook

列出仓库的 Webhook 配置：
```bash
tea webhooks list
```

列出组织的 Webhook 配置：
```bash
tea webhooks list --org myorg
```

创建一个新的 Webhook：
```bash
tea webhooks create https://example.com/hook --events push,pull_request
```

## 其他实体

列出仓库的分支：
```bash
tea branches --repo owner/repo
```

列出仓库的标签：
```bash
tea labels --repo owner/repo
```

列出所有的里程碑：
```bash
tea milestones --repo owner/repo
```

列出所有的组织：
```bash
tea organizations
```

查看仓库的详细信息：
```bash
tea repo --repo owner/repo
```

## 辅助功能

在浏览器中打开某个文件：
```bash
tea open 189                 # open issue/PR 189
tea open milestones          # open milestones page
```

克隆一个仓库：
```bash
tea clone owner/repo
```

查看通知信息：
```bash
tea notifications --mine
```

## 输出格式

使用 `--output` 或 `-o` 参数来控制输出格式：
```bash
tea issues --output simple   # simple text output
tea issues --output csv      # CSV format
tea issues --output yaml     # YAML format
```