---
name: markdown-linter
description: 使用 Lint 工具检查 Markdown 文件中的格式问题、失效的链接以及样式一致性。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - markdown
        - requests
---
# Markdown Linter

## 功能介绍

这是一个命令行工具（CLI），用于检查Markdown文件中的常见格式问题、样式一致性以及失效的链接。通过在发布前捕获错误，帮助维护文档的质量。

**主要功能：**
- **标题层级验证**：确保标题层级正确（没有层级缺失）
- **图片alt文本检查**：标记缺少描述性alt文本的图片
- **内部链接验证**：检查文档内的内部链接是否指向有效的锚点
- **行长度检查**：警告超出可配置长度（默认80个字符）的行
- **末尾空白检测**：查找并报告行尾的空白字符/制表符
- **列表标记一致性**：确保同一文档内列表标记（-、*、+）的一致性
- **代码块语言标注**：建议为代码块添加语言标识
- **空链接检测**：标记文本或URL为空的链接
- **重复标题**：警告同一文件中存在重复的标题文本
- **外部链接验证**：可选地验证外部URL（需要网络连接）

## 使用方法

运行该工具：
```bash
./scripts/main.py run --input path/to/file.md
```

或者批量检查多个文件：
```bash
./scripts/main.py run --input "*.md"
```

### 参数选项

- `--input`：Markdown文件的路径（支持通配符）
- `--max-line-length`：允许的最大行长度（默认：80）
- `--check-external-links`：启用外部URL验证（默认：关闭）
- `--ignore-rules`：以逗号分隔的规则ID列表，用于忽略某些规则

### 输出结果

以JSON格式返回检查结果：
```json
{
  "file": "example.md",
  "issues": [
    {
      "line": 10,
      "column": 1,
      "rule": "MD001",
      "severity": "warning",
      "message": "Header levels should only increment by one level at a time",
      "fix": "Change ## to #"
    }
  ],
  "summary": {
    "total_issues": 5,
    "errors": 2,
    "warnings": 3
  }
}
```

## 限制事项

- 外部链接验证需要网络连接，可能会影响执行速度
- 目前尚未实现可读性评分功能
- 某些Markdown扩展（如表格、脚注）可能无法被完全验证
- 大文件（超过10,000行）的处理时间可能会较长
- 内部链接的锚点检测仅支持简单的锚点格式

## 使用示例

- 基本检查：
```bash
./scripts/main.py run --input README.md
```

- 自定义行长度检查：
```bash
./scripts/main.py run --input docs/*.md --max-line-length 100
```

- 启用外部链接验证：
```bash
./scripts/main.py run --input "**/*.md" --check-external-links
```

## 规则参考

- **MD001**：标题层级违规
- **MD002**：图片alt文本缺失
- **MD003**：内部链接失效
- **MD004**：行过长
- **MD005**：行尾有空白字符
- **MD006**：列表标记不一致
- **MD007**：代码块缺少语言标识
- **MD008**：链接为空
- **MD009**：标题重复
- **MD010**：外部链接失效（如果启用了该功能）