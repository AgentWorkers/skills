---
name: plant-tracker
description: 专为园艺爱好者设计的个人植物和花园管理工具。您可以跟踪植物的生长情况，设置养护计划，并监控植物的生长进度。无论您需要管理花园、记录浇水/施肥的时间表，还是维护植物库存，这款工具都能为您提供帮助。安全性方面：文件导出仅限于安全的目录（工作区、个人文件夹或 /tmp）。非常适合家庭园艺爱好者、室内植物爱好者，以及任何自己种植食物的人使用。
---

# 植物追踪器

通过结构化的追踪和护理计划来管理您的植物和花园。

## 快速入门

### 向您的收藏中添加植物
```bash
plant_tracker.py add "<plant_name>" --species "<species>" --location "<location>"
```

### 列出所有植物
```bash
plant_tracker.py list
```

### 查看植物详情
```bash
plant_tracker.py show "<plant_name>"
```

### 记录护理信息（浇水、施肥等）
```bash
plant_tracker.py care "<plant_name>" --action "<action>" [notes]
```

### 搜索植物
```bash
plant_tracker.py search "<query>"
```

### 导出植物数据
```bash
plant_tracker.py export "<output_file>"
```

## 使用场景

### 室内植物管理
为室内植物制定护理计划：
```bash
# Add your plants
plant_tracker.py add "Snake Plant" --species "Sansevieria trifasciata" --location "Living Room - North Window"
plant_tracker.py add "Monstera" --species "Monstera deliciosa" --location "Bedroom - East Window"
plant_tracker.py add "Pothos" --species "Epipremnum aureum" --location "Bathroom"

# Record watering
plant_tracker.py care "Snake Plant" --action "water" "Watered thoroughly, let drain"
plant_tracker.py care "Monstera" --action "water" "Watered until runoff, humidity 60%"

# Check what needs attention
plant_tracker.py list
```

### 蔬菜园管理
记录可食用植物的种植日期和收获情况：
```bash
# Add vegetables
plant_tracker.py add "Tomatoes" --species "Solanum lycopersicum" --location "Backyard - Bed 3" --planted "2026-04-15"
plant_tracker.py add "Basil" --species "Ocimum basilicum" --location "Backyard - Container" --planted "2026-05-01"
plant_tracker.py add "Lettuce" --species "Lactuca sativa" --location "Front Yard - Raised Bed" --planted "2026-04-20"

# Record care and harvests
plant_tracker.py care "Tomatoes" --action "water" "Deep watering, weather hot"
plant_tracker.py care "Tomatoes" --action "fertilize" "Added organic tomato fertilizer"
plant_tracker.py care "Basil" --action "harvest" "Harvested 20 leaves for pesto"

# See what's ready to harvest
plant_tracker.py search "harvest"
```

### 花园管理
追踪观赏植物及其季节性护理需求：
```bash
# Add flowers
plant_tracker.py add "Roses" --species "Rosa" --location "Front Garden" --planted "2025-03-10"
plant_tracker.py add "Lavender" --species "Lavandula" --location "Side Garden" --planted "2025-04-20"
plant_tracker.py add "Sunflowers" --species "Helianthus annuus" --location "Backyard" --planted "2026-05-15"

# Record seasonal care
plant_tracker.py care "Roses" --action "prune" "Spring pruning, removed dead wood"
plant_tracker.py care "Lavender" --action "prune" "Post-bloom pruning to encourage new growth"
plant_tracker.py care "Sunflowers" --action "harvest" "Harvested seeds for next year"
```

### 多个花园管理
在不同地点跟踪植物：
```bash
# Indoor plants
plant_tracker.py add "Peace Lily" --location "Living Room"
plant_tracker.py add "Fiddle Leaf Fig" --location "Bedroom"

# Outdoor beds
plant_tracker.py add "Peppers" --location "Backyard - Bed 1"
plant_tracker.py add "Carrots" --location "Backyard - Bed 2"

# Community garden plot
plant_tracker.py add "Squash" --location "Community Plot A - Row 3"

# Filter by location
plant_tracker.py search "Bedroom"
plant_tracker.py search "Backyard"
```

## 操作参考

### 可用的护理操作
- `water` - 浇水
- `fertilize` - 施肥/添加有机肥料
- `prune` - 修剪
- `harvest` - 收获果实/蔬菜/草药
- `repot` - 换盆
- `plant` - 初始种植或移植
- `pesticide` - 治虫
- `inspect` - 检查植物健康状况
- `note` - 记录观察结果

## 安全性

### 路径验证
`export` 函数会验证输出路径，以防止恶意写入：
- ✅ 允许的路径：`~/.openclaw/workspace/`, `/tmp/` 和用户主目录
- ❌ 禁止的路径：系统路径（`/etc/`, `/usr/`, `/var/` 等）
- ❌ 禁止的路径：敏感的配置文件（`~/.bashrc`, `~/.ssh` 等）

## 数据存储

- 所有植物数据存储在：`~/.openclaw/workspace/plants_db.json`
- 每株植物记录的信息包括：名称、品种、位置、种植日期、护理历史
- 护理历史包括：操作类型、时间戳、备注
- JSON 格式便于数据备份或迁移

## 搜索功能

- 全文不区分大小写地搜索所有植物信息
- 可匹配植物名称、品种、位置和护理备注
- 显示包含护理历史的完整植物详情
- 非常适合查找特定植物或护理记录

## 示例

### 新花园设置
```bash
# Plan and track your new garden
plant_tracker.py add "Tomatoes - Beefsteak" --species "Solanum lycopersicum" --location "Backyard - Bed 1" --planted "2026-04-15"
plant_tracker.py add "Tomatoes - Cherry" --species "Solanum lycopersicum" --location "Backyard - Bed 1" --planted "2026-04-15"
plant_tracker.py add "Bell Peppers" --species "Capsicum annuum" --location "Backyard - Bed 2" --planted "2026-04-20"
plant_tracker.py add "Cucumbers" --species "Cucumis sativus" --location "Trellis - South Wall" --planted "2026-05-01"

# Export your garden plan
plant_tracker.py export "~/garden-planting-plan.md"
```

### 每周花园维护
```bash
# Check your garden
plant_tracker.py list

# Record this week's care
plant_tracker.py care "Tomatoes - Beefsteak" --action "water" "Deep watering, mulch added"
plant_tracker.py care "Bell Peppers" --action "fertilize" "Added compost, plants look healthy"
plant_tracker.py care "Cucumbers" --action "inspect" "Found aphids on some leaves, treated with neem oil"
```

### 跟踪植物生长和产量
```bash
# Record harvests
plant_tracker.py care "Tomatoes - Cherry" --action "harvest" "Harvested 2 cups, sweet and juicy"
plant_tracker.py care "Bell Peppers" --action "harvest" "Harvested 3 peppers, good size"
plant_tracker.py care "Cucumbers" --action "harvest" "Harvested 5 cucumbers, about 15cm each"

# Review harvest history
plant_tracker.py search "harvest"
```

## 最佳实践

1. **使用描述性名称** - 例如“Tomatoes - Beefsteak”而非“Tomatoes”
2. **记录种植日期** - 有助于追踪植物的生长周期和收获时间
3. **明确指定位置** - 例如“Backyard - Bed 1”而非“Garden”
4. **定期记录护理情况** - 为将来参考建立历史记录
5. **记录观察结果** - 如病虫害、开花情况、果实产量等
6. **定期导出数据** - 备份植物信息