---
name: garden-layout-planner
description: **园艺设计与布局规划工具**  
专为园艺爱好者设计，帮助您规划花园布局，包括作物搭配种植、植株间距以及光照需求。适用于新花园的建设、轮作计划制定或空间优化。  

**安全保障**：文件导出仅限于安全目录，确保数据安全。  
**适用人群**：非常适合家庭园艺爱好者、小型农场主以及任何希望最大化利用种植空间的人士。
---

# 花园布局规划器

使用智能规划工具来设计您的花园，包括伴生种植、植物间距和光照需求等方面的规划。

## 快速入门

### 向布局中添加花坛
```bash
garden_layout.py add-bed "<bed_name>" --width <feet> --length <feet> --sun "full/partial/shade"
```

### 向花坛中添加植物
```bash
garden_layout.py add-plant "<bed_name>" "<plant>" --row <row> --col <col>
```

### 获取伴生种植建议
```bash
garden_layout.py companions "<plant>"
```

### 获取植物间距要求
```bash
garden_layout.py spacing "<plant>"
```

### 显示完整的花园布局
```bash
garden_layout.py layout
```

### 将布局导出为Markdown格式
```bash
garden_layout.py export "<output_file>"
```

## 使用场景

### 新花园的设置
```bash
# Define your beds
garden_layout.py add-bed "Bed 1" --width 4 --length 8 --sun "full"
garden_layout.py add-bed "Bed 2" --width 3 --length 6 --sun "partial"

# Check companion planting
garden_layout.py companions "tomato"  # Best with basil, carrots, onions
garden_layout.py companions "cucumber"   # Best with beans, corn, peas

# Add plants with proper spacing
garden_layout.py add-plant "Bed 1" "tomato" --row 1 --col 1
garden_layout.py add-plant "Bed 1" "basil" --row 1 --col 3  # Companion!
garden_layout.py add-plant "Bed 2" "beans" --row 1 --col 1
garden_layout.py add-plant "Bed 2" "corn" --row 2 --col 1  # Companion!

# Review your layout
garden_layout.py layout
```

### 优化伴生种植
```bash
# Check what grows well together
garden_layout.py companions "carrots"  # Good with tomatoes, onions, lettuce
garden_layout.py companions "onions"   # Good with carrots, tomatoes, beets

# Avoid bad combinations
garden_layout.py incompatible "potatoes"  # Avoid with tomatoes, cucumbers
```

### 最大化小空间利用率
```bash
# Use vertical growing for space efficiency
garden_layout.py add-bed "Trellis" --width 1 --length 6 --sun "full"
garden_layout.py add-plant "Trellis" "cucumber" --row 1 --col 1
garden_layout.py add-plant "Trellis" "peas" --row 2 --col 1

# Intensive planting with succession
garden_layout.py add-bed "Intensive Bed" --width 3 --length 4 --sun "full"
garden_layout.py add-plant "Intensive Bed" "lettuce" --row 1 --col 1
garden_layout.py add-plant "Intensive Bed" "radishes" --row 1 --col 2  # Fast harvest
```

### 作物轮作规划
```bash
# Track what you planted each year
garden_layout.py add-season "2026"  # Starts fresh layout
garden_layout.py add-plant "Bed 1" "tomatoes" --row 1 --col 1
garden_layout.py add-plant "Bed 2" "beans" --row 1 --col 1

# Next year, change families
garden_layout.py add-season "2027"  # New layout
garden_layout.py add-plant "Bed 1" "carrots" --row 1 --col 1  # Different family
garden_layout.py add-plant "Bed 2" "corn" --row 1 --col 1      # Different family
```

## 伴生种植指南

### 最佳搭配（适合一起种植的植物）
| 植物 | 适合与...一起种植 | 原因 |
|-------|-----------|------|
| 番茄 | 罗勒、胡萝卜、洋葱、万寿菊 | 罗勒能提升番茄的风味，胡萝卜能驱虫 |
| 黄瓜 | 豆类、玉米、豌豆、萝卜 | 豆类能固定氮肥，玉米能为其他植物提供支撑 |
| 生菜 | 胡萝卜、萝卜、洋葱 | 萝卜可以标记种植行，胡萝卜有助于松土 |
| 辣椒 | 罗勒、洋葱、胡萝卜 | 罗勒能驱赶蚜虫 |
| 豆类 | 玉米、土豆、黄瓜 | 豆类能固定氮肥，有利于其他植物生长 |
| 胡萝卜 | 番茄、洋葱、生菜 | 洋葱能驱赶胡萝卜蝇 |
| 玉米 | 豆类、南瓜、黄瓜 | 这是“三姐妹”种植法 |
| 南瓜 | 玉米、豆类、萝卜 | 豆类能驱赶南瓜甲虫 |

### 不适合一起种植的植物（应避免搭配）
| 植物 | 应避免与...一起种植 | 原因 |
|-------|-----------|------|
| 番茄 | 土豆、黄瓜、茴香 | 这些植物容易感染相同的病虫害 |
| 豆类 | 洋葱、大蒜 | 大蒜会抑制豆类的生长 |
| 胡萝卜 | 莳萝、欧芹 | 莳萝会吸引胡萝卜蝇 |
| 黄瓜 | 土豆、鼠尾草 | 土豆会与黄瓜争夺空间 |
| 洋葱 | 豆类、豌豆 | 洋葱会抑制豆类的生长 |

## 植物间距要求

### 小型植物（间距6-12英寸）
- 生菜：6-8英寸
- 菠菜：4-6英寸
- 萝卜：2-3英寸
- 洋葱：4-6英寸
- 胡萝卜：2-3英寸

### 中型植物（间距12-24英寸）
- 辣椒：18-24英寸
- 茄子：18-24英寸
- 灌木状豆类：12-18英寸
- 甘蓝：18-24英寸

### 大型植物（间距24英寸以上）
- 番茄：24-36英寸
- 南瓜：24-48英寸（或使用棚架）
- 玉米：12-18英寸（需要间隔种植以便授粉）
- 土豆：12-15英寸

## 光照需求

### 全日照（每天6-8小时以上）
- 番茄、辣椒、茄子、南瓜、玉米、豆类、黄瓜

### 半日照（每天4-6小时）
- 生菜、菠菜、羽衣甘蓝、豌豆、胡萝卜、甜菜

### 阴凉环境（每天光照少于4小时）
- 一些叶类蔬菜和香草（如薄荷、细香葱）

## 实例

### “三姐妹”种植法（传统种植方式）
```bash
# Classic Native American companion planting
garden_layout.py add-bed "Three Sisters" --width 8 --length 8 --sun "full"

# Plant corn in center (support)
garden_layout.py add-plant "Three Sisters" "corn" --row 4 --col 4

# Plant beans around corn (nitrogen)
garden_layout.py add-plant "Three Sisters" "beans" --row 4 --col 2
garden_layout.py add-plant "Three Sisters" "beans" --row 4 --col 6

# Plant squash at edges (ground cover)
garden_layout.py add-plant "Three Sisters" "squash" --row 1 --col 1
garden_layout.py add-plant "Three Sisters" "squash" --row 1 --col 8
garden_layout.py add-plant "Three Sisters" "squash" --row 8 --col 1
garden_layout.py add-plant "Three Sisters" "squash" --row 8 --col 8
```

### 番茄-罗勒种植组合
```bash
# Simple companion planting
garden_layout.py add-bed "Tomato Patch" --width 4 --length 6 --sun "full"

garden_layout.py add-plant "Tomato Patch" "tomato" --row 1 --col 1
garden_layout.py add-plant "Tomato Patch" "basil" --row 1 --col 3  # Companion!
garden_layout.py add-plant "Tomato Patch" "carrots" --row 2 --col 1  # Under tomatoes
garden_layout.py add-plant "Tomato Patch" "carrots" --row 2 --col 3
```

### 小空间混合种植方案
```bash
# Intensive planting
garden_layout.py add-bed "Small Space" --width 3 --length 4 --sun "partial"

garden_layout.py add-plant "Small Space" "lettuce" --row 1 --col 1
garden_layout.py add-plant "Small Space" "radishes" --row 1 --col 2  # Fast, marks row
garden_layout.py add-plant "Small Space" "lettuce" --row 1 --col 3

garden_layout.py add-plant "Small Space" "spinach" --row 2 --col 1
garden_layout.py add-plant "Small Space" "onions" --row 2 --col 2
garden_layout.py add-plant "Small Space" "spinach" --row 2 --col 3
```

## 搜索功能

- 查找适合伴生种植的植物组合
- 获取任何植物的间距要求
- 按植物名称搜索布局方案
- 按光照需求筛选布局

## 安全性

### 路径验证
`export`函数会验证输出路径，防止恶意写入：
- ✅ 允许的路径：`~/.openclaw/workspace/`、`/tmp/` 和用户主目录
- ❌ 禁止的路径：系统路径（`/etc/`、`/usr/`、`/var/` 等）
- ❌ 禁止的路径：敏感的配置文件（`~/.bashrc`、`~/.ssh` 等）

## 数据存储

- 花园布局数据存储在：`~/.openclaw/workspace/garden_layout_db.json`
- 每个花坛的记录包括：尺寸、光照条件以及植物的具体位置
- 内置了包含50多种植物搭配关系的伴生种植数据库
- 数据采用JSON格式，便于备份或迁移

## 最佳实践

1. **种植前先规划** - 使用布局规划器来预览种植方案
2. **采用伴生种植** - 将适合的植物种在一起
3. **注意植物间距** - 避免过度拥挤，植物需要足够的生长空间
4. **关注光照条件** - 不同植物对光照的需求不同
5. **进行轮作规划** - 记录每年种植的作物
6. **导出布局方案** - 保留花园规划的备份

## 相关工具

- **植物追踪器** - 可追踪每株植物的生长情况和收获时间
- **季节性种植指南** - 根据您的种植区域推荐适合种植的植物

结合使用这些工具，实现全面的花园管理！