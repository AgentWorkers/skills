---
name: midea_ac
description: **控制美的空调**  
当用户需要控制空调时，可以使用此技能。该技能支持开启/关闭空调、设置温度、调节风扇转速、切换运行模式等功能。
invocable: true
---

# 米家智能家居控制

通过 msmart 控制米家的空调设备。

## 使用方法

技能路径：`~/.openclaw/skills/midea_ac`

### 空调控制命令

```bash
# Navigate to skill directory
cd ~/.openclaw/skills/midea_ac

# Check status
python scripts/midea_ac.py bedroom status

# Turn on/off
python scripts/midea_ac.py bedroom on
python scripts/midea_ac.py bedroom off
python scripts/midea_ac.py bedroom toggle

# Set operation mode
python scripts/midea_ac.py bedroom --mode cool

# Set target temperature
python scripts/midea_ac.py bedroom --temperature 26

# Set fan speed
python scripts/midea_ac.py bedroom --fan_speed low

# Set aux hear mode
python scripts/midea_ac.py bedroom --aux_mode on

# Set multiple parameters at once
python scripts/midea_ac.py bedroom --mode heat --temperature 28 --fan_speed medium --aux_mode off
```

## 自然语言理解

当用户说出以下指令时，执行相应的命令：

| 用户指令 | 命令             |
|-----------|-------------------|
| 打开 <房间名称> 的空调 / 开启空调 | `scripts/midea_ac.py <房间名称> on` |
| 关闭 <房间名称> 的空调 | `scripts/midea_ac.py <房间名称> off` |
| 切换 <房间名称> 的空调模式 | `scripts/midea_ac.py <房间名称> toggle` |
| 提高温度 | 先检查空调状态，然后将温度提高 2-10 度 |
| 降低温度 | 先检查空调状态，然后将温度降低 2-10 度 |
| 最高风速 | 如果模式为制热：`scripts/midea_ac.py <房间名称> --temperature 30 --fan_speed max`；如果模式为制冷：`scripts/midea_ac.py <房间名称> --temperature 16 --fan_speed max` |
| 最低风速 | `scripts/midea_ac.py <房间名称> --fan_speed low` |
| 查看 <房间名称> 空调的状态 | `scripts/midea_ac.py <房间名称> status` |

## 执行前的准备

1. 导航到技能目录：`cd ~/.openclaw/skills/midea_ac`
2. 使用 uv 运行命令：`python scripts/midea_ac.py <房间名称> <命令>`
3. 执行命令后向用户报告结果