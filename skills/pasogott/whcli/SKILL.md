---
name: whcli
description: **Willhaben CLI**：用于搜索奥地利最大的分类广告市场。您可以搜索广告列表、查看详细信息以及卖家资料。
homepage: https://github.com/pasogott/whcli
metadata: {"clawdis":{"emoji":"🏠","requires":{"bins":["whcli"]},"install":[{"id":"brew","kind":"brew","formula":"pasogott/tap/whcli","bins":["whcli"],"label":"Install whcli (Homebrew)"},{"id":"source","kind":"shell","command":"git clone https://github.com/pasogott/whcli.git && cd whcli && uv sync","label":"Install from source (uv)"}]}}
---

# whcli - Willhaben CLI 🏠

通过命令行搜索和浏览 [willhaben.at](https://willhaben.at)，这是奥地利最大的分类广告交易平台。

## 安装

### 使用 Homebrew（推荐）

```bash
brew install pasogott/tap/whcli
```

### 从源代码安装（使用 uv）

```bash
git clone https://github.com/pasogott/whcli.git
cd whcli
uv sync
uv run whcli --help
```

## 命令

### 搜索

```bash
# Basic search
whcli search "iphone 15"

# With filters
whcli search "rtx 4090" --category grafikkarten --max-price 1500

# Location filter
whcli search "bicycle" -l Wien -n 20

# Only PayLivery (buyer protection)
whcli search "playstation" --paylivery

# Output as JSON for scripting
whcli search "laptop" --format json
```

**选项：**
| 选项 | 简写 | 描述 |
|--------|-------|-------------|
| `--category` | `-c` | 商品类别（例如：grafikkarten、smartphones 等） |
| `--min-price` | | 最低价格（欧元） |
| `--max-price` | | 最高价格（欧元） |
| `--condition` | | 商品状态（例如：neu、gebraucht、defekt、neuwertig） |
| `--location` | `-l` | 地点/区域筛选 |
| `--rows` | `-n` | 显示结果数量（默认：30） |
| `--page` | `-p` | 页码 |
| `--paylivery` | | 仅显示 PayLivery 广告 |
| `--format` | `-f` | 输出格式（table、json、csv） |

### 查看商品详情

```bash
# View listing by ID
whcli show 1993072190

# JSON output
whcli show 1993072190 --format json
```

### 卖家资料

```bash
# View seller profile and ratings
whcli seller 29159134
```

## 示例

```bash
# Find cheap iPhones in Vienna
whcli search "iphone" -l Wien --max-price 500

# Graphics cards under €1000
whcli search "grafikkarte" --category grafikkarten --max-price 1000

# New condition only
whcli search "ps5" --condition neu

# Export search results as CSV
whcli search "furniture" -l "1220" -n 50 --format csv > results.csv
```

## 常见商品类别：

- `grafikkarten` - 显卡
- `smartphones` - 手机
- `notebooks-laptops` - 笔记本电脑
- `spielkonsolen` - 游戏机
- `fahrraeder` - 自行车
- `moebel` - 家具

## 注意事项：

- ⚠️ `show` 命令存在 bug（正在修复中）
- 地点筛选功能可用，但可能会显示附近的地区信息
- 目前尚不支持 OAuth 登录（因此无法发送消息或查看卖家信息）

## 链接：

- **仓库：** https://github.com/pasogott/whcli
- **问题报告：** https://github.com/pasogott/whcli/issues
- **Homebrew 配置源：** https://github.com/pasogott/homebrew-tap