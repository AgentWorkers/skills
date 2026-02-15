---
name: clawd-modifier
description: **修改 Clawd（Claude Code 的吉祥物）**  
当用户希望自定义 Clawd 在 Claude Code CLI 中的外观时，可以使用此技能。具体操作包括：更改 Clawd 的颜色（蓝色、绿色或节日主题）、添加手臂、帽子等装饰元素，或者创建自定义的 ASCII 艺术图案。  
可使用的命令示例：  
- `change Clawd color`  
- `give Clawd arms`  
- `customize the mascot`  
- `modify Clawd`  
- `make Clawd [color]`  
- 任何用于个性化 Claude Code 终端吉祥物的请求。
---

# Clawd 修改器

通过修改颜色和 ASCII 艺术图案来自定义 Claude 代码吉祥物的外观。

## 快速参考

**命令行工具位置**：`/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js`

**Clawd 的颜色**：
- 正文：`rgb(215,119,87)` / `ansi:redBright`
- 背景：`rgb(0,0,0)` / `ansi:black`

**小型的 Clawd**（提示符）：
```
 ▐▛███▜▌
▝▜█████▛▘
  ▘▘ ▝▝
```

## 工作流程

### 更改 Clawd 的颜色

使用 `scripts/patch_color.py`：

```bash
# List available colors
python scripts/patch_color.py --list

# Apply preset
python scripts/patch_color.py blue

# Custom RGB
python scripts/patch_color.py --rgb 100,200,150

# Restore original
python scripts/patch_color.py --restore
```

### 添加手臂或修改艺术图案

使用 `scripts/patch_art.py`：

```bash
# List variants
python scripts/patch_art.py --list

# Add arms
python scripts/patch_art.py --variant with-arms

# Individual modifications
python scripts/patch_art.py --add-left-arm
python scripts/patch_art.py --add-right-arm

# Restore original
python scripts/patch_art.py --restore
```

### 提取当前的 Clawd 外观

使用 `scripts/extract_clawd.py` 来查看当前的状态：

```bash
python scripts/extract_clawd.py
```

### 手动修改

对于脚本未覆盖的自定义修改，请直接编辑 `cli.js`：

1. 备份：`cp cli.js cli.js.bak`
2. 使用 `grep` 查找需要修改的文本模式
3. 使用 `sed` 或文本编辑器进行替换
4. 通过运行 `claude` 来测试修改效果

**模式示例**：
```bash
# Find color definitions
grep -o 'clawd_body:"[^"]*"' cli.js | head -5

# Replace color
sed -i 's/rgb(215,119,87)/rgb(100,149,237)/g' cli.js
```

## 资源

- **Unicode 参考**：请参阅 `references/unicode-blocks.md` 以获取相关字符信息
- **技术细节**：请参阅 `references/clawd-anatomy.md` 了解渲染原理
- **设计图库**：请参阅 `assets/clawd-variants.txt` 以获取设计灵感

## 注意事项

- 修改内容会在执行 `npm update` 时被覆盖
- 修改前请务必创建备份
- 修改后请使用 `claude --version` 来测试功能是否正常
- 有些终端对 Unicode 的支持有限