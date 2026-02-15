---
name: openclaw-security
description: "这是一个统一的安全套件，专为代理工作空间设计。它通过一个命令即可完成所有11个OpenClaw安全工具的安装、配置和协调工作，这些工具包括：数据完整性保护、密钥管理、权限控制、网络安全、审计追踪、签名验证、供应链安全、身份认证管理、注入防御、合规性检查以及事件响应机制。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🔒","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw 安全套件

这是一个用于安装、配置和协调整个 OpenClaw 安全解决方案的工具。

## 安装所有安全工具

```bash
python3 {baseDir}/scripts/security.py install --workspace /path/to/workspace
```

通过 ClawHub 安装全部 11 个免费的安全工具。

## 统一仪表盘

```bash
python3 {baseDir}/scripts/security.py status --workspace /path/to/workspace
```

汇总所有已安装安全工具的运行状态（健康检查）。

## 全面安全扫描

```bash
python3 {baseDir}/scripts/security.py scan --workspace /path/to/workspace
```

运行所有安全扫描工具：完整性验证、秘密信息检测、权限审计、网络数据丢失防护（DLP）、供应链分析、注入攻击检测、凭证泄露检测以及合规性审计。

## 首次设置

```bash
python3 {baseDir}/scripts/security.py setup --workspace /path/to/workspace
```

初始化所有需要的工具：设置完整性基准、工具签名机制、审计记录以及合规性策略。

## 更新所有工具

```bash
python3 {baseDir}/scripts/security.py update --workspace /path/to/workspace
```

通过 ClawHub 将所有已安装的安全工具更新至最新版本。

## 列出已安装的工具

```bash
python3 {baseDir}/scripts/security.py list --workspace /path/to/workspace
```

显示已安装的安全工具及其版本信息。

## 专业级防护扫描

```bash
python3 {baseDir}/scripts/security.py protect --workspace /path/to/workspace
```

在所有已安装的专业级（Pro）工具上运行自动化防护措施。需要使用专业级版本。

## 被协调的工具及功能

| 工具        | 功能领域        | 免费版本 | 专业版本 |
|-------------|--------------|---------|---------|
| **warden**     | 工作区完整性检测、注入攻击检测 | 支持检测 | 支持恢复、回滚、隔离 |
| **sentry**     | 秘密信息/凭证扫描      | 支持检测 | 支持删除、隔离 |
| **arbiter**     | 权限审计        | 支持检测 | 支持撤销、强制执行 |
| **egress**     | 网络数据丢失防护（DLP）、数据泄露检测 | 支持检测 | 支持阻止、允许列表设置 |
| **ledger**     | 哈希链审计追踪      | 支持记录 | 支持冻结、取证分析 |
| **signet**     | 加密工具签名      | 支持验证 | 支持拒绝、恢复 |
| **sentinel**    | 供应链安全扫描     | 支持扫描 | 支持隔离、阻止 |
| **vault**     | 凭证生命周期管理    | 支持审计 | 支持修复、轮换 |
| **bastion**     | 即时注入攻击防御    | 支持扫描 | 支持清理、强制执行 |
| **marshal**     | 合规性/策略执行     | 支持审计 | 支持强制执行、挂钩设置 |
| **triage**     | 事件响应与取证分析   | 支持调查 | 支持遏制、修复 |

## 系统要求

- Python 3.8 及以上版本
- 无外部依赖项（仅需要标准库）
- 跨平台支持：Windows、macOS、Linux