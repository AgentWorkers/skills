# 使用 [VHS](https://github.com/charmbracelet/vhs) 生成终端截图和动画 GIF/视频

**VHS** 是一个基于 Charmbracelet 的工具，可以用来生成终端截图和动画 GIF/视频。

## 适用场景

- 为文档生成终端截图
- 录制命令行工具的动画 GIF
- 制作命令行工具的教学视频
- 生成一致且可复制的终端操作可视化效果
- 通过黄金文件（golden files）进行集成测试

## 先决条件

### 安装检查

```bash
# Check if vhs is installed
which vhs && vhs --version

# Check dependencies
which ttyd && which ffmpeg
```

### 安装方法

**推荐使用：Homebrew（macOS/Linux）**

```bash
brew install vhs
```

使用 Homebrew 可以同时安装 VHS 及其所有依赖项（ttyd、ffmpeg）。

**其他安装方法：**

```bash
# Fedora/RHEL
echo '[charm]
name=Charm
baseurl=https://repo.charm.sh/yum/
enabled=1
gpgcheck=1
gpgkey=https://repo.charm.sh/yum/gpg.key' | sudo tee /etc/yum.repos.d/charm.repo
sudo dnf install vhs ffmpeg
# Also install ttyd: https://github.com/tsl0922/ttyd/releases

# Arch Linux
pacman -S vhs

# Docker (includes all dependencies)
docker run --rm -v $PWD:/vhs ghcr.io/charmbracelet/vhs <cassette>.tape
```

## 基本用法

### 1. 创建一个 `tape` 文件

```bash
vhs new demo.tape
```

### 2. 编辑 `tape` 文件

`tape` 文件是一种简单的脚本，用于指定需要输入的内容和捕获的操作。

### 3. 运行 VHS

```bash
vhs demo.tape
```

## `tape` 文件的语法

### 输出格式

```tape
Output demo.gif          # Animated GIF
Output demo.mp4          # Video file
Output demo.webm         # WebM video
Output frames/           # PNG sequence (directory)
```

你可以在一个 `tape` 文件中指定多个输出格式。

### 设置（必须放在文件开头）

```tape
# Terminal dimensions
Set Width 1200
Set Height 600

# Font settings
Set FontSize 22
Set FontFamily "JetBrains Mono"

# Appearance
Set Theme "Catppuccin Mocha"
Set Padding 20
Set Margin 20
Set MarginFill "#1e1e2e"
Set BorderRadius 10
Set WindowBar Colorful

# Behavior
Set Shell "bash"
Set TypingSpeed 50ms
Set Framerate 30
Set CursorBlink false
```

### 可用的主题

运行 `vhs themes` 可以查看所有可用的主题：
- `Catppuccin Mocha`
- `Catppuccin Frappe`
- `Dracula`
- `Tokyo Night`
- `Nord`
- `One Dark`

### 常用命令

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `Type "text"` | 输入文本 | `Type "echo hello"` |
| `Type@500ms "text"` | 慢速输入文本 | `Type@500ms "important"` |
| `Enter` | 按回车键 | `Enter` |
| `Enter 2` | 按两次回车键 | `Enter 2` |
| `Sleep 1s` | 等待 1 秒 | `Sleep 500ms` |
| `Backspace` | 删除一个字符 | `Backspace 5` |
| `Tab` | 按 Tab 键 | `Tab` |
| `Space` | 按空格键 | `Space` |
| `Ctrl+C` | 执行控制序列 | `Ctrl+L` |
| `Up/Down/Left/Right` | 方向键 | `Up 3` |
| `Hide` | 停止录制帧 | `Hide` |
| `Show` | 恢复录制 | `Show` |
| `Screenshot file.png` | 保存当前帧为图片 | `Screenshot out.png` |
| `Wait /regex/` | 等待特定文本出现 | `Wait /\$\s*$/` |
| `Env KEY "value"` | 设置环境变量 | `Env PS1 "$ "` |
| `Require program` | 如果程序缺失则失败 | `Require git` |
| `Source file.tape` | 引用另一个 `tape` 文件 | `Source setup.tape` |

### 引用引号

使用反引号（``）来转义引号：

```tape
Type `echo "hello world"`
Type `VAR='value'`
```

## 示例

### 静态截图

```tape
Output screenshot.png

Set Width 800
Set Height 400
Set FontSize 18
Set Theme "Catppuccin Mocha"
Set Padding 20

# Hide setup
Hide
Type "clear"
Enter
Show

# The actual content
Type "ls -la"
Enter
Sleep 500ms

Screenshot screenshot.png
```

### 动画演示 GIF

```tape
Output demo.gif

Set Width 1000
Set Height 500
Set FontSize 20
Set Theme "Dracula"
Set TypingSpeed 50ms
Set Padding 20
Set WindowBar Colorful

# Clean start
Hide
Type "clear"
Enter
Show

# Demo sequence
Type "echo 'Hello from VHS!'"
Sleep 300ms
Enter
Sleep 1s

Type "date"
Enter
Sleep 1s

Type "echo 'That was easy!'"
Enter
Sleep 2s
```

### 带有简洁提示信息的 MP4 视频

```tape
Output tutorial.mp4

Set Width 1200
Set Height 600
Set FontSize 24
Set Theme "Tokyo Night"
Set Shell "bash"
Set Framerate 30

# Set a clean, minimal prompt
Hide
Env PS1 "$ "
Type "clear"
Enter
Show

Type "# Welcome to the tutorial"
Enter
Sleep 1s

Type "git status"
Enter
Sleep 2s

Type "git log --oneline -5"
Enter
Sleep 3s
```

## 优化输出效果的技巧

### 1. 隐藏初始化和清理操作

```tape
# Setup (hidden)
Hide
Type "cd ~/project && clear"
Enter
Show

# Your demo here...

# Cleanup (hidden)
Hide
Type "cd - && rm temp-files"
Enter
```

### 2. 使用简洁的提示信息

```tape
Hide
Env PS1 "$ "
Type "clear"
Enter
Show
```

### 3. 控制时间间隔

- 为了提高可读性，可以频繁使用 `Sleep` 命令来控制操作之间的延迟：
  - 输入后等待 `Sleep 500ms` 再按回车
  - 命令输出后等待 `Sleep 1s` 到 `2s`
  - 最后一帧等待 `Sleep 2s` 或更长时间

### 4. 输入速度

```tape
# Default speed for setup
Set TypingSpeed 10ms

# Slow down for important parts
Type@100ms "Important command here"
```

### 5. 等待输出结果

```tape
Type "npm install"
Enter
Wait /added \d+ packages/  # Wait for completion message
Sleep 1s
```

### 6. 在关键时刻截取屏幕截图

```tape
Type "make build"
Enter
Wait /Build complete/
Screenshot build-success.png
```

## 文档制作的工作流程

1. **规划** 演示的顺序
2. **创建** 一个包含设置信息的 `.tape` 文件
3. **使用 `vhs demo.tape` 进行测试（生成输出结果）
4. **迭代**：调整操作的时间间隔、显示尺寸和主题样式
5. **将 `.tape` 文件和输出结果提交到代码仓库**

## 录制实际操作过程

你可以录制终端操作并生成 `tape` 文件：

```bash
vhs record > session.tape
```

之后可以对生成的 `tape` 文件进行编辑，以优化显示效果。

## 文件参考

- `basic-screenshot.tape`：简单的静态截图示例
- `demo-recording.tape`：动画 GIF 演示示例

## 资源链接

- [VHS 官方 GitHub 仓库](https://github.com/charmbracelet/vhs)
- [VHS 主题样式](https://github.com/charmbracelet/vhs/blob/main/THEMES.md)
- [示例 `tape` 文件](https://github.com/charmbracelet/vhs/tree/main/examples)