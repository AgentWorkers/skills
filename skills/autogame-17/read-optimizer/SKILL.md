# 技能：读取优化器（read-optimizer）

## 描述
通过提供更智能的读取策略（如头部读取、尾部读取、grep搜索、差异对比等），来优化文件读取操作，从而减少令牌的使用量和读取延迟。当您需要高效地检查大文件而不必加载全部内容时，可以使用此工具。

## 使用方法

### 智能读取（头部 + 尾部）
读取文件的前 N 行和后 N 行。适用于日志文件或大型文档。
```bash
node skills/read-optimizer/index.js --file <path> --mode smart --lines 100
```

### grep 搜索
读取与指定模式匹配的行（支持正则表达式）。
```bash
node skills/read-optimizer/index.js --file <path> --mode grep --pattern "error|exception"
```

### 差异对比
仅读取自上次 Git 提交以来发生变化的行（适用于 Git 仓库）。
```bash
node skills/read-optimizer/index.js --file <path> --mode diff
```

## 参数选项
- `--file <路径>`：文件路径。
- `--mode <智能|grep|差异>`：操作模式（默认：智能模式）。
- `--lines <数量>`：头部/尾部读取的行数（默认：50 行）。
- `--pattern <字符串>`：grep 模式使用的正则表达式。
- `--context <数量>`：grep 搜索时的上下文行数（默认：2 行）。