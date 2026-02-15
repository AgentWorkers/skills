---
name: vhs-recorder
description: 使用 VHS 磁带文件创建专业的终端录制内容：涵盖语法、时间控制、设置及最佳实践指南
---

# VHS 录像工具

使用 Charm 的 VHS 工具在终端中创建录制内容。适用于生成 CLI 演示、README 文档中的动画以及技术文档视频。

## 先决条件
- 已安装 `vhs` 工具（通过 `brew install vhs` 或 `go install github.com/charmbracelet/vhs@latest` 安装）
- `ttyd` 和 `ffmpeg` 已添加到系统的 PATH 环境变量中

## 磁带文件结构
```tape
Output demo.gif         # Outputs first
Set Width 1200          # Settings second
Set Theme "Catppuccin Mocha"
Require git             # Requirements third
Hide                    # Hidden setup
Type "cd /tmp && clear"
Enter
Show
Type "your command"     # Main recording
Enter
Wait
Sleep 2s
```

## 核心命令
| 命令 | 功能 |
|---------|---------|
| `Type "text"` | 输入文本（使用 `TypingSpeed` 设置） |
| `Enter` / `Tab` / `Space` | 执行按键操作 |
| `Up` / `Down` / `Left` / `Right` | 方向键导航 |
| `PageUp` / `PageDown` | 页面导航 |
| `Ctrl+C` / `Ctrl+D` / `Ctrl+L` | 发送信号、结束输入或清除内容 |
| `Wait` / `Wait /pattern/` | 等待命令提示或正则表达式匹配结果 |
| `Sleep 2s` | 暂停 2 秒（支持毫秒、秒或分钟为单位） |
| `Hide`/`Show` | 隐藏或显示终端界面（包括设置和清理信息） |
| `Type@50ms "text"` | 直接设置输入速度（单位：毫秒） |
| `Backspace N` / `Delete N` | 删除指定数量的字符 |
| `Copy` / `Paste` | 复制/粘贴文本 |
| `Screenshot path.png` | 截取当前终端屏幕的图片 |
| `Env VAR "value"` | 设置环境变量 |

## 基本配置选项
| 选项 | 默认值 | 说明 |
|---------|---------|-------|
| Width/Height | 1200/600 | 终端窗口的宽度/高度（单位：像素） |
| FontSize | 32 | 文本字号；支持自定义字体 |
| TypingSpeed | 50ms | 每个字符的输入延迟时间（可通过 `Type@Xms` 重置） |
| Theme | - | 使用 `vhs themes` 查看可用的主题样式 |
| Padding | 40 | 界面边框间距；也可设置 `LetterSpacing` 和 `LineHeight` |

## 时间控制与操作节奏
**3-2-1 规则**：重要命令后延迟 3 秒，操作之间间隔 2 秒，过渡效果持续 1 秒
- **干净启动流程**：`Hide` → `Type "clear"` → `Enter` → `Show`
- **命令执行后等待**：`Type` → `Enter` → `Wait` → `Sleep 2s`
- **快速隐藏界面**：`Type@10ms "setup command"`（立即隐藏界面）
- **ASCII 预览**：`Output demo.ascii`（快速查看输出结果）

## 输出格式
| 格式 | 适用场景 |
|--------|----------|
| `.gif` | 适用于网页或 README 文件 |
| `.mp4`/`.webm` | 适用于社交媒体和现代浏览器 |
| `.ascii` | 用于预览或快速测试（无需 `ffmpeg` 处理） |
| `frames/` | 生成 PNG 图片序列，便于后续处理 |

## 常见问题及解决方法
| 问题 | 解决方案 |
|-------|----------|
| 命令执行过快 | 在输入命令后添加 `Wait` 和 `Sleep 2s` 来控制执行速度 |
| 终端界面显示混乱 | 启动时执行 `Hide` → `clear` → `Show` 来清理界面 |
| 动作节奏不一致 | 遵循 3-2-1 的时间控制规则 |

## 命令行接口（CLI）命令
```bash
vhs demo.tape       # Run tape file
vhs themes          # List all available themes
vhs manual          # Show full command reference
```

## 参考资料
- [vhs-syntax.md](./references/vhs-syntax.md) - 完整的命令参考文档 |
- [timing-control.md](./references/timing-control.md) - 时间控制策略说明 |
- [settings.md](./references/settings.md) - 所有配置选项的详细说明 |
- [examples.md](./references/examples.md) - 实际使用案例及示例文件