---
name: marketplace-publishing
description: Claude Code市场发布功能包括：通过npm进行发布、在GitHub上上传代码、使用语义化版本控制（semantic versioning）以及插件打包（plugin packaging）。这些功能专门用于插件（plugins）的发布过程。
---

# 市场发布专家

提供关于如何将 Claude Code 插件发布到 npm 和相关市场的专业指导。

## 发布平台

**1. GitHub**（推荐）：
```bash
# Install from GitHub
claude plugin add github:username/plugin-name

# Pros:
- Free hosting
- Version control
- Issue tracking
- Easy updates

# Requirements:
- Public repository
- Proper directory structure
- README with installation
```

**2. npm**：
```bash
# Install from npm
claude plugin add plugin-name

# Pros:
- Centralized registry
- Semantic versioning
- Easy discovery

# Requirements:
- npm account
- package.json
- Unique name (prefix: claude-plugin-)
```

**3. 市场平台**：
```bash
# Official Claude Code marketplace
# PR to marketplace repository

# Requirements:
- Quality standards
- Complete documentation
- No security issues
- Proper licensing
```

## 语义版本控制

**版本格式**：`MAJOR.MINOR.PATCH`

**规则**：
```yaml
MAJOR (1.0.0 → 2.0.0):
  - Breaking changes
  - Remove commands
  - Change skill keywords
  - Incompatible API changes

MINOR (1.0.0 → 1.1.0):
  - New features
  - Add commands
  - Add skills
  - Backward compatible

PATCH (1.0.0 → 1.0.1):
  - Bug fixes
  - Documentation updates
  - Performance improvements
  - No API changes
```

**示例**：
```bash
# Bug fix
npm version patch  # 1.0.0 → 1.0.1

# New feature
npm version minor  # 1.0.1 → 1.1.0

# Breaking change
npm version major  # 1.1.0 → 2.0.0
```

## package.json 配置

**最低要求**：
```json
{
  "name": "claude-plugin-my-plugin",
  "version": "1.0.0",
  "description": "Expert [domain] plugin for Claude Code",
  "keywords": ["claude-code", "plugin", "keyword1"],
  "author": "Your Name",
  "license": "MIT",
  "files": [
    ".claude-plugin",
    "commands",
    "skills",
    "agents",
    "README.md",
    "LICENSE"
  ]
}
```

**完整配置**：
```json
{
  "name": "claude-plugin-my-plugin",
  "version": "1.0.0",
  "description": "Expert [domain] plugin with [features]",
  "main": "index.js",
  "scripts": {
    "test": "echo \"No tests yet\"",
    "validate": "bash validate.sh"
  },
  "keywords": [
    "claude-code",
    "plugin",
    "development-tools",
    "keyword1",
    "keyword2"
  ],
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/username/my-plugin"
  },
  "homepage": "https://github.com/username/my-plugin#readme",
  "bugs": {
    "url": "https://github.com/username/my-plugin/issues"
  },
  "files": [
    ".claude-plugin/**/*",
    "commands/**/*",
    "skills/**/*",
    "agents/**/*",
    "README.md",
    "LICENSE"
  ]
}
```

## 发布工作流程

**在 GitHub 上发布**：
```bash
# 1. Update version
npm version patch

# 2. Commit changes
git add .
git commit -m "Release v1.0.1"

# 3. Create tag
git tag v1.0.1

# 4. Push
git push && git push --tags

# 5. Create GitHub release
gh release create v1.0.1 \
  --title "v1.0.1" \
  --notes "Bug fixes and improvements"
```

**通过 npm 发布**：
```bash
# 1. Login
npm login

# 2. Validate package
npm pack --dry-run

# 3. Publish
npm publish

# 4. Verify
npm view claude-plugin-my-plugin
```

## 文档要求

**README.md**：
```markdown
# Plugin Name

> One-line tagline

Brief description.

## Features

- Feature 1
- Feature 2

## Installation

\```
bash
claude plugin add github:user/plugin
\```

## Commands

### /plugin:command

Description.

## Examples

[Working examples]

## License

MIT
```

**CHANGELOG.md**：
```markdown
# Changelog

## [1.0.1] - 2025-01-15

### Fixed
- Bug fix 1
- Bug fix 2

## [1.0.0] - 2025-01-01

### Added
- Initial release
```

## 质量检查清单

**发布前**：
- ✅ 所有命令都能正常运行
- ✅ 插件功能能够正确激活
- ✅ 不存在硬编码的敏感信息（如密码等）
- ✅ README 文件中包含使用示例
- ✅ 有完整的 LICENSE 文件
- ✅ 使用语义版本控制
- ✅ CHANGELOG 文件已更新
- ✅ 已创建 Git 标签

**发布后**：
- ✅ 测试插件的安装过程
- ✅ 在 npm 上验证插件的可用性
- ✅ 检查 GitHub 上的发布信息
- ✅ （如适用）更新市场平台上的信息

发布专业的 Claude Code 插件吧！