---
name: markdown-formatter
description: 使用可配置的样式来格式化和美化 Markdown 文档。保持文档的结构，修复格式错误，并确保一致性。
metadata:
  {
    "openclaw":
      {
        "version": "1.0.0",
        "author": "Vernox",
        "license": "MIT",
        "tags": ["markdown", "formatter", "beautifier", "text", "formatting", "documentation"],
        "category": "tools"
      }
  }
---

# Markdown-Formatter - 美化您的 Markdown 文档

**Vernox 工具技能 - 让您的 Markdown 文档看起来更专业。**

## 概述

Markdown-Formatter 是一个强大的工具，用于格式化、检查语法错误并美化 Markdown 文档。它支持多种样式指南（CommonMark、GitHub Flavored Markdown 和自定义规则），能够处理从简单清理到复杂重新格式化的各种任务。

## 特点

### ✅ 格式化引擎
- 支持多种样式指南（CommonMark、GitHub、自定义）
- 保留文档结构
- 支持嵌套列表、代码块和表格
- 可配置行宽和缩进
- 智能化标题格式化
- 优化链接引用

### ✅ 语法检查与清理
- 删除尾随的空格
- 规范化行尾字符（LF 或 CRLF）
- 修复不一致的列表标记
- 删除文件末尾的空行
- 修复连续的多行空格

### ✅ 美化
- 改进标题层次结构
- 优化列表格式
- 为代码块添加适当的间距
- 在指定宽度下自动换行长文本
- 为强调内容添加适当的间距

### ✅ 验证
- 检查 Markdown 语法的有效性
- 报告语法错误
- 提出改进建议
- 验证链接和引用

## 安装

```bash
clawhub install markdown-formatter
```

## 快速入门

### 格式化文档

```javascript
const result = await formatMarkdown({
  markdown: '# My Document\n\n\n## Section 1\nContent here...',
  style: 'github',
  options: {
    maxWidth: 80,
    headingStyle: 'atx'
  }
});

console.log(result.formattedMarkdown);
```

### 美化多个文件

```javascript
const results = await formatBatch({
  markdownFiles: ['./doc1.md', './doc2.md', './README.md'],
  style: 'github',
  options: { wrapWidth: 80 }
});

results.forEach(result => {
  console.log(`${result.file}: ${result.warnings} warnings`);
});
```

### 检查语法并修复错误

```javascript
const result = await lintMarkdown({
  markdown: '# My Document\n\n\nBad list\n\n- item 1\n- item 2',
  style: 'github'
});

console.log(`Errors found: ${result.errors}`);
console.log(`Fixed: ${result.fixed}`);
```

## 工具功能

### `formatMarkdown`
根据指定的样式指南格式化 Markdown 内容。

**参数：**
- `markdown` (字符串，必填)：要格式化的 Markdown 内容
- `style` (字符串，必填)：样式指南名称（'commonmark', 'github', 'custom')
- `options` (对象，可选)：
  - `maxWidth` (数字)：行换行宽度（默认：80）
  - `headingStyle` (字符串)：'atx' | 'setext' | 'underlined' | 'consistent'（默认：'atx')
  - `listStyle` (字符串)：'consistent' | 'dash' | 'asterisk' | 'plus'（默认：'consistent')
  - `codeStyle` (字符串)：'fenced' | 'indented'（默认：'fenced')
  - `emphasisStyle` (字符串)：'underscore' | 'asterisk'（默认：'asterisk')
  - `strongStyle` (字符串)：'asterisk' | 'underline'（默认：'asterisk')
  - `linkStyle` (字符串)：'inline' | 'reference' | 'full'（默认：'inline')
  - `preserveHtml` (布尔值)：保留 HTML 标签（默认：false）
  - `fixLists` (布尔值)：修复不一致的列表标记（默认：true）
  - `normalizeSpacing` (布尔值)：修复格式周围的间距（默认：true）

**返回值：**
- `formattedMarkdown` (字符串)：格式化后的 Markdown
- `warnings` (数组)：警告信息
- `stats` (对象)：格式化统计信息
- `lintResult` (对象)：语法检查错误及修复建议
- `originalLength` (数字)：原始字符数
- `formattedLength` (数字)：格式化后的字符数

### `formatBatch`
一次性格式化多个 Markdown 文件。

**参数：**
- `markdownFiles` (数组，必填)：文件路径数组
- `style` (字符串)：样式指南名称
- `options` (对象，可选)：与 `formatMarkdown` 相同的参数

**返回值：**
- `results` (数组)：格式化结果
- `totalFiles` (数字)：处理的文件数量
- `totalWarnings` (数字)：所有文件的总警告数
- `processingTime` (数字)：处理时间（毫秒）

### `lintMarkdown`
检查 Markdown 语法错误，但不进行格式化。

**参数：**
- `markdown` (字符串，必填)：要检查的语法内容
- `style` (字符串)：样式指南名称
- `options` (对象，可选)：额外的检查选项
  - `checkLinks` (布尔值)：验证链接（默认：true）
  - `checkHeadingLevels` (布尔值)：检查标题层次结构（默认：true）
  - `checkListConsistency` (布尔值)：检查列表标记的一致性（默认：true）
  - `checkEmphasisBalance` (布尔值)：检查强调内容的配对情况（默认：false）

**返回值：**
- `errors` (数组)：错误对象
- `warnings` (数组)：警告信息
- `stats` (对象)：检查统计信息
- `suggestions` (数组)：改进建议

## 样式指南

### CommonMark (默认)
- 标准的 CommonMark 规范
- ATX 标题格式
- 参考链接格式 [text]
- 下划线强调
- 星号强调

### GitHub Flavored Markdown
- 使用 ````\`\` 标记的代码块
- 使用竖线分隔的表格
- 任务列表使用 `[]` 和 `x`
- 划线文本 `~~text~~`
- 自动链接 `https://url`

### Consistent (默认)
- 一致的 ATX 标题层次结构
- 一致的列表标记
- 一致的强调样式
- 一致的代码块样式

### 自定义
- 用户定义的规则
- 基于正则的表达式转换
- 自定义标题样式

## 使用场景

### 文档清理
- 修复 README 文件中的格式不一致问题
- 规范化标题样式
- 修复列表标记
- 清理多余的空格

### 内容创作
- 以统一风格格式化文章
- 在发布前美化博客文章
- 确保标题层次结构一致

### 技术写作
- 格式化代码文档
- 美化 API 文档
- 清理来自大型语言模型的杂乱 Markdown

### README 生成
- 格式化并美化项目 README 文件
- 确保结构一致
- 为开源项目提供专业的外观

### Markdown 转换
- 将 HTML 转换为 Markdown
- 在不同样式之间进行转换
- 从其他格式中提取并格式化 Markdown

## 配置

### 编辑 `config.json`：
```json
{
  "defaultStyle": "github",
  "maxWidth": 80,
  "headingStyle": "atx",
  "listStyle": "consistent",
  "codeStyle": "fenced",
  "emphasisStyle": "asterisk",
  "linkStyle": "inline",
  "customRules": [],
  "linting": {
    "checkLinks": true,
    "checkHeadingLevels": true,
    "checkListConsistency": true
  }
}
```

## 示例

### 简单格式化

```javascript
const result = await formatMarkdown({
  markdown: '# My Title\n\n\nThis is content.',
  style: 'github'
});

console.log(result.formattedMarkdown);
```

### 复杂美化

```javascript
const result = await formatMarkdown({
  markdown: '# Header 1\n## Header 2\n\nParagraph...',
  style: 'github',
  options: {
    fixLists: true,
    normalizeSpacing: true,
    wrapWidth: 80
  }
});

console.log(result.formattedMarkdown);
```

### 检查语法并修复错误

```javascript
const result = await lintMarkdown({
  markdown: '# Title\n\n- Item 1\n- Item 2\n\n## Section 2',
  style: 'github'
});

console.log(`Errors: ${result.errors.length}`);
result.errors.forEach(err => {
  console.log(`  - ${err.message} at line ${err.line}`);
});

// Fix automatically
const fixed = await formatMarkdown({
  markdown: result.fixed,
  style: 'github'
});
```

### 批量处理

```javascript
const results = await formatBatch({
  markdownFiles: ['./doc1.md', './doc2.md', './README.md'],
  style: 'github'
});

console.log(`Processed ${results.totalFiles} files`);
console.log(`Total warnings: ${results.totalWarnings}`);
```

## 性能

### 速度
- **小型文档**（<1000 字）：<50 毫秒
- **中型文档**（1000-5000 字）：50-200 毫秒
- **大型文档**（5000+ 字）：200-500 毫秒

### 准确性
- **结构保留**：100%
- **样式指南符合度**：95% 以上
- **空格规范化**：100%

## 错误处理

### 无效输入
- 显示清晰的错误信息
- 建议检查文件路径
- 在格式化前验证 Markdown 内容

### Markdown 解析错误
- 清晰报告解析问题
- 建议手动修复
- 在遇到错误时提供优雅的降级处理

### 文件 I/O 错误
- 显示包含文件路径的错误信息
- 检查文件是否存在
- 建议解决权限问题
- 即使出现错误，批量处理也会继续进行

## 故障排除

### 格式未应用
- 检查样式是否正确
- 确认选项是否被正确应用
- 检查是否存在冲突的规则
- 使用简单示例进行测试

### 检查语法时显示过多错误
- 有些错误只是样式选择问题，并非实际问题
- 可以考虑禁用特定的检查
- 根据需要使用自定义规则

## 提示

### 最佳效果
- 使用统一的样式指南
- 启用 `fixLists` 和 `normalizeSpacing` 选项
- 根据输出媒介设置合适的 `maxWidth`
- 先在小型样本上进行测试

### 性能优化
- 分批处理大型文件
- 禁用不必要的检查
- 对于常见模式使用更简单的规则

## 许可证

MIT

---

**格式化您的 Markdown，让文档更加美观。** 🔮