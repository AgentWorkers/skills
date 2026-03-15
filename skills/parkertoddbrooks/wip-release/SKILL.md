---
name: wip-release
description: >
  单命令发布流程：  
  1. 提升版本号；  
  2. 更新变更日志（changelog）和 SKILL.md 文件；  
  3. 将更新内容发布到 npm 和 GitHub。
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

这是一个用于本地发布的自动化脚本。通过一个命令即可完成版本更新、所有文档的更新以及内容的发布。

## 适用场景

**适用于：**
- 发布任何 @wipcomputer 包的新版本
- 在将 PR 合并到主分支（main）后需要立即发布新版本时
- 一步完成版本更新、更新日志（changelog）以及 SKILL.md 文件的更新

**使用 --dry-run 的场景：**
- 在提交代码之前预览发布过程

**使用 --no-publish 的场景：**
- 仅更新版本和添加标签，但不将内容发布到注册中心（registries）

### 不适用场景

- 预发布/测试版本（目前不支持）
- 没有 `package.json` 文件的仓库

## API 参考

### 命令行接口（CLI）

```bash
wip-release patch --notes="fix X"           # full pipeline
wip-release minor --dry-run                 # preview only
wip-release major --no-publish              # bump + tag only
wip-release patch --skip-product-check      # skip product docs gate
```

### 产品文档检查机制

在发布之前，wip-release 会检查产品文档（包括开发更新信息、路线图以及用户手册）是否已经更新。该脚本仅适用于包含 `ai/` 目录的仓库。

- **patch**：如果产品文档过时，会发出警告（此操作不会阻止发布流程）
- **minor/major**：在产品文档更新完成前，会阻止发布
- **--skip-product-check**：跳过文档检查步骤

检查内容：
1. `ai/dev-updates/` 目录中是否有自上次发布以来被修改的文件
2. `ai/product/plans-prds/roadmap.md` 是否自上次发布以来被修改
3. `ai/product/readme-first-product.md` 是否自上次发布以来被修改

### 文档发布到网站

发布完成后，wip-release 会自动将 SKILL.md 文件作为纯文本复制到你的网站。任何访问网站的用户都可以通过该 URL 获取安装说明。

**配置方法：** 在仓库根目录下添加 `.publish-skill.json` 文件：
```json
{ "name": "wip-my-tool", "websiteRepo": "/path/to/website-repo" }
```

**工作原理：**
1. 如果存在 SKILL.md 文件且配置了网站仓库，脚本会将文件复制到 `{website}/wip.computer/install/{name}.txt` 路径下
2. 在网站仓库中运行 `deploy.sh` 命令以完成部署
3. 此过程是非阻塞的：即使部署失败，发布操作仍会继续执行

**网站仓库的确定方式：**
- 通过 `.publish-skill.json` 文件中的 `websiteRepo` 字段（针对每个仓库）
- 或者使用环境变量 `WIP_WEBSITE_REPO`（作为全局备用方案）

**名称确定方式（优先级从高到低）：**
- `.publish-skill.json` 文件中的 `name` 字段
- `package.json` 文件中的名称（去除 `@scope/` 前缀）
- 文件所在的目录名称（去除 `-private` 后缀）

### 模块相关设置

```javascript
import { release, detectCurrentVersion, bumpSemver, syncSkillVersion } from '@wipcomputer/wip-release';

await release({ repoPath: '.', level: 'patch', notes: 'fix', dryRun: false, noPublish: false });
```

## 常见问题排查

- **“无法从 1Password 获取 npm 令牌”**：请确认 `~/.openclaw/secrets/op-sa-token` 文件存在，并且已安装 `op` CLI 工具。
- **“推送失败”**：可能是分支保护机制导致的。请确保在合并 PR 后处于主分支（main）。
- **SKILL.md 未更新**：只有当文件中包含 YAML 格式的 `version:` 字段（位于 `---` 标签之间）时，才会触发更新。

## MCP 相关工具

相关工具：`release`、`release_status`

请将这些工具的配置信息添加到 `.mcp.json` 文件中：
```json
{
  "wip-release": {
    "command": "node",
    "args": ["/path/to/tools/wip-release/mcp-server.mjs"]
  }
}
```