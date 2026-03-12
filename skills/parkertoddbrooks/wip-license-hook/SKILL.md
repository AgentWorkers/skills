---
name: wip-license-hook
description: >
  **许可证变更检测功能**：  
  该功能会扫描项目所依赖的库和分支，以检测许可证是否发生变更；在允许上游代码合并之前进行审核；维护一个许可证变更的记录数据库（许可证账本），并生成一个公开的合规性监控仪表板。
license: MIT
interface: [cli, module, mcp]
metadata:
  display-name: "License Rug-Pull Detection"
  version: "1.0.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - license-scanning
    - rug-pull-detection
    - compliance-gating
    - license-ledger
  requires:
    bins: [node, git, npm]
  openclaw:
    requires:
      bins: [node, git, npm]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-license-hook"
        bins: [wip-license-hook]
        label: "Install via npm"
    emoji: "🛡️"
compatibility: Requires git, npm, node. Node.js 18+.
---
# wip-license-hook  
在许可证信息被篡改之前及时发现并预警。  

## 命令  

### 为项目初始化许可证信息记录  
```bash
wip-license-hook init --repo /path/to/repo
```  
扫描所有当前的依赖项及其分支，记录它们的许可证信息，并生成 `LICENSE-LEDGER.json` 文件。  

### 扫描所有依赖项  
```bash
wip-license-hook scan --all
```  
将每个依赖项及其分支与许可证信息记录进行比对，更新 `last_checked` 的值，并标记任何变化。  

### 合并前检查  
```bash
wip-license-hook gate --upstream <remote>
```  
获取上游代码的许可证信息（但不进行合并操作）。返回退出码 0 表示“安全”，返回码 1 表示“许可证信息已更改或被阻止”。  
可用于 Git 钩子（git hooks）或持续集成（CI）流程中。  

### 生成报告  
```bash
wip-license-hook report
```  
输出一份易于阅读的许可证状态报告。  

### 生成仪表盘  
```bash
wip-license-hook dashboard --output ./docs
```  
根据许可证信息记录生成静态 HTML 仪表盘，并部署到 GitHub Pages 上。  

## 日常 Cron 任务使用方法  
将相关命令添加到 `HEARTBEAT.md` 文件中，或设置为 Cron 作业：  
```
wip-license-hook scan --all --alert
```  

**当许可证信息发生变化时，** 会通过配置的渠道（电子邮件、iMessage 或 Discord）发送警报。  

## 检测内容：  
- `LICENSE` 文件内容的变更  
- `package.json` 中的许可证字段变更  
- SPDX 标头的变更  
- 许可证的移除（文件被删除）  
- 许可证权限的降低（从宽松变为严格）  

## 不会执行的功能：  
- 不提供法律建议  
- 从不自动合并任何代码  
- 不会修改上游代码  

## 警报等级：  
- 🟢 **正常** — 自项目采用许可证以来未发生变更  
- 🟡 **警告** — 许可证元数据不一致（例如，`LICENSE` 文件声明使用 MIT 许可证，但 `package.json` 声明使用 ISC 许可证）  
- 🔴 **阻止** — 许可证信息与最初采用的版本不同，合并操作被阻止，需要人工审核。  

## 所使用的工具：  
`license_scan`、`license_audit`、`license_gate`、`license_ledger`  

**将这些工具添加到 `.mcp.json` 文件中：**  
```json
{
  "wip-license-hook": {
    "command": "node",
    "args": ["/path/to/tools/wip-license-hook/mcp-server.mjs"]
  }
}
```