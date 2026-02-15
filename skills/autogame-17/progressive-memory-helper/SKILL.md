# 进阶记忆辅助工具

这是一个用于管理“进阶记忆”文件的辅助工具（包括索引部分和详细内容）。

## 使用方法

使用该工具可以轻松地向每日记忆文件中添加新条目，无需担心Markdown格式或ID冲突的问题。

### 命令

```bash
node skills/progressive-memory-helper/index.js add --type <TYPE> --summary "<SUMMARY>" --details "<DETAILS>"
```

### 参数

- `type`：记忆条目的类型。可选值：
  - `rule` (🚨)：关键规则
  - `gotcha` (🔴)：需要避免的错误
  - `fix` (🟡)：修复方法/变通方案
  - `how` (🔵)：操作指南/说明
  - `change` (🟢)：所做的更改
  - `discovery` (🟣)：新发现/收获
  - `decision` (🟤)：所做的决定
- `summary`：索引表的简短摘要（最多10个字）
- `details`：记忆条目的完整内容

### 示例

```bash
node skills/progressive-memory-helper/index.js add \
  --type decision \
  --summary "Switched to Progressive Memory" \
  --details "Decided to use progressive memory format to save tokens. Created helper script."
```

## 功能优势

- **自动格式化**：自动更新索引表并添加详细内容。
- **ID管理**：ID会自动递增（例如：#1、#2等）。
- **令牌统计**：自动计算索引中的令牌数量。
- **文件初始化**：如果文件不存在，会创建每日记录文件。