# 代码搜索技能

这是一个智能的、具备上下文感知能力的仓库搜索工具。使用它来替代复杂的 `grep` 或 `find` 命令。

## 为什么使用它？
- **比 `grep` 更智能**：会自动忽略 `node_modules`、`.git` 和锁定文件（lockfiles）。
- **具备上下文感知能力**：可以显示匹配项前后的代码行（使用 `--context 2` 选项）。
- **结构化输出**：支持以 JSON 格式输出结果，便于机器解析。
- **安全性**：限制输出结果的大小，以防止数据溢出。

## 使用方法

### 命令行界面 (CLI)
```bash
# Basic search
node skills/code-search/index.js --query "function main"

# Search specific file types (glob pattern support is basic: *.js, *.ts)
node skills/code-search/index.js --query "TODO" --include "*.js"

# Search with context (2 lines around match)
node skills/code-search/index.js --query "error" --context 2

# Output JSON
node skills/code-search/index.js --query "export default" --json
```

### 与其他技能的集成（Node.js）
```javascript
const { execSync } = require('child_process');
const output = execSync('node skills/code-search/index.js --query "myFunction" --json').toString();
const results = JSON.parse(output);
```

## 配置选项
- 默认匹配数量：50 条（防止输出信息过多）
- 默认忽略的文件目录：`.git`、`node_modules`、`dist`、`build`、`coverage`、`.npm-global`

## 故障排除
- 如果没有找到结果，尝试扩大搜索范围。
- 如果搜索结果太多，可以使用 `--include` 选项来过滤文件类型。