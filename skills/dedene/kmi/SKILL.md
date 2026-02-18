---
name: kmi-cli
description: 通过 KMI/IRM meteo.be API 查询比利时天气。当用户需要比利时地区的天气预报、当前天气信息、雷达图、天气警报或紫外线指数时，可以使用该功能。该功能会在用户提及“Belgian weather”、“KMI”、“IRM”、“meteo.be”或“Belgian forecast”时被触发。
license: MIT
homepage: https://github.com/dedene/kmi-irm-cli
metadata:
  author: dedene
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - kmi
    install:
      - kind: brew
        tap: dedene/tap
        formula: kmi
        bins: [kmi]
      - kind: go
        package: github.com/dedene/kmi-irm-cli/cmd/kmi
        bins: [kmi]
      - kind: binary
        url: https://github.com/dedene/kmi-irm-cli/releases/latest
        bins: [kmi]
---
# kmi-cli

这是一个用于 [KMI/IRM](https://www.meteo.be/) 的命令行工具（CLI），该平台提供来自比利时皇家气象研究所的天气数据。

## 快速入门

```bash
# Current weather
kmi current Brussels

# 7-day forecast
kmi forecast Leuven

# Weather warnings
kmi warnings Belgium

# UV index
kmi uv Antwerp
```

## 无需身份验证

此 CLI 使用的是公开的 meteo.be API，因此无需 API 密钥或注册。

## 核心规则

1. **在程序化解析输出时，务必使用 `--json` 标志**。
2. **位置输入格式**：城市名称（如 `Brussels`）、坐标（如 `50.85,4.35`），或收藏地点（如 `@home`）。
3. **收藏地点的格式**：使用 `@` 前缀，例如 `kmi forecast @home`。
4. **速率限制是自动执行的**——CLI 会自动处理这一机制。

## 输出格式

| 标志 | 格式 | 用途 |
|------|--------|----------|
| （默认） | 表格形式 | 适用于用户界面显示 |
| `--json` | JSON | 适用于代理解析或脚本编写 |
| `--plain` | TSV | 可用于传递给 awk 或 cut 等工具进行处理 |

## 功能流程

### 当前天气

```bash
# By city name
kmi current Brussels

# By coordinates
kmi current 50.85,4.35

# By saved favorite
kmi current @home

# JSON output for parsing
kmi current Brussels --json
```

### 天气预报

```bash
# 7-day forecast
kmi forecast Leuven

# Daily breakdown
kmi daily Leuven

# Hourly for next 12 hours
kmi hourly Leuven

# JSON output
kmi forecast Leuven --json
```

### 雷达图

```bash
# Download radar animation frames
kmi radar Brussels

# Specify output directory
kmi radar Brussels --output-dir ~/tmp
```

**注意**：雷达图数据会下载到当前目录或指定的目录中。

### 警报信息

```bash
# Get active weather warnings
kmi warnings Belgium

# JSON for scripting
kmi warnings Belgium --json
```

### 紫外线指数

```bash
# UV index for location
kmi uv Antwerp

# JSON output
kmi uv Antwerp --json
```

### 收藏地点

```bash
# Save a favorite location
kmi favorites add home 50.85,4.35
kmi favorites add work Brussels

# List all favorites
kmi favorites list

# Use favorites with @ prefix
kmi forecast @home
kmi current @work

# Remove a favorite
kmi favorites remove work
```

## 脚本示例

```bash
# Get current temperature
kmi current Brussels --json | jq -r '.temperature'

# Check if rain is expected today
kmi forecast Brussels --json | jq -r '.[0].precipitation'

# Get warning count
kmi warnings Belgium --json | jq 'length'

# List all forecasted conditions
kmi forecast Brussels --json | jq -r '.[] | "\(.day): \(.condition)"'
```

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `KMI_LANG` | 语言设置（en, nl, fr, de） |
| `NO_COLOR` | 禁用彩色输出 |

## 使用指南

- 无需 API 密钥，即可直接使用。
- 收藏地点功能需要用户自行设置；未经用户同意，不得创建收藏地点。
- 速率限制会自动执行，无需额外处理。
- 雷达图数据会下载到指定目录中；系统会向用户提示文件下载情况。

## 安装方法

```bash
# macOS/Linux
brew install dedene/tap/kmi

# Windows - download from GitHub Releases
# https://github.com/dedene/kmi-irm-cli/releases
```