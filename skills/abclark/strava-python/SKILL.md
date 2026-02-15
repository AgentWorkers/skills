---
name: strava-python
version: 1.0.0
description: 使用 Python 和 stravalib 查询 Strava 的活动、统计数据以及锻炼数据，并提供交互式的设置指南
homepage: https://www.strava.com
metadata:
  openclaw:
    emoji: 🏃
    requires:
      bins:
        - python3
    install:
      - id: pip
        kind: pip
        package: stravalib
        label: Install stravalib (pip)
---

# Strava Python

通过 Python 和 stravalib，您可以使用 OpenClaw 查询您的 Strava 活动、统计数据以及锻炼数据。

**为什么选择这个技能？**  
这个技能结合了 Python 和 stravalib，并提供了一个交互式的设置向导（而非基于 curl 的技能，后者需要手动配置 JSON 数据）。

## 前提条件

- Python 3.7 或更高版本  
- `stravalib` 包  
- Strava API 凭据（免费）

## 设置步骤

1. **安装依赖项：**  
   ```bash
   pip install stravalib
   ```

2. **运行设置向导：**  
   ```bash
   python3 setup.py
   ```  
   此步骤将：  
   - 指导您创建一个 Strava API 应用程序  
   - 处理 OAuth 认证  
   - 将凭据保存到 `~/.strava_credentials.json` 文件中  

## 命令示例

- **查看最近的活动：**  
   ```bash
python3 strava_control.py recent
```

- **查看每周/每月的统计数据：**  
   ```bash
python3 strava_control.py stats
```

- **查看最近的一次锻炼：**  
   ```bash
python3 strava_control.py last
```

## 示例用法

您可以向 OpenClaw 发送以下请求：  
- “显示我最近的 Strava 活动”  
- “我这周的 Strava 统计数据是什么？”  
- “我最近的一次锻炼是什么？”  

## 相关文件

- `strava_control.py`：主要控制脚本  
- `setup.py`：交互式设置向导  
- `SKILL.md`：本文档文件  
- `~/.strava_credentials.json`：凭据文件（自动生成）

## 注意事项

- 需要拥有 Strava 账户（免费）  
- API 凭据属于个人隐私信息，切勿共享  
- 使用限制：15 分钟内最多 100 次请求，每天最多 1,000 次请求