---
name: obsidian-cloudflare-pages
description: 将选定的 Obsidian Markdown 文件从存储库发布到静态网站，并部署到 Cloudflare Pages。
homepage: https://pages.cloudflare.com/
---
# OpenClaw 技能：将 Obsidian/Markdown 内容发布到 Cloudflare Pages

这是一个用于将 Markdown 内容发布到 Cloudflare Pages 的 OpenClaw 技能。

- 支持使用 Obsidian 的 vault 文件夹，或任何 Markdown 文件夹；
- 最初是为读取 Obsidian Web Clipper 的输出而开发的（链接：https://obsidian.md/clipper）。

该技能可自动化以下发布流程：
1. 从源文件夹中选择需要发布的笔记；
2. 将这些笔记同步到指定的发布工作区；
3. 使用 Quartz 工具生成静态 HTML 文件；
4. 将生成的 HTML 文件部署到 Cloudflare Pages 上。

## 命令

- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js init`：根据示例配置文件创建 `config/config.json`；
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js wizard`：提供交互式设置向导（用于配置 vault 文件夹、站点域名、Cloudflare 项目等）；
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js setup-project`：在缺少配置的情况下初始化 Quartz 项目；
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js doctor`：检查路径及所需二进制文件的完整性；
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js sync`：将选定的笔记和资源文件同步到发布文件夹；
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js build`：在项目目录中运行 Quartz 构建脚本；
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js deploy`：使用 wrangler 工具将生成的 HTML 文件部署到 Cloudflare Pages；
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js run`：执行同步、构建和部署的完整流程。

## 配置文件

请复制并编辑 `skills/obsidian-cloudflare-pages/config/config.example.json` 文件：

### 安全默认设置
- 按文件夹设置发布内容的允许列表；
- 可选地启用 `publish: true` 选项以控制内容的发布；
- 默认情况下，私有文件夹不会被包含在发布范围内。

## 所需软件
- `node`（版本 20 及以上）；
- `rsync`；
- `npm`；
- `npx quartz`；
- `wrangler`。

## Cloudflare API 令牌设置（推荐）

请创建一个 Cloudflare API 令牌，至少具备以下权限：
- **账户 → Cloudflare Pages:Edit**；
- （可选）**区域 → DNS:Edit**（如果需要自动化 DNS 配置）。

您可以在 shell 配置文件（如 `~/.zshrc`）中设置环境变量，或使用技能自带的 `.env` 文件来存储这些信息。

### 设置方式

**选项 A：通过 shell 配置文件（`~/.zshrc`）**

```bash
export CLOUDFLARE_API_TOKEN="<your-token>"
export CLOUDFLARE_ACCOUNT_ID="<your-account-id>"
```

**选项 B：使用技能自带的 `.env` 文件（推荐）**

```bash
cp skills/obsidian-cloudflare-pages/.env.example skills/obsidian-cloudflare-pages/.env
# then edit .env
```

该技能会自动加载 `skills/obsidian-cloudflare-pages/.env` 文件中的配置（而不会覆盖现有的 shell 环境变量）。

设置向导会要求您提供以下信息：
- 完整的生产域名（例如：`YOURDOMAIN.COM`）；
- 品牌设置（包括源文件夹路径、首页标题、侧边栏标题等）；
- API 令牌/账户相关的环境变量名称（如上所述）；
- 可选的基于基本身份验证（用户名/密码）的访问控制。

## 注意事项

- ⚠️ 如果直接使用 `setup-project` 命令失败，系统可能会在克隆 Quartz 之前清空配置工作区中的文件。建议为该技能创建专门的工作区路径。

### OpenClaw 使用提示

示例命令：
- “为我的 Markdown 文件夹设置 obsidian-cloudflare-pages 功能。”
- “运行 `doctor` 命令检查缺少哪些依赖项。”
- “同步、构建并部署到 Cloudflare Pages。”
- “启用基本身份验证后重新部署。”

**最佳实践**：
- 将敏感信息存储在 `.env` 文件中（切勿将其包含在聊天记录中）；
- 请提交 `config.example.json` 文件（而非个人配置文件）；
- 使用有限权限的 Cloudflare 令牌（仅在需要时使用 Cloudflare Pages 或 DNS 编辑功能）；
- 在生产环境之前，先在测试子域名上测试该技能。

### 独立使用（无需 OpenClaw）

该技能也可以作为独立的 Node CLI 工具使用：

```bash
node bin/publishmd-cf.js init
node bin/publishmd-cf.js wizard
cp .env.example .env
# fill .env values
node bin/publishmd-cf.js run
```

### 安全提示

该技能中的基本身份验证功能较为简单且为可选。除非您完全了解自己的安全策略和防护措施，否则请勿使用该功能来发布高度敏感的内容。