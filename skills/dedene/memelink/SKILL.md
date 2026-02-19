---
name: memelink
description: 使用 Memegen.link API 从终端生成表情包（meme）、图片宏（image macros）以及表情包的 URL。适用于创建表情包、选择表情包模板、生成有趣的图片，或根据文本构建表情包 URL。支持自动生成、基于模板的生成方式，以及自定义背景模式。
argument-hint: "[text or template]"
license: MIT
homepage: https://github.com/dedene/memelink-cli
metadata:
  author: dedene
  version: "1.1.0"
  openclaw:
    primaryEnv: MEMEGEN_API_KEY
    requires:
      bins:
        - memelink
    install:
      - kind: brew
        tap: dedene/tap
        formula: memelink
        bins: [memelink]
      - kind: go
        package: github.com/dedene/memelink-cli/cmd/memelink
        bins: [memelink]
---
# memelink CLI

这是一个用于从终端生成模因（meme）的工具，它封装了 Memegen.link API 的功能。

## 快速入门

```bash
# Auto-generate — API picks the best template
memelink "when the code finally compiles"

# Template-based — specify template ID + text lines
memelink drake "tabs" "spaces"

# Custom background
memelink custom --background https://example.com/bg.jpg "top" "bottom"

# Copy to clipboard and open in browser
memelink drake "before memelink" "after memelink" -c -o

# JSON output for scripting
memelink --json "deploy on friday"
```

## 命令

- `memelink "text"` -- 自动选择模板并生成模因（默认命令）
- `memelink <template> "top" "bottom"` -- 使用指定的模板生成模因
- `memelink custom --background <url> "text"` -- 使用自定义背景图片生成模因
- `memelink templates` -- 列出所有模板；支持TTY界面下的交互式选择（别名：ls）
- `memelink templates <id>` -- 显示指定模板的详细信息
- `memelink templates --filter <query>` -- 根据查询条件过滤模板
- `memelink fonts` -- 列出可用的字体
- `memelink config path|list|get|set|unset` -- 管理配置文件
- `memelink version` -- 显示版本信息

命令别名：`generate` → `gen`, `g`; `templates` → `ls`

## 生成模因的参数

- `--format png|jpg|gif|webp` / `-f` -- 输出格式
- `--font <name>` -- 使用的字体名称
- `--layout default|top` -- 文本布局方式
- `--width N` / `--height N` -- 图像尺寸
- `--style <style>` -- 模板样式（可重复使用）
- `--text-color <hex>` -- 每行的文本颜色（可重复使用）
- `--background <url>` -- 自定义背景图片（仅适用于使用“custom”模板的场景）
- `--center x,y` / `--scale N` -- 模因在屏幕上的显示位置和缩放比例
- `--safe` -- 过滤不适宜工作场所的内容
- `--copy` / `-c` -- 将模因的 URL 复制到剪贴板
- `--open` / `-o` -- 在浏览器中打开模因
- `--output <path>` / `-O` -- 下载生成的图片
- `--preview` / `--no-preview` -- 在终端中显示模因预览

## 配置

配置文件：`~/.config/memelink/config.json`

```bash
memelink config set default_format png
memelink config get default_format
memelink config list
```

配置项：default_format, default_font, default_layout, safe, auto_copy, auto_open, preview, cache_ttl

## 环境变量

- `MEMEGEN_API_KEY` -- 可选参数，用于获取更高的 API 访问速率限制

## 全局参数

- `--json` -- 以 JSON 格式输出结果（便于管道传输）
- `--no-input` -- 禁用交互式提示
- `--verbose` -- 开启详细日志记录
- `--color auto|always|never` -- 控制输出颜色的显示方式

## 安装方法

```bash
brew install dedene/tap/memelink-cli
```