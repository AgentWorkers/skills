---
name: openclaw-egress
user-invocable: true
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Egress

这是一个用于代理工作空间的网络数据泄露防护（Network DLP）工具，能够扫描技能（skills）和文件中的出站URL、数据泄露端点以及网络函数调用。

## 问题所在

某些技能（agents）可能存在安全风险：被入侵的技能可能会将工作空间内容、API密钥或对话记录发送到外部服务器。目前没有机制能够监控这些技能连接到哪些URL，或者它们可能传输哪些数据。

## 命令

### 全面扫描（Full Scan）

扫描工作空间中的所有出站网络风险。

```bash
python3 {baseDir}/scripts/egress.py scan --workspace /path/to/workspace
```

### 仅扫描技能（Skills-Only Scan）

```bash
python3 {baseDir}/scripts/egress.py scan --skills-only --workspace /path/to/workspace
```

### 域名映射（Domain Map）

列出工作空间中引用的所有外部域名。

```bash
python3 {baseDir}/scripts/egress.py domains --workspace /path/to/workspace
```

### 快速状态检查（Quick Status）

```bash
python3 {baseDir}/scripts/egress.py status --workspace /path/to/workspace
```

## 检测内容

| 风险等级 | 检测模式 |
|------|---------|
| **严重（CRITICAL）** | URL中的Base64或十六进制数据、Pastebin/分享服务、请求拦截器、动态DNS |
| **高风险（HIGH）** | 网络函数调用（如requests、urllib、curl、wget、fetch）、Webhook回调URL |
| **警告（WARNING）** | 可疑的顶级域名（.xyz、.tk、.ml）、URL缩短服务、IP地址端点 |
| **信息提示（INFO）** | 任何不在安全域名列表中的外部URL |

## 返回码

- `0` — 无风险
- `1` — 检测到网络请求（需要进一步审查）
- `2` — 检测到数据泄露风险（需要采取行动）

## 无外部依赖

仅使用Python标准库，无需安装任何第三方库（如pip），也不会进行任何网络请求。所有操作都在本地完成。

## 跨平台兼容性

支持OpenClaw、Claude Code、Cursor以及任何遵循“Agent Skills”规范的工具。