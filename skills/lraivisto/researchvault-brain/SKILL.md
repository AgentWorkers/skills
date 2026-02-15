---
name: vault
description: "本地研究协调与状态管理功能。适用于项目启动、进度记录或研究成果导出等场景。"
---

# Vault

这是一个用于管理长时间运行的研究任务的本地编排引擎，具有高可靠性和零外部成本的特点。

## 核心概念

- **Vault**：一个存储在 `~/.researchvault/` 目录中的本地 SQLite 数据库（可通过 `RESEARCHVAULT_DB` 配置）。
- **项目（Project）**：一个高层次的研究目标。
- **数据记录（Instrumentation）**：每个事件都会记录其置信度（0.0-1.0）、来源和标签。

## 工作流程

### 1. 初始化项目
```bash
python3 scripts/vault.py init --id "proj-v1" --objective "Project goal"
```

### 2. 多源研究
使用带有 SSRF 保护的统一 scuttle 命令：
```bash
python3 scripts/vault.py scuttle "https://example.com" --id "proj-v1"
```

### 3. 监控与总结
```bash
python3 scripts/vault.py summary --id "proj-v1"
python3 scripts/vault.py status --id "proj-v1"
```

### 4. 导出数据
```bash
python3 scripts/vault.py export --id "proj-v1" --format markdown --output summary.md
```

## 维护

该数据库是本地的，不包含在版本控制系统中。