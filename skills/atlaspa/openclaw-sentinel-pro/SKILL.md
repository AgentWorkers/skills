---
name: openclaw-sentinel-pro
description: "完整的供应链安全解决方案：扫描代码中用于混淆和传播恶意软件的技巧（即“技巧”），自动隔离存在风险的代码片段，生成软件成分清单（SBOMs），实现持续监控，并提供来自社区的威胁信息。这些功能均包含在 openclaw-sentinel（免费版本）中，同时还提供了自动化对策。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🏰","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Sentinel Pro

[openclaw-sentinel](https://github.com/AtlasPA/openclaw-sentinel)（免费版）的所有功能，外加自动化防护措施。

**免费版仅能检测威胁；Pro版则能主动应对、隔离威胁并进行防御。**

## 检测命令（免费版也提供）

### 扫描已安装的技能

深度扫描所有已安装的技能，检测供应链风险。将文件哈希与本地威胁数据库进行比对，识别混淆的代码模式、可疑的安装行为、依赖关系混乱以及元数据不一致的问题。为每个技能生成一个风险评分（0-100分）。

```bash
python3 {baseDir}/scripts/sentinel.py scan --workspace /path/to/workspace
```

### 扫描单个技能

```bash
python3 {baseDir}/scripts/sentinel.py scan openclaw-warden --workspace /path/to/workspace
```

### 安装前检查

在将技能复制到工作区之前，对其进行扫描。系统会给出“安全”、“需要审查”或“拒绝”的建议，并详细显示该技能将执行的二进制文件、网络调用和文件操作。

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

### 快速状态概览

显示已安装的技能、被隔离的技能、扫描历史记录、软件成分清单（SBOM）以及风险评分的总体情况。

```bash
python3 {baseDir}/scripts/sentinel.py status --workspace /path/to/workspace
```

## Pro版防护措施

### 隔离技能

通过将技能目录重命名为带有“.quarantined-”前缀的方式来禁用该技能。代理程序将不会加载被隔离的技能。所有相关证据（发现结果、文件清单、哈希值）会被记录在`.quarantine/sentinel/{skill}-evidence.json`文件中。

```bash
python3 {baseDir}/scripts/sentinel.py quarantine bad-skill --workspace /path/to/workspace
```

### 解除隔离

在调查后恢复被隔离的技能。在恢复之前会显示原始的隔离证据。

```bash
python3 {baseDir}/scripts/sentinel.py unquarantine bad-skill --workspace /path/to/workspace
```

### 拒绝技能

永久移除风险评分高于50分的技能。这些技能会被移至`.quarantine/sentinel/`目录以供进一步审查，但不会被删除。评分低于阈值的技能则建议使用隔离措施。

```bash
python3 {baseDir}/scripts/sentinel.py reject bad-skill --workspace /path/to/workspace
```

### 生成软件成分清单（SBOM）

为所有已安装的技能生成软件成分清单（SBOM），包括文件清单及其SHA-256哈希值、声明的依赖关系和检测到的依赖关系。结果保存在`.sentinel/sbom-{timestamp}.json`文件中。

```bash
python3 {baseDir}/scripts/sentinel.py sbom --workspace /path/to/workspace
```

### 持续监控

将当前扫描结果与上一次扫描结果进行比较，报告新出现的威胁、风险评分的变化、新增或被移除/隔离的技能。扫描结果会保存在`.sentinel/scans/`目录中以供历史记录。

```bash
python3 {baseDir}/scripts/sentinel.py monitor --workspace /path/to/workspace
```

### 自动防护（一键操作）

通过一个命令完成全部自动化防护流程：扫描所有技能，自动隔离风险等级为75分及以上的技能，生成软件成分清单（SBOM），更新扫描历史记录，并生成防护报告。这是启动会话时的推荐命令。

```bash
python3 {baseDir}/scripts/sentinel.py protect --workspace /path/to/workspace
```

## 推荐的集成方式

### 会话启动钩子（Claude Code）

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/sentinel.py protect",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 定期防护机制（OpenClaw）

将相关代码添加到`HEARTBEAT.md`文件中，以实现定期防护：

```
- Run supply chain protection sweep (python3 {skill:openclaw-sentinel-pro}/scripts/sentinel.py protect)
```

### 安装新技能后

运行`protect`命令，自动隔离含有恶意代码的技能。

## 工作区自动检测

如果省略`--workspace`参数，脚本会尝试以下路径：
1. `OPENCLAW_WORKSPACE`环境变量
2. 当前目录（如果存在`AGENTS.md`文件）
3. `~/.openclaw/workspace`（默认路径）

## 检测内容

| 类别 | 检测模式 |
|----------|----------|
| **编码执行** | `eval(base64.b64decode(...))`, `exec(compile(...))`, 使用编码字符串执行的命令 |
| **动态导入** | `import('os').system(...)`、动态导入`subprocess`或`ctypes` |
| **Shell注入** | 使用`subprocess.Popen`且`shell=True`结合字符串拼接、`os.system()` |
| **远程代码执行** | `urllib/requests`与`exec/eval`结合使用（用于下载并执行代码） |
| **代码混淆** | 长度超过1000个字符的代码行、高熵字符串、压缩后的代码块 |
| **安装行为** | 安装后的钩子脚本、在`_init_.py`文件中的自动执行、跨技能间的文件写入 |
| **隐藏文件** | 非标准的`.dot`文件和隐藏目录 |
| **依赖关系混乱** | 技能文件名称与流行软件包名称相似、存在拼写错误 |
| **元数据不一致** | 未声明的二进制文件、未声明的环境变量、可执行标志的不一致 |
| **序列化问题** | `pickle.loads`, `marshal.loads`——通过反序列化执行任意代码 |
| **已知恶意哈希** | 文件的SHA-256哈希值与本地威胁数据库中的恶意哈希匹配 |

## 风险评分

每个技能都会获得0-100分的评分：

| 评分 | 分类 | 含义 |
|-------|-------|---------|
| 0 | 无问题 | 未检测到任何风险 |
| 1-19 | 低风险 | 发现了小问题，可能是良性的 |
| 20-49 | 中等风险 | 建议进行审查 |
| 50-74 | 高风险 | 需要立即处理 |
| 75-100 | 严重风险 | 极高的供应链风险，系统会自动将其隔离 |

## 防护措施概览

| 命令 | 功能 |
|---------|--------|
| `protect` | 全面扫描 + 自动隔离高风险技能 + 生成软件成分清单 + 生成报告 |
| `quarantine <技能>` | 禁用该技能并记录相关证据 |
| `unquarantine <技能>` | 恢复被隔离的技能 |
| `reject <技能>` | 永久移除高风险技能 |
| `sbom` | 生成软件成分清单 |
| `monitor` | 比较当前扫描结果与上一次扫描结果，报告变化 |

## 错误代码

- `0`：一切正常，无问题 |
- `1`：需要审查 |
- `2`：检测到威胁或技能已被隔离 |

## 无外部依赖

仅使用Python标准库，无需安装额外的依赖包（如pip），也不进行网络调用。所有操作都在本地完成。

## 跨平台兼容性

支持OpenClaw、Claude Code、Cursor以及任何遵循“Agent Skills”规范的工具。