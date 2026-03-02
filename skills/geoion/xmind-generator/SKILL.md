---
name: xmind-generator
description: 将 Markdown 大纲或纯文本描述转换为 XMind 思维导图文件（.xmind 格式）。适用于用户需要创建思维导图、可视化结构或导出为 XMind 格式的情况。支持 Markdown 大纲语法（# 标题、- 列表项、缩进）以及自由形式的文本描述。输出结果将保存在工作区目录中，可直接在 XMind 应用程序中打开。
runtime: node
---
# XMind 生成器

使用 XMind SDK 从 Markdown 大纲或纯文本生成 `.xmind` 文件。

## 脚本

`scripts/generate_xmind.js` — 主生成脚本。需要 Node.js 和 `xmind` npm 包。

## 安装

**首次使用前，请安装依赖项：**
```bash
cd <skill_dir>
npm install
```

## 使用方法

```bash
# From Markdown outline file
node scripts/generate_xmind.js --input outline.md --output /path/to/output.xmind

# From inline text (use \n for newlines)
node scripts/generate_xmind.js --text "# Root\n- Branch 1\n  - Leaf\n- Branch 2" --output output.xmind

# From stdin
echo "..." | node scripts/generate_xmind.js --output output.xmind
```

**请始终从技能目录（skill directory）运行该脚本：**
```bash
cd <skill_dir>
```

**默认输出位置：** OpenClaw 工作区目录。

## 输入格式

支持两种输入格式：

**Markdown 大纲：**
```markdown
# Root Topic
- Main Branch 1
  - Sub topic 1
  - Sub topic 2
- Main Branch 2
  - Sub topic 3
    - Leaf node
```

**纯文本 / 自由格式描述：**
当用户提供纯文本描述而非 Markdown 大纲时，系统会先将其转换为 Markdown 大纲结构，然后再传递给生成脚本。

## 工作流程

1. 如果用户提供了 Markdown 大纲 → 通过 `--text` 或 `--input` 参数直接将其传递给脚本；
2. 如果用户提供了纯文本描述 → 系统会先将其转换为 Markdown 大纲，然后再生成 `.xmind` 文件；
3. 生成后的文件将保存在 OpenClaw 的工作区目录中（除非用户另有指定）；
4. 生成完成后，系统会向用户确认文件输出路径。