---
name: openclaw-egress-pro
description: "**全套网络数据泄露防护（DLP）解决方案：**  
能够检测出外发的URL、数据泄露行为以及可疑的网络通信请求，随后自动阻断相关连接、隔离被入侵的技能（系统组件），并强制执行域名白名单规则。该方案包含 openclaw-egress（免费版本）中的所有功能，同时还提供了自动化应对措施。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Egress Pro

这是一个专为代理工作空间设计的全功能网络数据丢失防护（DLP）解决方案。它能够检测出外发的URL、数据泄露行为以及可疑的网络请求，然后自动阻断这些连接，隔离被入侵的脚本，并执行域名白名单管理。

**工作原理：** 首先发出警报，接着采取应对措施，随后将受感染的脚本隔离，最后进行防御。

[openclaw-egress](https://github.com/AtlasPA/openclaw-egress)（免费版本）的所有功能基础上，还增加了自动化防护机制。

## 问题所在

被入侵的脚本可能会将工作空间的内容、API密钥或对话记录发送到外部服务器。仅仅依靠检测是不够的，还需要具备自动应对威胁的能力。

## 命令

### 全面扫描

扫描工作空间中的所有网络风险。

```bash
python3 {baseDir}/scripts/egress.py scan --workspace /path/to/workspace
```

### 仅扫描脚本

```bash
python3 {baseDir}/scripts/egress.py scan --skills-only --workspace /path/to/workspace
```

### 域名映射

列出工作空间中引用的所有外部域名。

```bash
python3 {baseDir}/scripts/egress.py domains --workspace /path/to/workspace
```

### 快速状态检查

```bash
python3 {baseDir}/scripts/egress.py status --workspace /path/to/workspace
```

## 高级防护措施

### 阻止网络请求

通过注释的方式屏蔽可疑的网络请求。仅针对“CRITICAL”（严重）和“HIGH”（高风险）级别的风险进行操作。修改后的文件会自动创建备份（`.bak`文件）。

```bash
python3 {baseDir}/scripts/egress.py block <skill-name> --workspace /path/to/workspace
```

- 使用 `# [BLOCKED by openclaw-egress-pro]` 对包含网络请求的代码行进行注释屏蔽
- 在修改任何文件之前会创建备份文件
- 仅修改代码文件（`.py`、`.js`、`.ts`、`.sh`、`.bash`）
- 将非代码文件标记为需要手动审核

### 隔离脚本

通过重命名受感染的脚本来禁用它们，从而防止OpenClaw加载这些脚本。

```bash
python3 {baseDir}/scripts/egress.py quarantine <skill-name> --workspace /path/to/workspace
```

### 解除隔离

恢复之前被隔离的脚本。

```bash
python3 {baseDir}/scripts/egress.py unquarantine <skill-name> --workspace /path/to/workspace
```

### 域名白名单

管理自定义的域名白名单。列表中的域名在扫描过程中不会被标记为风险。系统内置的安全域名始终有效。

```bash
# Show current allowlist (built-in + custom)
python3 {baseDir}/scripts/egress.py allowlist --workspace /path/to/workspace

# Add a domain
python3 {baseDir}/scripts/egress.py allowlist --add api.mycompany.com --workspace /path/to/workspace

# Remove a domain
python3 {baseDir}/scripts/egress.py allowlist --remove api.mycompany.com --workspace /path/to/workspace
```

自定义白名单存储在工作空间根目录下的 `.egress-allowlist.json` 文件中。

### 自动防护（全面扫描）

执行自动防护操作：扫描所有脚本，自动隔离存在“CRITICAL”级别数据泄露风险的脚本，阻断“HIGH”级别风险的网络请求，并报告扫描结果。建议在会话启动时使用此功能。

```bash
python3 {baseDir}/scripts/egress.py protect --workspace /path/to/workspace
```

**自动防护功能的操作步骤：**
1. 扫描所有未处于隔离状态的脚本
2. 对于“CRITICAL”级别的风险，隔离整个脚本
3. 对于“HIGH”级别的风险，屏蔽相关的网络请求代码行
4. 报告所有操作内容及后续处理步骤

## 检测内容

| 风险类型 | 检测模式 |
|------|---------|
| **CRITICAL** | URL中的Base64/十六进制数据、Pastebin/共享服务、请求拦截器、动态DNS |
| **HIGH** | 网络函数调用（如requests、urllib、curl、wget、fetch）、Webhook回调URL |
| **WARNING** | 可疑的顶级域名（.xyz、.tk、.ml）、URL缩短服务、IP地址端点 |
| **INFO** | 任何不在安全域名列表或自定义白名单中的外部URL |

## 返回码

- `0` — 无风险（或操作成功完成）
- `1` — 检测到警告/网络请求（需要进一步审核）
- `2` — 检测到严重的数据泄露风险（需要采取行动）

## 无外部依赖

仅使用Python标准库，无需安装任何第三方库（如pip），也不进行任何网络请求。所有操作都在本地执行。

## 跨平台兼容性

支持OpenClaw、Claude Code、Cursor以及任何遵循“Agent Skills”规范的工具。