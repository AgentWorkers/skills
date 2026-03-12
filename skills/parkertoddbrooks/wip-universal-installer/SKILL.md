---
name: wip-universal-installer
description: 用于 agent-native 软件的参考安装程序。该程序会扫描代码仓库（repo），检测该软件暴露出的所有接口（interfaces），并逐一安装这些接口。
license: MIT
interface: [cli, module, skill]
metadata:
  display-name: "Universal Installer"
  version: "2.1.5"
  homepage: "https://github.com/wipcomputer/wip-universal-installer"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - detect-interfaces
    - install-cli
    - install-mcp
    - install-openclaw-plugin
    - install-claude-code-hook
  requires:
    bins: [node, npm, git]
  openclaw:
    requires:
      bins: [node, npm, git]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/universal-installer"
        bins: [wip-install]
        label: "Install via npm"
    emoji: "🔌"
compatibility: Requires git, npm, node. Node.js 18+.
---
# wip-universal-installer

这是一个用于代理原生软件的参考安装工具。它会扫描代码仓库（repo），检测其中暴露的接口，并将所有这些接口安装到目标系统中。

## 适用场景

**使用 wip-universal-installer 的场景：**
- 安装遵循“通用接口”（Universal Interface）规范的代码仓库
- 检测代码仓库所提供的接口
- 通过一个命令同时配置 CLI 工具、MCP 服务器、OpenClaw 插件以及 Claude 代码钩子（Claude Code Hooks）

**使用 detect.mjs 的场景：**
- 以编程方式检测代码仓库中的接口
- 构建自定义安装程序或持续集成（CI）流程
- 验证代码仓库是否符合相关规范

### 不适用场景

- 安装标准的 npm 包（请直接使用 npm）
- 不遵循“通用接口”规范的代码仓库
- 编译或构建代码（该工具仅用于安装操作）

## API 参考

### 命令行接口（CLI）

```bash
wip-install /path/to/repo           # install all interfaces
wip-install org/repo                 # clone from GitHub + install
wip-install --dry-run /path/to/repo  # detect only, no changes
wip-install --json /path/to/repo     # JSON output
```

### 检测模块（detect.mjs）

```javascript
import { detectInterfaces, describeInterfaces, detectInterfacesJSON } from './detect.mjs';

const { interfaces, pkg } = detectInterfaces('/path/to/repo');
console.log(describeInterfaces(interfaces));

const json = detectInterfacesJSON('/path/to/repo');
console.log(JSON.stringify(json, null, 2));
```

## 通用接口规范

详细规范请参阅 [SPEC.md](https://github.com/wipcomputer/wip-universal-installer/blob/main/SPEC.md)：
1. **命令行接口（CLI）**：参考 `package.json` 文件中的 `bin` 字段
2. **检测模块（Module）**：参考 `package.json` 文件中的 `main` 和 `exports` 属性
3. **MCP 服务器（MCP Server）**：参考 `mcp-server.mjs` 文件
4. **OpenClaw 插件（OpenClaw Plugin）**：参考 `openclaw.plugin.json` 文件
5. **技能文件（Skill）**：参考 `SKILL.md` 文件
6. **Claude 代码钩子（Claude Code Hook）**：参考 `guard.mjs` 或 `claudeCode.hook` 文件