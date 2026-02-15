---
name: migrator
description: 将 OpenClaw Agent（包括配置文件、内存数据以及用户技能数据）安全地迁移到新机器上。
---

# OpenClaw Migrator

这是一个用于将代理（Agent）的状态打包成便携式、加密的归档文件（`.oca`）以方便迁移的工具。

## 特点

- **加密归档**：使用 AES-256-GCM 加密算法，并添加认证标签（auth tag）来确保数据的安全性和完整性。
- **路径规范化**：根据 `manifest.json` 元数据恢复工作区的路径。
- **依赖项清单**：记录系统的依赖关系（Brewfile），以确保新环境与旧环境一致。

## 使用方法

### 导出（在旧机器上）

```bash
migrator export --out my-agent.oca --password "secret"
```

### 导入（在新机器上）

```bash
migrator import --in my-agent.oca --password "secret"
```

## 安全性

该工具处理敏感数据（`openclaw.json`、`auth.token`）。  
导出过程 **始终** 需要密码来加密归档文件。  
设计上禁止生成未加密的导出文件。