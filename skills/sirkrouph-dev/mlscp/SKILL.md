---
name: mlscp
description: 解析并生成 MLSCP（Micro LLM Swarm Communication Protocol）命令。该协议用于高效地与其他代理进行通信、解析压缩后的命令，或生成占用较少令牌的指令。与自然语言相比，使用 MLSCP 可将令牌使用量减少 70-80%。
---

# MLSCP 技能

MLSCP（Micro LLM Swarm Communication Protocol）是一种高效、节省令牌的代理间通信命令语言。该技能允许您解析、验证和生成 MLSCP 命令，而无需任何大型语言模型（LLM）的开销。

## 为什么使用 MLSCP？

| 自然语言 | MLSCP | 节省的令牌数量 |
|-----------------|-------|---------|
| “请在文件 src/chain_orchestrator.py 的第 47 行添加重试逻辑” | `F+ s/co > ln47 + 'retry logic'` | 约 75% |
| “读取文件 utils/file_manager.py 中从第 10 行到第 50 行的内容” | `F? u/fm > ln10-50` | 约 80% |
| “删除文件 config.py 中的变量 ‘temp_cache’” | `V- c/c > 'temp_cache'` | 约 70% |

## 快速入门

### 解析命令
```bash
./scripts/mlscp.sh parse "F+ s/co > ln47 + 'retry logic'"
```

### 验证语法
```bash
./scripts/mlscp.sh validate "F+ s/co > ln47 + 'retry logic'"
```

### 生成词汇表
```bash
./scripts/mlscp.sh vocab /path/to/project
```

### 压缩自然语言
```bash
./scripts/mlscp.sh compress "Add error handling to the main function in app.py"
```

## 命令参考

### 操作
| 命令 | 含义 | 示例 |
|------|---------|---------|
| `F+` | 添加/插入文件内容 | `F+ s/app > ln10 + 'new code'` |
| `F~` | 修改文件内容 | `F~ s/app > ln10-20 ~ 'updated code'` |
| `F-` | 删除文件内容 | `F- s/app > ln10-15` |
| `F?` | 查询/读取文件内容 | `F? s/app > ln1-100` |
| `V+` | 添加变量 | `V+ s/app + 'new_var = 42'` |
| `V~` | 修改变量值 | `V~ s/app > 'old_var' ~ 'new_value'` |
| `V-` | 删除变量 | `V- s/app > 'temp_var'` |
| `V?` | 查询变量值 | `V? s/app > 'config_*'` |

### 位置指定符
- `ln47` - 单行
- `ln10-50` - 行范围
- `fn:main` - 函数名称
- `cls:MyClass` - 类名称

### 上下文块
```
CTX{"intent":"resilience","priority":"high","confidence":0.9}
```

## 脚本

- `mlscp.sh` - 主 CLI 工具
- `vocab.py` - 词汇表生成器（Python）

## 集成

### 与其他代理的集成
当从支持 MLSCP 的代理接收命令时：
```bash
./scripts/mlscp.sh parse "$INCOMING_COMMAND"
```

### 发送命令
为其他代理生成紧凑的命令：
```bash
./scripts/mlscp.sh compress "Your natural language instruction"
```

## API（Python）
```python
from mlscp import parse, MLSCPParser

# Quick parse
cmd = parse("F+ s/co > ln47 + 'retry logic'")
print(cmd.operation)  # OperationType.FILE_ADD
print(cmd.target)     # "s/co"

# With vocabulary
parser = MLSCPParser(vocab_lookup)
cmd = parser.parse("F+ s/co > ln47 + 'code'")
full_path = vocab_lookup.get("s/co")  # "src/chain_orchestrator.py"
```

## 资源

- GitHub: https://github.com/sirkrouph-dev/mlcp
- 语法规范：请参阅 `references/grammar.abnf`
- 协议定义：请参阅 `references/protocol.md`