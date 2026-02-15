---
name: netlify
description: 使用 Netlify CLI（`netlify`）来创建/链接 Netlify 网站，并配置持续集成/持续部署（CI/CD）流程，特别是对于单仓库项目（即一个仓库中包含多个网站，例如使用 Hugo 框架构建的网站，这些网站存储在 `sites/<domain>` 目录下）。当 Avery 提出部署新网站、将仓库连接到 Netlify、配置构建/发布设置、设置环境变量、启用部署预览功能或自动化 Netlify 网站创建流程时，可以使用该工具。
---

# Netlify

使用 `netlify` 命令行工具（CLI）来创建项目（“站点”），将本地文件夹与项目关联，并配置来自 GitHub 的持续集成/持续部署（CI/CD）流程。

## 先决条件

- 确保已安装 `netlify` 并知道其版本：`netlify --version`
- 已登录 Netlify 账户（`netlify login`）；或者提供登录凭据 `--auth $NETLIFY_AUTH_TOKEN`。
- 确定要在哪个 Netlify 团队/账户下创建站点（可选，但推荐）。

### 建议的代码示例（Monorepo 模式）

对于 **一个仓库中包含多个站点的情况**（例如 `sites/seattlecustomboatparts.com`、`sites/floridacustomerboatparts.com`）：

- 为每个域名创建一个独立的 Netlify 站点。
- 将站点的 **基础目录** 设置为对应的子文件夹。
- 在该子文件夹内创建一个 `netlify.toml` 文件。

这样可以确保每个域名的构建配置都是独立管理的。

#### 在 Hugo 子文件夹中创建 `netlify.toml`

在 `sites/<domain>/` 目录下创建 `netlify.toml` 文件：

（根据需要调整 `HUGO_VERSION` 的值。）

### 快速工作流程：创建站点 → 关联本地文件夹 → 配置 CI/CD

### 1) 创建一个 Netlify 站点

在要部署的站点文件夹内运行以下命令：

（具体命令根据实际情况填写。）

**注意：** `--with-ci` 选项用于启用 CI 钩子（持续集成流程）的设置。如果需要手动控制构建过程，可以添加 `--manual` 选项。

### 2) 将本地文件夹与创建的站点关联

如果本地文件夹尚未与站点关联，请执行以下操作：

（具体命令根据实际情况填写。）

### 3) 连接到 GitHub 以实现持续部署

（通常需要交互式操作，选择 Git 远程仓库并进行构建配置。对于自动化部署，可以先创建 `netlify.toml` 文件，然后接受默认设置。）

## 环境变量

可以为每个站点设置自定义环境变量：

（具体环境变量根据实际需求填写。）

### 对于单仓库多站点的场景：

- `CONTACT_EMAIL`：用于联系 Netlify 支持团队（或其他共享配置信息）。

### 部署

**手动部署**（适用于快速预览）：

（具体部署命令根据实际情况填写。）

### 包含的脚本

- `scripts/hugo_netlify_toml.sh`：用于在 Hugo 子文件夹中生成 `netlify.toml` 文件。
- `scripts/netlify_monorepo_site.sh`：用于帮助创建站点、关联本地文件夹并配置 CI/CD 流程。

在使用脚本时，建议通过环境变量 `NETLIFY_AUTH_TOKEN` 传递登录凭据，以确保非交互式操作的安全性。