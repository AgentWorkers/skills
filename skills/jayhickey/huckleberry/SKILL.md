---
name: huckleberry
description: 通过 Huckleberry CLI 追踪婴儿的睡眠、喂食、换尿布以及生长情况。当用户询问关于记录婴儿活动、开始/结束睡眠、使用奶瓶喂食、更换尿布或测量婴儿生长数据的相关信息时，可以使用该工具。
---

# Huckleberry CLI

这是一个用于 [Huckleberry](https://huckleberrycare.com/)（一款婴儿跟踪应用程序）的命令行接口。只需进行一次身份验证，即可在终端中记录宝宝的睡眠情况、喂食情况、换尿布情况以及成长数据。

> **注意：** 这是一个非官方工具，与 Huckleberry 无任何关联。

## 安装

```bash
pip install huckleberry-cli
```

## 快速入门

```bash
huckleberry login
huckleberry children
huckleberry sleep start
```

## 命令

### 睡眠记录

```bash
huckleberry sleep start      # Start sleep timer
huckleberry sleep stop       # Complete sleep (saves duration)
huckleberry sleep pause      # Pause sleep timer
huckleberry sleep resume     # Resume paused sleep
huckleberry sleep cancel     # Cancel without saving
```

### 喂食记录

**母乳喂养：**
```bash
huckleberry feed start --side=left    # Start nursing (left side)
huckleberry feed start --side=right   # Start nursing (right side)
huckleberry feed switch               # Switch sides mid-feed
huckleberry feed stop                 # Complete feeding
```

**配方奶喂养：**
```bash
huckleberry feed bottle <amount> [--type=TYPE] [--units=UNITS]

# Examples:
huckleberry feed bottle 120                           # 120ml formula (default)
huckleberry feed bottle 4 --units=oz                  # 4oz formula
huckleberry feed bottle 100 --type="Breast Milk"      # 100ml pumped milk
```

**喂食类型：** `Formula`（配方奶）、`Breast Milk`（母乳）、`Mixed`（混合喂养）
**单位：** `ml`（默认单位）、`oz`（盎司）

### 换尿布记录

```bash
huckleberry diaper pee                              # Wet only
huckleberry diaper poo                              # Dirty only
huckleberry diaper both                             # Wet + dirty
huckleberry diaper dry                              # Dry check

# With details:
huckleberry diaper poo --color=yellow               # With color
huckleberry diaper poo --consistency=soft           # With consistency
huckleberry diaper both --color=brown --consistency=runny
```

**尿布颜色：** `yellow`（黄色）、`green`（绿色）、`brown`（棕色）、`black`（黑色）、`red`（红色）
**尿布质地：** `runny`（稀薄）、`soft`（柔软）、`solid`（固态）、`hard`（硬质）

### 宝宝成长记录

```bash
huckleberry growth --weight=7.5                     # Weight in kg
huckleberry growth --height=65                      # Height in cm
huckleberry growth --head=42                        # Head circumference in cm
huckleberry growth --weight=7.5 --height=65 --head=42  # All at once

# Imperial units:
huckleberry growth --weight=16.5 --units=imperial   # Weight in lbs
```

### 信息查询

```bash
huckleberry children           # List children
huckleberry --json children    # JSON output (--json before subcommand)
huckleberry status             # Current status
```

### 多个宝宝的管理

```bash
huckleberry --child="Baby" sleep start   # Specify child by name
huckleberry -c "Baby" diaper pee
```

## 身份验证

身份验证配置存储在 `~/.config/huckleberry/config.json` 文件中。

```bash
huckleberry login                        # Interactive setup
```

或者，您也可以通过环境变量进行身份验证：
```bash
export HUCKLEBERRY_EMAIL="your@email.com"
export HUCKLEBERRY_PASSWORD="your-password"
export HUCKLEBERRY_TIMEZONE="America/Los_Angeles"
```

## 系统要求

- Python 3.11 或更高版本
- [huckleberry-api](https://github.com/Woyken/py-huckleberry-api) 库

## 单位换算

- 1盎司（oz）约等于 30 毫升（ml）
- 1磅（lb）约等于 0.45 千克（kg）
- 1英寸（inch）约等于 2.54 厘米（cm）