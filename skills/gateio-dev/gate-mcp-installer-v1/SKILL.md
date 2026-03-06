---
name: gate-mcp-installer
version: "2026.3.4-1"
updated: "2026-03-04"
description: >
  OpenClaw 中的 Gate MCP (mcporter) 一键安装和配置工具。适用于用户需要执行以下操作的情况：  
  1. 安装 mcporter CLI 工具；  
  2. 配置 Gate MCP 服务器连接；  
  3. 验证 Gate MCP 的设置是否正确；  
  4. 故障排除 Gate MCP 的连接问题。
---
# Gate MCP 安装器

用于在 OpenClaw 中一键安装 Gate MCP (mcporter)。

## 快速入门

要安装 Gate MCP，请运行安装脚本：

```bash
bash ~/.openclaw/skills/gate-mcp-installer/scripts/install-gate-mcp.sh
```

或者直接执行该技能，我会指导您完成安装过程。

## 该技能的功能

该技能可自动化完成 Gate MCP 的整个安装过程：

1. 通过 npm 全局安装 mcporter CLI；
2. 配置 Gate MCP 服务器及其正确的端点；
3. 通过列出可用的工具来验证连接是否正常；
4. 提供常见查询的使用示例。

## 手动安装步骤（如果脚本失败）

### 第一步：安装 mcporter

```bash
npm i -g mcporter
# Or verify installation
npx mcporter --version
```

### 第二步：配置 Gate MCP

```bash
mcporter config add gate https://api.gatemcp.ai/mcp --scope home
```

### 第三步：验证配置

```bash
# Check config is written
mcporter config get gate

# List available tools
mcporter list gate --schema
```

如果列出了可用的工具，那么 Gate MCP 就已经可以使用了！

## 常见使用示例

安装完成后，可以使用 Gate MCP 进行以下查询：

- “检查 BTC/USDT 的价格”
- “使用 gate mcp 分析 SOL”
- “Gate 上有哪些套利机会？”
- “检查 ETH 的融资费率”

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| “找不到 mcporter 命令” | 运行 `npm i -g mcporter` |
| 配置信息未找到 | 重新运行 `config add` 命令 |
| 连接超时 | 检查到 fulltrust.link 的网络连接是否正常 |
| 未列出任何工具 | 确认配置 URL 是否正确 |

## 资源

- **安装脚本**：`scripts/install-gate-mcp.sh` – 自动化的一键安装工具