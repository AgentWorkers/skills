---
name: openclaw-arbiter
user-invocable: true
metadata: {"openclaw":{"emoji":"⚖️","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Arbiter

OpenClaw Arbiter 会审计已安装的技能（skills），以准确报告每个技能所使用的系统资源——包括网络资源、子进程、文件读写操作、环境变量以及可能存在安全风险的操作。

## 问题所在

用户通常会盲目地安装各种技能，而对这些技能的实际行为缺乏了解。例如，一个声称用于格式化 Markdown 的技能，实际上也可能用于建立网络连接、执行 shell 命令或读取用户的环境变量。目前没有任何工具能够报告每个技能实际使用了哪些权限。

## 命令

### 全面审计（Full Audit）

对所有已安装的技能进行深度审计，并提供详细的审计结果（到行级别）。

```bash
python3 {baseDir}/scripts/arbiter.py audit --workspace /path/to/workspace
```

### 单个技能审计（Audit Single Skill）

```bash
python3 {baseDir}/scripts/arbiter.py audit openclaw-warden --workspace /path/to/workspace
```

### 权限矩阵（Permission Matrix）

以简洁的表格形式展示每个技能的权限类别。

```bash
python3 {baseDir}/scripts/arbiter.py report --workspace /path/to/workspace
```

### 快速状态检查（Quick Status）

以一行文字的形式概括每个技能的权限风险情况。

```bash
python3 {baseDir}/scripts/arbiter.py status --workspace /path/to/workspace
```

## 检测内容

| 权限类别 | 风险等级 | 示例 |
|----------|------|----------|
| **序列化（Serialization）** | 严重风险（CRITICAL） | pickle, eval(), exec(), __import__ |
| **子进程（Subprocess）** | 高风险（HIGH） | subprocess, os.system, Popen, 命令替换（command substitution） |
| **网络操作（Network）** | 高风险（HIGH） | urllib, requests, curl, wget, 硬编码的 URL（hardcoded URLs） |
| **文件写入（File Write）** | 中等风险（MEDIUM） | open('w'), shutil.copy, os.remove, rm |
| **环境变量（Environment）** | 中等风险（MEDIUM） | os.environ, os.getenv, os.putenv |
| **加密操作（Crypto）** | 低风险（LOW） | hashlib, hmac, ssl |
| **文件读取（File Read）** | 低风险（LOW） | open('r'), os.walk, glob |

## 返回码

- `0`：所有技能均正常使用，无权限问题 |
- `1`：检测到权限异常（需要审查） |
- `2`：检测到严重权限问题（需要采取行动） |

## 无外部依赖

仅使用 Python 标准库，无需通过 pip 安装任何第三方库，也不进行任何网络调用。所有操作都在本地执行。

## 跨平台兼容性

OpenClaw Arbiter 支持 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具。