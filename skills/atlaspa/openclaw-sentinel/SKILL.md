---
name: openclaw-sentinel
user-invocable: true
metadata: {"openclaw":{"emoji":"🏰","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Sentinel

这是一个用于检测代理技能（agent skills）中供应链安全问题的扫描工具。它能够在技能安装前后，识别出被混淆的代码、已知危险的签名、可疑的安装行为、依赖关系混乱以及元数据不一致等问题。

## 问题所在

您通常从社区中下载这些技能。任何技能都可能包含被混淆的负载（payloads）、安装后执行的脚本（post-install hooks），或者用于修改工作区中其他技能的供应链攻击。现有的工具只能在技能运行后验证文件的完整性，但无法在技能运行之前检测其中存在的供应链风险。

## 命令

### 扫描已安装的技能

对所有已安装的技能进行深度扫描，以检测供应链风险。该工具会将文件哈希值与本地威胁数据库进行比对，识别被混淆的代码模式、可疑的安装行为、依赖关系混乱以及元数据不一致的情况，并为每个技能生成一个风险评分（0-100分）。

```bash
python3 {baseDir}/scripts/sentinel.py scan --workspace /path/to/workspace
```

### 扫描单个技能

```bash
python3 {baseDir}/scripts/sentinel.py scan openclaw-warden --workspace /path/to/workspace
```

### 安装前检测

在将技能复制到工作区之前，对该技能目录进行扫描。系统会给出“SAFE”（安全）、“REVIEW”（需要审查）或“REJECT”（拒绝）的建议，并详细显示该技能将执行的二进制文件、网络请求和文件操作。

```bash
python3 {baseDir}/scripts/sentinel.py inspect /path/to/skill-directory
```

### 管理威胁数据库

查看当前的威胁数据库统计信息。

```bash
python3 {baseDir}/scripts/sentinel.py threats --workspace /path/to/workspace
```

导入社区共享的威胁列表。

```bash
python3 {baseDir}/scripts/sentinel.py threats --update-from threats.json --workspace /path/to/workspace
```

### 快速状态

提供已安装技能的概览、扫描历史记录以及风险评分的总结。

```bash
python3 {baseDir}/scripts/sentinel.py status --workspace /path/to/workspace
```

## 工作区自动检测

如果省略了 `--workspace` 参数，脚本会尝试以下路径来查找工作区位置：
1. `OPENCLAW_WORKSPACE` 环境变量
2. 当前目录（如果存在 `AGENTS.md` 文件）
3. `~/.openclaw/workspace`（默认路径）

## 可检测的问题类型

| 类别 | 典型特征 |
|----------|----------|
| **编码执行** | 使用 `eval(base64.b64decode(...))`、`exec(compile(...))` 等方式执行代码 |
| **动态导入** | 通过 `import('os').system(...)` 或 `dynamic subprocess/ctypes` 进行动态导入 |
| **Shell 注入** | 使用 `subprocess.Popen` 与字符串拼接来执行恶意代码 |
| **远程代码执行** | 结合 `urllib/requests` 和 `exec/eval` 来下载并执行恶意代码 |
| **代码混淆** | 代码行长度超过 1000 个字符、使用高熵字符串、代码被压缩 |
| **安装行为** | 安装后执行的脚本、在 `_init_.py` 文件中自动执行的代码、跨技能之间的文件写入 |
| **隐藏文件** | 非标准的 `.dot` 文件和隐藏目录 |
| **依赖关系混乱** | 技能名称与流行软件包名称相似、存在拼写错误 |
| **元数据不一致** | 未声明的二进制文件、未声明的环境变量、可执行标志的不一致 |
| **序列化问题** | 通过 `pickle.loads` 或 `marshal.loads` 导致任意代码执行 |
| **已知危险的哈希值** | 文件的 SHA-256 哈希值与本地威胁数据库中的恶意哈希值匹配 |

## 风险评分

每个技能的风险评分范围为 0-100 分：

| 评分 | 分类 | 含义 |
|-------|-------|---------|
| 0 | 清洁（CLEAN） | 未检测到任何问题 |
| 1-19 | 低风险（LOW） | 发现了一些小问题，可能是良性的 |
| 20-49 | 中等风险（MODERATE） | 建议进行审查 |
| 50-74 | 高风险（HIGH） | 存在重大风险，需要立即审查 |
| 75-100 | 临界风险（CRITICAL） | 存在严重的供应链风险 |

## 威胁数据库格式

社区共享的威胁列表采用以下 JSON 格式：

```json
{
  "hashes": {
    "<sha256hex>": {"name": "...", "severity": "...", "description": "..."}
  },
  "patterns": [
    {"name": "...", "regex": "...", "severity": "..."}
  ]
}
```

## 输出代码

- `0`：扫描完成，未发现任何问题 |
- `1`：需要审查技能 |
- `2`：检测到威胁 |

## 无外部依赖

该工具仅使用 Python 标准库，不依赖 `pip` 进行安装，也不进行任何网络请求，所有操作都在本地完成。

## 跨平台兼容性

该工具支持 OpenClaw、Claude Code、Cursor 以及任何遵循代理技能规范的工具。