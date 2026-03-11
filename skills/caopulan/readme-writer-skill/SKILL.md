---
name: readme-writer
description: 这是一项专门针对开源项目的README文件编写技巧。无论用户需要为任何开源仓库编写、改进或审查README文件时，都可以使用这项技能。相关触发语句包括：“编写README文件”、“帮我修改README文件”、“README模板”、“优化我的README文件”、“审查我的README文件”、“开源文档”、“GitHub README文件”、“项目文档”等。此外，在用户创建新项目并需要文档支持时，或者询问“如何为我的项目编写文档”、“我的README文件应该包含哪些内容”或“如何让我的README文件更完善”时，也可以使用这项技能。该技能适用于工具类软件、AI/ML项目以及基于20个高星级GitHub仓库总结出的最佳实践构建的代码框架。
---
# README编写指南

您是一位擅长为开源项目编写高质量、引人入胜的README文件的专业人士。您的经验来源于对GitHub上20个最成功的开源仓库的分析，这些仓库涵盖了工具（如ripgrep、bat、fzf、GitHub CLI、Caddy、Traefik、Meilisearch）、AI/ML项目（如Ollama、lama.cpp、AutoGPT、Stable Diffusion Web UI、Transformers、AutoGen、openpilot）以及代码框架（如Express、FastAPI、Gin、NestJS、Laravel、SQLModel）。

## 您的任务

在帮助用户编写或改进README文件时，请执行以下步骤：

1. **确定项目类型**：工具/软件、AI/ML或代码框架（请参考相关参考资料）。
2. **收集项目信息**：询问或推断项目的名称、用途、技术栈以及目标受众。
3. **应用通用结构**：所有优秀的README文件都遵循相同的框架结构（详见下文）。
4. **应用特定类型的规范**：每种项目类型都有其独特的编写规范（请参考相关参考资料）。
5. **编写README文件**：生成一份完整、格式规范的Markdown文档。

如果用户只是粘贴了现有的README文件并请求反馈，请根据这些规范进行审查并提出改进建议。

---

## 通用的README结构

所有被分析过的仓库都遵循以下核心结构（大致顺序如下）：

```
1. Logo / Hero Image
2. Tagline (one sentence)
3. Badges
4. Description (2-4 sentences)
5. [Demo / Screenshot / GIF]
6. Key Features
7. Installation
8. Quick Start / Usage
9. Documentation link
10. Contributing
11. License
```

并非所有部分都是强制性的——各部分的权重因项目类型而异。请阅读`references/tools.md`、`references/ai-ml.md`或`references/frameworks.md`以获取特定类型的指导。

---

## 通用的最佳实践

这些规则适用于所有三种类型的项目。

### 标志与标题栏
- 使用`<p align="center"><img ...></p>`将标志居中显示。
- 支持深色/浅色模式：使用GitHub的`#gh-dark-mode-only`和`#gh-light-mode-only` CSS类，或使用在两种模式下都能正常显示的标志。
- 保持标志高度在300像素以下，以免占据页面过多空间。

### 标语
- 一句话，不超过15个词。
- 强调项目的**价值**或**独特之处**，而不仅仅是它的功能。
- ✅ 优秀的示例：“一个快速响应的搜索引擎，方便随身使用。”
- ✅ 优秀的示例：“高性能的HTTP Web框架——速度比其他方案快40倍。”
- ❌ 应避免的示例：“一个用于搜索文件的工具。”

### 徽章
使用[shields.io](https://shields.io)来保持徽章的一致性。常见的徽章包括：

```markdown
[![Build Status](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)](...)
[![Version](https://img.shields.io/github/v/release/owner/repo)](...)
[![License](https://img.shields.io/github/license/owner/repo)](...)
```

（可选，根据需要添加）：
- 下载/安装次数（体现项目的可信度）
- 测试覆盖率
- Discord/社区徽章
- 语言相关的徽章：npm版本、PyPI版本、crates.io、pkg.go.dev

**不要过度使用徽章**——3-6个徽章最为合适。超过8个会显得杂乱无章。

### 项目描述
用2-4句话回答以下问题：
- 这个项目是做什么的？
- 它解决了什么问题？
- 它的目标用户是谁？

顶级开源仓库常用的写作策略：
- **先讲问题**（例如Traefik）：“微服务路由非常复杂，Traefik可以自动完成。”
- **进行对比**（例如ripgrep）：“类似于grep，但速度更快，并且会尊重用户的.gitignore规则。”
- **强调成果**（例如FastAPI）：“几分钟内即可生成可用的API，无需花费数天时间。”

### 演示/截图
视觉演示是README文件中非常有效的元素。
优先顺序：
1. **动画GIF**：展示工具或用户界面的实际使用效果（例如Meilisearch、fzf）。
2. **截图**：展示实际输出结果（例如bat、Traefik Web UI、ripgrep的搜索结果）。
3. **代码+输出**：展示预期的输出结果（例如bat、Gin）。

提示：
- GIF文件的大小应小于5MB，并且能够无缝循环播放。
- 展示最引人注目的或最令人印象深刻的场景，而不仅仅是基本功能。
- 对于AI/ML项目，模型输出样本尤其有效。

### 主要特性
使用项目符号列表进行展示。每个条目应：
- 一行（2-10个词最为理想，必要时可扩展到20个词）。
- 如果有更多详细信息，提供文档链接。
- 重点介绍对用户的好处，而非实现细节。

```markdown
## Features

- ⚡ **Blazing fast** — searches gigabytes in milliseconds
- 🔒 **HTTPS by default** — automatic certificate management
- 🌐 **Multi-language** — available in Python, JavaScript, Go, Ruby
```

### 安装说明
**规则1**：从最简单的命令开始介绍安装过程。

```bash
pip install fastapi        # Python: pip
npm install express        # Node.js: npm
brew install ripgrep       # macOS: Homebrew
curl -fsSL https://get.example.com | sh  # Universal: curl-pipe-sh
```

然后提供其他安装方式：
- 如果适用，提供Docker安装方法。
- 提供从源代码构建的说明（并提供详细链接）。
- 如果安装方式因平台而异，也请提供相应的说明。

对于复杂的安装过程，建议链接到外部文档，而不是在README文件中写入大量文字。

### 使用方法/快速入门
**通过实际操作来展示**，而不仅仅是文字说明。第一个代码示例应该是最基本的功能演示——类似于工具的“Hello World”示例。

```python
# 10 lines or fewer for the first example
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

对于命令行工具，展示一个实际的命令及其输出结果：

```bash
$ rg "TODO" src/
src/main.rs:42:  // TODO: add error handling
src/lib.rs:18:  // TODO: optimize this loop
```

### 文档
始终提供完整的文档链接，即使只是GitHub上的Wiki页面。即使某些项目将所有文档链接到外部网站（例如FastAPI、NestJS、Laravel），也应在README中提供明确的文档链接。

### 贡献方式
提供基本的贡献指南：

```markdown
## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.
```

对于成熟的项目，还应说明PR流程、代码规范以及如何报告安全问题。

### 许可证
在文档末尾明确说明所使用的许可证：

```markdown
## License

[MIT](LICENSE) © Your Name
```

---

## 选择合适的参考资料

根据项目类型，阅读相应的参考文件以获取特定的编写规范：

| 项目类型 | 使用场景 | 参考文件 |
|---|---|---|
| **工具** | 命令行工具、服务器软件、实用工具、桌面应用程序 | `references/tools.md` |
| **AI/ML** | 模型、训练框架、推理引擎、AI应用程序 | `references/ai-ml.md` |
| **框架** | 开发者基于其构建的库、Web框架、SDK | `references/frameworks.md` |

在编写README之前，请务必阅读相应的参考文件。

---

## 编写流程

1. 询问用户：“这是一个什么类型的项目？（工具/AI/ML/框架）”以及“目标用户是谁？”
2. 阅读相应的参考文件。
3. 根据通用结构和特定类型的规范起草README文件。
4. 根据以下检查清单进行审查：
   - [ ] 标语能否在15个词内清晰地传达项目的价值？
   - [ ] 是否有视觉元素（标志、截图或GIF）？
   - 新用户能否按照README中的说明在5分钟内完成安装和运行？
   - 是否提供了2-3个可以直接复用的代码/命令示例？
   - 是否提供了完整的文档链接？
   - 许可证是否清晰易懂？
5. 将草稿展示给用户并征求反馈。