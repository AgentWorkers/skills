---
name: wip-release
description: >
  单命令发布流程：  
  1. 提升版本号；  
  2. 更新变更日志（changelog）和 SKILL.md 文件；  
  3. 将更新内容发布到 npm 仓库；  
  4. 同时将更新内容推送到 GitHub。
license: MIT
interface: [cli, module, mcp]
metadata:
  display-name: "Release Pipeline"
  version: "1.2.4"
  homepage: "https://github.com/wipcomputer/wip-release"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - version-bump
    - changelog-update
    - skill-sync
    - npm-publish
    - github-release
  requires:
    bins: [git, npm, gh, op, clawhub]
    secrets:
      - path: ~/.openclaw/secrets/op-sa-token
        description: 1Password service account token
      - vault: Agent Secrets
        item: npm Token
        description: npm publish token
  openclaw:
    requires:
      bins: [git, npm, gh, op]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-release"
        bins: [wip-release]
        label: "Install via npm"
    emoji: "🚀"
compatibility: Requires git, npm, gh, op (1Password CLI). Node.js 18+.
---
# wip-release  
本地发布流程：通过一个命令即可提升版本号、更新所有文档，并将更新内容发布到所有渠道。  

## 适用场景  
- 发布任何 @wipcomputer 包的新版本  
- 合并 PR 到主分支后需要立即发布内容  
- 一次性完成版本号更新、变更日志更新以及 SKILL.md 文件的更新  

## 命令选项说明  
- `--dry-run`：在提交前预览发布流程的具体操作  
- `--no-publish`：仅更新版本号和标签，不将内容发布到注册中心  

### 不适用场景  
- 预发布/alpha 版本（该功能目前不支持）  
- 没有 `package.json` 文件的仓库  

## API 参考  
（此处可添加 API 相关信息，如果有的话）  

### 命令行接口（CLI）  
（此处可添加 CLI 命令的详细说明，包括参数和使用方法）  

### 产品文档检查机制  
`wip-release` 会在发布前检查产品文档（包括开发更新信息、路线图以及 `readme-first` 文件）是否已更新。该功能仅适用于包含 `ai/` 目录的仓库：  
- `patch`：若产品文档过时，会发出警告（不会阻止发布流程）  
- `minor/major`：在产品文档更新完成前，会阻止发布  
- `--skip-product-check`：跳过文档检查  

**检查内容：**  
1. `ai/dev-updates/` 目录中是否存在过去 3 天内的更新文件  
2. `ai/product/plans-prds/roadmap.md` 是否自上次发布后有修改  
3. `ai/product/readme-first-product.md` 是否自上次发布后有修改  

### 模块相关操作  
（此处可添加模块相关的使用说明）  

## 常见问题与解决方法  
- **“无法从 1Password 获取 npm 令牌”**：请确认 `~/.openclaw/secrets/op-sa-token` 文件存在，并且已安装 `op` CLI 工具。  
- **“推送失败”**：可能是分支保护机制导致的。请确保在合并 PR 后处于主分支（`main`）状态。  
- **SKILL.md 文件未更新**：只有当文件中包含 `---` 标签之间的 YAML 格式 `version:` 字段时，才会被更新。  

## MCP（Mission Control Panel）相关工具  
- `release`、`release_status`：用于管理发布流程的工具  

**配置说明：**  
请将以下配置添加到 `.mcp.json` 文件中：  
（此处可添加 MCP 相关的配置信息）