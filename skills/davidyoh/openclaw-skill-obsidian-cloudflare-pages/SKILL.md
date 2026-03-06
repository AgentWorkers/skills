---
name: obsidian-cloudflare-pages
description: 将选定的 Obsidian Markdown 文档从存储库发布到静态网站，并部署到 Cloudflare Pages。
homepage: https://pages.cloudflare.com/
---
# OpenClaw 技能：将 Obsidian/Markdown 内容发布到 Cloudflare Pages

这是一个用于将 Markdown 内容发布到 Cloudflare Pages 的 OpenClaw 技能。

- 支持使用 Obsidian 的 vault 文件夹或任何 Markdown 文件夹。
- 该技能最初是为读取 Obsidian Web Clipper 的输出而开发的：  
  - https://obsidian.md/clipper

该技能可自动化以下发布流程：
1. 从源文件夹中选择笔记。
2. 将内容同步到发布工作区。
3. 使用 Quartz 工具生成静态 HTML 文件。
4. 将生成的文件部署到 Cloudflare Pages。

## 命令

- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js init`  
  - 根据示例创建 `config/config.json` 配置文件。
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js wizard`  
  - 提供交互式设置向导，用于配置 vault 文件夹、站点域名以及 Cloudflare 项目的相关信息。
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js setup-project`  
  - 如果配置的工作区不存在，会初始化 Quartz 项目。
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js doctor`  
  - 验证路径和所需的二进制文件是否齐全。
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js sync`  
  - 将选中的笔记和资源文件同步到发布内容文件夹。
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js build`  
  - 在项目目录中运行 Quartz 构建脚本。
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js deploy`  
  - 使用 wrangler 工具将内容部署到 Cloudflare Pages。
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js run`  
  - 同步 → 构建 → 部署。
- `node skills/obsidian-cloudflare-pages/bin/publishmd-cf.js run --dry-run`  
  - 预览发布流程（不会修改文件或进行实际部署）。

## 配置

请复制并编辑 `skills/obsidian-cloudflare-pages/config/config.example.json` 文件，然后将其保存为 `skills/obsidian-cloudflare-pages/config/config.json`：

### 安全默认设置
- 按文件夹设置发布内容的允许列表。
- 可选地使用 `publish: true` 来控制内容的发布。
- 默认情况下，私有文件夹将被排除在发布范围之外。

## 所需软件
- `node`（版本 20 及以上）
- `rsync`
- `npm`
- `npx quartz`
- `wrangler`

## Cloudflare API 令牌设置（推荐）

请创建一个 Cloudflare API 令牌，至少需要具备以下权限：
- **Cloudflare Pages → 编辑** 操作权限。
- （可选）如果需要自动化 DNS 配置，还需要 **DNS → 编辑** 权限。

您可以在 shell 配置文件（`~/.zshrc`）中设置环境变量，或者使用技能特定的 `.env` 文件来存储这些信息。

### 方法一：通过 shell 配置文件（`~/.zshrc`）

```bash
export CLOUDFLARE_API_TOKEN="<your-token>"
export CLOUDFLARE_ACCOUNT_ID="<your-account-id>"
```

重新加载 shell 配置：

```bash
source ~/.zshrc
```

### 方法二：使用技能特定的 `.env` 文件（推荐）

```bash
cp skills/obsidian-cloudflare-pages/.env.example skills/obsidian-cloudflare-pages/.env
# then edit .env
# optional auth envs: BASIC_AUTH_USERNAME / BASIC_AUTH_PASSWORD
```

该技能会自动加载 `skills/obsidian-cloudflare-pages/.env` 文件中的配置（不会覆盖现有的 shell 环境变量）。

设置向导会要求用户提供以下信息：
- 完整的生产域名（例如：`YOURDOMAIN.COM`）。
- 品牌设置（根目录的索引标签、侧边栏标题等）。
- API 令牌/账户相关的环境变量名称（如上所述）。
- 可选的基本身份验证设置（用户名/密码）。

## 注意事项

- ⚠️ 如果直接使用 `setup-project` 命令失败，系统可能会在克隆 Quartz 之前清空配置的工作区目录。建议为该技能使用专门的工作区路径。
- 系统会进行安全检查；如果工作区不为空，必须设置 `ALLOW_DESTRUCTIVE=1` 才能执行清理操作。
- 在执行预发布操作（`--dry-run`）时，敏感信息（如 API 令牌）会被隐藏。

## OpenClaw 使用提示

示例命令：
- “为我的 Markdown 文件夹设置 obsidian-cloudflare-pages 功能。”
- “运行 `doctor` 命令，查看缺少哪些依赖项。”
- “同步、构建并部署到 Cloudflare Pages。”
- “启用基本身份验证后重新部署。”

最佳实践：
- 将敏感信息存储在 `.env` 文件中（切勿将其写入聊天记录）。
- 建议使用基于环境变量的基本身份验证方式（`BASIC_AUTH_USERNAME` / `BASIC_AUTH_PASSWORD`）。
- 请提交 `config.example.json` 文件，而非个人配置文件 `config.json`。
- 仅在生产环境前在测试子域名上测试该技能。

## 独立使用（无需 OpenClaw）

该技能也可以作为独立的 Node CLI 工具使用：

```bash
node bin/publishmd-cf.js init
node bin/publishmd-cf.js wizard
cp .env.example .env
# fill .env values
node bin/publishmd-cf.js run
```

## 安全提示

该技能中的基本身份验证功能较为简单且为可选设置。在发布高度敏感的内容之前，请确保您完全了解自己的安全策略和相应的安全措施。

安全控制选项：
- `--dry-run`（或 `DRY_RUN=1`）：用于预览发布流程，不会修改或部署实际内容。
- 只有在明确允许的情况下，才能设置 `ALLOW_DESTRUCTIVE=1` 以执行清理操作（即使工作区不为空）。