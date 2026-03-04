---
name: heliospice
description: 查询太阳系中航天器、行星、卫星和小行星的位置
---
# Heliospice

使用 SPICE 核函数查询航天器和行星的星历数据。

## 设置

```bash
pip install heliospice
```

## 可查询的内容

**航天器（36 种以上）**：Parker 太阳探测器、Solar Orbiter、Juno、Cassini、Voyager 1/2、Mars 2020、MRO、New Horizons、Europa Clipper、Psyche、BepiColombo、JUICE、Lucy、Galileo、Dawn、MESSENGER 等...

**行星**：水星、金星、地球、火星、木星、土星、天王星、海王星、冥王星

**卫星**：月球、土卫六（Titan）、欧罗巴（Europa）、木卫三（Ganymede）、木卫一（Io）、火卫一（Phobos）、火卫二（Deimos）等

**其他**：太阳、小行星、彗星、太阳系质心

## 工具

- `get_spacecraft_ephemeris` — 获取单个时间点或时间序列中的航天器位置（可选包含速度信息）
- `compute_distance` — 计算两个天体在指定时间范围内的距离（最小值/最大值/平均值、最近距离）
- `transform_coordinates` — 在不同的坐标系之间转换向量（RTN、J2000、ECLIPJ2000 等）
- `list_spice_missions` — 列出所有支持的航天器任务
- `list_coordinate_frames` — 列出可用的坐标系
- `manage_kernels` — 检查内核状态、下载、加载或清除内核缓存

## 示例

- “Parker 太阳探测器现在在哪里？”
- “地球距离太阳有多远？”
- “显示 Juno 在 2024 年 1 月的轨道轨迹”
- “火星在 2024 年什么时候最接近木星？”
- “将这个 RTN 向量转换为 J2000 坐标系”
- “当前月球的位置是多少？”