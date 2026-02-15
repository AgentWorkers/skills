---
name: pr-demo
description: **用途：**  
用于创建动画演示（GIF文件），以供提交 Pull Request 或用于文档说明。该方法包括使用 `ascinema` 工具记录终端操作过程，并将录制的视频转换为 GIF 或 SVG 格式，以便在 GitHub 上嵌入使用。
---

# PR演示创建

## 概述

使用`asciinema`录制的视频转换为GIF格式，为Pull Requests（PR）创建精美的终端演示。工作流程如下：**编写脚本 → 录制 → 转换 → 嵌入**。

## 工具选择

| 目标 | 工具链 | 输出格式 |
|------|------------|--------|
| 适用于GitHub PR的CLI演示 | asciinema → agg | GIF（小于5MB） |
| 需要更小的文件大小 | asciinema → svg-term-cli | SVG（小于500KB） |
| 图形界面截图 | tmux → freeze | SVG/PNG |

**默认选择：** asciinema + agg（兼容性最佳，GitHub原生支持GIF格式）

## 先决条件

```bash
# Install tools (macOS)
brew install asciinema
cargo install --git https://github.com/asciinema/agg
npm install -g svg-term-cli  # Optional: for SVG output
```

## 工作流程

### 1. 编写演示脚本（必选）

在录制之前，编写一个简短的脚本：

```markdown
## Demo: [feature name]
Duration: ~20-30 seconds

1. [0-3s] Show command being typed
2. [3-10s] Command executes, show key output
3. [10-25s] Highlight the "aha moment" - what makes this valuable
4. [25-30s] Clean exit or final state
```

**请保持脚本简短，时长控制在20-30秒以内，并重点展示一个功能或操作。**

### 2. 准备环境

```bash
# Clean terminal state
clear
export PS1='$ '                    # Simple prompt
export TERM=xterm-256color         # Consistent colors
# Hide sensitive info (API keys, paths with usernames)
```

终端尺寸：**100x24**（缩放后仍可清晰显示）

### 3. 录制

```bash
# Record to .cast file
asciinema rec demo.cast --cols 100 --rows 24

# Execute your scripted demo
# Press Ctrl+D or type 'exit' when done
```

**提示：**
- 以适中的速度输入内容（不要太快）
- 在关键操作后稍作停顿
- 如果出现错误，请重新开始录制（编辑比重新录制更麻烦）

### 4. 转换为GIF格式

```bash
# Basic conversion (recommended)
agg demo.cast demo.gif

# With speed adjustment (1.5x faster)
agg --speed 1.5 demo.cast demo.gif

# With custom font size for readability
agg --font-size 14 demo.cast demo.gif
```

**替代方案 - 使用SVG格式（文件更小）：**
```bash
svg-term --in demo.cast --out demo.svg --window
```

### 5. 自我验证

Claude可以通过以下三种方式对演示进行自我验证：

#### A. 自动检查（优先执行）

```bash
# Check file size (must be < 5MB for GitHub)
ls -lh demo.gif

# Check recording duration from .cast metadata
head -1 demo.cast | jq '.duration // "check manually"'
```

#### B. 视觉验证（使用大型语言模型进行评估）

提取一个静态帧供Claude分析：

```bash
# Option 1: Use svg-term to render a specific timestamp (e.g., 15 seconds in)
svg-term --in demo.cast --out demo-preview.svg --at 15000

# Option 2: Use asciinema cat + freeze for a snapshot
asciinema cat demo.cast | head -500 | freeze -o demo-preview.png

# Option 3: Just convert to GIF and use the file directly
# Claude can read GIF files with the Read tool
```

然后使用Read工具让Claude分析该图像：

**验证提示：**
```
Analyze this terminal demo screenshot. Check:
1. Is the text readable (not too small/blurry)?
2. Is the command being demonstrated visible?
3. Is there any sensitive info (API keys, /Users/username paths)?
4. Does the terminal look clean (simple prompt, no clutter)?
5. Is the "aha moment" visible - what value does this demo show?

Rate: PASS or FAIL with specific issues.
```

#### C. 内容验证（解析 `.cast` 文件）

`.cast` 文件包含JSON格式的数据——通过编程方式验证内容是否正确：

```bash
# Check what commands were typed (input events)
grep '"i"' demo.cast | head -20

# Check recording duration
head -1 demo.cast | jq -r '.duration | floor'
# Should be 20-30 seconds

# Look for sensitive patterns
grep -iE '(api.?key|password|secret|/Users/[a-z])' demo.cast && echo "WARNING: Sensitive data found!"
```

#### D. 完整的验证清单

执行上述步骤后，需确认以下内容：
- [ ] 文件大小小于5MB（自动检查）
- [ ] 时长在20-30秒之间（自动检查）
- `.cast` 文件中不含敏感信息（自动检查）
- 预览帧中的文本可读（视觉/语言模型评估）
- 演示功能展示清晰（视觉/语言模型评估）
- 终端界面整洁（视觉/语言模型评估）

### 6. 嵌入到PR中

将生成的演示文件存储在`docs/demos/`或`assets/`目录中。

## 快速参考

| 设置 | 推荐值 |
|---------|------------------|
| 时长 | 20-30秒 |
| 终端尺寸 | 100x24 |
| 显示速度 | 1.0-1.5倍 |
| 目标文件大小 | 理想值<2MB，最大值<5MB |
| 字体大小（agg格式） | 14-16 |

## 常见错误及解决方法

| 错误 | 解决方法 |
|---------|-----|
| 演示时间过长 | 先编写脚本，重点展示一个核心功能 |
| 文本无法阅读 | 使用`--font-size 14+`设置字体大小，并将终端尺寸设置为100x24 |
| 文件过大 | 改用`svg-term-cli`工具，或提高显示速度 |
| 终端界面杂乱 | 清理终端历史记录，隐藏路径信息 |
| PR中缺少上下文说明 | 在GIF文件下方添加简短描述 |

## 文件组织结构

```
docs/demos/
├── feature-name.gif      # The demo
├── feature-name.cast     # Source recording (optional, for re-rendering)
└── README.md             # Recording instructions for future maintainers
```