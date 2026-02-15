---
name: seasonal-planting-guide
description: **园艺季节性种植日历**  
帮助您了解在您的种植区域每月应种植哪些植物。适用于规划花园、查看种植时间表或寻找适合当前季节的植物。  

**安全提示：**  
文件导出仅限于受保护的目录中，确保数据安全。  
非常适合家庭园艺爱好者、小型农场主以及任何希望打造高效花园的人士使用。
---

# 季节性种植指南

根据您所在地区的具体种植时间表来规划您的花园。

## 快速入门

### 了解本月应种植的植物
```bash
seasonal_planting.py now --zone "8a"
```

### 获取某个月的种植日历
```bash
seasonal_planting.py month --month "april" --zone "6b"
```

### 获取全年种植日历
```bash
seasonal_planting.py year --zone "7a"
```

### 搜索植物
```bash
seasonal_planting.py search "tomato"
```

### 查看植物详情
```bash
seasonal_planting.py show "tomato"
```

### 将自定义植物添加到日历中
```bash
seasonal_planting.py add "tomato" --planting "april,may" --zone "6a,6b,7a,7b,8a,8b"
```

## 使用建议

### 面向新园艺爱好者
```bash
# Check what to plant right now
seasonal_planting.py now --zone "7a"

# Get full calendar for your zone
seasonal_planting.py year --zone "7a"

# Learn about specific plants
seasonal_planting.py show "lettuce"
seasonal_planting.py show "tomato"
```

### 面向有经验的园艺爱好者（提前规划）
```bash
# Check what to plant next month
seasonal_planting.py month --month "may" --zone "7a"

# Plan succession planting
seasonal_planting.py month --month "april" --zone "7a"
seasonal_planting.py month --month "june" --zone "7a"

# Add your local varieties
seasonal_planting.py add "local-corn" --planting "may,june" --zone "7a" --notes "Silver Queen variety"
```

### 面向小型农户
```bash
# Get full production schedule
seasonal_planting.py year --zone "6b" > planting-schedule.txt

# Plan staggered planting
seasonal_planting.py month --month "march" --zone "6b"  # Early crops
seasonal_planting.py month --month "april" --zone "6b"  # Main crops
seasonal_planting.py month --month "may" --zone "6b"   # Late crops

# Export calendar for team
seasonal_planting.py year --zone "6b" --export "~/farm-calendar.md"
```

### 面向容器/室内园艺爱好者
```bash
# Search for container-friendly plants
seasonal_planting.py search "lettuce"
seasonal_planting.py search "herbs"

# Check planting windows
seasonal_planting.py show "basil"
```

## 种植区域

了解您的 **USDA 耐寒区** 有助于正确规划种植：

| 耐寒区 | 温度范围 | 常见植物 |
|------|-------------|----------------|
| 3-4 | 非常寒冷 | 羽衣甘蓝、豌豆、生菜、胡萝卜 |
| 5-6 | 寒冷 | 番茄、辣椒、豆类、南瓜 |
| 7-8 | 温和 | 番茄、辣椒、茄子、玉米 |
| 9-10 | 温暖 | 全年均可种植，适合热带植物 |
| 11+ | 热带气候 | 所有植物均可全年种植 |

**如何查找您的耐寒区：**
- 在网上搜索 “USDA 耐寒区 [您的城市]”
- 大多数园艺资源都会提供耐寒区信息
- 如果不确定，可以参考相邻的耐寒区

## 植物分类

### 冷季作物
在春季（3月至5月）或秋季（8月至10月）种植：
- 生菜、菠菜、羽衣甘蓝、芝麻菜
- 豌豆、萝卜、胡萝卜
- 西兰花、花椰菜、布鲁塞尔芽菜

### 温季作物
在最后一次霜冻过后种植（5月至6月）：
- 番茄、辣椒、茄子
- 豆类、玉米、南瓜
- 黄瓜、甜瓜、西葫芦

### 草本植物（全年或季节性）
- 多年生植物：迷迭香、百里香、牛至、鼠尾草、细香葱
- 一年生植物：罗勒、香菜、莳萝、欧芹

### 根茎类蔬菜
- 早春种植：萝卜、芜菁
- 中季种植：胡萝卜、甜菜、欧防风
- 晚季种植：大蒜（秋季种植）、洋葱

## 实例

### 春季花园规划
```bash
# Zone 6b - April
seasonal_planting.py month --month "april" --zone "6b"
# Output: tomatoes, peppers, beans, squash, cucumbers

# Zone 8a - April
seasonal_planting.py month --month "april" --zone "8a"
# Output: tomatoes, peppers, eggplant, corn, okra (earlier start)

# Plan succession planting
seasonal_planting.py month --month "april" --zone "6b"
seasonal_planting.py month --month "may" --zone "6b"
seasonal_planting.py month --month "june" --zone "6b"
```

### 秋季花园规划
```bash
# Zone 7a - August (fall crops)
seasonal_planting.py month --month "august" --zone "7a"
# Output: lettuce, spinach, kale, radishes, peas

# Zone 5a - September (fall crops)
seasonal_planting.py month --month "september" --zone "5a"
# Output: lettuce, spinach, kale, garlic (for overwintering)
```

### 全年种植规划
```bash
# Get full calendar for your zone
seasonal_planting.py year --zone "7a"

# Export for reference
seasonal_planting.py year --zone "7a" --export "~/garden-calendar-2026.md"
```

### 结合本地知识
```bash
# Add your region-specific advice
seasonal_planting.py add "corn" --planting "may,june" --zone "7a" \
  --notes "Silver Queen variety best, plant in blocks for pollination"

# Add heirloom varieties
seasonal_planting.py add "heirloom-tomato" --planting "april,may" --zone "6b,7a" \
  --notes "Brandywine, Cherokee Purple - start indoors 6 weeks before last frost"
```

## 搜索功能

- 按名称或类别查找植物
- 查看每种植物的种植时间
- 获取针对特定耐寒区的种植建议
- 查找相似植物（例如，输入 “番茄” 可找到所有番茄品种）

## 安全性

### 路径验证
`export` 函数会验证输出路径，以防止恶意写入：
- ✅ 允许的路径：`~/.openclaw/workspace/`、`/tmp/` 和用户主目录
- ❌ 禁止的路径：系统路径（`/etc/`、`/usr/`、`/var/` 等）
- ❌ 禁止的文件：敏感的配置文件（`~/.bashrc`、`~/.ssh` 等）

## 数据存储

- 种植日历存储在：`~/.openclaw/workspace/planting_calendar.json`
- 自定义植物信息会与内置数据库一起记录
- 数据采用 JSON 格式，便于备份或扩展
- 每种植物都有针对特定耐寒区的种植建议

## 最佳实践

1. **了解您的耐寒区** —— 这决定了最佳的种植时间
2. **关注最后一次霜冻日期** —— 耐寒区只是一个参考，当地天气也很重要
3. **规划轮作种植** —— 分批种植以确保持续收获
4. **使用植物管理工具** —— 结合植物管理工具实现全面花园管理
5. **结合本地知识** —— 根据当地品种调整日历
6. **导出日历以备参考** —— 将种植计划保存下来方便查阅

## 伴生种植技巧

通过 **伴生种植** 可获得更好的种植效果：

| 植物 | 适合搭配的植物 | 应避免搭配的植物 |
|-------|----------------|--------|
| 番茄 | 罗勒、胡萝卜、洋葱 | 卷心菜、土豆 |
| 生菜 | 胡萝卜、萝卜、草莓 | 欧芹 |
| 豆类 | 玉米、胡萝卜、黄瓜 | 洋葱、大蒜 |
| 辣椒 | 罗勒、洋葱、胡萝卜 | 茴香、苤蓝 |

## 相关技能

- **植物管理工具** —— 用于管理单株植物、制定护理计划和跟踪收获情况
- **花园布局规划工具** —— 用于设计花园布局

结合使用这些工具，实现全面的花园管理！