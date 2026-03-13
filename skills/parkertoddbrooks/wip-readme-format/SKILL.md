---
name: wip-readme-format
description: 将任何仓库的 `README.md` 文件重新格式化，以符合 WIP Computer 的标准。
license: MIT
interface: [cli, skill]
metadata:
  display-name: "README Formatter"
  version: "1.0.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: repo-management
  capabilities:
    - readme-generation
    - readme-validation
    - section-staging
  requires:
    bins: [node]
  openclaw:
    requires:
      bins: [node]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-readme-format"
        bins: [wip-readme-format]
        label: "Install via npm"
    emoji: "📝"
compatibility: Requires node. Node.js 18+.
---
# README 格式化工具

该工具用于将仓库的 README 文件格式化，以符合 WIP Computer 的标准。优先考虑工具的可用性（Agent-first），同时确保内容易于人类阅读。

## 命令

```
wip-readme-format /path/to/repo              # rewrite README.md
wip-readme-format /path/to/repo --dry-run    # preview without writing
wip-readme-format /path/to/repo --check      # validate, exit 0/1
```

## 工作流程

1. 检测所有可用的接口（CLI、模块、MCP、OC 插件、技能、CC Hook）。
2. 从 `package.json` 文件中读取软件包的名称、描述以及仓库 URL。
3. 从 `SKILL.md` 文件中读取软件的功能信息。
4. 生成符合 WIP Computer 标准的 README 文件，内容包括：
   - WIP Computer 标头及相应的接口徽标
   - 标题和标语
   - “Teach Your AI” 的入门引导部分
   - 功能列表
   - 接口覆盖情况表（仅针对包含工具箱（toolbox）的仓库）
   - 更多信息链接
   - 许可证信息
5. 将所有技术性内容移至 `TECHNICAL.md` 文件中（这些内容不会被删除）。

## 标准要求

```
[badges]
# Tool Name
Tagline.

## Teach Your AI to [verb]
[onboarding prompt block]

## Features
[feature list]

## Interface Coverage (toolbox only)
[auto-generated table]

## More Info
- Technical Documentation ... link
- Universal Interface Spec ... link

## License
[standard block]
```

## 支持的接口类型

CLI（命令行接口）、Skill（技能相关接口）