---
name: wow
description: "查询《魔兽世界》中的角色信息——包括M+评分、最佳通关记录、团队副本进度、装备等。该工具基于Raider.io（免费服务）开发，同时支持与Blizzard API及Warcraft Logs的集成，以便获取装备详情和团队副本数据解析结果。"
metadata:
  openclaw:
    emoji: "⚔️"
    requires:
      bins: ["curl", "jq"]
      env_optional: ["BLIZZARD_CLIENT_ID", "BLIZZARD_CLIENT_SECRET", "WCL_CLIENT_ID", "WCL_CLIENT_SECRET"]
    install:
      - id: symlink
        kind: shell
        command: "ln -sf $(pwd)/wow /usr/local/bin/wow"
        label: "Install wow CLI (symlink)"
---
# 《魔兽世界》

您可以查询《魔兽世界》中的角色信息、M+评分、团队副本进度等。

## 快速入门

```bash
# Full character profile — M+ score, best runs, raid progression
wow lookup <name>-<realm>
wow lookup azunazx-hyjal

# Quick one-line summary
wow search azunazx-hyjal

# Current M+ affixes
wow affixes

# Top M+ runs this season
wow top-runs
```

## 角色查询

主要命令用于查看角色的M+评分、最佳通关记录、团队副本进度以及装备信息。

```bash
# Default region is US
wow lookup <name>-<realm>

# EU character
wow lookup <name>-<realm> -r eu

# Include recent runs
wow lookup <name>-<realm> --recent

# Raw JSON output (for programmatic use)
wow lookup <name>-<realm> --raw
```

**输出内容包括：**
- 角色信息（名称、职业、专精方向、种族、阵营、服务器）
- 神话难度（Mythic）评分（总评分及各职业细分）
- 最佳M+通关记录（副本名称、关键关卡、用时、评分）
- 团队副本进度（普通/英雄/神话难度下的击杀数）
- 装备等级

## 快速搜索

提供简短的角色信息以便快速查找：

```bash
wow search azunazx-hyjal
# → Azunazx | Fire Mage | Hyjal [US] | Alliance | M+ Score: 4002.6
```

## M+词缀

```bash
wow affixes           # US affixes
wow affixes -r eu     # EU affixes
```

## 最佳M+通关记录

```bash
wow top-runs              # Top runs in US
wow top-runs -r eu        # Top runs in EU
wow top-runs --page 1     # Page through results
```

## 团队副本信息

```bash
wow raids           # List current raids and boss counts
```

## API来源

### Raider.io（已启用——无需授权）
- ✅ 角色资料、M+评分、最佳/近期通关记录
- ✅ 团队副本进度概览
- ✅ 当前使用的词缀
- ✅ 最佳M+通关记录/排名
- ✅ 装备等级
- 免费使用，无使用频率限制

### Blizzard API（可选——需要OAuth2授权）
- 军械库数据：详细装备信息、属性、成就
- M+评分（Blizzard自家的评分系统）
- 角色图片
- 需要`BLIZZARD_CLIENT_ID`和`BLIZZARD_CLIENT_SECRET`
- 注册地址：https://develop.battle.net/access/clients

```bash
# When configured:
wow armory <name>-<realm>
```

### Warcraft Logs API v2（可选——需要OAuth2授权）
- 团队副本数据解析及百分位数统计
- 每场战斗中的伤害/治疗量分布
- 不同难度下的角色排名
- 支持GraphQL API
- 需要`WCL_CLIENT_ID`和`WCL_CLIENT_SECRET`
- 注册地址：https://www.warcraftlogs.com/api/clients

## 配置

```bash
# Check what's configured
wow config
```

### 环境变量

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `WOW_REGION` | 否 | 默认区域：`us`、`eu`、`kr`、`tw`（默认：`us`） |
| `WOW_CONFIG` | 否 | 配置文件路径（默认：`~/.config/wow/config.env`） |
| `BLIZZARD_CLIENT_ID` | 否 | Blizzard API客户端ID |
| `BLIZZARD_CLIENT_SECRET` | 否 | Blizzard API客户端密钥 |
| `WCL_CLIENT_ID` | 否 | Warcraft Logs客户端ID |
| `WCL_CLIENT_SECRET` | 否 | Warcraft Logs客户端密钥 |

### 配置文件

创建`~/.config/wow/config.env`文件：

```bash
# Defaults
WOW_REGION=us

# Blizzard API (https://develop.battle.net/access/clients)
BLIZZARD_CLIENT_ID=your_id
BLIZZARD_CLIENT_SECRET=your_secret

# Warcraft Logs (https://www.warcraftlogs.com/api/clients)
WCL_CLIENT_ID=your_id
WCL_CLIENT_SECRET=your_secret
```

## 服务器区域

| 代码 | 区域 |
|------|--------|
| `us` | 美国及大洋洲 |
| `eu` | 欧洲 |
| `kr` | 韩国 |
| `tw` | 台湾 |

## 服务器名称

服务器名称使用连字符和下划线表示：
- `area-52`（而非“Area 52”）
- `moon-guard`（而非“Moon Guard”）
- 单词形式的服务器名称保持原样

命令行工具会自动将空格转换为连字符，并删除引号。

## 用户示例

当用户询问某个《魔兽世界》角色的相关信息时：

```bash
# "What's my M+ score?" (if you know their character)
wow lookup charactername-realmname

# "Look up this character on EU"
wow lookup charactername-realmname -r eu

# "What are the affixes this week?"
wow affixes

# "What are the top keys right now?"
wow top-runs

# Quick check
wow search charactername-realmname

# Get raw data for further processing
wow lookup charactername-realmname --raw | jq '.mythic_plus_scores_by_season[0].scores.all'
```