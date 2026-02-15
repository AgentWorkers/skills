---
name: Humanize CLI - AI Text Detection & Rewriting
description: 检测由人工智能生成的文本模式，并提供相应的修复建议。评估文本被篡改的风险，识别其中使用的AI生成词汇，提出改进方案。为作家和内容创作者提供免费的命令行工具（CLI）。
---

# 优化命令行界面（CLI）以提升用户体验

该工具能够分析文本中的AI特征，并提供可操作的修改建议，帮助内容通过AI检测器的审核。

## 安装

```bash
npm install -g humanize-cli
```

## 命令

### 检测风险等级

```bash
humanize score "Your text here"
humanize score -f article.txt
```

返回0-100%的风险等级：
- 0-20%：低风险（看起来像人类编写）
- 21-40%：中等风险
- 41-70%：高风险（可能被标记为AI生成）
- 71-100%：非常高风险

### 分析AI写作特征

```bash
humanize analyze "This comprehensive solution leverages cutting-edge technology."
```

检测以下AI写作特征：
- AI常用的词汇（如“delve”、“leverage”、“comprehensive”、“robust”、“seamless”等）
- 重复的结构模式（如所有句子长度相同、引言和结论过于完美）
- 缺乏人类语言的元素（如不使用缩写、没有个人观点）

### 获取改进建议

```bash
humanize suggest "It is important to note that our solution utilizes..."
```

提供优先级排序的修改建议，并附上修改前后的对比示例。

### 自动转换文本

```bash
humanize transform "The solution utilizes robust methodologies."
# Output: "The solution uses strong methods."
```

自动替换AI风格的词汇，并添加更自然的人类语言表达。

### 监控目录

```bash
humanize watch ./content --threshold 60
```

实时监控文件内容，当检测风险超过预设阈值时发出警报。

## 常见使用场景

**发布前检查博客文章：**
```bash
humanize score -f blog-post.md
```

**修正具有AI特征的文本：**
```bash
humanize transform -f draft.txt > improved.txt
```

**从剪贴板导入内容（macOS）：**
```bash
pbpaste | humanize suggest
```

## 选项

| 选项 | 描述 |
|------|-------------|
| `-f, --file` | 从文件中读取内容 |
| `-j, --json` | 以JSON格式输出结果 |
| `-q, --quiet` | 减少输出信息 |
| `-t, --threshold` | 设置风险阈值（0-100） |

## 主要检测内容

**AI常用词汇：**
- delve, leverage, utilize, comprehensive, robust, seamless
- stakeholder, synergy, actionable, paradigm
- furthermore, moreover, consequently, nevertheless

**结构问题：**
- 不使用缩写（使文本听起来像机器生成）
- 所有句子长度相同
- 引言、正文和结论过于完美
- 过度使用过渡词

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/humanize-cli) · [Twitter](https://x.com/lxgicstudios)