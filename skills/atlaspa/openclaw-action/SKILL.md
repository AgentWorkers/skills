---
name: openclaw-action
description: "GitHub Action：用于自动化扫描代理工作区的安全问题。能够检测到 Pull Requests（PRs）和代码提交（commits）中存在的敏感信息泄露、命令注入（prompt/shell injection）以及数据窃取（data exfiltration）等安全风险。"
user-invocable: false
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw 安全检查动作

这是一个 GitHub 动作，用于在每个 Pull Request（PR）中扫描代理技能（agent skills）中的安全问题。

## 扫描内容

| 扫描工具 | 扫描内容 |
|---------|-----------------|
| **sentry** | 代码中的 API 密钥、令牌、密码和凭证 |
| **bastion** | 提示注入（prompt injection）标记、shell 注入（shell injection）模式 |
| **egress** | 可疑的网络调用、数据泄露（data exfiltration）模式 |

## 快速入门

将以下代码添加到 `.github/workflows/security.yml` 文件中：

```yaml
name: Security Scan
on:
  pull_request:
    paths:
      - 'skills/**'
      - '.openclaw/**'
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: AtlasPA/openclaw-action@v1
        with:
          workspace: '.'
          fail-on-findings: 'true'
```

## 输入参数

| 参数 | 默认值 | 说明 |
|-------|---------|-------------|
| `workspace` | `.` | 需要扫描的目录路径 |
| `fail-on-findings` | `true` | 如果发现安全问题，则检查失败 |
| `scan-secrets` | `true` | 启用秘密信息扫描 |
| `scan-injection` | `true` | 启用注入攻击扫描 |
| `scan-egress` | `true` | 启用网络流量输出（egress traffic）扫描 |

## 输出结果

| 输出内容 | 说明 |
|--------|-------------|
| `findings-count` | 发现的安全问题总数 |
| `has-critical` | 如果存在严重/高严重级别的问题，则返回 `true` |

## 功能说明

此动作仅用于**检测和报警**。它将：
- 在 PR 检查过程中标记安全问题 |
- 在相关代码行上标注问题位置 |
- 生成汇总报告

**注意**：此动作不会：
- 自动修改您的代码 |
- 将文件隔离或删除 |
- 对您的仓库进行任何更改

如需自动修复安全问题，请参考 [OpenClaw Pro](https://github.com/sponsors/AtlasPA)。

## 系统要求

- Python 3.8 及以上版本（该动作会自动安装相应版本） |
- 无需任何外部依赖库