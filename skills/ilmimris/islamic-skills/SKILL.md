---
name: islamic-companion
description: 统一的伊斯兰教实用工具，用于计算祷告时间、斋戒安排以及天课（Zakat）金额，支持使用共享的配置文件。
---
# Islamic Companion Skill

**一个集祈祷时间、斋戒安排和天课计算功能于一体的统一工具。**

该工具将多种伊斯兰相关功能整合到一个命令行界面（CLI）中，支持共享配置设置和高效的数据缓存。

## 主要功能

- **祈祷时间**：查询每日五次祈祷的时间（晨礼、晌礼、晡礼、昏礼、宵礼）。
- **斋戒**：查看斋戒开始的时刻（Imsak）和昏礼的时间。
- **天课**：根据当前市场价格计算黄金和白银的天课缴纳标准（Nisab）。
- **古兰经**：通过关键词搜索经文，或获取特定章节和经文的中文翻译。
- **日历**：为任意城市生成每月的祈祷时间表。
- **伊斯兰名言**：随机显示伊斯兰名言，或设置每日自动提醒功能。
- **日程安排**：生成用于提醒每日祈祷的OpenClaw cron任务。
- **缓存**：通过本地缓存每日结果来减少API调用次数。

## 使用方法

使用以下bash脚本运行该工具：

```bash
# Get today's prayer times
./bin/islamic-companion prayer --today

# Setup daily quote automation
./bin/islamic-companion quotes --setup

# Get a random quote
./bin/islamic-companion quotes --random

# Get monthly calendar (Example: Serang, Banten)
./bin/islamic-companion calendar --city "Serang" --month 2 --year 2026

# Sync prayer schedule to cron (generates commands)
./bin/islamic-companion prayer --sync

# Check fasting times (Imsak/Maghrib)
./bin/islamic-companion fasting --today

# Check Zakat Nisab values
./bin/islamic-companion zakat --nisab

# Search Quran for keyword
./bin/islamic-companion quran --search "sabar"

# Get specific Surah (e.g., Al-Fatihah)
./bin/islamic-companion quran --surah 1

# Get specific Ayah (e.g., Al-Baqarah:255)
./bin/islamic-companion quran --surah 2 --ayah 255
```

## 配置设置

编辑`skills/islamic-companion/config.json`文件以设置您的地理位置和计算方法。
注意：`config.bash`文件会根据`config.json`自动生成，以提高程序运行效率。

```json
{
  "location": {
    "latitude": -6.2088,
    "longitude": 106.8456,
    "name": "Jakarta"
  },
  "calculation": {
    "method": 20,
    "school": 0
  },
  "zakat": {
    "currency": "IDR",
    "gold_gram_threshold": 85,
    "api_key": ""
  },
  "quran_language": "id"
}
```

### 计算方法
- **方法20**：印度尼西亚宗教事务部（Kemenag RI）的标准计算方法
- **学派0**：沙斐仪派（Shafi）、马立克派（Maliki）、罕百里派（Hanbali）的标准计算方法
- **学派1**：哈乃斐派（Hanafi）的计算方法

## 用户指令与对应命令

| 用户指令 | 执行的命令 |
| :--- | :--- |
| "获取祈祷时间" | `./bin/islamic-companion prayer --today` |
| "显示[城市]的日历" | `./bin/islamic-companion calendar --city [城市]` |
| "设置每日伊斯兰名言提醒" | `./bin/islamic-companion quotes --setup` |
| "随机显示一条伊斯兰名言" | `./bin/islamic-companion quotes --random` |
| "同步祈祷时间表" | `./bin/islamic-companion prayer --sync` |
| "现在是什么时候（Imsak）?" | `./bin/islamic-companion fasting --today` |
| "查询天课缴纳标准" | `./bin/islamic-companion zakat --nisab` |
| "在古兰经中搜索[关键词]" | `./bin/islamic-companion quran --search "[关键词]"` |
| "阅读[章节名称/编号]" | `./bin/islamic-companion quran --surah [章节编号]` |
| "阅读[章节编号]第[经文编号]节" | `./bin/islamic-companion quran --surah [章节编号] --ayah [经文编号]` |

## 所需依赖库

- **系统要求**：`bash`、`curl`、`jq`（强烈推荐）
- **部分功能可能需要Python**：`python3`、`requests`（通过`pip install -r requirements.txt`安装）

## 安全性与隐私注意事项

> [!警告]
> **API密钥**：天课计算功能需要使用API密钥。您可以选择将其存储在`config.json`文件中（安全性较低），或将其设置为环境变量`ZAKAT_API_KEY`（推荐这种方式）。

> [!重要提示]
> **自动化设置**：`--sync`和`--setup`命令会生成用于自动执行祈祷提醒的cron任务。在将它们添加到系统crontab之前，请务必仔细检查命令的输出内容。

## 安装步骤

1. 克隆代码仓库或下载该工具。
2. 安装Python相关依赖库：
   ```bash
   pip install -r requirements.txt
   ```
3. 确保系统已安装`curl`。建议安装`jq`以提升JSON解析的效率和准确性。

## 使用示例

使用以下bash脚本运行该工具，脚本会自动处理配置加载和环境设置：

```bash
# 获取今天的祈祷时间（使用HTTPS）
./bin/islamic-companion prayer --today
```