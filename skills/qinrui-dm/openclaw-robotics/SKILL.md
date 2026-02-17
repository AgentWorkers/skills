---
name: unitree-robot
description: "通过即时通讯（IM）平台控制移动机器人（四足、两足、轮式、飞行型）。支持 Unitree 机器人以及 Insight9 AI 立体相机。"
metadata: {
  "openclaw": {
    "emoji": "🤖",
    "requires": {
      "python": ">=3.8",
      "pip": ["numpy"]
    }
  }
}
---
# Unitree机器人控制器技能

通过即时通讯平台控制各种移动机器人。

## 支持的机器人

| 代码 | 型号 | 类型 |
|------|-------|------|
| `unitree_go1` | Unitree GO1 | 四足机器人 |
| `unitree_go2` | Unitree GO2 | 四足机器人 |
| `unitree_g1` | Unitree G1 | 双足/人形机器人 |
| `unitree_h1` | Unitree H1 | 双足/人形机器人 |

## 即将推出的机器人类型

| 代码 | 类型 |
|------|------|
| `wheeled_*` | 轮式机器人 |
| `drone_*` | 飞行机器人 |
| `surface_*` | 地面车辆 |

## 支持的传感器

| 代码 | 传感器 |
|------|--------|
| `insight9` | Looper Robotics AI立体相机（RGB-D） |

## 导航功能

- 集成了**TinyNav**技术，用于路径规划和避障（即将推出）

## 使用方法

```python
from unitree_robot_skill import initialize, execute

initialize(robot="unitree_go2", im="wecom")
execute("forward 1m")
execute("turn left 45")
```